"""
# Sim Data 

A mirror of Spice Proto's Analysis Result objects for in-Python usage, 
using python data classes and numpy arrays.

Also provides round-tripping utilities between the two.
TODO: Go from proto -> sim_result
"""


from typing import List, Mapping, Union, ClassVar
from enum import Enum
from dataclasses import dataclass
import numpy as np

import vlsir


class AnalysisType(Enum):
    """Enumerated Analysis-Types
    Values are equal to the keys of the VLSIR `Analysis` type-union."""

    OP = "op"
    DC = "dc"
    AC = "ac"
    TRAN = "tran"
    NOISE = "noise"
    MONTE = "monte"
    SWEEP = "sweep"
    CUSTOM = "custom"


@dataclass
class OpResult:
    analysis_name: str
    data: Mapping[str, float]
    vlsir_type: ClassVar[AnalysisType] = AnalysisType.OP

    def to_proto(self) -> vlsir.spice.OpResult:
        res = vlsir.spice.OpResult(analysis_name=self.analysis_name)
        for k, v in self.data.items():
            res.signals.append(k)
            res.data.append(v)
        return res


@dataclass
class DcResult:
    analysis_name: str
    indep_name: str
    data: Mapping[str, np.ndarray]
    measurements: Mapping[str, float]
    vlsir_type: ClassVar[AnalysisType] = AnalysisType.DC

    def to_proto(self) -> vlsir.spice.DcResult:
        res = vlsir.spice.DcResult(
            analysis_name=self.analysis_name, indep_name=self.indep_name
        )
        for k, v in self.data.items():
            res.signals.append(k)
            for d in v:
                res.data.append(d)
        # TODO Add support for measurements
        return res


@dataclass
class TranResult:
    analysis_name: str
    data: Mapping[str, np.ndarray]
    measurements: Mapping[str, float]
    vlsir_type: ClassVar[AnalysisType] = AnalysisType.TRAN

    def to_proto(self) -> vlsir.spice.TranResult:
        res = vlsir.spice.TranResult(analysis_name=self.analysis_name)
        for k, v in self.data.items():
            res.signals.append(k)
            for d in v:
                res.data.append(d)
        # TODO Add support for measurements
        return res


@dataclass
class AcResult:
    analysis_name: str
    freq: np.ndarray
    data: Mapping[str, np.ndarray]
    measurements: Mapping[str, float]
    vlsir_type: ClassVar[AnalysisType] = AnalysisType.AC

    def to_proto(self) -> vlsir.spice.AcResult:
        raise NotImplementedError


@dataclass
class NoiseResult:
    analysis_name: str
    data: Mapping[str, np.ndarray]
    integrated_noise: Mapping[str, float]
    measurements: Mapping[str, float]
    vlsir_type: ClassVar[AnalysisType] = AnalysisType.NOISE

    def to_proto(self) -> vlsir.spice.AcResult:
        raise NotImplementedError


@dataclass
class SweepResult:
    vlsir_type: ClassVar[AnalysisType] = AnalysisType.SWEEP

    def __post_init__(self):
        raise NotImplementedError


@dataclass
class MonteResult:
    vlsir_type: ClassVar[AnalysisType] = AnalysisType.MONTE

    def __post_init__(self):
        raise NotImplementedError


@dataclass
class CustomAnalysisResult:
    """Custom Analysis "Results"
    No data is returned from these simulator-specific analyses;
    an empty `CustomAnalysisResult` is simply added to their overall results-list
    to pair with its input analysis, keeping all others aligned."""

    vlsir_type: ClassVar[AnalysisType] = AnalysisType.CUSTOM


# Type alias for the union of each result-type
AnalysisResult = Union[
    AcResult,
    DcResult,
    TranResult,
    OpResult,
    SweepResult,
    MonteResult,
    CustomAnalysisResult,
]


@dataclass
class SimResult:
    """Results from a Mult-Analysis `Sim`"""

    an: List[AnalysisResult]

    def to_proto(self) -> vlsir.spice.SimResult:
        res = vlsir.spice.SimResult()
        for a in self.an:
            res.an.append(
                vlsir.spice.AnalysisResult(**{a.vlsir_type.value: a.to_proto()})
            )
        return res

    def __getitem__(self, key: int) -> AnalysisResult:
        return self.an[key]
