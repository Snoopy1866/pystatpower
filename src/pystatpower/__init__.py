from importlib.metadata import version

from . import models

__version__ = version("pystatpower")

__all__ = [
    "models",
    "constant",
]
