"""
A mirror of Spice Proto's Analysis Result objects,
but using python data classes and numpy arrays.

Also provides round-tripping utilities between the two
TODO: Go from proto -> sim_result
"""


from dataclasses import dataclass
import numpy as np
from typing import List, Mapping, Union


import vlsir


@dataclass
class OpResult:
    analysis_name: str
    data: Mapping[str, float]
    vlsir_type: str = "op"

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
    vlsir_type: str = "dc"

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
    vlsir_type: str = "tran"

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
    vlsir_type: str = "ac"

    def to_proto(self) -> vlsir.spice.AcResult:
        raise NotImplementedError


# Type alias for the union of each result-type
AnalysisResult = Union[AcResult, DcResult, TranResult, OpResult]


@dataclass
class SimResult:
    """ Results from a Mult-Analysis `Sim` """

    an: List[AnalysisResult]

    def to_proto(self) -> vlsir.spice.SimResult:
        res = vlsir.spice.SimResult()
        for a in self.an:
            res.an.append(vlsir.spice.AnalysisResult(**{a.vlsir_type: a.to_proto()}))
        return res

    def __getitem__(self, key: int) -> AnalysisResult:
        return self.an[key]

