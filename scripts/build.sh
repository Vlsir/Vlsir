
# Python Protobuf Compilation
protoc -I=./protos \
    --python_out=./bindings/python/vlsir \
    --js_out=./bindings/js/vlsir \
    --cpp_out=./bindings/cpp/vlsir \
    ./protos/*.proto

# Sadly `protoc` doesn't seem to know how Python3 imports work. Correct them. 
2to3 -wn -f import bindings/python/vlsir/*.py
