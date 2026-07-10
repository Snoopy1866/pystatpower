from importlib.metadata import version

from . import correlation, mean, misc, proportion

__version__ = version("pystatpower")

__all__ = [
    "correlation",
    "mean",
    "proportion",
    "misc",
]
