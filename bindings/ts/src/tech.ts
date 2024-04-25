/* eslint-disable */
import Long from "long";
import _m0 from "protobufjs/minimal";

export enum LayerPurposeType {
  UNKNOWN = 0,
  /** LABEL - Layers identified as LABEL will be used to attach net labels. */
  LABEL = 1,
  DRAWING = 2,
  PIN = 3,
  OBSTRUCTION = 4,
  OUTLINE = 5,
  UNRECOGNIZED = -1,
}

export function layerPurposeTypeFromJSON(object: any): LayerPurposeType {
  switch (object) {
    case 0:
    case "UNKNOWN":
      return LayerPurposeType.UNKNOWN;
    case 1:
    case "LABEL":
      return LayerPurposeType.LABEL;
    case 2:
    case "DRAWING":
      return LayerPurposeType.DRAWING;
    case 3:
    case "PIN":
      return LayerPurposeType.PIN;
    case 4:
    case "OBSTRUCTION":
      return LayerPurposeType.OBSTRUCTION;
    case 5:
    case "OUTLINE":
      return LayerPurposeType.OUTLINE;
    case -1:
    case "UNRECOGNIZED":
    default:
      return LayerPurposeType.UNRECOGNIZED;
  }
}

export function layerPurposeTypeToJSON(object: LayerPurposeType): string {
  switch (object) {
    case LayerPurposeType.UNKNOWN:
      return "UNKNOWN";
    case LayerPurposeType.LABEL:
      return "LABEL";
    case LayerPurposeType.DRAWING:
      return "DRAWING";
    case LayerPurposeType.PIN:
      return "PIN";
    case LayerPurposeType.OBSTRUCTION:
      return "OBSTRUCTION";
    case LayerPurposeType.OUTLINE:
      return "OUTLINE";
    case LayerPurposeType.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

export interface Technology {
  /** Skywater130, S130, Sky130, etc */
  name: string;
  packages: Package[];
  layers: LayerInfo[];
}

export interface Package {
  /** sky130_fd_sc_hd, sk130_fd_sc_hs, etc */
  name: string;
}

export interface LayerPurpose {
  /** Short-hand description of the purpose of the sub-layer, e.g. "drawing". */
  description: string;
  type: LayerPurposeType;
}

/**
 * Layers in PDKs roughly correspond to physical layers in the semiconductor
 * fabrication process. In this schema, a "layer" is a pair: first, some major
 * layer (like "the first metal layer") and second, some sub-index into that
 * layer distinguishing the various purposes objects serve on the major layor.
 */
export interface LayerInfo {
  /** A canonical shorthand name for the layer, e.g. "met1". */
  name: string;
  purpose: LayerPurpose | undefined;
  /** An integer index identifying the major layer. */
  index: number;
  /** An integer index identifying the sub layer, or purpose. */
  subIndex: number;
}

function createBaseTechnology(): Technology {
  return { name: "", packages: [], layers: [] };
}

export const Technology = {
  encode(
    message: Technology,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    for (const v of message.packages) {
      Package.encode(v!, writer.uint32(90).fork()).ldelim();
    }
    for (const v of message.layers) {
      LayerInfo.encode(v!, writer.uint32(810).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Technology {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTechnology();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.name = reader.string();
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.packages.push(Package.decode(reader, reader.uint32()));
          continue;
        case 101:
          if (tag !== 810) {
            break;
          }

          message.layers.push(LayerInfo.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Technology {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      packages: globalThis.Array.isArray(object?.packages)
        ? object.packages.map((e: any) => Package.fromJSON(e))
        : [],
      layers: globalThis.Array.isArray(object?.layers)
        ? object.layers.map((e: any) => LayerInfo.fromJSON(e))
        : [],
    };
  },

  toJSON(message: Technology): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.packages?.length) {
      obj.packages = message.packages.map((e) => Package.toJSON(e));
    }
    if (message.layers?.length) {
      obj.layers = message.layers.map((e) => LayerInfo.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<Technology>): Technology {
    return Technology.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Technology>): Technology {
    const message = createBaseTechnology();
    message.name = object.name ?? "";
    message.packages =
      object.packages?.map((e) => Package.fromPartial(e)) || [];
    message.layers = object.layers?.map((e) => LayerInfo.fromPartial(e)) || [];
    return message;
  },
};

function createBasePackage(): Package {
  return { name: "" };
}

export const Package = {
  encode(
    message: Package,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Package {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePackage();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
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

  fromJSON(object: any): Package {
    return { name: isSet(object.name) ? globalThis.String(object.name) : "" };
  },

  toJSON(message: Package): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    return obj;
  },

  create(base?: DeepPartial<Package>): Package {
    return Package.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Package>): Package {
    const message = createBasePackage();
    message.name = object.name ?? "";
    return message;
  },
};

function createBaseLayerPurpose(): LayerPurpose {
  return { description: "", type: 0 };
}

export const LayerPurpose = {
  encode(
    message: LayerPurpose,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.description !== "") {
      writer.uint32(10).string(message.description);
    }
    if (message.type !== 0) {
      writer.uint32(16).int32(message.type);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): LayerPurpose {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLayerPurpose();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.description = reader.string();
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.type = reader.int32() as any;
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): LayerPurpose {
    return {
      description: isSet(object.description)
        ? globalThis.String(object.description)
        : "",
      type: isSet(object.type) ? layerPurposeTypeFromJSON(object.type) : 0,
    };
  },

  toJSON(message: LayerPurpose): unknown {
    const obj: any = {};
    if (message.description !== "") {
      obj.description = message.description;
    }
    if (message.type !== 0) {
      obj.type = layerPurposeTypeToJSON(message.type);
    }
    return obj;
  },

  create(base?: DeepPartial<LayerPurpose>): LayerPurpose {
    return LayerPurpose.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<LayerPurpose>): LayerPurpose {
    const message = createBaseLayerPurpose();
    message.description = object.description ?? "";
    message.type = object.type ?? 0;
    return message;
  },
};

function createBaseLayerInfo(): LayerInfo {
  return { name: "", purpose: undefined, index: 0, subIndex: 0 };
}

export const LayerInfo = {
  encode(
    message: LayerInfo,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.purpose !== undefined) {
      LayerPurpose.encode(message.purpose, writer.uint32(90).fork()).ldelim();
    }
    if (message.index !== 0) {
      writer.uint32(168).uint64(message.index);
    }
    if (message.subIndex !== 0) {
      writer.uint32(248).uint64(message.subIndex);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): LayerInfo {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLayerInfo();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.name = reader.string();
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.purpose = LayerPurpose.decode(reader, reader.uint32());
          continue;
        case 21:
          if (tag !== 168) {
            break;
          }

          message.index = longToNumber(reader.uint64() as Long);
          continue;
        case 31:
          if (tag !== 248) {
            break;
          }

          message.subIndex = longToNumber(reader.uint64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): LayerInfo {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      purpose: isSet(object.purpose)
        ? LayerPurpose.fromJSON(object.purpose)
        : undefined,
      index: isSet(object.index) ? globalThis.Number(object.index) : 0,
      subIndex: isSet(object.subIndex) ? globalThis.Number(object.subIndex) : 0,
    };
  },

  toJSON(message: LayerInfo): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.purpose !== undefined) {
      obj.purpose = LayerPurpose.toJSON(message.purpose);
    }
    if (message.index !== 0) {
      obj.index = Math.round(message.index);
    }
    if (message.subIndex !== 0) {
      obj.subIndex = Math.round(message.subIndex);
    }
    return obj;
  },

  create(base?: DeepPartial<LayerInfo>): LayerInfo {
    return LayerInfo.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<LayerInfo>): LayerInfo {
    const message = createBaseLayerInfo();
    message.name = object.name ?? "";
    message.purpose =
      object.purpose !== undefined && object.purpose !== null
        ? LayerPurpose.fromPartial(object.purpose)
        : undefined;
    message.index = object.index ?? 0;
    message.subIndex = object.subIndex ?? 0;
    return message;
  },
};

type Builtin =
  | Date
  | Function
  | Uint8Array
  | string
  | number
  | boolean
  | undefined;

type DeepPartial<T> = T extends Builtin
  ? T
  : T extends globalThis.Array<infer U>
    ? globalThis.Array<DeepPartial<U>>
    : T extends ReadonlyArray<infer U>
      ? ReadonlyArray<DeepPartial<U>>
      : T extends { $case: string }
        ? { [K in keyof Omit<T, "$case">]?: DeepPartial<T[K]> } & {
            $case: T["$case"];
          }
        : T extends {}
          ? { [K in keyof T]?: DeepPartial<T[K]> }
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
