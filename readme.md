# Vlsir

Interchange formats for chip design.

---

Vlsir defines data schema for integrated circuit (IC) circuits, layouts, and simulations,
using Google's [Protocol Buffer](https://developers.google.com/protocol-buffers/) schema definition language.

The name _Vlsir_ is a merger of _VLSI_ (very large scale integration - a way-outdated chip-world acronym)
and _IR_ (intermediate representation - the term every cool-kid copying compiler designers uses nowadays).

## Contents

All of Vlsir's schema-definitions live in the [protos](./protos) directory.

| Schema                                 | Description                     |
| -------------------------------------- | ------------------------------- |
| [Circuit](./protos/circuit.proto)      | Circuit / Hardware Descriptions |
| [Raw Layout](./protos/raw.proto)       | "Raw Polygon" IC Layout         |
| [Tetris Layout](./protos/tetris.proto) | "Tetris" Gridded IC Layout      |
| [Spice](./protos/spice.proto)          | Spice-Class Simulator Interface |
| [Utilities](./protos/utils.proto)      | Shared Utilities                |

## Projects

_Vlsir_ defines a data schema, which related projects use in code.
Projects using _vlsir_ can be written in any language with protobuf-compiler bindings,
which includes essentially every popular programming language.
Existing projects have prominently used Python, C++, and Rust.

| Project  | Description                                                        |
| -------- | ------------------------------------------------------------------ |
| hdl21    | Hardware Description in Python                                     |
| layout21 | Multi-Layered Layout-Programming                                   |
| boralago | Layout Generation for Open-Source FPGAs (and other cool stuff too) |
