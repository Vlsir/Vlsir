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
| [Circuit](https://github.com/Vlsir/schema-proto/blob/main/circuit.proto)      | Circuit / Hardware Descriptions |
| [Raw Layout](https://github.com/Vlsir/schema-proto/blob/main/layout/raw.proto)       | "Raw Polygon" IC Layout         |
| [Tetris Layout](https://github.com/Vlsir/schema-proto/blob/main/layout/tetris.proto) | "Tetris" Gridded IC Layout      |
| [Spice](https://github.com/Vlsir/schema-proto/blob/main/spice.proto)          | Spice-Class Simulator Interface |
| [Utilities](https://github.com/Vlsir/schema-proto/blob/main/utils.proto)      | Shared Utilities                |

## Language Bindings

_Vlsir_ defines a [data schema](https://github.com/Vlsir/schema-proto), which related projects use in code.
Projects using _vlsir_ can be written in any language with protobuf-compiler bindings - 
which includes essentially every popular programming language. 
Existing projects have prominently used Python, C++, and Rust. In this repository we have supported bindings
for Python and Rust which can be found in `bindings` and downloaded from their respective package managers:

| Language | Bindings Package | Compiler | 
| -------- | ---------------- | -------- | 
| Python   | https://pypi.org/project/vlsir/ | Google `protoc` |
| Rust     | https://crates.io/crates/vlsir  | [Prost](https://github.com/tokio-rs/prost) |

## Vlsir Tools 

The `Vlsir` repository also serves as home for the Python-language [VlsirTools](https://pypi.org/project/vlsirtools/) package. 
`VlsirTools` is a collection of tools for working with Vlsir's schema, including: 

* Netlisting to industry-standard formats (SPICE, Verilog, etc.)
* Drivers and result-parsers for Spice-class simulators

## Building

The repository includes build scripts for Python, Rust, C++, Javascript and Julia bindings, of which only Rust and Python are actively maintained and tested. These can all be built individually with `scripts/build_<your-language-here>.sh` or with either of the two joint scripts:

- `build_supported.sh`, this builds all supported bindings for use by Vlsir developers 
- `build_all_recipes.sh`, this builds all bindings and is primarily used for testing

To build, run the script below:

```
git clone git@github.com:Vlsir/Vlsir
cd Vlsir
scripts/build_<build_flavour>.sh
```

## Projects

Ongoing, co-developed projects which use `vlsir`: 

| Project  | Description | Language |
| -------- | ----------- | -------- |
| [Hdl21](https://github.com/dan-fritchman/Hdl21)        | Generator-Based Hardware Description Library | Python |
| [Layout21](https://github.com/dan-fritchman/Layout21)  | Multi-Layered Layout-Programming | Rust |
| [BFG](https://github.com/growly/bfg)         | Layout Generation for Open-Source FPGAs | C++ |
