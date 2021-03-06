# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tech.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\ntech.proto\x12\nvlsir.tech"h\n\nTechnology\x12\x0c\n\x04name\x18\x01 \x01(\t\x12%\n\x08packages\x18\x0b \x03(\x0b\x32\x13.vlsir.tech.Package\x12%\n\x06layers\x18\x65 \x03(\x0b\x32\x15.vlsir.tech.LayerInfo"\x17\n\x07Package\x12\x0c\n\x04name\x18\x01 \x01(\t"O\n\x0cLayerPurpose\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0e\x32\x1c.vlsir.tech.LayerPurposeType"f\n\tLayerInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12)\n\x07purpose\x18\x0b \x01(\x0b\x32\x18.vlsir.tech.LayerPurpose\x12\r\n\x05index\x18\x15 \x01(\x04\x12\x11\n\tsub_index\x18\x1f \x01(\x04*^\n\x10LayerPurposeType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\t\n\x05LABEL\x10\x01\x12\x0b\n\x07\x44RAWING\x10\x02\x12\x07\n\x03PIN\x10\x03\x12\x0f\n\x0bOBSTRUCTION\x10\x04\x12\x0b\n\x07OUTLINE\x10\x05\x62\x06proto3'
)

_LAYERPURPOSETYPE = DESCRIPTOR.enum_types_by_name["LayerPurposeType"]
LayerPurposeType = enum_type_wrapper.EnumTypeWrapper(_LAYERPURPOSETYPE)
UNKNOWN = 0
LABEL = 1
DRAWING = 2
PIN = 3
OBSTRUCTION = 4
OUTLINE = 5


_TECHNOLOGY = DESCRIPTOR.message_types_by_name["Technology"]
_PACKAGE = DESCRIPTOR.message_types_by_name["Package"]
_LAYERPURPOSE = DESCRIPTOR.message_types_by_name["LayerPurpose"]
_LAYERINFO = DESCRIPTOR.message_types_by_name["LayerInfo"]
Technology = _reflection.GeneratedProtocolMessageType(
    "Technology",
    (_message.Message,),
    {
        "DESCRIPTOR": _TECHNOLOGY,
        "__module__": "tech_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.tech.Technology)
    },
)
_sym_db.RegisterMessage(Technology)

Package = _reflection.GeneratedProtocolMessageType(
    "Package",
    (_message.Message,),
    {
        "DESCRIPTOR": _PACKAGE,
        "__module__": "tech_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.tech.Package)
    },
)
_sym_db.RegisterMessage(Package)

LayerPurpose = _reflection.GeneratedProtocolMessageType(
    "LayerPurpose",
    (_message.Message,),
    {
        "DESCRIPTOR": _LAYERPURPOSE,
        "__module__": "tech_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.tech.LayerPurpose)
    },
)
_sym_db.RegisterMessage(LayerPurpose)

LayerInfo = _reflection.GeneratedProtocolMessageType(
    "LayerInfo",
    (_message.Message,),
    {
        "DESCRIPTOR": _LAYERINFO,
        "__module__": "tech_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.tech.LayerInfo)
    },
)
_sym_db.RegisterMessage(LayerInfo)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _LAYERPURPOSETYPE._serialized_start = 342
    _LAYERPURPOSETYPE._serialized_end = 436
    _TECHNOLOGY._serialized_start = 26
    _TECHNOLOGY._serialized_end = 130
    _PACKAGE._serialized_start = 132
    _PACKAGE._serialized_end = 155
    _LAYERPURPOSE._serialized_start = 157
    _LAYERPURPOSE._serialized_end = 236
    _LAYERINFO._serialized_start = 238
    _LAYERINFO._serialized_end = 340
# @@protoc_insertion_point(module_scope)
