""" 
# Vlsir Netlisting 

Exports `vlsir.circuit.Package` to a netlist format.
"""

# Std-Lib Imports
from typing import Union, IO, Optional
from enum import Enum
from dataclasses import dataclass

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


@dataclass
class NetlistOptions:
    """Options for netlisting."""

    indent: str = 2 * " "  # Indentation. Defaults to two spaces.
    width: int = 80  # Line-width. Defaults to 80.


# Type-alias for specifying format, either in enum or string terms
NetlistFormatSpec = Union[NetlistFormat, str]

## FIXME: add more `Netlistable`s
##Netlistable = Union[vlsir.circuit.Package]
Netlistable = vlsir.circuit.Package


def netlist(
    pkg: Netlistable,  ## FIXME: rename
    dest: IO,
    fmt: NetlistFormatSpec = "spectre",
    opts: Optional[NetlistOptions] = None,
) -> None:
    """Netlist proto-Package `pkg` to destination `dest`.

    Example usages:
    ```python
    h.netlist(pkg, dest=open('mynetlist.v', 'w'), fmt='verilog')
    ```
    ```python
    s = StringIO()
    h.netlist(pkg, dest=s, fmt='spectre')
    ```
    ```python
    import sys
    h.netlist(pkg, dest=sys.stdout, fmt='spice')
    ```

    Primary argument `pkg` must be a `vlsir.circuit.Package`.
    Destination `dest` may be anything that supports the `typing.IO` bundle,
    commonly including open file-handles. `StringIO` is particularly helpful
    for producing a netlist in an in-memory string.
    Format-specifier `fmt` may be any of the `NetlistFormatSpec` enumerated values
    or their string equivalents.
    """

    if opts is not None:
        raise NotImplementedError("NetlistOptions not yet implemented.")  # FIXME!

    # If `fmt` is a string, turn it into an enum
    fmt_enum = NetlistFormat.get(fmt)

    # Get the corresponding `Netlister` class and instantiate it
    netlister_cls = fmt_enum.netlister()
    netlister = netlister_cls(dest=dest)

    # Write the netlist
    return netlister.write_package(pkg)


def netlist_from_proto(inp: vlsir.netlist.NetlistInput) -> vlsir.netlist.NetlistResult:
    """# Netlist a ProtoBuf-Dicatated `NetlistInput`"""
    try:
        netlist(
            pkg=inp.pkg,
            dest=open(inp.netlist_path, "w"),
            fmt=NetlistFormat.from_proto(inp.fmt),
            opts=None,
        )
    except Exception as e:
        return vlsir.netlist.NetlistResult(success=False, fail=str(e))
    return vlsir.netlist.NetlistResult(success=True)


# Set our exported content for star-imports
__all__ = ["netlist", "netlist_from_proto", "NetlistFormat", "NetlistFormatSpec"]
