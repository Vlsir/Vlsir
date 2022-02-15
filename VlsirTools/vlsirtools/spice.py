""" 
# Spice-Class Simulator Interface 

Base class(es), utilities, and shared functionality for simulators. 
"""

# Std-Lib Imports
import os, tempfile
from typing import IO, Union
from pathlib import Path

# Local/ Project Dependencies
import vlsir
from .sim_data import SimResult, ResultFormat


class Sim:
    """
    # Simulator State Base-Class 

    Shared basic functionality for simulators, including: 
    * Creating temporary run-directories, and named files within them 
    * Finding a valid top-level module 
    * Exception/ Error types for common simulator errors

    Typical usage is within a `sim` function, and particularly within a `with` block 
    dictating its lifetime. For example, using the theoretical sub-class `SomeSimClass`: 

    ```python
    def sim(inp: vlsir.spice.SimInput) -> vlsir.spice.SimResult:
        with SomeSimClass(inp) as sim:
            return sim.run()
    ```

    The `Sim` context manager creates and navigates to a temporary directory in the OS-conventional locations, 
    and cleans up all simulation files after itself. 

    The interface between the `Sim` base-class and its implementing sub-class is such that:

    * `run` is the primary entry point, implemented by this base class. 
      * After initial checks and setup, `run` hands off to a sub-class-specific `_run` method.
    * Creating a file in the sim-directory requires calling the `open` method on `Sim` 
      * I.e. call `self.open(filename, "w")`, rather than the built-in `open` function.
    * All other methods are implemented by the sub-class.
    * At no point should the sub-classes need to know any more about the `Sim` base-class, or call any of its `super` methods. 
    """

    def __init__(self, inp: vlsir.spice.SimInput) -> None:
        self.inp = inp
        self.tmpdir = None
        self.prevdir = os.getcwd()
        self.top = None

    def __enter__(self) -> "Sim":
        """ On entry, create and navigate to a temporary directory for the sim's files.  """
        self.tmpdir = tempfile.TemporaryDirectory()
        os.chdir(self.tmpdir.name)
        return self

    def __exit__(self, _type, _value, _traceback):
        """ On exit, clean up our temporary directory, and navigate back to its predecessor.  """
        os.chdir(self.prevdir)
        self.tmpdir.cleanup()

    def open(self, fname: str, mode: str) -> IO:
        """ Open a file in the temporary directory, in read/write-mode `mode`. """
        return open(Path(self.tmpdir.name) / fname, mode=mode)

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
            raise RuntimeError(f"Top-level module `{self.inp.top}` not found")

    def run(self) -> Union[SimResult, vlsir.spice.SimResult]:
        """ Primary invocation method. 
        Run the specified `SimInput` in directory `self.tmpdir`, returning its results. 
        Performs initial setup, then hands off to the simulator-specific sub-class's `_run` method. """

        # Setup
        self.validate_top()
        prev_dir = os.getcwd()
        os.chdir(self.tmpdir.name)

        # And hand off to the simulator-specific sub-class's `_run` method.
        return self._run()

    def _run(self) -> Union[SimResult, vlsir.spice.SimResult]:
        raise NotImplementedError("Sub-classes must implement `_run`")


class SimError(Exception):
    """ Exception raised when a simulation fails. """

    pass
