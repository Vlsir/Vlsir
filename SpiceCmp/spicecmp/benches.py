# Std-Lib Imports
from textwrap import dedent
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
from warnings import warn

# Some "Friendly" Imports
import hdl21 as h
import vlsirtools.spice as vsp

# Local Imports
from .testcase import Test, TestCase, TestCaseRun
from .pdk import Pdk, MosModel
from .simulator import Simulator
from .errormode import ErrorMode


@h.paramclass
class DcIvParams:
    dut = h.Param(dtype=h.Instantiable, desc="The transistor DUT")
    mos_type = h.Param(dtype=h.MosType, desc="Mos Type (NMOS/ PMOS)")
    mos_vth = h.Param(dtype=h.MosVth, desc="Mos Vth (enumerated)")
    ctrls = h.Param(dtype=List[vsp.Control], desc="Simulator control cards")
    rundir = h.Param(dtype=Path, desc="Run directory")
    vlsirtools_simulator = h.Param(
        dtype=vsp.SupportedSimulators, desc="VlsirTools Simulator Tag"
    )
    vdd = h.Param(dtype=str, desc="Supply Voltage (V), in string form")
    temper = h.Param(dtype=int, desc="Simulation Temperature")
    errormode = h.Param(
        dtype=ErrorMode, default=ErrorMode.WARN, desc="Error handling strategy"
    )


def dc_iv(params: DcIvParams) -> None:
    """Transistor I-V Curve Test"""

    @h.module
    class DcIvTestbench:
        """Transistor I-V Testbench"""

        vss = h.Port()  # The VLSIR "testbench interface", a sole port: VSS
        d, g = h.Signals(2)  # Drain and Gate Signals

        dut = params.dut(d=d, g=g, s=vss, b=vss)
        vg = h.V(h.V.Params(dc="polarity*vgs"))(p=g, n=vss)
        vd = h.V(h.V.Params(dc="polarity*vds"))(p=d, n=vss)

    polarity = -1 if params.mos_type == h.MosType.PMOS else 1

    from hdl21.sim import Sim

    # Create some simulation input
    sim = Sim(tb=DcIvTestbench)
    sim.param("polarity", polarity)
    sim.param("vds", params.vdd)
    sim.param("vgs", params.vdd)
    # sim.options(temper=params.temper) # FIXME!

    sim.dc(
        var="vgs", sweep=h.sim.LinearSweep(start=0.0, stop=float(params.vdd), step=0.01)
    )

    # Add the measurement, which requires a hierarchical path we sadly cannot yet distinguish per simulator.
    # And the temperature option, sadly.
    if params.vlsirtools_simulator == vsp.SupportedSimulators.XYCE:
        sim.literal(f".options device temp={params.temper}")
        sim.meas(name="idsat", expr=f"find i(xtop:vvd) at={params.vdd}", analysis="dc")
    else:
        sim.literal(f"options options temp={params.temper}")
        sim.meas(name="idsat", expr=f"find i(xtop.vd) at='{params.vdd}'", analysis="dc")

    # Convert to VLSIR ProtoBufs
    sim_input = h.sim.to_proto(sim)
    sim_input.ctrls.extend(params.ctrls)

    try:
        results = vsp.sim(
            sim_input,
            vsp.SimOptions(simulator=params.vlsirtools_simulator, rundir=params.rundir),
        )
    except Exception as e:
        if params.errormode == ErrorMode.WARN:
            warn(str(e))
        else:
            raise e


@dataclass
class MosDut:
    model: MosModel
    instantiable: h.Instantiable

    @property
    def name(self):
        return self.model.name


def mosiv_test(run: TestCaseRun) -> None:
    """MOS DC I-V Test Case"""
    testcase = run.testcase
    pdk = run.pdk
    simulator = run.simulator
    parentdir = run.parentdir

    mos_dut: MosDut = testcase.dut(pdk)
    params = DcIvParams(
        dut=mos_dut.instantiable,
        mos_type=mos_dut.model.mos_type,
        mos_vth=mos_dut.model.mos_vth,
        ctrls=[pdk.include(simulator.enum, testcase.corner)],
        rundir=parentdir / testcase.dirname,
        vlsirtools_simulator=simulator.vlsirtools,
        vdd=pdk.vdd,
        temper=testcase.temper,
        errormode=run.errormode,
    )
    results = dc_iv(params)
    return results


def mosiv_meas(inp: Dict[str, float]) -> Dict[str, float]:
    """MOS DC I-V Measurement Manipulations"""
    # Primarily sets everything positive,
    # as some measured parameters tend to vary in polarity for PMOS vs NMOS.
    # This could more intelligently edit values, if offered some more info.
    return {k: abs(v) for k, v in inp.items()}


mosiv_test = Test(name="MosIv", run_func=mosiv_test, meas_func=mosiv_meas)


@h.paramclass
class InvParams:
    """Inverter Generation Parameters
    Note both transistors are `h.Instantiable`, which means that any parameterization
    has been applied before being passed into this class."""

    pmos = h.Param(dtype=h.Instantiable, desc="PMOS to be instantiated")
    nmos = h.Param(dtype=h.Instantiable, desc="NMOS to be instantiated")


@h.generator
def Inv(params: InvParams) -> h.Module:
    @h.module
    class Inv:
        i = h.Input()
        o = h.Output()
        vdd, vss = h.Ports(2)

        p = params.pmos(d=o, g=i, s=vdd, b=vdd)
        n = params.nmos(d=o, g=i, s=vss, b=vss)

    return Inv


@h.generator
def Nor2Stg(params: InvParams) -> h.Module:
    """NOR2, arranged to be an RO Stage, with one input tied low.
    Tests the "slow input", i.e. the one furthest from the output."""

    @h.module
    class Nor2Stg:
        i = h.Input()
        o = h.Output()
        vdd, vss = h.Ports(2)
        mid = h.Signal()

        pdut = params.pmos(d=mid, g=i, s=vdd, b=vdd)
        poff = params.pmos(d=o, g=vss, s=vdd, b=vdd)
        noff = params.nmos(d=o, g=vss, s=vss, b=vss)
        ndut = params.nmos(d=o, g=i, s=vss, b=vss)

    return Nor2Stg


@h.generator
def Nand2Stg(params: InvParams) -> h.Module:
    """Nand2, arranged to be an RO Stage, with one input tied high.
    Tests the "slow input", i.e. the one furthest from the output."""

    @h.module
    class Nand2Stg:
        i = h.Input()
        o = h.Output()
        vdd, vss = h.Ports(2)
        mid = h.Signal()

        pdut = params.pmos(d=o, g=i, s=vdd, b=vdd)
        poff = params.pmos(d=o, g=vdd, s=vdd, b=vdd)
        non = params.nmos(d=o, g=vdd, s=mid, b=vss)
        ndut = params.nmos(d=mid, g=i, s=vss, b=vss)

    return Nand2Stg


@h.paramclass
class StdCellRoParams:
    dut = h.Param(dtype=h.Instantiable, desc="Single DUT Stage")
    nstg = h.Param(dtype=int, desc="Number of stages")
    ctrls = h.Param(dtype=List[vsp.Control], desc="Simualtor control cards")
    rundir = h.Param(dtype=Path, desc="Run directory")
    vlsirtools_simulator = h.Param(
        dtype=vsp.SupportedSimulators, desc="VlsirTools Simulator Tag"
    )
    vdd = h.Param(dtype=str, desc="Supply Voltage (V), in string form")
    temper = h.Param(dtype=int, desc="Simulation Temperature")
    errormode = h.Param(
        dtype=ErrorMode, default=ErrorMode.RAISE, desc="Error handling strategy"
    )


def std_cell_ro(params: StdCellRoParams) -> None:
    """Standard-Cell Ring Oscillator Test"""

    if params.nstg % 2 != 1:
        raise RuntimeError("Need an odd number of stages")

    @h.module
    class RoTb:
        """RO Testbench"""

        vss = h.Port()  # The VLSIR "testbench interface", a sole port: VSS

        # Supply Signal and its generating Source
        vdd = h.Signal()
        vvdd = h.V(h.V.Params(dc="vdd"))(p=vdd, n=vss)

        # Oscillator State Nodes
        osc = h.Signal(width=params.nstg)

    # Create an instance of `DUT` per stage
    for stgnum in range(params.nstg):
        inst = params.dut(
            vss=RoTb.vss,
            vdd=RoTb.vdd,
            i=RoTb.osc[stgnum],
            o=RoTb.osc[(stgnum + 1) % params.nstg],
        )
        RoTb.add(name=f"stg{stgnum}", val=inst)

    from hdl21.sim import Sim

    # Create some simulation input
    sim = Sim(tb=RoTb)
    sim.param(name="vdd", val=params.vdd)
    sim.tran(tstop=50e-9, tstep=1e-12)
    # sim.options(temper=params.temper) # FIXME!

    # An ugly part: the not-totally-supported input-differences, including
    # * (a) initial conditions,
    # * (b) hierarchical paths,
    # * (c) non-first-class spice-format `options`, e.g. `autostop`
    # # (d) options, particular the categorized xyce variety

    if params.vlsirtools_simulator == vsp.SupportedSimulators.XYCE:
        sim.literal(
            dedent(
                f"""
            .options device temp={params.temper}
            .ic xtop:osc_0 0 
            .measure tran trise5  when V(xtop:osc_0)={{vdd/2}} rise=5
            .measure tran trise15 when V(xtop:osc_0)={{vdd/2}} rise=15
        """
            )
        )
    else:
        sim.literal(
            dedent(
                f"""
            options options temp={params.temper}

            simulator lang=spice
            .ic xtop.osc_0 0 
            .measure tran trise5  when V(xtop:osc_0)='vdd/2' rise=5
            .measure tran trise15 when V(xtop:osc_0)='vdd/2' rise=15
            .option autostop
            simulator lang=spectre
        """
            )
        )

    # Convert all that to VLSIR protobuf
    sim_input = h.sim.to_proto(sim)

    # Add any control-cards from `params`
    sim_input.ctrls.extend(params.ctrls)

    try:
        results = vsp.sim(
            sim_input,
            vsp.SimOptions(simulator=params.vlsirtools_simulator, rundir=params.rundir),
        )
    except Exception as e:
        if params.errormode == ErrorMode.WARN:
            warn(str(e))
        else:
            raise e


def ro_test(run: TestCaseRun) -> None:
    """ "TestCase Interface" for the RO Tests
    Largely a thin wrapper around `std_cell_ro`."""
    testcase = run.testcase
    pdk = run.pdk
    simulator = run.simulator
    parentdir = run.parentdir

    params = StdCellRoParams(
        dut=testcase.dut(pdk),
        nstg=15,
        ctrls=[pdk.include(simulator.enum, testcase.corner)],
        rundir=parentdir / testcase.dirname,
        vlsirtools_simulator=simulator.vlsirtools,
        vdd=pdk.vdd,
        temper=testcase.temper,
        errormode=run.errormode,
    )
    results = std_cell_ro(params)
    return results


def ro_meas(inp: Dict[str, float]) -> Dict[str, float]:
    """Convert the measurements made directly by SPICE into others that we actually care about."""

    # Get the two relevant values
    trise15 = inp["trise15"]
    trise5 = inp["trise5"]
    # The raw measurements are of ten periods of a 15-stage oscillator.
    # So divided down to one period (by 10),
    # and then by the number of stage-delays (2 * nstg).
    # This will of course need some more parameterization for any-other-size ring.
    return dict(tdelay=(trise15 - trise5) / 10 / 30)


ro_test = Test(name="Ro", run_func=ro_test, meas_func=ro_meas)
