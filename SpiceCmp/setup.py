"""
# Setup Script

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
    name="spicecmp",
    version="1.0.0.dev0",
    description="Spice Models and Results Comparisons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="go/bodger",
    author="Dan Fritchman",
    author_email="dan@fritch.mn",
    packages=find_packages(),
    python_requires=">=3.8, <4",
    install_requires=[
        "pandas"
        "hdl21==1.0.0.dev0", 
        "vlsir==1.0.0.dev0", 
        "vlsirtools==1.0.0.dev0", 
    ],
    extras_require={
        "dev": ["pytest==5.2", "coverage", "pytest-cov", "black==19.10b0", "twine"]
    },
)
