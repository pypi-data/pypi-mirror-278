# Copyright: 2024 Cardiff University
# SPDX-License-Idenfitifer: MIT

"""Codeclimate parser for RPMlint.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

from .parser import parse as parse_rpmlint

try:
    from ._version import version as __version__
except ModuleNotFoundError:  # development mode
    __version__ = "dev"
