# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: layout/raw.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import utils_pb2 as utils__pb2
import circuit_pb2 as circuit__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x10layout/raw.proto\x12\tvlsir.raw\x1a\x0butils.proto\x1a\rcircuit.proto"\x1d\n\x05Point\x12\t\n\x01x\x18\x01 \x01(\x03\x12\t\n\x01y\x18\x02 \x01(\x03"(\n\x05Layer\x12\x0e\n\x06number\x18\x01 \x01(\x03\x12\x0f\n\x07purpose\x18\x02 \x01(\x03"]\n\tRectangle\x12\x0b\n\x03net\x18\x01 \x01(\t\x12$\n\nlower_left\x18\x02 \x01(\x0b\x32\x10.vlsir.raw.Point\x12\r\n\x05width\x18\x03 \x01(\x03\x12\x0e\n\x06height\x18\x04 \x01(\x03":\n\x07Polygon\x12\x0b\n\x03net\x18\x01 \x01(\t\x12"\n\x08vertices\x18\x02 \x03(\x0b\x32\x10.vlsir.raw.Point"D\n\x04Path\x12\x0b\n\x03net\x18\x01 \x01(\t\x12 \n\x06points\x18\x02 \x03(\x0b\x32\x10.vlsir.raw.Point\x12\r\n\x05width\x18\x03 \x01(\x03"\x9e\x01\n\x0bLayerShapes\x12\x1f\n\x05layer\x18\x01 \x01(\x0b\x32\x10.vlsir.raw.Layer\x12(\n\nrectangles\x18\x02 \x03(\x0b\x32\x14.vlsir.raw.Rectangle\x12$\n\x08polygons\x18\x03 \x03(\x0b\x32\x12.vlsir.raw.Polygon\x12\x1e\n\x05paths\x18\x04 \x03(\x0b\x32\x0f.vlsir.raw.Path"<\n\x0bTextElement\x12\x0e\n\x06string\x18\x01 \x01(\t\x12\x1d\n\x03loc\x18\x02 \x01(\x0b\x32\x10.vlsir.raw.Point"\xa3\x01\n\x08Instance\x12\x0c\n\x04name\x18\x01 \x01(\t\x12$\n\x04\x63\x65ll\x18\x03 \x01(\x0b\x32\x16.vlsir.utils.Reference\x12)\n\x0forigin_location\x18\x04 \x01(\x0b\x32\x10.vlsir.raw.Point\x12\x14\n\x0creflect_vert\x18\x06 \x01(\x08\x12"\n\x1arotation_clockwise_degrees\x18\x07 \x01(\x05"\x93\x01\n\x06Layout\x12\x0c\n\x04name\x18\x01 \x01(\t\x12&\n\x06shapes\x18\x02 \x03(\x0b\x32\x16.vlsir.raw.LayerShapes\x12&\n\tinstances\x18\x03 \x03(\x0b\x32\x13.vlsir.raw.Instance\x12+\n\x0b\x61nnotations\x18\x04 \x03(\x0b\x32\x16.vlsir.raw.TextElement"\x90\x01\n\x08\x41\x62stract\x12\x0c\n\x04name\x18\x01 \x01(\t\x12#\n\x07outline\x18\x02 \x01(\x0b\x32\x12.vlsir.raw.Polygon\x12&\n\x05ports\x18\x04 \x03(\x0b\x32\x17.vlsir.raw.AbstractPort\x12)\n\tblockages\x18\x05 \x03(\x0b\x32\x16.vlsir.raw.LayerShapes"C\n\x0c\x41\x62stractPort\x12\x0b\n\x03net\x18\x01 \x01(\t\x12&\n\x06shapes\x18\x02 \x03(\x0b\x32\x16.vlsir.raw.LayerShapes"\xb2\x01\n\x04\x43\x65ll\x12\x0c\n\x04name\x18\x01 \x01(\t\x12+\n\tinterface\x18\n \x01(\x0b\x32\x18.vlsir.circuit.Interface\x12%\n\x06module\x18\x0b \x01(\x0b\x32\x15.vlsir.circuit.Module\x12%\n\x08\x61\x62stract\x18\x0c \x01(\x0b\x32\x13.vlsir.raw.Abstract\x12!\n\x06layout\x18\r \x01(\x0b\x32\x11.vlsir.raw.Layout"\x87\x01\n\x07Library\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12\x1f\n\x05units\x18\x02 \x01(\x0e\x32\x10.vlsir.raw.Units\x12\x1e\n\x05\x63\x65lls\x18\n \x03(\x0b\x32\x0f.vlsir.raw.Cell\x12+\n\x06\x61uthor\x18\x14 \x01(\x0b\x32\x1b.vlsir.utils.AuthorMetadata**\n\x05Units\x12\t\n\x05MICRO\x10\x00\x12\x08\n\x04NANO\x10\x01\x12\x0c\n\x08\x41NGSTROM\x10\x02\x62\x06proto3'
)

_UNITS = DESCRIPTOR.enum_types_by_name["Units"]
Units = enum_type_wrapper.EnumTypeWrapper(_UNITS)
MICRO = 0
NANO = 1
ANGSTROM = 2


_POINT = DESCRIPTOR.message_types_by_name["Point"]
_LAYER = DESCRIPTOR.message_types_by_name["Layer"]
_RECTANGLE = DESCRIPTOR.message_types_by_name["Rectangle"]
_POLYGON = DESCRIPTOR.message_types_by_name["Polygon"]
_PATH = DESCRIPTOR.message_types_by_name["Path"]
_LAYERSHAPES = DESCRIPTOR.message_types_by_name["LayerShapes"]
_TEXTELEMENT = DESCRIPTOR.message_types_by_name["TextElement"]
_INSTANCE = DESCRIPTOR.message_types_by_name["Instance"]
_LAYOUT = DESCRIPTOR.message_types_by_name["Layout"]
_ABSTRACT = DESCRIPTOR.message_types_by_name["Abstract"]
_ABSTRACTPORT = DESCRIPTOR.message_types_by_name["AbstractPort"]
_CELL = DESCRIPTOR.message_types_by_name["Cell"]
_LIBRARY = DESCRIPTOR.message_types_by_name["Library"]
Point = _reflection.GeneratedProtocolMessageType(
    "Point",
    (_message.Message,),
    {
        "DESCRIPTOR": _POINT,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.Point)
    },
)
_sym_db.RegisterMessage(Point)

Layer = _reflection.GeneratedProtocolMessageType(
    "Layer",
    (_message.Message,),
    {
        "DESCRIPTOR": _LAYER,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.Layer)
    },
)
_sym_db.RegisterMessage(Layer)

Rectangle = _reflection.GeneratedProtocolMessageType(
    "Rectangle",
    (_message.Message,),
    {
        "DESCRIPTOR": _RECTANGLE,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.Rectangle)
    },
)
_sym_db.RegisterMessage(Rectangle)

Polygon = _reflection.GeneratedProtocolMessageType(
    "Polygon",
    (_message.Message,),
    {
        "DESCRIPTOR": _POLYGON,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.Polygon)
    },
)
_sym_db.RegisterMessage(Polygon)

Path = _reflection.GeneratedProtocolMessageType(
    "Path",
    (_message.Message,),
    {
        "DESCRIPTOR": _PATH,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.Path)
    },
)
_sym_db.RegisterMessage(Path)

LayerShapes = _reflection.GeneratedProtocolMessageType(
    "LayerShapes",
    (_message.Message,),
    {
        "DESCRIPTOR": _LAYERSHAPES,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.LayerShapes)
    },
)
_sym_db.RegisterMessage(LayerShapes)

TextElement = _reflection.GeneratedProtocolMessageType(
    "TextElement",
    (_message.Message,),
    {
        "DESCRIPTOR": _TEXTELEMENT,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.TextElement)
    },
)
_sym_db.RegisterMessage(TextElement)

Instance = _reflection.GeneratedProtocolMessageType(
    "Instance",
    (_message.Message,),
    {
        "DESCRIPTOR": _INSTANCE,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.Instance)
    },
)
_sym_db.RegisterMessage(Instance)

Layout = _reflection.GeneratedProtocolMessageType(
    "Layout",
    (_message.Message,),
    {
        "DESCRIPTOR": _LAYOUT,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.Layout)
    },
)
_sym_db.RegisterMessage(Layout)

Abstract = _reflection.GeneratedProtocolMessageType(
    "Abstract",
    (_message.Message,),
    {
        "DESCRIPTOR": _ABSTRACT,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.Abstract)
    },
)
_sym_db.RegisterMessage(Abstract)

AbstractPort = _reflection.GeneratedProtocolMessageType(
    "AbstractPort",
    (_message.Message,),
    {
        "DESCRIPTOR": _ABSTRACTPORT,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.AbstractPort)
    },
)
_sym_db.RegisterMessage(AbstractPort)

Cell = _reflection.GeneratedProtocolMessageType(
    "Cell",
    (_message.Message,),
    {
        "DESCRIPTOR": _CELL,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.Cell)
    },
)
_sym_db.RegisterMessage(Cell)

Library = _reflection.GeneratedProtocolMessageType(
    "Library",
    (_message.Message,),
    {
        "DESCRIPTOR": _LIBRARY,
        "__module__": "layout.raw_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.raw.Library)
    },
)
_sym_db.RegisterMessage(Library)

if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _UNITS._serialized_start = 1431
    _UNITS._serialized_end = 1473
    _POINT._serialized_start = 59
    _POINT._serialized_end = 88
    _LAYER._serialized_start = 90
    _LAYER._serialized_end = 130
    _RECTANGLE._serialized_start = 132
    _RECTANGLE._serialized_end = 225
    _POLYGON._serialized_start = 227
    _POLYGON._serialized_end = 285
    _PATH._serialized_start = 287
    _PATH._serialized_end = 355
    _LAYERSHAPES._serialized_start = 358
    _LAYERSHAPES._serialized_end = 516
    _TEXTELEMENT._serialized_start = 518
    _TEXTELEMENT._serialized_end = 578
    _INSTANCE._serialized_start = 581
    _INSTANCE._serialized_end = 744
    _LAYOUT._serialized_start = 747
    _LAYOUT._serialized_end = 894
    _ABSTRACT._serialized_start = 897
    _ABSTRACT._serialized_end = 1041
    _ABSTRACTPORT._serialized_start = 1043
    _ABSTRACTPORT._serialized_end = 1110
    _CELL._serialized_start = 1113
    _CELL._serialized_end = 1291
    _LIBRARY._serialized_start = 1294
    _LIBRARY._serialized_end = 1429
# @@protoc_insertion_point(module_scope)
