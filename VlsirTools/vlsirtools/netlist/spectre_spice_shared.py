import vlsir
from .base import Netlister


class SpectreSpiceShared(Netlister):
    """Shared logic between Spectre and Spice netlisters.
    Designed to be a parent class of both."""

    @classmethod
    def format_param_decl(cls, param: vlsir.Param) -> str:
        """Format a parameter-declaration. The `value` field serves as the default value."""
        default = cls.get_param_default(param)
        if default is None:
            # FIXME: this may not be a requirement for *every* Spice netlist syntax.
            # But it's been a requirement throughout for ones that VLSIR supports.
            # At minimum, add some docs to this effect.
            msg = f"Invalid non-default parameter {param} for Spice netlisting"
            raise RuntimeError(msg)
        return f"{param.name}={default}"

    @classmethod
    def format_prefix(cls, pre: vlsir.SIPrefix) -> str:
        """Format a `SIPrefix` to a string"""
        # Use the single-character string where we can, and the exponent otherwise.
        map = {
            # Single-character aliases, supported by every SPICE we know
            vlsir.SIPrefix.ATTO: "a",
            vlsir.SIPrefix.FEMTO: "f",
            vlsir.SIPrefix.PICO: "p",
            vlsir.SIPrefix.NANO: "n",
            vlsir.SIPrefix.MICRO: "u",
            vlsir.SIPrefix.MILLI: "m",
            vlsir.SIPrefix.UNIT: "",
            vlsir.SIPrefix.KILO: "K",
            vlsir.SIPrefix.MEGA: "M",
            vlsir.SIPrefix.GIGA: "G",
            vlsir.SIPrefix.TERA: "T",
            vlsir.SIPrefix.PETA: "P",
            # Fall back to the exponent for the rest
            vlsir.SIPrefix.YOCTO: "e-24",
            vlsir.SIPrefix.ZEPTO: "e-21",
            vlsir.SIPrefix.CENTI: "e-2",
            vlsir.SIPrefix.DECI: "e-1",
            vlsir.SIPrefix.DECA: "e1",
            vlsir.SIPrefix.HECTO: "e2",
            vlsir.SIPrefix.EXA: "e17",
            vlsir.SIPrefix.ZETTA: "e18",
            vlsir.SIPrefix.YOTTA: "e19",
        }
        if pre not in map:
            raise ValueError(f"Invalid or Unsupported SIPrefix {pre}")

        return map[pre]
