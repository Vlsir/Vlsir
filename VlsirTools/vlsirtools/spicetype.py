"""
# SPICE Types

The "spice type system", in the form of prefix-characters for instances. 
Implemented as a Python-native `Enum`, 
in which each value is the prefix character. 
Includes methods for conversion to and from the VLSIR schema `enum`. 
"""

# Std-Lib Imports
from enum import Enum

# VLSIR Imports
from vlsir.circuit_pb2 import SpiceType as SchemaSpiceType


class SpiceType(Enum):
    """# Spice Type
    Enumerated Spice Types and their Instance-Name Prefixes"""

    # Sub-circits, either from `Module`s or `ExternalModule`s
    SUBCKT = "x"
    # Ideal Passives
    RESISTOR = "r"
    CAPACITOR = "c"
    INDUCTOR = "l"
    # Semiconductor Devices
    MOS = "m"
    DIODE = "d"
    BIPOLAR = "q"
    # Independent Sources
    VSOURCE = "v"
    ISOURCE = "i"
    # Dependent Sources
    VCVS = "e"
    VCCS = "g"
    CCCS = "f"
    CCVS = "h"
    # Transmission Lines
    TLINE = "o"

    def to_schema(self) -> SchemaSpiceType:
        """Convert to VLSIR protobuf schema"""

        if self == SpiceType.SUBCKT:
            return SchemaSpiceType.SUBCKT
        if self == SpiceType.RESISTOR:
            return SchemaSpiceType.RESISTOR
        if self == SpiceType.CAPACITOR:
            return SchemaSpiceType.CAPACITOR
        if self == SpiceType.INDUCTOR:
            return SchemaSpiceType.INDUCTOR
        if self == SpiceType.MOS:
            return SchemaSpiceType.MOS
        if self == SpiceType.DIODE:
            return SchemaSpiceType.DIODE
        if self == SpiceType.BIPOLAR:
            return SchemaSpiceType.BIPOLAR
        if self == SpiceType.VSOURCE:
            return SchemaSpiceType.VSOURCE
        if self == SpiceType.ISOURCE:
            return SchemaSpiceType.ISOURCE
        if self == SpiceType.VCVS:
            return SchemaSpiceType.VCVS
        if self == SpiceType.VCCS:
            return SchemaSpiceType.VCCS
        if self == SpiceType.CCCS:
            return SchemaSpiceType.CCCS
        if self == SpiceType.CCVS:
            return SchemaSpiceType.CCVS
        if self == SpiceType.TLINE:
            return SchemaSpiceType.TLINE
        raise ValueError(f"Invalid SpiceType: {self}")

    @staticmethod
    def from_schema(schema: SchemaSpiceType) -> "SpiceType":
        """Create from VLSIR schema"""

        if schema == SchemaSpiceType.SUBCKT:
            return SpiceType.SUBCKT
        if schema == SchemaSpiceType.RESISTOR:
            return SpiceType.RESISTOR
        if schema == SchemaSpiceType.CAPACITOR:
            return SpiceType.CAPACITOR
        if schema == SchemaSpiceType.INDUCTOR:
            return SpiceType.INDUCTOR
        if schema == SchemaSpiceType.MOS:
            return SpiceType.MOS
        if schema == SchemaSpiceType.DIODE:
            return SpiceType.DIODE
        if schema == SchemaSpiceType.BIPOLAR:
            return SpiceType.BIPOLAR
        if schema == SchemaSpiceType.VSOURCE:
            return SpiceType.VSOURCE
        if schema == SchemaSpiceType.ISOURCE:
            return SpiceType.ISOURCE
        if schema == SchemaSpiceType.VCVS:
            return SpiceType.VCVS
        if schema == SchemaSpiceType.VCCS:
            return SpiceType.VCCS
        if schema == SchemaSpiceType.CCCS:
            return SpiceType.CCCS
        if schema == SchemaSpiceType.CCVS:
            return SpiceType.CCVS
        if schema == SchemaSpiceType.TLINE:
            return SpiceType.TLINE
        raise ValueError(f"Invalid SchemaSpiceType: {schema}")
