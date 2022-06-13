"""
Xyce Implementation of `vsp.Sim`
"""

# Std-Lib Imports
import subprocess, random, shutil, csv
from typing import List, Tuple, IO, Optional, Dict
from glob import glob

# Local/ Project Dependencies
import vlsir.spice_pb2 as vsp
from ..netlist import netlist, XyceNetlister
from .spice import (
    Sim,
    SimProcessError,
    ResultFormat,
    SimOptions,
    SupportedSimulators,
    SimResultUnion,
)


# Module-level configuration. Over-writeable by sufficiently motivated users.
XYCE_EXECUTABLE = "Xyce"  # The simulator executable invoked. If over-ridden, likely for sake of a specific path or version.


def available() -> bool:
    """ Boolean indication of whether the current running environment includes the simulator executable on its path. """
    return shutil.which(XYCE_EXECUTABLE) is not None


def sim(inp: vsp.SimInput, opts: Optional[SimOptions] = None) -> SimResultUnion:
    """ # Primary Simulation Method """

    if opts is None:  # Create the default options
        opts = SimOptions(simulator=SupportedSimulators.XYCE)

    if opts.fmt != ResultFormat.VLSIR_PROTO:
        raise RuntimeError(f"Unsupported ResultFormat: {opts.fmt} for Xyce")

    return XyceSim.sim(inp, opts)


class XyceSim(Sim):
    """ 
    State and execution logic for a Xyce-call to `vsp.Sim`. 
    
    Xyce can, in principle, run multiple analyses per process, 
    but seems to commonly confuse outputs or disallow saving them
    from multiple analyses. 

    Execution therefore instead occurs one Xyce-process per analysis. 
    Results from each analysis-process are collated into a single `SimResult`. 
    """

    @classmethod
    def enum(cls) -> SupportedSimulators:
        return SupportedSimulators.XYCE

    def _run(self) -> vsp.SimResult:
        """ Run the specified `SimInput` in directory `self.rundir`, 
        returning its results. """

        netlist_file = open("dut", "w")
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
        results = vsp.SimResult()
        for an in self.inp.an:
            results.an.append(self.analysis(an))
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

    def analysis(self, an: vsp.Analysis) -> vsp.AnalysisResult:
        """ Execute a `vsp.Analysis`, returning its `vsp.AnalysisResult`. """

        # `Analysis` is a Union (protobuf `oneof`) of the analysis-types.
        # Unwrap it, and dispatch based on the type.
        AR = vsp.AnalysisResult  # Quick shorthand
        inner = an.WhichOneof("an")

        if inner == "op":
            return AR(op=self.op(an.op))
        if inner == "dc":
            return AR(dc=self.dc(an.dc))
        if inner == "ac":
            return AR(ac=self.ac(an.ac))
        if inner == "tran":
            return AR(tran=self.tran(an.tran))
        if inner in ("sweep", "monte", "custom"):
            raise NotImplementedError(f"{inner} not implemented")
        raise RuntimeError(f"Unknown analysis type: {inner}")

    def ac(self, an: vsp.AcInput) -> vsp.AcResult:
        """ Run an AC analysis. """

        # Unpack the `AcInput`
        analysis_name = an.analysis_name or "ac"
        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        # Copy and append to the existing DUT netlist
        shutil.copy("dut", f"{analysis_name}.sp")
        netlist = open(f"{analysis_name}.sp", "a")

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
        self.run_xyce_process(analysis_name)

        # Read the results from CSV
        with open(f"{analysis_name}.sp.FD.csv", "r") as csv_handle:
            (signals, data) = read_csv(csv_handle)

        # Separate Frequency vector
        n_sigs = len(signals)  # Get length of signals vector because...
        freq = data[::n_sigs]  # ...every n-th data pt is a freq pt
        del data[::n_sigs]  # Clean the list of data of all frequencies
        signals.pop(0)  # Remove "Frequency" from list of signals

        # Build ComplexNumbers for each data point
        reals = data[::2]
        imags = data[1::2]
        if not len(reals) == len(imags):  # Sanity check
            raise RuntimeError("Unpaired complex number in data")
        cplx_data = [
            vsp.ComplexNum(re=real, im=imag) for real, imag in zip(reals, imags)
        ]

        # Parse any scalar measurement results
        measurements = parse_measurements(analysis_name)

        # And arrange them in an `AcResult`
        return vsp.AcResult(
            freq=freq, signals=signals, data=cplx_data, measurements=measurements
        )

    def dc(self, an: vsp.DcInput) -> vsp.DcResult:
        """ Run a DC analysis. """

        # Unpack the `DcInput`
        analysis_name = an.analysis_name or "dc"

        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        # Copy and append to the existing DUT netlist
        shutil.copy("dut", f"{analysis_name}.sp")
        netlist = open(f"{analysis_name}.sp", "a")

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
        self.run_xyce_process(analysis_name)

        # Read the results from CSV
        with open(f"{analysis_name}.sp.csv", "r") as csv_handle:
            (signals, data) = read_csv(csv_handle)

        # Parse any scalar measurement results
        measurements = parse_measurements(analysis_name)

        # And arrange them in an `OpResult`
        return vsp.DcResult(signals=signals, data=data, measurements=measurements)

    def op(self, an: vsp.OpInput) -> vsp.OpResult:
        """ Run an operating-point analysis. 
        Xyce describes the `.op` analysis as "partially supported". 
        Here the `vsp.Op` analysis is mapped to DC, with a dummy sweep. """

        # Unpack the `OpInput`
        analysis_name = an.analysis_name or "op"
        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        # Copy and append to the existing DUT netlist
        shutil.copy("dut", f"{analysis_name}.sp")
        netlist = open(f"{analysis_name}.sp", "a")

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
        self.run_xyce_process(analysis_name)

        # Read the results from CSV
        with open(f"{analysis_name}.sp.csv", "r") as csv_handle:
            (signals, data) = read_csv(csv_handle)

        # And arrange them in an `OpResult`
        return vsp.OpResult(signals=signals, data=data)

    def tran(self, an: vsp.TranInput) -> vsp.TranResult:
        """ Run a transient analysis. """

        # Extract fields from our `TranInput`
        analysis_name = an.analysis_name or "tran"

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
        shutil.copy("dut", f"{analysis_name}.sp")
        netlist = open(f"{analysis_name}.sp", "a")

        # Write the analysis command
        netlist.write(f".tran {tstep} {tstop} \n\n")

        # FIXME: always saving everything, no matter what
        # Note `csv` output-formatting is encoded here
        netlist.write(".print tran format=csv v(*) i(*) \n\n")

        # And don't forget - the thing SPICE can't live without - END!
        netlist.write(".end \n\n")
        netlist.flush()

        # Do the real work, running the simulation
        self.run_xyce_process(analysis_name)

        # Parse and organize our results
        # First pull them in from CSV
        with open(f"{analysis_name}.sp.csv", "r") as csv_handle:
            (signals, data) = read_csv(csv_handle)

        # Parse any scalar measurement results
        measurements = parse_measurements(analysis_name)

        # And organize them into a `TranResult` message
        return vsp.TranResult(
            analysis_name=analysis_name,
            signals=signals,
            data=data,
            measurements=measurements,
        )

    def run_xyce_process(self, name: str):
        """ Run a `Xyce` sub-process, collecting terminal output. """

        try:
            _result = subprocess.run(
                f"{XYCE_EXECUTABLE} {name}.sp ",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise SimProcessError(self, e)
        except Exception as e:
            raise


def read_csv(handle: IO) -> Tuple[List[str], List[float]]:
    """ Read a text-header + float CSV from file-handle `handle`. """

    # Get the header-list of strings
    header_line = handle.readline().strip()
    headers = header_line.split(",")

    # The remaining rows are data-values. Append them to the (single-dimension) list of results.
    data = []
    results_csv = csv.reader(handle, quoting=csv.QUOTE_NONNUMERIC)
    for row in results_csv:
        data.extend(row)

    # And return the two as a tuple
    return (headers, data)


def parse_meas(file: IO) -> Dict[str, float]:
    """ Parse an (open) measurement-file to a {name: value} dictionary. """
    rv = {}
    for line in file.readlines():
        contents = line.split()
        if len(contents) != 3 or contents[1] != "=":
            raise RuntimeError(f"Invalid line in Xyce measurements: {line}")
        name, val = contents[0], float(contents[2])
        rv[name] = val
    return rv


def parse_measurements(analysis_name: str) -> Dict[str, float]:
    # FIXME: the *input* should really be dictating whether we have measurements.
    # For now, we just search for any matching filenames via `glob`
    meas_glob = glob(f"*{analysis_name}*.m*0")
    if len(meas_glob) > 1:
        raise RuntimeError(f"Unsupported multiple measurement results for {self}")
    if len(meas_glob) == 1:
        measurements = parse_meas(open(meas_glob[0], "r"))
        return {k.lower(): v for k, v in measurements.items()}
    # No measurement-file, return an empty result
    return {}

