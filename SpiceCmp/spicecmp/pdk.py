# Std-Lib Imports
from dataclasses import dataclass
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
from .mos import MosModel


@dataclass
class Pdk:
    """Process Development Kit Dataclass
    Specifies corner names, include-file-paths, parameters, and supported simulators."""

    # Process Name
    name: str
    # Model-library paths, per simulator
    model_libs: Dict[Simulators, Path]
    # Mapping from enumerated corners to their lib-section names
    corners: Dict[Corner, str]
    # List of supported simulation classes
    supported_simulators: List[Simulator]
    # Transistor mapping from (type, vth) to module-definition
    xtors: Dict[MosModel, h.ExternalModule]
    # Supply voltage value
    vdd: str

    def include(self, sim: Simulators, corner: Corner) -> Control:
        """Generate a `LibInclude` statement for the combination of `sim` and `corner`."""
        path = self.model_libs.get(sim, None)
        if path is None:
            raise ValueError(f"Unsupported simulator {sim} for Pdk {self}")
        path = str(path)

        section = self.corners.get(corner, None)
        if section is None:
            raise ValueError(f"Unsupported corner {corner} for Pdk {self}")

        lib = LibInclude(path=path, section=section)
        return Control(lib=lib)


@h.paramclass
class PdkParam:
    """A single-element `paramclass`, for generators whose sole parameter is a `Pdk`.
    FIXME: this doesn't totally work as a generator parameter yet,
    seemingly due to the types of some of the `Pdk` fields not playing nice."""

    pdk = h.Param(dtype=Pdk, desc="PDK Object")


@dataclass
class PdkGeneratorWrapper:
    """A wrapper to call an Hdl21 `Generator` inside a `Pdk`-dependent function.
    FIXME: Ideally `Pdk` could just be a parameter to `Generator` object instead,
    and we wouldn't need this type. But can't be, yet."""

    # Outer, wrapper function, of the signature `def wrapper(pdk: Pdk) -> h.Module`
    wrapper: Callable[[Pdk], h.Module]
    # Inner Hdl21 Generator, really just used for naming.
    inner: h.Generator

    def __call__(self, pdk: Pdk) -> h.Module:
        return self.wrapper(pdk)

    @property
    def name(self):
        return self.inner.name
