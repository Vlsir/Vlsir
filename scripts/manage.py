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

import os, argparse
from enum import Enum
from pathlib import Path

VLSIR_VERSION = "4.0.0rc0"


class Actions(Enum):
    # The available command-line actions
    # Could this be a more elaborate CLI library thing? Sure.
    BUILD = "build"
    INSTALL = "install"
    UNINSTALL = "uninstall"
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
    ("gf180-hdl21", Path("Hdl21/pdks/Gf180")),
    ("spicecmp", Path("Vlsir/SpiceCmp")),
]


def build():
    """Build the internally-supported bindings."""
    # Just invokes `scripts/build_supported.sh`
    os.chdir(vlsir_path)
    os.system("./scripts/build_supported.sh")


def uninstall():
    """# Uninstall everything in `packages`."""
    pkgs = " ".join([pkgname for (pkgname, path) in packages])
    os.system(f"pip uninstall -y {pkgs}")


def install():
    """# Create dev installs of everything in `packages`.
    Installs everything in one `pip install` command,
    which is both faster and better for reporting any dependency incompatibilities."""

    # Get a string like "-e ./Vlsir/bindings/python[dev]" for each
    pathstr = lambda p: f"-e ./{str(p)}[dev]"
    args = " ".join([pathstr(p) for (_, p) in packages])
    cmd = "pip install " + args

    # And run it
    os.chdir(workspace_path)
    os.system(cmd)


def publish():
    """Publish all Python packages to PyPi
    Credentials must be provided by a .pypirc file or similar."""

    os.chdir(workspace_path)
    print(f"Publishing from {workspace_path}")

    for pkgname, path in packages:
        # Build a source distribution
        # No more `setup.py sdist`; that is bad now!
        # Use these guys: https://pypa-build.readthedocs.io/en/latest/
        build = f"python -m build --sdist --no-isolation {str(path)}"
        os.system(build)

        # Check it exists
        tarball = path / f"dist/{pkgname}-{VLSIR_VERSION}.tar.gz"
        if not tarball.exists():
            raise RuntimeError(f"Package build tarball {tarball} not found")

        # Run twine's built-in checks
        check = f"twine check {str(tarball)}"
        os.system(check)

        # Upload it to PyPi
        upload = f"twine upload {str(tarball)}"
        os.system(upload)

        # And sit here a minute to let it really sink into that server
        os.system("sleep 10")

    # Rust
    # cd ../bindings/rust
    # cargo publish


def main():
    """# Our fancy command-line interface."""

    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=[a.value for a in Actions])
    args = parser.parse_args()

    if args.action == Actions.BUILD.value:
        return build()
    if args.action == Actions.INSTALL.value:
        return install()
    if args.action == Actions.UNINSTALL.value:
        return uninstall()
    if args.action == Actions.PUBLISH.value:
        return publish()

    raise ValueError(f"Invalid manage.py action {args.action}")


if __name__ != "__main__":
    raise RuntimeError("It says SCRIPTS right there doesnt it?")

main()
