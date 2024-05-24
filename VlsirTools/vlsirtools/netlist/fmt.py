""" 
# Netlist Formats
"""

# Std-Lib Imports
from enum import Enum
from typing import Union

# Local Imports
import vlsir

# Locally-defined netlister classes
from .spectre import SpectreNetlister
from .verilog import VerilogNetlister
from .spice import (
    SpiceNetlister,
    HspiceNetlister,
    CdlNetlister,
    XyceNetlister,
    NgspiceNetlister,
)


class NetlistFormat(Enum):
    """Enumeration of available formats.
    Includes string-value conversion."""

    VERILOG = "verilog"
    SPECTRE = "spectre"

    # Spice Dialects
    SPICE = "spice"
    NGSPICE = "ngspice"
    XYCE = "xyce"
    HSPICE = "hspice"
    CDL = "cdl"

    @staticmethod
    def get(spec: "NetlistFormatSpec") -> "NetlistFormat":
        """Get the format specified by `spec`, in either enum or string terms.
        Only does real work in the case when `spec` is a string, otherwise returns it unchanged.
        """
        if isinstance(spec, (NetlistFormat, str)):
            return NetlistFormat(spec)
        raise TypeError

    def netlister(self) -> type:
        """Get the paired netlister-class"""
        if self == NetlistFormat.SPECTRE:
            return SpectreNetlister
        if self == NetlistFormat.VERILOG:
            return VerilogNetlister
        if self == NetlistFormat.SPICE:
            return SpiceNetlister
        if self == NetlistFormat.HSPICE:
            return HspiceNetlister
        if self == NetlistFormat.NGSPICE:
            return NgspiceNetlister
        if self == NetlistFormat.XYCE:
            return XyceNetlister
        if self == NetlistFormat.CDL:
            return CdlNetlister
        raise ValueError(f"Unknown NetlistFormat: {self}")

    def to_proto(self) -> vlsir.netlist.NetlistFormat:
        """Convert a `NetlistFormat` to a protobuf `NetlistFormat`."""
        F = vlsir.netlist.NetlistFormat
        if self == NetlistFormat.SPECTRE:
            return F.SPECTRE
        if self == NetlistFormat.SPICE:
            return F.SPICE
        if self == NetlistFormat.NGSPICE:
            return F.NGSPICE
        if self == NetlistFormat.XYCE:
            return F.XYCE
        if self == NetlistFormat.HSPICE:
            return F.HSPICE
        if self == NetlistFormat.CDL:
            return F.CDL
        if self == NetlistFormat.VERILOG:
            return F.VERILOG
        raise ValueError(f"Unknown NetlistFormat: {self}")

    @staticmethod
    def from_proto(proto: vlsir.netlist.NetlistFormat) -> "NetlistFormat":
        """Convert a protobuf `NetlistFormat` to a `NetlistFormat` enum."""
        F = vlsir.netlist.NetlistFormat
        if proto == F.UNSPECIFIED or proto == F.SPECTRE:
            return NetlistFormat.SPECTRE
        if proto == F.SPICE:
            return NetlistFormat.SPICE
        if proto == F.NGSPICE:
            return NetlistFormat.NGSPICE
        if proto == F.XYCE:
            return NetlistFormat.XYCE
        if proto == F.HSPICE:
            return NetlistFormat.HSPICE
        if proto == F.CDL:
            return NetlistFormat.CDL
        if proto == F.VERILOG:
            return NetlistFormat.VERILOG
        raise ValueError(f"Unknown NetlistFormat: {proto}")


# Type-alias for specifying format, either in enum or string terms
NetlistFormatSpec = Union[NetlistFormat, str]
