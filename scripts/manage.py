"""
# Package Manager(?) Script 

Does the handful of things commonly required across (mostly Python) packages defined here. 
An crucial element is the dependency-ordered `packages` list, 
which enumerates a valid order for installing or publishing this set of packages 
which tightly depend on one another. 

* Build 
    * Run the bindings build script
* Installation 
    * Creates "dev mode" `pip install`s for each package 
* Publication 
    * Uploads each set of language-bindings to its language-specific package-distributor.
    * Generally requires the executing-user to be logged into, and have access to, each.

While this script can be *run* anywhere, it expects that `Hdl21` is located alongside `Vlsir`, 
i.e. that the two have a shared parent directory. 
"""

import os
from enum import Enum
from pathlib import Path

VLSIR_VERSION = "4.0.dev0"


class Actions(Enum):
    # The available command-line actions
    # Could this be a more elaborate CLI library thing? Sure.
    BUILD = "build"
    INSTALL = "install"
    PUBLISH = "publish"


# Figure out the shared parent directory of Vlsir and Hdl21
# __file__ = manage.py, parent = scripts/, parent**2 = Vlsir, parent**3 = the "workspace"!
vlsir_path = Path(__file__).parent.parent
workspace_path = vlsir_path.parent
if not (workspace_path / "Vlsir").exists():
    raise RuntimeError(f"Something wrong here with this Path")

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


def build():
    """Build the bindings."""
    # Just invokes `scripts/build.sh`
    os.chdir(vlsir_path)
    os.system("./scripts/build.sh")


def install():
    """Create dev installs of everything in `packages`, in order."""

    os.chdir(workspace_path)
    for pkgname, path in packages:
        os.chdir(path)
        os.system('pip install -e ".[dev]" ')
        os.chdir(workspace_path)


def publish():
    """Publish all Python packages to PyPi"""

    USER = os.environ["PYPI_USERNAME"]
    PASS = os.environ["PYPI_PASSWORD"]

    os.chdir(workspace_path)

    def publish_pkg(pkgname: str, path: Path):
        os.chdir(path)
        os.system("python setup.py sdist")
        os.system(
            f"twine upload -u {USER} -p {PASS} dist/{pkgname}-{VLSIR_VERSION}.tar.gz"
        )
        os.chdir(workspace_path)

    for pkgname, path in packages:
        # Publish the package
        publish_pkg(pkgname, path)
        # And sit here a minute to let it really sink into that server
        os.system("sleep 10")

    # Rust
    # cd ../bindings/rust
    # cargo publish

    # FIXME/ Coming Soon: JS. And C++, maybe, to some package-manager to be named.


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=[a.value for a in Actions])
    args = parser.parse_args()

    if args.action == Actions.BUILD.value:
        return build()
    if args.action == Actions.INSTALL.value:
        return install()
    if args.action == Actions.PUBLISH.value:
        return publish()

    raise ValueError(f"Invalid manage.py action {args.action}")


if __name__ == "__main__":
    main()
