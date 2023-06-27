"""
# Vlsir Bindings Unit Tests 
"""

# Import the package under test
import vlsir
import vlsir.utils_pb2 as vutils
import vlsir.circuit_pb2 as vckt


def test_utils():
    """Test creation of utility types"""
    vutils.Path(parts=["top"])
    vutils.QualifiedName(domain="xyz", path=vutils.Path(parts=["top"]))
    vutils.Reference(local=vutils.Path(parts=["top"]))
    vutils.Reference(
        external=vutils.QualifiedName(domain="xyz", path=vutils.Path(parts=["top"]))
    )


def test_sim():
    """# Test creation of a `vlsir.spice.SimInput`"""

    inp = vlsir.spice.SimInput()
    inp.pkg.modules.append(
        vckt.Module(
            path=vutils.Path(parts=["top"]),
            ports=[vckt.Port(direction="NONE", signal="VSS")],
            signals=[vckt.Signal(name="1", width=1), vckt.Signal(name="VSS", width=1)],
            instances=[
                vckt.Instance(
                    name="r1",
                    module=vutils.Reference(
                        external=vutils.QualifiedName(
                            domain="vlsir.primitives",
                            path=vutils.Path(parts=["resistor"]),
                        )
                    ),
                    connections=[
                        vckt.Connection(
                            portname="p", target=vckt.ConnectionTarget(sig="1")
                        ),
                        vckt.Connection(
                            portname="n", target=vckt.ConnectionTarget(sig="VSS")
                        ),
                    ],
                )
            ],
        )
    )
    inp.top.parts.extend(["top"])
