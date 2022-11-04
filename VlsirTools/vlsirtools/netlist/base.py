"""
# Netlister Base Class 

"""

# Std-Lib Imports
from typing import Optional, Union, IO, Dict, Iterable
from enum import Enum
from dataclasses import dataclass, field

# Local Imports
import vlsir


# Internal type shorthand
ModuleLike = Union[vlsir.circuit.Module, vlsir.circuit.ExternalModule]


class SpicePrefix(Enum):
    """Enumerated Spice Primitives and their Instance-Name Prefixes"""

    # Sub-circits, either from `Module`s or `ExternalModule`s
    SUBCKT = "x"
    # Ideal Passives
    RESISTOR = "r"
    CAPACITOR = "c"
    INDUCTOR = "l"
    # Semiconductor Devices
    MOS = "m"
    DIODE = "d"
    BIPOLAR = "q"
    # Independent Sources
    VSOURCE = "v"
    ISOURCE = "i"
    # Dependent Sources
    VCVS = "e"
    VCCS = "g"
    CCCS = "f"
    CCVS = "h"
    # Transmission Lines
    TLINE = "o"


@dataclass
class ResolvedModule:
    """Resolved reference to a `Module` or `ExternalModule`.
    Includes its spice-language prefix, and if user-defined its netlist-sanitized module-name."""

    module: ModuleLike
    module_name: str
    spice_prefix: SpicePrefix


@dataclass
class ResolvedParams:
    """Resolved Instance-Parameter Values
    Factoring in defaults, and converted to strings.
    Largely a wrapper for `Dict[str, str]`, with accessors `get` and `pop` that raise `RuntimeError` if a key is missing."""

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

    def __init__(self, pkg: vlsir.circuit.Package, dest: IO):
        self.pkg = pkg
        self.dest = dest
        self.indent = Indent(chars="  ")

        self.module_names = set()  # Netlisted Module names
        self.pmodules = dict()  # Visited proto-Modules

        # FIXME: are we really using both of these?
        self.ext_modules = dict()  # Visited ExternalModules
        # Visited ExternalModule names, checked for duplicates
        self.ext_module_names = dict()

        # Attributes of the currently-netlisted Module

        # Signals in the currently-visited module, keyed by name
        # Includes *all* ports and internal signals
        self.signals_by_name: Dict[str, vlsir.circuit.Signal] = dict()
        # Internal signals, keyed by name, *excluding* ports
        self.internal_signals_by_name: Dict[str, vlsir.circuit.Signal] = dict()
        # Names of all ports, for membership testing
        self.port_names = set()  # : Set[str]

    def netlist(self) -> None:
        """Primary API Method.
        Convert everything in `self.pkg` and write to `self.dest`."""

        # First visit any externally-defined Modules,
        # Ensuring we have their port-orders.
        for emod in self.pkg.ext_modules:
            self.get_external_module(emod)

        # Add some header commentary
        self.write_header()

        # Now do the real stuff,
        # Creating netlist entries for each package-defined Module
        for mod in self.pkg.modules:
            self.write_module_definition(mod)
        # And ensure all output makes it to `self.dest`
        self.dest.flush()

    def write(self, s: str) -> None:
        """Helper/wrapper, passing to `self.dest`"""
        self.dest.write(s)

    def writeln(self, s: str) -> None:
        """Write `s` as a line, at our current `indent` level."""
        self.write(f"{self.indent.state}{s}\n")

    def get_external_module(self, emod: vlsir.circuit.ExternalModule) -> None:
        """Visit an ExternalModule definition.
        "Netlisting" these doesn't actually write anything,
        but just stores a reference  in internal dictionary `ext_modules`
        for future references to them."""
        key = (emod.name.domain, emod.name.name)
        if key in self.ext_modules:
            raise RuntimeError(f"Invalid doubly-defined external module {emod}")
        self.ext_modules[key] = emod

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

    @classmethod
    def get_instance_params(
        cls, pinst: vlsir.circuit.Instance, pmodule: ModuleLike
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
        for (pname, pval) in instance_parameters.items():
            values[pname] = cls.get_param_value(pval)

        # And wrap the resolved values in a `ResolvedParams` object
        return ResolvedParams(values)

    @classmethod
    def get_module_name(cls, module: vlsir.circuit.Module) -> str:
        """Create a netlist-compatible name for proto-Module `module`"""

        # Create the module name
        # Replace all format-invalid characters with underscores
        name = module.name.split(".")[-1]
        for ch in name:
            if not (ch.isalpha() or ch.isdigit() or ch == "_"):
                name = name.replace(ch, "_")
        return name

    def resolve_reference(self, ref: vlsir.utils.Reference) -> ResolvedModule:
        """Resolve the `ModuleLike` referent of `ref`."""

        if ref.WhichOneof("to") == "local":  # Internally-defined Module
            module = self.pmodules.get(ref.local, None)
            if module is None:
                raise RuntimeError(f"Invalid undefined Module {ref.local} ")
            return ResolvedModule(
                module=module,
                module_name=self.get_module_name(module),
                spice_prefix=SpicePrefix.SUBCKT,
            )

        if ref.WhichOneof("to") == "external":  # Defined outside package

            # First check the priviledged/ internally-defined domains
            if ref.external.domain == "vlsir.primitives":
                # Built-in primitive. Load its definition from the `vlsir.primitives` (python) module.
                name = ref.external.name
                module = vlsir.primitives.dct.get(ref.external.name, None)
                if module is None:
                    raise RuntimeError(f"Invalid undefined primitive {ref.external}")

                # Mapping from primitive-name to spice-prefix
                prefixes = dict(
                    resistor=SpicePrefix.RESISTOR,
                    capacitor=SpicePrefix.CAPACITOR,
                    inductor=SpicePrefix.INDUCTOR,
                    vdc=SpicePrefix.VSOURCE,
                    vpulse=SpicePrefix.VSOURCE,
                    vpwl=SpicePrefix.VSOURCE,
                    vsin=SpicePrefix.VSOURCE,
                    isource=SpicePrefix.ISOURCE,
                    vcvs=SpicePrefix.VCVS,
                    vccs=SpicePrefix.VCCS,
                    cccs=SpicePrefix.CCCS,
                    ccvs=SpicePrefix.CCVS,
                    mos=SpicePrefix.MOS,
                    bipolar=SpicePrefix.BIPOLAR,
                    diode=SpicePrefix.DIODE,
                )

                if name not in prefixes:
                    raise ValueError(f"Unsupported or Invalid Ideal Primitive {ref}")

                return ResolvedModule(
                    module=module,
                    module_name=module.name.name,
                    spice_prefix=prefixes[name],
                )

            if ref.external.domain == "hdl21.primitives":
                msg = f"Invalid direct-netlisting of physical `hdl21.Primitive` `{ref.external.name}`. "
                msg += "Either compile to a target technology, or replace with an `ExternalModule`. "
                raise RuntimeError(msg)

            else:  # Externally-Defined, External-Domain `ExternalModule`
                key = (ref.external.domain, ref.external.name)
                module = self.ext_modules.get(key, None)
                if module is None:
                    msg = f"Invalid Instance of undefined External Module {key}"
                    raise RuntimeError(msg)
                # Check for duplicate names which would conflict from other namespaces
                module_name = ref.external.name
                if (
                    module_name in self.ext_module_names
                    and self.ext_module_names[module_name] is not module
                ):
                    msg = f"Conflicting ExternalModule definitions {module} and {self.ext_module_names[module_name]}"
                    raise RuntimeError(msg)
                self.ext_module_names[module_name] = module
                return ResolvedModule(
                    module=module,
                    module_name=module_name,
                    spice_prefix=SpicePrefix.SUBCKT,
                )

        # Not a Module, not an ExternalModule, not sure what it is
        raise ValueError(f"Invalid Module reference {ref}")

    def format_connection_target(self, ptarget: vlsir.circuit.ConnectionTarget) -> str:
        """Format a `ConnectionTarget` reference.
        Does not *declare* any new connection objects, but generates references to existing ones."""
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

    def write_header(self) -> None:
        """Write header commentary
        This proves particularly important for many Spice-like formats,
        which *always* interpret the first line of an input-file as a comment (among many other dumb things).
        So, always write one there right off the bat."""

        if self.pkg.domain:
            self.write_comment(f"circuit.Package {self.pkg.domain}")
        else:
            self.write_comment(f"Anonymous circuit.Package")
        self.write_comment(f"Written by {self.__class__.__name__}")
        self.write_comment("")
        self.writeln("")

    def get_signal(self, name: str) -> vlsir.circuit.Signal:
        """Get Signal `name` from the current Module's mapping.
        Raises a `RuntimeError` if the Signal is not found."""

        sig = self.signals_by_name.get(name, None)
        if sig is None:
            msg = f"Unknown signal: {name} in {self.signals_by_name.keys()}"
            raise RuntimeError(msg)
        return sig

    def collect_signals_by_name(self, module: vlsir.circuit.Module):
        """Collect a `Module`'s worth of signals into a dictionary keyed by name.
        This often proves important for references to internal Signals, e.g. in Ports and Slices."""

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

    """ 
    Virtual `format` Methods 
    """

    @classmethod
    def format_param_decl(cls, param: vlsir.Param) -> str:
        """Format a named `Parameter` definition"""
        raise NotImplementedError

    @classmethod
    def format_port_decl(cls, pport: vlsir.circuit.Port) -> str:
        """Format a declaration of a `Port`"""
        raise NotImplementedError

    @classmethod
    def format_port_ref(cls, pport: vlsir.circuit.Port) -> str:
        """Format a reference to a `Port`"""
        raise NotImplementedError

    @classmethod
    def format_signal_decl(cls, psig: vlsir.circuit.Signal) -> str:
        """Format a declaration of Signal `psig`"""
        raise NotImplementedError

    @classmethod
    def format_signal_ref(cls, psig: vlsir.circuit.Signal) -> str:
        """Format a reference to Signal `psig`"""
        raise NotImplementedError

    @classmethod
    def format_signal_slice(cls, pslice: vlsir.circuit.Slice) -> str:
        """Format Signal-Slice `pslice`"""
        raise NotImplementedError

    def format_concat(self, pconc: vlsir.circuit.Concat) -> str:
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

    """ 
    Virtual `write` Methods 
    """

    def write_comment(self, comment: str) -> None:
        """Format and string a string comment.
        "Line comments" are the sole supported variety, which fit within a line, and extend to the end of that line.
        The `write_comment` method assumes responsibility for closing the line."""
        raise NotImplementedError

    def write_module_definition(self, pmodule: vlsir.circuit.Module) -> None:
        """Write Module `module`"""
        raise NotImplementedError

    def write_param_declarations(self, module: vlsir.circuit.Module) -> None:
        """Write all parameter declarations for `module`"""
        raise NotImplementedError

    def write_instance(self, pinst: vlsir.circuit.Instance) -> str:
        """Write Instance `pinst`"""
        raise NotImplementedError

    def write_instance_params(self, pvals: ResolvedParams) -> None:
        """Write Instance parameters `pvals`"""
        raise NotImplementedError

    """ 
    Other Virtual Methods 
    """

    @property
    def enum(self):
        """Get our entry in the `NetlistFormat` enumeration"""
        raise NotImplementedError
