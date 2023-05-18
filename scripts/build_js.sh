# 
# # VLSIR Python Build
# 
# Generates bindings from the schema defined in `protos/`.
# Must be run from the root of the Vlsir directory.
# 

# Make necessary directory
mkdir -p bindings/js/vlsir

# Protobuf Compilation
protoc -I=./protos \
    --js_out=./bindings/js/vlsir \
    ./protos/*.proto
