# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: circuit.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import utils_pb2 as utils__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="circuit.proto",
    package="vlsir.circuit",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\rcircuit.proto\x12\rvlsir.circuit\x1a\x0butils.proto"\x83\x01\n\x07Package\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12&\n\x07modules\x18\x02 \x03(\x0b\x32\x15.vlsir.circuit.Module\x12\x32\n\x0b\x65xt_modules\x18\x03 \x03(\x0b\x32\x1d.vlsir.circuit.ExternalModule\x12\x0c\n\x04\x64\x65sc\x18\n \x01(\t"\x81\x01\n\x04Port\x12\x0e\n\x06signal\x18\x01 \x01(\t\x12\x30\n\tdirection\x18\x02 \x01(\x0e\x32\x1d.vlsir.circuit.Port.Direction"7\n\tDirection\x12\t\n\x05INPUT\x10\x00\x12\n\n\x06OUTPUT\x10\x01\x12\t\n\x05INOUT\x10\x02\x12\x08\n\x04NONE\x10\x03"%\n\x06Signal\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05width\x18\x02 \x01(\x03"1\n\x05Slice\x12\x0e\n\x06signal\x18\x01 \x01(\t\x12\x0b\n\x03top\x18\x02 \x01(\x03\x12\x0b\n\x03\x62ot\x18\x03 \x01(\x03"8\n\x06\x43oncat\x12.\n\x05parts\x18\x01 \x03(\x0b\x32\x1f.vlsir.circuit.ConnectionTarget"z\n\x10\x43onnectionTarget\x12\r\n\x03sig\x18\x01 \x01(\tH\x00\x12%\n\x05slice\x18\x02 \x01(\x0b\x32\x14.vlsir.circuit.SliceH\x00\x12\'\n\x06\x63oncat\x18\x03 \x01(\x0b\x32\x15.vlsir.circuit.ConcatH\x00\x42\x07\n\x05stype"O\n\nConnection\x12\x10\n\x08portname\x18\x01 \x01(\t\x12/\n\x06target\x18\x02 \x01(\x0b\x32\x1f.vlsir.circuit.ConnectionTarget"\x98\x01\n\x08Instance\x12\x0c\n\x04name\x18\x01 \x01(\t\x12&\n\x06module\x18\x02 \x01(\x0b\x32\x16.vlsir.utils.Reference\x12&\n\nparameters\x18\x03 \x03(\x0b\x32\x12.vlsir.utils.Param\x12.\n\x0b\x63onnections\x18\x04 \x03(\x0b\x32\x19.vlsir.circuit.Connection"\xb6\x01\n\x06Module\x12\x0c\n\x04name\x18\x01 \x01(\t\x12"\n\x05ports\x18\x02 \x03(\x0b\x32\x13.vlsir.circuit.Port\x12&\n\x07signals\x18\x03 \x03(\x0b\x32\x15.vlsir.circuit.Signal\x12*\n\tinstances\x18\x04 \x03(\x0b\x32\x17.vlsir.circuit.Instance\x12&\n\nparameters\x18\x05 \x03(\x0b\x32\x12.vlsir.utils.Param"\xe9\x01\n\x0e\x45xternalModule\x12(\n\x04name\x18\x01 \x01(\x0b\x32\x1a.vlsir.utils.QualifiedName\x12\x0c\n\x04\x64\x65sc\x18\x02 \x01(\t\x12"\n\x05ports\x18\x03 \x03(\x0b\x32\x13.vlsir.circuit.Port\x12&\n\x07signals\x18\x04 \x03(\x0b\x32\x15.vlsir.circuit.Signal\x12&\n\nparameters\x18\x05 \x03(\x0b\x32\x12.vlsir.utils.Param\x12+\n\tspicetype\x18\x06 \x01(\x0e\x32\x18.vlsir.circuit.SpiceType"=\n\tInterface\x12\x0c\n\x04name\x18\x01 \x01(\t\x12"\n\x05ports\x18\n \x03(\x0b\x32\x13.vlsir.circuit.Port*\xb0\x01\n\tSpiceType\x12\n\n\x06SUBCKT\x10\x00\x12\x0c\n\x08RESISTOR\x10\x01\x12\r\n\tCAPACITOR\x10\x02\x12\x0c\n\x08INDUCTOR\x10\x03\x12\x07\n\x03MOS\x10\x04\x12\t\n\x05\x44IODE\x10\x05\x12\x0b\n\x07\x42IPOLAR\x10\x06\x12\x0b\n\x07VSOURCE\x10\x07\x12\x0b\n\x07ISOURCE\x10\x08\x12\x08\n\x04VCVS\x10\t\x12\x08\n\x04VCCS\x10\n\x12\x08\n\x04\x43\x43\x43S\x10\x0b\x12\x08\n\x04\x43\x43VS\x10\x0c\x12\t\n\x05TLINE\x10\rb\x06proto3'
    ),
    dependencies=[
        utils__pb2.DESCRIPTOR,
    ],
)

_SPICETYPE = _descriptor.EnumDescriptor(
    name="SpiceType",
    full_name="vlsir.circuit.SpiceType",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="SUBCKT", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="RESISTOR", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="CAPACITOR", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="INDUCTOR", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="MOS", index=4, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="DIODE", index=5, number=5, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="BIPOLAR", index=6, number=6, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="VSOURCE", index=7, number=7, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ISOURCE", index=8, number=8, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="VCVS", index=9, number=9, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="VCCS", index=10, number=10, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="CCCS", index=11, number=11, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="CCVS", index=12, number=12, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="TLINE", index=13, number=13, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1304,
    serialized_end=1480,
)
_sym_db.RegisterEnumDescriptor(_SPICETYPE)

SpiceType = enum_type_wrapper.EnumTypeWrapper(_SPICETYPE)
SUBCKT = 0
RESISTOR = 1
CAPACITOR = 2
INDUCTOR = 3
MOS = 4
DIODE = 5
BIPOLAR = 6
VSOURCE = 7
ISOURCE = 8
VCVS = 9
VCCS = 10
CCCS = 11
CCVS = 12
TLINE = 13


_PORT_DIRECTION = _descriptor.EnumDescriptor(
    name="Direction",
    full_name="vlsir.circuit.Port.Direction",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="INPUT", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="OUTPUT", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="INOUT", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="NONE", index=3, number=3, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=254,
    serialized_end=309,
)
_sym_db.RegisterEnumDescriptor(_PORT_DIRECTION)


_PACKAGE = _descriptor.Descriptor(
    name="Package",
    full_name="vlsir.circuit.Package",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="domain",
            full_name="vlsir.circuit.Package.domain",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="modules",
            full_name="vlsir.circuit.Package.modules",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="ext_modules",
            full_name="vlsir.circuit.Package.ext_modules",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="desc",
            full_name="vlsir.circuit.Package.desc",
            index=3,
            number=10,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=46,
    serialized_end=177,
)


_PORT = _descriptor.Descriptor(
    name="Port",
    full_name="vlsir.circuit.Port",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="signal",
            full_name="vlsir.circuit.Port.signal",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="direction",
            full_name="vlsir.circuit.Port.direction",
            index=1,
            number=2,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[
        _PORT_DIRECTION,
    ],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=180,
    serialized_end=309,
)


_SIGNAL = _descriptor.Descriptor(
    name="Signal",
    full_name="vlsir.circuit.Signal",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="vlsir.circuit.Signal.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="width",
            full_name="vlsir.circuit.Signal.width",
            index=1,
            number=2,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=311,
    serialized_end=348,
)


_SLICE = _descriptor.Descriptor(
    name="Slice",
    full_name="vlsir.circuit.Slice",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="signal",
            full_name="vlsir.circuit.Slice.signal",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="top",
            full_name="vlsir.circuit.Slice.top",
            index=1,
            number=2,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="bot",
            full_name="vlsir.circuit.Slice.bot",
            index=2,
            number=3,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=350,
    serialized_end=399,
)


_CONCAT = _descriptor.Descriptor(
    name="Concat",
    full_name="vlsir.circuit.Concat",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="parts",
            full_name="vlsir.circuit.Concat.parts",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=401,
    serialized_end=457,
)


_CONNECTIONTARGET = _descriptor.Descriptor(
    name="ConnectionTarget",
    full_name="vlsir.circuit.ConnectionTarget",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="sig",
            full_name="vlsir.circuit.ConnectionTarget.sig",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="slice",
            full_name="vlsir.circuit.ConnectionTarget.slice",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="concat",
            full_name="vlsir.circuit.ConnectionTarget.concat",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="stype",
            full_name="vlsir.circuit.ConnectionTarget.stype",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=459,
    serialized_end=581,
)


_CONNECTION = _descriptor.Descriptor(
    name="Connection",
    full_name="vlsir.circuit.Connection",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="portname",
            full_name="vlsir.circuit.Connection.portname",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="target",
            full_name="vlsir.circuit.Connection.target",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=583,
    serialized_end=662,
)


_INSTANCE = _descriptor.Descriptor(
    name="Instance",
    full_name="vlsir.circuit.Instance",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="vlsir.circuit.Instance.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="module",
            full_name="vlsir.circuit.Instance.module",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="parameters",
            full_name="vlsir.circuit.Instance.parameters",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="connections",
            full_name="vlsir.circuit.Instance.connections",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=665,
    serialized_end=817,
)


_MODULE = _descriptor.Descriptor(
    name="Module",
    full_name="vlsir.circuit.Module",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="vlsir.circuit.Module.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="ports",
            full_name="vlsir.circuit.Module.ports",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="signals",
            full_name="vlsir.circuit.Module.signals",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="instances",
            full_name="vlsir.circuit.Module.instances",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="parameters",
            full_name="vlsir.circuit.Module.parameters",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=820,
    serialized_end=1002,
)


_EXTERNALMODULE = _descriptor.Descriptor(
    name="ExternalModule",
    full_name="vlsir.circuit.ExternalModule",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="vlsir.circuit.ExternalModule.name",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="desc",
            full_name="vlsir.circuit.ExternalModule.desc",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="ports",
            full_name="vlsir.circuit.ExternalModule.ports",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="signals",
            full_name="vlsir.circuit.ExternalModule.signals",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="parameters",
            full_name="vlsir.circuit.ExternalModule.parameters",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="spicetype",
            full_name="vlsir.circuit.ExternalModule.spicetype",
            index=5,
            number=6,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1005,
    serialized_end=1238,
)


_INTERFACE = _descriptor.Descriptor(
    name="Interface",
    full_name="vlsir.circuit.Interface",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="vlsir.circuit.Interface.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="ports",
            full_name="vlsir.circuit.Interface.ports",
            index=1,
            number=10,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1240,
    serialized_end=1301,
)

_PACKAGE.fields_by_name["modules"].message_type = _MODULE
_PACKAGE.fields_by_name["ext_modules"].message_type = _EXTERNALMODULE
_PORT.fields_by_name["direction"].enum_type = _PORT_DIRECTION
_PORT_DIRECTION.containing_type = _PORT
_CONCAT.fields_by_name["parts"].message_type = _CONNECTIONTARGET
_CONNECTIONTARGET.fields_by_name["slice"].message_type = _SLICE
_CONNECTIONTARGET.fields_by_name["concat"].message_type = _CONCAT
_CONNECTIONTARGET.oneofs_by_name["stype"].fields.append(
    _CONNECTIONTARGET.fields_by_name["sig"]
)
_CONNECTIONTARGET.fields_by_name[
    "sig"
].containing_oneof = _CONNECTIONTARGET.oneofs_by_name["stype"]
_CONNECTIONTARGET.oneofs_by_name["stype"].fields.append(
    _CONNECTIONTARGET.fields_by_name["slice"]
)
_CONNECTIONTARGET.fields_by_name[
    "slice"
].containing_oneof = _CONNECTIONTARGET.oneofs_by_name["stype"]
_CONNECTIONTARGET.oneofs_by_name["stype"].fields.append(
    _CONNECTIONTARGET.fields_by_name["concat"]
)
_CONNECTIONTARGET.fields_by_name[
    "concat"
].containing_oneof = _CONNECTIONTARGET.oneofs_by_name["stype"]
_CONNECTION.fields_by_name["target"].message_type = _CONNECTIONTARGET
_INSTANCE.fields_by_name["module"].message_type = utils__pb2._REFERENCE
_INSTANCE.fields_by_name["parameters"].message_type = utils__pb2._PARAM
_INSTANCE.fields_by_name["connections"].message_type = _CONNECTION
_MODULE.fields_by_name["ports"].message_type = _PORT
_MODULE.fields_by_name["signals"].message_type = _SIGNAL
_MODULE.fields_by_name["instances"].message_type = _INSTANCE
_MODULE.fields_by_name["parameters"].message_type = utils__pb2._PARAM
_EXTERNALMODULE.fields_by_name["name"].message_type = utils__pb2._QUALIFIEDNAME
_EXTERNALMODULE.fields_by_name["ports"].message_type = _PORT
_EXTERNALMODULE.fields_by_name["signals"].message_type = _SIGNAL
_EXTERNALMODULE.fields_by_name["parameters"].message_type = utils__pb2._PARAM
_EXTERNALMODULE.fields_by_name["spicetype"].enum_type = _SPICETYPE
_INTERFACE.fields_by_name["ports"].message_type = _PORT
DESCRIPTOR.message_types_by_name["Package"] = _PACKAGE
DESCRIPTOR.message_types_by_name["Port"] = _PORT
DESCRIPTOR.message_types_by_name["Signal"] = _SIGNAL
DESCRIPTOR.message_types_by_name["Slice"] = _SLICE
DESCRIPTOR.message_types_by_name["Concat"] = _CONCAT
DESCRIPTOR.message_types_by_name["ConnectionTarget"] = _CONNECTIONTARGET
DESCRIPTOR.message_types_by_name["Connection"] = _CONNECTION
DESCRIPTOR.message_types_by_name["Instance"] = _INSTANCE
DESCRIPTOR.message_types_by_name["Module"] = _MODULE
DESCRIPTOR.message_types_by_name["ExternalModule"] = _EXTERNALMODULE
DESCRIPTOR.message_types_by_name["Interface"] = _INTERFACE
DESCRIPTOR.enum_types_by_name["SpiceType"] = _SPICETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Package = _reflection.GeneratedProtocolMessageType(
    "Package",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PACKAGE,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.Package)
    ),
)
_sym_db.RegisterMessage(Package)

Port = _reflection.GeneratedProtocolMessageType(
    "Port",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PORT,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.Port)
    ),
)
_sym_db.RegisterMessage(Port)

Signal = _reflection.GeneratedProtocolMessageType(
    "Signal",
    (_message.Message,),
    dict(
        DESCRIPTOR=_SIGNAL,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.Signal)
    ),
)
_sym_db.RegisterMessage(Signal)

Slice = _reflection.GeneratedProtocolMessageType(
    "Slice",
    (_message.Message,),
    dict(
        DESCRIPTOR=_SLICE,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.Slice)
    ),
)
_sym_db.RegisterMessage(Slice)

Concat = _reflection.GeneratedProtocolMessageType(
    "Concat",
    (_message.Message,),
    dict(
        DESCRIPTOR=_CONCAT,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.Concat)
    ),
)
_sym_db.RegisterMessage(Concat)

ConnectionTarget = _reflection.GeneratedProtocolMessageType(
    "ConnectionTarget",
    (_message.Message,),
    dict(
        DESCRIPTOR=_CONNECTIONTARGET,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.ConnectionTarget)
    ),
)
_sym_db.RegisterMessage(ConnectionTarget)

Connection = _reflection.GeneratedProtocolMessageType(
    "Connection",
    (_message.Message,),
    dict(
        DESCRIPTOR=_CONNECTION,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.Connection)
    ),
)
_sym_db.RegisterMessage(Connection)

Instance = _reflection.GeneratedProtocolMessageType(
    "Instance",
    (_message.Message,),
    dict(
        DESCRIPTOR=_INSTANCE,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.Instance)
    ),
)
_sym_db.RegisterMessage(Instance)

Module = _reflection.GeneratedProtocolMessageType(
    "Module",
    (_message.Message,),
    dict(
        DESCRIPTOR=_MODULE,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.Module)
    ),
)
_sym_db.RegisterMessage(Module)

ExternalModule = _reflection.GeneratedProtocolMessageType(
    "ExternalModule",
    (_message.Message,),
    dict(
        DESCRIPTOR=_EXTERNALMODULE,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.ExternalModule)
    ),
)
_sym_db.RegisterMessage(ExternalModule)

Interface = _reflection.GeneratedProtocolMessageType(
    "Interface",
    (_message.Message,),
    dict(
        DESCRIPTOR=_INTERFACE,
        __module__="circuit_pb2"
        # @@protoc_insertion_point(class_scope:vlsir.circuit.Interface)
    ),
)
_sym_db.RegisterMessage(Interface)


# @@protoc_insertion_point(module_scope)
