
# Python Protobuf Compilation
protoc -I=./protos \
    --python_out=./compiled/python \
    --js_out=./compiled/js \
    --cpp_out=./compiled/cpp \
    ./protos/*.proto

# Sadly `protoc` doesn't seem to know how Python3 imports work. Correct them. 
2to3 -wn -f import compiled/python/*.py
