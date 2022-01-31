
# Python Protobuf Compilation
protoc -I=./protos \
    --python_out=./bindings/python/vlsir \
    --js_out=./bindings/js/vlsir \
    --cpp_out=./bindings/cpp/vlsir \
    ./protos/*.proto

# Sadly `protoc` doesn't seem to know how Python3 imports work. Correct them. 
2to3 -wn -f import bindings/python/vlsir/*.py

# Run the primitive-generation script
python3 scripts/primitives.py 

# Copy its output to each language-directory 
cp primitives/vlsir.primitives.pb.txt bindings/python/vlsir/
cp primitives/vlsir.primitives.pb.txt bindings/cpp/vlsir/
cp primitives/vlsir.primitives.pb.txt bindings/js/vlsir/
