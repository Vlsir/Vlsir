# 
# # VLSIR C++ Build
# 
# Generates bindings from the schema defined in `protos/`.
# Must be run from the root of the Vlsir directory.
# 

# Make necessary directory
mkdir -p bindings/cpp/vlsir

# Protobuf Compilation
protoc -I=./protos \
    --cpp_out=./bindings/cpp/vlsir \
    ./protos/*.proto
