# Std-Lib Imports
from glob import glob
from dataclasses import dataclass
from pathlib import Path
from typing import List

# VLSIR-Land Imports
import vlsirtools

# Local Imports
from .testcase import TestCase
from .pdk_sim_combo import PdkSimCombo


@dataclass
class MeasComparison:
    """Comparison of a Measurement in one of our Tests.

    Serves as the row-type for the comparison table.
    Yes, these field-names are non-Pythonic,
    but they are designed to be nice header-fields in a table."""

    Test: str  # Test/ Test-Bench
    Dut: str  # Device Under Test
    Corner: str  # PVT Corner
    Temper: int  # Temperature
    Measurement: str  # Measurement Name

    Xyce: float  # Xyce Result
    Spectre: float  # Spectre Result
    Diff: float  # Difference (divided by average)


def compare_case(
    testcase: TestCase,
    xyce_combo: PdkSimCombo,
    spectre_combo: PdkSimCombo,
    rundirs: Path,
) -> List[MeasComparison]:
    """Compare each measurement in test-case `testcase`,
    creating and returning a list of `MeasComparison`s."""

    # Collect up the measurement-data
    simdir = rundirs / xyce_combo.name / testcase.dirname
    xyce_glob = glob(str(simdir / "*.m*0"))
    if not len(xyce_glob):
        raise RuntimeError(
            f"No Xyce measurement-files for TestCase {testcase} in {simdir}"
        )
    if len(xyce_glob) > 1:
        msg = f"Multiple potential measurement-files: {xyce_glob} for TestCase {testcase} in {simdir}"
        raise RuntimeError(msg)
    xyce_results = vlsirtools.xyce.parse_meas(open(xyce_glob[0], "r"))
    xyce_results = {k.lower(): v for k, v in xyce_results.items()}
    xyce_results = testcase.meas_func(xyce_results)

    spectre_glob = glob(str(rundirs / spectre_combo.name / testcase.dirname / "*.m*0"))
    if not len(spectre_glob):
        raise RuntimeError(f"No Spectre measurement-files for TestCase {testcase.name}")
    if len(spectre_glob) > 1:
        msg = f"Multiple potential measurement-files: {spectre_glob} for TestCase {testcase.name}"
        raise RuntimeError(msg)
    spectre_results = vlsirtools.spectre.parse_mt0(open(spectre_glob[0], "r"))
    spectre_results = {k.lower(): v for k, v in spectre_results.items()}
    spectre_results = testcase.meas_func(spectre_results)

    def comp(measname: str, xyce: float, spectre: float) -> MeasComparison:
        """Closure for creating a `MeasComparison`,
        with all the data shared by each measurement in this test."""

        # Take the normalized difference, divided by the average
        diff = (xyce - spectre) * 2 / (xyce + spectre)

        return MeasComparison(
            Test=testcase.name,
            Dut=testcase.dut.name,
            Corner=testcase.corner.value,
            Temper=testcase.temper,
            Measurement=measname,
            Xyce=xyce,
            Spectre=spectre,
            Diff=diff,
        )

    # Create such a comparison for each measured value
    comparisons = []
    for name, xyce_val in xyce_results.items():
        if name not in spectre_results.keys():
            msg = f"Measurement {name} in Xyce results not present in spectre results {spectre_results}"
            raise ValueError(msg)
        spectre_val = spectre_results[name]
        comparisons.append(comp(name, xyce_val, spectre_val))
    return comparisons
