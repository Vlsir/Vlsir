/* eslint-disable */
import _m0 from "protobufjs/minimal";
import { Package } from "./circuit";

export enum NetlistFormat {
  UNSPECIFIED = 0,
  SPECTRE = 1,
  SPICE = 2,
  NGSPICE = 3,
  XYCE = 4,
  HSPICE = 5,
  CDL = 6,
  VERILOG = 10,
  UNRECOGNIZED = -1,
}

export function netlistFormatFromJSON(object: any): NetlistFormat {
  switch (object) {
    case 0:
    case "UNSPECIFIED":
      return NetlistFormat.UNSPECIFIED;
    case 1:
    case "SPECTRE":
      return NetlistFormat.SPECTRE;
    case 2:
    case "SPICE":
      return NetlistFormat.SPICE;
    case 3:
    case "NGSPICE":
      return NetlistFormat.NGSPICE;
    case 4:
    case "XYCE":
      return NetlistFormat.XYCE;
    case 5:
    case "HSPICE":
      return NetlistFormat.HSPICE;
    case 6:
    case "CDL":
      return NetlistFormat.CDL;
    case 10:
    case "VERILOG":
      return NetlistFormat.VERILOG;
    case -1:
    case "UNRECOGNIZED":
    default:
      return NetlistFormat.UNRECOGNIZED;
  }
}

export function netlistFormatToJSON(object: NetlistFormat): string {
  switch (object) {
    case NetlistFormat.UNSPECIFIED:
      return "UNSPECIFIED";
    case NetlistFormat.SPECTRE:
      return "SPECTRE";
    case NetlistFormat.SPICE:
      return "SPICE";
    case NetlistFormat.NGSPICE:
      return "NGSPICE";
    case NetlistFormat.XYCE:
      return "XYCE";
    case NetlistFormat.HSPICE:
      return "HSPICE";
    case NetlistFormat.CDL:
      return "CDL";
    case NetlistFormat.VERILOG:
      return "VERILOG";
    case NetlistFormat.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

export interface NetlistInput {
  /** Circuit Package Content */
  pkg:
    | Package
    | undefined;
  /** Destination Path */
  netlistPath: string;
  /** Netlist Format */
  fmt: NetlistFormat;
  /** Result Path */
  resultPath: string;
}

export interface NetlistResult {
  variant?: { $case: "success"; success: boolean } | { $case: "fail"; fail: string } | undefined;
}

function createBaseNetlistInput(): NetlistInput {
  return { pkg: undefined, netlistPath: "", fmt: 0, resultPath: "" };
}

export const NetlistInput = {
  encode(message: NetlistInput, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.pkg !== undefined) {
      Package.encode(message.pkg, writer.uint32(10).fork()).ldelim();
    }
    if (message.netlistPath !== "") {
      writer.uint32(18).string(message.netlistPath);
    }
    if (message.fmt !== 0) {
      writer.uint32(24).int32(message.fmt);
    }
    if (message.resultPath !== "") {
      writer.uint32(34).string(message.resultPath);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): NetlistInput {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseNetlistInput();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.pkg = Package.decode(reader, reader.uint32());
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.netlistPath = reader.string();
          continue;
        case 3:
          if (tag !== 24) {
            break;
          }

          message.fmt = reader.int32() as any;
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.resultPath = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): NetlistInput {
    return {
      pkg: isSet(object.pkg) ? Package.fromJSON(object.pkg) : undefined,
      netlistPath: isSet(object.netlistPath) ? globalThis.String(object.netlistPath) : "",
      fmt: isSet(object.fmt) ? netlistFormatFromJSON(object.fmt) : 0,
      resultPath: isSet(object.resultPath) ? globalThis.String(object.resultPath) : "",
    };
  },

  toJSON(message: NetlistInput): unknown {
    const obj: any = {};
    if (message.pkg !== undefined) {
      obj.pkg = Package.toJSON(message.pkg);
    }
    if (message.netlistPath !== "") {
      obj.netlistPath = message.netlistPath;
    }
    if (message.fmt !== 0) {
      obj.fmt = netlistFormatToJSON(message.fmt);
    }
    if (message.resultPath !== "") {
      obj.resultPath = message.resultPath;
    }
    return obj;
  },

  create(base?: DeepPartial<NetlistInput>): NetlistInput {
    return NetlistInput.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<NetlistInput>): NetlistInput {
    const message = createBaseNetlistInput();
    message.pkg = (object.pkg !== undefined && object.pkg !== null) ? Package.fromPartial(object.pkg) : undefined;
    message.netlistPath = object.netlistPath ?? "";
    message.fmt = object.fmt ?? 0;
    message.resultPath = object.resultPath ?? "";
    return message;
  },
};

function createBaseNetlistResult(): NetlistResult {
  return { variant: undefined };
}

export const NetlistResult = {
  encode(message: NetlistResult, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    switch (message.variant?.$case) {
      case "success":
        writer.uint32(8).bool(message.variant.success);
        break;
      case "fail":
        writer.uint32(18).string(message.variant.fail);
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): NetlistResult {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseNetlistResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.variant = { $case: "success", success: reader.bool() };
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.variant = { $case: "fail", fail: reader.string() };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): NetlistResult {
    return {
      variant: isSet(object.success)
        ? { $case: "success", success: globalThis.Boolean(object.success) }
        : isSet(object.fail)
        ? { $case: "fail", fail: globalThis.String(object.fail) }
        : undefined,
    };
  },

  toJSON(message: NetlistResult): unknown {
    const obj: any = {};
    if (message.variant?.$case === "success") {
      obj.success = message.variant.success;
    }
    if (message.variant?.$case === "fail") {
      obj.fail = message.variant.fail;
    }
    return obj;
  },

  create(base?: DeepPartial<NetlistResult>): NetlistResult {
    return NetlistResult.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<NetlistResult>): NetlistResult {
    const message = createBaseNetlistResult();
    if (
      object.variant?.$case === "success" && object.variant?.success !== undefined && object.variant?.success !== null
    ) {
      message.variant = { $case: "success", success: object.variant.success };
    }
    if (object.variant?.$case === "fail" && object.variant?.fail !== undefined && object.variant?.fail !== null) {
      message.variant = { $case: "fail", fail: object.variant.fail };
    }
    return message;
  },
};

/**
 * ############################################################################
 * # `Netlist` Service
 * ############################################################################
 */
export interface Netlist {
  Netlist(request: NetlistInput): Promise<NetlistResult>;
}

export const NetlistServiceName = "vlsir.netlist.Netlist";
export class NetlistClientImpl implements Netlist {
  private readonly rpc: Rpc;
  private readonly service: string;
  constructor(rpc: Rpc, opts?: { service?: string }) {
    this.service = opts?.service || NetlistServiceName;
    this.rpc = rpc;
    this.Netlist = this.Netlist.bind(this);
  }
  Netlist(request: NetlistInput): Promise<NetlistResult> {
    const data = NetlistInput.encode(request).finish();
    const promise = this.rpc.request(this.service, "Netlist", data);
    return promise.then((data) => NetlistResult.decode(_m0.Reader.create(data)));
  }
}

interface Rpc {
  request(service: string, method: string, data: Uint8Array): Promise<Uint8Array>;
}

type Builtin = Date | Function | Uint8Array | string | number | boolean | undefined;

type DeepPartial<T> = T extends Builtin ? T
  : T extends globalThis.Array<infer U> ? globalThis.Array<DeepPartial<U>>
  : T extends ReadonlyArray<infer U> ? ReadonlyArray<DeepPartial<U>>
  : T extends { $case: string } ? { [K in keyof Omit<T, "$case">]?: DeepPartial<T[K]> } & { $case: T["$case"] }
  : T extends {} ? { [K in keyof T]?: DeepPartial<T[K]> }
  : Partial<T>;

function isSet(value: any): boolean {
  return value !== null && value !== undefined;
}
