import numpy as np
import hdl21 as h
import vlsir

from .mos_char import MosChar


# Module that lists the testbench params
@h.paramclass
class MosTbParams:
    dut = h.Param(h.Module, desc="DUT Module")
    dut_params = h.Param(dtype=h.Param, desc="Parameters for the DUT")


# Testbench Generator
@h.generator
def mos_tb_generator(params: MosTbParams):
    @h.module
    class MosTb:
        VSS = h.Inout()
        vg = h.Signal()
        vd = h.Signal()
        vb = h.Signal()

        vgs = h.DcVoltageSource(dc="vgs")(p=vg, n=VSS)
        vds = h.DcVoltageSource(dc="vds")(p=vd, n=VSS)
        vbs = h.DcVoltageSource(dc="vbs")(p=vb, n=VSS)
        dut = params.dut(params.dut_params)(D=vd, G=vg, S=VSS, B=vb)

    return MosTb


def generate_mos_db(mos_tb_params, vgs_start, vgs_stop, vgs_step, vds):
    proto = h.to_proto([mos_tb_generator(mos_tb_params)], domain="MosDB")
    sim_input = vlsir.spice.SimInput(pkg=proto)
    sim_input.top = "__main__.BasicCircuit"
    dc_input = vlsir.spice.DcInput(
        analysis_name="DC sweep", indep_name="vgs",
        sweep=vlsir.spice.Sweep(linear=vlsir.spice.LinearSweep(
            start=vgs_start, stop=vgs_stop, step=vgs_step))
    sim_input.an.append(vlsir.spice.Analysis(dc=dc_input)
    breakpoint()

