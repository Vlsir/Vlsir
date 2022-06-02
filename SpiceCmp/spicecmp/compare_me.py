""" 
# The Stuff Ultimately Being *Compared* in `spicecmp`

Pairs of Pdk + Simulator Combos, and associated functions to run 
their test-cases and collect resultant measurement results. 

"""

# Std-Lib Imports
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import List, Dict, Callable

# PyPi Imports
import pandas as pd

# "Friend" VLSIR-World Imports
from vlsir.spice_pb2 import Control, LibInclude
from vlsirtools.spice import SupportedSimulators
import hdl21 as h
from hdl21.primitives import MosType, MosVth

# Local Imports
from .corner import Corner
from .pdk import Pdk, MosModel
from .simulator import Simulator, Simulators
from .pdk_sim_combo import PdkSimCombo
from .testcase import TestCase
from .compare_meas import compare_case


@dataclass
class CompareMe:
    """ Pair of Pdk-Simulator Combos to be Compared. 
    One always uses spectre, and the other always uses xyce. 
    
    Exposes two primary methods, both of which operate over a list of `TestCase`s: 

    * `run` netlists and runs the test-case simulations, as well as it can. 
        * To date `SpiceCmp` is yet to meet a single computer which can run all its target simulators, 
          and so in many cases reverts to just netlisting their input for offline execution. 
    * `compare` gathers the results of each `TestCase`, compares them measurement-by-measurement, creates and saves a summary table. 
    """

    spectre: PdkSimCombo
    xyce: PdkSimCombo

    # Comparison name, for labeling and run-directory naming
    name: str

    # Other shared data for comparison
    xtors: List[MosModel]
    tempers: List[int]
    corners: List[Corner]
    ro_cells: List[Callable]

    def __post_init__(self):
        if self.spectre.sim.enum != Simulators.SPECTRE:
            raise RuntimeError(f"Unsupported sim-pdk combination {self.spectre}")
        if self.xyce.sim.enum != Simulators.XYCE:
            raise RuntimeError(f"Unsupported sim-pdk combination {self.xyce}")

    def run_test_case(self, testcase: TestCase, ps: PdkSimCombo):
        """ Run a single test-case, with a single `PdkSimCombo`. """
        pdk, simulator = ps.pdk, ps.sim
        testcase.run_func(
            testcase=testcase,
            pdk=pdk,
            simulator=simulator,
            parentdir=Path("./rundirs") / ps.name,
        )
    
    def run(self, testcases: List[TestCase]) -> None:
        """ Run all test cases (or at least "run" as much as we can). """
        for ps in (self.xyce, self.spectre):
            for testcase in testcases:
                self.run_test_case(testcase, ps)

    def run_one_combo(self, testcases: List[TestCase], which: Simulators):
        """ Run all the test-cases for one `PdkSimCombo`, denoted by an enumerated `Simulator`. """
        if which == Simulators.XYCE:
            ps = self.xyce 
        elif which == Simulators.SPECTRE:
            ps = self.spectre 
        else:
            raise ValueError
        
        for testcase in testcases:
                self.run_test_case(testcase, ps)

    def compare(self, testcases: List[TestCase]) -> pd.DataFrame:
        """ Perform comparisons between results, and save to a data-table. """

        comparisons = []
        for testcase in testcases:
            meas = compare_case(
                testcase,
                xyce_combo=self.xyce,
                spectre_combo=self.spectre,
                rundirs=Path("./rundirs"),
            )
            comparisons.extend(meas)

        # Convert these comparisons to a table, and save it to disk
        df = pd.DataFrame.from_records([asdict(comp) for comp in comparisons])
        df.to_csv(f"{self.name}.csv", index=False)
        print("Comparison Results Being Saved to `comparisons.csv`:")
        print(df)
        return df
