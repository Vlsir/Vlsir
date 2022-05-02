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
    version="0.2.0",
    description="Spice Models and Results Comparisons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="go/bodger",
    author="Dan Fritchman",
    author_email="dan@fritch.mn",
    packages=find_packages(),
    python_requires=">=3.8, <4",
    install_requires=["hdl21==0.2.1", "vlsir==0.2.1", "vlsirtools==0.2.1", "pandas"],
    extras_require={
        "dev": ["pytest==5.2", "coverage", "pytest-cov", "black==19.10b0", "twine"]
    },
)
