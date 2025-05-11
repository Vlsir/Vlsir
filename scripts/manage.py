"""
# Package Manager(?) Script

Does the handful of things commonly required across (mostly Python) packages defined here.
An crucial element is the dependency-ordered `packages` list,
which enumerates a valid order for installing or publishing this set of packages
which tightly depend on one another.

- Build
    - Run the bindings build script
- Installation
    - Creates "dev mode" `pip install`s for each package
- Publication
    - Uploads each set of language-bindings to its language-specific package-distributor.
    - Generally requires the executing-user to be logged into, and have access to, each.

While this script can be *run* anywhere, it expects that `Hdl21` is located alongside `Vlsir`,
i.e. that the two have a shared parent directory.
"""

import os, argparse
from enum import Enum
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

# NOTE: this here really needs to match all the package `setup.py` / `pyproject.toml` versions!
# Perhaps there is some nice monorepo-management tool for this, but we don't know it.
VLSIR_VERSION = "7.0.0"


# Figure out the shared parent directory of Vlsir and Hdl21
# __file__ = manage.py, parent = scripts/, parent**2 = Vlsir, parent**3 = the "workspace"!
vlsir_path = Path(__file__).parent.parent
workspace_path = vlsir_path.parent
if not (workspace_path / "Vlsir").exists():
    raise RuntimeError(f"Something wrong here with this Path")

# An ordered list of packages to publish, in dependency order as *many* depend on one another.
# Each is a tuple of (path to package, package name, optional module name).
packages = [
    (Path("Vlsir/VlsirDev"), "vlsirdev", None),
    (Path("Vlsir/bindings/python"), "vlsir", None),
    (Path("Vlsir/VlsirTools"), "vlsirtools", None),
    (Path("Hdl21"), "hdl21", None),
    (Path("Vlsir/SpiceCmp"), "spicecmp", None),
    (
        Path("Hdl21/pdks/Asap7"),
        "asap7-hdl21",
        "asap7_hdl21",
    ),
    (
        Path("Hdl21/pdks/Sky130"),
        "sky130-hdl21",
        "sky130_hdl21",
    ),
    (
        Path("Hdl21/pdks/Gf180"),
        "gf180-hdl21",
        "gf180_hdl21",
    ),
]


@dataclass
class Package:
    path: Path
    name: str
    module_name: Optional[str] = None


# Convert those tuples to structured `Package` objects
packages = [Package(*p) for p in packages]


def build():
    """Build the internally-supported bindings."""
    # Just invokes `scripts/build_supported.sh`
    os.chdir(vlsir_path)
    run("./scripts/build_supported.sh")


def uninstall():
    """# Uninstall everything in `packages`."""
    pkgs = " ".join([pkg.name for pkg in packages])
    run(f"pip uninstall -y {pkgs}")


def install():
    """# Create dev installs of everything in `packages`.
    Installs everything in one `pip install` command,
    which is both faster and better for reporting any dependency incompatibilities."""

    # Get a string like "-e ./Vlsir/bindings/python[dev]" for each
    pathstr = lambda p: f"-e ./{str(p)}[dev]"
    args = " ".join([pathstr(pkg.path) for pkg in packages])
    cmd = "pip install " + args

    # And run it
    os.chdir(workspace_path)
    run(cmd)


def publish():
    """Publish all Python packages to PyPi
    Credentials must be provided by a .pypirc file or similar."""

    os.chdir(workspace_path)
    print(f"Publishing from {workspace_path}")
    [publish_pkg(pkg) for pkg in packages]

    # Rust
    # cd ../bindings/rust
    # cargo publish


def publish_pkg(pkg: Package) -> None:
    """Publish `pkg` to PyPi."""
    # NOTE re the tools used here: https://github.com/Vlsir/Vlsir/issues/90

    # Build distributions
    # No more `setup.py sdist`; that is bad now!
    # Use these guys: https://pypa-build.readthedocs.io/en/latest/
    build = f"python -m build {str(pkg.path)}"
    run(build)

    module_name = pkg.module_name or pkg.name
    tarball = pkg.path / f"dist/{module_name}-{VLSIR_VERSION}.tar.gz"
    wheel = pkg.path / f"dist/{module_name}-{VLSIR_VERSION}-py3-none-any.whl"

    for dist in (tarball, wheel):
        # Check it exists
        if not dist.exists():
            raise RuntimeError(f"Package distribution {dist} not found")

        # Run twine's built-in checks
        check = f"twine check {str(dist)}"
        run(check)

        # Upload it to PyPi
        upload = f"twine upload {str(dist)}"
        run(upload)

    # And sit here a minute to let it really sink into that server
    run("sleep 10")


def run(cmd: str) -> None:
    # Print and run a shell command.
    print(f"Running: {cmd}")
    os.system(cmd)


class Actions(Enum):
    # The available command-line actions
    # Could this be a more elaborate CLI library thing? Sure.
    BUILD = "build"
    INSTALL = "install"
    UNINSTALL = "uninstall"
    PUBLISH = "publish"


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
