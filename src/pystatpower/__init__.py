from importlib.metadata import version

from .models import correlation, mean, proportion

__version__ = version("pystatpower")

__all__ = [
    "correlation",
    "mean",
    "proportion",
]
