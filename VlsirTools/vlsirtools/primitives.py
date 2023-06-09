""" 
# Vlsir(Tools) Primitives

Defines the `vlsir.circuit.Package`-worth of the primitive elements
"""

from typing import List, Sequence, Optional, Dict
from textwrap import dedent

from vlsir.utils_pb2 import QualifiedName, Param, ParamValue
from vlsir.circuit_pb2 import (
    Package,
    ExternalModule,
    Port,
    Signal,
    SpiceType,
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

domain = "vlsir.primitives"
desc = """
# Vlsir Primitive Modules 

Defines `ExternalModule`s for irreducible primitive elements, placing them in the namespace `vlsir.primitives`. 
The content of `vlsir.primitives` largely parallels the "elementary devices" or "primitive devices" 
implemented by Spice-class simulators. (Example: http://bwrcs.eecs.berkeley.edu/Classes/IcBook/SPICE/UserGuide/elements_fr.html)  

Many `vlsir.primitives` accept absolute-value parameters, such as the resistance of `resistor` and the inductance of `inductor`. 
Unless otherwise noted, these parameters are specified in SI units. 

Each `vlsir.primitive` also accepts arbitrary "pass-through" parameters, which are passed unmodifed when generating netlist-level formats. 
These parameters will generally be used, for instance, to specify `mos` devices across the wide variety of SPICE-supported models. 
"""

package = Package(
    domain=domain,
    desc=desc,
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
            spicetype=SpiceType.RESISTOR,
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
            spicetype=SpiceType.CAPACITOR,
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
            spicetype=SpiceType.INDUCTOR,
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
            spicetype=SpiceType.VCVS,
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
            spicetype=SpiceType.VCCS,
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
            spicetype=SpiceType.CCCS,
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
            spicetype=SpiceType.CCVS,
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
            spicetype=SpiceType.ISOURCE,
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
            spicetype=SpiceType.VSOURCE,
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
            spicetype=SpiceType.VSOURCE,
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
            spicetype=SpiceType.VSOURCE,
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
        #     spicetype = SpiceType.VSOURCE,
        # ),
    ],
)


# Also make each `ExternalModule` available in
# (a) A {name: ExternalModule} dictionary, and
# (b) This namespace, under its module-name.
dct: Dict[str, ExternalModule] = dict()

for emod in package.ext_modules:
    # First make sure the module-name is valid, and not already defined.
    modname = emod.name.name
    if "." in modname:
        raise RuntimeError(f"Invalid module-name: {emod.name}")

    # Check for duplicates/ conflicts
    if dct.get(modname, None) is not None:
        raise RuntimeError(f"Module-name conflict: {modname}")
    if globals().get(modname, None) is not None:
        raise RuntimeError(f"Module-name conflict: {modname}")

    # Checks out: add it
    globals()[modname] = emod
    dct[modname] = emod


"""
# Primitive "Generators" 

Functions which, provided principally a string `name`, produce a primitive-like `ExternalModule`.
These are most useful for SPICE `.model` references, i.e. those commonly used to describe MOS devices. 
"""


def mos(
    name: str, domain: Optional[str] = None, desc: Optional[str] = None
) -> ExternalModule:
    """# Mos Primitive"""

    # Apply defaults to `domain` and `desc`
    domain = domain or "vlsir.primitives.mos"
    desc = desc or dedent(
        """
            # Mosfet Transistor

            Ports: (d, g, s, b), in identical order to SPICE convention 
            Parameters are unconstrainted, and passed along as-is during netlisting.

            `vlsir.primitives.mos` Largely corresponds to the "M-prefix" element of Spice-class simulators. 
            Each instance maps to a *spice model* instance ("`m1`"), *not* to sub-circuit instance ("`x1`"). 
            In many cases, particularly for technology-provided devices, using a foundry-provided sub-circuit will be appropriate instead. 
            """
    )
    return ExternalModule(
        name=QualifiedName(domain=domain, name=name),
        desc=desc,
        ports=_ports(["d", "g", "s", "b"]),
        signals=_signals(["d", "g", "s", "b"]),
        parameters=[],  # Empty (required) parameters list
        spicetype=SpiceType.MOS,
    )


def bipolar(
    name: str, domain: Optional[str] = None, desc: Optional[str] = None
) -> ExternalModule:
    """# Bipolar Primitive"""

    # Apply defaults
    domain = domain or "vlsir.primitives.bipolar"
    desc = desc or dedent(
        """
        # Bipolar Junction Transistor (BJT)

        Ports: (c, b, e), in identical order to SPICE convention 
        Parameters are unconstrainted, and passed along as-is during netlisting.

        `vlsir.primitives.bipolar` Largely corresponds to the "Q-prefix" element of Spice-class simulators. 
        Each instance maps to a *spice model* instance ("`q1`"), *not* to sub-circuit instance ("`x1`"). 
        In many cases, particularly for technology-provided devices, using a foundry-provided sub-circuit will be appropriate instead. 
        Unlike the SPICE BJT, `vlsir.primitives.bipolar` *does not* include an optional fourth substrate terminal. 
        """
    )

    return ExternalModule(
        name=QualifiedName(domain=domain, name=name),
        desc=desc,
        ports=_ports(("c", "b", "e")),
        signals=_signals(("c", "b", "e")),
        parameters=[],  # Empty (required) parameters list
        spicetype=SpiceType.BIPOLAR,
    )


def diode(
    name: str, domain: Optional[str] = None, desc: Optional[str] = None
) -> ExternalModule:
    """# Diode Primitive"""

    # Apply defaults
    domain = domain or "vlsir.primitives.diode"
    desc = desc or dedent(
        """
        # Diode

        Ports: (p (anode), n (cathode)), in identical order to SPICE convention 
        Parameters are unconstrainted, and passed along as-is during netlisting.

        `vlsir.primitives.diode` largely corresponds to the "D-prefix" element of Spice-class simulators. 
        Each instance maps to a *spice model* instance ("`d1`"), *not* to sub-circuit instance ("`x1`"). 
        In many cases, particularly for technology-provided devices, using a foundry-provided sub-circuit will be appropriate instead. 
        """
    )
    return ExternalModule(
        name=QualifiedName(domain=domain, name=name),
        desc=desc,
        ports=_ports(("p", "n")),
        signals=_signals(("p", "n")),
        parameters=[],  # Empty (required) parameters list
        spicetype=SpiceType.DIODE,
    )


def tline(
    name: str, domain: Optional[str] = None, desc: Optional[str] = None
) -> ExternalModule:
    """# Transmission Line Primitive"""

    # Apply defaults
    domain = domain or "vlsir.primitives.tline"
    desc = desc or dedent(
        """
        # Transmission Line

        Ports: (p1p, p1n, (port 1), p2p, p2n (port 2)), in identical order to SPICE convention 
        Parameters are unconstrainted, and passed along as-is during netlisting.

        The "model-based" tline specification supports lossy lines in all known SPICE-class simulators, 
        and lossless lines in many or most. 
        """
    )

    return ExternalModule(
        name=QualifiedName(domain=domain, name=name),
        desc=desc,
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
        parameters=[],  # Empty (required) parameters list
        spicetype=SpiceType.TLINE,
    )
