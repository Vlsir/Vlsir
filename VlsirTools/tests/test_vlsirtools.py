"""
# Vlsir Python Tools
Unit Tests
"""

import pytest
import vlsirtools

from io import StringIO
from typing import Dict


def test_version():
    assert vlsirtools.__version__ == "1.0.0"


def test_netlist1():
    # Test netlisting, including instantiating primitives

    from vlsir import Reference, QualifiedName, ParamValue
    from vlsir.circuit_pb2 import (
        Module,
        Signal,
        Connection,
        Port,
        Instance,
        Package,
    )

    def _prim(name: str) -> Reference:
        # Shorthand for a `Reference` to primitive `name`
        return Reference(external=QualifiedName(domain="vlsir.primitives", name=name))

    def _conns() -> Dict:
        # Shorthand for connections between node "1" and "VSS", used for many instances below.
        return dict(
            p=Connection(sig=Signal(name="vvv", width=1)),
            n=Connection(sig=Signal(name="VSS", width=1)),
        )

    pkg = Package(
        domain="vlsir.tests.test_netlist1",
        modules=[
            Module(
                name="mid",
                ports=[
                    Port(direction="NONE", signal=Signal(name="vvv", width=1)),
                    Port(direction="NONE", signal=Signal(name="VSS", width=1)),
                ],
                signals=[],
                instances=[
                    Instance(
                        name="r",
                        module=_prim("resistor"),
                        connections=_conns(),
                        parameters=dict(r=ParamValue(double=1e3)),
                    ),
                    Instance(
                        name="c",
                        module=_prim("capacitor"),
                        connections=_conns(),
                        parameters=dict(c=ParamValue(double=1e-15)),
                    ),
                    Instance(
                        name="l",
                        module=_prim("inductor"),
                        connections=_conns(),
                        parameters=dict(l=ParamValue(double=1e-9)),
                    ),
                    Instance(
                        name="v",
                        module=_prim("vdc"),
                        connections=_conns(),
                        parameters=dict(dc=ParamValue(double=1.1)),
                    ),
                    Instance(
                        name="i",
                        module=_prim("isource"),
                        connections=_conns(),
                        parameters=dict(dc=ParamValue(double=1e-6)),
                    ),
                    Instance(
                        name="m",
                        module=_prim("mos"),
                        connections=dict(
                            d=Connection(sig=Signal(name="VSS", width=1)),
                            g=Connection(sig=Signal(name="VSS", width=1)),
                            s=Connection(sig=Signal(name="VSS", width=1)),
                            b=Connection(sig=Signal(name="VSS", width=1)),
                        ),
                        parameters=dict(modelname=ParamValue(string="some_model_name")),
                    ),
                    Instance(
                        name="q",
                        module=_prim("bipolar"),
                        connections=dict(
                            c=Connection(sig=Signal(name="VSS", width=1)),
                            b=Connection(sig=Signal(name="VSS", width=1)),
                            e=Connection(sig=Signal(name="VSS", width=1)),
                        ),
                        parameters=dict(modelname=ParamValue(string="some_model_name")),
                    ),
                    Instance(
                        name="d",
                        module=_prim("diode"),
                        connections=_conns(),
                        parameters=dict(modelname=ParamValue(string="some_model_name")),
                    ),
                ],
            ),
            Module(
                name="top",
                ports=[Port(direction="NONE", signal=Signal(name="VSS", width=1)),],
                signals=[Signal(name="vvv", width=1)],
                instances=[
                    Instance(
                        name="imid",
                        module=Reference(local="mid"),
                        connections=dict(
                            vvv=Connection(sig=Signal(name="vvv", width=1)),
                            VSS=Connection(sig=Signal(name="VSS", width=1)),
                        ),
                    )
                ],
            ),
        ],
    )
    dest = StringIO()
    vlsirtools.netlist(pkg=pkg, dest=dest, fmt="spice")


@pytest.mark.xfail(reason="Hdl21 dependency pending deprecation")
def test_netlist_hdl21_ideal1():
    # Test netlisting an `hdl21.ideal` element

    from vlsir.circuit_pb2 import Module, Signal, Connection, Port, Instance, Package
    from vlsir.utils_pb2 import Reference, QualifiedName

    pkg = Package(
        domain="vlsir.tests.test_netlist_hdl21_ideal1",
        modules=[
            Module(
                name="mid",
                ports=[
                    Port(direction="NONE", signal=Signal(name="vvv", width=1)),
                    Port(direction="NONE", signal=Signal(name="VSS", width=1)),
                ],
                signals=[],
                instances=[
                    Instance(
                        name="r1",
                        module=Reference(
                            external=QualifiedName(
                                domain="hdl21.ideal",
                                name="IdealResistor",  # FIXME: being deprecated
                            )
                        ),
                        connections=dict(
                            p=Connection(sig=Signal(name="vvv", width=1)),
                            n=Connection(sig=Signal(name="VSS", width=1)),
                        ),
                    ),
                ],
            )
        ],
    )
    dest = StringIO()
    vlsirtools.netlist(pkg=pkg, dest=dest, fmt="spice")


def empty_testbench_package():
    """ Create and return a `circuit.Package` with a single, (near) empty testbench module. 
    Some simulators *really* don't like empty DUT content, and others don't like singly-connected nodes. 
    So the simplest test-bench is two resistors, in parallel, between ground and a single "other node". """

    from vlsir import Reference, QualifiedName, ParamValue
    from vlsir.circuit_pb2 import (
        Module,
        Signal,
        Connection,
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
            connections=dict(
                p=Connection(sig=Signal(name="the_other_node", width=1)),
                n=Connection(sig=Signal(name="VSS", width=1)),
            ),
            parameters=dict(r=ParamValue(double=1e3)),
        )

    return Package(
        domain="vlsirtools.tests.empty_testbench_package",
        modules=[
            Module(
                name="empty_testbench",
                ports=[Port(direction="NONE", signal=Signal(name="VSS", width=1)),],
                signals=[Signal(name="the_other_node", width=1),],
                instances=[_r("r1"), _r("r2"),],
            )
        ],
    )


@pytest.mark.skipif(
    not vlsirtools.spectre.available(), reason="No spectre installation on path",
)
def test_spectre1():
    """ Test an empty-input call to the `vlsir.spice.Sim` interface to `spectre`. """
    from vlsir.spice_pb2 import SimInput, SimResult
    from vlsirtools.spectre import sim

    results = sim(SimInput(top="empty_testbench", pkg=empty_testbench_package(),))
    assert isinstance(results, SimResult)


@pytest.mark.skipif(
    not vlsirtools.xyce.available(), reason="No Xyce installation on path",
)
def test_xyce1():
    """ Test an empty-input call to the `vlsir.spice.Sim` interface to `xyce`. """
    from vlsir.spice_pb2 import SimInput, SimResult
    from vlsirtools.xyce import sim

    results = sim(SimInput(top="empty_testbench", pkg=empty_testbench_package(),))
    assert isinstance(results, SimResult)


def test_xyce_import():
    # Just test importing from the `vlsirtools.xyce` path
    from vlsirtools.xyce import sim


def test_spectre_import():
    # Just test importing from the `vlsirtools.spectre` path
    from vlsirtools.spectre import sim

