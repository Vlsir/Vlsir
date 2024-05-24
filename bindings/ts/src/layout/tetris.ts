/* eslint-disable */
import Long from "long";
import _m0 from "protobufjs/minimal";
import { Interface, Module } from "../circuit";
import { AuthorMetadata, Reference } from "../utils";
import { Layer, Point, Units, unitsFromJSON, unitsToJSON } from "./raw";

/**
 * # Library
 *
 * A collection of `Cells` and asssociated metadata.
 * Primary data in the `cells` field is valid only if stored in dependency order,
 * i.e. that each cell-definition must follow all cells that it depends upon.
 */
export interface Library {
  /** Library Name / Domain */
  domain: string;
  /** Cell Definitions */
  cells: Cell[];
  /** Author Information */
  author: AuthorMetadata | undefined;
}

/**
 * # Cell
 * A multi-view representation of a piece of hardware.
 */
export interface Cell {
  /** Cell Name */
  name: string;
  /** IO Interface */
  interface:
    | Interface
    | undefined;
  /** Circuit Module Definition */
  module:
    | Module
    | undefined;
  /** Physical Abstract */
  abstract:
    | Abstract
    | undefined;
  /** Physical Layout Implementation */
  layout: Layout | undefined;
}

/**
 * # Layout
 *
 * Physical implementation of a `Cell`. Tetris layouts consist of:
 * * `Instances` of other `Cells`,
 * * Net-assignments at grid crossings, and
 * * Cuts of the grid
 * (That's all.)
 *
 * `Layouts` have an explicit `Outline`, in which all their attributes must fit,
 * and into which no other `Layout` can encroach.
 * This operates similarly to "blockage" on all layers in legacy layout systems.
 */
export interface Layout {
  /** Cell Name */
  name: string;
  /** Outline */
  outline:
    | Outline
    | undefined;
  /** Layout Instances */
  instances: Instance[];
  /** Net-to-track assignments */
  assignments: Assign[];
  /** Track cuts */
  cuts: TrackCross[];
}

/**
 * # Assignment
 *
 * Assigns signal `net` to the two tracks crossing in location `at`.
 * Tetris signal-assignments are to track-crosses.
 * This operates much like assigning to a via, plus the tracks above and below.
 */
export interface Assign {
  /** Net Name */
  net: string;
  /** Location */
  at: TrackCross | undefined;
}

/**
 * # Track Cross
 * Crossing between two `TrackRefs`
 */
export interface TrackCross {
  /** "Primary" Track */
  track:
    | TrackRef
    | undefined;
  /** Intersection location, on an orthogonal layer */
  cross: TrackRef | undefined;
}

/**
 * # Track Reference
 * Integer-pair pointer to a layer-index and track-index
 */
export interface TrackRef {
  /** Layer Index */
  layer: number;
  /** Track Index */
  track: number;
}

/**
 * # Cell Outlines
 * ## "Tetris Shaped" rectilinear polygons
 *
 * These boundaries are closed, consist solely of 90-degree rectangular turns,
 * and are specified by a counter-clockwise set of points.
 * "Holes" such as the shapes "O" and "8" and "divots" such as the shapes "U" and "H" are not supported.
 * The z-axis top is uniform and specified by a single layer-index `top_layer`.
 *
 * Two equal-length vectors `x` and `y` describe an Outline's (x, y) points.
 * Counter-clockwise-ness and divot-free-ness requires that:
 * * (a) `x` values are monotonically non-increasing, and
 * * (b) `y` values are monotonically non-decreasing
 *
 * In point-space terms, such an outline has vertices at:
 * `[(0,0), (x[0], 0), (x[0], y[0]), (x[1], y[0]), ... , (0, y[-1]), (0,0)]`
 * With the final point at (0, y[-1]), and its connection back to the origin both implied.
 *
 * Example: a rectangular Outline would require a single entry for each of `x` and `y`,
 * at the rectangle's vertex opposite the origin in both axes.
 */
export interface Outline {
  /** X Coordinates */
  x: number[];
  /** Y Coordinates */
  y: number[];
  /** Number of metal layers used */
  metals: number;
}

/**
 * # Abstract Layout
 *
 * Defines the physical interface to a [Cell], including ports and internal blockages,
 * omitting internal implementation details.
 */
export interface Abstract {
  /** Cell Name */
  name: string;
  /** Outline */
  outline:
    | Outline
    | undefined;
  /** Ports */
  ports: AbstractPort[];
}

/**
 * # Abstract Port
 * Combination of a net and set of shapes
 */
export interface AbstractPort {
  /** Port Name */
  net: string;
  kind?: { $case: "edge"; edge: AbstractPort_EdgePort } | { $case: "ztopEdge"; ztopEdge: AbstractPort_ZTopEdgePort } | {
    $case: "ztopInner";
    ztopInner: AbstractPort_ZTopInner;
  } | undefined;
}

/**
 * # Abstract Port Side
 *
 * A two-value enum, as each layer either runs horizontally or vertically.
 * Ports on the nearer-origin (bottom or left) sides use variant `BOTTOM_OR_LEFT`,
 * while ports on the opposite sides use `TOP_OR_RIGHT`.
 */
export enum AbstractPort_PortSide {
  BOTTOM_OR_LEFT = 0,
  TOP_OR_RIGHT = 1,
  UNRECOGNIZED = -1,
}

export function abstractPort_PortSideFromJSON(object: any): AbstractPort_PortSide {
  switch (object) {
    case 0:
    case "BOTTOM_OR_LEFT":
      return AbstractPort_PortSide.BOTTOM_OR_LEFT;
    case 1:
    case "TOP_OR_RIGHT":
      return AbstractPort_PortSide.TOP_OR_RIGHT;
    case -1:
    case "UNRECOGNIZED":
    default:
      return AbstractPort_PortSide.UNRECOGNIZED;
  }
}

export function abstractPort_PortSideToJSON(object: AbstractPort_PortSide): string {
  switch (object) {
    case AbstractPort_PortSide.BOTTOM_OR_LEFT:
      return "BOTTOM_OR_LEFT";
    case AbstractPort_PortSide.TOP_OR_RIGHT:
      return "TOP_OR_RIGHT";
    case AbstractPort_PortSide.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/**
 * # Edge Port
 * On a layer less than `top_layer`. Only connectable on its `track` and `side`.
 */
export interface AbstractPort_EdgePort {
  track: TrackRef | undefined;
  side: AbstractPort_PortSide;
}

/**
 * # Z-Top, on Edge Port
 * Can be connected from either `top_layer+1`, or the edge on `top_layer`.
 */
export interface AbstractPort_ZTopEdgePort {
  /** Track index */
  track: number;
  /** Side */
  side: AbstractPort_PortSide;
  /**
   * Extent into the cell.
   * Must be a location which intersects with (track, Side) inside the Outline.
   */
  into: TrackRef | undefined;
}

/** # Z-Top, inside Outline Port */
export interface AbstractPort_ZTopInner {
  /** Locations. All must be on layers adjacent to the top-layer. */
  locs: TrackCross[];
}

/** # Cell Instance */
export interface Instance {
  /** Instance Name */
  name: string;
  /** Cell Reference */
  cell:
    | Reference
    | undefined;
  /**
   * Location of the defined Cell's origin
   * this location holds regardless of reflection settings.
   */
  loc:
    | Place
    | undefined;
  /** Horizontal reflection about y-axis */
  reflectHoriz: boolean;
  /** Vertical reflection about x-axis */
  reflectVert: boolean;
}

/**
 * # Place
 * An absolute or relative placement description
 */
export interface Place {
  place?: { $case: "abs"; abs: Point } | { $case: "rel"; rel: RelPlace } | undefined;
}

/** # Relative Place */
export interface RelPlace {
}

/**
 * # Stack
 *
 * The z-stack, primarily including metal, via, and primitive layers
 */
export interface Stack {
  /** Measurement units */
  units: Units;
  /** Primitive Layer */
  prim:
    | PrimitiveLayer
    | undefined;
  /** Set of metal layers */
  metals: MetalLayer[];
  /** Set of via layers */
  vias: ViaLayer[];
  /**
   * [raw::Layer] Mappings
   * vlsir.raw.Layers rawlayers = 1;
   * Layer used for cell outlines/ boundaries
   */
  boundaryLayer: Layer | undefined;
}

/**
 * # LayerEnum
 *
 * Type and index of a layer.
 */
export interface LayerEnum {
  /** Layer Type */
  type: LayerEnum_LayerType;
  /** Index into the associated `LayerType` set */
  index: number;
}

export enum LayerEnum_LayerType {
  PRIMITIVE = 0,
  METAL = 1,
  VIA = 2,
  UNRECOGNIZED = -1,
}

export function layerEnum_LayerTypeFromJSON(object: any): LayerEnum_LayerType {
  switch (object) {
    case 0:
    case "PRIMITIVE":
      return LayerEnum_LayerType.PRIMITIVE;
    case 1:
    case "METAL":
      return LayerEnum_LayerType.METAL;
    case 2:
    case "VIA":
      return LayerEnum_LayerType.VIA;
    case -1:
    case "UNRECOGNIZED":
    default:
      return LayerEnum_LayerType.UNRECOGNIZED;
  }
}

export function layerEnum_LayerTypeToJSON(object: LayerEnum_LayerType): string {
  switch (object) {
    case LayerEnum_LayerType.PRIMITIVE:
      return "PRIMITIVE";
    case LayerEnum_LayerType.METAL:
      return "METAL";
    case LayerEnum_LayerType.VIA:
      return "VIA";
    case LayerEnum_LayerType.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/**
 * # MetalLayer
 *
 * Metal layer in a [Stack]
 * Each layer is effectively infinite-spanning in one dimension, and periodic in the other.
 * Layers with `dir=Dir::Horiz` extend to infinity in x, and repeat in y, and vice-versa.
 */
export interface MetalLayer {
  /** Layer Name */
  name: string;
  /** Direction Enumeration (Horizontal/ Vertical) */
  dir: MetalLayer_Dir;
  /** Default size of wire-cuts */
  cutsize: number;
  /** Track Size & Type Entries */
  entries: TrackSpec[];
  /** Offset, in our periodic dimension */
  offset: number;
  /** Overlap between periods */
  overlap: number;
  /** Setting for period-by-period flipping */
  flip: boolean;
  /** Primitive-layer relationship */
  prim: MetalLayer_PrimitiveMode;
  /** Raw Layer */
  raw: Layer | undefined;
}

/** Direction Enumeration */
export enum MetalLayer_Dir {
  HORIZ = 0,
  VERT = 1,
  UNRECOGNIZED = -1,
}

export function metalLayer_DirFromJSON(object: any): MetalLayer_Dir {
  switch (object) {
    case 0:
    case "HORIZ":
      return MetalLayer_Dir.HORIZ;
    case 1:
    case "VERT":
      return MetalLayer_Dir.VERT;
    case -1:
    case "UNRECOGNIZED":
    default:
      return MetalLayer_Dir.UNRECOGNIZED;
  }
}

export function metalLayer_DirToJSON(object: MetalLayer_Dir): string {
  switch (object) {
    case MetalLayer_Dir.HORIZ:
      return "HORIZ";
    case MetalLayer_Dir.VERT:
      return "VERT";
    case MetalLayer_Dir.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/** Ownership split of a layer between Primitives and the Stack. */
export enum MetalLayer_PrimitiveMode {
  /** PRIM - Owned by Primitives */
  PRIM = 0,
  /** SPLIT - Split between Primitives and the Stack */
  SPLIT = 1,
  /** STACK - Owned by the Stack */
  STACK = 2,
  UNRECOGNIZED = -1,
}

export function metalLayer_PrimitiveModeFromJSON(object: any): MetalLayer_PrimitiveMode {
  switch (object) {
    case 0:
    case "PRIM":
      return MetalLayer_PrimitiveMode.PRIM;
    case 1:
    case "SPLIT":
      return MetalLayer_PrimitiveMode.SPLIT;
    case 2:
    case "STACK":
      return MetalLayer_PrimitiveMode.STACK;
    case -1:
    case "UNRECOGNIZED":
    default:
      return MetalLayer_PrimitiveMode.UNRECOGNIZED;
  }
}

export function metalLayer_PrimitiveModeToJSON(object: MetalLayer_PrimitiveMode): string {
  switch (object) {
    case MetalLayer_PrimitiveMode.PRIM:
      return "PRIM";
    case MetalLayer_PrimitiveMode.SPLIT:
      return "SPLIT";
    case MetalLayer_PrimitiveMode.STACK:
      return "STACK";
    case MetalLayer_PrimitiveMode.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/**
 * # ViaLayer
 *
 * Insulator and connector Layer Between `MetalLayers`
 */
export interface ViaLayer {
  /** Layer name */
  name: string;
  /** Top of the two layers connected by this layer */
  top:
    | LayerEnum
    | undefined;
  /** Bottom of the two layers connected by this layer */
  bot:
    | LayerEnum
    | undefined;
  /** Via size */
  size:
    | Xy
    | undefined;
  /** Raw Layer */
  raw: Layer | undefined;
}

/**
 * # Primitive Layer
 *
 * Encapsulates all layout information "below" an associated `Stack`.
 * In typical process technologies this primarily includes "base layers",
 * such as those used in primitive transistors and logic cells.
 */
export interface PrimitiveLayer {
  /** Pitches, in Database Units */
  pitches: Xy | undefined;
}

/**
 * # Track Specification
 *
 * Includes definitions for the single `TrackEntry`
 * and repitition thereof (`Repeat`).
 * Sole field `spec` is one of the two.
 */
export interface TrackSpec {
  spec?: { $case: "entry"; entry: TrackSpec_TrackEntry } | { $case: "repeat"; repeat: TrackSpec_Repeat } | undefined;
}

export interface TrackSpec_TrackEntry {
  /** TrackType */
  ttype: TrackSpec_TrackEntry_TrackType;
  /** Entry width */
  width: number;
}

export enum TrackSpec_TrackEntry_TrackType {
  /** GAP - Insulator Gap */
  GAP = 0,
  /** SIGNAL - Signal Track */
  SIGNAL = 1,
  /** RAIL - Rail Track. FIXME: Add rail type. */
  RAIL = 2,
  UNRECOGNIZED = -1,
}

export function trackSpec_TrackEntry_TrackTypeFromJSON(object: any): TrackSpec_TrackEntry_TrackType {
  switch (object) {
    case 0:
    case "GAP":
      return TrackSpec_TrackEntry_TrackType.GAP;
    case 1:
    case "SIGNAL":
      return TrackSpec_TrackEntry_TrackType.SIGNAL;
    case 2:
    case "RAIL":
      return TrackSpec_TrackEntry_TrackType.RAIL;
    case -1:
    case "UNRECOGNIZED":
    default:
      return TrackSpec_TrackEntry_TrackType.UNRECOGNIZED;
  }
}

export function trackSpec_TrackEntry_TrackTypeToJSON(object: TrackSpec_TrackEntry_TrackType): string {
  switch (object) {
    case TrackSpec_TrackEntry_TrackType.GAP:
      return "GAP";
    case TrackSpec_TrackEntry_TrackType.SIGNAL:
      return "SIGNAL";
    case TrackSpec_TrackEntry_TrackType.RAIL:
      return "RAIL";
    case TrackSpec_TrackEntry_TrackType.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/** Repeated Pattern of Track Entries */
export interface TrackSpec_Repeat {
  /** List of entries */
  entries: TrackSpec_TrackEntry[];
  /** Number of repetitions */
  nrep: number;
}

/**
 * # Xy
 *
 * Two-dimensional (x,y) pair.
 * While similar in content to `vlsir.raw.Point`, `Xy` data does not semantically
 * (necessarily) refer to a single point in Cartesian space.
 * More general use-cases include the size of blocks, or the pitch of a grid.
 */
export interface Xy {
  x: number;
  y: number;
}

function createBaseLibrary(): Library {
  return { domain: "", cells: [], author: undefined };
}

export const Library = {
  encode(message: Library, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.domain !== "") {
      writer.uint32(10).string(message.domain);
    }
    for (const v of message.cells) {
      Cell.encode(v!, writer.uint32(82).fork()).ldelim();
    }
    if (message.author !== undefined) {
      AuthorMetadata.encode(message.author, writer.uint32(162).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Library {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLibrary();
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

          message.cells.push(Cell.decode(reader, reader.uint32()));
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

  fromJSON(object: any): Library {
    return {
      domain: isSet(object.domain) ? globalThis.String(object.domain) : "",
      cells: globalThis.Array.isArray(object?.cells) ? object.cells.map((e: any) => Cell.fromJSON(e)) : [],
      author: isSet(object.author) ? AuthorMetadata.fromJSON(object.author) : undefined,
    };
  },

  toJSON(message: Library): unknown {
    const obj: any = {};
    if (message.domain !== "") {
      obj.domain = message.domain;
    }
    if (message.cells?.length) {
      obj.cells = message.cells.map((e) => Cell.toJSON(e));
    }
    if (message.author !== undefined) {
      obj.author = AuthorMetadata.toJSON(message.author);
    }
    return obj;
  },

  create(base?: DeepPartial<Library>): Library {
    return Library.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Library>): Library {
    const message = createBaseLibrary();
    message.domain = object.domain ?? "";
    message.cells = object.cells?.map((e) => Cell.fromPartial(e)) || [];
    message.author = (object.author !== undefined && object.author !== null)
      ? AuthorMetadata.fromPartial(object.author)
      : undefined;
    return message;
  },
};

function createBaseCell(): Cell {
  return { name: "", interface: undefined, module: undefined, abstract: undefined, layout: undefined };
}

export const Cell = {
  encode(message: Cell, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.interface !== undefined) {
      Interface.encode(message.interface, writer.uint32(82).fork()).ldelim();
    }
    if (message.module !== undefined) {
      Module.encode(message.module, writer.uint32(90).fork()).ldelim();
    }
    if (message.abstract !== undefined) {
      Abstract.encode(message.abstract, writer.uint32(98).fork()).ldelim();
    }
    if (message.layout !== undefined) {
      Layout.encode(message.layout, writer.uint32(106).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Cell {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseCell();
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

          message.interface = Interface.decode(reader, reader.uint32());
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.module = Module.decode(reader, reader.uint32());
          continue;
        case 12:
          if (tag !== 98) {
            break;
          }

          message.abstract = Abstract.decode(reader, reader.uint32());
          continue;
        case 13:
          if (tag !== 106) {
            break;
          }

          message.layout = Layout.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Cell {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      interface: isSet(object.interface) ? Interface.fromJSON(object.interface) : undefined,
      module: isSet(object.module) ? Module.fromJSON(object.module) : undefined,
      abstract: isSet(object.abstract) ? Abstract.fromJSON(object.abstract) : undefined,
      layout: isSet(object.layout) ? Layout.fromJSON(object.layout) : undefined,
    };
  },

  toJSON(message: Cell): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.interface !== undefined) {
      obj.interface = Interface.toJSON(message.interface);
    }
    if (message.module !== undefined) {
      obj.module = Module.toJSON(message.module);
    }
    if (message.abstract !== undefined) {
      obj.abstract = Abstract.toJSON(message.abstract);
    }
    if (message.layout !== undefined) {
      obj.layout = Layout.toJSON(message.layout);
    }
    return obj;
  },

  create(base?: DeepPartial<Cell>): Cell {
    return Cell.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Cell>): Cell {
    const message = createBaseCell();
    message.name = object.name ?? "";
    message.interface = (object.interface !== undefined && object.interface !== null)
      ? Interface.fromPartial(object.interface)
      : undefined;
    message.module = (object.module !== undefined && object.module !== null)
      ? Module.fromPartial(object.module)
      : undefined;
    message.abstract = (object.abstract !== undefined && object.abstract !== null)
      ? Abstract.fromPartial(object.abstract)
      : undefined;
    message.layout = (object.layout !== undefined && object.layout !== null)
      ? Layout.fromPartial(object.layout)
      : undefined;
    return message;
  },
};

function createBaseLayout(): Layout {
  return { name: "", outline: undefined, instances: [], assignments: [], cuts: [] };
}

export const Layout = {
  encode(message: Layout, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.outline !== undefined) {
      Outline.encode(message.outline, writer.uint32(82).fork()).ldelim();
    }
    for (const v of message.instances) {
      Instance.encode(v!, writer.uint32(162).fork()).ldelim();
    }
    for (const v of message.assignments) {
      Assign.encode(v!, writer.uint32(170).fork()).ldelim();
    }
    for (const v of message.cuts) {
      TrackCross.encode(v!, writer.uint32(178).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Layout {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLayout();
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

          message.outline = Outline.decode(reader, reader.uint32());
          continue;
        case 20:
          if (tag !== 162) {
            break;
          }

          message.instances.push(Instance.decode(reader, reader.uint32()));
          continue;
        case 21:
          if (tag !== 170) {
            break;
          }

          message.assignments.push(Assign.decode(reader, reader.uint32()));
          continue;
        case 22:
          if (tag !== 178) {
            break;
          }

          message.cuts.push(TrackCross.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Layout {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      outline: isSet(object.outline) ? Outline.fromJSON(object.outline) : undefined,
      instances: globalThis.Array.isArray(object?.instances)
        ? object.instances.map((e: any) => Instance.fromJSON(e))
        : [],
      assignments: globalThis.Array.isArray(object?.assignments)
        ? object.assignments.map((e: any) => Assign.fromJSON(e))
        : [],
      cuts: globalThis.Array.isArray(object?.cuts) ? object.cuts.map((e: any) => TrackCross.fromJSON(e)) : [],
    };
  },

  toJSON(message: Layout): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.outline !== undefined) {
      obj.outline = Outline.toJSON(message.outline);
    }
    if (message.instances?.length) {
      obj.instances = message.instances.map((e) => Instance.toJSON(e));
    }
    if (message.assignments?.length) {
      obj.assignments = message.assignments.map((e) => Assign.toJSON(e));
    }
    if (message.cuts?.length) {
      obj.cuts = message.cuts.map((e) => TrackCross.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<Layout>): Layout {
    return Layout.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Layout>): Layout {
    const message = createBaseLayout();
    message.name = object.name ?? "";
    message.outline = (object.outline !== undefined && object.outline !== null)
      ? Outline.fromPartial(object.outline)
      : undefined;
    message.instances = object.instances?.map((e) => Instance.fromPartial(e)) || [];
    message.assignments = object.assignments?.map((e) => Assign.fromPartial(e)) || [];
    message.cuts = object.cuts?.map((e) => TrackCross.fromPartial(e)) || [];
    return message;
  },
};

function createBaseAssign(): Assign {
  return { net: "", at: undefined };
}

export const Assign = {
  encode(message: Assign, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.net !== "") {
      writer.uint32(10).string(message.net);
    }
    if (message.at !== undefined) {
      TrackCross.encode(message.at, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Assign {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAssign();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.net = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.at = TrackCross.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Assign {
    return {
      net: isSet(object.net) ? globalThis.String(object.net) : "",
      at: isSet(object.at) ? TrackCross.fromJSON(object.at) : undefined,
    };
  },

  toJSON(message: Assign): unknown {
    const obj: any = {};
    if (message.net !== "") {
      obj.net = message.net;
    }
    if (message.at !== undefined) {
      obj.at = TrackCross.toJSON(message.at);
    }
    return obj;
  },

  create(base?: DeepPartial<Assign>): Assign {
    return Assign.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Assign>): Assign {
    const message = createBaseAssign();
    message.net = object.net ?? "";
    message.at = (object.at !== undefined && object.at !== null) ? TrackCross.fromPartial(object.at) : undefined;
    return message;
  },
};

function createBaseTrackCross(): TrackCross {
  return { track: undefined, cross: undefined };
}

export const TrackCross = {
  encode(message: TrackCross, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.track !== undefined) {
      TrackRef.encode(message.track, writer.uint32(10).fork()).ldelim();
    }
    if (message.cross !== undefined) {
      TrackRef.encode(message.cross, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): TrackCross {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTrackCross();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.track = TrackRef.decode(reader, reader.uint32());
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.cross = TrackRef.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): TrackCross {
    return {
      track: isSet(object.track) ? TrackRef.fromJSON(object.track) : undefined,
      cross: isSet(object.cross) ? TrackRef.fromJSON(object.cross) : undefined,
    };
  },

  toJSON(message: TrackCross): unknown {
    const obj: any = {};
    if (message.track !== undefined) {
      obj.track = TrackRef.toJSON(message.track);
    }
    if (message.cross !== undefined) {
      obj.cross = TrackRef.toJSON(message.cross);
    }
    return obj;
  },

  create(base?: DeepPartial<TrackCross>): TrackCross {
    return TrackCross.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<TrackCross>): TrackCross {
    const message = createBaseTrackCross();
    message.track = (object.track !== undefined && object.track !== null)
      ? TrackRef.fromPartial(object.track)
      : undefined;
    message.cross = (object.cross !== undefined && object.cross !== null)
      ? TrackRef.fromPartial(object.cross)
      : undefined;
    return message;
  },
};

function createBaseTrackRef(): TrackRef {
  return { layer: 0, track: 0 };
}

export const TrackRef = {
  encode(message: TrackRef, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.layer !== 0) {
      writer.uint32(8).int64(message.layer);
    }
    if (message.track !== 0) {
      writer.uint32(16).int64(message.track);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): TrackRef {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTrackRef();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.layer = longToNumber(reader.int64() as Long);
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.track = longToNumber(reader.int64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): TrackRef {
    return {
      layer: isSet(object.layer) ? globalThis.Number(object.layer) : 0,
      track: isSet(object.track) ? globalThis.Number(object.track) : 0,
    };
  },

  toJSON(message: TrackRef): unknown {
    const obj: any = {};
    if (message.layer !== 0) {
      obj.layer = Math.round(message.layer);
    }
    if (message.track !== 0) {
      obj.track = Math.round(message.track);
    }
    return obj;
  },

  create(base?: DeepPartial<TrackRef>): TrackRef {
    return TrackRef.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<TrackRef>): TrackRef {
    const message = createBaseTrackRef();
    message.layer = object.layer ?? 0;
    message.track = object.track ?? 0;
    return message;
  },
};

function createBaseOutline(): Outline {
  return { x: [], y: [], metals: 0 };
}

export const Outline = {
  encode(message: Outline, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    writer.uint32(10).fork();
    for (const v of message.x) {
      writer.int64(v);
    }
    writer.ldelim();
    writer.uint32(18).fork();
    for (const v of message.y) {
      writer.int64(v);
    }
    writer.ldelim();
    if (message.metals !== 0) {
      writer.uint32(24).int64(message.metals);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Outline {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseOutline();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag === 8) {
            message.x.push(longToNumber(reader.int64() as Long));

            continue;
          }

          if (tag === 10) {
            const end2 = reader.uint32() + reader.pos;
            while (reader.pos < end2) {
              message.x.push(longToNumber(reader.int64() as Long));
            }

            continue;
          }

          break;
        case 2:
          if (tag === 16) {
            message.y.push(longToNumber(reader.int64() as Long));

            continue;
          }

          if (tag === 18) {
            const end2 = reader.uint32() + reader.pos;
            while (reader.pos < end2) {
              message.y.push(longToNumber(reader.int64() as Long));
            }

            continue;
          }

          break;
        case 3:
          if (tag !== 24) {
            break;
          }

          message.metals = longToNumber(reader.int64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Outline {
    return {
      x: globalThis.Array.isArray(object?.x) ? object.x.map((e: any) => globalThis.Number(e)) : [],
      y: globalThis.Array.isArray(object?.y) ? object.y.map((e: any) => globalThis.Number(e)) : [],
      metals: isSet(object.metals) ? globalThis.Number(object.metals) : 0,
    };
  },

  toJSON(message: Outline): unknown {
    const obj: any = {};
    if (message.x?.length) {
      obj.x = message.x.map((e) => Math.round(e));
    }
    if (message.y?.length) {
      obj.y = message.y.map((e) => Math.round(e));
    }
    if (message.metals !== 0) {
      obj.metals = Math.round(message.metals);
    }
    return obj;
  },

  create(base?: DeepPartial<Outline>): Outline {
    return Outline.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Outline>): Outline {
    const message = createBaseOutline();
    message.x = object.x?.map((e) => e) || [];
    message.y = object.y?.map((e) => e) || [];
    message.metals = object.metals ?? 0;
    return message;
  },
};

function createBaseAbstract(): Abstract {
  return { name: "", outline: undefined, ports: [] };
}

export const Abstract = {
  encode(message: Abstract, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.outline !== undefined) {
      Outline.encode(message.outline, writer.uint32(82).fork()).ldelim();
    }
    for (const v of message.ports) {
      AbstractPort.encode(v!, writer.uint32(162).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Abstract {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAbstract();
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

          message.outline = Outline.decode(reader, reader.uint32());
          continue;
        case 20:
          if (tag !== 162) {
            break;
          }

          message.ports.push(AbstractPort.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Abstract {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      outline: isSet(object.outline) ? Outline.fromJSON(object.outline) : undefined,
      ports: globalThis.Array.isArray(object?.ports) ? object.ports.map((e: any) => AbstractPort.fromJSON(e)) : [],
    };
  },

  toJSON(message: Abstract): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.outline !== undefined) {
      obj.outline = Outline.toJSON(message.outline);
    }
    if (message.ports?.length) {
      obj.ports = message.ports.map((e) => AbstractPort.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<Abstract>): Abstract {
    return Abstract.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Abstract>): Abstract {
    const message = createBaseAbstract();
    message.name = object.name ?? "";
    message.outline = (object.outline !== undefined && object.outline !== null)
      ? Outline.fromPartial(object.outline)
      : undefined;
    message.ports = object.ports?.map((e) => AbstractPort.fromPartial(e)) || [];
    return message;
  },
};

function createBaseAbstractPort(): AbstractPort {
  return { net: "", kind: undefined };
}

export const AbstractPort = {
  encode(message: AbstractPort, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.net !== "") {
      writer.uint32(10).string(message.net);
    }
    switch (message.kind?.$case) {
      case "edge":
        AbstractPort_EdgePort.encode(message.kind.edge, writer.uint32(82).fork()).ldelim();
        break;
      case "ztopEdge":
        AbstractPort_ZTopEdgePort.encode(message.kind.ztopEdge, writer.uint32(90).fork()).ldelim();
        break;
      case "ztopInner":
        AbstractPort_ZTopInner.encode(message.kind.ztopInner, writer.uint32(98).fork()).ldelim();
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): AbstractPort {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAbstractPort();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.net = reader.string();
          continue;
        case 10:
          if (tag !== 82) {
            break;
          }

          message.kind = { $case: "edge", edge: AbstractPort_EdgePort.decode(reader, reader.uint32()) };
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.kind = { $case: "ztopEdge", ztopEdge: AbstractPort_ZTopEdgePort.decode(reader, reader.uint32()) };
          continue;
        case 12:
          if (tag !== 98) {
            break;
          }

          message.kind = { $case: "ztopInner", ztopInner: AbstractPort_ZTopInner.decode(reader, reader.uint32()) };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): AbstractPort {
    return {
      net: isSet(object.net) ? globalThis.String(object.net) : "",
      kind: isSet(object.edge)
        ? { $case: "edge", edge: AbstractPort_EdgePort.fromJSON(object.edge) }
        : isSet(object.ztopEdge)
        ? { $case: "ztopEdge", ztopEdge: AbstractPort_ZTopEdgePort.fromJSON(object.ztopEdge) }
        : isSet(object.ztopInner)
        ? { $case: "ztopInner", ztopInner: AbstractPort_ZTopInner.fromJSON(object.ztopInner) }
        : undefined,
    };
  },

  toJSON(message: AbstractPort): unknown {
    const obj: any = {};
    if (message.net !== "") {
      obj.net = message.net;
    }
    if (message.kind?.$case === "edge") {
      obj.edge = AbstractPort_EdgePort.toJSON(message.kind.edge);
    }
    if (message.kind?.$case === "ztopEdge") {
      obj.ztopEdge = AbstractPort_ZTopEdgePort.toJSON(message.kind.ztopEdge);
    }
    if (message.kind?.$case === "ztopInner") {
      obj.ztopInner = AbstractPort_ZTopInner.toJSON(message.kind.ztopInner);
    }
    return obj;
  },

  create(base?: DeepPartial<AbstractPort>): AbstractPort {
    return AbstractPort.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<AbstractPort>): AbstractPort {
    const message = createBaseAbstractPort();
    message.net = object.net ?? "";
    if (object.kind?.$case === "edge" && object.kind?.edge !== undefined && object.kind?.edge !== null) {
      message.kind = { $case: "edge", edge: AbstractPort_EdgePort.fromPartial(object.kind.edge) };
    }
    if (object.kind?.$case === "ztopEdge" && object.kind?.ztopEdge !== undefined && object.kind?.ztopEdge !== null) {
      message.kind = { $case: "ztopEdge", ztopEdge: AbstractPort_ZTopEdgePort.fromPartial(object.kind.ztopEdge) };
    }
    if (object.kind?.$case === "ztopInner" && object.kind?.ztopInner !== undefined && object.kind?.ztopInner !== null) {
      message.kind = { $case: "ztopInner", ztopInner: AbstractPort_ZTopInner.fromPartial(object.kind.ztopInner) };
    }
    return message;
  },
};

function createBaseAbstractPort_EdgePort(): AbstractPort_EdgePort {
  return { track: undefined, side: 0 };
}

export const AbstractPort_EdgePort = {
  encode(message: AbstractPort_EdgePort, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.track !== undefined) {
      TrackRef.encode(message.track, writer.uint32(10).fork()).ldelim();
    }
    if (message.side !== 0) {
      writer.uint32(16).int32(message.side);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): AbstractPort_EdgePort {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAbstractPort_EdgePort();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.track = TrackRef.decode(reader, reader.uint32());
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.side = reader.int32() as any;
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): AbstractPort_EdgePort {
    return {
      track: isSet(object.track) ? TrackRef.fromJSON(object.track) : undefined,
      side: isSet(object.side) ? abstractPort_PortSideFromJSON(object.side) : 0,
    };
  },

  toJSON(message: AbstractPort_EdgePort): unknown {
    const obj: any = {};
    if (message.track !== undefined) {
      obj.track = TrackRef.toJSON(message.track);
    }
    if (message.side !== 0) {
      obj.side = abstractPort_PortSideToJSON(message.side);
    }
    return obj;
  },

  create(base?: DeepPartial<AbstractPort_EdgePort>): AbstractPort_EdgePort {
    return AbstractPort_EdgePort.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<AbstractPort_EdgePort>): AbstractPort_EdgePort {
    const message = createBaseAbstractPort_EdgePort();
    message.track = (object.track !== undefined && object.track !== null)
      ? TrackRef.fromPartial(object.track)
      : undefined;
    message.side = object.side ?? 0;
    return message;
  },
};

function createBaseAbstractPort_ZTopEdgePort(): AbstractPort_ZTopEdgePort {
  return { track: 0, side: 0, into: undefined };
}

export const AbstractPort_ZTopEdgePort = {
  encode(message: AbstractPort_ZTopEdgePort, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.track !== 0) {
      writer.uint32(8).int64(message.track);
    }
    if (message.side !== 0) {
      writer.uint32(16).int32(message.side);
    }
    if (message.into !== undefined) {
      TrackRef.encode(message.into, writer.uint32(26).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): AbstractPort_ZTopEdgePort {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAbstractPort_ZTopEdgePort();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.track = longToNumber(reader.int64() as Long);
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.side = reader.int32() as any;
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.into = TrackRef.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): AbstractPort_ZTopEdgePort {
    return {
      track: isSet(object.track) ? globalThis.Number(object.track) : 0,
      side: isSet(object.side) ? abstractPort_PortSideFromJSON(object.side) : 0,
      into: isSet(object.into) ? TrackRef.fromJSON(object.into) : undefined,
    };
  },

  toJSON(message: AbstractPort_ZTopEdgePort): unknown {
    const obj: any = {};
    if (message.track !== 0) {
      obj.track = Math.round(message.track);
    }
    if (message.side !== 0) {
      obj.side = abstractPort_PortSideToJSON(message.side);
    }
    if (message.into !== undefined) {
      obj.into = TrackRef.toJSON(message.into);
    }
    return obj;
  },

  create(base?: DeepPartial<AbstractPort_ZTopEdgePort>): AbstractPort_ZTopEdgePort {
    return AbstractPort_ZTopEdgePort.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<AbstractPort_ZTopEdgePort>): AbstractPort_ZTopEdgePort {
    const message = createBaseAbstractPort_ZTopEdgePort();
    message.track = object.track ?? 0;
    message.side = object.side ?? 0;
    message.into = (object.into !== undefined && object.into !== null) ? TrackRef.fromPartial(object.into) : undefined;
    return message;
  },
};

function createBaseAbstractPort_ZTopInner(): AbstractPort_ZTopInner {
  return { locs: [] };
}

export const AbstractPort_ZTopInner = {
  encode(message: AbstractPort_ZTopInner, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    for (const v of message.locs) {
      TrackCross.encode(v!, writer.uint32(10).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): AbstractPort_ZTopInner {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAbstractPort_ZTopInner();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.locs.push(TrackCross.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): AbstractPort_ZTopInner {
    return { locs: globalThis.Array.isArray(object?.locs) ? object.locs.map((e: any) => TrackCross.fromJSON(e)) : [] };
  },

  toJSON(message: AbstractPort_ZTopInner): unknown {
    const obj: any = {};
    if (message.locs?.length) {
      obj.locs = message.locs.map((e) => TrackCross.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<AbstractPort_ZTopInner>): AbstractPort_ZTopInner {
    return AbstractPort_ZTopInner.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<AbstractPort_ZTopInner>): AbstractPort_ZTopInner {
    const message = createBaseAbstractPort_ZTopInner();
    message.locs = object.locs?.map((e) => TrackCross.fromPartial(e)) || [];
    return message;
  },
};

function createBaseInstance(): Instance {
  return { name: "", cell: undefined, loc: undefined, reflectHoriz: false, reflectVert: false };
}

export const Instance = {
  encode(message: Instance, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.cell !== undefined) {
      Reference.encode(message.cell, writer.uint32(26).fork()).ldelim();
    }
    if (message.loc !== undefined) {
      Place.encode(message.loc, writer.uint32(34).fork()).ldelim();
    }
    if (message.reflectHoriz !== false) {
      writer.uint32(48).bool(message.reflectHoriz);
    }
    if (message.reflectVert !== false) {
      writer.uint32(56).bool(message.reflectVert);
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
        case 3:
          if (tag !== 26) {
            break;
          }

          message.cell = Reference.decode(reader, reader.uint32());
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.loc = Place.decode(reader, reader.uint32());
          continue;
        case 6:
          if (tag !== 48) {
            break;
          }

          message.reflectHoriz = reader.bool();
          continue;
        case 7:
          if (tag !== 56) {
            break;
          }

          message.reflectVert = reader.bool();
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
      cell: isSet(object.cell) ? Reference.fromJSON(object.cell) : undefined,
      loc: isSet(object.loc) ? Place.fromJSON(object.loc) : undefined,
      reflectHoriz: isSet(object.reflectHoriz) ? globalThis.Boolean(object.reflectHoriz) : false,
      reflectVert: isSet(object.reflectVert) ? globalThis.Boolean(object.reflectVert) : false,
    };
  },

  toJSON(message: Instance): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.cell !== undefined) {
      obj.cell = Reference.toJSON(message.cell);
    }
    if (message.loc !== undefined) {
      obj.loc = Place.toJSON(message.loc);
    }
    if (message.reflectHoriz !== false) {
      obj.reflectHoriz = message.reflectHoriz;
    }
    if (message.reflectVert !== false) {
      obj.reflectVert = message.reflectVert;
    }
    return obj;
  },

  create(base?: DeepPartial<Instance>): Instance {
    return Instance.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Instance>): Instance {
    const message = createBaseInstance();
    message.name = object.name ?? "";
    message.cell = (object.cell !== undefined && object.cell !== null) ? Reference.fromPartial(object.cell) : undefined;
    message.loc = (object.loc !== undefined && object.loc !== null) ? Place.fromPartial(object.loc) : undefined;
    message.reflectHoriz = object.reflectHoriz ?? false;
    message.reflectVert = object.reflectVert ?? false;
    return message;
  },
};

function createBasePlace(): Place {
  return { place: undefined };
}

export const Place = {
  encode(message: Place, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    switch (message.place?.$case) {
      case "abs":
        Point.encode(message.place.abs, writer.uint32(10).fork()).ldelim();
        break;
      case "rel":
        RelPlace.encode(message.place.rel, writer.uint32(18).fork()).ldelim();
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Place {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePlace();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.place = { $case: "abs", abs: Point.decode(reader, reader.uint32()) };
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.place = { $case: "rel", rel: RelPlace.decode(reader, reader.uint32()) };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Place {
    return {
      place: isSet(object.abs)
        ? { $case: "abs", abs: Point.fromJSON(object.abs) }
        : isSet(object.rel)
        ? { $case: "rel", rel: RelPlace.fromJSON(object.rel) }
        : undefined,
    };
  },

  toJSON(message: Place): unknown {
    const obj: any = {};
    if (message.place?.$case === "abs") {
      obj.abs = Point.toJSON(message.place.abs);
    }
    if (message.place?.$case === "rel") {
      obj.rel = RelPlace.toJSON(message.place.rel);
    }
    return obj;
  },

  create(base?: DeepPartial<Place>): Place {
    return Place.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Place>): Place {
    const message = createBasePlace();
    if (object.place?.$case === "abs" && object.place?.abs !== undefined && object.place?.abs !== null) {
      message.place = { $case: "abs", abs: Point.fromPartial(object.place.abs) };
    }
    if (object.place?.$case === "rel" && object.place?.rel !== undefined && object.place?.rel !== null) {
      message.place = { $case: "rel", rel: RelPlace.fromPartial(object.place.rel) };
    }
    return message;
  },
};

function createBaseRelPlace(): RelPlace {
  return {};
}

export const RelPlace = {
  encode(_: RelPlace, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): RelPlace {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseRelPlace();
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

  fromJSON(_: any): RelPlace {
    return {};
  },

  toJSON(_: RelPlace): unknown {
    const obj: any = {};
    return obj;
  },

  create(base?: DeepPartial<RelPlace>): RelPlace {
    return RelPlace.fromPartial(base ?? {});
  },
  fromPartial(_: DeepPartial<RelPlace>): RelPlace {
    const message = createBaseRelPlace();
    return message;
  },
};

function createBaseStack(): Stack {
  return { units: 0, prim: undefined, metals: [], vias: [], boundaryLayer: undefined };
}

export const Stack = {
  encode(message: Stack, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.units !== 0) {
      writer.uint32(8).int32(message.units);
    }
    if (message.prim !== undefined) {
      PrimitiveLayer.encode(message.prim, writer.uint32(18).fork()).ldelim();
    }
    for (const v of message.metals) {
      MetalLayer.encode(v!, writer.uint32(26).fork()).ldelim();
    }
    for (const v of message.vias) {
      ViaLayer.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    if (message.boundaryLayer !== undefined) {
      Layer.encode(message.boundaryLayer, writer.uint32(90).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Stack {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseStack();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.units = reader.int32() as any;
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.prim = PrimitiveLayer.decode(reader, reader.uint32());
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.metals.push(MetalLayer.decode(reader, reader.uint32()));
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.vias.push(ViaLayer.decode(reader, reader.uint32()));
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.boundaryLayer = Layer.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Stack {
    return {
      units: isSet(object.units) ? unitsFromJSON(object.units) : 0,
      prim: isSet(object.prim) ? PrimitiveLayer.fromJSON(object.prim) : undefined,
      metals: globalThis.Array.isArray(object?.metals) ? object.metals.map((e: any) => MetalLayer.fromJSON(e)) : [],
      vias: globalThis.Array.isArray(object?.vias) ? object.vias.map((e: any) => ViaLayer.fromJSON(e)) : [],
      boundaryLayer: isSet(object.boundaryLayer) ? Layer.fromJSON(object.boundaryLayer) : undefined,
    };
  },

  toJSON(message: Stack): unknown {
    const obj: any = {};
    if (message.units !== 0) {
      obj.units = unitsToJSON(message.units);
    }
    if (message.prim !== undefined) {
      obj.prim = PrimitiveLayer.toJSON(message.prim);
    }
    if (message.metals?.length) {
      obj.metals = message.metals.map((e) => MetalLayer.toJSON(e));
    }
    if (message.vias?.length) {
      obj.vias = message.vias.map((e) => ViaLayer.toJSON(e));
    }
    if (message.boundaryLayer !== undefined) {
      obj.boundaryLayer = Layer.toJSON(message.boundaryLayer);
    }
    return obj;
  },

  create(base?: DeepPartial<Stack>): Stack {
    return Stack.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Stack>): Stack {
    const message = createBaseStack();
    message.units = object.units ?? 0;
    message.prim = (object.prim !== undefined && object.prim !== null)
      ? PrimitiveLayer.fromPartial(object.prim)
      : undefined;
    message.metals = object.metals?.map((e) => MetalLayer.fromPartial(e)) || [];
    message.vias = object.vias?.map((e) => ViaLayer.fromPartial(e)) || [];
    message.boundaryLayer = (object.boundaryLayer !== undefined && object.boundaryLayer !== null)
      ? Layer.fromPartial(object.boundaryLayer)
      : undefined;
    return message;
  },
};

function createBaseLayerEnum(): LayerEnum {
  return { type: 0, index: 0 };
}

export const LayerEnum = {
  encode(message: LayerEnum, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.type !== 0) {
      writer.uint32(8).int32(message.type);
    }
    if (message.index !== 0) {
      writer.uint32(16).int64(message.index);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): LayerEnum {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLayerEnum();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.type = reader.int32() as any;
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.index = longToNumber(reader.int64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): LayerEnum {
    return {
      type: isSet(object.type) ? layerEnum_LayerTypeFromJSON(object.type) : 0,
      index: isSet(object.index) ? globalThis.Number(object.index) : 0,
    };
  },

  toJSON(message: LayerEnum): unknown {
    const obj: any = {};
    if (message.type !== 0) {
      obj.type = layerEnum_LayerTypeToJSON(message.type);
    }
    if (message.index !== 0) {
      obj.index = Math.round(message.index);
    }
    return obj;
  },

  create(base?: DeepPartial<LayerEnum>): LayerEnum {
    return LayerEnum.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<LayerEnum>): LayerEnum {
    const message = createBaseLayerEnum();
    message.type = object.type ?? 0;
    message.index = object.index ?? 0;
    return message;
  },
};

function createBaseMetalLayer(): MetalLayer {
  return { name: "", dir: 0, cutsize: 0, entries: [], offset: 0, overlap: 0, flip: false, prim: 0, raw: undefined };
}

export const MetalLayer = {
  encode(message: MetalLayer, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.dir !== 0) {
      writer.uint32(16).int32(message.dir);
    }
    if (message.cutsize !== 0) {
      writer.uint32(24).int64(message.cutsize);
    }
    for (const v of message.entries) {
      TrackSpec.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    if (message.offset !== 0) {
      writer.uint32(40).int64(message.offset);
    }
    if (message.overlap !== 0) {
      writer.uint32(48).int64(message.overlap);
    }
    if (message.flip !== false) {
      writer.uint32(56).bool(message.flip);
    }
    if (message.prim !== 0) {
      writer.uint32(64).int32(message.prim);
    }
    if (message.raw !== undefined) {
      Layer.encode(message.raw, writer.uint32(90).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): MetalLayer {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseMetalLayer();
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

          message.dir = reader.int32() as any;
          continue;
        case 3:
          if (tag !== 24) {
            break;
          }

          message.cutsize = longToNumber(reader.int64() as Long);
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.entries.push(TrackSpec.decode(reader, reader.uint32()));
          continue;
        case 5:
          if (tag !== 40) {
            break;
          }

          message.offset = longToNumber(reader.int64() as Long);
          continue;
        case 6:
          if (tag !== 48) {
            break;
          }

          message.overlap = longToNumber(reader.int64() as Long);
          continue;
        case 7:
          if (tag !== 56) {
            break;
          }

          message.flip = reader.bool();
          continue;
        case 8:
          if (tag !== 64) {
            break;
          }

          message.prim = reader.int32() as any;
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.raw = Layer.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): MetalLayer {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      dir: isSet(object.dir) ? metalLayer_DirFromJSON(object.dir) : 0,
      cutsize: isSet(object.cutsize) ? globalThis.Number(object.cutsize) : 0,
      entries: globalThis.Array.isArray(object?.entries) ? object.entries.map((e: any) => TrackSpec.fromJSON(e)) : [],
      offset: isSet(object.offset) ? globalThis.Number(object.offset) : 0,
      overlap: isSet(object.overlap) ? globalThis.Number(object.overlap) : 0,
      flip: isSet(object.flip) ? globalThis.Boolean(object.flip) : false,
      prim: isSet(object.prim) ? metalLayer_PrimitiveModeFromJSON(object.prim) : 0,
      raw: isSet(object.raw) ? Layer.fromJSON(object.raw) : undefined,
    };
  },

  toJSON(message: MetalLayer): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.dir !== 0) {
      obj.dir = metalLayer_DirToJSON(message.dir);
    }
    if (message.cutsize !== 0) {
      obj.cutsize = Math.round(message.cutsize);
    }
    if (message.entries?.length) {
      obj.entries = message.entries.map((e) => TrackSpec.toJSON(e));
    }
    if (message.offset !== 0) {
      obj.offset = Math.round(message.offset);
    }
    if (message.overlap !== 0) {
      obj.overlap = Math.round(message.overlap);
    }
    if (message.flip !== false) {
      obj.flip = message.flip;
    }
    if (message.prim !== 0) {
      obj.prim = metalLayer_PrimitiveModeToJSON(message.prim);
    }
    if (message.raw !== undefined) {
      obj.raw = Layer.toJSON(message.raw);
    }
    return obj;
  },

  create(base?: DeepPartial<MetalLayer>): MetalLayer {
    return MetalLayer.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<MetalLayer>): MetalLayer {
    const message = createBaseMetalLayer();
    message.name = object.name ?? "";
    message.dir = object.dir ?? 0;
    message.cutsize = object.cutsize ?? 0;
    message.entries = object.entries?.map((e) => TrackSpec.fromPartial(e)) || [];
    message.offset = object.offset ?? 0;
    message.overlap = object.overlap ?? 0;
    message.flip = object.flip ?? false;
    message.prim = object.prim ?? 0;
    message.raw = (object.raw !== undefined && object.raw !== null) ? Layer.fromPartial(object.raw) : undefined;
    return message;
  },
};

function createBaseViaLayer(): ViaLayer {
  return { name: "", top: undefined, bot: undefined, size: undefined, raw: undefined };
}

export const ViaLayer = {
  encode(message: ViaLayer, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.top !== undefined) {
      LayerEnum.encode(message.top, writer.uint32(18).fork()).ldelim();
    }
    if (message.bot !== undefined) {
      LayerEnum.encode(message.bot, writer.uint32(26).fork()).ldelim();
    }
    if (message.size !== undefined) {
      Xy.encode(message.size, writer.uint32(34).fork()).ldelim();
    }
    if (message.raw !== undefined) {
      Layer.encode(message.raw, writer.uint32(90).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): ViaLayer {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseViaLayer();
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

          message.top = LayerEnum.decode(reader, reader.uint32());
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.bot = LayerEnum.decode(reader, reader.uint32());
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.size = Xy.decode(reader, reader.uint32());
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.raw = Layer.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): ViaLayer {
    return {
      name: isSet(object.name) ? globalThis.String(object.name) : "",
      top: isSet(object.top) ? LayerEnum.fromJSON(object.top) : undefined,
      bot: isSet(object.bot) ? LayerEnum.fromJSON(object.bot) : undefined,
      size: isSet(object.size) ? Xy.fromJSON(object.size) : undefined,
      raw: isSet(object.raw) ? Layer.fromJSON(object.raw) : undefined,
    };
  },

  toJSON(message: ViaLayer): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.top !== undefined) {
      obj.top = LayerEnum.toJSON(message.top);
    }
    if (message.bot !== undefined) {
      obj.bot = LayerEnum.toJSON(message.bot);
    }
    if (message.size !== undefined) {
      obj.size = Xy.toJSON(message.size);
    }
    if (message.raw !== undefined) {
      obj.raw = Layer.toJSON(message.raw);
    }
    return obj;
  },

  create(base?: DeepPartial<ViaLayer>): ViaLayer {
    return ViaLayer.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<ViaLayer>): ViaLayer {
    const message = createBaseViaLayer();
    message.name = object.name ?? "";
    message.top = (object.top !== undefined && object.top !== null) ? LayerEnum.fromPartial(object.top) : undefined;
    message.bot = (object.bot !== undefined && object.bot !== null) ? LayerEnum.fromPartial(object.bot) : undefined;
    message.size = (object.size !== undefined && object.size !== null) ? Xy.fromPartial(object.size) : undefined;
    message.raw = (object.raw !== undefined && object.raw !== null) ? Layer.fromPartial(object.raw) : undefined;
    return message;
  },
};

function createBasePrimitiveLayer(): PrimitiveLayer {
  return { pitches: undefined };
}

export const PrimitiveLayer = {
  encode(message: PrimitiveLayer, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.pitches !== undefined) {
      Xy.encode(message.pitches, writer.uint32(10).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): PrimitiveLayer {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePrimitiveLayer();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.pitches = Xy.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): PrimitiveLayer {
    return { pitches: isSet(object.pitches) ? Xy.fromJSON(object.pitches) : undefined };
  },

  toJSON(message: PrimitiveLayer): unknown {
    const obj: any = {};
    if (message.pitches !== undefined) {
      obj.pitches = Xy.toJSON(message.pitches);
    }
    return obj;
  },

  create(base?: DeepPartial<PrimitiveLayer>): PrimitiveLayer {
    return PrimitiveLayer.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<PrimitiveLayer>): PrimitiveLayer {
    const message = createBasePrimitiveLayer();
    message.pitches = (object.pitches !== undefined && object.pitches !== null)
      ? Xy.fromPartial(object.pitches)
      : undefined;
    return message;
  },
};

function createBaseTrackSpec(): TrackSpec {
  return { spec: undefined };
}

export const TrackSpec = {
  encode(message: TrackSpec, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    switch (message.spec?.$case) {
      case "entry":
        TrackSpec_TrackEntry.encode(message.spec.entry, writer.uint32(10).fork()).ldelim();
        break;
      case "repeat":
        TrackSpec_Repeat.encode(message.spec.repeat, writer.uint32(18).fork()).ldelim();
        break;
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): TrackSpec {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTrackSpec();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.spec = { $case: "entry", entry: TrackSpec_TrackEntry.decode(reader, reader.uint32()) };
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.spec = { $case: "repeat", repeat: TrackSpec_Repeat.decode(reader, reader.uint32()) };
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): TrackSpec {
    return {
      spec: isSet(object.entry)
        ? { $case: "entry", entry: TrackSpec_TrackEntry.fromJSON(object.entry) }
        : isSet(object.repeat)
        ? { $case: "repeat", repeat: TrackSpec_Repeat.fromJSON(object.repeat) }
        : undefined,
    };
  },

  toJSON(message: TrackSpec): unknown {
    const obj: any = {};
    if (message.spec?.$case === "entry") {
      obj.entry = TrackSpec_TrackEntry.toJSON(message.spec.entry);
    }
    if (message.spec?.$case === "repeat") {
      obj.repeat = TrackSpec_Repeat.toJSON(message.spec.repeat);
    }
    return obj;
  },

  create(base?: DeepPartial<TrackSpec>): TrackSpec {
    return TrackSpec.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<TrackSpec>): TrackSpec {
    const message = createBaseTrackSpec();
    if (object.spec?.$case === "entry" && object.spec?.entry !== undefined && object.spec?.entry !== null) {
      message.spec = { $case: "entry", entry: TrackSpec_TrackEntry.fromPartial(object.spec.entry) };
    }
    if (object.spec?.$case === "repeat" && object.spec?.repeat !== undefined && object.spec?.repeat !== null) {
      message.spec = { $case: "repeat", repeat: TrackSpec_Repeat.fromPartial(object.spec.repeat) };
    }
    return message;
  },
};

function createBaseTrackSpec_TrackEntry(): TrackSpec_TrackEntry {
  return { ttype: 0, width: 0 };
}

export const TrackSpec_TrackEntry = {
  encode(message: TrackSpec_TrackEntry, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.ttype !== 0) {
      writer.uint32(8).int32(message.ttype);
    }
    if (message.width !== 0) {
      writer.uint32(16).int64(message.width);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): TrackSpec_TrackEntry {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTrackSpec_TrackEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.ttype = reader.int32() as any;
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

  fromJSON(object: any): TrackSpec_TrackEntry {
    return {
      ttype: isSet(object.ttype) ? trackSpec_TrackEntry_TrackTypeFromJSON(object.ttype) : 0,
      width: isSet(object.width) ? globalThis.Number(object.width) : 0,
    };
  },

  toJSON(message: TrackSpec_TrackEntry): unknown {
    const obj: any = {};
    if (message.ttype !== 0) {
      obj.ttype = trackSpec_TrackEntry_TrackTypeToJSON(message.ttype);
    }
    if (message.width !== 0) {
      obj.width = Math.round(message.width);
    }
    return obj;
  },

  create(base?: DeepPartial<TrackSpec_TrackEntry>): TrackSpec_TrackEntry {
    return TrackSpec_TrackEntry.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<TrackSpec_TrackEntry>): TrackSpec_TrackEntry {
    const message = createBaseTrackSpec_TrackEntry();
    message.ttype = object.ttype ?? 0;
    message.width = object.width ?? 0;
    return message;
  },
};

function createBaseTrackSpec_Repeat(): TrackSpec_Repeat {
  return { entries: [], nrep: 0 };
}

export const TrackSpec_Repeat = {
  encode(message: TrackSpec_Repeat, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    for (const v of message.entries) {
      TrackSpec_TrackEntry.encode(v!, writer.uint32(10).fork()).ldelim();
    }
    if (message.nrep !== 0) {
      writer.uint32(16).int64(message.nrep);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): TrackSpec_Repeat {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTrackSpec_Repeat();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.entries.push(TrackSpec_TrackEntry.decode(reader, reader.uint32()));
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.nrep = longToNumber(reader.int64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): TrackSpec_Repeat {
    return {
      entries: globalThis.Array.isArray(object?.entries)
        ? object.entries.map((e: any) => TrackSpec_TrackEntry.fromJSON(e))
        : [],
      nrep: isSet(object.nrep) ? globalThis.Number(object.nrep) : 0,
    };
  },

  toJSON(message: TrackSpec_Repeat): unknown {
    const obj: any = {};
    if (message.entries?.length) {
      obj.entries = message.entries.map((e) => TrackSpec_TrackEntry.toJSON(e));
    }
    if (message.nrep !== 0) {
      obj.nrep = Math.round(message.nrep);
    }
    return obj;
  },

  create(base?: DeepPartial<TrackSpec_Repeat>): TrackSpec_Repeat {
    return TrackSpec_Repeat.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<TrackSpec_Repeat>): TrackSpec_Repeat {
    const message = createBaseTrackSpec_Repeat();
    message.entries = object.entries?.map((e) => TrackSpec_TrackEntry.fromPartial(e)) || [];
    message.nrep = object.nrep ?? 0;
    return message;
  },
};

function createBaseXy(): Xy {
  return { x: 0, y: 0 };
}

export const Xy = {
  encode(message: Xy, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.x !== 0) {
      writer.uint32(8).int64(message.x);
    }
    if (message.y !== 0) {
      writer.uint32(16).int64(message.y);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Xy {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseXy();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.x = longToNumber(reader.int64() as Long);
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.y = longToNumber(reader.int64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Xy {
    return {
      x: isSet(object.x) ? globalThis.Number(object.x) : 0,
      y: isSet(object.y) ? globalThis.Number(object.y) : 0,
    };
  },

  toJSON(message: Xy): unknown {
    const obj: any = {};
    if (message.x !== 0) {
      obj.x = Math.round(message.x);
    }
    if (message.y !== 0) {
      obj.y = Math.round(message.y);
    }
    return obj;
  },

  create(base?: DeepPartial<Xy>): Xy {
    return Xy.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Xy>): Xy {
    const message = createBaseXy();
    message.x = object.x ?? 0;
    message.y = object.y ?? 0;
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
