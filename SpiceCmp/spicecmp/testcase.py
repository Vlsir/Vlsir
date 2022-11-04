# Std-Lib Imports
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, Callable

# Local Imports
from .errormode import ErrorMode
from .corner import Corner


@dataclass
class Test:
    """# Simulation Comparison Test"""

    name: str  # Test Name
    # Run-Function
    run_func: Callable[["TestCaseRun"], None]
    # Measurement-Manipulation Function
    meas_func: Callable[[Dict[str, float]], Dict[str, float]]

    def case(self, **kwargs) -> "TestCase":
        """Create a derived `TestCase` with parameters `kwargs`."""
        return TestCase(test=self, **kwargs)

    @property
    def dirname(self) -> str:
        """Run-directory name, gathered from the test-case data."""
        # Format: TestCaseName_DutName_TT_25
        return f"{self.name}_{self.dut.name}_{self.corner.value}_{str(self.temper)}"


@dataclass
class TestCase:
    """# Test Case
    Combination of a `Test`, and the conditions under which it is run."""

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
        """Run-directory name, gathered from the test-case data."""
        # Format: TestCaseName_DutName_TT_25
        return f"{self.name}_{self.dut.name}_{self.corner.value}_{str(self.temper)}"


@dataclass
class TestCaseRun:
    """# Test Case Run
    Execution of a `TestCase` with a particular PDK & simulator."""

    testcase: TestCase
    pdk: "Pdk"
    simulator: "Simulator"
    parentdir: Path
    errormode: ErrorMode
