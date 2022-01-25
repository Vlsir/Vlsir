""" 
# Primitive Definitions 

Loaded from adjacent file `vlsir.primitives.pb.txt`
"""

from pathlib import Path
from .circuit_pb2 import Package

# Get the definition-file from this file's directory
here = Path(__file__).parent.absolute()
prims = here / "vlsir.primitives.pb.txt"

# And parse it into a `circuit.Package`
from google.protobuf import text_format

pkg = Package()
text_format.Parse(open(prims, "r").read(), pkg)
