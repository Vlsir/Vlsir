"""
# Vlsir Python Tools
Unit Tests
"""

import pytest
import vlsirtools

from io import StringIO
from typing import Dict


def test_version():
    assert vlsirtools.__version__ == "0.2.0"


def test_netlist1():
    # Test netlisting, including instantiating primitives

    from vlsir.circuit_pb2 import Module, Signal, Connection, Port, Instance, Package
    from vlsir.utils_pb2 import Reference, QualifiedName

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
                    Instance(name="r", module=_prim("resistor"), connections=_conns(),),
                    Instance(
                        name="c", module=_prim("capacitor"), connections=_conns(),
                    ),
                    Instance(name="l", module=_prim("inductor"), connections=_conns(),),
                    Instance(name="d", module=_prim("diode"), connections=_conns(),),
                    Instance(
                        name="v", module=_prim("voltagesource"), connections=_conns(),
                    ),
                    Instance(
                        name="i", module=_prim("currentsource"), connections=_conns(),
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
                    ),
                    Instance(
                        name="q",
                        module=_prim("bipolar"),
                        connections=dict(
                            c=Connection(sig=Signal(name="VSS", width=1)),
                            b=Connection(sig=Signal(name="VSS", width=1)),
                            e=Connection(sig=Signal(name="VSS", width=1)),
                        ),
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
