
# Python Protobuf Compilation
protoc -I=./protos \
    --python_out=./packages/python/vlsir \
    --js_out=./packages/js/vlsir \
    --cpp_out=./packages/cpp/vlsir \
    ./protos/*.proto

# Sadly `protoc` doesn't seem to know how Python3 imports work. Correct them. 
2to3 -wn -f import packages/python/vlsir/*.py
