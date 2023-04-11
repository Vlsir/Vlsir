# 
# # VLSIR Python Build
# 
# Generates Python bindings from the schema defined in `protos/`.
# Must be run from the root of the Vlsir directory.
# 

# Protobuf Compilation
protoc -I=./protos \
    --js_out=./bindings/js/vlsir \
    ./protos/*.proto

# Copy its output to javascript directory
cp primitives/vlsir.primitives.pb.txt bindings/js/vlsir/
