# 
# # VLSIR Python Build
# 
# Generates Python bindings from the schema defined in `protos/`.
# Must be run from the root of the Vlsir directory.
# 


set -eo 

# Protobuf Compilation
protoc -I=./protos \
    --python_out=./bindings/python/vlsir \
    ./protos/*.proto

# Sadly `protoc` doesn't seem to know how Python3 imports work. Correct them. 
2to3 -wn -f import bindings/python/vlsir/*.py

# Run the primitive-generation script
python3 scripts/primitives.py 

# Copy its output to python directory 
cp primitives/vlsir.primitives.pb.txt bindings/python/vlsir/

# Run language-specific formatting
black bindings/python