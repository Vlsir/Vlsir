"""
# Setup Script

Derived from the setuptools sample project at
https://github.com/pypa/sampleproject/blob/main/setup.py

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
readme = here / "readme.md"
long_description = "" if not readme.exists() else readme.read_text(encoding="utf-8")

_VLSIR_VERSION = "4.0.0rc0"

setup(
    name="vlsir",
    version=_VLSIR_VERSION,
    description="Python Bindings to the VLSIR Data Schemas for Chip Design",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vlsir/Vlsir",
    author="Dan Fritchman",
    author_email="dan@fritch.mn",
    packages=find_packages(),
    # There's really no code in this package that isn't generated from the schema,
    # So in principle we don't *need* to specify a python version.
    # But, it'll show it on the PyPi page and stuff, so we might as well.
    # As of this writing and protobuf version, that means 3.7+.
    python_requires=">=3.7",
    install_requires=[
        # Note:
        # This version of protobuf differs pretty substantially from the ones before it;
        # Most binding-code is *not* generated per-schema, but is in the protobuf package,
        # And schema-derived types are generated on the fly.
        # So, versions before this will generally fail pretty hard.
        "protobuf~=4.23"
    ],
    extras_require={
        "dev": ["pytest==7.1", "coverage", "pytest-cov", "black==22.6", "twine"]
    },
)
