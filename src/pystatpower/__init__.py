# Copyright 2024-2026 <wtwang>

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
