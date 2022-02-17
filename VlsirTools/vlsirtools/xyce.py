"""
Xyce Implementation of `vlsir.spice.Sim`
"""

# Std-Lib Imports
import subprocess, random, shutil, csv
from typing import List, Tuple, IO

# Local/ Project Dependencies
import vlsir
from .netlist import netlist
from .spice import Sim, SimError
from .sim_data import ResultFormat


# Module-level configuration. Over-writeable by sufficiently motivated users.
XYCE_EXECUTABLE = "Xyce"  # The simulator executable invoked. If over-ridden, likely for sake of a specific path or version.


def available() -> bool:
    """ Boolean indication of whether the current running environment includes the simulator executable on its path. """
    return shutil.which(XYCE_EXECUTABLE) is not None


def sim(
    inp: vlsir.spice.SimInput, fmt: ResultFormat = ResultFormat.VLSIR_PROTO
) -> vlsir.spice.SimResult:
    """ 
    # Primary Simulation Method 
    Implements the `vlsir.spice.Sim` RPC interface. 
    """

    if fmt != ResultFormat.VLSIR_PROTO:
        raise RuntimeError(f"Unsupported ResultFormat: {fmt} for Xyce")

    with XyceSim(inp) as sim:
        return sim.run()


class XyceSim(Sim):
    """ 
    State and execution logic for a Xyce-call to `vlsir.spice.Sim`. 
    
    Xyce can, in principle, run multiple analyses per process, 
    but seems to commonly confuse outputs or disallow saving them
    from multiple analyses. 

    Execution therefore instead occurs one Xyce-process per analysis. 
    Results from each analysis-process are collated into a single `SimResult`. 
    """

    def _run(self) -> vlsir.spice.SimResult:
        """ Run the specified `SimInput` in directory `self.tmpdir`, 
        returning its results. """

        netlist_file = open("dut", "w")
        netlist(pkg=self.inp.pkg, dest=netlist_file, fmt="xyce")

        # Write the top-level instance
        netlist_file.write(f"xtop 0 {self.inp.top} ; Top-Level DUT \n\n")

        # Write each control element
        for ctrl in self.inp.ctrls:
            inner = ctrl.WhichOneof("ctrl")
            if inner == "include":
                netlist_file.write(f".include '{ctrl.include.path}' \n")
            elif inner in ("lib", "save", "meas", "literal"):
                raise NotImplementedError  # FIXME!
            else:
                raise RuntimeError(f"Unknown control type: {inner}")

        # Flush the netlist to disk before handing off to analyses
        netlist_file.flush()

        # Run each analysis in the input
        results = vlsir.spice.SimResult()
        for an in self.inp.an:
            results.an.append(self.analysis(an))
        return results

    def analysis(self, an: vlsir.spice.Analysis) -> vlsir.spice.AnalysisResult:
        """ Execute a `vlsir.spice.Analysis`, returning its `vlsir.spice.AnalysisResult`. """

        # `Analysis` is a Union (protobuf `oneof`) of the analysis-types.
        # Unwrap it, and dispatch based on the type.
        AR = vlsir.spice.AnalysisResult  # Quick shorthand
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

    def ac(self, an: vlsir.spice.AcInput) -> vlsir.spice.AcResult:
        """ Run an AC analysis. """

        # Unpack the `AcInput`
        analysis_name = an.analysis_name or "ac"
        if len(an.ctrl):
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
            (signals, data) = self.read_csv(csv_handle)

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
            vlsir.spice.ComplexNum(re=real, im=imag) for real, imag in zip(reals, imags)
        ]

        # And arrange them in an `AcResult`
        return vlsir.spice.AcResult(freq=freq, signals=signals, data=cplx_data)

    def dc(self, an: vlsir.spice.DcInput) -> vlsir.spice.DcResult:
        """ Run a DC analysis. """

        # Unpack the `DcInput`
        analysis_name = an.analysis_name or "dc"

        if len(an.ctrl):
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
            (signals, data) = self.read_csv(csv_handle)

        # And arrange them in an `OpResult`
        return vlsir.spice.DcResult(signals=signals, data=data)

    def op(self, an: vlsir.spice.OpInput) -> vlsir.spice.OpResult:
        """ Run an operating-point analysis. 
        Xyce describes the `.op` analysis as "partially supported". 
        Here the `vlsir.spice.Op` analysis is mapped to DC, with a dummy sweep. """

        # Unpack the `OpInput`
        analysis_name = an.analysis_name or "op"
        if len(an.ctrl):
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
            (signals, data) = self.read_csv(csv_handle)

        # And arrange them in an `OpResult`
        return vlsir.spice.OpResult(signals=signals, data=data)

    def tran(self, an: vlsir.spice.TranInput) -> vlsir.spice.TranResult:
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
        if len(an.ctrl):
            raise NotImplementedError

        # Copy and append to the existing DUT netlist
        shutil.copy("dut", f"{analysis_name}.sp")

        netlist = open(f"{analysis_name}.sp", "a")

        # FIXME: add a few fake components!
        # netlist.write("r1 1 0 1k \n\n")
        # netlist.write("i1 1 0 -1e-3 \n\n")

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
            (signals, data) = self.read_csv(csv_handle)

        # And organize them into a `TranResult` message
        return vlsir.spice.TranResult(signals=signals, data=data)

    def run_xyce_process(self, name: str):
        """ Run a `Xyce` sub-process, collecting terminal output. """

        try:
            subprocess.run(
                f"{XYCE_EXECUTABLE} {name}.sp ",
                stdout=open(f"{name}.sp.stdout.log", "w"),
                stderr=open(f"{name}.sp.stderr.log", "w"),
                shell=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise SimError
        except Exception as e:
            raise

    def read_csv(self, handle: IO) -> Tuple[List[str], List[float]]:
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

