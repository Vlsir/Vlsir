"""
Xyce Implementation of `vsp.Sim`
"""

# Std-Lib Imports
import subprocess, random, shutil, csv
from glob import glob
from os import PathLike
from typing import List, Tuple, IO, Dict, Awaitable, Union

import numpy as np
import pandas as pd

# Local/ Project Dependencies
import vlsir.spice_pb2 as vsp
from ..netlist import netlist, XyceNetlister
from .base import Sim
from .sim_data import (
    TranResult,
    OpResult,
    SimResult,
    AcResult,
    DcResult,
    AnalysisResult,
)
from .spice import (
    ResultFormat,
    SupportedSimulators,
    sim,
    sim_async,  # Not directly used here, but "re-exported"
)


# Module-level configuration. Over-writeable by sufficiently motivated users.
XYCE_EXECUTABLE = "Xyce"  # The simulator executable invoked. If over-ridden, likely for sake of a specific path or version.


def available() -> bool:
    return XyceSim.available()


class XyceSim(Sim):
    """
    State and execution logic for a Xyce-call to `vsp.Sim`.

    Xyce can, in principle, run multiple analyses per process,
    but seems to commonly confuse outputs or disallow saving them
    from multiple analyses.

    Execution therefore instead occurs one Xyce-process per analysis.
    Results from each analysis-process are collated into a single `SimResult`.
    """

    @staticmethod
    def available() -> bool:
        """Boolean indication of whether the current running environment includes the simulator executable on its path."""
        # FIXME: add an attempt to execute it, get the version string etc, like Spectre and NgSpice do.
        if shutil.which(XYCE_EXECUTABLE) is None:
            return False
        try:
            # And if it's set, check that we can get its version without croaking.
            subprocess.run(
                f"{XYCE_EXECUTABLE} -v",  # Get the version,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
        except Exception:
            # Indicate "not available" for any Exception. Usually this will be a `subprocess.CalledProcessError`.
            return False
        return True  # Otherwise, installation looks good.

    @classmethod
    def enum(cls) -> SupportedSimulators:
        return SupportedSimulators.XYCE

    async def run(self) -> Awaitable[SimResult]:
        """Run the specified `SimInput` in directory `self.rundir`,
        returning its results."""

        netlist_file = self.open("dut", "w")
        netlist(pkg=self.inp.pkg, dest=netlist_file, fmt="xyce")

        # Write the top-level instance
        netlist_file.write(
            f"xtop 0 {XyceNetlister.get_module_name(self.top)} ; Top-Level DUT \n\n"
        )

        if self.inp.opts:
            raise NotImplementedError(f"SimInput Options")

        # Write each control element
        self.write_control_elements(netlist_file)

        # Flush the netlist to disk before handing off to analyses
        netlist_file.flush()

        # Run each analysis in the input
        results = SimResult()
        for an in self.inp.an:
            an_results = await self.analysis(an)
            results.an.append(an_results)

        return results

    def write_control_elements(self, netlist_file: IO) -> None:
        for ctrl in self.inp.ctrls:
            inner = ctrl.WhichOneof("ctrl")
            if inner == "include":
                netlist_file.write(f".include '{ctrl.include.path}' \n")
            elif inner == "lib":
                netlist_file.write(f".lib {ctrl.lib.path} {ctrl.lib.section} \n")
            elif inner == "param":
                line = f".param {ctrl.param.name}={XyceNetlister.get_param_value(ctrl.param.value)} \n"
                netlist_file.write(line)
            elif inner == "meas":
                line = f".meas {ctrl.meas.analysis_type} {ctrl.meas.name} {ctrl.meas.expr} \n"
                netlist_file.write(line)
            elif inner == "literal":
                netlist_file.write(ctrl.literal + "\n")
            elif inner in ("save"):
                raise NotImplementedError(
                    f"Unimplemented control card {ctrl} for {self}"
                )  # FIXME!
            else:
                raise RuntimeError(f"Unknown control type: {inner}")

    def analysis(self, an: vsp.Analysis) -> Awaitable[AnalysisResult]:
        """Execute a `vsp.Analysis`, returning its `AnalysisResult`.
        Note that while this method is not explicitly `async`,
        its inner methods `dc`, `ac`, `tran`, etc, all are,
        and hence return an `Awaitable` future."""

        # `Analysis` is a Union (protobuf `oneof`) of the analysis-types.
        # Unwrap it, and dispatch based on the type.
        inner = an.WhichOneof("an")

        if inner == "op":
            return self.op(an.op)
        if inner == "dc":
            return self.dc(an.dc)
        if inner == "ac":
            return self.ac(an.ac)
        if inner == "tran":
            return self.tran(an.tran)
        if inner in ("sweep", "monte", "custom"):
            raise NotImplementedError(f"{inner} not implemented")
        raise RuntimeError(f"Unknown analysis type: {inner}")

    async def ac(self, an: vsp.AcInput) -> Awaitable[vsp.AcResult]:
        """Run an AC analysis."""

        # Unpack the `AcInput`
        if not an.analysis_name:
            raise RuntimeError(f"Analysis name required for {an}")
        analysis_name = an.analysis_name
        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        # Copy and append to the existing DUT netlist
        netlist = self.copy_dut_netlist(f"{analysis_name}.sp")

        # Write the analysis command
        npts = an.npts
        fstart = an.fstart
        fstop = an.fstop
        netlist.write(f".ac DEC {npts} {fstart} {fstop} \n\n")

        # FIXME: always saving everything, no matter what
        # Note `csv` output-formatting is encoded here
        netlist.write(".print ac format=csv v(*) i(*) \n\n")

        # And don't forget - the thing SPICE can't live without - END!
        netlist.write(".end \n\n")
        netlist.flush()

        # Do the real work, running the simulation
        await self.run_xyce_process(analysis_name)

        # Read the results from CSV
        with self.open(f"{analysis_name}.sp.FD.csv", "r") as csv_handle:
            csv_data = read_csv(csv_handle)

        # Separate Frequency vector
        freq: np.ndarray = csv_data.pop("FREQ")
        data: Dict[str, np.ndarray] = {}

        # Pull together separate real/imaginary parts into complex numbers
        keys = list(csv_data.keys())
        for re, im in zip(keys[::2], keys[1::2]):
            # Check that node-names match, or fail.
            # Peel out "Re(" and "Im(" from the beginning, and a trailing ")" from the end.
            if re[3:-1] != im[3:-1]:
                raise RuntimeError(f"Unmatched complex number: {re}, {im}")
            name = re[3:-1]
            data[name] = np.array(
                [complex(r, i) for r, i in zip(csv_data[re], csv_data[im])]
            )

        # Parse any scalar measurement results
        measurements = self.parse_measurements(analysis_name)

        # And arrange them in an `AcResult`
        return AcResult(
            analysis_name=an.analysis_name,
            freq=freq,
            data=data,
            measurements=measurements,
        )

    async def dc(self, an: vsp.DcInput) -> Awaitable[DcResult]:
        """Run a DC analysis."""

        # Unpack the `DcInput`
        if not an.analysis_name:
            raise RuntimeError(f"Analysis name required for {an}")
        analysis_name = an.analysis_name
        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        # Copy and append to the existing DUT netlist
        netlist = self.copy_dut_netlist(f"{analysis_name}.sp")

        # Write the analysis command
        param = an.indep_name
        ## Interpret the sweep
        sweep_type = an.sweep.WhichOneof("tp")
        if sweep_type == "linear":
            sweep = an.sweep.linear
            netlist.write(
                f".dc LIN {param} {sweep.start} {sweep.stop} {sweep.step}\n\n"
            )
        elif sweep_type == "log":
            sweep = an.sweep.log
            netlist.write(
                f".dc DEC {param} {sweep.start} {sweep.stop} {sweep.npts}\n\n"
            )
        elif sweep_type == "points":
            sweep = an.sweep.points
            netlist.write(
                f".dc {param} LIST {' '.join([str(pt) for pt in sweep.points])}\n\n"
            )
        else:
            raise ValueError("Invalid sweep type")

        # FIXME: always saving everything, no matter what
        # Note `csv` output-formatting is encoded here
        netlist.write(".print dc format=csv v(*) i(*) \n\n")

        # And don't forget - the thing SPICE can't live without - END!
        netlist.write(".end \n\n")
        netlist.flush()

        # Do the real work, running the simulation
        await self.run_xyce_process(analysis_name)

        # Read the results from CSV
        with self.open(f"{analysis_name}.sp.csv", "r") as csv_handle:
            csv_data = read_csv(csv_handle)

        # Parse any scalar measurement results
        measurements = self.parse_measurements(analysis_name)

        # And arrange them in an `OpResult`
        return DcResult(
            analysis_name=an.analysis_name,
            indep_name=an.indep_name,
            data=csv_data,
            measurements=measurements,
        )

    async def op(self, an: vsp.OpInput) -> Awaitable[OpResult]:
        """Run an operating-point analysis.
        Xyce describes the `.op` analysis as "partially supported".
        Here the `vsp.Op` analysis is mapped to DC, with a dummy sweep."""

        # Unpack the `OpInput`
        if not an.analysis_name:
            raise RuntimeError(f"Analysis name required for {an}")
        analysis_name = an.analysis_name
        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        # Copy and append to the existing DUT netlist
        netlist = self.copy_dut_netlist(f"{analysis_name}.sp")

        # Create the dummy parameter, and "sweep" a single value of it
        dummy_param = f"_dummy_{random.randint(0,65536)}_"
        netlist.write(f".param {dummy_param}=1 \n\n")

        # Write the analysis command
        netlist.write(f".dc {dummy_param} 1 1 1 \n\n")

        # FIXME: always saving everything, no matter what
        # Note `csv` output-formatting is encoded here
        netlist.write(".print dc format=csv v(*) i(*) \n\n")

        # And don't forget - the thing SPICE can't live without - END!
        netlist.write(".end \n\n")
        netlist.flush()

        # Do the real work, running the simulation
        await self.run_xyce_process(analysis_name)

        # Read the results from CSV
        with self.open(f"{analysis_name}.sp.csv", "r") as csv_handle:
            csv_data = read_csv(csv_handle)

        # Each value in `csv_data` will be a single-element list.
        # Pull those single elements out.
        data = {k: v[0] for k, v in csv_data.items()}

        # And arrange them in an `OpResult`
        return OpResult(
            analysis_name=an.analysis_name,
            data=data,
        )

    async def tran(self, an: vsp.TranInput) -> Awaitable[vsp.TranResult]:
        """Run a transient analysis."""

        # Extract fields from our `TranInput`
        if not an.analysis_name:
            raise RuntimeError(f"Analysis name required for {an}")
        analysis_name = an.analysis_name

        # Why not make tstop/tstep required?
        if not an.tstop or not an.tstep:
            raise ValueError("tstop and tstep must be defined")
        tstop = an.tstop
        tstep = an.tstep
        if len(an.ic):
            raise NotImplementedError
        if len(an.ctrls):
            raise NotImplementedError

        # Copy and append to the existing DUT netlist
        netlist = self.copy_dut_netlist(f"{analysis_name}.sp")

        # Write the analysis command
        netlist.write(f".tran {tstep} {tstop} \n\n")

        # FIXME: always saving everything, no matter what
        # Note `csv` output-formatting is encoded here
        netlist.write(".print tran format=csv v(*) i(*) \n\n")

        # And don't forget - the thing SPICE can't live without - END!
        netlist.write(".end \n\n")
        netlist.flush()

        # Do the real work, running the simulation
        await self.run_xyce_process(analysis_name)

        # Parse and organize our results
        # First pull them in from CSV
        with self.open(f"{analysis_name}.sp.csv", "r") as csv_handle:
            csv_data = read_csv(csv_handle)

        # Parse any scalar measurement results
        measurements = self.parse_measurements(analysis_name)

        # And organize them into a `TranResult`
        return TranResult(
            analysis_name=an.analysis_name, data=csv_data, measurements=measurements
        )

    def run_xyce_process(self, name: str) -> Awaitable[None]:
        """Run a `Xyce` sub-process executing the simulation."""
        return self.run_subprocess(cmd=f"{XYCE_EXECUTABLE} {name}.sp ")

    def parse_measurements(self, analysis_name: str) -> Dict[str, float]:
        # FIXME: the *input* should really be dictating whether we have measurements.
        # For now, we just search for any matching filenames via `glob`
        meas_glob = glob(f"*{analysis_name}*.m*0")
        if len(meas_glob) > 1:
            raise RuntimeError(f"Unsupported multiple measurement results for {self}")
        if len(meas_glob) == 1:
            measurements = parse_meas(self.open(meas_glob[0], "r"))
            return {k.lower(): v for k, v in measurements.items()}
        # No measurement-file, return an empty result
        return {}

    def copy_dut_netlist(self, path: str) -> IO:
        """Copy the `DUT` part of the netlist to file `path`,
        in our working directory, and return a file-handle to it."""
        shutil.copy(self.path("dut"), self.path(path))
        return self.open(path, "a")


def read_csv(handle: Union[IO, PathLike]) -> Dict[str, np.ndarray]:
    """Read CSV from file-handle `handle` into a dictionary of {header: array}s."""

    df = pd.read_csv(handle)
    return {n: np.array(c) for n, c in df.items()}


def parse_meas(file: IO) -> Dict[str, float]:
    """Parse an (open) measurement-file to a {name: value} dictionary."""
    rv = {}
    for line in file.readlines():
        contents = line.split()
        if len(contents) != 3 or contents[1] != "=":
            raise RuntimeError(f"Invalid line in Xyce measurements: {line}")
        name, val = contents[0], float(contents[2])
        rv[name] = val
    return rv
