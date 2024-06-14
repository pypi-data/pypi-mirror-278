from setuptools import setup, find_packages
from flarejax import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


description = "Common neural network modules and utilities based on flarejax."

setup(
    name="flarenet",
    version=__version__,
    packages=find_packages(where="."),
    python_requires=">=3.10",
    install_requires=requirements,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pwolle/flarenet",
    author="Paul Wollenhaupt",
    author_email="paul.wollenhaupt@gmail.com",
)
