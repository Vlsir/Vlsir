"""
# VLSIR Python Bindings 

Note while most modules in this package are protobuf-compiler generated, 
*this* top-level namespace module is not! 
"""

__version__ = "7.0.0" # VLSIR_VERSION

# Schema
from . import utils_pb2 as utils
from . import spice_pb2 as spice
from . import circuit_pb2 as circuit
from . import netlist_pb2 as netlist
from . import raw_pb2 as raw
from . import tetris_pb2 as tetris

# Add the utility-types to the top-level namespace
from .utils_pb2 import *

# But not the other stuff, as quite a few names conflict, e.g. `Library`, `Package`.
# from .spice_pb2 import *
# from .circuit_pb2 import *
# from .raw_pb2 import *
# from .tetris_pb2 import *
