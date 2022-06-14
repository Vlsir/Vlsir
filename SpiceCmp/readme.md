
# SpiceCmp 

A Python library for making comparisons between Spice-class simulators.


## Running

`SpiceCmp`'s primary object of comparison is the `CompareMe` (names, we know), which includes two 
"PDK plus simulator combinations" (`PdkSimCombo`s), DUTs for comparison, and comparison conditions: 

```python
@dataclass
class CompareMe:
    """ Pair of Pdk-Simulator Combos to be Compared. 
    One always uses spectre, and the other always uses xyce. 
    
    Exposes two primary methods, both of which operate over a list of `TestCase`s: 

    * `run` netlists and runs the test-case simulations, as well as it can. 
    * `compare` gathers the results of each `TestCase`, compares them measurement-by-measurement, creates and saves a summary table. 
    """

    # The PDK + Simulator combinations
    spectre: PdkSimCombo
    xyce: PdkSimCombo

    # Comparison name, for labeling and run-directory naming
    name: str

    # DUTs for comparison
    xtors: List[MosModel]
    ro_cells: List[Callable]

    # Other shared data for comparison
    tempers: List[int]
    corners: List[Corner]
```

Each `CompareMe` has two primary API methods: 

* `run` generates netlists and invokes simulation 
* `compare` collects simulation results, runs post-processesing, and collates results into a summary table

Both take as their sole argument a list of `TestCase`s. 
Each test-case includes the test conditions (e.g. temperature, process corner) 
and a shared `Test` object: 

```python 
@dataclass
class TestCase:
    """ # Test Case 
    Combination of a `Test`, and the conditions under which it is run. """

    test: Test  # Reference to the parent `Test`
    dut: Any  # Device under test, or generator thereof
    corner: Corner  # PVT Corner
    temper: int  # Temperature

@dataclass
class Test:
    """ # Simulation Comparison Test """

    name: str  # Test Name
    run_func: Callable  # Run-Function
    meas_func: Callable  # Measurement-Manipulation Function
```

Each `Test`, in turn, is principally comprised of two functions: 

* A `run_func` which produces a simulatable DUT and invokes simulation, and 
* A `meas_func` which post-processes results which come back from said simulation 

The post-processing measurement functions (`meas_func`s) operate on solely on Spice *measurement* data. 
Measurements are typically mappings from string measurement-names to scalar, numeric result values. 
The required signature for each `meas_func` is therefore: 

```python
def meas_func(inp: Dict[str, float]) -> Dict[str, float]:
    """ Convert a "raw" input measurement-dictionary to post-processed form. """
```

In Python `typing` notation, the type of each `meas_func` is therefore:

```python
meas_func: Callable[[Dict[str, float]], Dict[str, float]]
```

Run-functions take as their sole argument a `TestCaseRun`, the combination of a `TestCase`, 
PDK, and simulator to run it against, along with other metadata. 

```python 
@dataclass
class TestCaseRun:
    """ # Test Case Run
    Execution of a `TestCase` with a particular PDK & simulator. """

    testcase: TestCase
    pdk: Pdk
    simulator: Simulator
    parentdir: Path
    errormode: ErrorMode
```

Their signature takes a `TestCaseRun` as input and returns nothing: 

```python
def run_func(run: TestCaseRun) -> None:
    """ Execute the `TestCaseRun` """
```

And again in `typing` module terms, run-functions are of type: 

```python
run_func: Callable[["TestCaseRun"], None]
```

### Comparison Results 

Results for each `TestCase`-measurement combination are collated into a `MeasComparison` 
including summary information about the test, conditions, and DUT. 

```python
@dataclass
class MeasComparison:
    """ Comparison of a Measurement in one of our Tests. 

    Serves as the row-type for the comparison table. 
    Yes, these field-names are non-Pythonic, 
    but they are designed to be nice header-fields in a table. """

    Test: str  # Test/ Test-Bench
    Dut: str  # Device Under Test
    Corner: str  # PVT Corner
    Temper: int  # Temperature
    Measurement: str  # Measurement Name

    Xyce: float  # Xyce Result
    Spectre: float  # Spectre Result
    Diff: float  # Difference (divided by average)
```

`CompareMe.compare` also generally saves the combined set of these `MeasComparison`s to a tabular CSV-format file, 
with column-names equal to the field-names of `MeasComparison`. An example such result: 

```
Test,   Dut,        Corner, Temper, Measurement,    Xyce,           Spectre,        Diff
MosIv,  NMOS_STD,   TT,     -25,    idsat,          0.0005419505,   0.000541951,    -9.225930586166412e-07
MosIv,  NMOS_STD,   FF,     -25,    idsat,          0.0006205647,   0.000620565,    -4.834305391191293e-07
# ...
```

Note the `Diff` field of each comparison is relative: it reports the difference between the two simulator results, divided by their average value. 


## Development

To set up a dev install: 
```
pip install -e ".[dev]"
```

