"""
# Vlsir Bindings Unit Tests 
"""

# Import the package under test
import vlsir


def test_version():
    assert vlsir.__version__ == "0.2.1"


def test_sim():
    # Test creation of a `vlsir.spice.SimInput`

    from vlsir.circuit_pb2 import Module, Signal, Connection, Port, Instance
    from vlsir.utils_pb2 import Reference, QualifiedName

    inp = vlsir.spice.SimInput()
    inp.pkg.modules.append(
        Module(
            name="top",
            ports=[Port(direction="NONE", signal=Signal(name="VSS", width=1))],
            signals=[Signal(name="1", width=1)],
            instances=[
                Instance(
                    name="r1",
                    module=Reference(
                        external=QualifiedName(
                            domain="vlsir.primitives", name="resistor"
                        )
                    ),
                    connections=dict(
                        p=Connection(sig=Signal(name="1", width=1)),
                        n=Connection(sig=Signal(name="VSS", width=1)),
                    ),
                )
            ],
        )
    )
    inp.top = "top"


def test_primitives1():
    # Load up and test the primitive definitions
    from vlsir import primitives

    assert isinstance(primitives.pkg, vlsir.circuit.Package)
    assert primitives.pkg.domain == "vlsir.primitives"
    assert isinstance(primitives.pkg.desc, str)
    assert len(primitives.pkg.desc)
    assert len(primitives.pkg.modules) == 0
    assert len(primitives.pkg.ext_modules) > 1

    assert isinstance(primitives.resistor, vlsir.circuit.ExternalModule)
    assert isinstance(primitives.dct["resistor"], vlsir.circuit.ExternalModule)
    assert primitives.resistor is primitives.dct["resistor"]

    assert isinstance(primitives.capacitor, vlsir.circuit.ExternalModule)
    assert isinstance(primitives.dct["capacitor"], vlsir.circuit.ExternalModule)
    assert primitives.capacitor is primitives.dct["capacitor"]

    assert isinstance(primitives.inductor, vlsir.circuit.ExternalModule)
    assert isinstance(primitives.dct["inductor"], vlsir.circuit.ExternalModule)
    assert primitives.inductor is primitives.dct["inductor"]

    assert isinstance(primitives.mos, vlsir.circuit.ExternalModule)
    assert isinstance(primitives.dct["mos"], vlsir.circuit.ExternalModule)
    assert primitives.mos is primitives.dct["mos"]

    assert isinstance(primitives.bipolar, vlsir.circuit.ExternalModule)
    assert isinstance(primitives.dct["bipolar"], vlsir.circuit.ExternalModule)
    assert primitives.bipolar is primitives.dct["bipolar"]

    assert isinstance(primitives.diode, vlsir.circuit.ExternalModule)
    assert isinstance(primitives.dct["diode"], vlsir.circuit.ExternalModule)
    assert primitives.diode is primitives.dct["diode"]

