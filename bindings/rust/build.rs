//!
//! # Build Module
//!
//! Primarily expands protobuf definitions, adding a number of annotations.
//!

use std::{env, path::PathBuf};
use prost_wkt_build::*;

fn main() {

    // Add serde traits, excluding the Struct
    let out = PathBuf::from(env::var("OUT_DIR").unwrap());
    let descriptor_file = out.join("descriptors.bin");
    let mut prost_build = prost_build::Config::new();
    prost_build
        .type_attribute(
            ".",
            "#[derive(serde::Serialize,serde::Deserialize)]"
        )
        .extern_path(
            ".google.protobuf.Struct",
            "::prost_wkt_types::Struct"
        )
        .file_descriptor_set_path(&descriptor_file)
        .compile_protos(
            &[
                "protos/utils.proto",
                "protos/layout/raw.proto",
                "protos/circuit.proto",
                "protos/layout/tetris.proto",
                "protos/spice.proto",
                "protos/tech.proto",
            ],
            &["protos/"],
        ).unwrap();

    // Add our custom annotations
    // config.type_attribute("example", "#[serde(tag = \"type\")]");
    // config.field_attribute("example", "#[serde(flatten)]");

    // And build!
    let descriptor_bytes =
    std::fs::read(descriptor_file)
    .unwrap();

    let descriptor =
        FileDescriptorSet::decode(&descriptor_bytes[..])
        .unwrap();

    prost_wkt_build::add_serde(out, descriptor);
}