"""
# VlsirTools CLI 
"""

# Std-Lib Imports
import argparse
from enum import Enum
from pathlib import Path
from typing import Any

# Local Imports
import vlsir
from .. import __version__
from ..netlist import netlist_from_proto


class Actions(Enum):
    """
    # Actions
    The available command-line actions
    Could this be a more elaborate CLI library thing? Sure.
    """

    VERSION = "version"
    NETLIST = "netlist"
    SIM = "sim"


def main() -> Any:
    """# VlsirTools CLI
    Our very fancy command-line interface."""

    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=[a.value for a in Actions])
    parser.add_argument("target", type=Path)
    args = parser.parse_args()

    if args.action == Actions.VERSION.value:
        return print(__version__)

    with open(args.target, "rb") as f:
        data = f.read()
        if args.action == Actions.NETLIST.value:
            return netlist_action(data)
        if args.action == Actions.SIM.value:
            return sim_action(data)

    raise ValueError(f"Invalid CLI action {args.action}")


def netlist_action(data: bytes) -> vlsir.netlist.NetlistResult:
    """
    # Netlisting CLI Action
    Grab a `NetlistInput` from disk and run it.
    If the input includes a non-empty `result_path`, it is written back to disk, in protobuf binary format.
    """

    inp = vlsir.netlist.NetlistInput()  #
    inp.ParseFromString(data)  # Parse
    result = netlist_from_proto(inp)  # Main action

    if inp.result_path:  # Write back
        result_file = open(inp.result_path, "wb")
        result_file.write(vlsir.NetlistResult.SerializeToString(result))

    return result  # And... why not return it?


def sim_action(data: bytes) -> None:
    raise NotImplementedError


if __name__ != "__main__":
    msg = f"This command-line interface should not be imported. You probably wanted to run 'python -m vlsirtools.cli' instead."
    raise ImportError(msg)

main()
