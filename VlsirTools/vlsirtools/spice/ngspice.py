"""
NGSpice Implementation of `vlsir.spice.Sim`
"""

# Std-Lib Imports
from concurrent.futures import ProcessPoolExecutor
import subprocess, re, shutil
from enum import Enum
from warnings import warn
from dataclasses import dataclass
from typing import Mapping, IO, Dict
import shlex

# External Imports
import numpy as np

# Local/ Project Dependencies
import vlsir.spice_pb2 as vsp
from ..netlist import netlist
from ..netlist.spice import NgspiceNetlister
from .base import Sim
from .sim_data import TranResult, OpResult, SimResult, AcResult, DcResult, NoiseResult
from .spice import SupportedSimulators, sim

# Module-level configuration. Over-writeable by sufficiently motivated users.

# The simulator executable invoked. If over-ridden, likely for sake of a specific path or version.
NGSPICE_EXECUTABLE = "ngspice"


def available() -> bool:
    return NGSpiceSim.available()


class NGSpiceSim(Sim):
    """
    State and execution logic for a NGSpice-call to `vsp.Sim`.
    """

    @staticmethod
    def available() -> bool:
        """Boolean indication of whether the current running environment includes the simulator executable."""
        if shutil.which(NGSPICE_EXECUTABLE) is None:
            return False
        try:
            subprocess.run(
                f"{NGSPICE_EXECUTABLE} -v",
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
        return SupportedSimulators.NGSPICE

    def run(self) -> SimResult:
        """Run the specified `SimInput` in directory `self.rundir`, returning its results."""

        # Write the netlist
        self.write_netlist()

        self.run_sim_process()

        # Handle stdout and stderr as needed
        # Parse up the results
        return self.parse_results()

    def write_netlist(self) -> None:
        """# Write our netlist to file"""

        netlist_file = self.open("netlist.sp", "w")
        netlister = NgspiceNetlister(dest=netlist_file)
        netlister.write_sim_input(self.inp)
        netlist_file.flush()
        netlist_file.close()

    def parse_results(self) -> SimResult:
        """# Parse output data"""

        data = parse_nutbin(self.open("netlist.raw", "rb"))
        an_type_dispatch = dict(
            ac=self.parse_ac,
            dc=self.parse_dc,
            op=self.parse_op,
            tran=self.parse_tran,
            noise=self.parse_noise,
        )
        an_name_dispatch = dict(
            op="Plotname: Operating Point\n",
            dc="Plotname: DC Analysis\n",
            ac="Plotname: AC Analysis\n",
            tran="Plotname: Transient Analysis\n",
            noise="FIXME! do we still want this setup?",
        )
        results = []
        for an in self.inp.an:
            an_type = an.WhichOneof("an")
            inner = getattr(an, an_type)

            if an_type == "noise":
                # FIXME: I read somewhere that "Special cases aren't special enough to break the rules."
                results.append(self.parse_noise(inner, data))
                continue

            if an_type not in an_type_dispatch:
                msg = f"Invalid or Unsupported analysis {an} with type {an_type}"
                raise RuntimeError(msg)
            func = an_type_dispatch[an_type]
            analysis_name = an_name_dispatch[an_type]
            if analysis_name not in data:
                msg = f"Cannot read results for analysis {an}"
                raise RuntimeError(msg)
            inner_data = data[analysis_name]
            an_results = func(inner, inner_data)
            results.append(an_results)

        return SimResult(an=results)

    def parse_ac(self, an: vsp.AcInput, nutbin: "NutBinAnalysis") -> AcResult:
        # FIXME: the `mt0` and friends file names collide with tran, if they are used in the same Sim!
        measurements = self.get_measurements("*.mt*")

        # Pop the frequence vector out of the data
        freq = nutbin.data.pop("frequency")

        # Nutbin format stores the frequency vector as complex numbers, along with all the complex-valued signal data.
        # NOTE: once upon a time, we checked that the imaginary part of all frequencies was zero.
        # And that used to work! Now it doesn't; ngspice just seemingly leaves it uninitialized, or set to some random value.
        # See https://github.com/Vlsir/Vlsir/issues/66
        # Now, just grab the real part.
        freq = freq.real

        return AcResult(
            analysis_name=an.analysis_name,
            freq=freq,
            data=nutbin.data,
            measurements=measurements,
        )

    def parse_dc(self, an: vsp.DcInput, nutbin: "NutBinAnalysis") -> DcResult:
        measurements = self.get_measurements("*.ms*")
        return DcResult(
            analysis_name=an.analysis_name,
            indep_name=an.indep_name,
            data=nutbin.data,
            measurements=measurements,
        )

    def parse_op(self, an: vsp.OpInput, nutbin: "NutBinAnalysis") -> OpResult:
        return OpResult(
            analysis_name=an.analysis_name,
            data={k: v[0] for k, v in nutbin.data.items()},
        )

    def parse_tran(self, an: vsp.TranInput, nutbin: "NutBinAnalysis") -> TranResult:
        """Extract the results for Analysis `an` from `data`."""
        measurements = self.get_measurements("*.mt*")
        return TranResult(
            analysis_name=an.analysis_name, data=nutbin.data, measurements=measurements
        )

    def parse_noise(
        self, an: vsp.NoiseInput, nutbin: Mapping[str, "NutBinAnalysis"]
    ) -> NoiseResult:
        # Noise results come in two "analyses": the frequency-sweep data, and the integrated noise.
        # Collate them into a `NoiseResult`
        # FIXME: add measurements (if there are such things?)
        noise_sweep_data = nutbin.get("Plotname: Noise Spectral Density Curves\n", None)
        if noise_sweep_data is None:
            raise RuntimeError
        integrated_noise = nutbin.get("Plotname: Integrated Noise\n", None)
        if integrated_noise is None:
            raise RuntimeError
        return NoiseResult(
            analysis_name=an.analysis_name,
            data=noise_sweep_data,
            integrated_noise=integrated_noise,
            measurements={},
        )

    def get_measurements(self, filepat: str) -> Dict[str, float]:
        """Get the measurements at files matching (glob) `filepat`.
        Returns only a single files-worth of measurements, and issues a warning if more than one such file exists.
        Returns an empty dictionary if no matching files are found."""
        meas_files = list(self.glob(filepat))
        if not meas_files:
            return dict()
        if len(meas_files) > 1:
            msg = f"Unsupported: more than one measurement-file generated. Only the first will be read"
            warn(msg)
        return parse_mt0(self.open(meas_files[0], "r"))

    def run_sim_process(self) -> None:
        """Run a NGSpice sub-process, executing the simulation"""
        # Note the `nutbin` output format is dictated here
        cmd = shlex.split(f"{NGSPICE_EXECUTABLE} -b netlist.sp -r netlist.raw")
        return self.run_subprocess(cmd)


class FromStr:
    """Mix-in for creating `Enum`s from string values."""

    @classmethod
    def from_str(cls, s: str) -> "FromStr":
        reversed = {v.value: v for v in cls}
        if s not in reversed:
            msg = f"Invalid `{cls.__name__}`: `{s}`"
            raise ValueError(msg)
        return reversed[s]


class NumType(FromStr, Enum):
    """# Numeric Datatypes
    Values equal the strings used in NutBin data files."""

    REAL = "real"
    COMPLEX = "complex"


class Units(FromStr, Enum):
    """# Unit Types
    Values equal the strings used in NutBin data files."""

    DUMMY = "dummy"
    SWEEP = "sweep"
    SECONDS = "seconds"
    VOLTS = "voltage"
    AMPS = "current"
    HERTZ = "frequency"
    CELSIUS = "C"

    @classmethod
    def from_str(cls, s: str) -> "FromStr":
        reversed_l = {v.value: v for v in cls}
        if s not in reversed_l:
            return cls.DUMMY
        return reversed_l[s]


@dataclass
class VarSpec:
    """Variable Spec"""

    name: str
    units: Units


@dataclass
class NutBinAnalysis:
    """Analysis result from a NutBin file."""

    analysis_name: str  # Analysis name
    numtype: NumType  # Numeric type in `data` field
    data: Mapping[str, np.ndarray]  # Signal name => data
    units: Mapping[str, Units]  # Signal name => units


def parse_nutbin(f: IO) -> Mapping[str, NutBinAnalysis]:
    """Parse a `nutbin` format set of simulation results.
    Returns results as a dictionary from `analysis_name` to `NutBinAnalysis`.
    Note this is paired with the simulator invocation commands, which include `format=nutbin`."""

    # Parse per-file header info
    # First 2 lines are ascii one line statements

    # And parse the rest of the file per-analysis
    rv = {}
    while f:
        _title = f.readline()  # Title, ignored
        _date = f.readline()  # Run date, ignored
        plotname = f.readline().decode("ascii")  # Simulation name
        if len(plotname) == 0:
            break
        an = parse_nutbin_analysis(f, plotname)
        rv[an.analysis_name] = an
    return rv


def parse_nutbin_analysis(f: IO, plotname: str) -> NutBinAnalysis:
    """Parse a `NutBinAnalysis` from an open nutbin-format file `f`."""

    # Next 4 lines are also ascii one line statements
    # Parse the `Flags` field, which primarily includes the numeric datatype
    flags = f.readline().decode("ascii")
    flags = flags.split()
    if len(flags) != 2 or flags[0] != "Flags:":
        raise ValueError(f"Invalid flags {flags}")
    numtype = NumType.from_str(flags[1])
    nptypes = {NumType.REAL: float, NumType.COMPLEX: complex}
    nptype = nptypes[numtype]

    # Parse the number of variables and points
    num_vars_line = f.readline()  # No. Variables:   [nvar]
    num_pts_line = f.readline()  # No. Points:      [npts]
    sim_name = plotname.split("`")[-1].split("'")[0]

    # Find the number of variables and number of points
    num_vars = int(
        re.match(
            r"No. Variables:\s+(?P<num_vars>\d+)\s*\n",
            num_vars_line.decode("ascii"),
        ).group("num_vars")
    )
    num_pts = int(
        re.match(
            r"No. Points:\s+(?P<num_pts>\d+)\s*\n",
            num_pts_line.decode("ascii"),
        ).group("num_pts")
    )

    # Decode the variables spec, looks like the following
    # Variables: [Variable idx] [Variable name] [units] [optional_flags]
    f.readline()
    var_specs = []
    for i in range(num_vars):
        var_specs.append(_read_var_spec(f.readline().decode("ascii")))

    # Read the binary data, should look like the following:
    # Binary: \n[Binary data]
    binary_line = f.readline().decode("ascii")
    assert binary_line == "Binary:\n"
    # Data is big endian
    bin_data = np.fromfile(
        f, dtype=np.dtype(nptype).newbyteorder("<"), count=num_vars * num_pts
    )
    data = {}
    units = {}
    for i, var in enumerate(var_specs):
        data[var.name] = bin_data[i::num_vars]
        units[var.name] = var.units

    return NutBinAnalysis(
        analysis_name=sim_name,
        numtype=numtype,
        data=data,
        units=units,
    )


def _read_var_spec(line: str) -> VarSpec:
    """Read a Variable spec line from the input
    and return the name and the units."""
    m = re.match(
        r"\s+(?P<idx>\d+)\s+(?P<name>\S+)\s+(?P<units>\S+)(?P<rest>.*)\n", line
    )
    return VarSpec(name=m.group("name"), units=Units.from_str(m.group("units")))


def parse_mt0(file: IO) -> Dict[str, float]:
    """Parse an (open) "mt0-format" measurement-file into a set of {name: value} pairs."""

    file.readline()  # Header
    file.readline()  # Netlist Title
    keys = file.readline()  # Measurement Names Line
    keys = keys.split()
    values = file.readline()  # Measurement Values Line

    def convert(s: str) -> float:
        """Convert a string to a float, converting failing cases to `NaN`"""
        try:
            return float(s)
        except:
            return float("NaN")

    values = [convert(s) for s in values.split()]
    return dict(zip(keys, values))
