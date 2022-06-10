"""
Spectre Implementation of `vlsir.spice.Sim`
"""

# Std-Lib Imports
import subprocess, re, shutil, glob
import numpy as np
from typing import Tuple, Any, Mapping, Optional, IO, Dict
from warnings import warn

# Local/ Project Dependencies
import vlsir.spice_pb2 as vsp
from ..netlist import netlist
from ..netlist.spectre import SpectreNetlister
from .sim_data import TranResult, OpResult, SimResult  ##, AcResult, DcResult,
from .spice import (
    Sim,
    SimProcessError,
    ResultFormat,
    SimOptions,
    SupportedSimulators,
    SimResultUnion,
)

# Module-level configuration. Over-writeable by sufficiently motivated users.
SPECTRE_EXECUTABLE = "spectre"  # The simulator executable invoked. If over-ridden, likely for sake of a specific path or version.


def available() -> bool:
    """ Boolean indication of whether the current running environment includes the simulator executable. """
    if shutil.which(SPECTRE_EXECUTABLE) is None:
        return False
    try:
        # And if it's set, check that we can get its version without croaking.
        # This can often happen because of an inaccessible license server, or just a badly-linked installation.
        subprocess.run(
            f"{SPECTRE_EXECUTABLE} -V",  # Yes, "version" gets a capital "V" for this program (ascii shrug)
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception:
        # Indicate "not available" for any Exception. Usually this will be a `subprocess.CalledProcessError`.
        return False
    return True  # Otherwise, installation looks good.


def sim(inp: vsp.SimInput, opts: Optional[SimOptions] = None,) -> SimResultUnion:
    """ # Primary Simulation Method """

    if opts is None:  # Create the default options
        opts = SimOptions(simulator=SupportedSimulators.SPECTRE)

    results = SpectreSim.sim(inp, opts)

    if opts.fmt == ResultFormat.VLSIR_PROTO:
        return results.to_proto()
    return results


class SpectreSim(Sim):
    """
    State and execution logic for a Spectre-call to `vsp.Sim`.
    """

    @classmethod
    def enum(cls) -> SupportedSimulators:
        return SupportedSimulators.SPECTRE

    def _run(self) -> SimResult:
        """ Run the specified `SimInput` in directory `self.tmpdir`, returning its results. """

        netlist_file = open("netlist.scs", "w")
        netlist_file.write("// Test Netlist \n\n")
        netlist_file.write("simulator lang=spectre \n\n")
        netlist_file.write("global 0\n\n")
        netlist(pkg=self.inp.pkg, dest=netlist_file, fmt="spectre")

        # Write the top-level instance
        top_name = SpectreNetlister.get_module_name(self.top)
        netlist_file.write(f"xtop 0 {top_name} // Top-Level DUT \n\n")

        if self.inp.opts:
            raise NotImplementedError(f"SimInput Options")

        # Write each control element
        self.write_control_elements(netlist_file)

        # Write each analysis
        for an in self.inp.an:
            self.netlist_analysis(an, netlist_file)

        # Run the simulation
        netlist_file.flush()
        netlist_file.close()
        self.run_simulation()

        # Parse output data
        data = parse("netlist.raw")
        an_type_dispatch = dict(
            ac=self.parse_ac, dc=self.parse_dc, op=self.parse_op, tran=self.parse_tran
        )
        results = []
        for an in self.inp.an:
            an_type = an.WhichOneof("an")
            inner = getattr(an, an_type)
            if an_type not in an_type_dispatch:
                msg = f"Invalid or Unsupported analysis {an} with type {an_type}"
                raise RuntimeError(msg)
            func = an_type_dispatch[an_type]
            if inner.analysis_name not in data:
                msg = f"Cannot read results for analysis {an}"
                raise RuntimeError(msg)
            inner_data = data[inner.analysis_name]
            an_results = func(inner, inner_data)
            results.append(an_results)

        return SimResult(an=results)

    def write_control_elements(self, netlist_file: IO) -> None:
        """ Write control elements to the netlist """
        for ctrl in self.inp.ctrls:
            inner = ctrl.WhichOneof("ctrl")
            if inner == "include":
                netlist_file.write(f'include "{ctrl.include.path}" \n')
            elif inner == "lib":
                txt = f'include "{ctrl.lib.path}" section={ctrl.lib.section} \n'
                netlist_file.write(txt)
            elif inner == "literal":
                netlist_file.write(ctrl.literal + "\n")
            elif inner == "param":
                # txt = f"parameters {ctrl.param.name}={str(ctrl.param.value)} \n"
                txt = f"parameters  {ctrl.param.name}={SpectreNetlister.get_param_value(ctrl.param.value)} \n"
                netlist_file.write(txt)
            elif inner == "meas":
                # Measurements are written in Spice syntax; wrap them in "simulator lang".
                netlist_file.write(f"simulator lang=spice \n")
                txt = f".meas {ctrl.meas.analysis_type} {ctrl.meas.name} {ctrl.meas.expr} \n"
                netlist_file.write(txt)
                netlist_file.write(f"simulator lang=spectre \n")
            elif inner in ("save"):
                raise NotImplementedError(
                    f"Unimplemented control card {ctrl} for {self}"
                )  # FIXME!
            else:
                raise RuntimeError(f"Unknown control type: {inner}")

    def netlist_analysis(self, an: vsp.Analysis, netlist_file) -> None:
        inner = an.WhichOneof("an")
        inner_dispatch = dict(
            ac=self.netlist_ac,
            dc=self.netlist_dc,
            op=self.netlist_op,
            tran=self.netlist_tran,
        )

        inner_dispatch[inner](getattr(an, inner), netlist_file)

    def netlist_ac(self, an: vsp.AcInput, netlist_file) -> None:
        """ Run an AC analysis. """
        raise NotImplementedError

    def netlist_dc(self, an: vsp.DcInput, netlist_file) -> None:
        """ Run a DC analysis. """
        # Unpack the `DcInput`
        analysis_name = an.analysis_name or "dc"

        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        # Write the analysis command
        param = an.indep_name
        ## Interpret the sweep
        sweep_type = an.sweep.WhichOneof("tp")
        if sweep_type == "linear":
            sweep = an.sweep.linear
            netlist_file.write(
                f"{analysis_name} dc param={param} start={sweep.start} stop={sweep.stop} step={sweep.step}\n\n"
            )
        elif sweep_type in ("log", "points"):
            raise NotImplementedError
        else:
            raise ValueError("Invalid sweep type")

    def netlist_op(self, an: vsp.OpInput, netlist_file) -> None:
        """
        This netlists as a single point DC analysis
        """
        # Unpack the `OpInput`
        analysis_name = an.analysis_name or "op"
        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        netlist_file.write(f"{analysis_name} dc oppoint=rawfile\n\n")

    def netlist_tran(self, an: vsp.TranInput, netlist_file) -> None:
        analysis_name = an.analysis_name or "tran"
        if len(an.ctrls):
            raise NotImplementedError
        if len(an.ic):
            raise NotImplementedError

        netlist_file.write(f"{analysis_name} tran stop={an.tstop} \n\n")

    def parse_ac(self, an: vsp.AcInput, data: Mapping[str, Any]) -> vsp.AcResult:
        raise NotImplementedError

    def parse_dc(self, an: vsp.DcInput, data: Mapping[str, Any]) -> vsp.DcResult:
        raise NotImplementedError

    def parse_op(self, an: vsp.OpInput, data: Mapping[str, Any]) -> OpResult:
        return OpResult(
            analysis_name=an.analysis_name,
            data={k: v[0] for k, v in data["data"].items()},
        )

    def parse_tran(self, an: vsp.TranInput, data: Mapping[str, Any]) -> TranResult:
        meas_files = glob.glob("*.mt*")
        if len(meas_files) > 1:
            msg = f"Unsupported: more than one measurement-file generated. Only the first will be read"
            warn(msg)
        elif len(meas_files) == 1:
            measurements = parse_mt0(open(meas_files[0], "r"))
        else:
            measurements = dict()

        return TranResult(
            analysis_name=an.analysis_name, data=data["data"], measurements=measurements
        )

    def run_simulation(self):
        """ Run a Spectre simulation """

        cmd = f"{SPECTRE_EXECUTABLE} -E -format nutbin netlist.scs"
        try:
            subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise SimProcessError(self, e)
        except Exception as e:
            raise


def parse(filename: str) -> Mapping[str, Any]:
    """ 
    Parse a... what now? PSF Directory? In what format? 
    FIXME: @avi 
    """
    data = {}
    with open(filename, "rb") as f:
        # First 2 lines are ascii one line statements
        _title = f.readline()  # Title, ignored
        _date = f.readline()  # Run date, ignored
        while True:
            # Next 4 lines are also ascii one line statements
            plotname = f.readline()  # Simulation name
            if len(plotname) == 0:
                break
            flags = f.readline()  # Flags for this simulation result
            num_vars_line = f.readline()  # No. Variables:   [nvar]
            num_pts_line = f.readline()  # No. Points:      [npts]
            sim_name = plotname.decode("ascii").split("`")[-1].split("'")[0]
            data[sim_name] = dict(data={}, units={})

            # Find the number of variables and number of points
            num_vars = int(
                re.match(
                    r"No. Variables:\s+(?P<num_vars>\d+)\n",
                    num_vars_line.decode("ascii"),
                ).group("num_vars")
            )
            num_pts = int(
                re.match(
                    r"No. Points:\s+(?P<num_pts>\d+)\n", num_pts_line.decode("ascii"),
                ).group("num_pts")
            )

            # Decode the variables spec, looks like the following
            # Variables: [Variable idx] [Variable name] [units] [optional_flags]
            var_line = f.readline().decode("ascii")
            var_specs = [_read_var_spec(var_line[10:])]
            for i in range(num_vars - 1):
                var_specs.append(_read_var_spec(f.readline().decode("ascii")))

            # Read the binary data, should look like the following:
            # Binary: \n[Binary data]
            binary_line = f.readline().decode("ascii")
            assert binary_line == "Binary:\n"
            # Data is big endian
            bin_data = np.fromfile(
                f, dtype=np.dtype(float).newbyteorder(">"), count=num_vars * num_pts
            )
            for i, var in enumerate(var_specs):
                data[sim_name]["data"][var[0]] = bin_data[i::num_vars]
                data[sim_name]["units"][var[0]] = var[1]

        return data


def _read_var_spec(line: str) -> Tuple[str, str]:
    """Read a Variable spec line from the input
    and return the name and the units."""
    m = re.match(
        r"\s+(?P<idx>\d+)\s+(?P<name>\S+)\s+(?P<units>\S+)(?P<rest>.*)\n", line
    )
    return (m.group("name"), m.group("units"))


def parse_mt0(file: IO) -> Dict[str, float]:
    """ Parse an (open) "mt0-format" measurement-file into a set of {name: value} pairs. """

    file.readline()  # Header
    file.readline()  # Netlist Title
    keys = file.readline()  # Measurement Names Line
    keys = keys.split()
    values = file.readline()  # Measurement Values Line
    values = [float(s) for s in values.split()]
    return dict(zip(keys, values))
