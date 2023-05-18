import vlsir.circuit_pb2 as vckt
import vlsir.spice_pb2 as vsp


def test_primitives1():
    # Load up and test the primitive definitions
    from vlsirtools import primitives

    assert isinstance(primitives.package, vckt.Package)
    assert primitives.package.domain == "vlsir.primitives"
    assert isinstance(primitives.package.desc, str)
    assert len(primitives.package.desc)
    assert len(primitives.package.modules) == 0
    assert len(primitives.package.ext_modules) > 1

    assert isinstance(primitives.resistor, vckt.ExternalModule)
    assert isinstance(primitives.dct["resistor"], vckt.ExternalModule)
    assert primitives.resistor is primitives.dct["resistor"]

    assert isinstance(primitives.capacitor, vckt.ExternalModule)
    assert isinstance(primitives.dct["capacitor"], vckt.ExternalModule)
    assert primitives.capacitor is primitives.dct["capacitor"]

    assert isinstance(primitives.inductor, vckt.ExternalModule)
    assert isinstance(primitives.dct["inductor"], vckt.ExternalModule)
    assert primitives.inductor is primitives.dct["inductor"]

    assert isinstance(primitives.mos, vckt.ExternalModule)
    assert isinstance(primitives.dct["mos"], vckt.ExternalModule)
    assert primitives.mos is primitives.dct["mos"]

    assert isinstance(primitives.bipolar, vckt.ExternalModule)
    assert isinstance(primitives.dct["bipolar"], vckt.ExternalModule)
    assert primitives.bipolar is primitives.dct["bipolar"]

    assert isinstance(primitives.diode, vckt.ExternalModule)
    assert isinstance(primitives.dct["diode"], vckt.ExternalModule)
    assert primitives.diode is primitives.dct["diode"]
