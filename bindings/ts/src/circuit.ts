/* eslint-disable */
import Long from "long";
import _m0 from "protobufjs/minimal";
import { Param, QualifiedName, Reference } from "./utils";

/** Spice Type, used to identify what a component is in spice */
export enum SpiceType {
  /** SUBCKT - The default value is implicitly SUBCKT */
  SUBCKT = 0,
  RESISTOR = 1,
  CAPACITOR = 2,
  INDUCTOR = 3,
  MOS = 4,
  DIODE = 5,
  BIPOLAR = 6,
  VSOURCE = 7,
  ISOURCE = 8,
  VCVS = 9,
  VCCS = 10,
  CCCS = 11,
  CCVS = 12,
  TLINE = 13,
  UNRECOGNIZED = -1,
}

export function spiceTypeFromJSON(object: any): SpiceType {
  switch (object) {
    case 0:
    case "SUBCKT":
      return SpiceType.SUBCKT;
    case 1:
    case "RESISTOR":
      return SpiceType.RESISTOR;
    case 2:
    case "CAPACITOR":
      return SpiceType.CAPACITOR;
    case 3:
    case "INDUCTOR":
      return SpiceType.INDUCTOR;
    case 4:
    case "MOS":
      return SpiceType.MOS;
    case 5:
    case "DIODE":
      return SpiceType.DIODE;
    case 6:
    case "BIPOLAR":
      return SpiceType.BIPOLAR;
    case 7:
    case "VSOURCE":
      return SpiceType.VSOURCE;
    case 8:
    case "ISOURCE":
      return SpiceType.ISOURCE;
    case 9:
    case "VCVS":
      return SpiceType.VCVS;
    case 10:
    case "VCCS":
      return SpiceType.VCCS;
    case 11:
    case "CCCS":
      return SpiceType.CCCS;
    case 12:
    case "CCVS":
      return SpiceType.CCVS;
    case 13:
    case "TLINE":
      return SpiceType.TLINE;
    case -1:
    case "UNRECOGNIZED":
    default:
      return SpiceType.UNRECOGNIZED;
  }
}

export function spiceTypeToJSON(object: SpiceType): string {
  switch (object) {
    case SpiceType.SUBCKT:
      return "SUBCKT";
    case SpiceType.RESISTOR:
      return "RESISTOR";
    case SpiceType.CAPACITOR:
      return "CAPACITOR";
    case SpiceType.INDUCTOR:
      return "INDUCTOR";
    case SpiceType.MOS:
      return "MOS";
    case SpiceType.DIODE:
      return "DIODE";
    case SpiceType.BIPOLAR:
      return "BIPOLAR";
    case SpiceType.VSOURCE:
      return "VSOURCE";
    case SpiceType.ISOURCE:
      return "ISOURCE";
    case SpiceType.VCVS:
      return "VCVS";
    case SpiceType.VCCS:
      return "VCCS";
    case SpiceType.CCCS:
      return "CCCS";
    case SpiceType.CCVS:
      return "CCVS";
    case SpiceType.TLINE:
      return "TLINE";
    case SpiceType.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/**
 * # Package
 * A Collection of Modules and ExternalModules
 */
export interface Package {
  /** Domain Name */
  domain: string;
  /** `Module` Definitions */
  modules: Module[];
  /** `ExternalModule` interfaces used by `modules`, and available externally */
  extModules: ExternalModule[];
  /** Description */
  desc: string;
}

/**
 * # Port
 * An externally-visible `Signal` with a `Direction`.
 */
export interface Port {
  /** Reference to `Signal` by name */
  signal: string;
  /** Port direction */
  direction: Port_Direction;
}

export enum Port_Direction {
  INPUT = 0,
  OUTPUT = 1,
  INOUT = 2,
  NONE = 3,
  UNRECOGNIZED = -1,
}

export function port_DirectionFromJSON(object: any): Port_Direction {
  switch (object) {
    case 0:
    case "INPUT":
      return Port_Direction.INPUT;
    case 1:
    case "OUTPUT":
      return Port_Direction.OUTPUT;
    case 2:
    case "INOUT":
      return Port_Direction.INOUT;
    case 3:
    case "NONE":
      return Port_Direction.NONE;
    case -1:
    case "UNRECOGNIZED":
    default:
      return Port_Direction.UNRECOGNIZED;
  }
}

export function port_DirectionToJSON(object: Port_Direction): string {
  switch (object) {
    case Port_Direction.INPUT:
      return "INPUT";
    case Port_Direction.OUTPUT:
      return "OUTPUT";
    case Port_Direction.INOUT:
      return "INOUT";
    case Port_Direction.NONE:
      return "NONE";
    case Port_Direction.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/**
 * # Signal
 * A named connection element, potentially with non-unit `width`.
 */
export interface Signal {
  /** Signal Name */
  name: string;
  /** Bus Width */
  width: number;
}

/**
 * # Signal Slice
 * Reference to a subset of bits of `signal`.
 * Indices `top` and `bot` are both inclusive, similar to popular HDLs.
 */
export interface Slice {
  /** Parent Signal Name */
  signal: string;
  /** Top Index */
  top: number;
  /** Bottom Index */
  bot: number;
}

/**
 * Signal Concatenation
 * FIXME: documentation of ordering, MSB-LSB
 */
export interface Concat {
  parts: ConnectionTarget[];
}

/**
 * # ConnectionTarget Union
 * Enumerates all types that can be
 * (a) Connected to Ports, and
 * (b) Concatenated
 */
export interface ConnectionTarget {
  stype?:
    | { $case: "sig"; sig: string }
    | { $case: "slice"; slice: Slice }
    | { $case: "concat"; concat: Concat }
    | undefined;
}

/**
 * # Port Connection
 * Pairing between an Instance port (name) and a parent-module ConnectionTarget.
 */
export interface Connection {
  portname: string;
  target: ConnectionTarget | undefined;
}

/** Module Instance */
export interface Instance {
  /** Instance Name */
  name: string;
  /** Reference to Module instantiated */
  module:
    | Reference
    | undefined;
  /** Parameter Values */
  parameters: Param[];
  /** Port `Connection`s */
  connections: Connection[];
}

/** Module - the primary unit of hardware re-use */
export interface Module {
  /** Module Name */
  name: string;
  /**
   * Port List, referring to elements of `signals` by name
   * Ordered as they will be in order-sensitive formats, such as typical netlist formats.
   */
  ports: Port[];
  /** Signal Definitions, including externally-facing `Port` signals */
  signals: Signal[];
  /** Module Instances */
  instances: Instance[];
  /** Parameters */
  parameters: Param[];
  /** Literal Contents, e.g. in downstream EDA formats */
  literals: string[];
}

/**
 * # Externally Defined Module
 * Primarily for sake of port-ordering, for translation with connect-by-position
 * formats.
 */
export interface ExternalModule {
  /** Qualified External Module Name */
  name:
    | QualifiedName
    | undefined;
  /** Description */
  desc: string;
  /**
   * Port Definitions
   * Ordered as they will be in order-sensitive formats, such as typical netlist formats.
   */
  ports: Port[];
  /** Signal Definitions, limited to those used by external-facing ports. */
  signals: Signal[];
  /** Params */
  parameters: Param[];
  /** Spice Type, SUBCKT by default */
  spicetype: SpiceType;
}

/**
 * # Interface
 * Defines the logical IO of a `Module`
 */
export interface Interface {
  /** Cell Name */
  name: string;
  /** Port List */
  ports: Port[];
}

function createBasePackage(): Package {
  return { domain: "", modules: [], extModules: [], desc: "" };
}

export const Package = {
  encode(message: Package, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.domain !== "") {
      writer.uint32(10).string(message.domain);
    }
    for (const v of message.modules) {
      Module.encode(v!, writer.uint32(18).fork()).ldelim();
    }
    for (const v of message.extModules) {
      ExternalModule.encode(v!, writer.uint32(26).fork()).ldelim();
    }
    if (message.desc !== "") {
      writer.uint32(82).string(message.desc);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Package {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePackage();
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

          message.modules.push(Module.decode(reader, reader.uint32()));
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.extModules.push(ExternalModule.decode(reader, reader.uint32()));
          continue;
        case 10:
          if (tag !== 82) {
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

  fromJSON(object: any): Package {
    return {
      domain: isSet(object.domain) ? globalThis.String(object.domain) : "",
      modules: globalThis.Array.isArray(object?.modules) ? object.modules.map((e: any) => Module.fromJSON(e)) : [],
      extModules: globalThis.Array.isArray(object?.extModules)
        ? object.extModules.map((e: any) => ExternalModule.fromJSON(e))
        : [],
      desc: isSet(object.desc) ? globalThis.String(object.desc) : "",
    };
  },

  toJSON(message: Package): unknown {
    const obj: any = {};
    if (message.domain !== "") {
      obj.domain = message.domain;
    }
    if (message.modules?.length) {
      obj.modules = message.modules.map((e) => Module.toJSON(e));
    }
    if (message.extModules?.length) {
      obj.extModules = message.extModules.map((e) => ExternalModule.toJSON(e));
    }
    if (message.desc !== "") {
      obj.desc = message.desc;
    }
    return obj;
  },

  create(base?: DeepPartial<Package>): Package {
    return Package.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Package>): Package {
    const message = createBasePackage();
    message.domain = object.domain ?? "";
    message.modules = object.modules?.map((e) => Module.fromPartial(e)) || [];
    message.extModules = object.extModules?.map((e) => ExternalModule.fromPartial(e)) || [];
    message.desc = object.desc ?? "";
    return message;
  },
};

function createBasePort(): Port {
  return { signal: "", direction: 0 };
}

export const Port = {
  encode(message: Port, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.signal !== "") {
      writer.uint32(10).string(message.signal);
    }
    if (message.direction !== 0) {
      writer.uint32(16).int32(message.direction);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Port {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePort();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.signal = reader.string();
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.direction = reader.int32() as any;
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Port {
    return {
      signal: isSet(object.signal) ? globalThis.String(object.signal) : "",
      direction: isSet(object.direction) ? port_DirectionFromJSON(object.direction) : 0,
    };
  },

  toJSON(message: Port): unknown {
    const obj: any = {};
    if (message.signal !== "") {
      obj.signal = message.signal;
    }
    if (message.direction !== 0) {
      obj.direction = port_DirectionToJSON(message.direction);
    }
    return obj;
  },

  create(base?: DeepPartial<Port>): Port {
    return Port.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Port>): Port {
    const message = createBasePort();
    message.signal = object.signal ?? "";
    message.direction = object.direction ?? 0;
    return message;
  },
};

function createBaseSignal(): Signal {
  return { name: "", width: 0 };
}

export const Signal = {
  encode(message: Signal, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.width !== 0) {
      writer.uint32(16).int64(message.width);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Signal {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseSignal();
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
          if (tag !== 16) {
            break;
          }

          message.width = longToNumber(reader.int64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Signal {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      width: isSet(object.width) ? globalThis.Number(object.width) : 0,
    };
  },

  toJSON(message: Signal): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.width !== 0) {
      obj.width = Math.round(message.width);
    }
    return obj;
  },

  create(base?: DeepPartial<Signal>): Signal {
    return Signal.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Signal>): Signal {
    const message = createBaseSignal();
    message.name = object.name ?? "";
    message.width = object.width ?? 0;
    return message;
  },
};

function createBaseSlice(): Slice {
  return { signal: "", top: 0, bot: 0 };
}

export const Slice = {
  encode(message: Slice, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.signal !== "") {
      writer.uint32(10).string(message.signal);
    }
    if (message.top !== 0) {
      writer.uint32(16).int64(message.top);
    }
    if (message.bot !== 0) {
      writer.uint32(24).int64(message.bot);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Slice {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseSlice();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.signal = reader.string();
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.top = longToNumber(reader.int64() as Long);
          continue;
        case 3:
          if (tag !== 24) {
            break;
          }

          message.bot = longToNumber(reader.int64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Slice {
    return {
      signal: isSet(object.signal) ? globalThis.String(object.signal) : "",
      top: isSet(object.top) ? globalThis.Number(object.top) : 0,
      bot: isSet(object.bot) ? globalThis.Number(object.bot) : 0,
    };
  },

  toJSON(message: Slice): unknown {
    const obj: any = {};
    if (message.signal !== "") {
      obj.signal = message.signal;
    }
    if (message.top !== 0) {
      obj.top = Math.round(message.top);
    }
    if (message.bot !== 0) {
      obj.bot = Math.round(message.bot);
    }
    return obj;
  },

  create(base?: DeepPartial<Slice>): Slice {
    return Slice.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Slice>): Slice {
    const message = createBaseSlice();
    message.signal = object.signal ?? "";
    message.top = object.top ?? 0;
    message.bot = object.bot ?? 0;
    return message;
  },
};

function createBaseConcat(): Concat {
  return { parts: [] };
}

export const Concat = {
  encode(message: Concat, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    for (const v of message.parts) {
      ConnectionTarget.encode(v!, writer.uint32(10).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Concat {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseConcat();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.parts.push(ConnectionTarget.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Concat {
    return {
      parts: globalThis.Array.isArray(object?.parts) ? object.parts.map((e: any) => ConnectionTarget.fromJSON(e)) : [],
    };
  },

  toJSON(message: Concat): unknown {
    const obj: any = {};
    if (message.parts?.length) {
      obj.parts = message.parts.map((e) => ConnectionTarget.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<Concat>): Concat {
    return Concat.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Concat>): Concat {
    const message = createBaseConcat();
    message.parts = object.parts?.map((e) => ConnectionTarget.fromPartial(e)) || [];
    return message;
  },
};

function createBaseConnectionTarget(): ConnectionTarget {
  return { stype: undefined };
}

export const ConnectionTarget = {
  encode(message: ConnectionTarget, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    switch (message.stype?.$case) {
      case "sig":
        writer.uint32(10).string(message.stype.sig);
        break;
      case "slice":
        Slice.encode(message.stype.slice, writer.uint32(18).fork()).ldelim();
        break;
      case "concat":
        Concat.encode(message.stype.concat, writer.uint32(26).fork()).ldelim();
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): ConnectionTarget {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseConnectionTarget();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.stype = { $case: "sig", sig: reader.string() };
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.stype = { $case: "slice", slice: Slice.decode(reader, reader.uint32()) };
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.stype = { $case: "concat", concat: Concat.decode(reader, reader.uint32()) };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): ConnectionTarget {
    return {
      stype: isSet(object.sig)
        ? { $case: "sig", sig: globalThis.String(object.sig) }
        : isSet(object.slice)
        ? { $case: "slice", slice: Slice.fromJSON(object.slice) }
        : isSet(object.concat)
        ? { $case: "concat", concat: Concat.fromJSON(object.concat) }
        : undefined,
    };
  },

  toJSON(message: ConnectionTarget): unknown {
    const obj: any = {};
    if (message.stype?.$case === "sig") {
      obj.sig = message.stype.sig;
    }
    if (message.stype?.$case === "slice") {
      obj.slice = Slice.toJSON(message.stype.slice);
    }
    if (message.stype?.$case === "concat") {
      obj.concat = Concat.toJSON(message.stype.concat);
    }
    return obj;
  },

  create(base?: DeepPartial<ConnectionTarget>): ConnectionTarget {
    return ConnectionTarget.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<ConnectionTarget>): ConnectionTarget {
    const message = createBaseConnectionTarget();
    if (object.stype?.$case === "sig" && object.stype?.sig !== undefined && object.stype?.sig !== null) {
      message.stype = { $case: "sig", sig: object.stype.sig };
    }
    if (object.stype?.$case === "slice" && object.stype?.slice !== undefined && object.stype?.slice !== null) {
      message.stype = { $case: "slice", slice: Slice.fromPartial(object.stype.slice) };
    }
    if (object.stype?.$case === "concat" && object.stype?.concat !== undefined && object.stype?.concat !== null) {
      message.stype = { $case: "concat", concat: Concat.fromPartial(object.stype.concat) };
    }
    return message;
  },
};

function createBaseConnection(): Connection {
  return { portname: "", target: undefined };
}

export const Connection = {
  encode(message: Connection, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.portname !== "") {
      writer.uint32(10).string(message.portname);
    }
    if (message.target !== undefined) {
      ConnectionTarget.encode(message.target, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Connection {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseConnection();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.portname = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.target = ConnectionTarget.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Connection {
    return {
      portname: isSet(object.portname) ? globalThis.String(object.portname) : "",
      target: isSet(object.target) ? ConnectionTarget.fromJSON(object.target) : undefined,
    };
  },

  toJSON(message: Connection): unknown {
    const obj: any = {};
    if (message.portname !== "") {
      obj.portname = message.portname;
    }
    if (message.target !== undefined) {
      obj.target = ConnectionTarget.toJSON(message.target);
    }
    return obj;
  },

  create(base?: DeepPartial<Connection>): Connection {
    return Connection.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Connection>): Connection {
    const message = createBaseConnection();
    message.portname = object.portname ?? "";
    message.target = (object.target !== undefined && object.target !== null)
      ? ConnectionTarget.fromPartial(object.target)
      : undefined;
    return message;
  },
};

function createBaseInstance(): Instance {
  return { name: "", module: undefined, parameters: [], connections: [] };
}

export const Instance = {
  encode(message: Instance, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.module !== undefined) {
      Reference.encode(message.module, writer.uint32(18).fork()).ldelim();
    }
    for (const v of message.parameters) {
      Param.encode(v!, writer.uint32(26).fork()).ldelim();
    }
    for (const v of message.connections) {
      Connection.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Instance {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseInstance();
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

          message.module = Reference.decode(reader, reader.uint32());
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.parameters.push(Param.decode(reader, reader.uint32()));
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.connections.push(Connection.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Instance {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      module: isSet(object.module) ? Reference.fromJSON(object.module) : undefined,
      parameters: globalThis.Array.isArray(object?.parameters)
        ? object.parameters.map((e: any) => Param.fromJSON(e))
        : [],
      connections: globalThis.Array.isArray(object?.connections)
        ? object.connections.map((e: any) => Connection.fromJSON(e))
        : [],
    };
  },

  toJSON(message: Instance): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.module !== undefined) {
      obj.module = Reference.toJSON(message.module);
    }
    if (message.parameters?.length) {
      obj.parameters = message.parameters.map((e) => Param.toJSON(e));
    }
    if (message.connections?.length) {
      obj.connections = message.connections.map((e) => Connection.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<Instance>): Instance {
    return Instance.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Instance>): Instance {
    const message = createBaseInstance();
    message.name = object.name ?? "";
    message.module = (object.module !== undefined && object.module !== null)
      ? Reference.fromPartial(object.module)
      : undefined;
    message.parameters = object.parameters?.map((e) => Param.fromPartial(e)) || [];
    message.connections = object.connections?.map((e) => Connection.fromPartial(e)) || [];
    return message;
  },
};

function createBaseModule(): Module {
  return { name: "", ports: [], signals: [], instances: [], parameters: [], literals: [] };
}

export const Module = {
  encode(message: Module, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    for (const v of message.ports) {
      Port.encode(v!, writer.uint32(18).fork()).ldelim();
    }
    for (const v of message.signals) {
      Signal.encode(v!, writer.uint32(26).fork()).ldelim();
    }
    for (const v of message.instances) {
      Instance.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    for (const v of message.parameters) {
      Param.encode(v!, writer.uint32(42).fork()).ldelim();
    }
    for (const v of message.literals) {
      writer.uint32(50).string(v!);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Module {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseModule();
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

          message.ports.push(Port.decode(reader, reader.uint32()));
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.signals.push(Signal.decode(reader, reader.uint32()));
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.instances.push(Instance.decode(reader, reader.uint32()));
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.parameters.push(Param.decode(reader, reader.uint32()));
          continue;
        case 6:
          if (tag !== 50) {
            break;
          }

          message.literals.push(reader.string());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Module {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      ports: globalThis.Array.isArray(object?.ports) ? object.ports.map((e: any) => Port.fromJSON(e)) : [],
      signals: globalThis.Array.isArray(object?.signals) ? object.signals.map((e: any) => Signal.fromJSON(e)) : [],
      instances: globalThis.Array.isArray(object?.instances)
        ? object.instances.map((e: any) => Instance.fromJSON(e))
        : [],
      parameters: globalThis.Array.isArray(object?.parameters)
        ? object.parameters.map((e: any) => Param.fromJSON(e))
        : [],
      literals: globalThis.Array.isArray(object?.literals) ? object.literals.map((e: any) => globalThis.String(e)) : [],
    };
  },

  toJSON(message: Module): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.ports?.length) {
      obj.ports = message.ports.map((e) => Port.toJSON(e));
    }
    if (message.signals?.length) {
      obj.signals = message.signals.map((e) => Signal.toJSON(e));
    }
    if (message.instances?.length) {
      obj.instances = message.instances.map((e) => Instance.toJSON(e));
    }
    if (message.parameters?.length) {
      obj.parameters = message.parameters.map((e) => Param.toJSON(e));
    }
    if (message.literals?.length) {
      obj.literals = message.literals;
    }
    return obj;
  },

  create(base?: DeepPartial<Module>): Module {
    return Module.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Module>): Module {
    const message = createBaseModule();
    message.name = object.name ?? "";
    message.ports = object.ports?.map((e) => Port.fromPartial(e)) || [];
    message.signals = object.signals?.map((e) => Signal.fromPartial(e)) || [];
    message.instances = object.instances?.map((e) => Instance.fromPartial(e)) || [];
    message.parameters = object.parameters?.map((e) => Param.fromPartial(e)) || [];
    message.literals = object.literals?.map((e) => e) || [];
    return message;
  },
};

function createBaseExternalModule(): ExternalModule {
  return { name: undefined, desc: "", ports: [], signals: [], parameters: [], spicetype: 0 };
}

export const ExternalModule = {
  encode(message: ExternalModule, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== undefined) {
      QualifiedName.encode(message.name, writer.uint32(10).fork()).ldelim();
    }
    if (message.desc !== "") {
      writer.uint32(18).string(message.desc);
    }
    for (const v of message.ports) {
      Port.encode(v!, writer.uint32(26).fork()).ldelim();
    }
    for (const v of message.signals) {
      Signal.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    for (const v of message.parameters) {
      Param.encode(v!, writer.uint32(42).fork()).ldelim();
    }
    if (message.spicetype !== 0) {
      writer.uint32(48).int32(message.spicetype);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): ExternalModule {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseExternalModule();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.name = QualifiedName.decode(reader, reader.uint32());
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.desc = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.ports.push(Port.decode(reader, reader.uint32()));
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.signals.push(Signal.decode(reader, reader.uint32()));
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.parameters.push(Param.decode(reader, reader.uint32()));
          continue;
        case 6:
          if (tag !== 48) {
            break;
          }

          message.spicetype = reader.int32() as any;
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): ExternalModule {
    return {
      name: isSet(object.name) ? QualifiedName.fromJSON(object.name) : undefined,
      desc: isSet(object.desc) ? globalThis.String(object.desc) : "",
      ports: globalThis.Array.isArray(object?.ports) ? object.ports.map((e: any) => Port.fromJSON(e)) : [],
      signals: globalThis.Array.isArray(object?.signals) ? object.signals.map((e: any) => Signal.fromJSON(e)) : [],
      parameters: globalThis.Array.isArray(object?.parameters)
        ? object.parameters.map((e: any) => Param.fromJSON(e))
        : [],
      spicetype: isSet(object.spicetype) ? spiceTypeFromJSON(object.spicetype) : 0,
    };
  },

  toJSON(message: ExternalModule): unknown {
    const obj: any = {};
    if (message.name !== undefined) {
      obj.name = QualifiedName.toJSON(message.name);
    }
    if (message.desc !== "") {
      obj.desc = message.desc;
    }
    if (message.ports?.length) {
      obj.ports = message.ports.map((e) => Port.toJSON(e));
    }
    if (message.signals?.length) {
      obj.signals = message.signals.map((e) => Signal.toJSON(e));
    }
    if (message.parameters?.length) {
      obj.parameters = message.parameters.map((e) => Param.toJSON(e));
    }
    if (message.spicetype !== 0) {
      obj.spicetype = spiceTypeToJSON(message.spicetype);
    }
    return obj;
  },

  create(base?: DeepPartial<ExternalModule>): ExternalModule {
    return ExternalModule.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<ExternalModule>): ExternalModule {
    const message = createBaseExternalModule();
    message.name = (object.name !== undefined && object.name !== null)
      ? QualifiedName.fromPartial(object.name)
      : undefined;
    message.desc = object.desc ?? "";
    message.ports = object.ports?.map((e) => Port.fromPartial(e)) || [];
    message.signals = object.signals?.map((e) => Signal.fromPartial(e)) || [];
    message.parameters = object.parameters?.map((e) => Param.fromPartial(e)) || [];
    message.spicetype = object.spicetype ?? 0;
    return message;
  },
};

function createBaseInterface(): Interface {
  return { name: "", ports: [] };
}

export const Interface = {
  encode(message: Interface, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    for (const v of message.ports) {
      Port.encode(v!, writer.uint32(82).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Interface {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseInterface();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.name = reader.string();
          continue;
        case 10:
          if (tag !== 82) {
            break;
          }

          message.ports.push(Port.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Interface {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      ports: globalThis.Array.isArray(object?.ports) ? object.ports.map((e: any) => Port.fromJSON(e)) : [],
    };
  },

  toJSON(message: Interface): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.ports?.length) {
      obj.ports = message.ports.map((e) => Port.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<Interface>): Interface {
    return Interface.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Interface>): Interface {
    const message = createBaseInterface();
    message.name = object.name ?? "";
    message.ports = object.ports?.map((e) => Port.fromPartial(e)) || [];
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
