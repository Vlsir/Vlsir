# Std-Lib Imports
from textwrap import dedent
from copy import deepcopy
from dataclasses import dataclass, asdict
from enum import Enum, auto
from pathlib import Path
from typing import List, Any, Dict, Tuple, Callable

# Local Imports 
from .corner import Corner 

@dataclass
class Test:
    """ # Simulation Comparison Test """

    name: str  # Test Name
    run_func: Callable  # Run-Function
    meas_func: Callable  # Measurement-Manipulation Function

    def case(self, **kwargs) -> "TestCase":
        """ Create a derived `TestCase` with parameters `kwargs`. """
        return TestCase(test=self, **kwargs)

    @property
    def dirname(self) -> str:
        """ Run-directory name, gathered from the test-case data. """
        # Format: TestCaseName_DutName_TT_25
        return f"{self.name}_{self.dut.name}_{self.corner.value}_{str(self.temper)}"


@dataclass
class TestCase:
    """ # Test Case 
    Combination of a `Test`, and the conditions under which it is run. """

    test: Test  # Reference to the parent `Test`
    dut: Any  # Device under test, or generator thereof
    corner: Corner  # PVT Corner
    temper: int  # Temperature

    @property
    def name(self) -> str:
        return self.test.name

    @property
    def run_func(self) -> str:
        return self.test.run_func

    @property
    def meas_func(self) -> str:
        return self.test.meas_func

    @property
    def dirname(self) -> str:
        """ Run-directory name, gathered from the test-case data. """
        # Format: TestCaseName_DutName_TT_25
        return f"{self.name}_{self.dut.name}_{self.corner.value}_{str(self.temper)}"

