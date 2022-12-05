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
# TODO: There is a circular dependency on
# bindings/python/vlsir/vlsir.primitives.pb.txt when importing the following
# modules. If the schema changes and the old .pb.txt files does not load this
# import will break, and we will not be able to generate a new .pb.txt file.
# A temporary fix is to comment out the code in
# bindings/python/vlsir/primitives.py.
from vlsir.utils_pb2 import QualifiedName, Param, ParamValue
from vlsir.circuit_pb2 import (
    Package,
    ExternalModule,
    Port,
    Signal,
)


"""
Some Helper Content
"""


def _signal(name: str, width: int = 1) -> Signal:
    return Signal(name=name, width=1)


def _signals(names: Sequence[str]) -> List[Signal]:
    return [_signal(name) for name in names]


def _port(name: str) -> Port:
    # Shorthand to create a width-one, non-directional port named `name`
    return Port(signal=name, direction="NONE")


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

        Defines `ExternalModule`s for irreducible primitive elements, placing them in the namespace `vlsir.primitives`. 
        The content of `vlsir.primitives` largely parallels the "elementary devices" or "primitive devices" 
        implemented by Spice-class simulators. (Example: http://bwrcs.eecs.berkeley.edu/Classes/IcBook/SPICE/UserGuide/elements_fr.html)  

        Many `vlsir.primitives` accept absolute-value parameters, such as the resistance of `resistor` and the inductance of `inductor`. 
        Unless otherwise noted, these parameters are specified in SI units. 
        
        Each `vlsir.primitive` also accepts arbitrary "pass-through" parameters, which are passed unmodifed when generating netlist-level formats. 
        These parameters will generally be used, for instance, to specify `mos` devices across the wide variety of SPICE-supported models. 

    """
    ),
    modules=[],  # Empty: no hierarchical/ internally-defined modules
    ext_modules=[  # Primitives are all `ExternalModule`s
        ExternalModule(
            name=_qname("resistor"),
            desc=dedent(
                """
                # Ideal Resistor

                Ports: (p, n) 
                Params: `r`, resistance (in Ohms)

                Primitive ideal resistor. 
                Largely corresponds to the "R-prefix" element of Spice-class simulators. 
                
                Additional parameters such as temperature coefficients are allowed, and are to be passed unmodified to netlist formats. 
                """
            ),
            ports=_ports(("p", "n")),
            signals=_signals(("p", "n")),
            parameters=[
                Param(name="r", desc="Resistance (Ohms)"),
            ],
        ),
        ExternalModule(
            name=_qname("capacitor"),
            desc=dedent(
                """
                # Ideal Capacitor

                Ports: (p, n) 
                Params: `c`, capacitance (in Farads)

                Primitive ideal capacitor. 
                Largely corresponds to the "C-prefix" element of Spice-class simulators. 
                
                Additional parameters are allowed, and are to be passed unmodified to netlist formats. 
                """
            ),
            ports=_ports(("p", "n")),
            signals=_signals(("p", "n")),
            parameters=[
                Param(name="c", desc="Capacitance (Farads)"),
            ],
        ),
        ExternalModule(
            name=_qname("inductor"),
            desc=dedent(
                """
                # Ideal Inductor

                Ports: (p, n) 
                Params: `l`, inductance (in Henries)

                Primitive ideal inductor. 
                Largely corresponds to the "L-prefix" element of Spice-class simulators. 
                
                Additional parameters are allowed, and are to be passed unmodified to netlist formats. 
                """
            ),
            ports=_ports(("p", "n")),
            signals=_signals(("p", "n")),
            parameters=[
                Param(name="l", desc="Inductance (Henries)"),
            ],
        ),
        ExternalModule(
            name=_qname("vcvs"),
            desc=dedent(
                """
                # Voltage-Controlled Voltage Source

                Ports: (p, n, ctrlp, ctrln) 
                Params: `gain`, voltage gain (in Volts/Volt)

                Largely corresponds to the "e-prefix" element of Spice-class simulators. 
                """
            ),
            ports=_ports(("p", "n", "cp", "cn")),
            signals=_signals(("p", "n", "cp", "cn")),
            parameters=[
                Param(name="gain", desc="Voltage Gain (Volts/Volt)"),
            ],
        ),
        ExternalModule(
            name=_qname("vccs"),
            desc=dedent(
                """
                # Voltage-Controlled Current Source

                Ports: (p, n, ctrlp, ctrln) 
                Params: `gain`, transconductance gain (in Amps/Volt)

                Largely corresponds to the "g-prefix" element of Spice-class simulators. 
                """
            ),
            ports=_ports(("p", "n", "cp", "cn")),
            signals=_signals(("p", "n", "cp", "cn")),
            parameters=[
                Param(name="gain", desc="Transconductance Gain (Amps/Volt)"),
            ],
        ),
        ExternalModule(
            name=_qname("cccs"),
            desc=dedent(
                """
                # Current-Controlled Current Source

                Ports: (p, n, ctrlp, ctrln) 
                Params: `gain`, current gain (in Amps/Amp)

                Largely corresponds to the "f-prefix" element of Spice-class simulators. 
                """
            ),
            ports=_ports(("p", "n", "cp", "cn")),
            signals=_signals(("p", "n", "cp", "cn")),
            parameters=[
                Param(name="gain", desc="Current Gain (Amps/Amp)"),
            ],
        ),
        ExternalModule(
            name=_qname("ccvs"),
            desc=dedent(
                """
                # Current-Controlled Voltage Source

                Ports: (p, n, ctrlp, ctrln) 
                Params: `gain`, transresistance gain (in Volts/Amp)

                Largely corresponds to the "h-prefix" element of Spice-class simulators. 
                """
            ),
            ports=_ports(("p", "n", "cp", "cn")),
            signals=_signals(("p", "n", "cp", "cn")),
            parameters=[
                Param(name="gain", desc="Transresistance Gain (Volts/Amp)"),
            ],
        ),
        ExternalModule(
            name=_qname("isource"),
            desc=dedent(
                """
                # Independent Current Source

                Ports: (p, n) 
                Params: `dc`, dc current (in Amps)

                Largely corresponds to the "i-prefix" element of Spice-class simulators. 
                Sole required parameter `dc` sets the DC value. 
                All other parameters are passed unmodifed to netlist-level formats. 
                """
            ),
            ports=_ports(("p", "n")),
            signals=_signals(("p", "n")),
            parameters=[
                Param(name="dc", desc="DC Current (Amps)"),
            ],
        ),
        ExternalModule(
            name=_qname("vdc"),
            desc=dedent(
                """
                # Independent Voltage Source

                Ports: (p, n) 
                Params: `dc`, dc voltage (in Volts)

                All other parameters are passed unmodifed to netlist-level formats. 
                """
            ),
            ports=_ports(("p", "n")),
            signals=_signals(("p", "n")),
            parameters=[
                Param(name="dc", desc="DC Voltage (Volts)"),
                Param(
                    name="ac",
                    desc="AC/ Small-Signal Magnitude (Volts)",
                    value=ParamValue(integer=0),
                ),
            ],
        ),
        ExternalModule(
            name=_qname("vpulse"),
            desc=dedent(
                """
                # Pulse Voltage Source
                Two-value time-alternating voltage, with parametrizable rise and fall times and delays.

                Ports: (p, n) 
                Params: FIXME!

                All other parameters are passed unmodifed to netlist-level formats. 
                """
            ),
            ports=_ports(("p", "n")),
            signals=_signals(("p", "n")),
            parameters=[
                Param(name="v1", desc="Initial Value (V)"),
                Param(name="v2", desc="Pulse Value (V)"),
                Param(name="td", desc="Delay Time (s)"),
                Param(name="tr", desc="Rise Time (s)"),
                Param(name="tf", desc="Fall Time (s)"),
                Param(name="tpw", desc="Pulse Width (s)"),
                Param(name="tper", desc="Period (s)"),
            ],
        ),
        ExternalModule(
            name=_qname("vsin"),
            desc=dedent(
                """
                # Sinusoidal Voltage Source

                Ports: (p, n) 
                Params: FIXME!

                All other parameters are passed unmodifed to netlist-level formats. 
                """
            ),
            ports=_ports(("p", "n")),
            signals=_signals(("p", "n")),
            parameters=[
                Param(name="voff", desc="Offset voltage (V)"),
                Param(name="vamp", desc="Amplitude (V)"),
                Param(name="freq", desc="Frequency (Hz)"),
                Param(name="td", desc="Delay Time (s)"),
                Param(name="phase", desc="Phase when t=td (degrees)"),
            ],
        ),
        # FIXME: there's no straightforward way to implement "pwl", without list-valued parameters
        # ExternalModule(
        #     name=_qname("vpwl"),
        #     desc=dedent(
        #         """
        #         # Piece-wise Linear Voltage Source
        #         Driven by a set of (time, voltage) pairs.
        #
        #         Ports: (p, n)
        #         Params: FIXME
        #
        #         All other parameters are passed unmodifed to netlist-level formats.
        #         """
        #     ),
        #     ports=_ports(("p", "n")),
        #     signals=_signals(("p", "n")),
        #     parameters=[],
        # ),
        ExternalModule(
            name=_qname("mos"),
            desc=dedent(
                """
                # Mosfet Transistor

                Ports: (d, g, s, b), in identical order to SPICE convention 
                Params: string modelname

                `vlsir.primitives.mos` Largely corresponds to the "M-prefix" element of Spice-class simulators. 
                Each instance maps to a *spice model* instance ("`m1`"), *not* to sub-circuit instance ("`x1`"). 
                In many cases, particularly for technology-provided devices, using a foundry-provided sub-circuit will be appropriate instead. 

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
            signals=_signals(["d", "g", "s", "b"]),
            parameters=[
                Param(name="modelname", desc="Model Name (string)"),
            ],
        ),
        ExternalModule(
            name=_qname("bipolar"),
            desc=dedent(
                """
                # Bipolar Junction Transistor (BJT)

                Ports: (c, b, e), in identical order to SPICE convention 
                Params: string modelname

                `vlsir.primitives.bipolar` Largely corresponds to the "Q-prefix" element of Spice-class simulators. 
                Each instance maps to a *spice model* instance ("`q1`"), *not* to sub-circuit instance ("`x1`"). 
                In many cases, particularly for technology-provided devices, using a foundry-provided sub-circuit will be appropriate instead. 

                Unlike the SPICE BJT, `vlsir.primitives.bipolar` *does not* include an optional fourth substrate terminal. 

                The *sole* required parameter to each `vlsir.primitives.bipolar` is its string-valued `modelname`. 
                While the level-one BJT model has much more prevalence than any MOS model, 
                there remains a diversity of instance parameters not first-class enumerated here. 

                """
            ),
            ports=_ports(("c", "b", "e")),
            signals=_signals(("c", "b", "e")),
            parameters=[
                Param(name="modelname", desc="Model Name (string)"),
            ],
        ),
        ExternalModule(
            name=_qname("diode"),
            desc=dedent(
                """
                # Diode

                Ports: (p (anode), n (cathode)), in identical order to SPICE convention 
                Params: string modelname

                `vlsir.primitives.diode` largely corresponds to the "D-prefix" element of Spice-class simulators. 
                Each instance maps to a *spice model* instance ("`d1`"), *not* to sub-circuit instance ("`x1`"). 
                In many cases, particularly for technology-provided devices, using a foundry-provided sub-circuit will be appropriate instead. 

                The *sole* required parameter to each `vlsir.primitives.diode` is its string-valued `modelname`. 
                While the level-one diode model has much more prevalence than any MOS model, 
                there remains a diversity of instance parameters not first-class enumerated here. 

                """
            ),
            ports=_ports(("p", "n")),
            signals=_signals(("p", "n")),
            parameters=[
                Param(name="modelname", desc="Model Name (string)"),
            ],
        ),
        ExternalModule(
            name=_qname("tline"),
            desc=dedent(
                """
                # Transmission Line

                Ports: (p1p, p1n, (port 1), p2p, p2n (port 2)), in identical order to SPICE convention 
                Params: string modelname

                The *sole* required parameter is the string-valued `modelname`. 
                All other parameters are passed unmodified to netlist-level formats. 
                
                The "model-based" tline specification supports lossy lines in all known SPICE-class simulators, 
                and lossless lines in many or most. 

                """
            ),
            ports=_ports(
                (
                    "p1p",
                    "p1n",
                    "p2p",
                    "p2n",
                )
            ),
            signals=_signals(
                (
                    "p1p",
                    "p1n",
                    "p2p",
                    "p2n",
                )
            ),
            parameters=[
                Param(name="modelname", desc="Model Name (string)"),
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
