import Pkg
Pkg.add("ProtoBuf")
Pkg.add("Glob")

using ProtoBuf
using Glob
# Define path variables
proto_directory = "../../protos"
proto_files = glob("*.proto", proto_directory)  # Collect all .proto files in the directory
search_directories = [".","../../protos"]
output_directory = "./src"
# Compile the .proto files
protojl(
    proto_files,
    search_directories,
    output_directory;
)
