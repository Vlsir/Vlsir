"""
# Vlsir Bindings Unit Tests 
"""

# Import the package under test
import vlsir


def test_sim():
    """# Test creation of a `vlsir.spice.SimInput`"""

    from vlsir.circuit_pb2 import (
        Module,
        Signal,
        Connection,
        ConnectionTarget,
        Port,
        Instance,
    )
    from vlsir.utils_pb2 import Reference, QualifiedName

    inp = vlsir.spice.SimInput()
    inp.pkg.modules.append(
        Module(
            name="top",
            ports=[Port(direction="NONE", signal="VSS")],
            signals=[Signal(name="1", width=1), Signal(name="VSS", width=1)],
            instances=[
                Instance(
                    name="r1",
                    module=Reference(
                        external=QualifiedName(
                            domain="vlsir.primitives", name="resistor"
                        )
                    ),
                    connections=[
                        Connection(portname="p", target=ConnectionTarget(sig="1")),
                        Connection(portname="n", target=ConnectionTarget(sig="VSS")),
                    ],
                )
            ],
        )
    )
    inp.top = "top"
