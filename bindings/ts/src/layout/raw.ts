/* eslint-disable */
import Long from "long";
import _m0 from "protobufjs/minimal";
import { Interface, Module } from "../circuit";
import { AuthorMetadata, Reference } from "../utils";

/** Distance unit enumeration */
export enum Units {
  MICRO = 0,
  NANO = 1,
  ANGSTROM = 2,
  UNRECOGNIZED = -1,
}

export function unitsFromJSON(object: any): Units {
  switch (object) {
    case 0:
    case "MICRO":
      return Units.MICRO;
    case 1:
    case "NANO":
      return Units.NANO;
    case 2:
    case "ANGSTROM":
      return Units.ANGSTROM;
    case -1:
    case "UNRECOGNIZED":
    default:
      return Units.UNRECOGNIZED;
  }
}

export function unitsToJSON(object: Units): string {
  switch (object) {
    case Units.MICRO:
      return "MICRO";
    case Units.NANO:
      return "NANO";
    case Units.ANGSTROM:
      return "ANGSTROM";
    case Units.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/**
 * # Point
 * An (x,y) point in Cartesian layout space.
 */
export interface Point {
  x: number;
  y: number;
}

/**
 * # Layer-Purpose Pair
 * As in many legacy layout systems, layers are described by two numbers:
 * * `number` describes describes a "physical layer". Example enumerated values might include "metal3", "diffusion".
 * * `purpose` describes an "intent" of the [Layer]. Typical enumerated values include pins, labels, and drawings.
 */
export interface Layer {
  number: number;
  purpose: number;
}

/** # Rectangle Primitive */
export interface Rectangle {
  /** Net Name */
  net: string;
  /** The lower-left corner of the rectangle. */
  lowerLeft: Point | undefined;
  width: number;
  height: number;
}

/** # Polygon Primitive */
export interface Polygon {
  /** Net Name */
  net: string;
  /**
   * List of Vertices
   * `Polygons` implicitly "close themselves", i.e. the first vertex-location need not be repeated as the last.
   * N-sided `Polygons` therefore require `N` elements in their `vertices` array.
   */
  vertices: Point[];
}

/**
 * # Path Primitive
 * A single-layer, fixed-width path through a series of points
 */
export interface Path {
  /** Net Name */
  net: string;
  /** Points */
  points: Point[];
  /** Width */
  width: number;
}

/**
 * # LayerShapes
 * Container for Geometric Shapes on a single `Layer`
 */
export interface LayerShapes {
  layer: Layer | undefined;
  rectangles: Rectangle[];
  polygons: Polygon[];
  paths: Path[];
}

/**
 * # Text Annotation
 *
 * Note `TextElements` are "layer-less", i.e. they do not sit on different layers, and do not describe connectivity or generate pins.
 * These are purely annotations in the sense of "design notes".
 */
export interface TextElement {
  /** String Value */
  string: string;
  /** Location */
  loc: Point | undefined;
}

/** # Layout-Cell Instance */
export interface Instance {
  /** Instance Name */
  name: string;
  /** Cell Reference */
  cell:
    | Reference
    | undefined;
  /**
   * Location of the defined Cell's origin
   * this location holds regardless of reflection or rotation
   */
  originLocation:
    | Point
    | undefined;
  /**
   * Vertical reflection about x-axis,
   * applied *before* rotation.
   */
  reflectVert: boolean;
  /**
   * Angle of rotation (degrees),
   * Clockwise and applied *after* reflection
   */
  rotationClockwiseDegrees: number;
}

/**
 * # Layout Cell
 *
 * The most common element of layout re-use.
 * Comprises a named set of geometric elements and [Instance]s of other [Layout]s.
 */
export interface Layout {
  /** Cell Name */
  name: string;
  /** Shapes, grouped by layer */
  shapes: LayerShapes[];
  /** Instances of other cells */
  instances: Instance[];
  /** Text Annotations */
  annotations: TextElement[];
}

/**
 * # Abstract Layout View
 *
 * Defines the physical interface to a [Cell], including ports and internal blockages,
 * omitting internal implementation details.
 */
export interface Abstract {
  /** Cell Name */
  name: string;
  /** Outline */
  outline:
    | Polygon
    | undefined;
  /** Ports */
  ports: AbstractPort[];
  /** Blockages */
  blockages: LayerShapes[];
}

/**
 * # Abstract Port
 * Combination of a net and set of shapes
 */
export interface AbstractPort {
  /** Port Name */
  net: string;
  /** Shapes, grouped by layer */
  shapes: LayerShapes[];
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
  /** Circuit Module */
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
 * # Library
 * A collection of cells and asssociated meta-data.
 */
export interface Library {
  /** Library Name / Domain */
  domain: string;
  /** Distance Units */
  units: Units;
  /** Cell Definitions */
  cells: Cell[];
  /** Author Information */
  author: AuthorMetadata | undefined;
}

function createBasePoint(): Point {
  return { x: 0, y: 0 };
}

export const Point = {
  encode(message: Point, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.x !== 0) {
      writer.uint32(8).int64(message.x);
    }
    if (message.y !== 0) {
      writer.uint32(16).int64(message.y);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Point {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePoint();
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

  fromJSON(object: any): Point {
    return {
      x: isSet(object.x) ? globalThis.Number(object.x) : 0,
      y: isSet(object.y) ? globalThis.Number(object.y) : 0,
    };
  },

  toJSON(message: Point): unknown {
    const obj: any = {};
    if (message.x !== 0) {
      obj.x = Math.round(message.x);
    }
    if (message.y !== 0) {
      obj.y = Math.round(message.y);
    }
    return obj;
  },

  create(base?: DeepPartial<Point>): Point {
    return Point.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Point>): Point {
    const message = createBasePoint();
    message.x = object.x ?? 0;
    message.y = object.y ?? 0;
    return message;
  },
};

function createBaseLayer(): Layer {
  return { number: 0, purpose: 0 };
}

export const Layer = {
  encode(message: Layer, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.number !== 0) {
      writer.uint32(8).int64(message.number);
    }
    if (message.purpose !== 0) {
      writer.uint32(16).int64(message.purpose);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Layer {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLayer();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.number = longToNumber(reader.int64() as Long);
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.purpose = longToNumber(reader.int64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Layer {
    return {
      number: isSet(object.number) ? globalThis.Number(object.number) : 0,
      purpose: isSet(object.purpose) ? globalThis.Number(object.purpose) : 0,
    };
  },

  toJSON(message: Layer): unknown {
    const obj: any = {};
    if (message.number !== 0) {
      obj.number = Math.round(message.number);
    }
    if (message.purpose !== 0) {
      obj.purpose = Math.round(message.purpose);
    }
    return obj;
  },

  create(base?: DeepPartial<Layer>): Layer {
    return Layer.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Layer>): Layer {
    const message = createBaseLayer();
    message.number = object.number ?? 0;
    message.purpose = object.purpose ?? 0;
    return message;
  },
};

function createBaseRectangle(): Rectangle {
  return { net: "", lowerLeft: undefined, width: 0, height: 0 };
}

export const Rectangle = {
  encode(message: Rectangle, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.net !== "") {
      writer.uint32(10).string(message.net);
    }
    if (message.lowerLeft !== undefined) {
      Point.encode(message.lowerLeft, writer.uint32(18).fork()).ldelim();
    }
    if (message.width !== 0) {
      writer.uint32(24).int64(message.width);
    }
    if (message.height !== 0) {
      writer.uint32(32).int64(message.height);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Rectangle {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseRectangle();
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

          message.lowerLeft = Point.decode(reader, reader.uint32());
          continue;
        case 3:
          if (tag !== 24) {
            break;
          }

          message.width = longToNumber(reader.int64() as Long);
          continue;
        case 4:
          if (tag !== 32) {
            break;
          }

          message.height = longToNumber(reader.int64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Rectangle {
    return {
      net: isSet(object.net) ? globalThis.String(object.net) : "",
      lowerLeft: isSet(object.lowerLeft) ? Point.fromJSON(object.lowerLeft) : undefined,
      width: isSet(object.width) ? globalThis.Number(object.width) : 0,
      height: isSet(object.height) ? globalThis.Number(object.height) : 0,
    };
  },

  toJSON(message: Rectangle): unknown {
    const obj: any = {};
    if (message.net !== "") {
      obj.net = message.net;
    }
    if (message.lowerLeft !== undefined) {
      obj.lowerLeft = Point.toJSON(message.lowerLeft);
    }
    if (message.width !== 0) {
      obj.width = Math.round(message.width);
    }
    if (message.height !== 0) {
      obj.height = Math.round(message.height);
    }
    return obj;
  },

  create(base?: DeepPartial<Rectangle>): Rectangle {
    return Rectangle.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Rectangle>): Rectangle {
    const message = createBaseRectangle();
    message.net = object.net ?? "";
    message.lowerLeft = (object.lowerLeft !== undefined && object.lowerLeft !== null)
      ? Point.fromPartial(object.lowerLeft)
      : undefined;
    message.width = object.width ?? 0;
    message.height = object.height ?? 0;
    return message;
  },
};

function createBasePolygon(): Polygon {
  return { net: "", vertices: [] };
}

export const Polygon = {
  encode(message: Polygon, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.net !== "") {
      writer.uint32(10).string(message.net);
    }
    for (const v of message.vertices) {
      Point.encode(v!, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Polygon {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePolygon();
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

          message.vertices.push(Point.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Polygon {
    return {
      net: isSet(object.net) ? globalThis.String(object.net) : "",
      vertices: globalThis.Array.isArray(object?.vertices) ? object.vertices.map((e: any) => Point.fromJSON(e)) : [],
    };
  },

  toJSON(message: Polygon): unknown {
    const obj: any = {};
    if (message.net !== "") {
      obj.net = message.net;
    }
    if (message.vertices?.length) {
      obj.vertices = message.vertices.map((e) => Point.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<Polygon>): Polygon {
    return Polygon.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Polygon>): Polygon {
    const message = createBasePolygon();
    message.net = object.net ?? "";
    message.vertices = object.vertices?.map((e) => Point.fromPartial(e)) || [];
    return message;
  },
};

function createBasePath(): Path {
  return { net: "", points: [], width: 0 };
}

export const Path = {
  encode(message: Path, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.net !== "") {
      writer.uint32(10).string(message.net);
    }
    for (const v of message.points) {
      Point.encode(v!, writer.uint32(18).fork()).ldelim();
    }
    if (message.width !== 0) {
      writer.uint32(24).int64(message.width);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Path {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePath();
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

          message.points.push(Point.decode(reader, reader.uint32()));
          continue;
        case 3:
          if (tag !== 24) {
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

  fromJSON(object: any): Path {
    return {
      net: isSet(object.net) ? globalThis.String(object.net) : "",
      points: globalThis.Array.isArray(object?.points) ? object.points.map((e: any) => Point.fromJSON(e)) : [],
      width: isSet(object.width) ? globalThis.Number(object.width) : 0,
    };
  },

  toJSON(message: Path): unknown {
    const obj: any = {};
    if (message.net !== "") {
      obj.net = message.net;
    }
    if (message.points?.length) {
      obj.points = message.points.map((e) => Point.toJSON(e));
    }
    if (message.width !== 0) {
      obj.width = Math.round(message.width);
    }
    return obj;
  },

  create(base?: DeepPartial<Path>): Path {
    return Path.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Path>): Path {
    const message = createBasePath();
    message.net = object.net ?? "";
    message.points = object.points?.map((e) => Point.fromPartial(e)) || [];
    message.width = object.width ?? 0;
    return message;
  },
};

function createBaseLayerShapes(): LayerShapes {
  return { layer: undefined, rectangles: [], polygons: [], paths: [] };
}

export const LayerShapes = {
  encode(message: LayerShapes, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.layer !== undefined) {
      Layer.encode(message.layer, writer.uint32(10).fork()).ldelim();
    }
    for (const v of message.rectangles) {
      Rectangle.encode(v!, writer.uint32(18).fork()).ldelim();
    }
    for (const v of message.polygons) {
      Polygon.encode(v!, writer.uint32(26).fork()).ldelim();
    }
    for (const v of message.paths) {
      Path.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): LayerShapes {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseLayerShapes();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.layer = Layer.decode(reader, reader.uint32());
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.rectangles.push(Rectangle.decode(reader, reader.uint32()));
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.polygons.push(Polygon.decode(reader, reader.uint32()));
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.paths.push(Path.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): LayerShapes {
    return {
      layer: isSet(object.layer) ? Layer.fromJSON(object.layer) : undefined,
      rectangles: globalThis.Array.isArray(object?.rectangles)
        ? object.rectangles.map((e: any) => Rectangle.fromJSON(e))
        : [],
      polygons: globalThis.Array.isArray(object?.polygons) ? object.polygons.map((e: any) => Polygon.fromJSON(e)) : [],
      paths: globalThis.Array.isArray(object?.paths) ? object.paths.map((e: any) => Path.fromJSON(e)) : [],
    };
  },

  toJSON(message: LayerShapes): unknown {
    const obj: any = {};
    if (message.layer !== undefined) {
      obj.layer = Layer.toJSON(message.layer);
    }
    if (message.rectangles?.length) {
      obj.rectangles = message.rectangles.map((e) => Rectangle.toJSON(e));
    }
    if (message.polygons?.length) {
      obj.polygons = message.polygons.map((e) => Polygon.toJSON(e));
    }
    if (message.paths?.length) {
      obj.paths = message.paths.map((e) => Path.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<LayerShapes>): LayerShapes {
    return LayerShapes.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<LayerShapes>): LayerShapes {
    const message = createBaseLayerShapes();
    message.layer = (object.layer !== undefined && object.layer !== null) ? Layer.fromPartial(object.layer) : undefined;
    message.rectangles = object.rectangles?.map((e) => Rectangle.fromPartial(e)) || [];
    message.polygons = object.polygons?.map((e) => Polygon.fromPartial(e)) || [];
    message.paths = object.paths?.map((e) => Path.fromPartial(e)) || [];
    return message;
  },
};

function createBaseTextElement(): TextElement {
  return { string: "", loc: undefined };
}

export const TextElement = {
  encode(message: TextElement, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.string !== "") {
      writer.uint32(10).string(message.string);
    }
    if (message.loc !== undefined) {
      Point.encode(message.loc, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): TextElement {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTextElement();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.string = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.loc = Point.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): TextElement {
    return {
      string: isSet(object.string) ? globalThis.String(object.string) : "",
      loc: isSet(object.loc) ? Point.fromJSON(object.loc) : undefined,
    };
  },

  toJSON(message: TextElement): unknown {
    const obj: any = {};
    if (message.string !== "") {
      obj.string = message.string;
    }
    if (message.loc !== undefined) {
      obj.loc = Point.toJSON(message.loc);
    }
    return obj;
  },

  create(base?: DeepPartial<TextElement>): TextElement {
    return TextElement.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<TextElement>): TextElement {
    const message = createBaseTextElement();
    message.string = object.string ?? "";
    message.loc = (object.loc !== undefined && object.loc !== null) ? Point.fromPartial(object.loc) : undefined;
    return message;
  },
};

function createBaseInstance(): Instance {
  return { name: "", cell: undefined, originLocation: undefined, reflectVert: false, rotationClockwiseDegrees: 0 };
}

export const Instance = {
  encode(message: Instance, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.cell !== undefined) {
      Reference.encode(message.cell, writer.uint32(26).fork()).ldelim();
    }
    if (message.originLocation !== undefined) {
      Point.encode(message.originLocation, writer.uint32(34).fork()).ldelim();
    }
    if (message.reflectVert !== false) {
      writer.uint32(48).bool(message.reflectVert);
    }
    if (message.rotationClockwiseDegrees !== 0) {
      writer.uint32(56).int32(message.rotationClockwiseDegrees);
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

          message.originLocation = Point.decode(reader, reader.uint32());
          continue;
        case 6:
          if (tag !== 48) {
            break;
          }

          message.reflectVert = reader.bool();
          continue;
        case 7:
          if (tag !== 56) {
            break;
          }

          message.rotationClockwiseDegrees = reader.int32();
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
      originLocation: isSet(object.originLocation) ? Point.fromJSON(object.originLocation) : undefined,
      reflectVert: isSet(object.reflectVert) ? globalThis.Boolean(object.reflectVert) : false,
      rotationClockwiseDegrees: isSet(object.rotationClockwiseDegrees)
        ? globalThis.Number(object.rotationClockwiseDegrees)
        : 0,
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
    if (message.originLocation !== undefined) {
      obj.originLocation = Point.toJSON(message.originLocation);
    }
    if (message.reflectVert !== false) {
      obj.reflectVert = message.reflectVert;
    }
    if (message.rotationClockwiseDegrees !== 0) {
      obj.rotationClockwiseDegrees = Math.round(message.rotationClockwiseDegrees);
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
    message.originLocation = (object.originLocation !== undefined && object.originLocation !== null)
      ? Point.fromPartial(object.originLocation)
      : undefined;
    message.reflectVert = object.reflectVert ?? false;
    message.rotationClockwiseDegrees = object.rotationClockwiseDegrees ?? 0;
    return message;
  },
};

function createBaseLayout(): Layout {
  return { name: "", shapes: [], instances: [], annotations: [] };
}

export const Layout = {
  encode(message: Layout, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    for (const v of message.shapes) {
      LayerShapes.encode(v!, writer.uint32(18).fork()).ldelim();
    }
    for (const v of message.instances) {
      Instance.encode(v!, writer.uint32(26).fork()).ldelim();
    }
    for (const v of message.annotations) {
      TextElement.encode(v!, writer.uint32(34).fork()).ldelim();
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
        case 2:
          if (tag !== 18) {
            break;
          }

          message.shapes.push(LayerShapes.decode(reader, reader.uint32()));
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.instances.push(Instance.decode(reader, reader.uint32()));
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.annotations.push(TextElement.decode(reader, reader.uint32()));
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
      shapes: globalThis.Array.isArray(object?.shapes) ? object.shapes.map((e: any) => LayerShapes.fromJSON(e)) : [],
      instances: globalThis.Array.isArray(object?.instances)
        ? object.instances.map((e: any) => Instance.fromJSON(e))
        : [],
      annotations: globalThis.Array.isArray(object?.annotations)
        ? object.annotations.map((e: any) => TextElement.fromJSON(e))
        : [],
    };
  },

  toJSON(message: Layout): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.shapes?.length) {
      obj.shapes = message.shapes.map((e) => LayerShapes.toJSON(e));
    }
    if (message.instances?.length) {
      obj.instances = message.instances.map((e) => Instance.toJSON(e));
    }
    if (message.annotations?.length) {
      obj.annotations = message.annotations.map((e) => TextElement.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<Layout>): Layout {
    return Layout.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<Layout>): Layout {
    const message = createBaseLayout();
    message.name = object.name ?? "";
    message.shapes = object.shapes?.map((e) => LayerShapes.fromPartial(e)) || [];
    message.instances = object.instances?.map((e) => Instance.fromPartial(e)) || [];
    message.annotations = object.annotations?.map((e) => TextElement.fromPartial(e)) || [];
    return message;
  },
};

function createBaseAbstract(): Abstract {
  return { name: "", outline: undefined, ports: [], blockages: [] };
}

export const Abstract = {
  encode(message: Abstract, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.outline !== undefined) {
      Polygon.encode(message.outline, writer.uint32(18).fork()).ldelim();
    }
    for (const v of message.ports) {
      AbstractPort.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    for (const v of message.blockages) {
      LayerShapes.encode(v!, writer.uint32(42).fork()).ldelim();
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
        case 2:
          if (tag !== 18) {
            break;
          }

          message.outline = Polygon.decode(reader, reader.uint32());
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.ports.push(AbstractPort.decode(reader, reader.uint32()));
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.blockages.push(LayerShapes.decode(reader, reader.uint32()));
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
      outline: isSet(object.outline) ? Polygon.fromJSON(object.outline) : undefined,
      ports: globalThis.Array.isArray(object?.ports) ? object.ports.map((e: any) => AbstractPort.fromJSON(e)) : [],
      blockages: globalThis.Array.isArray(object?.blockages)
        ? object.blockages.map((e: any) => LayerShapes.fromJSON(e))
        : [],
    };
  },

  toJSON(message: Abstract): unknown {
    const obj: any = {};
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.outline !== undefined) {
      obj.outline = Polygon.toJSON(message.outline);
    }
    if (message.ports?.length) {
      obj.ports = message.ports.map((e) => AbstractPort.toJSON(e));
    }
    if (message.blockages?.length) {
      obj.blockages = message.blockages.map((e) => LayerShapes.toJSON(e));
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
      ? Polygon.fromPartial(object.outline)
      : undefined;
    message.ports = object.ports?.map((e) => AbstractPort.fromPartial(e)) || [];
    message.blockages = object.blockages?.map((e) => LayerShapes.fromPartial(e)) || [];
    return message;
  },
};

function createBaseAbstractPort(): AbstractPort {
  return { net: "", shapes: [] };
}

export const AbstractPort = {
  encode(message: AbstractPort, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.net !== "") {
      writer.uint32(10).string(message.net);
    }
    for (const v of message.shapes) {
      LayerShapes.encode(v!, writer.uint32(18).fork()).ldelim();
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
        case 2:
          if (tag !== 18) {
            break;
          }

          message.shapes.push(LayerShapes.decode(reader, reader.uint32()));
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
      shapes: globalThis.Array.isArray(object?.shapes) ? object.shapes.map((e: any) => LayerShapes.fromJSON(e)) : [],
    };
  },

  toJSON(message: AbstractPort): unknown {
    const obj: any = {};
    if (message.net !== "") {
      obj.net = message.net;
    }
    if (message.shapes?.length) {
      obj.shapes = message.shapes.map((e) => LayerShapes.toJSON(e));
    }
    return obj;
  },

  create(base?: DeepPartial<AbstractPort>): AbstractPort {
    return AbstractPort.fromPartial(base ?? {});
  },
  fromPartial(object: DeepPartial<AbstractPort>): AbstractPort {
    const message = createBaseAbstractPort();
    message.net = object.net ?? "";
    message.shapes = object.shapes?.map((e) => LayerShapes.fromPartial(e)) || [];
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

function createBaseLibrary(): Library {
  return { domain: "", units: 0, cells: [], author: undefined };
}

export const Library = {
  encode(message: Library, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.domain !== "") {
      writer.uint32(10).string(message.domain);
    }
    if (message.units !== 0) {
      writer.uint32(16).int32(message.units);
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
        case 2:
          if (tag !== 16) {
            break;
          }

          message.units = reader.int32() as any;
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
      units: isSet(object.units) ? unitsFromJSON(object.units) : 0,
      cells: globalThis.Array.isArray(object?.cells) ? object.cells.map((e: any) => Cell.fromJSON(e)) : [],
      author: isSet(object.author) ? AuthorMetadata.fromJSON(object.author) : undefined,
    };
  },

  toJSON(message: Library): unknown {
    const obj: any = {};
    if (message.domain !== "") {
      obj.domain = message.domain;
    }
    if (message.units !== 0) {
      obj.units = unitsToJSON(message.units);
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
    message.units = object.units ?? 0;
    message.cells = object.cells?.map((e) => Cell.fromPartial(e)) || [];
    message.author = (object.author !== undefined && object.author !== null)
      ? AuthorMetadata.fromPartial(object.author)
      : undefined;
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
