# Std-Lib Imports
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Callable

# "Friend" VLSIR-World Imports
from vlsir.spice_pb2 import Control, LibInclude
from vlsirtools.spice import SupportedSimulators
import hdl21 as h
from hdl21.primitives import MosType, MosVth

# Local Imports
from .corner import Corner
from .pdk import Pdk, MosModel
from .simulator import Simulator, Simulators


@dataclass
class PdkSimCombo:
    """Combination of a PDK and a supported simulator."""

    pdk: Pdk
    sim: Simulator

    def __post_init__(self):
        if self.sim.enum not in self.pdk.supported_simulators:
            msg = f"Unsupported simulator {self.sim} for PDK {self.pdk.name}"
            raise RuntimeError(msg)

    @property
    def name(self):
        return self.pdk.name + "_" + self.sim.enum.value
