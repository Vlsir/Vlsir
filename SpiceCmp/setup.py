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
    name="spicecmp",
    version=_VLSIR_VERSION,
    description="Spice Models and Results Comparisons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vlsir/Vlsir",
    author="Dan Fritchman",
    author_email="dan@fritch.mn",
    packages=find_packages(),
    python_requires=">=3.7, <3.12",
    install_requires=[
        "pandas~=1.3",
        f"hdl21=={_VLSIR_VERSION}",
        f"vlsir=={_VLSIR_VERSION}",
        f"vlsirtools=={_VLSIR_VERSION}",
    ],
    extras_require={
        "dev": ["pytest==7.1", "coverage", "pytest-cov", "black==22.6", "twine"]
    },
)
