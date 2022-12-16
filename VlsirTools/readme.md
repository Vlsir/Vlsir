
# Vlsir Tools 

Python-based tools and utilites for working with the Vlsir IC design schema. 

## Netlisting 

FIXME! Details here. 

## Spice-Class Simulation 

VlsirTools includes drivers and result-parsers for popular spice-class simulation engines including: 

```python 
class SupportedSimulators(Enum):
    """Enumerated, Internally-Defined Spice-Class Simulators"""

    SPECTRE = "spectre"
    XYCE = "xyce"
    NGSPICE = "ngspice"
```

The primary entry-point for simulation is `vlsirtools.spice.sim`. 

```python
def sim(
    inp: OneOrMore[vsp.SimInput], opts: Optional[SimOptions] = None
) -> OneOrMore[SimResultUnion]:
```

The `sim` function takes as input one or more `vlsir.spice.SimInput`s and a set of simulation options (`vlsirtools.spice.SimOptions`), and returns one of two result-types depending on its input `options`.


```python
class ResultFormat(Enum):
    """Enumerated Result Formats"""

    SIM_DATA = "sim_data" 
    VLSIR_PROTO = "vlsir_proto" 
```

The `VLSIR_PROTO` result-format returns a `vlsir.spice.SimResult` object, which is a protobuf-encoded representation of the simulation results. The `SIM_DATA` format instead uses the types defined in `vlsirtools.spice.sim_data`, a python-native combination of dataclasses and numpy arrays. The former is generally more convenient for sharing with other programs, and the latter for further in-Python processing. 

Simulations can be invoked asynchronously by instead invoking `vlsirtools.spice.sim_async`. 
Its interface is identical to `vlsirtools.spice.sim`, but for returning an `Awaitable`. 

```python
async def sim_async(
    inp: OneOrMore[vsp.SimInput], opts: Optional[SimOptions] = None
) -> Awaitable[OneOrMore[SimResultUnion]]:
```

Asynchronously invoking simulation is particularly valuable for large batches of simulations, 
e.g. for "corner" or other parametric variations, as the simulator invocations can be run in parallel.

### Simulator and Analysis Support

Each spice-class simulator includes its own netlist syntax and opinions about the specification for analyses. 
The `vlsir.spice` schema  

| Analysis             | Spectre            | Xyce               | NgSpice     |
| -------------------- | ------------------ | ------------------ | ------------------ |
| Op                   | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Dc                   | :white_check_mark: | :white_check_mark: | |
| Tran                 | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Ac                   | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Noise                |                    |                    | :white_check_mark: |
| Sweep                |  |  |  |
| Monte Carlo          |  |  |  |
| Custom               |  |  |  |

