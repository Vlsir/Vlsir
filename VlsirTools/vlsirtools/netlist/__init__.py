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
    HSPICE = "hspice"
    NGSPICE = "ngspice"
    XYCE = "xyce"
    CDL = "cdl"

    @staticmethod
    def get(spec: "NetlistFormatSpec") -> "NetlistFormat":
        """Get the format specified by `spec`, in either enum or string terms.
        Only does real work in the case when `spec` is a string, otherwise returns it unchanged."""
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
        raise ValueError


@dataclass
class NetlistOptions:
    """Options for netlisting."""

    indent: str = 2 * " "  # Indentation. Defaults to two spaces.
    width: int = 80  # Line-width. Defaults to 80.


# Type-alias for specifying format, either in enum or string terms
NetlistFormatSpec = Union[NetlistFormat, str]


def netlist(
    pkg: vlsir.circuit.Package,
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

    fmt_enum = NetlistFormat.get(fmt)
    netlister_cls = fmt_enum.netlister()
    netlister = netlister_cls(pkg, dest)
    netlister.netlist()


# Set our exported content for star-imports
__all__ = ["netlist", "NetlistFormat", "NetlistFormatSpec"]
