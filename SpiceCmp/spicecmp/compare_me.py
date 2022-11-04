""" 
# The Stuff Ultimately Being *Compared* in `spicecmp`

Pairs of Pdk + Simulator Combos, and associated functions to run 
their test-cases and collect resultant measurement results. 

"""

# Std-Lib Imports
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Callable

# PyPi Imports
import pandas as pd

# Local Imports
from .corner import Corner
from .pdk import MosModel
from .simulator import Simulators
from .pdk_sim_combo import PdkSimCombo
from .testcase import TestCase, TestCaseRun
from .compare_meas import compare_case
from .errormode import ErrorMode


@dataclass
class CompareMe:
    """Pair of Pdk-Simulator Combos to be Compared.
    One always uses spectre, and the other always uses xyce.

    Exposes two primary methods, both of which operate over a list of `TestCase`s:

    * `run` netlists and runs the test-case simulations, as well as it can.
        * To date `SpiceCmp` is yet to meet a single computer which can run all its target simulators,
          and so in many cases reverts to just netlisting their input for offline execution.
    * `compare` gathers the results of each `TestCase`, compares them measurement-by-measurement, creates and saves a summary table.
    """

    # The PDK-simulator combinations under comparison
    spectre: PdkSimCombo
    xyce: PdkSimCombo

    # Comparison name, for labeling and run-directory naming
    name: str

    # DUTs Under Comparison
    xtors: List[MosModel]
    ro_cells: List[Callable]

    # Comparison Conditions
    tempers: List[int]
    corners: List[Corner]

    # Options
    errormode: ErrorMode = ErrorMode.WARN

    def __post_init__(self):
        if self.spectre.sim.enum != Simulators.SPECTRE:
            raise RuntimeError(f"Unsupported sim-pdk combination {self.spectre}")
        if self.xyce.sim.enum != Simulators.XYCE:
            raise RuntimeError(f"Unsupported sim-pdk combination {self.xyce}")

    def run_test_case(self, testcase: TestCase, ps: PdkSimCombo) -> None:
        """Run a single test-case, with a single `PdkSimCombo`."""
        run = TestCaseRun(
            testcase=testcase,
            pdk=ps.pdk,
            simulator=ps.sim,
            parentdir=Path("./rundirs") / ps.name,
            errormode=self.errormode,
        )
        testcase.run_func(run)

    def run(self, testcases: List[TestCase]) -> None:
        """Run all test cases (or at least "run" as much as we can)."""
        for ps in (self.xyce, self.spectre):
            for testcase in testcases:
                self.run_test_case(testcase, ps)

    def run_one_combo(self, testcases: List[TestCase], which: Simulators) -> None:
        """Run all the test-cases for one `PdkSimCombo`, denoted by an enumerated `Simulator`."""
        if which == Simulators.XYCE:
            ps = self.xyce
        elif which == Simulators.SPECTRE:
            ps = self.spectre
        else:
            raise ValueError

        for testcase in testcases:
            self.run_test_case(testcase, ps)

    def compare(self, testcases: List[TestCase]) -> pd.DataFrame:
        """Perform comparisons between results, and save to a data-table."""

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
