"""Setup for the the NCBI Taxonomy package."""

import os
import re

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with open(os.path.join(here, "README.md"), encoding="utf8") as f:
    long_description = f.read()


def read(*parts):
    with open(os.path.join(here, *parts), "r", encoding="utf8") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("ncbi_taxonomy", "__version__.py")

test_deps = [
    "pytest",
    "pytest-cov",
    "pytest-readme",
    "validate_version_code",
]

extras = {
    "test": test_deps,
}

setup(
    name="ncbi_taxonomy",
    version=__version__,
    description="Python package to interact with the NCBI Taxonomy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    tests_require=test_deps,
    python_requires=">=3.12",
    install_requires=[
        "cache-decorator>=2.2.0",
        "compress-json>=1.1.0",
        "downloaders>=1.0.20",
        "ipython>=8.28.0",
        "networkx>=3.4.1",
        "pandas>=2.2.3",
        "polars>=1.9.0",
        "requests>=2.32.3",
        "setuptools>=75.1.0",
    ],
    extras_require=extras,
)
