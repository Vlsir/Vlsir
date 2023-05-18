"""
# VlsirTools Pytest Utilities 

Primarily adds and parses the command-line options for enabling and disabling `vlsirtools.spice` simulators. 
To use these utilities, add the following to your `conftest.py`:

```python
from vlsirtools.pytest import (
    pytest_configure,
    pytest_addoption,
    pytest_collection_modifyitems,
)
```

See VlsirTools' own `conftest.py` for an example.  
With these functions included, by those names, in `conftest.py`, invocations of `pytest` can use: 

* The `--simulator_test_mode` command-line option 
  * Values are `required`, `if_available`, or `disabled`
* Markers for each supported simulator
  * `spectre`, `xyce`, and `ngspice` are currently supported
* Command-line options for each supported simulator, to override `simulator_test_mode`


Examples: 

```
pytest --simulator_test_mode disabled       # Disables all simulation tests
pytest --simulator_test_mode required       # Requires all simulation tests
pytest --simulator_test_mode if_available   # Runs tests on available simulators

pytest --simulator_test_mode if_available --ngspice required  # Requires ngspice, tests all others available 
pytest --simulator_test_mode required --xyce disabled         # Disables xyce, requires all others
pytest --simulator_test_mode disabled --spectre required      # Requires spectre, disables all others
```

"""


import pytest
from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass

import vlsirtools.spice as vsp


class SimulatorTestMode(Enum):
    """# Enumerated Per-Simulator Test Modes"""

    REQUIRED = "required"
    IF_AVAILABLE = "if_available"
    DISABLED = "disabled"

    def skip(self) -> bool:
        """Boolean indication of whether this Simulator should be skipped."""
        return self.value == "disabled"


@dataclass
class Simulator:
    marker: str
    # Simulator name/ command-line option/ pytest-marker name
    available: bool
    # Boolean indicator of availability in the current environment

    def getoption(self, config: "Config") -> Optional["SimulatorTestMode"]:
        """Get this simulator's pytest option"""
        option = config.getoption(f"--{self.marker}")
        if option is None:
            return None
        return SimulatorTestMode(option)


# The "registry" of supported simulators and their availability in the current process environment
# In other words, the stuff about the simulators that we know before we start running tests
simulators: Dict[str, Simulator] = {
    s.marker: s
    for s in [
        Simulator(marker="spectre", available=vsp.spectre.available()),
        Simulator(marker="xyce", available=vsp.xyce.available()),
        Simulator(marker="ngspice", available=vsp.ngspice.available()),
    ]
}


class Why(Enum):
    """# Enumerated reasons to be enabled or disabled."""

    DISABLED = "DISABLED"
    NOT_AVAILABLE = "NOT_AVAILABLE"
    AVAILABLE = "AVAILABLE"
    REQUIRED = "REQUIRED"

    def enabled(self) -> bool:
        """# Boolean enabledness indicator"""
        if self in (Why.DISABLED, Why.NOT_AVAILABLE):
            return False
        if self in (Why.REQUIRED, Why.AVAILABLE):
            return True
        raise ValueError(f"Unknown Why: {self}")


@dataclass
class SimulatorSettingPair:
    """# Simulator-Setting Pair
    The combination of a `Simulator` and its current test-setting."""

    simulator: Simulator  # The simulator
    mode: SimulatorTestMode  # Configured test mode
    enabled: bool  # Boolean indicator of whether this simulator is enabled
    why: Why  # Why this simulator is enabled or disabled

    @staticmethod
    def new(simulator: Simulator, mode: SimulatorTestMode) -> "SimulatorSettingPair":
        """# Create a SimulatorSettingPair from a Simulator and a test mode."""

        # Mostly suss out the reason "why"
        if mode == SimulatorTestMode.DISABLED:
            why = Why.DISABLED
        elif mode == SimulatorTestMode.IF_AVAILABLE:
            why = Why.AVAILABLE if simulator.available else Why.NOT_AVAILABLE
        elif mode == SimulatorTestMode.REQUIRED:
            why = Why.REQUIRED
        else:
            raise ValueError(f"Unknown mode: {mode}")

        return SimulatorSettingPair(
            simulator=simulator,
            mode=mode,
            enabled=why.enabled(),
            why=why,
        )


def pytest_configure(config):
    """# PyTest Configuration
    Adds a marker for each supported simulator."""

    for s in simulators.keys():
        config.addinivalue_line("markers", f"{s}")


def pytest_addoption(parser):
    """PyTest Command-Line Option Additions"""

    # Add the `--simulator_test_mode` option
    parser.addoption(
        "--simulator_test_mode",
        action="store",
        default=SimulatorTestMode.IF_AVAILABLE.value,
        help=f"Simulation test mode. One of {[m.value for m in SimulatorTestMode]}.",
    )
    # Add an option for each supported simulator
    for s in simulators.keys():
        parser.addoption(
            f"--{s}",
            action="store",
            default=None,
            help=f"{s.title()} test mode. One of {[m.value for m in SimulatorTestMode]}.",
        )


# Skip markers
skip_disabled = pytest.mark.skip(reason="Disabled by command-line simulator options")
skip_not_available = pytest.mark.skip(
    reason="Simulator not available & not required by command-line options"
)


def pytest_collection_modifyitems(config, items):
    """Examine each test item, and skip them based on `SimulatorSettings`."""

    # First grab the "overall mode"
    default_mode = SimulatorTestMode(config.getoption("--simulator_test_mode"))

    # Now check for any simulator-specific overrides, and turn them into setting-pairs
    simulator_settings = {
        s.marker: SimulatorSettingPair.new(
            simulator=s, mode=s.getoption(config) or default_mode
        )
        for s in simulators.values()
    }

    # print(f"Testing with simulation settings:")
    # print(simulator_settings)

    # Alright finally the point: apply the `skip` attribute to test we don't wanna run.
    for item in items:
        for marker in simulators.keys():
            if marker in item.keywords:
                pair = simulator_settings[marker]
                if pair.why == Why.DISABLED:
                    item.add_marker(skip_disabled)
                elif pair.why == Why.NOT_AVAILABLE:
                    item.add_marker(skip_not_available)
