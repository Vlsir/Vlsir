""" 
# Simulator State Base-Class 
"""

# Std-Lib Imports
import asyncio, os, tempfile
from typing import Optional, Awaitable, List, IO
from pathlib import Path

# Local/ Project Dependencies
import vlsir.spice_pb2 as vsp
import vlsir.circuit_pb2 as vckt
from . import SimResultUnion, SupportedSimulators, SimOptions, ResultFormat


class Sim:
    """
    # Simulator State Base-Class

    Shared basic functionality for simulators, including:
    * Creating run-directories, and named files within them
    * Asynchronously invoking simulation subprocesses
    * Finding a valid top-level module
    * Exception/ Error types for common simulator errors

    Each `SupportedSimulator` is generally implemented as a sub-class of `Sim`.
    The interface between the `Sim` base-class and its implementing sub-class is such that:

    * The base-class `Sim.sim` class-method should really be the entry point for everything! It will:
      * Create the class instance
      * Set up the run-directory via `setup()`
      * Invoke the primary sub-class-specific method `run`
      * After completion, perform any clean-up activites via `cleanup()`.
    * All other methods are implemented by the sub-classes.
      * The only required method is `run`, which performs the actual simulation.
      * Other methods will generally do things including: writing simulator-specific netlist-content, launching a sim process, parsing results.
      * At no point should the sub-classes need to know any more about the `Sim` base-class, or call any of its `super` methods.
    """

    @classmethod
    def enum(cls) -> SupportedSimulators:
        raise NotImplementedError

    @classmethod
    async def sim(
        cls, inp: vsp.SimInput, opts: Optional[SimOptions] = None
    ) -> Awaitable[SimResultUnion]:
        """Sim-invoking class method.
        Creates an instance of `cls` as a context manager, run in its simulation directory.
        This should be invoked by typical implementations of a free-standing `sim` function."""

        if opts is None:  # Create the default `SimOptions`
            opts = SimOptions(simulator=cls.enum())

        # Create the simulation-class instance, and execute its main `run` method
        sim = cls(inp=inp, opts=opts)
        try:
            sim.setup()
            results = await sim.run()
        finally:
            sim.cleanup()

        # FIXME: we shouldn't need this `isinstance`; get Xyce to return `sd.SimResult` and decide whether to convert here
        if opts.fmt == ResultFormat.VLSIR_PROTO and not isinstance(
            results, vsp.SimResult
        ):
            return results.to_proto()
        return results

    def run(self) -> Awaitable[SimResultUnion]:
        raise NotImplementedError("`Sim` subclasses must implement `run`")

    def __init__(self, inp: vsp.SimInput, opts: SimOptions) -> None:
        self.inp = inp
        self.opts = opts
        self.rundir = opts.rundir
        self.tmpdir: Optional[tempfile.TemporaryDirectory] = None
        self.top: Optional[vckt.Module] = None
        self.subprocesses: List[asyncio.Process] = []

    def setup(self):
        """Perform simulation setup, including the simulation directory and top-level Module validation."""

        # Set up the simulation directory
        if self.rundir is not None:  # User-specified `rundir`
            self.tmpdir = None
            self.rundir = Path(self.rundir).absolute()
            if not self.rundir.exists():
                os.makedirs(self.rundir)
        else:  # Create a new temp directory
            self.tmpdir = tempfile.TemporaryDirectory()
            self.rundir = Path(self.tmpdir.name).absolute()

        # Ensure that we have a valid top-level module
        self.validate_top()

    def cleanup(self):
        """On completion, clean up after ourselves."""
        if self.tmpdir is not None:
            self.tmpdir.cleanup()

    def validate_top(self) -> None:
        """Ensure that the `top` module exists,
        and adheres to the "Spice top-level" port-interface: a single port for ground / VSS / node-zero.
        Sets the `self.top` attribute when successful, or raises a `RuntimeError` when not."""

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
            msg = f"Top-level module `{self.inp.top}` not found among Modules {names}"
            raise RuntimeError(msg)

    async def run_subprocess(self, cmd: str) -> Awaitable[None]:
        """Asynchronously run a shell subprocess invoking command `cmd`.
        All subprocesses are run in `self.rundir`, and tracked in the list `self.subprocesses`."""

        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.rundir),
        )
        self.subprocesses.append(proc)
        stdout, stderr = await proc.communicate()

        # The async subprocess module does not raise Python exceptions: check the return code instead.
        if proc.returncode != 0:
            from . import SimError

            raise SimError(sim=self, stdout=stdout, stderr=stderr)
        return None

    def open(self, name: str, mode: str = "r") -> IO:
        """Open a file in the simulation directory."""
        return self.path(name).open(mode)

    def path(self, name: str) -> Path:
        """Return a path in the simulation directory."""
        return Path(self.rundir) / Path(name)

    def glob(self, pat: str):
        """Return a list of paths in the simulation directory matching `pat`."""
        return Path(self.rundir).glob(pat)
