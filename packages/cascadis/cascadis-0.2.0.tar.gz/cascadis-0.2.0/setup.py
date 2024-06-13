#!/usr/bin/env python3
# coding: utf-8
import os
import re

import setuptools
from setuptools import find_packages

# CAUTION:
# Do NOT import your package from your setup.py

_nsp = ""
_pkg = "cascadis"
_desc = ""
_names = [_nsp, _pkg]
_names = [s for s in _names if s]


def read(filename):
    with open(filename) as f:
        return f.read()


def _find_version():
    names = _names + ["__init__.py"]
    root = os.path.dirname(__file__)
    path = os.path.join(root, *names)
    regex = re.compile(r"""^__version__\s*=\s*('|"|'{3}|"{3})([.\w]+)\1\s*(#|$)""")
    with open(path) as fin:
        for line in fin:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            mat = regex.match(line)
            if mat:
                return mat.groups()[1]
    raise ValueError("__version__ definition not found")


config = {
    "name": "cascadis",
    "version": _find_version(),
    "description": "A simple content-addressed storage service.",
    "keywords": "",
    "url": "https://github.com/frozflame/cascadis",
    "author": "frozflame",
    "author_email": "frozflame@outlook.com",
    "license": "GNU General Public License (GPL)",
    "packages": find_packages(include=["cascadis", "cascadis.*"]),
    "zip_safe": False,
    "install_requires": read("requirements.txt"),
    "entry_points": {
        "console_scripts": [
            "cas = cascadis.__main__:registry",
            "cascadis = cascadis.__main__:registry",
        ]
    },
    "classifiers": [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    # ensure copy static file to runtime directory
    "include_package_data": True,
    "long_description": read("README.md"),
    "long_description_content_type": "text/markdown",
}

if _nsp:
    config["namespace_packages"] = [_nsp]

setuptools.setup(**config)
