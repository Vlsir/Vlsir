"""
# Vlsir Python Tools
Unit Tests
"""

import pytest
from io import StringIO
from typing import Dict, List


import vlsirtools
import vlsir.utils_pb2 as vutils
import vlsir.circuit_pb2 as vckt
import vlsir.spice_pb2 as vsp

from vlsir import Reference, QualifiedName, ParamValue, Param
from vlsirtools.spice import SimOptions, SupportedSimulators, ResultFormat

from vlsir.circuit_pb2 import (
    Module,
    Signal,
    Connection,
    ConnectionTarget,
    Port,
    Instance,
    Package,
)

"""
## Utility & Helper Functions
"""


def _connections(**kwargs):
    """Create a list of `Connection`s from keyword args of the form `portname=conn_target`, where `conn_target` is a `ConnectionTarget`."""
    return [Connection(portname=key, target=value) for key, value in kwargs.items()]


def _params(**kwargs):
    """Create a list of `Param`s from keyword args of the form `r=ParamValue(double=1e3)`"""
    return [Param(name=key, value=value) for key, value in kwargs.items()]


def _prim(name: str) -> Reference:
    """Create a `Reference` to primitive `name`"""
    return Reference(external=QualifiedName(domain="vlsir.primitives", name=name))


from vlsir.utils_pb2 import Reference, QualifiedName, ParamValue, Param


def test_version():
    assert vlsirtools.__version__ == "2.0.dev0"


def test_verilog_netlist1():
    """Test netlisting to a handful of formats, including Verilog-compatible contents."""

    # "Verilog Compatibility" requires:
    # * All ports must be directed. No "NONE" directions.
    # * No primitive instances.
    #
    # The test here covers module, signal, and port creation,
    # and basic instantiation of other local Modules.

    def _ports() -> List[vckt.Port]:
        return [
            Port(direction="INPUT", signal="inp"),
            Port(direction="OUTPUT", signal="out"),
            Port(direction="INOUT", signal="io"),
        ]

    def _signals() -> List[vckt.Signal]:
        return [
            Signal(name="inp", width=1),
            Signal(name="out", width=1),
            Signal(name="io", width=1),
        ]

    pkg = Package(
        domain="vlsirtools.tests.test_verilog_netlist1",
        modules=[
            # Inner, content-less Module, with a port of each direction
            Module(
                name="inner",
                parameters=_params(
                    a=ParamValue(integer=3),
                    b=ParamValue(double=1e-9),
                    d=ParamValue(literal="1+1"),
                    e=ParamValue(
                        prefixed=vutils.Prefixed(prefix="MICRO", string="11.11")
                    ),
                ),
                ports=_ports(),
                signals=_signals(),
            ),
            # Outer top Module which instantiates `inner`
            Module(
                name="top",
                ports=[],
                signals=_signals(),
                instances=[
                    Instance(
                        name="inner",
                        module=Reference(local="inner"),
                        parameters=_params(
                            a=ParamValue(integer=4),
                            b=ParamValue(double=2e-9),
                            d=ParamValue(literal="2+2"),
                            e=ParamValue(
                                prefixed=vutils.Prefixed(prefix="MICRO", string="22.22")
                            ),
                        ),
                        connections=[
                            Connection(portname=name, target=ConnectionTarget(sig=name))
                            for name in ("inp", "out", "io")
                        ],
                    )
                ],
            ),
        ],
    )
    dest = StringIO()
    vlsirtools.netlist(pkg=pkg, dest=dest, fmt="verilog")
    # While verilog is the point here, the other formats should work too:
    vlsirtools.netlist(pkg=pkg, dest=dest, fmt="spice")
    vlsirtools.netlist(pkg=pkg, dest=dest, fmt="spectre")
    vlsirtools.netlist(pkg=pkg, dest=dest, fmt="xyce")


def test_spice_netlist1():
    """Test spice netlisting, including instantiating primitives"""

    def default_conns() -> Dict:
        # Shorthand for connections between node "vvv" and "VSS", used for many instances below.
        return _connections(
            p=ConnectionTarget(sig="vvv"),
            n=ConnectionTarget(sig="VSS"),
        )

    pkg = Package(
        domain="vlsir.tests.test_netlist1",
        modules=[
            Module(
                name="mid",
                parameters=_params(
                    r=ParamValue(double=1e3),
                    l=ParamValue(double=1e-9),
                    c=ParamValue(double=1e-15),
                ),
                ports=[
                    Port(direction="NONE", signal="vvv"),
                    Port(direction="NONE", signal="VSS"),
                ],
                signals=[Signal(name="vvv", width=1), Signal(name="VSS", width=1)],
                instances=[
                    Instance(
                        name="r",
                        module=_prim("resistor"),
                        connections=default_conns(),
                        parameters=_params(r=ParamValue(double=1e3)),
                    ),
                    Instance(
                        name="l",
                        module=_prim("inductor"),
                        connections=default_conns(),
                        parameters=_params(l=ParamValue(double=1e-9)),
                    ),
                    Instance(
                        name="c",
                        module=_prim("capacitor"),
                        connections=default_conns(),
                        parameters=_params(c=ParamValue(double=1e-15)),
                    ),
                    Instance(
                        name="v",
                        module=_prim("vdc"),
                        connections=default_conns(),
                        parameters=_params(
                            dc=ParamValue(double=1.1), ac=ParamValue(double=0)
                        ),
                    ),
                    Instance(
                        name="i",
                        module=_prim("isource"),
                        connections=default_conns(),
                        parameters=_params(dc=ParamValue(double=1e-6)),
                    ),
                    Instance(
                        name="m",
                        module=_prim("mos"),
                        connections=_connections(
                            d=ConnectionTarget(sig="VSS"),
                            g=ConnectionTarget(sig="VSS"),
                            s=ConnectionTarget(sig="VSS"),
                            b=ConnectionTarget(sig="VSS"),
                        ),
                        parameters=_params(
                            modelname=ParamValue(string="some_model_name")
                        ),
                    ),
                    Instance(
                        name="q",
                        module=_prim("bipolar"),
                        connections=_connections(
                            c=ConnectionTarget(sig="VSS"),
                            b=ConnectionTarget(sig="VSS"),
                            e=ConnectionTarget(sig="VSS"),
                        ),
                        parameters=_params(
                            modelname=ParamValue(string="some_model_name")
                        ),
                    ),
                    Instance(
                        name="d",
                        module=_prim("diode"),
                        connections=default_conns(),
                        parameters=_params(
                            modelname=ParamValue(string="some_model_name")
                        ),
                    ),
                ],
            ),
            Module(
                name="top",
                ports=[
                    Port(direction="NONE", signal="VSS"),
                ],
                signals=[Signal(name="vvv", width=1), Signal(name="VSS", width=1)],
                instances=[
                    Instance(
                        name="imid",
                        module=Reference(local="mid"),
                        connections=_connections(
                            vvv=ConnectionTarget(sig="vvv"),
                            VSS=ConnectionTarget(sig="VSS"),
                        ),
                    )
                ],
            ),
        ],
    )
    dest = StringIO()
    vlsirtools.netlist(pkg=pkg, dest=dest, fmt="spice")


def test_netlist_hdl21_ideal1():
    """Test that netlisting a (deprecated) `hdl21.ideal` element fails with a `RuntimeError`."""

    pkg = Package(
        domain="vlsir.tests.test_netlist_hdl21_ideal1",
        modules=[
            Module(
                name="mid",
                ports=[
                    Port(direction="NONE", signal="vvv"),
                    Port(direction="NONE", signal="VSS"),
                ],
                signals=[Signal(name="vvv", width=1), Signal(name="VSS", width=1)],
                instances=[
                    Instance(
                        name="r1",
                        module=Reference(
                            external=QualifiedName(
                                domain="hdl21.ideal",
                                name="IdealResistor",  # FIXME: being deprecated
                            )
                        ),
                        connections=[
                            Connection(
                                portname="p", target=ConnectionTarget(sig="vvv")
                            ),
                            Connection(
                                portname="n", target=ConnectionTarget(sig="VSS")
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
    dest = StringIO()
    with pytest.raises(RuntimeError):
        vlsirtools.netlist(pkg=pkg, dest=dest, fmt="spice")


def empty_testbench_package():
    """Create and return a `circuit.Package` with a single, (near) empty testbench module.
    Some simulators *really* don't like empty DUT content, and others don't like singly-connected nodes.
    So the simplest test-bench is two resistors, in parallel, between ground and a single "other node"."""

    from vlsir import Reference, QualifiedName, Param, ParamValue
    from vlsir.circuit_pb2 import (
        Module,
        Signal,
        Connection,
        ConnectionTarget,
        Port,
        Instance,
        Package,
    )

    def _r(name: str) -> Instance:
        # Create a canned instance of `vlsir.primitives.resistor` with instance-name `name`
        return Instance(
            name=name,  # <= Instance name argument here
            module=Reference(
                external=QualifiedName(domain="vlsir.primitives", name="resistor")
            ),
            connections=[
                Connection(portname="p", target=ConnectionTarget(sig="the_other_node")),
                Connection(portname="n", target=ConnectionTarget(sig="VSS")),
            ],
            parameters=[Param(name="r", value=ParamValue(double=1e3))],
        )

    return Package(
        domain="vlsirtools.tests.empty_testbench_package",
        modules=[
            Module(
                name="empty_testbench",
                ports=[
                    Port(direction="NONE", signal="VSS"),
                ],
                signals=[
                    Signal(name="VSS", width=1),
                    Signal(name="the_other_node", width=1),
                ],
                instances=[
                    _r("r1"),
                    _r("r2"),
                ],
            )
        ],
    )


def test_netlist_empty_testbench():
    """Test netlisting the empty testbench package, used later for simulation tests"""

    dest = StringIO()
    vlsirtools.netlist(pkg=empty_testbench_package(), dest=dest, fmt="spice")
    vlsirtools.netlist(pkg=empty_testbench_package(), dest=dest, fmt="spectre")
    vlsirtools.netlist(pkg=empty_testbench_package(), dest=dest, fmt="xyce")

    # The testbench package is not verilog-compatible; check that it fails.
    with pytest.raises(RuntimeError):
        vlsirtools.netlist(pkg=empty_testbench_package(), dest=dest, fmt="verilog")


@pytest.mark.skipif(
    not vlsirtools.spectre.available(),
    reason="No spectre installation on path",
)
def test_spectre1():
    """Test an empty-input call to the `vlsir.spice.Sim` interface to `spectre`."""
    from vlsir.spice_pb2 import SimInput, SimResult
    from vlsirtools.spectre import sim  # FIXME: this does not specify simulator!

    results = sim(
        SimInput(
            top="empty_testbench",
            pkg=empty_testbench_package(),
        )
    )
    assert isinstance(results, SimResult)


@pytest.mark.skipif(
    not vlsirtools.xyce.available(),
    reason="No Xyce installation on path",
)
def test_xyce1():
    """Test an empty-input call to the `vlsir.spice.Sim` interface to `xyce`."""
    from vlsir.spice_pb2 import SimInput, SimResult
    from vlsirtools.xyce import sim  # FIXME: this does not specify simulator!

    results = sim(
        SimInput(
            top="empty_testbench",
            pkg=empty_testbench_package(),
        )
    )
    assert isinstance(results, SimResult)


@pytest.mark.skipif(
    not vlsirtools.spice.ngspice.available(),
    reason="No ngspice installation on path",
)
def test_ngspice1():
    """Test an empty-input call to the `vlsir.spice.Sim` interface to `xyce`."""
    from vlsir.spice_pb2 import SimInput, SimResult
    from vlsirtools.spice.ngspice import sim  # FIXME: this does not specify simulator!

    results = sim(
        SimInput(
            top="empty_testbench",
            pkg=empty_testbench_package(),
        )
    )
    assert isinstance(results, SimResult)


def test_xyce_import():
    # Just test importing from the `vlsirtools.xyce` path
    from vlsirtools.xyce import sim


def test_spectre_import():
    # Just test importing from the `vlsirtools.spectre` path
    from vlsirtools.spectre import sim


@pytest.mark.skipif(
    not vlsirtools.spice.ngspice.available(),
    reason="No ngspice installation on path",
)
def test_noise1():
    """Test the Noise analysis"""

    # A very complicated testbench: a voltage source and resistor in parallel.
    pkg = vckt.Package(
        domain="vlsirtools.tests.test_noise1",
        modules=[
            vckt.Module(
                name="noisetb",
                ports=[
                    vckt.Port(direction="NONE", signal="VSS"),
                ],
                signals=[
                    vckt.Signal(name="VSS", width=1),
                    vckt.Signal(name="the_other_node", width=1),
                ],
                instances=[
                    Instance(
                        name="r1",
                        module=Reference(
                            external=QualifiedName(
                                domain="vlsir.primitives", name="resistor"
                            )
                        ),
                        connections=[
                            Connection(
                                portname="p",
                                target=ConnectionTarget(sig="the_other_node"),
                            ),
                            Connection(
                                portname="n", target=ConnectionTarget(sig="VSS")
                            ),
                        ],
                        parameters=[Param(name="r", value=ParamValue(double=1e3))],
                    ),
                    Instance(
                        name="v1",
                        module=Reference(
                            external=QualifiedName(
                                domain="vlsir.primitives", name="vdc"
                            )
                        ),
                        connections=[
                            Connection(
                                portname="p",
                                target=ConnectionTarget(sig="the_other_node"),
                            ),
                            Connection(
                                portname="n", target=ConnectionTarget(sig="VSS")
                            ),
                        ],
                        parameters=[
                            Param(name="dc", value=ParamValue(double=0)),
                            Param(name="ac", value=ParamValue(double=0)),
                        ],
                    ),
                ],
            )
        ],
    )
    sim_input = vsp.SimInput(
        pkg=pkg,
        top="noisetb",
        an=[
            vsp.Analysis(
                noise=vsp.NoiseInput(
                    analysis_name="noise1",
                    output_p="the_other_node",
                    output_n="VSS",
                    input_source="v1",
                    fstart=1,
                    fstop=1e10,
                    npts=10,
                    ctrls=[],
                )
            )
        ],
    )
    vlsirtools.spice.sim(
        sim_input,
        opts=SimOptions(
            simulator=SupportedSimulators.NGSPICE, fmt=ResultFormat.SIM_DATA
        ),
    )
