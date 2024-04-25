/* eslint-disable */
import Long from "long";
import _m0 from "protobufjs/minimal";
import { Package } from "./circuit";
import { Param, ParamValue } from "./utils";

/**
 * # Simulation Input
 *
 * Consists of:
 * * The design under test (DUT) circuit `ckt`,
 * * Global simulator options, e.g. tolerance requirements,
 * * A list of circuit-analyses to be completed,
 * * An optional list of control-elements
 */
export interface SimInput {
  /**
   * # Circuit Input
   * The DUT circuit-package under test
   */
  pkg: Package | undefined;
  /** Top-level module (name) */
  top: string;
  /**
   * # Simulation Configuration Input
   * List of simulator options
   */
  opts: SimOptions[];
  /** List of circuit analyses */
  an: Analysis[];
  /**
   * Control elements.
   * `SimInput` level controls are applied to *all* analyses.
   */
  ctrls: Control[];
}

/**
 * # Simulation Result
 * A list of results per analysis
 */
export interface SimResult {
  an: AnalysisResult[];
}

/**
 * # Simulator Options
 * Global, cross-analysis settings.
 */
export interface SimOptions {
  /** Option name */
  name: string;
  /** Option argument */
  value: ParamValue | undefined;
}

/**
 * # Analysis Union
 *
 * Enumerated analysis-input types.
 * Primary component of a `Sim`.
 */
export interface Analysis {
  an?:
    | { $case: "op"; op: OpInput }
    | { $case: "dc"; dc: DcInput }
    | { $case: "tran"; tran: TranInput }
    | { $case: "ac"; ac: AcInput }
    | { $case: "noise"; noise: NoiseInput }
    | { $case: "sweep"; sweep: SweepInput }
    | { $case: "monte"; monte: MonteInput }
    | { $case: "custom"; custom: CustomAnalysisInput }
    | undefined;
}

/**
 * # Analysis Results Union
 *
 * Union of result-types for each `Analysis`.
 */
export interface AnalysisResult {
  an?:
    | { $case: "op"; op: OpResult }
    | { $case: "dc"; dc: DcResult }
    | { $case: "tran"; tran: TranResult }
    | { $case: "ac"; ac: AcResult }
    | { $case: "noise"; noise: NoiseResult }
    | { $case: "sweep"; sweep: SweepResult }
    | { $case: "monte"; monte: MonteResult }
    | { $case: "custom"; custom: CustomAnalysisResult }
    | undefined;
}

/** # Operating Point Inputs */
export interface OpInput {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Control Elements */
  ctrls: Control[];
}

/** Operating Point Results */
export interface OpResult {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Signal names and quantities */
  signals: string[];
  /** Data values, in `signals` order */
  data: number[];
}

/** # Dc Sweep Inputs */
export interface DcInput {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Sweep Variable Name */
  indepName: string;
  /** Sweep Data */
  sweep: Sweep | undefined;
  /** Control Elements */
  ctrls: Control[];
}

/**
 * # Dc Sweep Result
 *
 * Provides result data for a `Dc` analysis.
 */
export interface DcResult {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Independent Variable Name */
  indepName: string;
  /** Ordered signal names and quantities */
  signals: string[];
  /** Primary Data Field */
  data: number[];
  /** Scalar measurement values */
  measurements: { [key: string]: number };
}

export interface DcResult_MeasurementsEntry {
  key: string;
  value: number;
}

/** # Transient Analysis Inputs */
export interface TranInput {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Stop Time */
  tstop: number;
  /** Time-step requirement or recommendation */
  tstep: number;
  /** Initial Conditions. Mapping in the form of {signal-name: value} */
  ic: { [key: string]: number };
  /** Control Elements */
  ctrls: Control[];
}

export interface TranInput_IcEntry {
  key: string;
  value: number;
}

/** # Transient Analysis Results */
export interface TranResult {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Ordered signal names and quantities */
  signals: string[];
  /** Primary Data Field */
  data: number[];
  /** Scalar measurement values */
  measurements: { [key: string]: number };
}

export interface TranResult_MeasurementsEntry {
  key: string;
  value: number;
}

/** # Complex Number */
export interface ComplexNum {
  re: number;
  im: number;
}

/** # AC Analysis Inputs */
export interface AcInput {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Start (min) frequency in Hz */
  fstart: number;
  /** Stop (max) frequency in Hz */
  fstop: number;
  /** Number of points per interval of frequency sweep. */
  npts: number;
  /** Control Elements */
  ctrls: Control[];
}

/**
 * # AC Analysis Results
 *
 * AC analysis produces a set of complex-valued results,
 * along with a single real-valued independent variable, which is always frequency.
 */
export interface AcResult {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Frequency Vector */
  freq: number[];
  /** Ordered signal names and quantities */
  signals: string[];
  /** Primary Data Field. Of length `len(signals) * num_points`. */
  data: ComplexNum[];
  /** Scalar measurement values */
  measurements: { [key: string]: number };
}

export interface AcResult_MeasurementsEntry {
  key: string;
  value: number;
}

/** # Noise Analysis Inputs */
export interface NoiseInput {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Output Signal Name */
  outputP: string;
  /**
   * Output Signal Name, Negative.
   * Optional, defaults to VSS.
   */
  outputN: string;
  /** Input Source Name */
  inputSource: string;
  /** Start (min) frequency in Hz */
  fstart: number;
  /** Stop (max) frequency in Hz */
  fstop: number;
  /** Number of points per interval of frequency sweep. */
  npts: number;
  /** Control Elements */
  ctrls: Control[];
}

/**
 * # Noise Analysis Results
 *
 * Noise analysis produces a set of complex-valued results,
 * along with a single real-valued independent variable, which is always frequency.
 */
export interface NoiseResult {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Ordered signal names and quantities */
  signals: string[];
  /**
   * Primary Data Values
   * Noise values are specified in per-Hz units, i.e. V^2/Hz for voltage noise, A^2/Hz for current noise.
   */
  data: number[];
  /** Integrated noise values, mapped from signal name to value. */
  integratedNoise: { [key: string]: number };
  /** Scalar measurement values */
  measurements: { [key: string]: number };
}

export interface NoiseResult_IntegratedNoiseEntry {
  key: string;
  value: number;
}

export interface NoiseResult_MeasurementsEntry {
  key: string;
  value: number;
}

/**
 * # Sweep
 *
 * The "for loop" of Spice analyses.
 * Defines a scalar variable `var` to be swept, and a set of inner child-analyses
 * to be performed for each value of `var`.
 * `Sweeps` themselves are `Analyses`, and therefore can be arbitrarily nested.
 */
export interface SweepInput {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Sweep-variable name */
  variable: string;
  /** Sweep-values */
  sweep: Sweep | undefined;
  /** Child Analyses */
  an: Analysis[];
  /** Control Elements */
  ctrls: Control[];
}

/** # Sweep Results */
export interface SweepResult {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Sweep-variable name */
  variable: string;
  /** Sweep-values */
  sweep: Sweep | undefined;
  /**
   * Child Analysis Results
   * FIXME: should these just be a flattened list, or organized by sweep-value
   */
  an: AnalysisResult[];
}

/**
 * # Monte Carlo Simulation Input
 *
 * Define a set of child analyses to be simulated across `npts` randomly-generated circuit variations.
 */
export interface MonteInput {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Number of points */
  npts: number;
  /** Random-number seed */
  seed: number;
  /** Child Analyses */
  an: Analysis[];
  /** Control Elements */
  ctrls: Control[];
}

/** # Sweep Results */
export interface MonteResult {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** Sweep-variable name */
  variable: string;
  /** Sweep-values */
  sweep: Sweep | undefined;
  /**
   * Child Analysis Results
   * FIXME: should these just be a flattened list, or organized by iteration
   */
  an: AnalysisResult[];
}

/**
 * # Custom Analysis Input
 *
 * String-defined, non-first-class analysis statement.
 * Primarily for simulator-specific specialty analyses.
 * Note the paired `Result` type is empty,
 * as the schema has no means to comprehend externally-defined
 * analysis data-shapes
 */
export interface CustomAnalysisInput {
  /** (Optional) Analysis Name */
  analysisName: string;
  /** String-literal analysis command */
  cmd: string;
  /** Control Elements */
  ctrls: Control[];
}

/**
 * # Custom Analysis Result
 *
 * Does not return any data. Defined solely for filling slots in lists of analysis-results.
 */
export interface CustomAnalysisResult {}

/** # Sweep Union */
export interface Sweep {
  tp?:
    | { $case: "linear"; linear: LinearSweep }
    | { $case: "log"; log: LogSweep }
    | {
        $case: "points";
        points: PointSweep;
      }
    | undefined;
}

/** # Linear Sweep */
export interface LinearSweep {
  start: number;
  stop: number;
  step: number;
}

/** # Log Sweep */
export interface LogSweep {
  start: number;
  stop: number;
  /** FIXME: move to int */
  npts: number;
}

/** # Enumerated (List of Points) Sweep */
export interface PointSweep {
  points: number[];
  stop: number;
  npts: number;
}

/** / # Control Elements Union */
export interface Control {
  ctrl?:
    | { $case: "include"; include: Include }
    | { $case: "lib"; lib: LibInclude }
    | { $case: "save"; save: Save }
    | { $case: "meas"; meas: Meas }
    | { $case: "param"; param: Param }
    | { $case: "literal"; literal: string }
    | undefined;
}

/** # Signal-Saving Controls */
export interface Save {
  save?:
    | { $case: "mode"; mode: Save_SaveMode }
    | { $case: "signal"; signal: string }
    | undefined;
}

/** Enumerated Modes */
export enum Save_SaveMode {
  NONE = 0,
  ALL = 1,
  UNRECOGNIZED = -1,
}

export function save_SaveModeFromJSON(object: any): Save_SaveMode {
  switch (object) {
    case 0:
    case "NONE":
      return Save_SaveMode.NONE;
    case 1:
    case "ALL":
      return Save_SaveMode.ALL;
    case -1:
    case "UNRECOGNIZED":
    default:
      return Save_SaveMode.UNRECOGNIZED;
  }
}

export function save_SaveModeToJSON(object: Save_SaveMode): string {
  switch (object) {
    case Save_SaveMode.NONE:
      return "NONE";
    case Save_SaveMode.ALL:
      return "ALL";
    case Save_SaveMode.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/** # Include External Content */
export interface Include {
  /**
   * File-system path
   * FIXME: add more methods of specifying this
   */
  path: string;
}

/**
 * # Library "Section" Include
 *
 * Commonly used for "PVT corner" inclusion, in which a single includable file
 * often defines several named "sections", e.g. "TT", "FF", "SS",
 * only one of which at a time may be included in a simulation.
 */
export interface LibInclude {
  /**
   * File-system path
   * FIXME: add more methods of specifying this
   */
  path: string;
  /** Section name */
  section: string;
}

/** # Scalar Measurement */
export interface Meas {
  /** Analysis Name (FIXME: or analysis-type) */
  analysisType: string;
  /** Measurement Name */
  name: string;
  /** Expression to be evaluated */
  expr: string;
}

/**
 * # Signal Declaration
 *
 * Declares a `Signal` name and type for output data.
 */
export interface Signal {
  /** Signal Name */
  name: string;
  quantity: Signal_Quantity;
}

/** Physical Quantity */
export enum Signal_Quantity {
  VOLTAGE = 0,
  CURRENT = 1,
  NONE = 3,
  UNRECOGNIZED = -1,
}

export function signal_QuantityFromJSON(object: any): Signal_Quantity {
  switch (object) {
    case 0:
    case "VOLTAGE":
      return Signal_Quantity.VOLTAGE;
    case 1:
    case "CURRENT":
      return Signal_Quantity.CURRENT;
    case 3:
    case "NONE":
      return Signal_Quantity.NONE;
    case -1:
    case "UNRECOGNIZED":
    default:
      return Signal_Quantity.UNRECOGNIZED;
  }
}

export function signal_QuantityToJSON(object: Signal_Quantity): string {
  switch (object) {
    case Signal_Quantity.VOLTAGE:
      return "VOLTAGE";
    case Signal_Quantity.CURRENT:
      return "CURRENT";
    case Signal_Quantity.NONE:
      return "NONE";
    case Signal_Quantity.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

function createBaseSimInput(): SimInput {
  return { pkg: undefined, top: "", opts: [], an: [], ctrls: [] };
}

export const SimInput = {
  encode(
    message: SimInput,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.pkg !== undefined) {
      Package.encode(message.pkg, writer.uint32(10).fork()).ldelim();
    }
    if (message.top !== "") {
      writer.uint32(18).string(message.top);
    }
    for (const v of message.opts) {
      SimOptions.encode(v!, writer.uint32(82).fork()).ldelim();
    }
    for (const v of message.an) {
      Analysis.encode(v!, writer.uint32(90).fork()).ldelim();
    }
    for (const v of message.ctrls) {
      Control.encode(v!, writer.uint32(98).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): SimInput {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseSimInput();
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

          message.top = reader.string();
          continue;
        case 10:
          if (tag !== 82) {
            break;
          }

          message.opts.push(SimOptions.decode(reader, reader.uint32()));
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.an.push(Analysis.decode(reader, reader.uint32()));
          continue;
        case 12:
          if (tag !== 98) {
            break;
          }

          message.ctrls.push(Control.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): SimInput {
    return {
      pkg: isSet(object.pkg) ? Package.fromJSON(object.pkg) : undefined,
      top: isSet(object.top) ? globalThis.String(object.top) : "",
      opts: globalThis.Array.isArray(object?.opts)
        ? object.opts.map((e: any) => SimOptions.fromJSON(e))
        : [],
      an: globalThis.Array.isArray(object?.an)
        ? object.an.map((e: any) => Analysis.fromJSON(e))
        : [],
      ctrls: globalThis.Array.isArray(object?.ctrls)
        ? object.ctrls.map((e: any) => Control.fromJSON(e))
        : [],
    };
  },

  toJSON(message: SimInput): unknown {
    const obj: any = {};
    if (message.pkg !== undefined) {
      obj.pkg = Package.toJSON(message.pkg);
    }
    if (message.top !== "") {
      obj.top = message.top;
    }
    if (message.opts?.length) {
      obj.opts = message.opts.map((e) => SimOptions.toJSON(e));
    }
    if (message.an?.length) {
      obj.an = message.an.map((e) => Analysis.toJSON(e));
    }
    if (message.ctrls?.length) {
      obj.ctrls = message.ctrls.map((e) => Control.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<SimInput>): SimInput {
    return SimInput.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<SimInput>): SimInput {
    const message = createBaseSimInput();
    message.pkg =
      object.pkg !== undefined && object.pkg !== null
        ? Package.fromPartial(object.pkg)
        : undefined;
    message.top = object.top ?? "";
    message.opts = object.opts?.map((e) => SimOptions.fromPartial(e)) || [];
    message.an = object.an?.map((e) => Analysis.fromPartial(e)) || [];
    message.ctrls = object.ctrls?.map((e) => Control.fromPartial(e)) || [];
    return message;
  },
};

function createBaseSimResult(): SimResult {
  return { an: [] };
}

export const SimResult = {
  encode(
    message: SimResult,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    for (const v of message.an) {
      AnalysisResult.encode(v!, writer.uint32(10).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): SimResult {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseSimResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.an.push(AnalysisResult.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): SimResult {
    return {
      an: globalThis.Array.isArray(object?.an)
        ? object.an.map((e: any) => AnalysisResult.fromJSON(e))
        : [],
    };
  },

  toJSON(message: SimResult): unknown {
    const obj: any = {};
    if (message.an?.length) {
      obj.an = message.an.map((e) => AnalysisResult.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<SimResult>): SimResult {
    return SimResult.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<SimResult>): SimResult {
    const message = createBaseSimResult();
    message.an = object.an?.map((e) => AnalysisResult.fromPartial(e)) || [];
    return message;
  },
};

function createBaseSimOptions(): SimOptions {
  return { name: "", value: undefined };
}

export const SimOptions = {
  encode(
    message: SimOptions,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.value !== undefined) {
      ParamValue.encode(message.value, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): SimOptions {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseSimOptions();
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
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): SimOptions {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      value: isSet(object.value)
        ? ParamValue.fromJSON(object.value)
        : undefined,
    };
  },

  toJSON(message: SimOptions): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.value !== undefined) {
      obj.value = ParamValue.toJSON(message.value);
    }
    return obj;
  },

  create(base?: DeepPartial<SimOptions>): SimOptions {
    return SimOptions.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<SimOptions>): SimOptions {
    const message = createBaseSimOptions();
    message.name = object.name ?? "";
    message.value =
      object.value !== undefined && object.value !== null
        ? ParamValue.fromPartial(object.value)
        : undefined;
    return message;
  },
};

function createBaseAnalysis(): Analysis {
  return { an: undefined };
}

export const Analysis = {
  encode(
    message: Analysis,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    switch (message.an?.$case) {
      case "op":
        OpInput.encode(message.an.op, writer.uint32(10).fork()).ldelim();
        break;
      case "dc":
        DcInput.encode(message.an.dc, writer.uint32(18).fork()).ldelim();
        break;
      case "tran":
        TranInput.encode(message.an.tran, writer.uint32(26).fork()).ldelim();
        break;
      case "ac":
        AcInput.encode(message.an.ac, writer.uint32(34).fork()).ldelim();
        break;
      case "noise":
        NoiseInput.encode(message.an.noise, writer.uint32(42).fork()).ldelim();
        break;
      case "sweep":
        SweepInput.encode(message.an.sweep, writer.uint32(82).fork()).ldelim();
        break;
      case "monte":
        MonteInput.encode(message.an.monte, writer.uint32(90).fork()).ldelim();
        break;
      case "custom":
        CustomAnalysisInput.encode(
          message.an.custom,
          writer.uint32(162).fork(),
        ).ldelim();
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Analysis {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAnalysis();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.an = {
            $case: "op",
            op: OpInput.decode(reader, reader.uint32()),
          };
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.an = {
            $case: "dc",
            dc: DcInput.decode(reader, reader.uint32()),
          };
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.an = {
            $case: "tran",
            tran: TranInput.decode(reader, reader.uint32()),
          };
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.an = {
            $case: "ac",
            ac: AcInput.decode(reader, reader.uint32()),
          };
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.an = {
            $case: "noise",
            noise: NoiseInput.decode(reader, reader.uint32()),
          };
          continue;
        case 10:
          if (tag !== 82) {
            break;
          }

          message.an = {
            $case: "sweep",
            sweep: SweepInput.decode(reader, reader.uint32()),
          };
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.an = {
            $case: "monte",
            monte: MonteInput.decode(reader, reader.uint32()),
          };
          continue;
        case 20:
          if (tag !== 162) {
            break;
          }

          message.an = {
            $case: "custom",
            custom: CustomAnalysisInput.decode(reader, reader.uint32()),
          };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Analysis {
    return {
      an: isSet(object.op)
        ? { $case: "op", op: OpInput.fromJSON(object.op) }
        : isSet(object.dc)
          ? { $case: "dc", dc: DcInput.fromJSON(object.dc) }
          : isSet(object.tran)
            ? { $case: "tran", tran: TranInput.fromJSON(object.tran) }
            : isSet(object.ac)
              ? { $case: "ac", ac: AcInput.fromJSON(object.ac) }
              : isSet(object.noise)
                ? { $case: "noise", noise: NoiseInput.fromJSON(object.noise) }
                : isSet(object.sweep)
                  ? { $case: "sweep", sweep: SweepInput.fromJSON(object.sweep) }
                  : isSet(object.monte)
                    ? {
                        $case: "monte",
                        monte: MonteInput.fromJSON(object.monte),
                      }
                    : isSet(object.custom)
                      ? {
                          $case: "custom",
                          custom: CustomAnalysisInput.fromJSON(object.custom),
                        }
                      : undefined,
    };
  },

  toJSON(message: Analysis): unknown {
    const obj: any = {};
    if (message.an?.$case === "op") {
      obj.op = OpInput.toJSON(message.an.op);
    }
    if (message.an?.$case === "dc") {
      obj.dc = DcInput.toJSON(message.an.dc);
    }
    if (message.an?.$case === "tran") {
      obj.tran = TranInput.toJSON(message.an.tran);
    }
    if (message.an?.$case === "ac") {
      obj.ac = AcInput.toJSON(message.an.ac);
    }
    if (message.an?.$case === "noise") {
      obj.noise = NoiseInput.toJSON(message.an.noise);
    }
    if (message.an?.$case === "sweep") {
      obj.sweep = SweepInput.toJSON(message.an.sweep);
    }
    if (message.an?.$case === "monte") {
      obj.monte = MonteInput.toJSON(message.an.monte);
    }
    if (message.an?.$case === "custom") {
      obj.custom = CustomAnalysisInput.toJSON(message.an.custom);
    }
    return obj;
  },

  create(base?: DeepPartial<Analysis>): Analysis {
    return Analysis.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Analysis>): Analysis {
    const message = createBaseAnalysis();
    if (
      object.an?.$case === "op" &&
      object.an?.op !== undefined &&
      object.an?.op !== null
    ) {
      message.an = { $case: "op", op: OpInput.fromPartial(object.an.op) };
    }
    if (
      object.an?.$case === "dc" &&
      object.an?.dc !== undefined &&
      object.an?.dc !== null
    ) {
      message.an = { $case: "dc", dc: DcInput.fromPartial(object.an.dc) };
    }
    if (
      object.an?.$case === "tran" &&
      object.an?.tran !== undefined &&
      object.an?.tran !== null
    ) {
      message.an = {
        $case: "tran",
        tran: TranInput.fromPartial(object.an.tran),
      };
    }
    if (
      object.an?.$case === "ac" &&
      object.an?.ac !== undefined &&
      object.an?.ac !== null
    ) {
      message.an = { $case: "ac", ac: AcInput.fromPartial(object.an.ac) };
    }
    if (
      object.an?.$case === "noise" &&
      object.an?.noise !== undefined &&
      object.an?.noise !== null
    ) {
      message.an = {
        $case: "noise",
        noise: NoiseInput.fromPartial(object.an.noise),
      };
    }
    if (
      object.an?.$case === "sweep" &&
      object.an?.sweep !== undefined &&
      object.an?.sweep !== null
    ) {
      message.an = {
        $case: "sweep",
        sweep: SweepInput.fromPartial(object.an.sweep),
      };
    }
    if (
      object.an?.$case === "monte" &&
      object.an?.monte !== undefined &&
      object.an?.monte !== null
    ) {
      message.an = {
        $case: "monte",
        monte: MonteInput.fromPartial(object.an.monte),
      };
    }
    if (
      object.an?.$case === "custom" &&
      object.an?.custom !== undefined &&
      object.an?.custom !== null
    ) {
      message.an = {
        $case: "custom",
        custom: CustomAnalysisInput.fromPartial(object.an.custom),
      };
    }
    return message;
  },
};

function createBaseAnalysisResult(): AnalysisResult {
  return { an: undefined };
}

export const AnalysisResult = {
  encode(
    message: AnalysisResult,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    switch (message.an?.$case) {
      case "op":
        OpResult.encode(message.an.op, writer.uint32(10).fork()).ldelim();
        break;
      case "dc":
        DcResult.encode(message.an.dc, writer.uint32(18).fork()).ldelim();
        break;
      case "tran":
        TranResult.encode(message.an.tran, writer.uint32(26).fork()).ldelim();
        break;
      case "ac":
        AcResult.encode(message.an.ac, writer.uint32(34).fork()).ldelim();
        break;
      case "noise":
        NoiseResult.encode(message.an.noise, writer.uint32(42).fork()).ldelim();
        break;
      case "sweep":
        SweepResult.encode(message.an.sweep, writer.uint32(82).fork()).ldelim();
        break;
      case "monte":
        MonteResult.encode(message.an.monte, writer.uint32(90).fork()).ldelim();
        break;
      case "custom":
        CustomAnalysisResult.encode(
          message.an.custom,
          writer.uint32(162).fork(),
        ).ldelim();
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): AnalysisResult {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAnalysisResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.an = {
            $case: "op",
            op: OpResult.decode(reader, reader.uint32()),
          };
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.an = {
            $case: "dc",
            dc: DcResult.decode(reader, reader.uint32()),
          };
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.an = {
            $case: "tran",
            tran: TranResult.decode(reader, reader.uint32()),
          };
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.an = {
            $case: "ac",
            ac: AcResult.decode(reader, reader.uint32()),
          };
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.an = {
            $case: "noise",
            noise: NoiseResult.decode(reader, reader.uint32()),
          };
          continue;
        case 10:
          if (tag !== 82) {
            break;
          }

          message.an = {
            $case: "sweep",
            sweep: SweepResult.decode(reader, reader.uint32()),
          };
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.an = {
            $case: "monte",
            monte: MonteResult.decode(reader, reader.uint32()),
          };
          continue;
        case 20:
          if (tag !== 162) {
            break;
          }

          message.an = {
            $case: "custom",
            custom: CustomAnalysisResult.decode(reader, reader.uint32()),
          };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): AnalysisResult {
    return {
      an: isSet(object.op)
        ? { $case: "op", op: OpResult.fromJSON(object.op) }
        : isSet(object.dc)
          ? { $case: "dc", dc: DcResult.fromJSON(object.dc) }
          : isSet(object.tran)
            ? { $case: "tran", tran: TranResult.fromJSON(object.tran) }
            : isSet(object.ac)
              ? { $case: "ac", ac: AcResult.fromJSON(object.ac) }
              : isSet(object.noise)
                ? { $case: "noise", noise: NoiseResult.fromJSON(object.noise) }
                : isSet(object.sweep)
                  ? {
                      $case: "sweep",
                      sweep: SweepResult.fromJSON(object.sweep),
                    }
                  : isSet(object.monte)
                    ? {
                        $case: "monte",
                        monte: MonteResult.fromJSON(object.monte),
                      }
                    : isSet(object.custom)
                      ? {
                          $case: "custom",
                          custom: CustomAnalysisResult.fromJSON(object.custom),
                        }
                      : undefined,
    };
  },

  toJSON(message: AnalysisResult): unknown {
    const obj: any = {};
    if (message.an?.$case === "op") {
      obj.op = OpResult.toJSON(message.an.op);
    }
    if (message.an?.$case === "dc") {
      obj.dc = DcResult.toJSON(message.an.dc);
    }
    if (message.an?.$case === "tran") {
      obj.tran = TranResult.toJSON(message.an.tran);
    }
    if (message.an?.$case === "ac") {
      obj.ac = AcResult.toJSON(message.an.ac);
    }
    if (message.an?.$case === "noise") {
      obj.noise = NoiseResult.toJSON(message.an.noise);
    }
    if (message.an?.$case === "sweep") {
      obj.sweep = SweepResult.toJSON(message.an.sweep);
    }
    if (message.an?.$case === "monte") {
      obj.monte = MonteResult.toJSON(message.an.monte);
    }
    if (message.an?.$case === "custom") {
      obj.custom = CustomAnalysisResult.toJSON(message.an.custom);
    }
    return obj;
  },

  create(base?: DeepPartial<AnalysisResult>): AnalysisResult {
    return AnalysisResult.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<AnalysisResult>): AnalysisResult {
    const message = createBaseAnalysisResult();
    if (
      object.an?.$case === "op" &&
      object.an?.op !== undefined &&
      object.an?.op !== null
    ) {
      message.an = { $case: "op", op: OpResult.fromPartial(object.an.op) };
    }
    if (
      object.an?.$case === "dc" &&
      object.an?.dc !== undefined &&
      object.an?.dc !== null
    ) {
      message.an = { $case: "dc", dc: DcResult.fromPartial(object.an.dc) };
    }
    if (
      object.an?.$case === "tran" &&
      object.an?.tran !== undefined &&
      object.an?.tran !== null
    ) {
      message.an = {
        $case: "tran",
        tran: TranResult.fromPartial(object.an.tran),
      };
    }
    if (
      object.an?.$case === "ac" &&
      object.an?.ac !== undefined &&
      object.an?.ac !== null
    ) {
      message.an = { $case: "ac", ac: AcResult.fromPartial(object.an.ac) };
    }
    if (
      object.an?.$case === "noise" &&
      object.an?.noise !== undefined &&
      object.an?.noise !== null
    ) {
      message.an = {
        $case: "noise",
        noise: NoiseResult.fromPartial(object.an.noise),
      };
    }
    if (
      object.an?.$case === "sweep" &&
      object.an?.sweep !== undefined &&
      object.an?.sweep !== null
    ) {
      message.an = {
        $case: "sweep",
        sweep: SweepResult.fromPartial(object.an.sweep),
      };
    }
    if (
      object.an?.$case === "monte" &&
      object.an?.monte !== undefined &&
      object.an?.monte !== null
    ) {
      message.an = {
        $case: "monte",
        monte: MonteResult.fromPartial(object.an.monte),
      };
    }
    if (
      object.an?.$case === "custom" &&
      object.an?.custom !== undefined &&
      object.an?.custom !== null
    ) {
      message.an = {
        $case: "custom",
        custom: CustomAnalysisResult.fromPartial(object.an.custom),
      };
    }
    return message;
  },
};

function createBaseOpInput(): OpInput {
  return { analysisName: "", ctrls: [] };
}

export const OpInput = {
  encode(
    message: OpInput,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    for (const v of message.ctrls) {
      Control.encode(v!, writer.uint32(42).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): OpInput {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseOpInput();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.ctrls.push(Control.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): OpInput {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      ctrls: globalThis.Array.isArray(object?.ctrls)
        ? object.ctrls.map((e: any) => Control.fromJSON(e))
        : [],
    };
  },

  toJSON(message: OpInput): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.ctrls?.length) {
      obj.ctrls = message.ctrls.map((e) => Control.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<OpInput>): OpInput {
    return OpInput.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<OpInput>): OpInput {
    const message = createBaseOpInput();
    message.analysisName = object.analysisName ?? "";
    message.ctrls = object.ctrls?.map((e) => Control.fromPartial(e)) || [];
    return message;
  },
};

function createBaseOpResult(): OpResult {
  return { analysisName: "", signals: [], data: [] };
}

export const OpResult = {
  encode(
    message: OpResult,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    for (const v of message.signals) {
      writer.uint32(26).string(v!);
    }
    writer.uint32(42).fork();
    for (const v of message.data) {
      writer.double(v);
    }
    writer.ldelim();
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): OpResult {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseOpResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.signals.push(reader.string());
          continue;
        case 5:
          if (tag === 41) {
            message.data.push(reader.double());

            continue;
          }

          if (tag === 42) {
            const end2 = reader.uint32() + reader.pos;
            while (reader.pos < end2) {
              message.data.push(reader.double());
            }

            continue;
          }

          break;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): OpResult {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      signals: globalThis.Array.isArray(object?.signals)
        ? object.signals.map((e: any) => globalThis.String(e))
        : [],
      data: globalThis.Array.isArray(object?.data)
        ? object.data.map((e: any) => globalThis.Number(e))
        : [],
    };
  },

  toJSON(message: OpResult): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.signals?.length) {
      obj.signals = message.signals;
    }
    if (message.data?.length) {
      obj.data = message.data;
    }
    return obj;
  },

  create(base?: DeepPartial<OpResult>): OpResult {
    return OpResult.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<OpResult>): OpResult {
    const message = createBaseOpResult();
    message.analysisName = object.analysisName ?? "";
    message.signals = object.signals?.map((e) => e) || [];
    message.data = object.data?.map((e) => e) || [];
    return message;
  },
};

function createBaseDcInput(): DcInput {
  return { analysisName: "", indepName: "", sweep: undefined, ctrls: [] };
}

export const DcInput = {
  encode(
    message: DcInput,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    if (message.indepName !== "") {
      writer.uint32(18).string(message.indepName);
    }
    if (message.sweep !== undefined) {
      Sweep.encode(message.sweep, writer.uint32(26).fork()).ldelim();
    }
    for (const v of message.ctrls) {
      Control.encode(v!, writer.uint32(42).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): DcInput {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseDcInput();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.indepName = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.sweep = Sweep.decode(reader, reader.uint32());
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.ctrls.push(Control.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): DcInput {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      indepName: isSet(object.indepName)
        ? globalThis.String(object.indepName)
        : "",
      sweep: isSet(object.sweep) ? Sweep.fromJSON(object.sweep) : undefined,
      ctrls: globalThis.Array.isArray(object?.ctrls)
        ? object.ctrls.map((e: any) => Control.fromJSON(e))
        : [],
    };
  },

  toJSON(message: DcInput): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.indepName !== "") {
      obj.indepName = message.indepName;
    }
    if (message.sweep !== undefined) {
      obj.sweep = Sweep.toJSON(message.sweep);
    }
    if (message.ctrls?.length) {
      obj.ctrls = message.ctrls.map((e) => Control.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<DcInput>): DcInput {
    return DcInput.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<DcInput>): DcInput {
    const message = createBaseDcInput();
    message.analysisName = object.analysisName ?? "";
    message.indepName = object.indepName ?? "";
    message.sweep =
      object.sweep !== undefined && object.sweep !== null
        ? Sweep.fromPartial(object.sweep)
        : undefined;
    message.ctrls = object.ctrls?.map((e) => Control.fromPartial(e)) || [];
    return message;
  },
};

function createBaseDcResult(): DcResult {
  return {
    analysisName: "",
    indepName: "",
    signals: [],
    data: [],
    measurements: {},
  };
}

export const DcResult = {
  encode(
    message: DcResult,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    if (message.indepName !== "") {
      writer.uint32(18).string(message.indepName);
    }
    for (const v of message.signals) {
      writer.uint32(26).string(v!);
    }
    writer.uint32(42).fork();
    for (const v of message.data) {
      writer.double(v);
    }
    writer.ldelim();
    Object.entries(message.measurements).forEach(([key, value]) => {
      DcResult_MeasurementsEntry.encode(
        { key: key as any, value },
        writer.uint32(82).fork(),
      ).ldelim();
    });
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): DcResult {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseDcResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.indepName = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.signals.push(reader.string());
          continue;
        case 5:
          if (tag === 41) {
            message.data.push(reader.double());

            continue;
          }

          if (tag === 42) {
            const end2 = reader.uint32() + reader.pos;
            while (reader.pos < end2) {
              message.data.push(reader.double());
            }

            continue;
          }

          break;
        case 10:
          if (tag !== 82) {
            break;
          }

          const entry10 = DcResult_MeasurementsEntry.decode(
            reader,
            reader.uint32(),
          );
          if (entry10.value !== undefined) {
            message.measurements[entry10.key] = entry10.value;
          }
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): DcResult {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      indepName: isSet(object.indepName)
        ? globalThis.String(object.indepName)
        : "",
      signals: globalThis.Array.isArray(object?.signals)
        ? object.signals.map((e: any) => globalThis.String(e))
        : [],
      data: globalThis.Array.isArray(object?.data)
        ? object.data.map((e: any) => globalThis.Number(e))
        : [],
      measurements: isObject(object.measurements)
        ? Object.entries(object.measurements).reduce<{ [key: string]: number }>(
            (acc, [key, value]) => {
              acc[key] = Number(value);
              return acc;
            },
            {},
          )
        : {},
    };
  },

  toJSON(message: DcResult): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.indepName !== "") {
      obj.indepName = message.indepName;
    }
    if (message.signals?.length) {
      obj.signals = message.signals;
    }
    if (message.data?.length) {
      obj.data = message.data;
    }
    if (message.measurements) {
      const entries = Object.entries(message.measurements);
      if (entries.length > 0) {
        obj.measurements = {};
        entries.forEach(([k, v]) => {
          obj.measurements[k] = v;
        });
      }
    }
    return obj;
  },

  create(base?: DeepPartial<DcResult>): DcResult {
    return DcResult.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<DcResult>): DcResult {
    const message = createBaseDcResult();
    message.analysisName = object.analysisName ?? "";
    message.indepName = object.indepName ?? "";
    message.signals = object.signals?.map((e) => e) || [];
    message.data = object.data?.map((e) => e) || [];
    message.measurements = Object.entries(object.measurements ?? {}).reduce<{
      [key: string]: number;
    }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = globalThis.Number(value);
      }
      return acc;
    }, {});
    return message;
  },
};

function createBaseDcResult_MeasurementsEntry(): DcResult_MeasurementsEntry {
  return { key: "", value: 0 };
}

export const DcResult_MeasurementsEntry = {
  encode(
    message: DcResult_MeasurementsEntry,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== 0) {
      writer.uint32(17).double(message.value);
    }
    return writer;
  },

  decode(
    input: _m0.Reader | Uint8Array,
    length?: number,
  ): DcResult_MeasurementsEntry {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseDcResult_MeasurementsEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.key = reader.string();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.value = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): DcResult_MeasurementsEntry {
    return {
      key: isSet(object.key) ? globalThis.String(object.key) : "",
      value: isSet(object.value) ? globalThis.Number(object.value) : 0,
    };
  },

  toJSON(message: DcResult_MeasurementsEntry): unknown {
    const obj: any = {};
    if (message.key !== "") {
      obj.key = message.key;
    }
    if (message.value !== 0) {
      obj.value = message.value;
    }
    return obj;
  },

  create(
    base?: DeepPartial<DcResult_MeasurementsEntry>,
  ): DcResult_MeasurementsEntry {
    return DcResult_MeasurementsEntry.fromPartial(base ?? {});
  },
  fromPartial(
    object: DeepPartial<DcResult_MeasurementsEntry>,
  ): DcResult_MeasurementsEntry {
    const message = createBaseDcResult_MeasurementsEntry();
    message.key = object.key ?? "";
    message.value = object.value ?? 0;
    return message;
  },
};

function createBaseTranInput(): TranInput {
  return { analysisName: "", tstop: 0, tstep: 0, ic: {}, ctrls: [] };
}

export const TranInput = {
  encode(
    message: TranInput,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    if (message.tstop !== 0) {
      writer.uint32(17).double(message.tstop);
    }
    if (message.tstep !== 0) {
      writer.uint32(25).double(message.tstep);
    }
    Object.entries(message.ic).forEach(([key, value]) => {
      TranInput_IcEntry.encode(
        { key: key as any, value },
        writer.uint32(34).fork(),
      ).ldelim();
    });
    for (const v of message.ctrls) {
      Control.encode(v!, writer.uint32(42).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): TranInput {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTranInput();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.tstop = reader.double();
          continue;
        case 3:
          if (tag !== 25) {
            break;
          }

          message.tstep = reader.double();
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          const entry4 = TranInput_IcEntry.decode(reader, reader.uint32());
          if (entry4.value !== undefined) {
            message.ic[entry4.key] = entry4.value;
          }
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.ctrls.push(Control.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): TranInput {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      tstop: isSet(object.tstop) ? globalThis.Number(object.tstop) : 0,
      tstep: isSet(object.tstep) ? globalThis.Number(object.tstep) : 0,
      ic: isObject(object.ic)
        ? Object.entries(object.ic).reduce<{ [key: string]: number }>(
            (acc, [key, value]) => {
              acc[key] = Number(value);
              return acc;
            },
            {},
          )
        : {},
      ctrls: globalThis.Array.isArray(object?.ctrls)
        ? object.ctrls.map((e: any) => Control.fromJSON(e))
        : [],
    };
  },

  toJSON(message: TranInput): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.tstop !== 0) {
      obj.tstop = message.tstop;
    }
    if (message.tstep !== 0) {
      obj.tstep = message.tstep;
    }
    if (message.ic) {
      const entries = Object.entries(message.ic);
      if (entries.length > 0) {
        obj.ic = {};
        entries.forEach(([k, v]) => {
          obj.ic[k] = v;
        });
      }
    }
    if (message.ctrls?.length) {
      obj.ctrls = message.ctrls.map((e) => Control.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<TranInput>): TranInput {
    return TranInput.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<TranInput>): TranInput {
    const message = createBaseTranInput();
    message.analysisName = object.analysisName ?? "";
    message.tstop = object.tstop ?? 0;
    message.tstep = object.tstep ?? 0;
    message.ic = Object.entries(object.ic ?? {}).reduce<{
      [key: string]: number;
    }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = globalThis.Number(value);
      }
      return acc;
    }, {});
    message.ctrls = object.ctrls?.map((e) => Control.fromPartial(e)) || [];
    return message;
  },
};

function createBaseTranInput_IcEntry(): TranInput_IcEntry {
  return { key: "", value: 0 };
}

export const TranInput_IcEntry = {
  encode(
    message: TranInput_IcEntry,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== 0) {
      writer.uint32(17).double(message.value);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): TranInput_IcEntry {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTranInput_IcEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.key = reader.string();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.value = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): TranInput_IcEntry {
    return {
      key: isSet(object.key) ? globalThis.String(object.key) : "",
      value: isSet(object.value) ? globalThis.Number(object.value) : 0,
    };
  },

  toJSON(message: TranInput_IcEntry): unknown {
    const obj: any = {};
    if (message.key !== "") {
      obj.key = message.key;
    }
    if (message.value !== 0) {
      obj.value = message.value;
    }
    return obj;
  },

  create(base?: DeepPartial<TranInput_IcEntry>): TranInput_IcEntry {
    return TranInput_IcEntry.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<TranInput_IcEntry>): TranInput_IcEntry {
    const message = createBaseTranInput_IcEntry();
    message.key = object.key ?? "";
    message.value = object.value ?? 0;
    return message;
  },
};

function createBaseTranResult(): TranResult {
  return { analysisName: "", signals: [], data: [], measurements: {} };
}

export const TranResult = {
  encode(
    message: TranResult,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    for (const v of message.signals) {
      writer.uint32(26).string(v!);
    }
    writer.uint32(42).fork();
    for (const v of message.data) {
      writer.double(v);
    }
    writer.ldelim();
    Object.entries(message.measurements).forEach(([key, value]) => {
      TranResult_MeasurementsEntry.encode(
        { key: key as any, value },
        writer.uint32(82).fork(),
      ).ldelim();
    });
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): TranResult {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTranResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.signals.push(reader.string());
          continue;
        case 5:
          if (tag === 41) {
            message.data.push(reader.double());

            continue;
          }

          if (tag === 42) {
            const end2 = reader.uint32() + reader.pos;
            while (reader.pos < end2) {
              message.data.push(reader.double());
            }

            continue;
          }

          break;
        case 10:
          if (tag !== 82) {
            break;
          }

          const entry10 = TranResult_MeasurementsEntry.decode(
            reader,
            reader.uint32(),
          );
          if (entry10.value !== undefined) {
            message.measurements[entry10.key] = entry10.value;
          }
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): TranResult {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      signals: globalThis.Array.isArray(object?.signals)
        ? object.signals.map((e: any) => globalThis.String(e))
        : [],
      data: globalThis.Array.isArray(object?.data)
        ? object.data.map((e: any) => globalThis.Number(e))
        : [],
      measurements: isObject(object.measurements)
        ? Object.entries(object.measurements).reduce<{ [key: string]: number }>(
            (acc, [key, value]) => {
              acc[key] = Number(value);
              return acc;
            },
            {},
          )
        : {},
    };
  },

  toJSON(message: TranResult): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.signals?.length) {
      obj.signals = message.signals;
    }
    if (message.data?.length) {
      obj.data = message.data;
    }
    if (message.measurements) {
      const entries = Object.entries(message.measurements);
      if (entries.length > 0) {
        obj.measurements = {};
        entries.forEach(([k, v]) => {
          obj.measurements[k] = v;
        });
      }
    }
    return obj;
  },

  create(base?: DeepPartial<TranResult>): TranResult {
    return TranResult.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<TranResult>): TranResult {
    const message = createBaseTranResult();
    message.analysisName = object.analysisName ?? "";
    message.signals = object.signals?.map((e) => e) || [];
    message.data = object.data?.map((e) => e) || [];
    message.measurements = Object.entries(object.measurements ?? {}).reduce<{
      [key: string]: number;
    }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = globalThis.Number(value);
      }
      return acc;
    }, {});
    return message;
  },
};

function createBaseTranResult_MeasurementsEntry(): TranResult_MeasurementsEntry {
  return { key: "", value: 0 };
}

export const TranResult_MeasurementsEntry = {
  encode(
    message: TranResult_MeasurementsEntry,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== 0) {
      writer.uint32(17).double(message.value);
    }
    return writer;
  },

  decode(
    input: _m0.Reader | Uint8Array,
    length?: number,
  ): TranResult_MeasurementsEntry {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTranResult_MeasurementsEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.key = reader.string();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.value = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): TranResult_MeasurementsEntry {
    return {
      key: isSet(object.key) ? globalThis.String(object.key) : "",
      value: isSet(object.value) ? globalThis.Number(object.value) : 0,
    };
  },

  toJSON(message: TranResult_MeasurementsEntry): unknown {
    const obj: any = {};
    if (message.key !== "") {
      obj.key = message.key;
    }
    if (message.value !== 0) {
      obj.value = message.value;
    }
    return obj;
  },

  create(
    base?: DeepPartial<TranResult_MeasurementsEntry>,
  ): TranResult_MeasurementsEntry {
    return TranResult_MeasurementsEntry.fromPartial(base ?? {});
  },
  fromPartial(
    object: DeepPartial<TranResult_MeasurementsEntry>,
  ): TranResult_MeasurementsEntry {
    const message = createBaseTranResult_MeasurementsEntry();
    message.key = object.key ?? "";
    message.value = object.value ?? 0;
    return message;
  },
};

function createBaseComplexNum(): ComplexNum {
  return { re: 0, im: 0 };
}

export const ComplexNum = {
  encode(
    message: ComplexNum,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.re !== 0) {
      writer.uint32(9).double(message.re);
    }
    if (message.im !== 0) {
      writer.uint32(17).double(message.im);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): ComplexNum {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseComplexNum();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 9) {
            break;
          }

          message.re = reader.double();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.im = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): ComplexNum {
    return {
      re: isSet(object.re) ? globalThis.Number(object.re) : 0,
      im: isSet(object.im) ? globalThis.Number(object.im) : 0,
    };
  },

  toJSON(message: ComplexNum): unknown {
    const obj: any = {};
    if (message.re !== 0) {
      obj.re = message.re;
    }
    if (message.im !== 0) {
      obj.im = message.im;
    }
    return obj;
  },

  create(base?: DeepPartial<ComplexNum>): ComplexNum {
    return ComplexNum.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<ComplexNum>): ComplexNum {
    const message = createBaseComplexNum();
    message.re = object.re ?? 0;
    message.im = object.im ?? 0;
    return message;
  },
};

function createBaseAcInput(): AcInput {
  return { analysisName: "", fstart: 0, fstop: 0, npts: 0, ctrls: [] };
}

export const AcInput = {
  encode(
    message: AcInput,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    if (message.fstart !== 0) {
      writer.uint32(17).double(message.fstart);
    }
    if (message.fstop !== 0) {
      writer.uint32(25).double(message.fstop);
    }
    if (message.npts !== 0) {
      writer.uint32(32).uint64(message.npts);
    }
    for (const v of message.ctrls) {
      Control.encode(v!, writer.uint32(42).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): AcInput {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAcInput();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.fstart = reader.double();
          continue;
        case 3:
          if (tag !== 25) {
            break;
          }

          message.fstop = reader.double();
          continue;
        case 4:
          if (tag !== 32) {
            break;
          }

          message.npts = longToNumber(reader.uint64() as Long);
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.ctrls.push(Control.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): AcInput {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      fstart: isSet(object.fstart) ? globalThis.Number(object.fstart) : 0,
      fstop: isSet(object.fstop) ? globalThis.Number(object.fstop) : 0,
      npts: isSet(object.npts) ? globalThis.Number(object.npts) : 0,
      ctrls: globalThis.Array.isArray(object?.ctrls)
        ? object.ctrls.map((e: any) => Control.fromJSON(e))
        : [],
    };
  },

  toJSON(message: AcInput): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.fstart !== 0) {
      obj.fstart = message.fstart;
    }
    if (message.fstop !== 0) {
      obj.fstop = message.fstop;
    }
    if (message.npts !== 0) {
      obj.npts = Math.round(message.npts);
    }
    if (message.ctrls?.length) {
      obj.ctrls = message.ctrls.map((e) => Control.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<AcInput>): AcInput {
    return AcInput.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<AcInput>): AcInput {
    const message = createBaseAcInput();
    message.analysisName = object.analysisName ?? "";
    message.fstart = object.fstart ?? 0;
    message.fstop = object.fstop ?? 0;
    message.npts = object.npts ?? 0;
    message.ctrls = object.ctrls?.map((e) => Control.fromPartial(e)) || [];
    return message;
  },
};

function createBaseAcResult(): AcResult {
  return {
    analysisName: "",
    freq: [],
    signals: [],
    data: [],
    measurements: {},
  };
}

export const AcResult = {
  encode(
    message: AcResult,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    writer.uint32(18).fork();
    for (const v of message.freq) {
      writer.double(v);
    }
    writer.ldelim();
    for (const v of message.signals) {
      writer.uint32(26).string(v!);
    }
    for (const v of message.data) {
      ComplexNum.encode(v!, writer.uint32(42).fork()).ldelim();
    }
    Object.entries(message.measurements).forEach(([key, value]) => {
      AcResult_MeasurementsEntry.encode(
        { key: key as any, value },
        writer.uint32(82).fork(),
      ).ldelim();
    });
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): AcResult {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAcResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag === 17) {
            message.freq.push(reader.double());

            continue;
          }

          if (tag === 18) {
            const end2 = reader.uint32() + reader.pos;
            while (reader.pos < end2) {
              message.freq.push(reader.double());
            }

            continue;
          }

          break;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.signals.push(reader.string());
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.data.push(ComplexNum.decode(reader, reader.uint32()));
          continue;
        case 10:
          if (tag !== 82) {
            break;
          }

          const entry10 = AcResult_MeasurementsEntry.decode(
            reader,
            reader.uint32(),
          );
          if (entry10.value !== undefined) {
            message.measurements[entry10.key] = entry10.value;
          }
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): AcResult {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      freq: globalThis.Array.isArray(object?.freq)
        ? object.freq.map((e: any) => globalThis.Number(e))
        : [],
      signals: globalThis.Array.isArray(object?.signals)
        ? object.signals.map((e: any) => globalThis.String(e))
        : [],
      data: globalThis.Array.isArray(object?.data)
        ? object.data.map((e: any) => ComplexNum.fromJSON(e))
        : [],
      measurements: isObject(object.measurements)
        ? Object.entries(object.measurements).reduce<{ [key: string]: number }>(
            (acc, [key, value]) => {
              acc[key] = Number(value);
              return acc;
            },
            {},
          )
        : {},
    };
  },

  toJSON(message: AcResult): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.freq?.length) {
      obj.freq = message.freq;
    }
    if (message.signals?.length) {
      obj.signals = message.signals;
    }
    if (message.data?.length) {
      obj.data = message.data.map((e) => ComplexNum.toJSON(e));
    }
    if (message.measurements) {
      const entries = Object.entries(message.measurements);
      if (entries.length > 0) {
        obj.measurements = {};
        entries.forEach(([k, v]) => {
          obj.measurements[k] = v;
        });
      }
    }
    return obj;
  },

  create(base?: DeepPartial<AcResult>): AcResult {
    return AcResult.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<AcResult>): AcResult {
    const message = createBaseAcResult();
    message.analysisName = object.analysisName ?? "";
    message.freq = object.freq?.map((e) => e) || [];
    message.signals = object.signals?.map((e) => e) || [];
    message.data = object.data?.map((e) => ComplexNum.fromPartial(e)) || [];
    message.measurements = Object.entries(object.measurements ?? {}).reduce<{
      [key: string]: number;
    }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = globalThis.Number(value);
      }
      return acc;
    }, {});
    return message;
  },
};

function createBaseAcResult_MeasurementsEntry(): AcResult_MeasurementsEntry {
  return { key: "", value: 0 };
}

export const AcResult_MeasurementsEntry = {
  encode(
    message: AcResult_MeasurementsEntry,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== 0) {
      writer.uint32(17).double(message.value);
    }
    return writer;
  },

  decode(
    input: _m0.Reader | Uint8Array,
    length?: number,
  ): AcResult_MeasurementsEntry {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAcResult_MeasurementsEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.key = reader.string();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.value = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): AcResult_MeasurementsEntry {
    return {
      key: isSet(object.key) ? globalThis.String(object.key) : "",
      value: isSet(object.value) ? globalThis.Number(object.value) : 0,
    };
  },

  toJSON(message: AcResult_MeasurementsEntry): unknown {
    const obj: any = {};
    if (message.key !== "") {
      obj.key = message.key;
    }
    if (message.value !== 0) {
      obj.value = message.value;
    }
    return obj;
  },

  create(
    base?: DeepPartial<AcResult_MeasurementsEntry>,
  ): AcResult_MeasurementsEntry {
    return AcResult_MeasurementsEntry.fromPartial(base ?? {});
  },
  fromPartial(
    object: DeepPartial<AcResult_MeasurementsEntry>,
  ): AcResult_MeasurementsEntry {
    const message = createBaseAcResult_MeasurementsEntry();
    message.key = object.key ?? "";
    message.value = object.value ?? 0;
    return message;
  },
};

function createBaseNoiseInput(): NoiseInput {
  return {
    analysisName: "",
    outputP: "",
    outputN: "",
    inputSource: "",
    fstart: 0,
    fstop: 0,
    npts: 0,
    ctrls: [],
  };
}

export const NoiseInput = {
  encode(
    message: NoiseInput,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    if (message.outputP !== "") {
      writer.uint32(18).string(message.outputP);
    }
    if (message.outputN !== "") {
      writer.uint32(26).string(message.outputN);
    }
    if (message.inputSource !== "") {
      writer.uint32(34).string(message.inputSource);
    }
    if (message.fstart !== 0) {
      writer.uint32(81).double(message.fstart);
    }
    if (message.fstop !== 0) {
      writer.uint32(89).double(message.fstop);
    }
    if (message.npts !== 0) {
      writer.uint32(96).uint64(message.npts);
    }
    for (const v of message.ctrls) {
      Control.encode(v!, writer.uint32(162).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): NoiseInput {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseNoiseInput();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.outputP = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.outputN = reader.string();
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.inputSource = reader.string();
          continue;
        case 10:
          if (tag !== 81) {
            break;
          }

          message.fstart = reader.double();
          continue;
        case 11:
          if (tag !== 89) {
            break;
          }

          message.fstop = reader.double();
          continue;
        case 12:
          if (tag !== 96) {
            break;
          }

          message.npts = longToNumber(reader.uint64() as Long);
          continue;
        case 20:
          if (tag !== 162) {
            break;
          }

          message.ctrls.push(Control.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): NoiseInput {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      outputP: isSet(object.outputP) ? globalThis.String(object.outputP) : "",
      outputN: isSet(object.outputN) ? globalThis.String(object.outputN) : "",
      inputSource: isSet(object.inputSource)
        ? globalThis.String(object.inputSource)
        : "",
      fstart: isSet(object.fstart) ? globalThis.Number(object.fstart) : 0,
      fstop: isSet(object.fstop) ? globalThis.Number(object.fstop) : 0,
      npts: isSet(object.npts) ? globalThis.Number(object.npts) : 0,
      ctrls: globalThis.Array.isArray(object?.ctrls)
        ? object.ctrls.map((e: any) => Control.fromJSON(e))
        : [],
    };
  },

  toJSON(message: NoiseInput): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.outputP !== "") {
      obj.outputP = message.outputP;
    }
    if (message.outputN !== "") {
      obj.outputN = message.outputN;
    }
    if (message.inputSource !== "") {
      obj.inputSource = message.inputSource;
    }
    if (message.fstart !== 0) {
      obj.fstart = message.fstart;
    }
    if (message.fstop !== 0) {
      obj.fstop = message.fstop;
    }
    if (message.npts !== 0) {
      obj.npts = Math.round(message.npts);
    }
    if (message.ctrls?.length) {
      obj.ctrls = message.ctrls.map((e) => Control.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<NoiseInput>): NoiseInput {
    return NoiseInput.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<NoiseInput>): NoiseInput {
    const message = createBaseNoiseInput();
    message.analysisName = object.analysisName ?? "";
    message.outputP = object.outputP ?? "";
    message.outputN = object.outputN ?? "";
    message.inputSource = object.inputSource ?? "";
    message.fstart = object.fstart ?? 0;
    message.fstop = object.fstop ?? 0;
    message.npts = object.npts ?? 0;
    message.ctrls = object.ctrls?.map((e) => Control.fromPartial(e)) || [];
    return message;
  },
};

function createBaseNoiseResult(): NoiseResult {
  return {
    analysisName: "",
    signals: [],
    data: [],
    integratedNoise: {},
    measurements: {},
  };
}

export const NoiseResult = {
  encode(
    message: NoiseResult,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    for (const v of message.signals) {
      writer.uint32(26).string(v!);
    }
    writer.uint32(42).fork();
    for (const v of message.data) {
      writer.double(v);
    }
    writer.ldelim();
    Object.entries(message.integratedNoise).forEach(([key, value]) => {
      NoiseResult_IntegratedNoiseEntry.encode(
        { key: key as any, value },
        writer.uint32(82).fork(),
      ).ldelim();
    });
    Object.entries(message.measurements).forEach(([key, value]) => {
      NoiseResult_MeasurementsEntry.encode(
        { key: key as any, value },
        writer.uint32(90).fork(),
      ).ldelim();
    });
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): NoiseResult {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseNoiseResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.signals.push(reader.string());
          continue;
        case 5:
          if (tag === 41) {
            message.data.push(reader.double());

            continue;
          }

          if (tag === 42) {
            const end2 = reader.uint32() + reader.pos;
            while (reader.pos < end2) {
              message.data.push(reader.double());
            }

            continue;
          }

          break;
        case 10:
          if (tag !== 82) {
            break;
          }

          const entry10 = NoiseResult_IntegratedNoiseEntry.decode(
            reader,
            reader.uint32(),
          );
          if (entry10.value !== undefined) {
            message.integratedNoise[entry10.key] = entry10.value;
          }
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          const entry11 = NoiseResult_MeasurementsEntry.decode(
            reader,
            reader.uint32(),
          );
          if (entry11.value !== undefined) {
            message.measurements[entry11.key] = entry11.value;
          }
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): NoiseResult {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      signals: globalThis.Array.isArray(object?.signals)
        ? object.signals.map((e: any) => globalThis.String(e))
        : [],
      data: globalThis.Array.isArray(object?.data)
        ? object.data.map((e: any) => globalThis.Number(e))
        : [],
      integratedNoise: isObject(object.integratedNoise)
        ? Object.entries(object.integratedNoise).reduce<{
            [key: string]: number;
          }>((acc, [key, value]) => {
            acc[key] = Number(value);
            return acc;
          }, {})
        : {},
      measurements: isObject(object.measurements)
        ? Object.entries(object.measurements).reduce<{ [key: string]: number }>(
            (acc, [key, value]) => {
              acc[key] = Number(value);
              return acc;
            },
            {},
          )
        : {},
    };
  },

  toJSON(message: NoiseResult): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.signals?.length) {
      obj.signals = message.signals;
    }
    if (message.data?.length) {
      obj.data = message.data;
    }
    if (message.integratedNoise) {
      const entries = Object.entries(message.integratedNoise);
      if (entries.length > 0) {
        obj.integratedNoise = {};
        entries.forEach(([k, v]) => {
          obj.integratedNoise[k] = v;
        });
      }
    }
    if (message.measurements) {
      const entries = Object.entries(message.measurements);
      if (entries.length > 0) {
        obj.measurements = {};
        entries.forEach(([k, v]) => {
          obj.measurements[k] = v;
        });
      }
    }
    return obj;
  },

  create(base?: DeepPartial<NoiseResult>): NoiseResult {
    return NoiseResult.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<NoiseResult>): NoiseResult {
    const message = createBaseNoiseResult();
    message.analysisName = object.analysisName ?? "";
    message.signals = object.signals?.map((e) => e) || [];
    message.data = object.data?.map((e) => e) || [];
    message.integratedNoise = Object.entries(
      object.integratedNoise ?? {},
    ).reduce<{ [key: string]: number }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = globalThis.Number(value);
      }
      return acc;
    }, {});
    message.measurements = Object.entries(object.measurements ?? {}).reduce<{
      [key: string]: number;
    }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = globalThis.Number(value);
      }
      return acc;
    }, {});
    return message;
  },
};

function createBaseNoiseResult_IntegratedNoiseEntry(): NoiseResult_IntegratedNoiseEntry {
  return { key: "", value: 0 };
}

export const NoiseResult_IntegratedNoiseEntry = {
  encode(
    message: NoiseResult_IntegratedNoiseEntry,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== 0) {
      writer.uint32(17).double(message.value);
    }
    return writer;
  },

  decode(
    input: _m0.Reader | Uint8Array,
    length?: number,
  ): NoiseResult_IntegratedNoiseEntry {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseNoiseResult_IntegratedNoiseEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.key = reader.string();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.value = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): NoiseResult_IntegratedNoiseEntry {
    return {
      key: isSet(object.key) ? globalThis.String(object.key) : "",
      value: isSet(object.value) ? globalThis.Number(object.value) : 0,
    };
  },

  toJSON(message: NoiseResult_IntegratedNoiseEntry): unknown {
    const obj: any = {};
    if (message.key !== "") {
      obj.key = message.key;
    }
    if (message.value !== 0) {
      obj.value = message.value;
    }
    return obj;
  },

  create(
    base?: DeepPartial<NoiseResult_IntegratedNoiseEntry>,
  ): NoiseResult_IntegratedNoiseEntry {
    return NoiseResult_IntegratedNoiseEntry.fromPartial(base ?? {});
  },
  fromPartial(
    object: DeepPartial<NoiseResult_IntegratedNoiseEntry>,
  ): NoiseResult_IntegratedNoiseEntry {
    const message = createBaseNoiseResult_IntegratedNoiseEntry();
    message.key = object.key ?? "";
    message.value = object.value ?? 0;
    return message;
  },
};

function createBaseNoiseResult_MeasurementsEntry(): NoiseResult_MeasurementsEntry {
  return { key: "", value: 0 };
}

export const NoiseResult_MeasurementsEntry = {
  encode(
    message: NoiseResult_MeasurementsEntry,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== 0) {
      writer.uint32(17).double(message.value);
    }
    return writer;
  },

  decode(
    input: _m0.Reader | Uint8Array,
    length?: number,
  ): NoiseResult_MeasurementsEntry {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseNoiseResult_MeasurementsEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.key = reader.string();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.value = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): NoiseResult_MeasurementsEntry {
    return {
      key: isSet(object.key) ? globalThis.String(object.key) : "",
      value: isSet(object.value) ? globalThis.Number(object.value) : 0,
    };
  },

  toJSON(message: NoiseResult_MeasurementsEntry): unknown {
    const obj: any = {};
    if (message.key !== "") {
      obj.key = message.key;
    }
    if (message.value !== 0) {
      obj.value = message.value;
    }
    return obj;
  },

  create(
    base?: DeepPartial<NoiseResult_MeasurementsEntry>,
  ): NoiseResult_MeasurementsEntry {
    return NoiseResult_MeasurementsEntry.fromPartial(base ?? {});
  },
  fromPartial(
    object: DeepPartial<NoiseResult_MeasurementsEntry>,
  ): NoiseResult_MeasurementsEntry {
    const message = createBaseNoiseResult_MeasurementsEntry();
    message.key = object.key ?? "";
    message.value = object.value ?? 0;
    return message;
  },
};

function createBaseSweepInput(): SweepInput {
  return {
    analysisName: "",
    variable: "",
    sweep: undefined,
    an: [],
    ctrls: [],
  };
}

export const SweepInput = {
  encode(
    message: SweepInput,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    if (message.variable !== "") {
      writer.uint32(18).string(message.variable);
    }
    if (message.sweep !== undefined) {
      Sweep.encode(message.sweep, writer.uint32(26).fork()).ldelim();
    }
    for (const v of message.an) {
      Analysis.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    for (const v of message.ctrls) {
      Control.encode(v!, writer.uint32(42).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): SweepInput {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseSweepInput();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.variable = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.sweep = Sweep.decode(reader, reader.uint32());
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.an.push(Analysis.decode(reader, reader.uint32()));
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.ctrls.push(Control.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): SweepInput {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      variable: isSet(object.variable)
        ? globalThis.String(object.variable)
        : "",
      sweep: isSet(object.sweep) ? Sweep.fromJSON(object.sweep) : undefined,
      an: globalThis.Array.isArray(object?.an)
        ? object.an.map((e: any) => Analysis.fromJSON(e))
        : [],
      ctrls: globalThis.Array.isArray(object?.ctrls)
        ? object.ctrls.map((e: any) => Control.fromJSON(e))
        : [],
    };
  },

  toJSON(message: SweepInput): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.variable !== "") {
      obj.variable = message.variable;
    }
    if (message.sweep !== undefined) {
      obj.sweep = Sweep.toJSON(message.sweep);
    }
    if (message.an?.length) {
      obj.an = message.an.map((e) => Analysis.toJSON(e));
    }
    if (message.ctrls?.length) {
      obj.ctrls = message.ctrls.map((e) => Control.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<SweepInput>): SweepInput {
    return SweepInput.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<SweepInput>): SweepInput {
    const message = createBaseSweepInput();
    message.analysisName = object.analysisName ?? "";
    message.variable = object.variable ?? "";
    message.sweep =
      object.sweep !== undefined && object.sweep !== null
        ? Sweep.fromPartial(object.sweep)
        : undefined;
    message.an = object.an?.map((e) => Analysis.fromPartial(e)) || [];
    message.ctrls = object.ctrls?.map((e) => Control.fromPartial(e)) || [];
    return message;
  },
};

function createBaseSweepResult(): SweepResult {
  return { analysisName: "", variable: "", sweep: undefined, an: [] };
}

export const SweepResult = {
  encode(
    message: SweepResult,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    if (message.variable !== "") {
      writer.uint32(18).string(message.variable);
    }
    if (message.sweep !== undefined) {
      Sweep.encode(message.sweep, writer.uint32(26).fork()).ldelim();
    }
    for (const v of message.an) {
      AnalysisResult.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): SweepResult {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseSweepResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.variable = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.sweep = Sweep.decode(reader, reader.uint32());
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.an.push(AnalysisResult.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): SweepResult {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      variable: isSet(object.variable)
        ? globalThis.String(object.variable)
        : "",
      sweep: isSet(object.sweep) ? Sweep.fromJSON(object.sweep) : undefined,
      an: globalThis.Array.isArray(object?.an)
        ? object.an.map((e: any) => AnalysisResult.fromJSON(e))
        : [],
    };
  },

  toJSON(message: SweepResult): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.variable !== "") {
      obj.variable = message.variable;
    }
    if (message.sweep !== undefined) {
      obj.sweep = Sweep.toJSON(message.sweep);
    }
    if (message.an?.length) {
      obj.an = message.an.map((e) => AnalysisResult.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<SweepResult>): SweepResult {
    return SweepResult.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<SweepResult>): SweepResult {
    const message = createBaseSweepResult();
    message.analysisName = object.analysisName ?? "";
    message.variable = object.variable ?? "";
    message.sweep =
      object.sweep !== undefined && object.sweep !== null
        ? Sweep.fromPartial(object.sweep)
        : undefined;
    message.an = object.an?.map((e) => AnalysisResult.fromPartial(e)) || [];
    return message;
  },
};

function createBaseMonteInput(): MonteInput {
  return { analysisName: "", npts: 0, seed: 0, an: [], ctrls: [] };
}

export const MonteInput = {
  encode(
    message: MonteInput,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    if (message.npts !== 0) {
      writer.uint32(16).int64(message.npts);
    }
    if (message.seed !== 0) {
      writer.uint32(24).int64(message.seed);
    }
    for (const v of message.an) {
      Analysis.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    for (const v of message.ctrls) {
      Control.encode(v!, writer.uint32(42).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): MonteInput {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseMonteInput();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.npts = longToNumber(reader.int64() as Long);
          continue;
        case 3:
          if (tag !== 24) {
            break;
          }

          message.seed = longToNumber(reader.int64() as Long);
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.an.push(Analysis.decode(reader, reader.uint32()));
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.ctrls.push(Control.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): MonteInput {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      npts: isSet(object.npts) ? globalThis.Number(object.npts) : 0,
      seed: isSet(object.seed) ? globalThis.Number(object.seed) : 0,
      an: globalThis.Array.isArray(object?.an)
        ? object.an.map((e: any) => Analysis.fromJSON(e))
        : [],
      ctrls: globalThis.Array.isArray(object?.ctrls)
        ? object.ctrls.map((e: any) => Control.fromJSON(e))
        : [],
    };
  },

  toJSON(message: MonteInput): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.npts !== 0) {
      obj.npts = Math.round(message.npts);
    }
    if (message.seed !== 0) {
      obj.seed = Math.round(message.seed);
    }
    if (message.an?.length) {
      obj.an = message.an.map((e) => Analysis.toJSON(e));
    }
    if (message.ctrls?.length) {
      obj.ctrls = message.ctrls.map((e) => Control.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<MonteInput>): MonteInput {
    return MonteInput.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<MonteInput>): MonteInput {
    const message = createBaseMonteInput();
    message.analysisName = object.analysisName ?? "";
    message.npts = object.npts ?? 0;
    message.seed = object.seed ?? 0;
    message.an = object.an?.map((e) => Analysis.fromPartial(e)) || [];
    message.ctrls = object.ctrls?.map((e) => Control.fromPartial(e)) || [];
    return message;
  },
};

function createBaseMonteResult(): MonteResult {
  return { analysisName: "", variable: "", sweep: undefined, an: [] };
}

export const MonteResult = {
  encode(
    message: MonteResult,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    if (message.variable !== "") {
      writer.uint32(18).string(message.variable);
    }
    if (message.sweep !== undefined) {
      Sweep.encode(message.sweep, writer.uint32(26).fork()).ldelim();
    }
    for (const v of message.an) {
      AnalysisResult.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): MonteResult {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseMonteResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.variable = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.sweep = Sweep.decode(reader, reader.uint32());
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.an.push(AnalysisResult.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): MonteResult {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      variable: isSet(object.variable)
        ? globalThis.String(object.variable)
        : "",
      sweep: isSet(object.sweep) ? Sweep.fromJSON(object.sweep) : undefined,
      an: globalThis.Array.isArray(object?.an)
        ? object.an.map((e: any) => AnalysisResult.fromJSON(e))
        : [],
    };
  },

  toJSON(message: MonteResult): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.variable !== "") {
      obj.variable = message.variable;
    }
    if (message.sweep !== undefined) {
      obj.sweep = Sweep.toJSON(message.sweep);
    }
    if (message.an?.length) {
      obj.an = message.an.map((e) => AnalysisResult.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<MonteResult>): MonteResult {
    return MonteResult.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<MonteResult>): MonteResult {
    const message = createBaseMonteResult();
    message.analysisName = object.analysisName ?? "";
    message.variable = object.variable ?? "";
    message.sweep =
      object.sweep !== undefined && object.sweep !== null
        ? Sweep.fromPartial(object.sweep)
        : undefined;
    message.an = object.an?.map((e) => AnalysisResult.fromPartial(e)) || [];
    return message;
  },
};

function createBaseCustomAnalysisInput(): CustomAnalysisInput {
  return { analysisName: "", cmd: "", ctrls: [] };
}

export const CustomAnalysisInput = {
  encode(
    message: CustomAnalysisInput,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.analysisName !== "") {
      writer.uint32(10).string(message.analysisName);
    }
    if (message.cmd !== "") {
      writer.uint32(18).string(message.cmd);
    }
    for (const v of message.ctrls) {
      Control.encode(v!, writer.uint32(42).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): CustomAnalysisInput {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseCustomAnalysisInput();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisName = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.cmd = reader.string();
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.ctrls.push(Control.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): CustomAnalysisInput {
    return {
      analysisName: isSet(object.analysisName)
        ? globalThis.String(object.analysisName)
        : "",
      cmd: isSet(object.cmd) ? globalThis.String(object.cmd) : "",
      ctrls: globalThis.Array.isArray(object?.ctrls)
        ? object.ctrls.map((e: any) => Control.fromJSON(e))
        : [],
    };
  },

  toJSON(message: CustomAnalysisInput): unknown {
    const obj: any = {};
    if (message.analysisName !== "") {
      obj.analysisName = message.analysisName;
    }
    if (message.cmd !== "") {
      obj.cmd = message.cmd;
    }
    if (message.ctrls?.length) {
      obj.ctrls = message.ctrls.map((e) => Control.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<CustomAnalysisInput>): CustomAnalysisInput {
    return CustomAnalysisInput.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<CustomAnalysisInput>): CustomAnalysisInput {
    const message = createBaseCustomAnalysisInput();
    message.analysisName = object.analysisName ?? "";
    message.cmd = object.cmd ?? "";
    message.ctrls = object.ctrls?.map((e) => Control.fromPartial(e)) || [];
    return message;
  },
};

function createBaseCustomAnalysisResult(): CustomAnalysisResult {
  return {};
}

export const CustomAnalysisResult = {
  encode(
    _: CustomAnalysisResult,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    return writer;
  },

  decode(
    input: _m0.Reader | Uint8Array,
    length?: number,
  ): CustomAnalysisResult {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseCustomAnalysisResult();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(_: any): CustomAnalysisResult {
    return {};
  },

  toJSON(_: CustomAnalysisResult): unknown {
    const obj: any = {};
    return obj;
  },

  create(base?: DeepPartial<CustomAnalysisResult>): CustomAnalysisResult {
    return CustomAnalysisResult.fromPartial(base ?? {});
  },
  fromPartial(_: DeepPartial<CustomAnalysisResult>): CustomAnalysisResult {
    const message = createBaseCustomAnalysisResult();
    return message;
  },
};

function createBaseSweep(): Sweep {
  return { tp: undefined };
}

export const Sweep = {
  encode(message: Sweep, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    switch (message.tp?.$case) {
      case "linear":
        LinearSweep.encode(
          message.tp.linear,
          writer.uint32(10).fork(),
        ).ldelim();
        break;
      case "log":
        LogSweep.encode(message.tp.log, writer.uint32(18).fork()).ldelim();
        break;
      case "points":
        PointSweep.encode(message.tp.points, writer.uint32(26).fork()).ldelim();
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Sweep {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseSweep();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.tp = {
            $case: "linear",
            linear: LinearSweep.decode(reader, reader.uint32()),
          };
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.tp = {
            $case: "log",
            log: LogSweep.decode(reader, reader.uint32()),
          };
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.tp = {
            $case: "points",
            points: PointSweep.decode(reader, reader.uint32()),
          };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Sweep {
    return {
      tp: isSet(object.linear)
        ? { $case: "linear", linear: LinearSweep.fromJSON(object.linear) }
        : isSet(object.log)
          ? { $case: "log", log: LogSweep.fromJSON(object.log) }
          : isSet(object.points)
            ? { $case: "points", points: PointSweep.fromJSON(object.points) }
            : undefined,
    };
  },

  toJSON(message: Sweep): unknown {
    const obj: any = {};
    if (message.tp?.$case === "linear") {
      obj.linear = LinearSweep.toJSON(message.tp.linear);
    }
    if (message.tp?.$case === "log") {
      obj.log = LogSweep.toJSON(message.tp.log);
    }
    if (message.tp?.$case === "points") {
      obj.points = PointSweep.toJSON(message.tp.points);
    }
    return obj;
  },

  create(base?: DeepPartial<Sweep>): Sweep {
    return Sweep.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Sweep>): Sweep {
    const message = createBaseSweep();
    if (
      object.tp?.$case === "linear" &&
      object.tp?.linear !== undefined &&
      object.tp?.linear !== null
    ) {
      message.tp = {
        $case: "linear",
        linear: LinearSweep.fromPartial(object.tp.linear),
      };
    }
    if (
      object.tp?.$case === "log" &&
      object.tp?.log !== undefined &&
      object.tp?.log !== null
    ) {
      message.tp = { $case: "log", log: LogSweep.fromPartial(object.tp.log) };
    }
    if (
      object.tp?.$case === "points" &&
      object.tp?.points !== undefined &&
      object.tp?.points !== null
    ) {
      message.tp = {
        $case: "points",
        points: PointSweep.fromPartial(object.tp.points),
      };
    }
    return message;
  },
};

function createBaseLinearSweep(): LinearSweep {
  return { start: 0, stop: 0, step: 0 };
}

export const LinearSweep = {
  encode(
    message: LinearSweep,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.start !== 0) {
      writer.uint32(9).double(message.start);
    }
    if (message.stop !== 0) {
      writer.uint32(17).double(message.stop);
    }
    if (message.step !== 0) {
      writer.uint32(25).double(message.step);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): LinearSweep {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLinearSweep();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 9) {
            break;
          }

          message.start = reader.double();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.stop = reader.double();
          continue;
        case 3:
          if (tag !== 25) {
            break;
          }

          message.step = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): LinearSweep {
    return {
      start: isSet(object.start) ? globalThis.Number(object.start) : 0,
      stop: isSet(object.stop) ? globalThis.Number(object.stop) : 0,
      step: isSet(object.step) ? globalThis.Number(object.step) : 0,
    };
  },

  toJSON(message: LinearSweep): unknown {
    const obj: any = {};
    if (message.start !== 0) {
      obj.start = message.start;
    }
    if (message.stop !== 0) {
      obj.stop = message.stop;
    }
    if (message.step !== 0) {
      obj.step = message.step;
    }
    return obj;
  },

  create(base?: DeepPartial<LinearSweep>): LinearSweep {
    return LinearSweep.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<LinearSweep>): LinearSweep {
    const message = createBaseLinearSweep();
    message.start = object.start ?? 0;
    message.stop = object.stop ?? 0;
    message.step = object.step ?? 0;
    return message;
  },
};

function createBaseLogSweep(): LogSweep {
  return { start: 0, stop: 0, npts: 0 };
}

export const LogSweep = {
  encode(
    message: LogSweep,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.start !== 0) {
      writer.uint32(9).double(message.start);
    }
    if (message.stop !== 0) {
      writer.uint32(17).double(message.stop);
    }
    if (message.npts !== 0) {
      writer.uint32(25).double(message.npts);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): LogSweep {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLogSweep();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 9) {
            break;
          }

          message.start = reader.double();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.stop = reader.double();
          continue;
        case 3:
          if (tag !== 25) {
            break;
          }

          message.npts = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): LogSweep {
    return {
      start: isSet(object.start) ? globalThis.Number(object.start) : 0,
      stop: isSet(object.stop) ? globalThis.Number(object.stop) : 0,
      npts: isSet(object.npts) ? globalThis.Number(object.npts) : 0,
    };
  },

  toJSON(message: LogSweep): unknown {
    const obj: any = {};
    if (message.start !== 0) {
      obj.start = message.start;
    }
    if (message.stop !== 0) {
      obj.stop = message.stop;
    }
    if (message.npts !== 0) {
      obj.npts = message.npts;
    }
    return obj;
  },

  create(base?: DeepPartial<LogSweep>): LogSweep {
    return LogSweep.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<LogSweep>): LogSweep {
    const message = createBaseLogSweep();
    message.start = object.start ?? 0;
    message.stop = object.stop ?? 0;
    message.npts = object.npts ?? 0;
    return message;
  },
};

function createBasePointSweep(): PointSweep {
  return { points: [], stop: 0, npts: 0 };
}

export const PointSweep = {
  encode(
    message: PointSweep,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    writer.uint32(10).fork();
    for (const v of message.points) {
      writer.double(v);
    }
    writer.ldelim();
    if (message.stop !== 0) {
      writer.uint32(17).double(message.stop);
    }
    if (message.npts !== 0) {
      writer.uint32(25).double(message.npts);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): PointSweep {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePointSweep();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag === 9) {
            message.points.push(reader.double());

            continue;
          }

          if (tag === 10) {
            const end2 = reader.uint32() + reader.pos;
            while (reader.pos < end2) {
              message.points.push(reader.double());
            }

            continue;
          }

          break;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.stop = reader.double();
          continue;
        case 3:
          if (tag !== 25) {
            break;
          }

          message.npts = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): PointSweep {
    return {
      points: globalThis.Array.isArray(object?.points)
        ? object.points.map((e: any) => globalThis.Number(e))
        : [],
      stop: isSet(object.stop) ? globalThis.Number(object.stop) : 0,
      npts: isSet(object.npts) ? globalThis.Number(object.npts) : 0,
    };
  },

  toJSON(message: PointSweep): unknown {
    const obj: any = {};
    if (message.points?.length) {
      obj.points = message.points;
    }
    if (message.stop !== 0) {
      obj.stop = message.stop;
    }
    if (message.npts !== 0) {
      obj.npts = message.npts;
    }
    return obj;
  },

  create(base?: DeepPartial<PointSweep>): PointSweep {
    return PointSweep.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<PointSweep>): PointSweep {
    const message = createBasePointSweep();
    message.points = object.points?.map((e) => e) || [];
    message.stop = object.stop ?? 0;
    message.npts = object.npts ?? 0;
    return message;
  },
};

function createBaseControl(): Control {
  return { ctrl: undefined };
}

export const Control = {
  encode(
    message: Control,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    switch (message.ctrl?.$case) {
      case "include":
        Include.encode(message.ctrl.include, writer.uint32(10).fork()).ldelim();
        break;
      case "lib":
        LibInclude.encode(message.ctrl.lib, writer.uint32(18).fork()).ldelim();
        break;
      case "save":
        Save.encode(message.ctrl.save, writer.uint32(42).fork()).ldelim();
        break;
      case "meas":
        Meas.encode(message.ctrl.meas, writer.uint32(50).fork()).ldelim();
        break;
      case "param":
        Param.encode(message.ctrl.param, writer.uint32(58).fork()).ldelim();
        break;
      case "literal":
        writer.uint32(82).string(message.ctrl.literal);
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Control {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseControl();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.ctrl = {
            $case: "include",
            include: Include.decode(reader, reader.uint32()),
          };
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.ctrl = {
            $case: "lib",
            lib: LibInclude.decode(reader, reader.uint32()),
          };
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.ctrl = {
            $case: "save",
            save: Save.decode(reader, reader.uint32()),
          };
          continue;
        case 6:
          if (tag !== 50) {
            break;
          }

          message.ctrl = {
            $case: "meas",
            meas: Meas.decode(reader, reader.uint32()),
          };
          continue;
        case 7:
          if (tag !== 58) {
            break;
          }

          message.ctrl = {
            $case: "param",
            param: Param.decode(reader, reader.uint32()),
          };
          continue;
        case 10:
          if (tag !== 82) {
            break;
          }

          message.ctrl = { $case: "literal", literal: reader.string() };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Control {
    return {
      ctrl: isSet(object.include)
        ? { $case: "include", include: Include.fromJSON(object.include) }
        : isSet(object.lib)
          ? { $case: "lib", lib: LibInclude.fromJSON(object.lib) }
          : isSet(object.save)
            ? { $case: "save", save: Save.fromJSON(object.save) }
            : isSet(object.meas)
              ? { $case: "meas", meas: Meas.fromJSON(object.meas) }
              : isSet(object.param)
                ? { $case: "param", param: Param.fromJSON(object.param) }
                : isSet(object.literal)
                  ? {
                      $case: "literal",
                      literal: globalThis.String(object.literal),
                    }
                  : undefined,
    };
  },

  toJSON(message: Control): unknown {
    const obj: any = {};
    if (message.ctrl?.$case === "include") {
      obj.include = Include.toJSON(message.ctrl.include);
    }
    if (message.ctrl?.$case === "lib") {
      obj.lib = LibInclude.toJSON(message.ctrl.lib);
    }
    if (message.ctrl?.$case === "save") {
      obj.save = Save.toJSON(message.ctrl.save);
    }
    if (message.ctrl?.$case === "meas") {
      obj.meas = Meas.toJSON(message.ctrl.meas);
    }
    if (message.ctrl?.$case === "param") {
      obj.param = Param.toJSON(message.ctrl.param);
    }
    if (message.ctrl?.$case === "literal") {
      obj.literal = message.ctrl.literal;
    }
    return obj;
  },

  create(base?: DeepPartial<Control>): Control {
    return Control.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Control>): Control {
    const message = createBaseControl();
    if (
      object.ctrl?.$case === "include" &&
      object.ctrl?.include !== undefined &&
      object.ctrl?.include !== null
    ) {
      message.ctrl = {
        $case: "include",
        include: Include.fromPartial(object.ctrl.include),
      };
    }
    if (
      object.ctrl?.$case === "lib" &&
      object.ctrl?.lib !== undefined &&
      object.ctrl?.lib !== null
    ) {
      message.ctrl = {
        $case: "lib",
        lib: LibInclude.fromPartial(object.ctrl.lib),
      };
    }
    if (
      object.ctrl?.$case === "save" &&
      object.ctrl?.save !== undefined &&
      object.ctrl?.save !== null
    ) {
      message.ctrl = {
        $case: "save",
        save: Save.fromPartial(object.ctrl.save),
      };
    }
    if (
      object.ctrl?.$case === "meas" &&
      object.ctrl?.meas !== undefined &&
      object.ctrl?.meas !== null
    ) {
      message.ctrl = {
        $case: "meas",
        meas: Meas.fromPartial(object.ctrl.meas),
      };
    }
    if (
      object.ctrl?.$case === "param" &&
      object.ctrl?.param !== undefined &&
      object.ctrl?.param !== null
    ) {
      message.ctrl = {
        $case: "param",
        param: Param.fromPartial(object.ctrl.param),
      };
    }
    if (
      object.ctrl?.$case === "literal" &&
      object.ctrl?.literal !== undefined &&
      object.ctrl?.literal !== null
    ) {
      message.ctrl = { $case: "literal", literal: object.ctrl.literal };
    }
    return message;
  },
};

function createBaseSave(): Save {
  return { save: undefined };
}

export const Save = {
  encode(message: Save, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    switch (message.save?.$case) {
      case "mode":
        writer.uint32(8).int32(message.save.mode);
        break;
      case "signal":
        writer.uint32(18).string(message.save.signal);
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Save {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseSave();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.save = { $case: "mode", mode: reader.int32() as any };
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.save = { $case: "signal", signal: reader.string() };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Save {
    return {
      save: isSet(object.mode)
        ? { $case: "mode", mode: save_SaveModeFromJSON(object.mode) }
        : isSet(object.signal)
          ? { $case: "signal", signal: globalThis.String(object.signal) }
          : undefined,
    };
  },

  toJSON(message: Save): unknown {
    const obj: any = {};
    if (message.save?.$case === "mode") {
      obj.mode = save_SaveModeToJSON(message.save.mode);
    }
    if (message.save?.$case === "signal") {
      obj.signal = message.save.signal;
    }
    return obj;
  },

  create(base?: DeepPartial<Save>): Save {
    return Save.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Save>): Save {
    const message = createBaseSave();
    if (
      object.save?.$case === "mode" &&
      object.save?.mode !== undefined &&
      object.save?.mode !== null
    ) {
      message.save = { $case: "mode", mode: object.save.mode };
    }
    if (
      object.save?.$case === "signal" &&
      object.save?.signal !== undefined &&
      object.save?.signal !== null
    ) {
      message.save = { $case: "signal", signal: object.save.signal };
    }
    return message;
  },
};

function createBaseInclude(): Include {
  return { path: "" };
}

export const Include = {
  encode(
    message: Include,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.path !== "") {
      writer.uint32(10).string(message.path);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Include {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseInclude();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.path = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Include {
    return { path: isSet(object.path) ? globalThis.String(object.path) : "" };
  },

  toJSON(message: Include): unknown {
    const obj: any = {};
    if (message.path !== "") {
      obj.path = message.path;
    }
    return obj;
  },

  create(base?: DeepPartial<Include>): Include {
    return Include.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Include>): Include {
    const message = createBaseInclude();
    message.path = object.path ?? "";
    return message;
  },
};

function createBaseLibInclude(): LibInclude {
  return { path: "", section: "" };
}

export const LibInclude = {
  encode(
    message: LibInclude,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.path !== "") {
      writer.uint32(10).string(message.path);
    }
    if (message.section !== "") {
      writer.uint32(18).string(message.section);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): LibInclude {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLibInclude();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.path = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.section = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): LibInclude {
    return {
      path: isSet(object.path) ? globalThis.String(object.path) : "",
      section: isSet(object.section) ? globalThis.String(object.section) : "",
    };
  },

  toJSON(message: LibInclude): unknown {
    const obj: any = {};
    if (message.path !== "") {
      obj.path = message.path;
    }
    if (message.section !== "") {
      obj.section = message.section;
    }
    return obj;
  },

  create(base?: DeepPartial<LibInclude>): LibInclude {
    return LibInclude.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<LibInclude>): LibInclude {
    const message = createBaseLibInclude();
    message.path = object.path ?? "";
    message.section = object.section ?? "";
    return message;
  },
};

function createBaseMeas(): Meas {
  return { analysisType: "", name: "", expr: "" };
}

export const Meas = {
  encode(message: Meas, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.analysisType !== "") {
      writer.uint32(10).string(message.analysisType);
    }
    if (message.name !== "") {
      writer.uint32(18).string(message.name);
    }
    if (message.expr !== "") {
      writer.uint32(26).string(message.expr);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Meas {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseMeas();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.analysisType = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.name = reader.string();
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.expr = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Meas {
    return {
      analysisType: isSet(object.analysisType)
        ? globalThis.String(object.analysisType)
        : "",
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      expr: isSet(object.expr) ? globalThis.String(object.expr) : "",
    };
  },

  toJSON(message: Meas): unknown {
    const obj: any = {};
    if (message.analysisType !== "") {
      obj.analysisType = message.analysisType;
    }
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.expr !== "") {
      obj.expr = message.expr;
    }
    return obj;
  },

  create(base?: DeepPartial<Meas>): Meas {
    return Meas.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Meas>): Meas {
    const message = createBaseMeas();
    message.analysisType = object.analysisType ?? "";
    message.name = object.name ?? "";
    message.expr = object.expr ?? "";
    return message;
  },
};

function createBaseSignal(): Signal {
  return { name: "", quantity: 0 };
}

export const Signal = {
  encode(
    message: Signal,
    writer: _m0.Writer = _m0.Writer.create(),
  ): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.quantity !== 0) {
      writer.uint32(16).int32(message.quantity);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Signal {
    const reader =
      input instanceof _m0.Reader ? input : _m0.Reader.create(input);
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

          message.quantity = reader.int32() as any;
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
      quantity: isSet(object.quantity)
        ? signal_QuantityFromJSON(object.quantity)
        : 0,
    };
  },

  toJSON(message: Signal): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.quantity !== 0) {
      obj.quantity = signal_QuantityToJSON(message.quantity);
    }
    return obj;
  },

  create(base?: DeepPartial<Signal>): Signal {
    return Signal.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Signal>): Signal {
    const message = createBaseSignal();
    message.name = object.name ?? "";
    message.quantity = object.quantity ?? 0;
    return message;
  },
};

/**
 * # The SPICE Service
 *
 * Defines a single method `Sim` which accepts simulator input via a `SimInput` message,
 * performs the requested set of circuit-analyses, and returns results via a `SimResult`.
 */
export interface Spice {
  Sim(request: SimInput): Promise<SimResult>;
}

export const SpiceServiceName = "vlsir.spice.Spice";
export class SpiceClientImpl implements Spice {
  private readonly rpc: Rpc;
  private readonly service: string;
  constructor(rpc: Rpc, opts?: { service?: string }) {
    this.service = opts?.service || SpiceServiceName;
    this.rpc = rpc;
    this.Sim = this.Sim.bind(this);
  }
  Sim(request: SimInput): Promise<SimResult> {
    const data = SimInput.encode(request).finish();
    const promise = this.rpc.request(this.service, "Sim", data);
    return promise.then((data) => SimResult.decode(_m0.Reader.create(data)));
  }
}

interface Rpc {
  request(
    service: string,
    method: string,
    data: Uint8Array,
  ): Promise<Uint8Array>;
}

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

function isObject(value: any): boolean {
  return typeof value === "object" && value !== null;
}

function isSet(value: any): boolean {
  return value !== null && value !== undefined;
}
