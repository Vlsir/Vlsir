# Std-Lib Imports
from dataclasses import dataclass
from enum import Enum
from typing import List

# "Friend" VLSIR-World Imports
from vlsir.spice_pb2 import Control
from vlsirtools.spice import SupportedSimulators


class Simulators(Enum):
    """Enumerated Simulators tested for Comparison"""

    XYCE = "xyce"
    SPECTRE = "spectre"


@dataclass
class Simulator:
    """Data associated with each Simulator program.
    Generally file-system include-paths, control cards, and the like."""

    enum: Simulators  # Enumerated value/ name
    vlsirtools: SupportedSimulators  # Format-tag from `vlsirtools`
    ctrls: List[Control]  # Simulator control cards


xyce = Simulator(
    enum=Simulators.XYCE,
    vlsirtools=SupportedSimulators.XYCE,
    ctrls=[],
)
spectre = Simulator(
    enum=Simulators.SPECTRE,
    vlsirtools=SupportedSimulators.SPECTRE,
    ctrls=[],
)

simulators = [xyce, spectre]
