/* eslint-disable */
import Long from "long";
import _m0 from "protobufjs/minimal";

/** Enumerated SI Prefixes */
export enum SIPrefix {
  /** YOCTO - E-24 */
  YOCTO = 0,
  /** ZEPTO - E-21 */
  ZEPTO = 1,
  /** ATTO - E-18 */
  ATTO = 2,
  /** FEMTO - E-15 */
  FEMTO = 3,
  /** PICO - E-12 */
  PICO = 4,
  /** NANO - E-9 */
  NANO = 5,
  /** MICRO - E-6 */
  MICRO = 6,
  /** MILLI - E-3 */
  MILLI = 7,
  /** CENTI - E-2 */
  CENTI = 8,
  /** DECI - E-1 */
  DECI = 9,
  /** DECA - E1 */
  DECA = 10,
  /** HECTO - E2 */
  HECTO = 11,
  /** KILO - E3 */
  KILO = 12,
  /** MEGA - E6 */
  MEGA = 13,
  /** GIGA - E9 */
  GIGA = 14,
  /** TERA - E12 */
  TERA = 15,
  /** PETA - E15 */
  PETA = 16,
  /** EXA - E18 */
  EXA = 17,
  /** ZETTA - E21 */
  ZETTA = 18,
  /** YOTTA - E24 */
  YOTTA = 19,
  /** UNIT - Added v2.0 */
  UNIT = 20,
  UNRECOGNIZED = -1,
}

export function sIPrefixFromJSON(object: any): SIPrefix {
  switch (object) {
    case 0:
    case "YOCTO":
      return SIPrefix.YOCTO;
    case 1:
    case "ZEPTO":
      return SIPrefix.ZEPTO;
    case 2:
    case "ATTO":
      return SIPrefix.ATTO;
    case 3:
    case "FEMTO":
      return SIPrefix.FEMTO;
    case 4:
    case "PICO":
      return SIPrefix.PICO;
    case 5:
    case "NANO":
      return SIPrefix.NANO;
    case 6:
    case "MICRO":
      return SIPrefix.MICRO;
    case 7:
    case "MILLI":
      return SIPrefix.MILLI;
    case 8:
    case "CENTI":
      return SIPrefix.CENTI;
    case 9:
    case "DECI":
      return SIPrefix.DECI;
    case 10:
    case "DECA":
      return SIPrefix.DECA;
    case 11:
    case "HECTO":
      return SIPrefix.HECTO;
    case 12:
    case "KILO":
      return SIPrefix.KILO;
    case 13:
    case "MEGA":
      return SIPrefix.MEGA;
    case 14:
    case "GIGA":
      return SIPrefix.GIGA;
    case 15:
    case "TERA":
      return SIPrefix.TERA;
    case 16:
    case "PETA":
      return SIPrefix.PETA;
    case 17:
    case "EXA":
      return SIPrefix.EXA;
    case 18:
    case "ZETTA":
      return SIPrefix.ZETTA;
    case 19:
    case "YOTTA":
      return SIPrefix.YOTTA;
    case 20:
    case "UNIT":
      return SIPrefix.UNIT;
    case -1:
    case "UNRECOGNIZED":
    default:
      return SIPrefix.UNRECOGNIZED;
  }
}

export function sIPrefixToJSON(object: SIPrefix): string {
  switch (object) {
    case SIPrefix.YOCTO:
      return "YOCTO";
    case SIPrefix.ZEPTO:
      return "ZEPTO";
    case SIPrefix.ATTO:
      return "ATTO";
    case SIPrefix.FEMTO:
      return "FEMTO";
    case SIPrefix.PICO:
      return "PICO";
    case SIPrefix.NANO:
      return "NANO";
    case SIPrefix.MICRO:
      return "MICRO";
    case SIPrefix.MILLI:
      return "MILLI";
    case SIPrefix.CENTI:
      return "CENTI";
    case SIPrefix.DECI:
      return "DECI";
    case SIPrefix.DECA:
      return "DECA";
    case SIPrefix.HECTO:
      return "HECTO";
    case SIPrefix.KILO:
      return "KILO";
    case SIPrefix.MEGA:
      return "MEGA";
    case SIPrefix.GIGA:
      return "GIGA";
    case SIPrefix.TERA:
      return "TERA";
    case SIPrefix.PETA:
      return "PETA";
    case SIPrefix.EXA:
      return "EXA";
    case SIPrefix.ZETTA:
      return "ZETTA";
    case SIPrefix.YOTTA:
      return "YOTTA";
    case SIPrefix.UNIT:
      return "UNIT";
    case SIPrefix.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/**
 * # Prefixed
 * A quantity annotated with an `SIPrefix`
 */
export interface Prefixed {
  /** The metric `SIPrefix` */
  prefix: SIPrefix;
  number?: { $case: "int64Value"; int64Value: number } | { $case: "doubleValue"; doubleValue: number } | {
    $case: "stringValue";
    stringValue: string;
  } | undefined;
}

/**
 * # Param-Value Enumeration
 *
 * Supports the common param-types supported in legacy HDLs
 * such as Verilog and SPICE.
 */
export interface ParamValue {
  value?:
    | { $case: "boolValue"; boolValue: boolean }
    | { $case: "int64Value"; int64Value: number }
    | { $case: "doubleValue"; doubleValue: number }
    | { $case: "stringValue"; stringValue: string }
    | { $case: "literal"; literal: string }
    | { $case: "prefixed"; prefixed: Prefixed }
    | undefined;
}

/**
 * # Param Declaration
 * Named parameter with a sometimes over-ride-able value.
 */
export interface Param {
  /** Param name */
  name: string;
  /** Value, or default */
  value:
    | ParamValue
    | undefined;
  /** Description */
  desc: string;
}

/**
 * # Domain-Qualified Name
 * Refers to an object outside its own namespace, at the global domain `domain`.
 */
export interface QualifiedName {
  domain: string;
  name: string;
}

/**
 * # Reference
 * Pointer to another Message, either defined in its own namespace (local) or
 * another (external).
 */
export interface Reference {
  to?: { $case: "local"; local: string } | { $case: "external"; external: QualifiedName } | undefined;
}

/**
 * # Library Metadata
 *
 * Summary information about any of several categories of `Library`, including:
 * * Library domain
 * * (String) cell names
 * * Author information
 */
export interface LibraryMetadata {
  /** Library Name / Domain */
  domain: string;
  /** Cell Names */
  cellNames: string[];
  /** Author Information */
  author: AuthorMetadata | undefined;
}

/**
 * # Authorship Metadata
 *
 * Summary information regarding authorship, ownership, and licensing
 * of any of several categories of design data.
 */
export interface AuthorMetadata {
  /** Author Name */
  author: string;
  /** Copyright Information */
  copyright: string;
  /** License Information, in SPDX Format */
  license: string;
}

function createBasePrefixed(): Prefixed {
  return { prefix: 0, number: undefined };
}

export const Prefixed = {
  encode(message: Prefixed, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.prefix !== 0) {
      writer.uint32(8).int32(message.prefix);
    }
    switch (message.number?.$case) {
      case "int64Value":
        writer.uint32(16).int64(message.number.int64Value);
        break;
      case "doubleValue":
        writer.uint32(25).double(message.number.doubleValue);
        break;
      case "stringValue":
        writer.uint32(34).string(message.number.stringValue);
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Prefixed {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePrefixed();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.prefix = reader.int32() as any;
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.number = { $case: "int64Value", int64Value: longToNumber(reader.int64() as Long) };
          continue;
        case 3:
          if (tag !== 25) {
            break;
          }

          message.number = { $case: "doubleValue", doubleValue: reader.double() };
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.number = { $case: "stringValue", stringValue: reader.string() };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Prefixed {
    return {
      prefix: isSet(object.prefix) ? sIPrefixFromJSON(object.prefix) : 0,
      number: isSet(object.int64Value)
        ? { $case: "int64Value", int64Value: globalThis.Number(object.int64Value) }
        : isSet(object.doubleValue)
        ? { $case: "doubleValue", doubleValue: globalThis.Number(object.doubleValue) }
        : isSet(object.stringValue)
        ? { $case: "stringValue", stringValue: globalThis.String(object.stringValue) }
        : undefined,
    };
  },

  toJSON(message: Prefixed): unknown {
    const obj: any = {};
    if (message.prefix !== 0) {
      obj.prefix = sIPrefixToJSON(message.prefix);
    }
    if (message.number?.$case === "int64Value") {
      obj.int64Value = Math.round(message.number.int64Value);
    }
    if (message.number?.$case === "doubleValue") {
      obj.doubleValue = message.number.doubleValue;
    }
    if (message.number?.$case === "stringValue") {
      obj.stringValue = message.number.stringValue;
    }
    return obj;
  },

  create(base?: DeepPartial<Prefixed>): Prefixed {
    return Prefixed.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Prefixed>): Prefixed {
    const message = createBasePrefixed();
    message.prefix = object.prefix ?? 0;
    if (
      object.number?.$case === "int64Value" &&
      object.number?.int64Value !== undefined &&
      object.number?.int64Value !== null
    ) {
      message.number = { $case: "int64Value", int64Value: object.number.int64Value };
    }
    if (
      object.number?.$case === "doubleValue" &&
      object.number?.doubleValue !== undefined &&
      object.number?.doubleValue !== null
    ) {
      message.number = { $case: "doubleValue", doubleValue: object.number.doubleValue };
    }
    if (
      object.number?.$case === "stringValue" &&
      object.number?.stringValue !== undefined &&
      object.number?.stringValue !== null
    ) {
      message.number = { $case: "stringValue", stringValue: object.number.stringValue };
    }
    return message;
  },
};

function createBaseParamValue(): ParamValue {
  return { value: undefined };
}

export const ParamValue = {
  encode(message: ParamValue, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    switch (message.value?.$case) {
      case "boolValue":
        writer.uint32(8).bool(message.value.boolValue);
        break;
      case "int64Value":
        writer.uint32(16).int64(message.value.int64Value);
        break;
      case "doubleValue":
        writer.uint32(25).double(message.value.doubleValue);
        break;
      case "stringValue":
        writer.uint32(34).string(message.value.stringValue);
        break;
      case "literal":
        writer.uint32(42).string(message.value.literal);
        break;
      case "prefixed":
        Prefixed.encode(message.value.prefixed, writer.uint32(50).fork()).ldelim();
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): ParamValue {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseParamValue();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.value = { $case: "boolValue", boolValue: reader.bool() };
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.value = { $case: "int64Value", int64Value: longToNumber(reader.int64() as Long) };
          continue;
        case 3:
          if (tag !== 25) {
            break;
          }

          message.value = { $case: "doubleValue", doubleValue: reader.double() };
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.value = { $case: "stringValue", stringValue: reader.string() };
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.value = { $case: "literal", literal: reader.string() };
          continue;
        case 6:
          if (tag !== 50) {
            break;
          }

          message.value = { $case: "prefixed", prefixed: Prefixed.decode(reader, reader.uint32()) };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): ParamValue {
    return {
      value: isSet(object.boolValue)
        ? { $case: "boolValue", boolValue: globalThis.Boolean(object.boolValue) }
        : isSet(object.int64Value)
        ? { $case: "int64Value", int64Value: globalThis.Number(object.int64Value) }
        : isSet(object.doubleValue)
        ? { $case: "doubleValue", doubleValue: globalThis.Number(object.doubleValue) }
        : isSet(object.stringValue)
        ? { $case: "stringValue", stringValue: globalThis.String(object.stringValue) }
        : isSet(object.literal)
        ? { $case: "literal", literal: globalThis.String(object.literal) }
        : isSet(object.prefixed)
        ? { $case: "prefixed", prefixed: Prefixed.fromJSON(object.prefixed) }
        : undefined,
    };
  },

  toJSON(message: ParamValue): unknown {
    const obj: any = {};
    if (message.value?.$case === "boolValue") {
      obj.boolValue = message.value.boolValue;
    }
    if (message.value?.$case === "int64Value") {
      obj.int64Value = Math.round(message.value.int64Value);
    }
    if (message.value?.$case === "doubleValue") {
      obj.doubleValue = message.value.doubleValue;
    }
    if (message.value?.$case === "stringValue") {
      obj.stringValue = message.value.stringValue;
    }
    if (message.value?.$case === "literal") {
      obj.literal = message.value.literal;
    }
    if (message.value?.$case === "prefixed") {
      obj.prefixed = Prefixed.toJSON(message.value.prefixed);
    }
    return obj;
  },

  create(base?: DeepPartial<ParamValue>): ParamValue {
    return ParamValue.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<ParamValue>): ParamValue {
    const message = createBaseParamValue();
    if (
      object.value?.$case === "boolValue" && object.value?.boolValue !== undefined && object.value?.boolValue !== null
    ) {
      message.value = { $case: "boolValue", boolValue: object.value.boolValue };
    }
    if (
      object.value?.$case === "int64Value" &&
      object.value?.int64Value !== undefined &&
      object.value?.int64Value !== null
    ) {
      message.value = { $case: "int64Value", int64Value: object.value.int64Value };
    }
    if (
      object.value?.$case === "doubleValue" &&
      object.value?.doubleValue !== undefined &&
      object.value?.doubleValue !== null
    ) {
      message.value = { $case: "doubleValue", doubleValue: object.value.doubleValue };
    }
    if (
      object.value?.$case === "stringValue" &&
      object.value?.stringValue !== undefined &&
      object.value?.stringValue !== null
    ) {
      message.value = { $case: "stringValue", stringValue: object.value.stringValue };
    }
    if (object.value?.$case === "literal" && object.value?.literal !== undefined && object.value?.literal !== null) {
      message.value = { $case: "literal", literal: object.value.literal };
    }
    if (object.value?.$case === "prefixed" && object.value?.prefixed !== undefined && object.value?.prefixed !== null) {
      message.value = { $case: "prefixed", prefixed: Prefixed.fromPartial(object.value.prefixed) };
    }
    return message;
  },
};

function createBaseParam(): Param {
  return { name: "", value: undefined, desc: "" };
}

export const Param = {
  encode(message: Param, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.value !== undefined) {
      ParamValue.encode(message.value, writer.uint32(18).fork()).ldelim();
    }
    if (message.desc !== "") {
      writer.uint32(26).string(message.desc);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Param {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseParam();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.name = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.value = ParamValue.decode(reader, reader.uint32());
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.desc = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Param {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      value: isSet(object.value) ? ParamValue.fromJSON(object.value) : undefined,
      desc: isSet(object.desc) ? globalThis.String(object.desc) : "",
    };
  },

  toJSON(message: Param): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.value !== undefined) {
      obj.value = ParamValue.toJSON(message.value);
    }
    if (message.desc !== "") {
      obj.desc = message.desc;
    }
    return obj;
  },

  create(base?: DeepPartial<Param>): Param {
    return Param.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Param>): Param {
    const message = createBaseParam();
    message.name = object.name ?? "";
    message.value = (object.value !== undefined && object.value !== null)
      ? ParamValue.fromPartial(object.value)
      : undefined;
    message.desc = object.desc ?? "";
    return message;
  },
};

function createBaseQualifiedName(): QualifiedName {
  return { domain: "", name: "" };
}

export const QualifiedName = {
  encode(message: QualifiedName, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.domain !== "") {
      writer.uint32(10).string(message.domain);
    }
    if (message.name !== "") {
      writer.uint32(18).string(message.name);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): QualifiedName {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseQualifiedName();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.domain = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.name = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): QualifiedName {
    return {
      domain: isSet(object.domain) ? globalThis.String(object.domain) : "",
      name: isSet(object.name) ? globalThis.String(object.name) : "",
    };
  },

  toJSON(message: QualifiedName): unknown {
    const obj: any = {};
    if (message.domain !== "") {
      obj.domain = message.domain;
    }
    if (message.name !== "") {
      obj.name = message.name;
    }
    return obj;
  },

  create(base?: DeepPartial<QualifiedName>): QualifiedName {
    return QualifiedName.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<QualifiedName>): QualifiedName {
    const message = createBaseQualifiedName();
    message.domain = object.domain ?? "";
    message.name = object.name ?? "";
    return message;
  },
};

function createBaseReference(): Reference {
  return { to: undefined };
}

export const Reference = {
  encode(message: Reference, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    switch (message.to?.$case) {
      case "local":
        writer.uint32(10).string(message.to.local);
        break;
      case "external":
        QualifiedName.encode(message.to.external, writer.uint32(18).fork()).ldelim();
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Reference {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseReference();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.to = { $case: "local", local: reader.string() };
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.to = { $case: "external", external: QualifiedName.decode(reader, reader.uint32()) };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Reference {
    return {
      to: isSet(object.local)
        ? { $case: "local", local: globalThis.String(object.local) }
        : isSet(object.external)
        ? { $case: "external", external: QualifiedName.fromJSON(object.external) }
        : undefined,
    };
  },

  toJSON(message: Reference): unknown {
    const obj: any = {};
    if (message.to?.$case === "local") {
      obj.local = message.to.local;
    }
    if (message.to?.$case === "external") {
      obj.external = QualifiedName.toJSON(message.to.external);
    }
    return obj;
  },

  create(base?: DeepPartial<Reference>): Reference {
    return Reference.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Reference>): Reference {
    const message = createBaseReference();
    if (object.to?.$case === "local" && object.to?.local !== undefined && object.to?.local !== null) {
      message.to = { $case: "local", local: object.to.local };
    }
    if (object.to?.$case === "external" && object.to?.external !== undefined && object.to?.external !== null) {
      message.to = { $case: "external", external: QualifiedName.fromPartial(object.to.external) };
    }
    return message;
  },
};

function createBaseLibraryMetadata(): LibraryMetadata {
  return { domain: "", cellNames: [], author: undefined };
}

export const LibraryMetadata = {
  encode(message: LibraryMetadata, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.domain !== "") {
      writer.uint32(10).string(message.domain);
    }
    for (const v of message.cellNames) {
      writer.uint32(82).string(v!);
    }
    if (message.author !== undefined) {
      AuthorMetadata.encode(message.author, writer.uint32(162).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): LibraryMetadata {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLibraryMetadata();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.domain = reader.string();
          continue;
        case 10:
          if (tag !== 82) {
            break;
          }

          message.cellNames.push(reader.string());
          continue;
        case 20:
          if (tag !== 162) {
            break;
          }

          message.author = AuthorMetadata.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): LibraryMetadata {
    return {
      domain: isSet(object.domain) ? globalThis.String(object.domain) : "",
      cellNames: globalThis.Array.isArray(object?.cellNames)
        ? object.cellNames.map((e: any) => globalThis.String(e))
        : [],
      author: isSet(object.author) ? AuthorMetadata.fromJSON(object.author) : undefined,
    };
  },

  toJSON(message: LibraryMetadata): unknown {
    const obj: any = {};
    if (message.domain !== "") {
      obj.domain = message.domain;
    }
    if (message.cellNames?.length) {
      obj.cellNames = message.cellNames;
    }
    if (message.author !== undefined) {
      obj.author = AuthorMetadata.toJSON(message.author);
    }
    return obj;
  },

  create(base?: DeepPartial<LibraryMetadata>): LibraryMetadata {
    return LibraryMetadata.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<LibraryMetadata>): LibraryMetadata {
    const message = createBaseLibraryMetadata();
    message.domain = object.domain ?? "";
    message.cellNames = object.cellNames?.map((e) => e) || [];
    message.author = (object.author !== undefined && object.author !== null)
      ? AuthorMetadata.fromPartial(object.author)
      : undefined;
    return message;
  },
};

function createBaseAuthorMetadata(): AuthorMetadata {
  return { author: "", copyright: "", license: "" };
}

export const AuthorMetadata = {
  encode(message: AuthorMetadata, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.author !== "") {
      writer.uint32(10).string(message.author);
    }
    if (message.copyright !== "") {
      writer.uint32(82).string(message.copyright);
    }
    if (message.license !== "") {
      writer.uint32(90).string(message.license);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): AuthorMetadata {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAuthorMetadata();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.author = reader.string();
          continue;
        case 10:
          if (tag !== 82) {
            break;
          }

          message.copyright = reader.string();
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.license = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): AuthorMetadata {
    return {
      author: isSet(object.author) ? globalThis.String(object.author) : "",
      copyright: isSet(object.copyright) ? globalThis.String(object.copyright) : "",
      license: isSet(object.license) ? globalThis.String(object.license) : "",
    };
  },

  toJSON(message: AuthorMetadata): unknown {
    const obj: any = {};
    if (message.author !== "") {
      obj.author = message.author;
    }
    if (message.copyright !== "") {
      obj.copyright = message.copyright;
    }
    if (message.license !== "") {
      obj.license = message.license;
    }
    return obj;
  },

  create(base?: DeepPartial<AuthorMetadata>): AuthorMetadata {
    return AuthorMetadata.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<AuthorMetadata>): AuthorMetadata {
    const message = createBaseAuthorMetadata();
    message.author = object.author ?? "";
    message.copyright = object.copyright ?? "";
    message.license = object.license ?? "";
    return message;
  },
};

type Builtin = Date | Function | Uint8Array | string | number | boolean | undefined;

type DeepPartial<T> = T extends Builtin ? T
  : T extends globalThis.Array<infer U> ? globalThis.Array<DeepPartial<U>>
  : T extends ReadonlyArray<infer U> ? ReadonlyArray<DeepPartial<U>>
  : T extends { $case: string } ? { [K in keyof Omit<T, "$case">]?: DeepPartial<T[K]> } & { $case: T["$case"] }
  : T extends {} ? { [K in keyof T]?: DeepPartial<T[K]> }
  : Partial<T>;

function longToNumber(long: Long): number {
  if (long.gt(globalThis.Number.MAX_SAFE_INTEGER)) {
    throw new globalThis.Error("Value is larger than Number.MAX_SAFE_INTEGER");
  }
  return long.toNumber();
}

if (_m0.util.Long !== Long) {
  _m0.util.Long = Long as any;
  _m0.configure();
}

function isSet(value: any): boolean {
  return value !== null && value !== undefined;
}
