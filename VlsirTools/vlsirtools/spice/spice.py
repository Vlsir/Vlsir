""" 
# Spice-Class Simulator Interface 

Base class(es), utilities, and shared functionality for simulators. 
"""

# Std-Lib Imports
import os, tempfile, subprocess
from typing import Union, Optional
from enum import Enum
from pathlib import Path
from textwrap import dedent
from dataclasses import dataclass, field

# Local/ Project Dependencies
import vlsir.spice_pb2 as vsp
from vlsir.spice_pb2 import *  # Not used here intentionally, but "re-exported"
from . import sim_data as sd


class ResultFormat(Enum):
    """ Enumerated Result Formats """

    SIM_DATA = "sim_data"  # Types defined in the `sim_data` module
    VLSIR_PROTO = "vlsir_proto"  # `vsp.SimResults` and related protobuf-defined types


# Union of the two result-types, returned by many simulation methods
SimResultUnion = Union[vsp.SimResult, sd.SimResult]


class AnalysisType(Enum):
    """ Enumerated Analysis-Types 
    Corresponding to the entries in the `Analysis` type-union. """

    DC = "dc"
    AC = "ac"
    TRAN = "tran"
    MONTE = "monte"
    SWEEP = "sweep"
    CUSTOM = "custom"


class SupportedSimulators(Enum):
    """ Enumerated, Internally-Defined Spice-Class Simulators """

    SPECTRE = "spectre"
    XYCE = "xyce"


def default() -> Optional[SupportedSimulators]:
    """ Get the default simulator, for this Python-process and its environment. 
    This largely consists of a priority-ordered walk through `SupportedSimulators`, 
    returning the first whose `available()` method indicates its availability. 
    Returns `None` if no such simulator appears available. """

    from .spectre import available as spectre_available
    from .xyce import available as xyce_available

    if spectre_available():
        return SupportedSimulators.SPECTRE
    if xyce_available():
        return SupportedSimulators.XYCE
    return None  # Nothing found


@dataclass
class SimOptions:
    """ Options to `vsp.Sim` which are *not* passed along to the simulator. 
    I.e. options which effect the Python-process invoking simulation, 
    but not the internals of the simulation itself. """

    # Simulator. FIXME: debatable whether to include this.
    simulator: SupportedSimulators = field(default_factory=default)

    # In-memory results format
    fmt: ResultFormat = ResultFormat.VLSIR_PROTO

    # Simulation run-directory. Uses a `tempdir` if unspecified.
    rundir: Optional[os.PathLike] = None


def sim(inp: vsp.SimInput, opts: Optional[SimOptions] = None) -> SimResultUnion:
    """
    Execute a `vlir.spice.Sim`. 
    Dispatches across `SupportedSimulators` specified in `SimOptions` `opts`. 
    Uses the default `Simulator` as detected by the `default` method if no `simulator` is specified.
    """
    if opts is None:  # Create the default `SimOptions`
        opts = SimOptions()

    if opts.simulator is None:  # If we didn't specify or find a simulator, fail.
        msg = f"vlsirtools.spice: No Supported Simulators available for call to `sim()`"
        raise RuntimeError(msg)

    # Get the per-simulator callable
    if opts.simulator == SupportedSimulators.XYCE:
        from .xyce import sim
    elif opts.simulator == SupportedSimulators.SPECTRE:
        from .spectre import sim
    else:
        raise ValueError(f"Unsupported simulator: {opts.simulator}")

    # And do the real work, invoking the target simulator
    return sim(inp, opts)


class Sim:
    """
    # Simulator State Base-Class 

    Shared basic functionality for simulators, including: 
    * Creating run-directories, and named files within them 
    * Finding a valid top-level module 
    * Exception/ Error types for common simulator errors

    Each `SupportedSimulator` is generally implemented as a (python) module including:

    * A `sim` free-standing function, and 
    * An implementation sub-class of `Sim` which manages run-state and simulator-specific behavior 

    The latter generally should (and generally does) call the classmethod `Sim.sim`, 
    which creates and navigates to a specified or temporary directory, 
    and cleans up all simulation files after itself. 

    The interface between the `Sim` base-class and its implementing sub-class is such that:

    * `run` is the primary entry point, implemented by this base class. 
      * After initial checks and setup, `run` hands off to a sub-class-specific `_run` method.
    * When used as a context manager via `with`, all internal activity occurs within the simulation's temporary directory.
      * System-calls to create and manage files can be made without knowledge of this directory.
      * E.g. `open('netlist', 'w')` will land `netlist` in the temporary directory.
    * All other methods are implemented by the sub-classes. 
      * No requirements or conventions are placed on their names or activities. 
      * Such methods will generally do things including: writing simulator-specific netlist-content, launching a sim process, parsing results. 
      * At no point should the sub-classes need to know any more about the `Sim` base-class, or call any of its `super` methods. 
    """

    @classmethod
    def enum(cls) -> SupportedSimulators:
        raise NotImplementedError

    @classmethod
    def sim(
        cls, inp: vsp.SimInput, opts: Optional[SimOptions] = None
    ) -> SimResultUnion:
        """ Sim-invoking class method. 
        Creates an instance of `cls` as a context manager, run in its simulation directory. 
        This should be invoked by typical implementations of a free-standing `sim` function. """

        if opts is None:  # Create the default `SimOptions`
            opts = SimOptions(simulator=cls.enum())

        # Create the simulation class, and execute its main `run` method in `rundir`
        with cls(inp=inp, rundir=opts.rundir) as sim:
            results = sim.run()

        # FIXME: And handle output formatting, when these `Sim` classes are actually compatible
        # if opts.fmt == ResultFormat.VLSIR_PROTO:
        #     return results.to_proto()
        return results

    def __init__(self, inp: vsp.SimInput, rundir: Optional[os.PathLike] = None) -> None:
        self.inp = inp
        self.rundir = rundir
        self.prevdir = os.getcwd()
        self.top = None

    def __enter__(self) -> "Sim":
        """ On entry, create and navigate to a directory for the sim's files.  """
        if self.rundir is not None:
            self.rundir = Path(self.rundir).absolute()
            if not self.rundir.exists():
                os.makedirs(self.rundir)
            os.chdir(self.rundir)
        else:  # Create a new temp directory
            self.rundir = tempfile.TemporaryDirectory()
            os.chdir(self.rundir.name)
        return self

    def __exit__(self, _type, _value, _traceback):
        """ On exit, clean up our temporary directory, and navigate back to its predecessor.  """
        os.chdir(self.prevdir)
        if isinstance(self.rundir, tempfile.TemporaryDirectory):
            self.rundir.cleanup()

    def validate_top(self) -> None:
        """ Ensure that the `top` module exists,
        and adheres to the "Spice top-level" port-interface: a single port for ground / VSS / node-zero. 
        Sets the `self.top` attribute when successful, or raises a `RuntimeError` when not. """

        if not self.inp.top:
            raise RuntimeError(f"No top-level module specified")

        found = False
        for module in self.inp.pkg.modules:
            if module.name == self.inp.top:
                found = True
                self.top = module
                if len(module.ports) != 1:
                    msg = f"`vlsir.SimInput` top-level module {self.inp.top} must have *one* (VSS) port - has {len(module.ports)} ports [{module.ports}]"
                    raise RuntimeError(msg)
                break

        if not found:
            names = [m.name for m in self.inp.pkg.modules]
            raise RuntimeError(
                f"Top-level module `{self.inp.top}` not found among Modules {names}"
            )

    def run(self) -> SimResultUnion:
        """ Primary invocation method. 
        Run the specified `SimInput` in directory `self.rundir`, returning its results. 
        Performs initial setup, then hands off to the simulator-specific sub-class's `_run` method. """

        # Setup
        self.validate_top()

        # And hand off to the simulator-specific sub-class's `_run` method.
        return self._run()

    def _run(self) -> SimResultUnion:
        raise NotImplementedError("`Sim` subclasses must implement `_run`")


class SimError(Exception):
    """ Exception raised when a simulation fails. """

    pass


class SimProcessError(SimError):
    """ Exception raised when an external simulator process fails. """

    def __init__(self, sim: Sim, e: subprocess.CalledProcessError) -> None:
        s = dedent(
            f"""
            rundir: {str(sim.rundir)}
            stdout: {str(e.stdout)}
            stderr: {str(e.stderr)}
        """
        )
        super().__init__(s)
        self.rundir = str(sim.rundir)
        self.stdout = e.stdout
        self.stderr = e.stderr

