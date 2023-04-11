# 
# # VLSIR C++ Build
# 
# Generates Julia bindings from the schema defined in `protos/`.
# Must be run from the root of the Vlsir directory.
# 

# Make necessary directory
mkdir -p bindings/cpp/vlsir

# Protobuf Compilation
protoc -I=./protos \
    --cpp_out=./bindings/cpp/vlsir \
    ./protos/*.proto

# Copy its output to each language-directory
cp primitives/vlsir.primitives.pb.txt bindings/cpp/vlsir/