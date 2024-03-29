# 
# # VLSIR Julia Build
# 
# Generates bindings from the schema defined in `protos/`.
# Must be run from the root of the Vlsir directory.
# 

# Mkdir
cd bindings/julia
mkdir src

# Build the package
julia build.jl

# Copy the files to the correct location
echo "Reorganizing files..."
cp -r ./src/vlsir/* ./src
rm -rf ./src/vlsir

# Remove duplicate lines and replace dependencies
echo "Cleaning up..."
find . -type f  ! -name '*_pb.jl' -exec sh -c 'awk "!visited[\$0]++" {} > {}.tmp && mv {}.tmp {}' \;
sed -i 's|include("../google/google.jl")|include("google/google.jl")|' ./src/vlsir.jl
find ./src -type f -name '*.jl' -exec sed -i 's|vlsir|Vlsir|' {} +

# Rename to appropriate package name
mv ./src/vlsir.jl ./src/Vlsir.jl
cd -

# TODO: Add a way to programmatically precompile the package