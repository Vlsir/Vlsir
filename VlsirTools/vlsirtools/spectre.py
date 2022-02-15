"""
Spectre Implementation of `vlsir.spice.Sim`
"""

# Std-Lib Imports
import subprocess, re, shutil
from typing import Tuple, Any, Mapping, Union
import numpy as np

# Local/ Project Dependencies
import vlsir
from .netlist import netlist
from .netlist.spectre import SpectreNetlister
from .sim_data import TranResult, AcResult, DcResult, OpResult, SimResult, ResultFormat
from .spice import Sim, SimProcessError

# Module-level configuration. Over-writeable by sufficiently motivated users.
SPECTRE_EXECUTABLE = "spectre"  # The simulator executable invoked. If over-ridden, likely for sake of a specific path or version.


def available() -> bool:
    """ Boolean indication of whether the current running environment includes the simulator executable on its path. """
    return shutil.which(SPECTRE_EXECUTABLE) is not None


def _read_var_spec(line: str) -> Tuple[str, str]:
    """Read a Variable spec line from the input
    and return the name and the units."""
    m = re.match(
        r"\s+(?P<idx>\d+)\s+(?P<name>\S+)\s+(?P<units>\S+)(?P<rest>.*)\n", line
    )
    return (m.group("name"), m.group("units"))


def sim(
    inp: vlsir.spice.SimInput, fmt: ResultFormat = ResultFormat.SIM_DATA
) -> Union[SimResult, vlsir.spice.SimResult]:
    """
    # Primary Simulation Method
    Implements the `vlsir.spice.Sim` RPC interface.

    Returns resultant data in a format dictated by argument `fmt`,
    generally either the `vlsir` protobuf-schema, or the pythonic `SimResult`.
    """
    if not isinstance(fmt, ResultFormat):
        raise TypeError(f"Invalid ResultFormat: {fmt}")

    with SpectreSim(inp) as sim:
        results: SimResult = sim.run()

    if fmt == ResultFormat.VLSIR_PROTO:
        return results.to_proto()
    return results


class SpectreSim(Sim):
    """
    State and execution logic for a Spectre-call to `vlsir.spice.Sim`.
    """

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
            results.append(an_type_dispatch[an_type](inner, data[inner.analysis_name]))
        return SimResult(an=results)

    def write_control_elements(self, netlist_file) -> None:
        """ Write control elements to the netlist """
        for ctrl in self.inp.ctrls:
            inner = ctrl.WhichOneof("ctrl")
            if inner == "include":
                netlist_file.write(f'include "{ctrl.include.path}" \n')
            elif inner in ("lib", "save", "meas", "literal"):
                raise NotImplementedError  # FIXME!
            else:
                raise RuntimeError(f"Unknown control type: {inner}")

    def netlist_analysis(self, an: vlsir.spice.Analysis, netlist_file) -> None:
        inner = an.WhichOneof("an")
        inner_dispatch = dict(
            ac=self.netlist_ac,
            dc=self.netlist_dc,
            op=self.netlist_op,
            tran=self.netlist_tran,
        )

        inner_dispatch[inner](getattr(an, inner), netlist_file)

    def netlist_ac(self, an: vlsir.spice.AcInput, netlist_file) -> None:
        """ Run an AC analysis. """
        raise NotImplementedError

    def netlist_dc(self, an: vlsir.spice.DcInput, netlist_file) -> None:
        """ Run a DC analysis. """
        raise NotImplementedError

    def netlist_op(self, an: vlsir.spice.OpInput, netlist_file) -> None:
        """
        This netlists as a single point DC analysis
        """
        # Unpack the `OpInput`
        analysis_name = an.analysis_name or "op"
        if len(an.ctrl):
            raise NotImplementedError  # FIXME!

        netlist_file.write(f"{analysis_name} dc oppoint=rawfile\n\n")

    def netlist_tran(self, an: vlsir.spice.TranInput, netlist_file) -> None:
        analysis_name = an.analysis_name or "tran"
        if len(an.ctrl):
            raise NotImplementedError
        if len(an.ic):
            raise NotImplementedError

        netlist_file.write(f"{analysis_name} tran stop={an.tstop} \n\n")

    def parse_ac(
        self, an: vlsir.spice.AcInput, data: Mapping[str, Any]
    ) -> vlsir.spice.AcResult:
        raise NotImplementedError

    def parse_dc(
        self, an: vlsir.spice.DcInput, data: Mapping[str, Any]
    ) -> vlsir.spice.DcResult:
        raise NotImplementedError

    def parse_op(self, an: vlsir.spice.OpInput, data: Mapping[str, Any]) -> OpResult:
        return OpResult(
            analysis_name=an.analysis_name,
            data={k: v[0] for k, v in data["data"].items()},
        )

    def parse_tran(
        self, an: vlsir.spice.TranInput, data: Mapping[str, Any]
    ) -> TranResult:
        return TranResult(analysis_name=an.analysis_name, data=data["data"])

    def run_simulation(self):
        """ Run a Spectre simulation """

        cmd = f"{SPECTRE_EXECUTABLE} -E -format nutbin netlist.scs"
        try:
            subprocess.run(
                cmd,
                capture_output=True,
                # stdout=open(f"netlist.scs.stdout.log", "w"),
                # stderr=open(f"netlist.scs.stderr.log", "w"),
                shell=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise SimProcessError(e)
        except Exception as e:
            raise


def parse(filename: str) -> Mapping[str, Any]:
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
