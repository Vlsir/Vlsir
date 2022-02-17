# -------------------------------------
# Publication Script 
# 
# Uploads each set of language-bindings to its language-specific package-distributor.
# Generally requires the executing-user to be logged into, and have access to, each.
# 
# This script is intended to be run from the root of the project, 
# i.e. the folder generally named `Vlsir`. 
# -------------------------------------

set -eo pipefail

VERSION=0.2.1

# Python
cd bindings/python 
python setup.py sdist 
twine upload dist/vlsir-${VERSION}.tar.gz

# Python Tools 
cd ../../VlsirTools 
python setup.py sdist 
twine upload dist/vlsirtools-${VERSION}.tar.gz

# Rust
cd ../bindings/rust 
cargo publish 

# FIXME/ Coming Soon: JS. And C++, maybe, to some package-manager to be named.

