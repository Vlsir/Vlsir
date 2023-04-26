"""
# VlsirTools Pytest Configuration 
Primarily adds and parses the command-line options for enabling and disabling `vlsirtools.spice` simulators.  
Example usage: 
```
pytest --simulator_test_mode disabled       # Disables all simulation tests
pytest --simulator_test_mode required       # Requires all simulation tests
pytest --simulator_test_mode if_available   # Runs tests on available simulators
```
Each `SupportedSimulator` can be individually overridden, e.g.:
```
pytest --simulator_test_mode if_available --ngspice required  # Requires ngspice, tests all others available 
pytest --simulator_test_mode required --ngspice disabled      # Disables ngspice, requires all others
```
"""


import pytest
from enum import Enum
from typing import Callable, Dict, Optional
from dataclasses import dataclass

import vlsirtools


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

    def getoption(self, config: "Config") -> Optional[str]:
        """Get this simulator's pytest option"""
        return config.getoption(f"--{self.marker}")


@dataclass
class SimulatorSettingPair:
    """# Simulator-Setting Pair
    The combination of a `Simulator` and its current test-setting."""

    simulator: Simulator
    mode: SimulatorTestMode

    def skip(self) -> bool:
        """Boolean indication of whether this simulator-setting pair should be skipped."""
        return self.mode == SimulatorTestMode.DISABLED or (
            self.mode == SimulatorTestMode.IF_AVAILABLE and not self.simulator.available
        )


simulators = [
    Simulator(marker="spectre", available=vlsirtools.spice.spectre.available()),
    Simulator(marker="xyce", available=vlsirtools.spice.xyce.available()),
    Simulator(marker="ngspice", available=vlsirtools.spice.ngspice.available()),
]
simulators: Dict[str, Simulator] = {s.marker: s for s in simulators}


def pytest_configure(config):
    config.addinivalue_line("markers", "simulator_test_mode")

    for s in simulators.keys():
        config.addinivalue_line("markers", f"{s}")


def pytest_addoption(parser):
    parser.addoption(
        "--simulator_test_mode",
        action="store",
        default=SimulatorTestMode.IF_AVAILABLE.value,
        help=f"Simulation test mode. One of {[m.value for m in SimulatorTestMode]}.",
    )
    for s in simulators.keys():
        parser.addoption(
            f"--{s}",
            action="store",
            default=None,
            help=f"{s.title()} test mode. One of {[m.value for m in SimulatorTestMode]}.",
        )


def pytest_collection_modifyitems(config, items):
    """Examine each test item, and skip them based on `SimulatorSettings`."""

    # First grab the "overall mode"
    default_mode = SimulatorTestMode(config.getoption("--simulator_test_mode"))

    # Convert this into a per-simulator dictionary of settings
    simulator_settings: Dict[str, SimulatorSettingPair] = {
        s.marker: default_mode for s in simulators.values()
    }

    # Now check for any simulator-specific overrides
    for marker, simulator in simulators.items():
        option = simulator.getoption(config)
        if option is not None:
            simulator_settings[marker] = SimulatorTestMode(option)

    # Alright finally the point: apply the `skip` attribute to test we don't wanna run.
    skipme = pytest.mark.skip(reason="Disabled by command-line simulator options")
    for item in items:
        for marker in simulators.keys():
            if marker in item.keywords:
                pair = simulator_settings[marker]
                if pair.skip():
                    item.add_marker(skipme)
