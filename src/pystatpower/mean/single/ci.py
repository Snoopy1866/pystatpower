# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Power analysis for the confidence interval of a single mean.

This module provides functions to calculate or estimate the following parameters:

- precision
- sample size
- standard deviation
"""

from math import ceil
from math import sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm
from scipy.stats import t


def _precision_z(
    std: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "one-sided", "lower", "upper"],
) -> float:
    """Calculate the distance from the mean to the confidence limit (commonly known as precision), using the z-distribution."""
    alpha = 1 - conf_level

    se = std / sqrt(size)

    match interval_type:
        case "two-sided":
            precision = norm.ppf(1 - alpha / 2) * se
        case "one-sided" | "lower" | "upper":
            precision = norm.ppf(1 - alpha) * se

    return float(precision)


def _precision_t(
    std: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "one-sided", "lower", "upper"],
) -> float:
    """Calculate the distance from the mean to the confidence limit (commonly known as precision), using the t-distribution."""
    alpha = 1 - conf_level

    se = std / sqrt(size)
    df = size - 1

    match interval_type:
        case "two-sided":
            precision = t.ppf(1 - alpha / 2, df) * se
        case "one-sided" | "lower" | "upper":
            precision = t.ppf(1 - alpha, df) * se

    return float(precision)


def _precision(
    std: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "one-sided", "lower", "upper"],
    dist: Literal["z", "t"],
) -> float:
    """Calculate the distance from the mean to the confidence limit (commonly known as precision)."""
    match dist:
        case "z":
            return _precision_z(std, size, conf_level, interval_type)
        case "t":
            return _precision_t(std, size, conf_level, interval_type)


def solve_precision(
    *,
    std: float,
    size: int,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "one-sided", "lower", "upper"] = "two-sided",
    dist: Literal["z", "t"] = "t",
) -> float:
    """Calculate the distance from the mean to the confidence limit (commonly known as precision).

    Args:
        std:
            Standard deviation.
        size:
            Sample size.
        conf_level:
            Confidence level.

            - If `interval_type` is `'two-sided'`, a two-sided confidence level should be specified
            - If `interval_type` is `'one-sided'`, `'lower'` or `'upper'`, a one-sided confidence level should be specified
        interval_type:
            The type of confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'one-sided'`: One-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        dist:
            The distribution used to construct the confidence interval.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t-distribution.

    Returns:
        The distance from the mean to the confidence limit (commonly known as precision).

    Notes:
        Since the confidence interval for the mean is symmetric, specifying `interval_type` as `'lower'`, `'upper'`, or `'one-sided'` works consistently.
    """
    return _precision(std, size, conf_level, interval_type, dist)


def solve_size(
    *,
    precision: float,
    std: float,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "one-sided", "lower", "upper"] = "two-sided",
    dist: Literal["z", "t"] = "t",
) -> int:
    """Estimate the required sample size.

    Args:
        precision:
            Distance from the mean to the confidence limit.
        std:
            Standard deviation.
        conf_level:
            Confidence level.

            - If `interval_type` is `'two-sided'`, a two-sided confidence level should be specified
            - If `interval_type` is `'one-sided'`, `'lower'` or `'upper'`, a one-sided confidence level should be specified
        interval_type:
            The type of confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'one-sided'`: One-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        dist:
            The distribution used to construct the confidence interval.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t-distribution.

    Returns:
        The required sample size.

    Notes:
        Since the confidence interval for the mean is symmetric, specifying `interval_type` as `'lower'`, `'upper'`, or `'one-sided'` works consistently.
    """

    def func(size: float) -> float:
        return _precision(std, size, conf_level, interval_type, dist) - precision

    return ceil(brentq(func, 1 + 1e-12, 1e12))


def solve_std(
    *,
    precision: float,
    size: int,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "one-sided", "lower", "upper"] = "two-sided",
    dist: Literal["z", "t"] = "t",
) -> float:
    """Estimate the required standard deviation.

    Args:
        precision:
            Distance from the mean to the confidence limit.
        size:
            Sample size.
        conf_level:
            Confidence level.

            - If `interval_type` is `'two-sided'`, a two-sided confidence level should be specified
            - If `interval_type` is `'one-sided'`, `'lower'` or `'upper'`, a one-sided confidence level should be specified
        interval_type:
            The type of confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'one-sided'`: One-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        dist:
            The distribution used to construct the confidence interval.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t-distribution.

    Returns:
        The required standard deviation.

    Notes:
        Since the confidence interval for the mean is symmetric, specifying `interval_type` as `'lower'`, `'upper'`, or `'one-sided'` works consistently.
    """
    # First calculate precision d' under standard deviation s' = 1, and then use the conversion formula s = d/d' to
    # directly obtain the required standard deviation s under given precision d.
    # This algorithm does not require the use of brentq inverse solution.
    return precision / _precision(1, size, conf_level, interval_type, dist)
