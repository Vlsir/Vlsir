"""
# Vlsir Setup Script

Derived from the setuptools sample project at
https://github.com/pypa/sampleproject/blob/main/setup.py

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "readme.md").read_text(encoding="utf-8")

setup(
    name="vlsir",
    version="0.2.1",
    description="Data Schemas for Chip Design",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dan-fritchman/Vlsir",
    author="Dan Fritchman",
    packages=find_packages(),
    package_data={"vlsir": ["*.pb.txt"]},  # Include the protobuf-text literals
    python_requires=">=3.7, <4",
    install_requires=["protobuf==3.19.1"],
    extras_require={
        "dev": ["pytest==5.2", "coverage", "pytest-cov", "black==19.10b0", "twine"]
    },
)
