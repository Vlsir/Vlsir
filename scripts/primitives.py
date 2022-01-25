""" 
# Vlsir Primitive-Literals Generation Script 

* Creates a `vlsir.circuit.Package`-worth of primitive elements, 
* Writes it in protobuf-text format to file, 
* And (coming soon) copies that file into each language-binding package

Additional code in each language-binding package generally loads the protobuf-text file, 
and potentially adds niceties such as by-name lookup. 
"""

import os, sys, pathlib, copy
from typing import List, Sequence

# Since this all runs in a bootstrappy/ compile-script context,
# tuck your tail between your legs and add the python bindings via `sys.path`.
here = pathlib.Path(__file__).parent.parent.absolute()
pybindings = here / "bindings" / "python"
sys.path.append(str(pybindings))

# Now this should be valid
import vlsir  # noqa
from vlsir.utils_pb2 import QualifiedName
from vlsir.circuit_pb2 import Package, ExternalModule, Port, Signal

# Note this dependency is not stated anywhere either. Just be sure to have it.
from google.protobuf import text_format


def _port(name: str) -> Port:
    # Shorthand to create a width-one, non-directional port named `name`
    return Port(signal=Signal(name=name, width=1), direction="NONE")


def _ports(names: Sequence[str]) -> List[Port]:
    # Shorthand to create a list of `_port`s
    return [_port(name) for name in names]


# Define the frequently re-copied two-terminal passive ports
passive_ports = _ports(["p", "n"])

primitives = Package(
    domain="vlsir.primitives",
    modules=[],  # Empty: no hierarchical/ internally-defined modules
    ext_modules=[  # Primitives are all `ExternalModule`s
        ExternalModule(
            name=vlsir.utils.QualifiedName(domain="vlsir.primitives", name="resistor"),
            desc="Resistor",
            ports=copy.copy(passive_ports),
            parameters=[],  # FIXME
        ),
        ExternalModule(
            name=vlsir.utils.QualifiedName(domain="vlsir.primitives", name="capacitor"),
            desc="Capacitor",
            ports=copy.copy(passive_ports),
            parameters=[],  # FIXME
        ),
        ExternalModule(
            name=vlsir.utils.QualifiedName(domain="vlsir.primitives", name="inductor"),
            desc="Inductor",
            ports=copy.copy(passive_ports),
            parameters=[],  # FIXME
        ),
        ExternalModule(
            name=vlsir.utils.QualifiedName(domain="vlsir.primitives", name="mos"),
            desc="Mosfet Transistor",
            ports=_ports(["d", "g", "s", "b"]),
            parameters=[],  # FIXME
        ),
    ],
)


# Serialize the primitives-package to text
proto_text = text_format.MessageToString(primitives)

# Round-trip it to make sure we get a matching Package
p2 = Package()
text_format.Parse(proto_text, p2)
assert p2 == primitives

# And write to file
txtpath = here / "primitives" / "vlsir.primitives.pb.txt"
with open(str(txtpath), "w") as txtfile:
    txtfile.write(proto_text)

