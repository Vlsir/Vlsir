""" 
# Spice-Class Simulator Interface 
"""

# Std-Lib Imports
import asyncio, os, subprocess
from typing import Union, Optional, Sequence, Awaitable, TypeVar
from enum import Enum
from textwrap import dedent
from dataclasses import dataclass, field

# Local/ Project Dependencies
import vlsir.spice_pb2 as vsp
from vlsir.spice_pb2 import *  # Not used here intentionally, but "re-exported"
from . import sim_data as sd


class ResultFormat(Enum):
    """Enumerated Result Formats"""

    SIM_DATA = "sim_data"  # Types defined in the `sim_data` module
    VLSIR_PROTO = "vlsir_proto"  # `vsp.SimResults` and related protobuf-defined types


# Union of the two result-types, returned by many simulation methods
SimResultUnion = Union[vsp.SimResult, sd.SimResult]


class SupportedSimulators(Enum):
    """Enumerated, Internally-Defined Spice-Class Simulators"""

    SPECTRE = "spectre"
    XYCE = "xyce"
    NGSPICE = "ngspice"


def default() -> Optional[SupportedSimulators]:
    """Get the default simulator, for this Python-process and its environment.
    This largely consists of a priority-ordered walk through `SupportedSimulators`,
    returning the first whose `available()` method indicates its availability.
    Returns `None` if no such simulator appears available."""

    from .spectre import available as spectre_available
    from .xyce import available as xyce_available
    from .ngspice import available as ngspice_available

    if spectre_available():
        return SupportedSimulators.SPECTRE
    if xyce_available():
        return SupportedSimulators.XYCE
    if ngspice_available():
        return SupportedSimulators.NGSPICE
    return None  # Nothing found


@dataclass
class SimOptions:
    """Options to `vsp.Sim` which are *not* passed along to the simulator.
    I.e. options which effect the Python-process invoking simulation,
    but not the internals of the simulation itself."""

    # Simulator. FIXME: debatable whether to include this.
    simulator: SupportedSimulators = field(default_factory=default)

    # In-memory results format
    fmt: ResultFormat = ResultFormat.VLSIR_PROTO

    # Simulation run-directory. Uses a `tempdir` if unspecified.
    rundir: Optional[os.PathLike] = None


# Shorthand type alias for "an element or list thereof", used by all the call signatures below
T = TypeVar("T")
OneOrMore = Union[T, Sequence[T]]


def sim(
    inp: OneOrMore[vsp.SimInput], opts: Optional[SimOptions] = None
) -> OneOrMore[SimResultUnion]:
    """
    Execute one or more `vlir.spice.Sim`.
    Dispatches across `SupportedSimulators` specified in `SimOptions` `opts`.
    Uses the default `Simulator` as detected by the `default` method if no `simulator` is specified.
    """
    return asyncio.run(sim_async(inp, opts))


async def sim_async(
    inp: OneOrMore[vsp.SimInput], opts: Optional[SimOptions] = None
) -> Awaitable[OneOrMore[SimResultUnion]]:
    """
    Asynchronously execute one or more `vlir.spice.Sim`.
    Dispatches across `SupportedSimulators` specified in `SimOptions` `opts`.
    Uses the default `Simulator` as detected by the `default` method if no `simulator` is specified.
    """
    from .xyce import XyceSim
    from .spectre import SpectreSim
    from .ngspice import NGSpiceSim

    # Sort out the difference between "One" "OrMore" cases of input
    # For a single `SimInput`, create a list, but note we only want to return a single `SimResult`
    inp_is_a_single_sim = False
    if not isinstance(inp, Sequence):
        inp = [inp]
        inp_is_a_single_sim = True
    for x in inp:
        if not isinstance(x, vsp.SimInput):
            raise TypeError(f"Expected `vsp.SimInput`, got {x}")

    if opts is None:  # Create the default `SimOptions`
        opts = SimOptions()

    if opts.simulator is None:  # If we didn't specify or find a simulator, fail.
        msg = f"vlsirtools.spice: No Supported Simulators available for call to `sim()`"
        raise RuntimeError(msg)

    # Get the per-simulator callable
    if opts.simulator == SupportedSimulators.XYCE:
        cls = XyceSim
    elif opts.simulator == SupportedSimulators.SPECTRE:
        cls = SpectreSim
    elif opts.simulator == SupportedSimulators.NGSPICE:
        cls = NGSpiceSim
    else:
        raise ValueError(f"Unsupported simulator: {opts.simulator}")

    if len(inp) > 1 and opts.rundir is not None:
        # FIXME: how to ultimately handle this "multi-inputs plus specified directory" case
        raise RuntimeError("Cannot specify a run-directory for multiple simulations")

    # And do the real work, invoking the target simulator
    futures = [cls.sim(i, opts) for i in inp]
    results = await asyncio.gather(*futures)

    # For the sequence of inputs case, return the sequence of results that came back
    if not inp_is_a_single_sim:
        return results

    # Unpack the single-input case
    if len(results) != 1:
        raise RuntimeError("Expected a single result")
    return results[0]


class SimError(Exception):
    """Exception raised when a simulation fails."""

    def __init__(self, sim: "Sim", stdout: bytes, stderr: bytes) -> None:
        s = dedent(
            f"""
            rundir: {str(sim.rundir)}
            stdout: {str(stdout)}
            stderr: {str(stderr)}
        """
        )
        super().__init__(s)
        self.rundir = sim.rundir
        self.stdout = stdout
        self.stderr = stderr


class SimProcessError(SimError):
    """Exception raised when an external simulator process fails."""

    def __init__(self, sim: "Sim", e: subprocess.CalledProcessError) -> None:
        super().__init__(sim=sim, stdout=e.stdout, stderr=e.stderr)
