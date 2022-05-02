# Std-Lib Imports
from textwrap import dedent
from copy import deepcopy
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

import vlsirtools
from vlsir.spice_pb2 import (
    SimInput,
    Analysis,
    DcInput,
    DcResult,
    TranInput,
    TranResult,
    Sweep,
    LinearSweep,
    Control,
)
from vlsirtools.spice import SupportedSimulators
import hdl21 as h
from hdl21.primitives import MosType, MosVth

# Local Imports
from .testcase import Test, TestCase
from .pdk import Pdk, MosModel
from .simulator import Simulator, Simulators


@h.paramclass
class DcIvParams:
    dut = h.Param(dtype=h.Instantiable, desc="The transistor DUT")
    mos_type = h.Param(dtype=MosType, desc="Mos Type (NMOS/ PMOS)")
    mos_vth = h.Param(dtype=MosVth, desc="Mos Vth (enumerated)")
    ctrls = h.Param(dtype=List[Control], desc="Simulator control cards")
    rundir = h.Param(dtype=Path, desc="Run directory")
    vlsirtools_simulator = h.Param(
        dtype=SupportedSimulators, desc="VlsirTools Simulator Tag"
    )
    vdd = h.Param(dtype=str, desc="Supply Voltage (V), in string form")
    temper = h.Param(dtype=int, desc="Simulation Temperature")


def dc_iv(params: DcIvParams) -> DcResult:
    """ Transistor I-V Curve Test """

    @h.module
    class DcIvTestbench:
        """ Transistor I-V Testbench """

        vss = h.Port()  # The VLSIR "testbench interface", a sole port: VSS
        d, g = h.Signals(2)  # Drain and Gate Signals

        dut = params.dut(d=d, g=g, s=vss, b=vss)
        vg = h.V(h.V.Params(dc="polarity*vgs"))(p=g, n=vss)
        vd = h.V(h.V.Params(dc="polarity*vds"))(p=d, n=vss)

    # Convert to VLSIR protobuf schema
    tb_pkg = h.to_proto(DcIvTestbench)

    # FIXME: this generated-module-name-extraction should be a feature of the libraries, somehow
    top_name = tb_pkg.modules[0].name

    polarity = -1 if params.mos_type == MosType.PMOS else 1

    for_xyce = dedent(
        f"""
        .param polarity={polarity} vds={params.vdd} vgs={params.vdd}
        .measure dc idsat find i(xtop:vvd) at={params.vdd}
        .options device temp={params.temper} 
        """
    )
    for_spectre = dedent(
        f"""
        parameters polarity={polarity} vds={params.vdd} vgs={params.vdd}
        options options temp={params.temper}
        simulator lang=spice
        .measure dc idsat find i(xtop.vd) at='{params.vdd}'
        simulator lang=spectre
        """
    )
    literal = (
        for_xyce
        if params.vlsirtools_simulator == SupportedSimulators.XYCE
        else for_spectre
    )
    ctrls = params.ctrls + [Control(literal=literal)]

    sim_input = SimInput(
        top=top_name,
        pkg=tb_pkg,
        an=[
            Analysis(
                dc=DcInput(
                    # analysis_name="dc_iv",
                    indep_name="vgs",
                    sweep=Sweep(
                        linear=LinearSweep(start=0.0, stop=float(params.vdd), step=0.01)
                    ),
                ),
            ),
        ],
        ctrls=ctrls,
    )
    try:
        res = vlsirtools.spice.sim(params.vlsirtools_simulator)(
            sim_input, rundir=params.rundir
        )
    except Exception as e:
        print(e)
        return None
    print(f"ran {params}")
    return res.an[0].dc


@dataclass
class MosDut:
    model: MosModel
    instantiable: h.Instantiable

    @property
    def name(self):
        return self.model.name


def mosiv_test(
    testcase: TestCase, pdk: Pdk, simulator: Simulator, parentdir: Path
) -> TranResult:
    """ MOS DC I-V Test Case """
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
    )
    results = dc_iv(params)
    return results


def mosiv_meas(inp: Dict[str, float]) -> Dict[str, float]:
    """ MOS DC I-V Measurement Manipulations """
    # Primarily sets everything positive,
    # as some measured parameters tend to vary in polarity for PMOS vs NMOS.
    # This could more intelligently edit values, if offered some more info.
    return {k: abs(v) for k, v in inp.items()}


mosiv_test = Test(name="MosIv", run_func=mosiv_test, meas_func=mosiv_meas)


@h.paramclass
class InvParams:
    """ Inverter Generation Parameters 
    Note both transistors are `h.Instantiable`, which means that any parameterization 
    has been applied before being passed into this class. """

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
    """ NOR2, arranged to be an RO Stage, with one input tied low. 
    Tests the "slow input", i.e. the one furthest from the output. """

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
    """ Nand2, arranged to be an RO Stage, with one input tied high. 
    Tests the "slow input", i.e. the one furthest from the output. """

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
    ctrls = h.Param(dtype=List[Control], desc="Simualtor control cards")
    rundir = h.Param(dtype=Path, desc="Run directory")
    vlsirtools_simulator = h.Param(
        dtype=SupportedSimulators, desc="VlsirTools Simulator Tag"
    )
    vdd = h.Param(dtype=str, desc="Supply Voltage (V), in string form")
    temper = h.Param(dtype=int, desc="Simulation Temperature")


def std_cell_ro(params: StdCellRoParams) -> TranResult:
    """ Standard-Cell Ring Oscillator Test """

    if params.nstg % 2 != 1:
        raise RuntimeError("Need an odd number of stages")

    @h.module
    class RoTb:
        """ RO Testbench """

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

    # Convert to VLSIR protobuf schema
    tb_pkg = h.to_proto(RoTb)

    # FIXME: this generated-module-name-extraction should be a feature of the libraries, somehow
    top_name = tb_pkg.modules[-1].name
    print([m.name for m in tb_pkg.modules])

    # An ugly part: the not-totally-supported input-differences, including
    # (a) initial condition syntax, (b) hierarchical paths, (c) parameter declarations, (d) using SPICE-format `meas`
    for_xyce = dedent(
        f"""
        .ic xtop:osc_0 0 
        .options device temp={params.temper}
        .param vdd={params.vdd}
        .measure tran trise5  when V(xtop:osc_0)={{vdd/2}} rise=5
        .measure tran trise15 when V(xtop:osc_0)={{vdd/2}} rise=15
    """
    )
    for_spectre = dedent(
        f"""
        options options temp={params.temper}

        simulator lang=spice
        .ic xtop.osc_0 0 
        .param vdd={params.vdd}
        .measure tran trise5  when V(xtop:osc_0)='vdd/2' rise=5
        .measure tran trise15 when V(xtop:osc_0)='vdd/2' rise=15
        .option autostop
        simulator lang=spectre
    """
    )
    literal = (
        for_xyce
        if params.vlsirtools_simulator == SupportedSimulators.XYCE
        else for_spectre
    )
    ctrls = params.ctrls + [Control(literal=literal)]

    sim_input = SimInput(
        top=top_name,
        pkg=tb_pkg,
        an=[
            Analysis(
                tran=TranInput(
                    # analysis_name=f"{top_name}_ro_tran",
                    tstop=50e-9,
                    tstep=1e-12,
                ),
            ),
        ],
        ctrls=ctrls,
    )
    try:
        res = vlsirtools.spice.sim(params.vlsirtools_simulator)(
            sim_input, rundir=params.rundir
        )
    except Exception as e:
        print(e)
        return None
    print(f"ran {params}")
    return res.an[0].tran


def ro_test(
    testcase: TestCase, pdk: Pdk, simulator: Simulator, parentdir: Path
) -> TranResult:
    """ "TestCase Interface" for the RO Tests
    Largely a thin wrapper around `std_cell_ro`. """

    params = StdCellRoParams(
        dut=testcase.dut(pdk),
        nstg=15,
        ctrls=[pdk.include(simulator.enum, testcase.corner)],
        rundir=parentdir / testcase.dirname,
        vlsirtools_simulator=simulator.vlsirtools,
        vdd=pdk.vdd,
        temper=testcase.temper,
    )
    results = std_cell_ro(params)
    return results


def ro_meas(inp: Dict[str, float]) -> Dict[str, float]:
    """ Convert the measurements made directly by SPICE into others that we actually care about. """

    # Get the two relevant values
    trise15 = inp["trise15"]
    trise5 = inp["trise5"]
    # The raw measurements are of ten periods of a 15-stage oscillator.
    # So divided down to one period (by 10),
    # and then by the number of stage-delays (2 * nstg).
    # This will of course need some more parameterization for any-other-size ring.
    return dict(tdelay=(trise15 - trise5) / 10 / 30)


ro_test = Test(name="Ro", run_func=ro_test, meas_func=ro_meas)
