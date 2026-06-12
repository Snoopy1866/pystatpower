from importlib.metadata import version

from . import correlation, mean, proportion

__version__ = version("pystatpower")

__all__ = [
    "correlation",
    "mean",
    "proportion",
]
