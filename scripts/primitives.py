""" 
# Vlsir Primitive-Literals Generation Script 

* Creates a `vlsir.circuit.Package`-worth of primitive elements, and 
* Writes it in protobuf-text format to file, 

Additional code in each language-binding package generally loads the protobuf-text file, 
and potentially adds niceties such as by-name lookup. 
"""

import sys, pathlib
from typing import List, Sequence
from textwrap import dedent


"""
Bootstrapping Section 
Load up the python bindings from nearby in this repository.  

Since this all runs in a bootstrappy/ compile-script context,
tuck your tail between your legs and add via `sys.path`.
"""

here = pathlib.Path(__file__).parent.parent.absolute()
pybindings = here / "bindings" / "python"
sys.path.append(str(pybindings))

# Now importing `vlsir` should work
from vlsir.utils_pb2 import QualifiedName
from vlsir.circuit_pb2 import (
    Package,
    ExternalModule,
    Port,
    Signal,
    Parameter,
    ParameterValue,
)


"""
Some Helper Content
"""


def _port(name: str) -> Port:
    # Shorthand to create a width-one, non-directional port named `name`
    return Port(signal=Signal(name=name, width=1), direction="NONE")


def _ports(names: Sequence[str]) -> List[Port]:
    # Shorthand to create a list of `_port`s
    return [_port(name) for name in names]


def _qname(name: str) -> QualifiedName:
    # Shorthand to create a `QualifiedName` in the `vlsir.primitives` domain
    return QualifiedName(domain="vlsir.primitives", name=name)


"""
The Main Event
Definition of the `vlsir.primitives` Package
"""


primitives = Package(
    domain="vlsir.primitives",
    desc=dedent(
        """\
        # Vlsir Primitive Modules 

        Defines `ExternalModule`s for each irreducible primitive element in the namespace `vlsir.primitives`. 
        The content of `vlsir.primitives` largely parallels the "elementary devices" or "primitive devices" 
        implemented by Spice-class simulators. (Example: http://bwrcs.eecs.berkeley.edu/Classes/IcBook/SPICE/UserGuide/elements_fr.html)  

    """
    ),
    modules=[],  # Empty: no hierarchical/ internally-defined modules
    ext_modules=[  # Primitives are all `ExternalModule`s
        ExternalModule(
            name=_qname("mos"),
            desc=dedent(
                """
                # Mosfet Transistor

                Ports: (d, g, s, b), in identical order to SPICE convention 
                Parameters: string modelname

                `Vlsir.primitives.mos` Largely corresponds to the "M-prefix" element of Spice-class simulators. 
                Each instance maps to a *spice model* instance ("`m1`"), *not* to sub-circuit instance ("`x1`"). 
                In many cases, particularly for technology-provided Mos devices, 
                using a foundry-provided sub-circuit will be appropriate instead. 

                The *sole* required parameter to each `vlsir.primitives.mos` is its string-valued `modelname`. 
                Additional parameters such as physical dimensions are typically model-specific and vary widely between models. 
                Conversion from `vlsir.primitives.mos` to spice-netlist formats is to pass all such additional parameters unmodified. 

                Example instantiation:

                ```python
                Instance(
                    name="mos1",
                    module=Reference(domain="vlsir.primitives", name="mos"),
                    connections=dict(d=d, g=g, s=s, b=b),
                    parameters=dict(
                        modelname="my_favorite_nmos", 
                        w=1e-6, 
                        geomod=2, # An example highly model-specific parameter
                    ),
                )
                ```

                Corresponds to netlist-level content along the lines of: 

                ```spice
                .model my_favorite_nmos     * Model statement provided externally 
                + nmos level=53             * Model parameters

                * Instance compiled from `vlsir.primitives.mos`:
                mmos1                       * Note the `m` prefix
                + d g s b                   * Connections 
                + my_favorite_nmos          * Model name
                + w=1e-6 geomod=2           * Instance parameters, unmodified
                ```
                """
            ),
            ports=_ports(["d", "g", "s", "b"]),
            parameters=[Parameter(name="modelname", desc="Model Name (string)"),],
        ),
        ExternalModule(
            name=_qname("bipolar"),
            desc="Bipolar Junction Transistor (BJT)",
            ports=_ports(("c", "b", "e")),
            parameters=[],  # FIXME
        ),
        ExternalModule(
            name=_qname("diode"),
            desc="Diode",
            ports=_ports(("p", "n")),
            parameters=[],  # FIXME
        ),
        ExternalModule(
            name=_qname("resistor"),
            desc="Ideal Resistor",
            ports=_ports(("p", "n")),
            parameters=[],  # FIXME
        ),
        ExternalModule(
            name=_qname("capacitor"),
            desc="Ideal Capacitor",
            ports=_ports(("p", "n")),
            parameters=[],  # FIXME
        ),
        ExternalModule(
            name=_qname("inductor"),
            desc="Ideal Inductor",
            ports=_ports(("p", "n")),
            parameters=[],  # FIXME
        ),
        ExternalModule(
            name=_qname("currentsource"),
            desc="Ideal Current Source",
            ports=_ports(("p", "n")),
            parameters=[],  # FIXME
        ),
        ExternalModule(
            name=_qname("voltagesource"),
            desc="Ideal Voltage Source",
            ports=_ports(("p", "n")),
            parameters=[
                Parameter(
                    name="dc", default=ParameterValue(integer=0), desc="DC Value (V)"
                ),
                Parameter(name="delay", desc="Time Delay (s)"),
                # Pulse source parameters
                Parameter(name="v0", desc="Zero Value (V)"),
                Parameter(name="v1", desc="One Value (V)"),
                Parameter(name="period", desc="Period (s)"),
                Parameter(name="rise", desc="Rise time (s)"),
                Parameter(name="fall", desc="Fall time (s)"),
                Parameter(name="width", desc="Pulse width (s)"),
            ],
        ),
    ],
)

# Note this dependency is not stated anywhere either. Just be sure to have it.
from google.protobuf import text_format

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

