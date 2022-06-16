"""
# Publication Script 

Uploads each set of language-bindings to its language-specific package-distributor.
Generally requires the executing-user to be logged into, and have access to, each.

"""

import os
from pathlib import Path

script_path = os.getcwd()
VLSIR_VERSION = "1.0.0"
USER = os.environ["PYPI_USERNAME"]
PASS = os.environ["PYPI_PASSWORD"]

# An ordered list of packages to publish, in dependency order as *many* depend on one another.
# Each is a two-tuple of (package name, path to package).
packages = [
    ("vlsir", Path("Vlsir/bindings/python")),
    ("vlsirtools", Path("Vlsir/VlsirTools")),
    ("hdl21", Path("Hdl21")),
    ("asap7-hdl21", Path("Hdl21/pdks/Asap7")),
    ("sky130-hdl21", Path("Hdl21/pdks/Sky130")),
    ("spicecmp", Path("Vlsir/SpiceCmp")),
]


def publish_pkg(pkgname: str, path: Path):
    os.chdir(path)
    os.system("python setup.py sdist")
    os.system(f"twine upload -u {USER} -p {PASS} dist/{pkgname}-{VLSIR_VERSION}.tar.gz")
    os.chdir(script_path)


for pkgname, path in packages:
    # Publish the package 
    publish_pkg(pkgname, path)
    # And sit here a minute to let it really sink into that server 
    os.system("sleep 10")

# Rust
# cd ../bindings/rust
# cargo publish

# FIXME/ Coming Soon: JS. And C++, maybe, to some package-manager to be named.

