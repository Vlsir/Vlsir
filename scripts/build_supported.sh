# 
# # VLSIR Build
# 
# Generates supported bindings from the schema defined in `protos/`.
# as determined in Issue #49 in the Vlsir repository.
#
# Must be run from the root of the Vlsir directory.
# 

set -eo 

# Call all build scripts
scripts/build_python.sh
scripts/build_rust.sh