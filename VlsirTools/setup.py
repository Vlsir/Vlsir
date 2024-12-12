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

VLSIR_VERSION = "7.0.0"

setup(
    name="vlsirtools",
    version=VLSIR_VERSION,
    description="Tools for the Vlsir IC Design Schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vlsir/Vlsir",
    author="Dan Fritchman",
    author_email="dan@fritch.mn",
    packages=find_packages(),
    python_requires=">=3.7, <3.13",
    install_requires=[
        f"vlsir=={VLSIR_VERSION}",  # VLSIR Core Python Bindings
        "numpy",  # For `sim_data` simulation results
        "pandas",  # For CSV reading
    ],
    extras_require={"dev": ["vlsirdev"]},
)
