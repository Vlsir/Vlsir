"""
# Spectre-Format Netlister
"""

# Std-Lib Imports
from typing import Union, List

# Local Imports
import vlsir

# Import the base-class
from .base import Netlister, ResolvedModule, ResolvedParams, SpicePrefix


def map_primitive(rmodule: ResolvedModule, paramvals: ResolvedParams) -> str:
    """ Map a primitive into Spectre's supported names and parameters. 
    Returns the "apparent module name" for instances of the primitive. 
    Argument `paramvals` is often modified along the way. 

    Note spectre syntax is such that the "apparent module name" can be either of: 
    (a) a fixed name per spice-prefix, for basic types (r, c, l, etc), or 
    (b) the *model* name for model-based devices, (mos, bjt, diode, etc) """

    # For voltage sources, add spectre's "type" parameter, and potentially rename several parameters
    if rmodule.spice_prefix == SpicePrefix.VSOURCE:
        vname = rmodule.module_name
        vtypes = dict(vdc="dc", vpulse="pulse", vsin="sine",)
        if vname not in vtypes:
            msg = f"Invalid or unsupported voltage-source type {vname}"
            raise ValueError(msg)
        paramvals.set("type", vtypes[vname])

        if vname == "vpulse":
            # For pulse sources, need to rename most parameters
            paramvals.rename("v1", "val0")
            paramvals.rename("v2", "val1")
            paramvals.rename("td", "delay")
            paramvals.rename("tr", "rise")
            paramvals.rename("tf", "fall")
            paramvals.rename("tpw", "width")
            paramvals.rename("tper", "period")

    # Mapping from spice-prefix to spectre-name for fixed-name types
    basics = {
        SpicePrefix.RESISTOR: "resistor",
        SpicePrefix.CAPACITOR: "capacitor",
        SpicePrefix.INDUCTOR: "inductor",
        SpicePrefix.VSOURCE: "vsource",
        SpicePrefix.ISOURCE: "isource",
        SpicePrefix.VCVS: "vcvs",
        SpicePrefix.VCCS: "vccs",
        SpicePrefix.CCCS: "cccs",
        SpicePrefix.CCVS: "ccvs",
    }
    if rmodule.spice_prefix in basics:
        return basics[rmodule.spice_prefix]

    # Other primitive-types get an "apparent module name" equal to their *model* name.
    model_based = {
        SpicePrefix.MOS,
        SpicePrefix.BIPOLAR,
        SpicePrefix.DIODE,
        SpicePrefix.TLINE,
    }
    if rmodule.spice_prefix in model_based:
        # Get the model-name from its instance parameters
        return paramvals.pop("modelname")

    # Otherwise, unclear what this is or how we got here.
    raise RuntimeError(f"Unsupported or Invalid Primitive {rmodule}")


class SpectreNetlister(Netlister):
    """ Spectre-Format Netlister """

    @property
    def enum(self):
        """ Get our entry in the `NetlistFormat` enumeration """
        from . import NetlistFormat

        return NetlistFormat.SPECTRE

    def write_module_definition(self, module: vlsir.circuit.Module) -> None:
        """ Create a Spectre-format definition for proto-Module `module` """

        # Create the module name
        module_name = self.get_module_name(module)
        # Check for double-definition
        if module_name in self.module_names:
            raise RuntimeError(f"Module {module_name} doubly defined")
        # Add to our visited lists
        self.module_names.add(module_name)
        self.pmodules[module.name] = module

        # Create the sub-circuit definition header
        self.write(f"subckt {module_name} \n")

        if module.ports:  # Create its ports
            self.write("+  ")
            for pport in module.ports:
                self.write(self.format_port_decl(pport) + " ")
            self.write("\n")
        else:
            self.write("+  // No ports \n")

        # Create its parameters, if defined
        if module.parameters:
            self.write("parameters ")
            for name, pparam in module.parameters.items():
                self.write(
                    self.format_param_decl(name, pparam)
                )  # FIXME! NotImplemented
            self.write("\n")
        else:
            self.write("+  // No parameters \n")

        self.write("\n")  # End "header" facets
        # Note nothing need be done for internal signals;
        # spice and spectre create these "out of thin air"

        # Create its instances
        for pinst in module.instances:
            self.write_instance(pinst)
        self.write("\n")

        # Close up the sub-circuit
        self.write("ends \n\n")

    def write_instance(self, pinst: vlsir.circuit.Instance) -> None:
        """Create and return a netlist-string for Instance `pinst`"""

        # Initial resolution phase.
        # Start by getting the Module or ExternalModule definition
        rmodule = self.resolve_reference(pinst.module)

        # Resolve its parameter values
        resolved_instance_parameters = self.get_instance_params(pinst, rmodule.module)

        module, module_name = rmodule.module, rmodule.module_name
        if rmodule.spice_prefix == SpicePrefix.SUBCKT:
            module_name = rmodule.module_name
        else:  # Primitive element. Look up spectre-format module-name
            module_name = map_primitive(rmodule, resolved_instance_parameters)

        # Create the instance name
        self.write(pinst.name + "\n")

        if module.ports:
            self.write("+  // Ports: \n")
            self.write("+  ( ")
            # Get `module`'s port-order
            port_order = [pport.signal.name for pport in module.ports]
            # And write the Instance ports, in that order
            for pname in port_order:
                pconn = pinst.connections.get(pname, None)
                if pconn is None:
                    raise RuntimeError(f"Unconnected Port {pname} on {pinst.name}")
                self.write(self.format_connection(pconn) + " ")
            self.write(" ) \n")
        else:
            self.write("+  // No ports \n")

        # Write the module-name
        self.write("+  " + module_name + " \n")

        if resolved_instance_parameters:  # Write its parameter-values
            self.write("+  ")
            for pname, pval in resolved_instance_parameters.items():
                self.write(f"{pname}={pval} ")
            self.write(" \n")
        else:
            self.write("+  // No parameters \n")

        # And add a post-instance blank line
        self.write("\n")

    def format_concat(self, pconc: vlsir.circuit.Concat) -> str:
        """ Format the Concatenation of several other Connections """
        out = ""
        for part in pconc.parts:
            out += self.format_connection(part) + " "
        return out

    @classmethod
    def format_port_decl(cls, pport: vlsir.circuit.Port) -> str:
        """ Get a netlist `Port` definition """
        return cls.format_signal_ref(pport.signal)

    @classmethod
    def format_port_ref(cls, pport: vlsir.circuit.Port) -> str:
        """ Get a netlist `Port` reference """
        return cls.format_signal_ref(pport.signal)

    @classmethod
    def format_signal_ref(cls, psig: vlsir.circuit.Signal) -> str:
        """ Get a netlist definition for Signal `psig` """
        if psig.width < 1:
            raise RuntimeError
        if psig.width == 1:  # width==1, i.e. a scalar signal
            return psig.name
        # Vector/ multi "bit" Signal. Creates several spice signals.
        return " ".join(
            [f"{psig.name}{cls.format_bus_bit(k)}" for k in reversed(range(psig.width))]
        )

    @classmethod
    def format_signal_slice(cls, pslice: vlsir.circuit.Slice) -> str:
        """Get a netlist definition for Signal-Slice `pslice`"""
        base = pslice.signal
        indices = list(reversed(range(pslice.bot, pslice.top + 1)))
        if not len(indices):
            raise RuntimeError(f"Attempting to netlist empty slice {pslice}")
        return " ".join([f"{base}{cls.format_bus_bit(k)}" for k in indices])

    @classmethod
    def format_bus_bit(cls, index: Union[int, str]) -> str:
        """ Format-specific string-representation of a bus bit-index"""
        # Spectre netlisting uses an underscore prefix, e.g. `bus_0`
        return "_" + str(index)

    def write_comment(self, comment: str) -> None:
        """ While Spectre *can* do a bunch of other comment-styles, 
        the canonical one is generally the C-style line comment beginning with `//`. """
        self.write(f"// {comment}\n")

