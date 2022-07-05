""" 
# Simulator State Base-Class 
"""

# Std-Lib Imports
import asyncio, os, tempfile, subprocess
from typing import Union, Optional, Awaitable, List
from enum import Enum
from pathlib import Path
from textwrap import dedent
from dataclasses import dataclass, field

# Local/ Project Dependencies
import vlsir.spice_pb2 as vsp
from . import sim_data as sd
from . import SimResultUnion, SupportedSimulators, SimOptions


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
    async def sim(
        cls, inp: vsp.SimInput, opts: Optional[SimOptions] = None
    ) -> Awaitable[SimResultUnion]:
        """ Sim-invoking class method. 
        Creates an instance of `cls` as a context manager, run in its simulation directory. 
        This should be invoked by typical implementations of a free-standing `sim` function. """

        if opts is None:  # Create the default `SimOptions`
            opts = SimOptions(simulator=cls.enum())

        # Create the simulation class, and execute its main `run` method in `rundir`
        async with cls(inp=inp, rundir=opts.rundir) as sim:
            results = await sim.run()

        # FIXME: And handle output formatting, when these `Sim` classes are actually compatible
        # if opts.fmt == ResultFormat.VLSIR_PROTO:
        #     return results.to_proto()
        return results

    def __init__(self, inp: vsp.SimInput, rundir: Optional[os.PathLike] = None) -> None:
        self.inp = inp
        self.rundir = rundir
        self.prevdir = os.getcwd()
        self.top = None
        self.subprocesses: List[asyncio.Process] = []
        self.all_procs_launched = False

    # def __enter__(self) -> "Sim":
    async def __aenter__(self):  # Yes, that is the name of the async version of "__enter__"
        """ On entry, create and navigate to a directory for the sim's files.  """
        if self.rundir is not None:
            self.rundir = Path(self.rundir).absolute()
            if not self.rundir.exists():
                os.makedirs(self.rundir)
            os.chdir(self.rundir)
        else:  # Create a new temp directory
            self.rundir = tempfile.TemporaryDirectory()
            os.chdir(self.rundir.name)
        print("IN SIM __ENTER__")
        print(os.getcwd())
        return self

    # def __exit__(self, _type, _value, _traceback):
    async def __aexit__(self, _type, _value, _traceback):  # Yes, that is the name of the async version of "__exit__"
        """ On exit, clean up our temporary directory, and navigate back to its predecessor.  """
        print("IN SIM __EXIT__")
        print(os.getcwd())
        print("AWAITING PROCESSES")
        print(f"SUBPROCS: {self.subprocesses}")
        # Ensure all of our sub-processes are finished. FIXME: this really just makes sure they are *launched*, could die during output parsing etc 
        while not self.all_procs_launched:
            print(f"NOT LAUNCHED, SLEEPING")
            await asyncio.sleep(0.1)
        # await asyncio.gather(*self.subprocesses)
        print("GATHER FINISHED")
        print(os.getcwd())
        os.chdir(self.prevdir)
        if isinstance(self.rundir, tempfile.TemporaryDirectory):
            self.rundir.cleanup()
        print("DONE WITH __EXIT__")
        print(os.getcwd())

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

    def run(self) -> Awaitable[SimResultUnion]:
        """ Primary invocation method. 
        Run the specified `SimInput` in directory `self.rundir`, returning its results. 
        Performs initial setup, then hands off to the simulator-specific sub-class's `_run` method. """

        # Setup
        self.validate_top()

        # And hand off to the simulator-specific sub-class's `_run` method.
        return self._run()

    async def _run(self) -> Awaitable[SimResultUnion]:
        raise NotImplementedError("`Sim` subclasses must implement `_run`")

    async def run_subprocess(self, cmd: str) -> Awaitable[None]:
        """ Asynchronously run a shell subprocess invoking command `cmd`. """
        try:
            print("LAUNCHING SUBPRC")
            print(os.getcwd())
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            self.subprocesses.append(proc)
            stdout, stderr = await proc.communicate()
            print("SUBPRC DONE(?)")
            print(os.getcwd())

            # The async subprocess module does not raise Python exceptions: check the return code instead. 
            if proc.returncode != 0:
                from . import SimError
                raise SimError(sim=self, stdout=stdout, stderr=stderr)
            return None

        except Exception as e:
            raise
