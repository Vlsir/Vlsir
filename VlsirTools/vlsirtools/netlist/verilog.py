"""
# Verilog-Format Netlister 
"""
# Local Imports
import vlsir
import vlsir.circuit_pb2 as vckt

# Import the base-class
from .base import Netlister, SpicePrefix, ResolvedParams


class VerilogNetlister(Netlister):
    """
    # Structural Verilog Netlister
    """

    @property
    def enum(self):
        """Get our entry in the `NetlistFormat` enumeration"""
        from . import NetlistFormat

        return NetlistFormat.VERILOG

    def write_module_definition(self, module: vckt.Module) -> None:
        """Create a Verilog module definition for proto-Module `module`"""

        # Create the module name
        module_name = self.get_module_name(module)
        # Check for double-definition
        if module_name in self.module_names:
            raise RuntimeError(f"Module {module_name} doubly defined")
        # Add to our visited lists
        self.module_names.add(module_name)
        self.pmodules[module.name] = module

        # Collect and index vckt.Signals in this Module by name.
        self.collect_signals_by_name(module)

        # Create the module header
        self.writeln(f"module {module_name}")

        # Write its parameters, if defined
        self.write_param_declarations(module)

        if module.ports:  # Create its ports
            # Don't forget, a trailing comma after the last one is fatal to high-tech Verilog parsers!
            self.writeln("( ")
            self.indent += 1
            for num, pport in enumerate(module.ports):
                comma = "" if num == len(module.ports) - 1 else ","
                self.writeln(self.format_port_decl(pport) + comma)
            self.indent -= 1
            self.writeln("); ")
        else:
            self.writeln("( ) ;  // No ports ")

        self.writeln("")  # Blank line to end "header" facets
        self.indent += 1

        # Write the internal signal declarations
        self.write_internal_signal_declarations()

        if module.instances:  # Create its instances
            self.writeln("")
            self.writeln("// Instance Declarations")
            for pinst in module.instances:
                self.write_instance(pinst)
        else:
            self.writeln("// No Instances")

        # Close up the module
        self.indent -= 1
        self.writeln("")  # Blank before `endmodule`
        self.writeln(f"endmodule // {module_name} \n\n")

    def write_internal_signal_declarations(self) -> None:
        if not self.internal_signals_by_name:
            return self.writeln("// No Signal Declarations")

        self.writeln("// Signal Declarations")
        for psig in self.internal_signals_by_name.values():
            self.writeln(self.format_signal_decl(psig) + "; ")

    def write_param_declarations(self, module: vlsir.circuit.Module) -> None:
        """Write the parameter declarations for Module `module`."""

        if not len(module.parameters):  # No parameters
            # Note we check `len` because `module.parameters` is a protobuf thing, and *who knows* how it converts to `bool`.
            return self.writeln("// No parameters ")

        # Get all the formatted parameter-strings
        formatted = [self.format_param_decl(param) for param in module.parameters]
        # Add the commas to all *BUT THE LAST*. Like JSON, Verilog demands it, or fails.
        formatted = [d + "," for d in formatted[:-1]] + [formatted[-1]]

        # Write them all to our destination
        self.writeln("#( ")
        self.indent += 1
        [self.writeln(f) for f in formatted]
        self.indent -= 1
        self.writeln(") \n")

    def write_instance(self, pinst: vckt.Instance) -> None:
        """Format and write Instance `pinst`"""

        # Get its Module or ExternalModule definition
        rmodule = self.resolve_reference(pinst.module)
        if rmodule.spice_prefix != SpicePrefix.SUBCKT:
            # Spice-level primitives are generally not available in Verilog runtimes,
            # and hence generate errors here if attempted in netlisting.
            raise RuntimeError(f"Invalid module for Verilog: {rmodule}")
        module, module_name = rmodule.module, rmodule.module_name

        # Resolve its parameter values
        resolved_instance_parameters = self.get_instance_params(pinst, module)

        # Write the module-name
        self.writeln(module_name)

        # Write its parameter-values
        self.write_instance_params(resolved_instance_parameters)

        # Write the instance name
        self.writeln(pinst.name)

        if module.ports:  # Write connections, by-name, in-order
            self.writeln("( ")
            self.indent += 1
            # Get `module`'s port-order
            port_order = [pport.signal for pport in module.ports]
            connection_targets = {
                connection.portname: connection.target
                for connection in pinst.connections
            }
            # And write the Instance ports, in that order
            for num, pname in enumerate(port_order):
                ptarget = connection_targets.get(pname, None)
                if ptarget is None:
                    raise RuntimeError(f"Unconnected Port {pname} on {pinst.name}")
                # Again a trailing comma after the last one is fatal!
                comma = "" if num == len(port_order) - 1 else ","
                self.writeln(
                    f".{pname}({self.format_connection_target(ptarget)}){comma} "
                )
            # Close up the ports
            self.indent -= 1
            self.writeln("); ")
        else:
            self.writeln("// No ports ")

        self.writeln("")  # Post-Instance blank line

    def write_instance_params(self, pvals: ResolvedParams) -> None:
        """Write Instance parameters `pvals`"""
        if not pvals:
            return self.writeln("// No parameters ")

        # Write the parameter-values
        self.writeln("#( ")
        self.indent += 1
        # ANSI-style params: .NAME(VALUE)
        formatted = ", ".join([f".{pname}({pval})" for pname, pval in pvals.items()])
        self.writeln(formatted)
        self.indent -= 1
        self.writeln(") ")

    @classmethod
    def format_param_type(cls, pparam: vlsir.Param) -> str:
        """Verilog type-string for `Parameter` `param`."""
        ptype = pparam.WhichOneof("value")
        if ptype == "integer":
            return "longint"
        if ptype == "double":
            return "real"
        if ptype == "string":
            return "string"
        raise ValueError

    @classmethod
    def format_param_decl(cls, param: vlsir.Param) -> str:
        """Format a parameter-declaration"""
        rv = f"parameter {param.name}"
        # FIXME: whether to include datatype
        # dtype = cls.format_param_type(param)
        default = cls.get_param_default(param)
        if default is not None:
            rv += f" = {default}"
        return rv

    def format_concat(self, pconc: vckt.Concat) -> str:
        """Format the Concatenation of several other Connections"""
        # Verilog { a, b, c } concatenation format
        parts = [self.format_connection_target(part) for part in pconc.parts]
        return "{" + ", ".join(parts) + "}"

    def format_port_decl(self, pport: vckt.Port) -> str:
        """Format a `Port` declaration"""

        # First retrieve and check the validity of its direction
        port_type_to_str = {
            vckt.Port.Direction.Value("INPUT"): "input",
            vckt.Port.Direction.Value("OUTPUT"): "output",
            vckt.Port.Direction.Value("INOUT"): "inout",
            vckt.Port.Direction.Value("NONE"): "NO_DIRECTION",
        }
        dir_ = port_type_to_str.get(pport.direction, None)
        if dir_ is None:
            msg = f"Invalid Verilog netlisting for unknown Port direction {pport.direction}"
            raise RuntimeError(msg)
        if dir_ == "NO_DIRECTION":
            msg = f"Invalid Verilog netlisting for undirected Port {pport}"
            raise RuntimeError(msg)

        return dir_ + " " + self.format_signal_decl(self.get_signal(pport.signal))

    def format_signal_decl(self, psig: vckt.Signal) -> str:
        """Format a `Signal` declaration"""
        rv = "wire"
        if psig.width > 1:
            rv += f" [{psig.width-1}:0]"
        rv += f" {psig.name}"
        return rv

    def format_port_ref(self, pport: vckt.Port) -> str:
        """Format a reference to a `Port`.
        Unlike declarations, this just requires the name of its `Signal`."""
        return self.format_signal_ref(self.get_signal(pport.signal))

    @classmethod
    def format_signal_ref(cls, psig: vckt.Signal) -> str:
        """Format a reference to a `Signal`.
        Unlike declarations, this just requires its name."""
        return psig.name

    @classmethod
    def format_signal_slice(cls, pslice: vckt.Slice) -> str:
        """Format Signal-Slice `pslice`"""
        if pslice.top == pslice.bot:  # Single-bit slice
            return f"{pslice.signal}[{pslice.top}]"
        return f"{pslice.signal}[{pslice.top}:{pslice.bot}]"  # Multi-bit slice

    def write_comment(self, comment: str) -> None:
        """Verilog uses C-style line comments, beginning with `//`"""
        self.write(f"// {comment}\n")

    @classmethod
    def format_prefix(cls, pre: vlsir.SIPrefix) -> str:
        """Format a `SIPrefix` to a string"""
        # Verilog does not have the SI prefixes built in. Always write the exponent value.
        map = {
            # Single-character aliases, supported by every SPICE we know
            vlsir.SIPrefix.YOCTO: "e-24",
            vlsir.SIPrefix.ZEPTO: "e-21",
            vlsir.SIPrefix.ATTO: "e-18",
            vlsir.SIPrefix.FEMTO: "e-15",
            vlsir.SIPrefix.PICO: "e-12",
            vlsir.SIPrefix.NANO: "e-9",
            vlsir.SIPrefix.MICRO: "e-6",
            vlsir.SIPrefix.MILLI: "e-3",
            vlsir.SIPrefix.CENTI: "e-2",
            vlsir.SIPrefix.DECI: "e-1",
            vlsir.SIPrefix.UNIT: "",
            vlsir.SIPrefix.DECA: "e1",
            vlsir.SIPrefix.HECTO: "e2",
            vlsir.SIPrefix.KILO: "e3",
            vlsir.SIPrefix.MEGA: "e6",
            vlsir.SIPrefix.GIGA: "e9",
            vlsir.SIPrefix.TERA: "e12",
            vlsir.SIPrefix.PETA: "e15",
            vlsir.SIPrefix.EXA: "e17",
            vlsir.SIPrefix.ZETTA: "e18",
            vlsir.SIPrefix.YOTTA: "e19",
        }
        if pre not in map:
            raise ValueError(f"Invalid or Unsupported SIPrefix {pre}")

        return map[pre]
