"""
# Netlister Base Class 
"""

# Std-Lib Imports
from typing import Optional, Union, IO, Dict, Iterable, List, Tuple
from dataclasses import dataclass, field

# Local Imports
import vlsir
import vlsir.circuit_pb2 as vckt
import vlsir.spice_pb2 as vsp
from .. import primitives
from ..spicetype import SpiceType

# Internal type shorthand
ModuleLike = Union[vckt.Module, vckt.ExternalModule]


@dataclass
class ResolvedModule:
    """Resolved reference to a `Module` or `ExternalModule`.
    Includes its spice-language prefix, and if user-defined its netlist-sanitized module-name.
    """

    module: ModuleLike
    module_name: str


@dataclass
class SpiceBuiltin:
    """# Reference to a SPICE built-in element, e.g. the ideal resistor, capacitor, or voltage source.
    Many formats include special syntax for defining these, e.g. parameter specifications that work for no other instance."""

    module: vckt.ExternalModule
    # External module definition, generally from `vlsir.primitives`. Largely used for ports and parameters.
    spice_type: SpiceType  # Spice type. One of the "non-model" variants.


@dataclass
class SpiceModelRef:
    """# Reference to a SPICE Model, e.g. a MOSFET model, defined with some variant of the `.model` statement."""

    module: vckt.ExternalModule  # External module definition
    model_name: str  # Model name
    spice_type: SpiceType  # Spice type. Can be any variant but SUBCKT.


# Union type of the targets for netlist instances
ResolvedRef = Union[ResolvedModule, SpiceBuiltin, SpiceModelRef]


@dataclass
class ResolvedParams:
    """Resolved Instance-Parameter Values
    Factoring in defaults, and converted to strings.
    Largely a wrapper for `Dict[str, str]`, with accessors `get` and `pop` that raise `RuntimeError` if a key is missing.
    """

    inner: Dict[str, str]

    def set(self, key: str, val: str) -> None:
        """Set the value of `key` to `val` in the resolved parameters."""
        self.inner[key] = val

    def get(self, key: str) -> str:
        """Get the value of `key` from the resolved parameters.
        Raises `RuntimeError` if `key` is not present."""
        if key not in self.inner:
            raise RuntimeError(f"Missing parameter {key}")
        return self.inner[key]

    def pop(self, key: str) -> str:
        """Get the value of `key` from the resolved parameters, and remove it from the `ResolvedParams`.
        Raises `RuntimeError` if `key` is not present."""
        if key not in self.inner:
            raise RuntimeError(f"Missing parameter {key}")
        return self.inner.pop(key)

    def pop_many(self, keys: Iterable[str]) -> Dict[str, str]:
        """Get the values of `keys` from the resolved parameters, and remove them from the `ResolvedParams`.
        Raises `RuntimeError` if any `key` is not present."""
        return {key: self.pop(key) for key in keys}

    def rename(self, old: str, new: str) -> None:
        """Rename a key from `old` to `new`.
        Raises an exception if `old` is not a key."""
        val = self.pop(old)
        self.set(new, val)

    @property
    def items(self):
        return self.inner.items

    def __bool__(self) -> bool:
        """Boolean conversions, generally through the `not` keyword or `bool` constructor,
        are forwarded down to the internal `inner` dictionary."""
        return bool(self.inner)

    def __contains__(self, key: str) -> bool:
        return key in self.inner


@dataclass
class Indent:
    """
    # Indentation Helper

    Supports in-place addition and subtraction of indentation levels, e.g. via
    ```python
    indent = Indent()
    indent += 1 # Adds one "tab", or indentation level
    indent += 1 # Adds another
    indent -= 1 # Drops back by one
    ```
    The current indentation-string is available via the `state` attribute.
    Writers using such an indenter will likely be of the form:
    ```python
    dest.write(f"{indent.state}{content}")
    ```
    """

    # Per-"tab" indentation characters. Defaults to two spaces.
    chars: str = 2 * " "
    # Current (integer) indentation-level, in number of "tabs"
    num: int = field(init=False, default=0)
    # Current indentation-string. Always equals `num * chars`.
    state: str = field(init=False, default="")

    def __post_init_post_parse__(self) -> None:
        self.state = self.chars * self.num

    def __iadd__(self, other: int) -> None:
        """In-place add, i.e. `indent += 1`"""
        self.num += other
        self.state = self.chars * self.num
        return self

    def __isub__(self, other: int) -> None:
        """In-place subtract, i.e. `indent -= 1`"""
        self.num = self.num - other
        if self.num < 0:
            raise ValueError("Negative indentation")
        self.state = self.chars * self.num
        return self


class Netlister:
    """# Abstract Base `Netlister` Class

    `Netlister` is not directly instantiable, and none of its sub-classes are intended
    for usage outside the `netlist` package. The primary API method `netlist` is designed to
    create, use, and drop a `Netlister` instance.
    Once instantiated a `Netlister`'s primary API method is `netlist`.
    This writes all content in its `pkg` field to destination `dest`.

    Internal methods come in three primary flavors:
    * `write_*` methods, which write to `self.dest`. These methods are generally format-specific.
    * `format_*` methods, which return format-specific strings, but *do not* write to `dest`.
    * `get_*` methods, which retrieve some internal data, e.g. extracting the type of a `Connection`.
    """

    def __init__(self, dest: IO):
        self.dest = dest
        self.indent = Indent(chars="  ")

        self.module_names = set()  # Netlisted Module names
        self.pmodules = dict()  # Visited proto-Modules

        # Keep two dictionaries tracking `ExternalModule`s:
        # * The VLSIR schema identifies them to two-string (domain, name) tuples. This is their "primary key".
        # * Most netlist formats use a single global namespace, and require a unique name for each `ExternalModule`.
        # So it's possible for two distinct VLSIR ExternalModules to conflict in netlist-language.
        # If and when this happens netlisting will raise an exception.
        # FIXME: that could maybe be configurable?
        self.ext_modules_by_key: Dict[Tuple[str, str], vckt.ExternalModule] = dict()
        self.ext_modules_by_name: Dict[str, vckt.ExternalModule] = dict()

        # Similar tracking of ExternalModules which resolve to SPICE `.model` definitions
        # Note in many formats, sub-circuits and models have different namespaces -
        # i.e. it is possible to have a sub-circuit and a model with the same name.
        self.spice_models_by_name: Dict[str, vckt.ExternalModule] = dict()

        # Attributes of the currently-netlisted Module

        # Signals in the currently-visited module, keyed by name
        # Includes *all* ports and internal signals
        self.signals_by_name: Dict[str, vckt.Signal] = dict()
        # Internal signals, keyed by name, *excluding* ports
        self.internal_signals_by_name: Dict[str, vckt.Signal] = dict()
        # Names of all ports, for membership testing
        self.port_names = set()  # : Set[str]

    """
    # Core Interactions with our Destination `IO`
    """

    def write(self, s: str) -> None:
        """Helper/wrapper, passing to `self.dest`"""
        self.dest.write(s)

    def writeln(self, s: str) -> None:
        """Write `s` as a line, at our current `indent` level."""
        self.write(f"{self.indent.state}{s}\n")

    def flush(self) -> None:
        """Flush `self.dest`."""
        self.dest.flush()

    """ 
    # Data Model Helpers
    """

    def get_external_module(self, emod: vckt.ExternalModule) -> None:
        """# Visit an `ExternalModule`
        "Netlisting" these doesn't actually write anything, but just stores a reference in internal dictionaries for future references to them.

        Note each netlister keeps two dictionaries tracking `ExternalModule`s:
        * The VLSIR schema identifies them to two-string (domain, name) tuples. This is their "primary key".
        * Most netlist formats use a single global namespace, and require a unique name for each `ExternalModule`.
        So it's possible for two distinct VLSIR ExternalModules to conflict in netlist-language.
        If and when this happens netlisting will raise an exception.
        FIXME: that could maybe be configurable?
        """

        # Check for duplicate definitions by "primary key" (domain, name)
        # Note we *do not* check on a name-only basis here; this is left to instantiation-time,
        # largely so that we can determine which ExternalModules resolve to subcircuits vs SPICE models.
        key = (emod.name.domain, emod.name.name)
        if key in self.ext_modules_by_key:
            raise RuntimeError(f"Invalid doubly-defined external module {emod}")
        self.ext_modules_by_key[key] = emod

    @classmethod
    def get_param_default(cls, pparam: vlsir.Param) -> Optional[str]:
        """Get the default value of `pparam`. Returns `None` for no default."""
        if pparam.value.WhichOneof("value") is None:
            return None
        return cls.get_param_value(pparam.value)

    @classmethod
    def get_param_value(cls, ppval: vlsir.ParamValue) -> str:
        """Get a string representation of a parameter-value"""
        ptype = ppval.WhichOneof("value")
        if ptype == "integer":
            return str(int(ppval.integer))
        if ptype == "double":
            return str(float(ppval.double))
        if ptype == "string":
            # String-valued parameters get embedded in double-quotes
            return f'"{str(ppval.string)}"'
        if ptype == "literal":
            # Whereas *literal* strings, e.g. "22.22e6-11e-1", do not.
            return str(ppval.literal)
        if ptype == "prefixed":
            return cls.format_prefixed(ppval.prefixed)
        raise ValueError(f"Invalid Param type {ptype}")

    @classmethod
    def get_instance_params(
        cls, pinst: vckt.Instance, pmodule: ModuleLike
    ) -> ResolvedParams:
        """Resolve the parameters of `pinst` to their values, including default values provided by `pmodule`.
        Raises a `RuntimeError` if any required parameter is not defined.

        Note this method *does not* raise errors for parameters *not specified* in `pmodule`,
        allowing for "pass-through" parameters not explicitly defined."""

        values = dict()
        # The price of not attaching this as a property of the instance is that we have to recompute it every time.
        instance_parameters = dict()
        for param in pinst.parameters:
            instance_parameters[param.name] = param.value

        # Step through each of `pmodule`'s declared parameters first, applying defaults if necessary
        for mparam in pmodule.parameters:
            if mparam.name in instance_parameters:  # Specified by the Instance
                inst_pval = instance_parameters.pop(mparam.name)
                values[mparam.name] = cls.get_param_value(inst_pval)
            else:  # Not specified by the instance. Apply the default, or fail.
                pdefault = cls.get_param_default(mparam)
                if pdefault is None:
                    msg = f"Required parameter `{mparam.name}` not specified for Instance `{pinst}`"
                    raise RuntimeError(msg)
                values[mparam.name] = pdefault

        # Convert the remaining instance-provided parameters to strings
        for pname, pval in instance_parameters.items():
            values[pname] = cls.get_param_value(pval)

        # And wrap the resolved values in a `ResolvedParams` object
        return ResolvedParams(values)

    @classmethod
    def get_module_name(cls, module: vckt.Module) -> str:
        """Create a netlist-compatible name for proto-Module `module`"""

        # Create the module name
        # Replace all format-invalid characters with underscores
        name = module.name.split(".")[-1]
        for ch in name:
            if not (ch.isalpha() or ch.isdigit() or ch == "_"):
                name = name.replace(ch, "_")
        return name

    def resolve_reference(self, ref: vlsir.utils.Reference) -> ResolvedRef:
        """Resolve the `ModuleLike` referent of `ref`."""

        if ref.WhichOneof("to") == "local":  # Internally-defined Module
            module = self.pmodules.get(ref.local, None)
            if module is None:
                raise RuntimeError(f"Invalid undefined Module {ref.local} ")
            return ResolvedModule(
                module=module,
                module_name=self.get_module_name(module),
            )

        if ref.WhichOneof("to") == "external":  # Defined outside package
            # First check the priviledged/ internally-defined domains
            if ref.external.domain == "vlsir.primitives":
                # Built-in primitive. Load its definition from the `vlsir.primitives` (python) module.
                name = ref.external.name
                module = primitives.dct.get(ref.external.name, None)
                if module is None:
                    raise RuntimeError(f"Invalid undefined primitive {ref.external}")

                schema_spice_type = vckt.SpiceType.Name(module.spicetype)
                if schema_spice_type is None:
                    msg = f"Invalid SpiceType for {module}"
                    raise RuntimeError(msg)
                spice_type = SpiceType[schema_spice_type]

                # Double-check it has a valid SpiceType
                # Note the `vlsir.primitives` module *itself* should be well-behaved, only defining types in the `valid_types` list below.
                # But it's Python! Nothing stops *users* from modifying them, or trying to define their own!

                if spice_type == SpiceType.SUBCKT:
                    msg = f"Invalid SUBCKT in the `vlsir.primitives` namespace: {ref}\n"
                    msg += "(Did you try to define this yourself?)\n"
                    msg += "`vlsir.primitives` is a priviledged namespace, and cannot be modified."
                    raise RuntimeError(msg)

                model_based = {
                    SpiceType.MOS,
                    SpiceType.BIPOLAR,
                    SpiceType.DIODE,
                    SpiceType.TLINE,
                }
                if spice_type in model_based:
                    msg = f"Invalid/ deprecated model-based `vlsir.primitive` {ref}"
                    raise RuntimeError(msg)

                valid_types = {
                    SpiceType.RESISTOR,
                    SpiceType.CAPACITOR,
                    SpiceType.INDUCTOR,
                    SpiceType.VSOURCE,
                    SpiceType.ISOURCE,
                    SpiceType.VCVS,
                    SpiceType.VCCS,
                    SpiceType.CCCS,
                    SpiceType.CCVS,
                }
                if spice_type not in valid_types:
                    raise ValueError(f"Unsupported or Invalid Primitive {ref}")

                return SpiceBuiltin(
                    module=module,
                    spice_type=spice_type,
                )

            if ref.external.domain == "hdl21.primitives":
                msg = f"Invalid direct-netlisting of physical `hdl21.Primitive` `{ref.external.name}`. "
                msg += "Either compile to a target technology, or replace with an `ExternalModule`. "
                raise RuntimeError(msg)

            else:  # Externally-Defined, External-Domain `ExternalModule`
                key = (ref.external.domain, ref.external.name)
                module = self.ext_modules_by_key.get(key, None)
                if module is None:
                    msg = f"Invalid Instance of undefined External Module {key}"
                    raise RuntimeError(msg)

                schema_spice_type = vckt.SpiceType.Name(module.spicetype)
                if schema_spice_type is None:
                    msg = f"Invalid SpiceType for {module}"
                    raise RuntimeError(msg)
                spice_type = SpiceType[schema_spice_type]

                if spice_type == SpiceType.SUBCKT:  # External sub-circuit

                    # Check for duplicates on a name-only basis
                    # Most netlist formats have a single global namespace, so same-names conflict in netlist-language.
                    module_name = ref.external.name
                    cached = self.ext_modules_by_name.get(module_name, None)
                    if cached is not None and cached is not module:
                        msg = f"Conflicting ExternalModule definitions {module} and {cached}"
                        raise RuntimeError(msg)
                    self.ext_modules_by_name[module_name] = module

                    return ResolvedModule(
                        module=module,
                        module_name=module_name,
                    )

                else:  # SPICE Model Reference

                    # Again check for duplicates on a name-only basis
                    modelname = ref.external.name
                    cached = self.spice_models_by_name.get(modelname, None)
                    if cached is not None and cached is not module:
                        msg = f"Conflicting ExternalModule definitions {module} and {cached}"
                        raise RuntimeError(msg)
                    self.spice_models_by_name[modelname] = module

                    return SpiceModelRef(
                        module=module,
                        model_name=modelname,
                        spice_type=spice_type,
                    )

        # Not a Module, not an ExternalModule, not sure what it is
        raise ValueError(f"Invalid Module reference {ref}")

    def get_signal(self, name: str) -> vckt.Signal:
        """Get Signal `name` from the current Module's mapping.
        Raises a `RuntimeError` if the Signal is not found."""

        sig = self.signals_by_name.get(name, None)
        if sig is None:
            msg = f"Unknown signal: {name} in {self.signals_by_name.keys()}"
            raise RuntimeError(msg)
        return sig

    def collect_signals_by_name(self, module: vckt.Module):
        """Collect a `Module`'s worth of signals into a dictionary keyed by name.
        This often proves important for references to internal Signals, e.g. in Ports and Slices.
        """

        # Reset the state of our mappings
        self.signals_by_name = {}
        self.port_names = set()
        self.internal_signals_by_name = {}

        # Collect all the port-names into our set
        for port in module.ports:
            if port.signal in self.port_names:
                raise RuntimeError(f"Duplicate Port {port.signal}")
            self.port_names.add(port.signal)

        # Collect all Signals into dictionaries
        for signal in module.signals:
            if signal.name in self.signals_by_name:
                msg = f"Duplicate signal definition in Module {module.name}"
                raise RuntimeError(msg)
            self.signals_by_name[signal.name] = signal
            if signal.name not in self.port_names:
                self.internal_signals_by_name[signal.name] = signal

    @classmethod
    def validate_sim_top(cls, inp: vsp.SimInput) -> vckt.Module:
        """# Ensure that `SimInput` `inp`'s `top` module exists,
        and adheres to the "Spice top-level" port-interface: a single port for ground / VSS / node-zero.
        Returns the top-level `ModuleLike` when successful, or raises a `RuntimeError` when not.
        # FIXME: make `ExternalModule` valid too!
        """
        if not inp.top:
            cls.fail(f"No top-level module specified in {inp}")

        # Build a mapping from names to Modules
        module_name_dict: Dict[str, vckt.Module] = {m.name: m for m in inp.pkg.modules}

        # Check that the top-level module exists
        top = module_name_dict.get(inp.top, None)
        if top is None:
            msg = f"Top-level module `{inp.top}` not found among Modules {list(module_name_dict.keys())}"
            cls.fail(msg)

        # Check that the top-level module has a single port, for ground / VSS / node-zero
        if len(top.ports) != 1:
            msg = f"`vlsir.SimInput` top-level module {inp.top} must have *one* (VSS) port - has {len(module.ports)} ports [{module.ports}]"
            cls.fail(msg)

        return top

    """
    # Write Methods Implemented Here 
    Largely the things which are *not* format-specific, but instead traverse the data model and dispatch to other, format-specific methods.
    """

    def write_sim_input(self, inp: vsp.SimInput) -> None:
        """# Write simulation-input `inp` to `self.dest`."""

        # Write the header
        self.write_sim_header(inp)

        # Write the circuit-definitions package
        self.write_package(pkg=inp.pkg)

        # Write the top-level instance
        self.write_sim_dut(inp)

        # Write sim options
        self.write_sim_options(inp.opts)

        # Write each control element
        self.write_control_elements(inp.ctrls)

        # Write each analysis
        for an in inp.an:
            self.write_analysis(an)

        # Write a few blanks at the end
        self.write(3 * "\n")

        # And ensure all output makes it to `self.dest`
        self.dest.flush()

    def write_sim_header(self, inp: vsp.SimInput) -> None:
        """# Write header commentary for a `SimInput`
        This proves particularly important for many Spice-like formats,
        which *always* interpret the first line of an input-file as a comment (among many other dumb things).
        So, always write one there right off the bat."""

        self.write_comment(f"`{self.enum.value}` Sim Input for `{inp.top}`")
        self.write_comment(f"Generated by `vlsirtools.{self.__class__.__name__}`")
        self.write_comment("")

    def write_sim_dut(self, inp: vsp.SimInput) -> None:
        """# Write the top-level DUT instance for `inp`."""

        top = self.validate_sim_top(inp)
        top_name = self.get_module_name(top)
        self.writeln(self.format_sim_dut(top_name))

    def write_package(self, pkg: vckt.Package) -> None:
        """# Write circuit-Package `pkg` to `self.dest`."""

        # First visit any externally-defined Modules,
        # Ensuring we have their port-orders.
        for emod in pkg.ext_modules:
            self.get_external_module(emod)

        # Add some header commentary
        self.write_package_header(pkg)

        # Now do the real stuff,
        # Creating netlist entries for each package-defined Module
        for mod in pkg.modules:
            self.write_module_definition(mod)

        # And ensure all output makes it to `self.dest`
        self.dest.flush()

    def write_package_header(self, pkg: vckt.Package) -> None:
        """# Write header commentary for a `Package`
        This proves particularly important for many Spice-like formats,
        which *always* interpret the first line of an input-file as a comment (among many other dumb things).
        So, always write one there right off the bat."""

        if pkg.domain:
            self.write_comment(f"`circuit.Package` `{pkg.domain}`")
        else:
            self.write_comment(f"Anonymous `circuit.Package`")
        self.write_comment(f"Generated by `vlsirtools.{self.__class__.__name__}`")
        self.write_comment("")
        self.writeln("")

    def write_control_elements(self, ctrls: List[vsp.Control]) -> None:
        """# Write a list of `Control` elements"""
        for ctrl in ctrls:
            self.write_control_element(ctrl=ctrl)

    def write_control_element(self, ctrl: vsp.Control) -> None:
        """# Write a `Control` element"""

        # `Control` is largely a type-union of these things; dispatch across them.
        inner = ctrl.WhichOneof("ctrl")
        if inner == "include":
            return self.write_include(ctrl.include)
        if inner == "lib":
            return self.write_lib_include(ctrl.lib)
        if inner == "literal":
            return self.write_literal(ctrl.literal)
        if inner == "param":
            return self.write_sim_param(ctrl.param)
        if inner == "meas":
            return self.write_meas(ctrl.meas)
        if inner == "save":
            return self.write_save(ctrl.save)
        self.fail(f"Unknown control type: {inner}")

    def write_sim_options(self, options: List[vsp.SimOptions]) -> None:
        # FIXME: make this just `List[Param]` instead
        for opt in options:
            self.write_sim_option(opt)

    def write_analysis(self, an: vsp.Analysis) -> None:
        """# Write an `Analysis`, largely dispatching its content to a type-specific method."""

        inner = an.WhichOneof("an")
        inner_dispatch = dict(
            ac=self.write_ac,
            dc=self.write_dc,
            op=self.write_op,
            tran=self.write_tran,
            noise=self.write_noise,
        )
        if inner not in inner_dispatch:
            self.fail(f"Invalid analysis type {inner}")
        analysis_writer = inner_dispatch[inner]
        return analysis_writer(getattr(an, inner))

    def write_literal(self, literal: str) -> None:
        """# Write a literal string"""
        return self.writeln(literal)

    """ 
    # Format Methods Implemented Here
    """

    def format_connection_target(self, ptarget: vckt.ConnectionTarget) -> str:
        """Format a `ConnectionTarget` reference.
        Does not *declare* any new connection objects, but generates references to existing ones.
        """
        # `ConnectionTarget`s are a proto `oneof` union
        # which includes signals, slices, and concatenations.
        # Figure out which to import

        stype = ptarget.WhichOneof("stype")
        if stype == "sig":
            signal = self.get_signal(ptarget.sig)
            return self.format_signal_ref(signal)
        if stype == "slice":
            return self.format_signal_slice(ptarget.slice)
        if stype == "concat":
            return self.format_concat(ptarget.concat)
        raise ValueError(f"Invalid Type {stype} for Connection Target {ptarget}")

    @classmethod
    def format_prefixed(cls, pre: vlsir.Prefixed) -> str:
        prefix = cls.format_prefix(pre.prefix)
        numtp = pre.WhichOneof("number")
        if numtp == "integer":
            num = str(pre.integer)
        elif numtp == "string":
            num = str(pre.string)
        elif numtp == "double":
            raise ValueError(f"Deprecated double-valued Prefixed parameter {pre}")
        else:
            raise ValueError(f"Invalid `Prefixed` number type {numtp}")

        # Note the "prefix" is in fact at the *end*,
        # e.g. "5u", "11K".
        # (Calling it a *pre*-fix refers to *units*, not to numeric values)
        return f"{num}{prefix}"

    def write_literals(self, literals: List[str]) -> None:
        """# Write a list of literal strings, one per line."""
        for literal in literals:
            self.writeln(literal)

    """ 
    Virtual `write` Methods 
    """

    def write_comment(self, comment: str) -> None:
        """Format and string a string comment.
        "Line comments" are the sole supported variety, which fit within a line, and extend to the end of that line.
        The `write_comment` method assumes responsibility for closing the line."""
        raise NotImplementedError

    def write_module_definition(self, pmodule: vckt.Module) -> None:
        """Write Module `module`"""
        raise NotImplementedError

    def write_param_declarations(self, module: vckt.Module) -> None:
        """Write all parameter declarations for `module`"""
        raise NotImplementedError

    def write_instance(self, pinst: vckt.Instance) -> str:
        """Write Instance `pinst`"""
        raise NotImplementedError

    def write_instance_params(self, pvals: ResolvedParams) -> None:
        """Write Instance parameters `pvals`"""
        raise NotImplementedError

    def write_include(self, inc: vsp.Include) -> None:
        """# Write an `Include` statement"""
        raise NotImplementedError

    def write_lib_include(self, lib: vsp.LibInclude) -> None:
        """# Write a `LibInclude` statement"""
        raise NotImplementedError

    def write_save(self, save: vsp.Save) -> None:
        """# Write a `Save` statement"""
        raise NotImplementedError

    def write_meas(self, meas: vsp.Meas) -> None:
        """# Write a `Meas` statement"""
        raise NotImplementedError

    def write_sim_param(self, param: vlsir.Param) -> None:
        """# Write a simulation-level parameter"""
        raise NotImplementedError

    def write_sim_option(self, opt: vsp.SimOptions) -> None:
        """# Write a simulation option"""
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

    """ 
    Virtual `format` Methods 
    """

    @classmethod
    def format_param_decl(cls, param: vlsir.Param) -> str:
        """Format a named `Parameter` definition"""
        raise NotImplementedError

    @classmethod
    def format_port_decl(cls, pport: vckt.Port) -> str:
        """Format a declaration of a `Port`"""
        raise NotImplementedError

    @classmethod
    def format_port_ref(cls, pport: vckt.Port) -> str:
        """Format a reference to a `Port`"""
        raise NotImplementedError

    @classmethod
    def format_signal_decl(cls, psig: vckt.Signal) -> str:
        """Format a declaration of Signal `psig`"""
        raise NotImplementedError

    @classmethod
    def format_signal_ref(cls, psig: vckt.Signal) -> str:
        """Format a reference to Signal `psig`"""
        raise NotImplementedError

    @classmethod
    def format_signal_slice(cls, pslice: vckt.Slice) -> str:
        """Format Signal-Slice `pslice`"""
        raise NotImplementedError

    def format_concat(self, pconc: vckt.Concat) -> str:
        """Format the Concatenation of several other Connections"""
        raise NotImplementedError

    @classmethod
    def format_bus_bit(cls, index: Union[int, str]) -> str:
        """Format bus-bit `index`"""
        raise NotImplementedError

    @classmethod
    def format_prefix(cls, pre: vlsir.SIPrefix) -> str:
        """Format a `SIPrefix` to a string"""
        raise NotImplementedError

    @classmethod
    def format_sim_dut(cls, module_name: str) -> str:
        """# Format the top-level DUT instance for module name `module_name`."""
        raise NotImplementedError

    """ 
    Other Virtual Methods 
    """

    @property
    def enum(self):
        """Get our entry in the `NetlistFormat` enumeration"""
        raise NotImplementedError

    """ 
    Other Helper Methods
    """

    @staticmethod
    def fail(msg: str) -> None:
        """# Error Helper. Raise a `RuntimeError` with message `msg`.
        Primarily for tracking nested state upon failure."""
        # Note: also a great place for a debugger breakpoint.
        raise RuntimeError(msg)
