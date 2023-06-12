from types import FunctionType
import vlsir.circuit_pb2 as vckt
from vlsirtools import primitives


def test_primitives1():
    """Test the built-in primitives"""

    assert isinstance(primitives.package, vckt.Package)
    assert primitives.package.domain == "vlsir.primitives"
    assert isinstance(primitives.package.desc, str)
    assert len(primitives.package.desc)
    assert len(primitives.package.modules) == 0
    assert len(primitives.package.ext_modules) == 11
    assert [m.name.name for m in primitives.package.ext_modules] == [
        "resistor",
        "capacitor",
        "inductor",
        "vcvs",
        "vccs",
        "cccs",
        "ccvs",
        "isource",
        "vdc",
        "vpulse",
        "vsin",
    ]

    assert isinstance(primitives.resistor, vckt.ExternalModule)
    assert isinstance(primitives.dct["resistor"], vckt.ExternalModule)
    assert primitives.resistor is primitives.dct["resistor"]

    assert isinstance(primitives.capacitor, vckt.ExternalModule)
    assert isinstance(primitives.dct["capacitor"], vckt.ExternalModule)
    assert primitives.capacitor is primitives.dct["capacitor"]

    assert isinstance(primitives.inductor, vckt.ExternalModule)
    assert isinstance(primitives.dct["inductor"], vckt.ExternalModule)
    assert primitives.inductor is primitives.dct["inductor"]

    assert isinstance(primitives.vcvs, vckt.ExternalModule)
    assert isinstance(primitives.dct["vcvs"], vckt.ExternalModule)
    assert primitives.vcvs is primitives.dct["vcvs"]

    assert isinstance(primitives.vccs, vckt.ExternalModule)
    assert isinstance(primitives.dct["vccs"], vckt.ExternalModule)
    assert primitives.vccs is primitives.dct["vccs"]

    assert isinstance(primitives.cccs, vckt.ExternalModule)
    assert isinstance(primitives.dct["cccs"], vckt.ExternalModule)
    assert primitives.cccs is primitives.dct["cccs"]

    assert isinstance(primitives.ccvs, vckt.ExternalModule)
    assert isinstance(primitives.dct["ccvs"], vckt.ExternalModule)
    assert primitives.ccvs is primitives.dct["ccvs"]

    assert isinstance(primitives.isource, vckt.ExternalModule)
    assert isinstance(primitives.dct["isource"], vckt.ExternalModule)
    assert primitives.isource is primitives.dct["isource"]

    assert isinstance(primitives.vdc, vckt.ExternalModule)
    assert isinstance(primitives.dct["vdc"], vckt.ExternalModule)
    assert primitives.vdc is primitives.dct["vdc"]

    assert isinstance(primitives.vpulse, vckt.ExternalModule)
    assert isinstance(primitives.dct["vpulse"], vckt.ExternalModule)
    assert primitives.vpulse is primitives.dct["vpulse"]

    assert isinstance(primitives.vsin, vckt.ExternalModule)
    assert isinstance(primitives.dct["vsin"], vckt.ExternalModule)
    assert primitives.vsin is primitives.dct["vsin"]


def test_primitive_functions():
    """Test the "primitive generator functions" """

    assert isinstance(primitives.mos, FunctionType)
    mos1 = primitives.mos("mos1")
    assert isinstance(mos1, vckt.ExternalModule)
    assert mos1.name.domain == "vlsir.primitives.mos"
    assert mos1.name.name == "mos1"

    assert isinstance(primitives.bipolar, FunctionType)
    bjt1 = primitives.bipolar("bjt1")
    assert isinstance(bjt1, vckt.ExternalModule)
    assert bjt1.name.domain == "vlsir.primitives.bipolar"
    assert bjt1.name.name == "bjt1"

    assert isinstance(primitives.diode, FunctionType)
    d1 = primitives.diode("d1")
    assert isinstance(d1, vckt.ExternalModule)
    assert d1.name.domain == "vlsir.primitives.diode"
    assert d1.name.name == "d1"

    assert isinstance(primitives.tline, FunctionType)
    t1 = primitives.tline("t1")
    assert isinstance(t1, vckt.ExternalModule)
    assert t1.name.domain == "vlsir.primitives.tline"
    assert t1.name.name == "t1"
