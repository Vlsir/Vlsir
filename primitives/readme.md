
# Vlsir Primitive Definitions 

Adjacent file `vlsir.primitives.pb.txt` contains the protobuf-text-format definition of the Vlsir primitives. 
These definitions are generally copied into each language-specific package, and loaded by language-specific code. 

The `vlsir.primitives.pb.txt` file is typically script-generated by the `primitives.py` script, 
generally run as part of the bindings build-process. 

The `vlsir.primitives` `Package` as well as each primitive includes a markdown-format description in their `desc` field. 
