
# Python Protobuf Compilation
protoc -I=./protos --python_out=./compiled/python ./protos/*.proto
# Sadly protoc doesn't seem to know how Python3 imports work
2to3 -wn -f import compiled/python/*.py
