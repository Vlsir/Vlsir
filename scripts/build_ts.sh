# 
# # VLSIR TypeScript Build
# 
# Generates bindings from the schema defined in `protos/`.
# Must be run from the root of the Vlsir directory.
# 

# Make necessary directory
mkdir -p bindings/ts/src

# Protobuf Compilation
protoc \
    -I=./protos \
    -I=./protos/layout \
    --plugin=./bindings/ts/node_modules/.bin/protoc-gen-ts_proto \
    --ts_proto_out=./bindings/ts/src \
    --ts_proto_opt=esModuleInterop=true \
    --ts_proto_opt=oneof=unions \
    --ts_proto_opt=useExactTypes=false \
    --ts_proto_opt=exportCommonSymbols=false \
    ./protos/*.proto \
    ./protos/*/*.proto 

