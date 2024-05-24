""" 
# Vlsir Netlisting 
## The main `netlist` function(s).
"""

# Std-Lib Imports
from dataclasses import dataclass
from typing import IO, Optional

# Local Imports
import vlsir
from .fmt import NetlistFormat, NetlistFormatSpec


@dataclass
class NetlistOptions:
    """Options for netlisting."""

    indent: str = 2 * " "  # Indentation. Defaults to two spaces.
    width: int = 80  # Line-width. Defaults to 80.


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
        raise NotImplementedError("NetlistOptions")  # FIXME!

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
__all__ = [
    "netlist",
    "netlist_from_proto",
    "NetlistFormat",
    "NetlistFormatSpec",
    "NetlistOptions",
]
