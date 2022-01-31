""" 
# Primitive Definitions 

Loaded from adjacent file `vlsir.primitives.pb.txt`
"""

import sys
from pathlib import Path
from .circuit_pb2 import Package

# Get the definition-file from this file's directory
here = Path(__file__).parent.absolute()
prims = here / "vlsir.primitives.pb.txt"

# And parse it into a `circuit.Package`
from google.protobuf import text_format

pkg = Package()
text_format.Parse(open(prims, "r").read(), pkg)

# Also make each `ExternalModule` available in
# (a) A {name: ExternalModule} dictionary, and
# (b) This namespace, under its module-name.
dct = dict()
for emod in pkg.ext_modules:
    # First make sure the module-name is valid, and not already defined.
    modname = emod.name.name
    if "." in modname:
        raise RuntimeError(f"Invalid module-name: {emod.name}")
    if getattr(sys.modules[__name__], modname, None) is not None:
        raise RuntimeError(f"Module-name conflict: {modname}")

    # Checks out: add it
    setattr(sys.modules[__name__], modname, emod)
    dct[modname] = emod
