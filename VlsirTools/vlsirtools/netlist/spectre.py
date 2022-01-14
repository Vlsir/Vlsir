"""
# Spectre-Format Netlister 
"""

# Std-Lib Imports
from typing import Union

# Local Imports
import vlsir

# Import the base-class
from .base import Netlister


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

        # Create the instance name
        self.write(pinst.name + "\n")

        # Get its Module or ExternalModule definition, primarily for sake of port-order
        target = self.resolve_reference(pinst.module)
        module, module_name = target.module, target.module_name

        if module.ports:
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

        if pinst.parameters:  # Write the parameter-values
            self.write("+  ")
            for pname, pparam in pinst.parameters.items():
                pval = self.get_param_value(pparam)
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

