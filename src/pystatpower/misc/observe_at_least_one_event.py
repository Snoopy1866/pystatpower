# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Power analysis for observing at least one event.

This module provides functions to calculate or estimate the following parameters:

- detectable power
- sample size
"""

from math import ceil
from math import exp
from typing import Literal

from scipy.optimize import brentq


def _power_binom(proportion: float, size: float) -> float:
    """Calculate the power to observe at least one event, based on the binomial distribution."""
    return 1 - (1 - proportion) ** size


def _power_poisson(proportion: float, size: float) -> float:
    """Calculate the power to observe at least one event, based on the Poisson distribution."""
    return 1 - exp(-size * proportion)


def _power(proportion: float, size: float, dist: Literal["bin", "poisson"]) -> float:
    match dist:
        case "bin":
            return _power_binom(proportion, size)
        case "poisson":
            return _power_poisson(proportion, size)


def solve_power(*, proportion: float, size: int, dist: Literal["bin", "poisson"] = "bin") -> float:
    """Calculate the detection power.

    Args:
        proportion:
            Event proportion.
        size:
            Sample size.
        dist:
            The distribution of the number of events that occurred.

            - `'bin'`: binomial distribution
            - `'poisson'`: Poisson distribution

    Returns:
        The power to observe at least one event.
    """
    return _power(proportion, size, dist)


def solve_size(*, proportion: float, power: float = 0.95, dist: Literal["bin", "poisson"] = "bin") -> int:
    """Estimate the required sample size.

    Args:
        proportion:
            Event proportion.
        power:
            The detection power.

            0.95 is a commonly used value for the detection power.
        dist:
            The distribution of the number of events that occurred.

            - `'bin'`: binomial distribution
            - `'poisson'`: Poisson distribution

    Returns:
        The required sample size.
    """

    def func(size: float) -> float:
        return _power(proportion, size, dist) - power

    return ceil(brentq(func, 1e-12, 1e12))


def solve_proportion(*, size: int, power: float = 0.95, dist: Literal["bin", "poisson"] = "bin") -> float:
    """Estimate the required event proportion.

    Args:
        size:
            Sample size.
        power:
            The detection power.

            0.95 is a commonly used value for the detection power.
        dist:
            The distribution of the number of events that occurred.

            - `'bin'`: binomial distribution
            - `'poisson'`: Poisson distribution

    Returns:
        The required event proportion.
    """

    def func(proportion: float) -> float:
        return _power(proportion, size, dist) - power

    return float(brentq(func, 0, 1))
