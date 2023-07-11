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
    name="vlsirtools",
    version=_VLSIR_VERSION,
    description="Tools for the Vlsir IC Design Schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vlsir/Vlsir",
    author="Dan Fritchman",
    author_email="dan@fritch.mn",
    packages=find_packages(),
    python_requires=">=3.7, <3.12",
    install_requires=[
        f"vlsir=={_VLSIR_VERSION}",  # VLSIR Core Python Bindings
        "numpy~=1.21",  # For `sim_data` simulation results
        "pandas~=1.3",  # For CSV reading
    ],
    extras_require={
        "dev": ["pytest==7.1", "coverage", "pytest-cov", "black==22.6", "twine"]
    },
)
