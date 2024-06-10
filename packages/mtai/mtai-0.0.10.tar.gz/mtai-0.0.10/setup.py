"""
A setuptools based setup module.
See:
https://www.ktechhub.com/tutorials/how-to-package-a-python-code-and-upload-to-pypi
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import io
from os import path, getenv
from setuptools import setup, find_packages

# Package meta-data.
NAME = "mtai"
DESCRIPTION = "A python library to consume meditranscribe ai API"
EMAIL = "pypi@ktechhub.com"
AUTHOR = "KtechHub"
REQUIRES_PYTHON = ">=3.8.0"
VERSION = getenv("VERSION", "0.0.1")  # package version
if "v" in VERSION:
    VERSION = VERSION[1:]

# Which packages are required for this module to be executed?
REQUIRED = [
    "requests",
]

here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with io.open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mediatranscribe/mt-ai-python",
    # Author details
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    license="MIT",
    keywords="mtai mediatranscribe mtaiapi python library",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=REQUIRED,
    include_package_data=True,
    setup_requires=["wheel"],
    extras_require={
        "test": ["coverage"],
    },
)
