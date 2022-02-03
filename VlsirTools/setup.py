"""
# VlsirTools Setup Script

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
    name="vlsirtools",
    version="0.1.1",
    description="Tools for the Vlsir IC Design Schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dan-fritchman/Vlsir",
    author="Dan Fritchman",
    author_email="dan@fritch.mn",
    packages=find_packages(where=".", exclude=["tests"]),
    python_requires=">=3.7, <4",
    install_requires=["vlsir==0.1.1",],
    extras_require={"dev": ["pytest==5.2", "coverage", "pytest-cov", "black==19.10b0"]},
)
