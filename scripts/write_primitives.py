""" 
# Vlsir Primitive-Literals Writer Script 

Writes the primitives `Package` in protobuf-text format. 
"""

import sys
from google.protobuf import text_format
from vlsirtools import primitives
from vlsir.circuit_pb2 import Package


# Serialize the primitives-package to text
proto_text = text_format.MessageToString(primitives)

# Round-trip it to make sure we get a matching Package
p2 = Package()
text_format.Parse(proto_text, p2)
assert p2 == primitives

# Get our destination
if len(sys.argv) > 1:
    dest = open(sys.argv[1], "w")
else:
    dest = sys.stdout

# And write the content
dest.write(proto_text)

# Note there is not "if __main__" here; this is a script, it is ALWAYS main.
