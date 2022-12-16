"""
# Sim Data 

A mirror of Spice Proto's Analysis Result objects for in-Python usage, 
using python data classes and numpy arrays.

Also provides round-tripping utilities between the two.
TODO: Go from proto -> sim_result
"""


from enum import Enum
from dataclasses import dataclass, field
from typing import List, Mapping, Union, ClassVar, Dict, Optional

import numpy as np

import vlsir.spice_pb2 as vsp


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

    def to_proto(self) -> vsp.OpResult:
        res = vsp.OpResult(analysis_name=self.analysis_name)
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

    def to_proto(self) -> vsp.DcResult:
        res = vsp.DcResult(analysis_name=self.analysis_name, indep_name=self.indep_name)
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

    def to_proto(self) -> vsp.TranResult:
        res = vsp.TranResult(analysis_name=self.analysis_name)
        for k, v in self.data.items():
            res.signals.append(k)
            for d in v:
                res.data.append(d)
        # TODO Add support for measurements
        return res


@dataclass
class AcResult:
    analysis_name: str  # Analysis name
    freq: np.ndarray  # Real/ float-valued frequency data
    data: Mapping[str, np.ndarray]  # Complex-valued signal data
    measurements: Mapping[str, float]  # Measurement data
    vlsir_type: ClassVar[AnalysisType] = AnalysisType.AC

    def to_proto(self) -> vsp.AcResult:
        """Convert to a VLSIR `AcResult` proto object
        Primarily "flattens" the complex-valued data into a single list."""

        data: List[vsp.ComplexNum] = []
        for v in self.data.values():
            data.extend([vsp.ComplexNum(re=c.real, im=c.imag) for c in v])

        return vsp.AcResult(
            analysis_name=self.analysis_name,
            freq=self.freq,
            signals=list(self.data.keys()),
            data=data,
            measurements=self.measurements,
        )


@dataclass
class NoiseResult:
    analysis_name: str
    data: Mapping[str, np.ndarray]
    integrated_noise: Mapping[str, float]
    measurements: Mapping[str, float]
    vlsir_type: ClassVar[AnalysisType] = AnalysisType.NOISE

    def to_proto(self) -> vsp.AcResult:
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


# Type union for indexing into AnalysisResults
AnalysisIndex = Union[int, str, AnalysisType, vsp.Analysis]


@dataclass
class AnalysisResultsTable:
    """# Multi-Indexed Table of Analysis Results
    Accessible by analysis-type, index, and name."""

    order: List[AnalysisResult]
    # In-order list of results, as ordered in `SimInput`.
    names: Dict[str, AnalysisResult]
    # Mapping by analysis-name
    types: Dict[AnalysisType, List[AnalysisResult]]
    # Mapping by analysis-type. Note there can be more than one of each type.

    @classmethod
    def create(cls, results: "SimResult") -> "AnalysisResultsTable":
        """Create an index from a `SimResult` object."""
        order = results.an
        names = {r.analysis_name: r for r in order}
        # "By type" is different, since there can be several of each type.
        types = {}
        for r in order:
            if r.vlsir_type in types:
                types[r.vlsir_type].append(r)
            else:
                types[r.vlsir_type] = [r]
        return cls(order, names, types)

    def get(self, key: AnalysisIndex) -> AnalysisResult:
        """Index into our results by type, index, or name."""

        if isinstance(key, int):
            return self.order[key]
        if isinstance(key, str):
            return self.names[key]
        if isinstance(key, AnalysisType):
            if key not in self.types:
                raise ValueError(f"No results for AnalysisType {key}")
            if len(self.types[key]) != 1:
                raise RuntimeError(f"Multiple results of type {key}")
            return self.types[key][0]
        raise TypeError(f"Invalid index into SimResults: {key} ({type(key)})")


@dataclass
class SimResult:
    """Results from a Mult-Analysis `Sim`"""

    an: List[AnalysisResult] = field(default_factory=list)
    # List of per-analysis results, in the same order specified in `SimInput.an`.

    def __post_init__(self):
        # Our multi-indexed table of results.
        # Unset until accessed with `get or __getitem__`
        self._table: Optional[AnalysisResultsTable] = None

    def index(self):
        """Recreate our multi-index table. Generally required on changes to primary list `an`."""
        self._table = AnalysisResultsTable.create(self)

    def __getitem__(self, key: AnalysisIndex) -> AnalysisResult:
        """Index into our results by type, index, or name."""
        return self.get(key)

    def get(self, key: AnalysisIndex) -> AnalysisResult:
        """Get one of our analysis-results by type, index, or name."""
        if self._table is None:
            self.index()
        return self._table.get(key)

    def to_proto(self) -> vsp.SimResult:
        """Convert to a VLSIR `SimResult` proto object."""
        res = vsp.SimResult()
        for an in self.an:
            ar = vsp.AnalysisResult(**{an.vlsir_type.value: an.to_proto()})
            res.an.append(ar)
        return res
