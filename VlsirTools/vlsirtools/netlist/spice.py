""" 
# Spice Format Netlisting

"Spice-format" is a bit of a misnomer in netlist-world. 
Of the countless Spice-class simulators have been designed the past half-century, 
most have a similar general netlist format, including: 

* Simulation input comprises a file-full of: 
  * (a) Circuit elements, arranged in `vlsir.Module`s, and
  * (b) Simulator control "cards", such as analysis statements, global parameters, measurements, probes, and the like.
* Circuit-specification is aided by hierarchy, generally in the form of "sub-circuits", denoted `SUBCKT`. 
  * Sub-circuits can commonly be parameterized, and can use a limited set of "parameter programming" to maniupulate their own parameter-values into those of their child-instances. 
  * For example, an instance might be declared as: `xdiode p n area=`width*length``, where `width` and `length` are parameters or its parent.
* `Signal`s are all scalar nets, which are created "out of thin air" whenever referenced. 
* "Typing" performed by instance-name prefixes, e.g. instances named `r1` being interpreted as resistors. 
* Many other subtleties, such as the typical case-insensitivity of netlist content (e.g. `V1` and `v1` are the same net). 

However each simulator also differs in ways large and small. 
Common differences manifest in the areas of: 

* How sub-circuits parameters are declared, and correspondingly how instance-parameter values are set. 
  * Sandia Lab's *Xyce* differs in a prominent fashion, adding a `PARAMS:` keyword where declarations and values begin. 
* How arithmetic expressions are specified, and what functions and expressions are available.
  * Common methods include back-ticks (Hspice) and squiggly-brackets (NgSpice).
  * Notably the asterisk-character (`*`) is the comment-character in many of these formats, and must be wrapped in an expression to perform multiplication. 
* The types and locations of *comments* that are supported. 
  * Some include the fun behavior that comments beginning mid-line require *different* comment-characters from those starting at the beginning of a line.
* While not an HDL attribute, they often differ even more in how simulation control is specified, particularly in analysis and saving is specified. 

"Spice" netlisting therefore requires a small family of "Spice Dialects", 
heavily re-using a central `SpiceNetlister` class, but requiring simulator-specific implementation details. 

"""

# Std-Lib Imports
from typing import Union

# Local Imports
import vlsir
import vlsir.circuit_pb2 as vckt
import vlsir.spice_pb2 as vsp

# Import the base-class
from .spectre_spice_shared import SpectreSpiceShared
from .base import (
    ResolvedModule,
    ResolvedParams,
    SpiceType,
    ModuleLike,
    SpiceBuiltin,
    SpiceModelRef,
)


class SpiceNetlister(SpectreSpiceShared):
    """
    # "Generic" Spice Netlister
    and base-class for Spice dialects.

    Performs nearly all data-model traversal,
    offloading syntax-specifics to dialect-specific sub-classes.

    Attempts to write only the "generic" subset of Spice-content,
    in the "most generic" methods as perceived by the authors.
    This may not work for *any* particular simulator; see the simulator-specific dialects below,
    and the module-level commentary above for more on why.
    """

    @property
    def enum(self):
        """Get our entry in the `NetlistFormat` enumeration"""
        from . import NetlistFormat

        return NetlistFormat.SPICE

    def write_module_definition(self, module: vckt.Module) -> None:
        """Write the `SUBCKT` definition for `Module` `module`."""

        # Create the module name
        module_name = self.get_module_name(module)
        # Check for double-definition
        if module_name in self.module_names:
            raise RuntimeError(f"Module {module_name} doubly defined")

        # Collect and index vckt.Signals in this Module by name.
        self.collect_signals_by_name(module)

        # Add to our visited lists
        self.module_names.add(module_name)
        self.pmodules[module.name] = module

        # Create the sub-circuit definition header
        self.writeln(f".SUBCKT {module_name}")

        # Create its ports, if any are defined
        if module.ports:
            self.write_port_declarations(module)
        else:
            self.write_comment("No ports")

        # Create its parameters, if any are defined
        if module.parameters:
            self.write_param_declarations(module)
        else:
            self.write_comment("No parameters")

        # End the `subckt` header-content with a blank line
        self.write("\n")

        # Create its instances
        for pinst in module.instances:
            self.write_instance(pinst)

        # Write any netlist-literal content
        self.write_literals(module.literals)

        # And close up the sub-circuit
        self.write(".ENDS\n\n")

    def write_port_declarations(self, module: vckt.Module) -> None:
        """Write the port declarations for Module `module`."""
        self.write("+ ")
        for pport in module.ports:
            self.write(self.format_port_decl(pport) + " ")
        self.write("\n")

    def write_param_declarations(self, module: vckt.Module) -> None:
        """Write the parameter declarations for Module `module`.
        Parameter declaration format: `name1=val1 name2=val2 name3=val3`"""
        self.write("+ ")
        for pparam in module.parameters:
            self.write(self.format_param_decl(pparam))
        self.write("\n")

    def write_instance_name(
        self,
        pinst: vckt.Instance,
        spice_type: SpiceType = SpiceType.SUBCKT,
    ) -> None:
        """Write the instance-name line for `pinst`, including the SPICE-dictated primitive-prefix."""
        self.writeln(f"{spice_type.value}{pinst.name}")

    def write_instance(self, pinst: vckt.Instance) -> None:
        """Create and return a netlist-string for Instance `pinst`"""

        # Resolve what kinda thing we are to instantiate
        ref = self.resolve_reference(pinst.module)

        # And dispatch to our writers
        if isinstance(ref, ResolvedModule):
            return self.write_subckt_instance(pinst, ref)

        if isinstance(ref, SpiceModelRef):
            return self.write_model_instance(pinst, ref)

        if isinstance(ref, SpiceBuiltin):
            if ref.spice_type == SpiceType.VSOURCE:
                # Voltage sources get weird, and vary between dialiects. Farm them out to a dedicated method.
                return self.write_voltage_source_instance(pinst, ref)

            # Everything else falls into the `primitive` category
            return self.write_primitive_instance(pinst, ref)

        raise RuntimeError(f"Unrecognized reference type {ref}")

    def write_model_instance(self, pinst: vckt.Instance, ref: SpiceModelRef) -> None:
        """# Write a `.model` instance.
        While sub-classes may modify this behavior, the default is to produce netlist-content
        very similar to that of `write_subckt_instance`, hence the sharing via `write_instance_inner`."""

        return self.write_instance_inner(
            pinst=pinst,
            module=ref.module,
            module_name=ref.model_name,
            spice_type=ref.spice_type,
        )

    def write_subckt_instance(
        self, pinst: vckt.Instance, rmodule: ResolvedModule
    ) -> None:
        """# Write a subcircuit instance.
        While sub-classes may modify this behavior, the default is to produce netlist-content
        very similar to that of `write_model_instance`, hence the sharing via `write_instance_inner`."""

        return self.write_instance_inner(
            pinst=pinst,
            module=rmodule.module,
            module_name=rmodule.module_name,
            spice_type=SpiceType.SUBCKT,
        )

    def write_instance_inner(
        self,
        pinst: vckt.Instance,
        module: ModuleLike,
        module_name: str,
        spice_type: SpiceType,
    ) -> None:
        """Inner implementation of `write_subckt_instance` and `write_model_instance`"""

        # Write the instance name
        self.write_instance_name(pinst, spice_type=spice_type)

        # Write its port-connections
        self.write_instance_conns(pinst, module)

        # Write the sub-circuit name
        self.writeln("+ " + module_name)

        # Write its parameter values
        resolved_param_values = self.get_instance_params(pinst, module)
        self.write_instance_params(resolved_param_values)

        # Add a blank after each instance
        self.write("\n")
        ...

    def write_primitive_instance(self, pinst: vckt.Instance, ref: SpiceBuiltin) -> None:
        """Write primitive-instance `pinst` of `rmodule`.
        Note spice's primitive instances often differn syntactically from sub-circuit instances,
        in that they can have positional (only) parameters."""

        # Write the instance name
        self.write_instance_name(pinst, ref.spice_type)

        # Write its port-connections
        self.write_instance_conns(pinst, ref.module)

        # Resolve its parameter-values to spice-strings
        resolved_param_values = self.get_instance_params(pinst, ref.module)

        # Write special and/or positional parameters
        if ref.spice_type == SpiceType.RESISTOR:
            positional_keys = ["r"]
        elif ref.spice_type == SpiceType.CAPACITOR:
            positional_keys = ["c"]
        elif ref.spice_type == SpiceType.INDUCTOR:
            positional_keys = ["l"]
        elif ref.spice_type == SpiceType.ISOURCE:
            positional_keys = ["dc"]
        elif ref.spice_type in {
            SpiceType.VCVS,
            SpiceType.VCCS,
            SpiceType.CCCS,
            SpiceType.CCVS,
        }:
            positional_keys = ["gain"]
        elif ref.spice_type in {
            SpiceType.MOS,
            SpiceType.BIPOLAR,
            SpiceType.DIODE,
            SpiceType.TLINE,
        }:
            raise RuntimeError(f"Internal error: {ref} should be netlisted as a model")
        elif ref.spice_type == SpiceType.SUBCKT:
            raise RuntimeError(f"Internal error: {ref} should be netlisted as a subckt")
        else:
            raise RuntimeError(f"Unrecognized primitive type {ref.spice_type}")

        # Pop all positional parameters ("pp") from `resolved_param_values`
        pp = resolved_param_values.pop_many(positional_keys)

        # Write the positional parameters, in the order specified by `positional_keys`
        self.writeln("+ " + " ".join([pp[pkey] for pkey in positional_keys]))

        # Now! Write its subckt-style by-name parameter values
        self.write_instance_params(resolved_param_values)

        # Add a blank after each instance
        self.write("\n")

    def write_voltage_source_instance(
        self,
        pinst: vckt.Instance,
        ref: SpiceBuiltin,
    ) -> None:
        """Write a voltage-source instance `pinst`.
        Throws an Exception if `rmodule` is not a known voltage-source type."""

        # Resolve its parameter values
        resolved_param_values = self.get_instance_params(pinst, ref.module)

        # Write the instance name
        self.write_instance_name(pinst, ref.spice_type)

        # Write its port-connections
        self.write_instance_conns(pinst, ref.module)

        # Handle each of the voltage-source cases
        name = ref.module.name.name
        if name == "vdc":
            dc = resolved_param_values.pop("dc")
            self.write(f"+ dc {self.format_expression(dc)} \n")
            ac = resolved_param_values.pop("ac")
            self.write(f"+ ac {self.format_expression(ac)} \n")

        elif name == "vpulse":
            keys = ["v1", "v2", "td", "tr", "tf", "tpw", "tper"]
            pp = resolved_param_values.pop_many(keys)
            self.write(
                f"+ pulse ("
                + " ".join([self.format_expression(pp[k]) for k in keys])
                + ") \n"
            )

        elif name == "vsin":
            keys = ["voff", "vamp", "freq", "td", "phase"]
            pp = resolved_param_values.pop_many(keys)
            self.write(
                f"+ sin ("
                + " ".join([self.format_expression(pp[k]) for k in keys])
                + ") \n"
            )

        else:
            raise ValueError(f"Invalid or unsupported voltage-source type: {name}")

        # Now! Write its subckt-style by-name parameter values
        self.write_instance_params(resolved_param_values)

        # Add a blank after each instance
        self.write("\n")

    def write_instance_conns(self, pinst: vckt.Instance, module: ModuleLike) -> None:
        """Write the port-connections for Instance `pinst`"""

        # Write a quick comment for port-less modules
        if not module.ports:
            self.write("+ ")
            return self.write_comment("No ports")

        self.write("+ ")
        # And write the Instance ports, in that order
        port_order = [pport.signal for pport in module.ports]
        connection_targets = {
            connection.portname: connection.target for connection in pinst.connections
        }
        for pname in port_order:
            ptarget = connection_targets.get(pname, None)
            if ptarget is None:
                raise RuntimeError(f"Unconnected Port {pname} on {pinst.name}")
            self.write(self.format_connection_target(ptarget) + " ")
        self.write("\n")

    def write_instance_params(self, pvals: ResolvedParams) -> None:
        """
        Format and write the parameter-values in dictionary `pvals`.

        Parameter-values format:
        ```
        XNAME
        + <ports>
        + <subckt-name>
        + name1=val1 name2=val2 name3=val3
        """

        if not pvals:  # Write a quick comment for no parameters
            self.write_comment("No parameters")
        else:
            self.write("+ ")

        # And write them
        for (pname, pval) in pvals.items():
            self.write(f"{pname}={self.format_expression(pval)} ")

        self.write("\n")

    def format_concat(self, pconc: vckt.Concat) -> str:
        """Format the Concatenation of several other Connections"""
        out = ""
        for part in pconc.parts:
            out += self.format_connection_target(part) + " "
        return out

    def format_port_decl(self, pport: vckt.Port) -> str:
        """Get a netlist `Port` definition"""
        signal = self.get_signal(pport.signal)
        return self.format_signal_ref(signal)

    def format_port_ref(self, pport: vckt.Port) -> str:
        """Get a netlist `Port` reference"""
        signal = self.get_signal(pport.signal)
        return self.format_signal_ref(signal)

    @classmethod
    def format_signal_ref(cls, psig: vckt.Signal) -> str:
        """Get a netlist definition for Signal `psig`"""
        if psig.width < 1:
            raise RuntimeError
        if psig.width == 1:  # width==1, i.e. a scalar signal
            return psig.name
        # Vector/ multi "bit" Signal. Creates several spice signals.
        return " ".join(
            [f"{psig.name}{cls.format_bus_bit(k)}" for k in reversed(range(psig.width))]
        )

    @classmethod
    def format_signal_slice(cls, pslice: vckt.Slice) -> str:
        """Get a netlist definition for Signal-Slice `pslice`"""
        base = pslice.signal
        indices = list(reversed(range(pslice.bot, pslice.top + 1)))
        if not len(indices):
            raise RuntimeError(f"Attempting to netlist empty slice {pslice}")
        return " ".join([f"{base}{cls.format_bus_bit(k)}" for k in indices])

    @classmethod
    def format_bus_bit(cls, index: Union[int, str]) -> str:
        """Format-specific string-representation of a bus bit-index"""
        # Spectre netlisting uses an underscore prefix, e.g. `bus_0`
        return "_" + str(index)

    def write_comment(self, comment: str) -> None:
        """While dialects vary, the *generic* Spice-comment begins with the asterisk."""
        self.write(f"* {comment}\n")

    def format_expression(self, expr: str) -> str:
        """Format a string such that the target format interprets it as an expression.
        Example:
        ```
        * Parameter Declarations
        .param v0=1 v1='v0+1' * <= Here
        * Instance with the same name
        v0 1 0 dc='v0+2*v1' * <= And here
        ```
        Note the latter case includes the star character (`*`) for multiplication,
        where in many other contexts it is treated as the comment-character.
        """
        # The base class does what (we think) is the most common practice:
        # wrapping expressions in single-tick quotes.
        return f"'{expr}'"


class HspiceNetlister(SpiceNetlister):
    """
    # Hspice-Format Netlister

    Other than its `NetlistFormat` enumeration, `HspiceNetlister` is identical to the base `SpiceNetlister`.
    """

    @property
    def enum(self):
        """Get our entry in the `NetlistFormat` enumeration"""
        from . import NetlistFormat

        return NetlistFormat.HSPICE


class XyceNetlister(SpiceNetlister):
    """Xyce-Format Netlister"""

    @property
    def enum(self):
        """Get our entry in the `NetlistFormat` enumeration"""
        from . import NetlistFormat

        return NetlistFormat.XYCE

    def write_param_declarations(self, module: vckt.Module) -> None:
        """Write the parameter declarations for Module `module`.
        Parameter declaration format:
        .SUBCKT <name> <ports>
        + PARAMS: name1=val1 name2=val2 name3=val3 \n
        """
        self.write("+ PARAMS: ")  # <= Xyce-specific
        for pparam in module.parameters:
            self.write(self.format_param_decl(pparam))
        self.write("\n")

    def write_instance_params(self, pvals: ResolvedParams) -> None:
        """Write the parameter-values for Instance `pinst`.

        Parameter-values format:
        ```
        XNAME
        + <ports>
        + <subckt-name>
        + PARAMS: name1=val1 name2=val2 name3=val3
        """

        self.write("+ ")
        if not pvals:  # Write a quick comment for no parameters
            return self.write_comment("No parameters")

        self.write("PARAMS: ")  # <= Xyce-specific
        for (pname, pval) in pvals.items():
            self.write(f"{pname}={self.format_expression(pval)} ")

        self.write("\n")

    def write_comment(self, comment: str) -> None:
        """Xyce comments *kinda* support the Spice-typical `*` charater,
        but *only* as the first character in a line.
        Any mid-line-starting comments must use `;` instead.
        So, just use it all the time."""
        self.write(f"; {comment}\n")

    def format_expression(self, expr: str) -> str:
        # Xyce expressions are wrapped in curly braces.
        return f"{{{expr}}}"

    @classmethod
    def format_sim_dut(cls, module_name: str) -> str:
        """# Format the top-level DUT instance for module name `module_name`."""
        return f"xtop 0 {module_name} ; Top-Level DUT \n"

    def write_include(self, inc: vsp.Include) -> None:
        """# Write an `Include`"""
        self.writeln(f".include '{inc.path}'")

    def write_lib_include(self, lib: vsp.LibInclude) -> None:
        """# Write a `LibInclude`"""
        self.writeln(f".lib {lib.path} {lib.section}")

    def write_save(self, save: vsp.Save) -> None:
        # FIXME!
        raise NotImplementedError(f"Unimplemented control card {save} for {self}")

    def write_meas(self, meas: vsp.Meas) -> None:
        """# Write a measurement."""
        line = f".meas {meas.analysis_type} {meas.name} {meas.expr} \n"
        self.writeln(line)

    def write_sim_param(self, param: vlsir.Param) -> None:
        """# Write a simulation parameter."""
        line = f".param {param.name}={self.get_param_value(param.value)} \n"
        self.writeln(line)

    def write_sim_option(self, opt: vsp.SimOptions) -> None:
        # FIXME: make this just `Param` instead
        raise NotImplementedError

    def write_ac(self, an: vsp.AcInput) -> None:
        """# Write an AC analysis."""
        raise NotImplementedError

    def write_dc(self, an: vsp.DcInput) -> None:
        """# Write a DC analysis."""
        raise NotImplementedError

    def write_op(self, an: vsp.OpInput) -> None:
        """# Write an operating point analysis."""
        raise NotImplementedError

    def write_tran(self, an: vsp.TranInput) -> None:
        """# Write a transient analysis."""
        raise NotImplementedError

    def write_noise(self, an: vsp.NoiseInput) -> None:
        """# Write a noise analysis."""
        raise NotImplementedError


class NgspiceNetlister(SpiceNetlister):
    """
    Ngspice-Format Netlister
    Should be identical to the base Spice netlister
    """

    @property
    def enum(self):
        """Get our entry in the `NetlistFormat` enumeration"""
        from . import NetlistFormat

        return NetlistFormat.NGSPICE

    @classmethod
    def format_sim_dut(cls, module_name: str) -> str:
        """# Format the top-level DUT instance for module name `module_name`."""
        return f"xtop 0 {module_name} // Top-Level DUT \n\n"

    def write_include(self, inc: vsp.Include) -> None:
        return self.writeln(f'.include "{inc.path}"')

    def write_lib_include(self, lib: vsp.LibInclude) -> None:
        txt = f'.lib "{lib.path}" {lib.section}'
        return self.writeln(txt)

    def write_save(self, save: vsp.Save) -> None:
        # FIXME!
        raise NotImplementedError(f"Unimplemented Save {save} for {self}")

    def write_meas(self, meas: vsp.Meas) -> None:
        txt = f".meas {meas.analysis_type} {meas.name} {meas.expr}"
        return self.writeln(txt)

    def write_sim_param(self, param: vlsir.Param) -> None:
        txt = f".param {param.name}={self.get_param_value(param.value)}"
        return self.writeln(txt)

    def write_sim_option(self, opt: vsp.SimOptions) -> None:
        # FIXME: make this just `Param` instead
        return self.writeln(f".option {opt.name} = {self.get_param_value(opt.value)}\n")

    def write_ac(self, an: vsp.AcInput) -> None:
        """# Write an AC analysis."""

        if not an.analysis_name:
            raise RuntimeError(f"Analysis name required for {an}")
        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        # Unpack the analysis / sweep content
        fstart = an.fstart
        if fstart <= 0:
            raise ValueError(f"Invalid `fstart` {fstart}")
        fstop = an.fstop
        if fstop <= 0:
            raise ValueError(f"Invalid `fstop` {fstop}")
        npts = an.npts
        if npts <= 0:
            raise ValueError(f"Invalid `npts` {npts}")

        # Write the analysis command
        line = f".ac dec {npts} {fstart} {fstop}\n\n"
        self.writeln(line)

    def write_dc(self, an: vsp.DcInput) -> None:
        """# Write a DC analysis."""

        if not an.analysis_name:
            raise RuntimeError(f"Analysis name required for {an}")
        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        # Write the analysis command
        param = an.indep_name
        ## Interpret the sweep
        sweep_type = an.sweep.WhichOneof("tp")
        if sweep_type == "linear":
            sweep = an.sweep.linear
            line = (
                f".dc param start={sweep.start} stop={sweep.stop} step={sweep.step}\n\n"
            )
            self.writeln(line)
        elif sweep_type == "points":
            raise ValueError("NG Spice does not support a DC point sweep")
            sweep = an.sweep.points
            line = f".dc values=[{sweep.points}]\n\n"
            self.writeln(line)
        elif sweep_type == "log":
            raise NotImplementedError
        else:
            raise ValueError("Invalid sweep type")

    def write_op(self, an: vsp.OpInput) -> None:
        """# Write an operating point analysis."""

        if not an.analysis_name:
            raise RuntimeError(f"Analysis name required for {an}")
        if len(an.ctrls):
            raise NotImplementedError  # FIXME!

        self.writeln(f".op\n")

    def write_tran(self, an: vsp.TranInput) -> None:
        """# Write a transient analysis."""
        if not an.analysis_name:
            raise RuntimeError(f"Analysis name required for {an}")
        if len(an.ctrls):
            raise NotImplementedError
        if len(an.ic):
            raise NotImplementedError

        self.writeln(f".tran {an.tstep} {an.tstop}\n")

    def write_noise(self, an: vsp.NoiseInput) -> None:
        """# Write a noise analysis."""

        if not an.analysis_name:
            raise RuntimeError(f"Analysis name required for {an}")
        if len(an.ctrls):
            raise NotImplementedError

        self.writeln(f".save all")

        # NgSpice's syntax for a hierarchical reference to a net is (apparently) `v(v.<dot-separated-path>)`
        # and similarly a source is `v.<dot-separated-path>`.
        #
        # In response to "where on earth did you find this?" @avi wrote:
        # "this isn't really documented anywhere. I figured this out on a hunch from the syntax for saving transistor parameters, which is something like @m.path_to_transistor[param_name]"
        #
        if an.output_n:  # Differential output spec
            noise_output = f"v(v.xtop.{an.output_p}, v.xtop.{an.output_n})"
        else:
            noise_output = f"v(v.xtop.{an.output_p})"

        # NOTE: the `noise_input_source` being a *voltage* source is functionally encoded here,
        # particularly by the "v" prepended to its name.
        # Should we ever support current source noise inputs, we'll need to change this.
        noise_input_source = f"v.xtop.v{an.input_source}"
        noise_sweep = f"dec {an.npts} {an.fstart} {an.fstop}"
        self.writeln(f".noise {noise_output} {noise_input_source} {noise_sweep}\n")


class CdlNetlister(SpiceNetlister):
    """FIXME: CDL-Format Netlister"""

    def __init__(self, *_, **__):
        raise NotImplementedError

    @property
    def enum(self):
        """Get our entry in the `NetlistFormat` enumeration"""
        from . import NetlistFormat

        return NetlistFormat.CDL
