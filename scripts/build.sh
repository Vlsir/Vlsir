# 
# # VLSIR Build
# 
# Primarily generates language-specific bindings from the schema defined in `protos/`.
#
# Must be run from the root of the Vlsir directory.
# 
# TODO: you need to run this so that 'protos' exists before you build rust
# TODO: add the separate Rust build process 

SCHEMA_VERSION=main
 
if [ ! -d protos ]; then
  git clone -b "${SCHEMA_VERSION}" git@github.com:Vlsir/schema-proto protos
else
  cd protos
  git fetch
  git checkout -q "${SCHEMA_VERSION}"
  cd ../
fi

set -eo 

# Protobuf Compilation
protoc -I=./protos \
    --python_out=./bindings/python/vlsir \
    --js_out=./bindings/js/vlsir \
    --cpp_out=./bindings/cpp/vlsir \
    ./protos/*.proto

# Rust Bindings
cd bindings/rust 
cargo build 
cd -

# Sadly `protoc` doesn't seem to know how Python3 imports work. Correct them. 
2to3 -wn -f import bindings/python/vlsir/*.py

# Run the primitive-generation script
python3 scripts/primitives.py 

# Copy its output to each language-directory 
cp primitives/vlsir.primitives.pb.txt bindings/python/vlsir/
cp primitives/vlsir.primitives.pb.txt bindings/cpp/vlsir/
cp primitives/vlsir.primitives.pb.txt bindings/js/vlsir/

# Run language-specific formatting
black bindings/python 

