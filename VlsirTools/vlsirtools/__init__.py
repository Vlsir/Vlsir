"""
# Vlsir Tools
"""

__version__ = "2.0.dev0"

# Python module namespaces
from . import spice
from . import spicetype
from .spicetype import SpiceType

# Primitive Definitions
from . import primitives  # The python module

# Note `vlsirtools.netlist` becomes a *function* here, where there is also a *module* by that name. Maybe not ideal.
from .netlist import netlist

# Pull the `spice/{simulator}` namespaces into the `vlsirtools` namespace as well
# FIXME: probably integrate netlisting into these at some point
from .spice import xyce
from .spice import spectre
from .spice import ngspice
