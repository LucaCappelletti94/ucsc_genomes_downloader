import os
import re

# To use a consistent encoding
from codecs import open as copen
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with copen(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def read(*parts):
    with copen(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("ucsc_genomes_downloader", "__version__.py")

test_deps = ["coveralls", "pytest", "codacy-coverage",
             "validate_version_code", "pytest-cov"]

extras = {
    'test': test_deps,
}

setup(
    name='ucsc_genomes_downloader',
    version=__version__,
    description="Python package to quickly download genomes from the UCSC.",
    long_description=long_description,
    url="https://github.com/LucaCappelletti94/ucsc_genomes_downloader",
    author="Luca Cappelletti",
    author_email="cappelletti.luca94@gmail.com",
    # Choose your license
    license='MIT',
    include_package_data=True,
    python_requires='>3.5.2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    tests_require=test_deps,
    # Add here the package dependencies
    install_requires=[
        "requests",
        "tqdm",
        "dateparser",
        "pandas",
        "userinput",
        "compress_json",
        "numba>=0.50.0"
    ],
    extras_require=extras,
)
