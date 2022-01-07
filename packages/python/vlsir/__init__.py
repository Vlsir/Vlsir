"""
VLSIR Python Bindings 
"""

# This is `__init__.py` is the sole non-compiled python-file in `vlsir`.
# It exists to re-name `protoc`'s ugly "pb2" names,
# and generally ensure other tools regard `vlsir` as a package.

from . import utils_pb2 as utils

from . import spice_pb2 as spice
from . import circuit_pb2 as circuit
from . import raw_pb2 as raw
from . import tetris_pb2 as tetris
