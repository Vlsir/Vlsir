#!/usr/bin/env python3
#
# Running this script requires that Vlsir schema bindings and VlsirTools both be
# importable by Python. For development you can invoke with:
#   PYTHONPATH=../VlsirTools/:../bindings/python/ ./proto2spice.py

from collections.abc import Sequence
from typing import Optional

import optparse

import google.protobuf.text_format as text_format

import vlsir.raw_pb2 as vlsir_layout
import vlsir.circuit_pb2 as vlsir_circuit
import vlsirtools.netlist as netlist
import vlsirtools as tools


def define_options(optparser: optparse.OptionParser):
    optparser.add_option(
        "-l",
        "--library",
        dest="library",
        default=None,
        help="path to vlsir.raw.Library, in either text- or"
        "binary-format (will try binary first)",
    )
    optparser.add_option(
        "-p",
        "--package",
        dest="package",
        default=None,
        help="path to vlsir.circuit.Package, in either text-"
        " or binary-format proto.",
    )
    optparser.add_option(
        "-o",
        "--output",
        dest="output",
        default="output.sp",
        help="destination path of spice netlist",
    )
    optparser.add_option(
        "-f",
        "--format",
        dest="format",
        default="xyce",
        help="spice format/style/dialect to write",
    )


# Extracts the circuit definitions in a layout Library into a circuit Package,
# and then runs the netlister.
def load_library_into_package(path: str) -> vlsir_circuit.Package:
    library_pb = None
    try:
        with open(path, "rb") as f:
            library_pb = vlsir_layout.Library()
            library_pb.ParseFromString(f.read())
    except FileNotFoundError as err:
        raise err
    except:
        try:
            with open(path, "r") as f:
                library_pb = text_format.Parse(f.read(), vlsir_layout.Library())
        except Exception as err:
            raise IOError(f"Could not load input Library at {path}: {err}")

    package_pb = vlsir_circuit.Package()
    package_pb.modules.extend([cell.module for cell in library_pb.cells])
    return package_pb


def load_package(path: str) -> vlsir_circuit.Package:
    package_pb = None
    try:
        with open(path, "rb") as f:
            package_pb = vlsir_circuit.Package()
            package_pb.ParseFromString(f.read())
    except FileNotFoundError as err:
        raise err
    except:
        try:
            with open(path, "r") as f:
                package_pb = text_format.Parse(f.read(), vlsir_circuit.Package())
        except Exception as err:
            raise IOError(f"Could not load input Package at {path}: {err}")

    return package_pb


def process(options: optparse.Values):
    package_pb = None
    if options.library:
        package_pb = load_library_into_package(options.library)
    elif options.package:
        package_pb = load_package(options.package)

    assert package_pb is not None

    # This is not yet implemented.
    netlist_options = None

    with open(options.output, "w") as output:
        tools.netlist(package_pb, output, fmt=options.format, opts=netlist_options)


def main():
    optparser = optparse.OptionParser()
    define_options(optparser)
    options, _ = optparser.parse_args()
    process(options)


if __name__ == "__main__":
    main()
