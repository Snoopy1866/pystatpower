# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""PyStatpower: Power Analysis Toolkit for Python.

Documentation is available in the docstrings and online at https://pystatpower.readthedocs.io/.
"""

from importlib.metadata import version

from . import correlation
from . import mean
from . import misc
from . import proportion

__version__ = version("pystatpower")

__all__ = [
    "correlation",
    "mean",
    "proportion",
    "misc",
]
