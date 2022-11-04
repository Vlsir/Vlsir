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
from .simulator import Simulator, Simulators


@dataclass(frozen=True, eq=True)
class MosModel:
    """Fields which dictate a Mos Model, at least in this context: mos-type and threshold."""

    mos_type: MosType
    mos_vth: MosVth

    @property
    def name(self):
        # Format: NMOS_STD, PMOS_HIGH, etc
        return f"{self.mos_type.value}_{self.mos_vth.value}"
