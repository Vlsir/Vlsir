# 
# # VLSIR Build
# 
# Builds all language binding recipes in repository
# Must be run from the root of the Vlsir directory.
# 

set -eo 

# Call all build scripts
scripts/build_cpp.sh
scripts/build_ts.sh
scripts/build_python.sh
scripts/build_rust.sh
scripts/build_julia.sh

