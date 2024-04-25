"""
# VlsirTools CLI 
"""

# Std-Lib Imports
import argparse
from enum import Enum
from pathlib import Path
from typing import Union

# Local Imports
from .. import __version__


class Actions(Enum):
    """
    # Actions
    The available command-line actions
    Could this be a more elaborate CLI library thing? Sure.
    """

    VERSION = "version"
    NETLIST = "netlist"
    SIM = "sim"


def main() -> None:
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
            return netlist(data)
        if args.action == Actions.SIM.value:
            return sim(data)

    raise ValueError(f"Invalid CLI action {args.action}")


def netlist(data: Union[str, bytes]) -> None:
    raise TabError


def sim(data: Union[str, bytes]) -> None:
    raise TabError


if __name__ != "__main__":
    msg = f"This command-line interface should not be imported. You probably wanted to run 'python -m vlsirtools.cli' instead."
    raise ImportError(msg)

main()
