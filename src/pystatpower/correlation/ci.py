# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Power analysis for the confidence interval of a correlation coefficient.

This module provides functions to calculate or estimate the following parameters:

- width/distance
- sample size
"""

from math import atanh
from math import ceil
from math import sqrt
from math import tanh
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm


def _distance_not_adjusted(
    correlation: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the correlation coefficient confidence interval width or the distance from the correlation coefficient to the confidence limit."""
    alpha = 1 - conf_level
    zr = atanh(correlation)
    se_recip = sqrt(size - 3)

    match interval_type:
        case "two-sided":
            L = zr - norm.ppf(1 - alpha / 2) / se_recip
            U = zr + norm.ppf(1 - alpha / 2) / se_recip
            distance = tanh(U) - tanh(L)
        case "lower":
            L = zr - norm.ppf(1 - alpha) / se_recip
            distance = correlation - tanh(L)
        case "upper":
            U = zr + norm.ppf(1 - alpha) / se_recip
            distance = tanh(U) - correlation

    return float(distance)


def _distance_adjusted(
    correlation: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the width of correlation coefficient confidence interval or the distance from the correlation coefficient to the confidence limit, adjusted for bias."""
    alpha = 1 - conf_level
    zr = atanh(correlation)
    bias = 0.5 * correlation / (size - 1)
    se_recip = sqrt(size - 3)

    match interval_type:
        case "two-sided":
            L = zr - bias - norm.ppf(1 - alpha / 2) / se_recip
            U = zr - bias + norm.ppf(1 - alpha / 2) / se_recip
            distance = tanh(U) - tanh(L)
        case "lower":
            L = zr - bias - norm.ppf(1 - alpha) / se_recip
            distance = correlation - tanh(L)
        case "upper":
            U = zr - bias + norm.ppf(1 - alpha) / se_recip
            distance = tanh(U) - correlation

    return float(distance)


def _distance(
    correlation: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
    bias_adj: bool,
) -> float:
    """Calculate the width of correlation coefficient confidence interval or the distance from the correlation coefficient to the confidence limit."""
    if bias_adj:
        return _distance_adjusted(correlation, size, conf_level, interval_type)
    else:  # bias_adj == False
        return _distance_not_adjusted(correlation, size, conf_level, interval_type)


def solve_distance(
    *,
    correlation: float,
    size: int,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    bias_adj: bool = False,
) -> float:
    """Calculate the width of correlation coefficient confidence interval or the distance from the correlation coefficient to the confidence limit.

    Args:
        correlation:
            Correlation coefficient.
        size:
            Sample size.
        conf_level:
            Confidence level.

            - If `alternative` is `'two-sided'`, a two-sided confidence interval is required.
            - If `alternative` is `'lower'` or `'upper'`, a one-sided confidence interval is required.
        interval_type:
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        bias_adj:
            Whether to adjust for the bias.

    Returns:
        The width of correlation coefficient confidence interval or the distance from the correlation coefficient to the confidence limit.

            - If `interval_type` is `'two-sided'`, the width of correlation coefficient confidence interval is returned.
            - If `interval_type` is `'lower'` or `'upper'`, the distance from the correlation coefficient to the confidence limit is returned.
    """
    return _distance(correlation, size, conf_level, interval_type, bias_adj)


def solve_size(
    *,
    correlation: float,
    distance: float,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    bias_adj: bool = False,
) -> int:
    """Estimate the required sample size.

    Args:
        correlation:
            Correlation coefficient.
        distance:
            The width of correlation coefficient confidence interval or the distance from the correlation coefficient to the confidence limit.

            - If `interval_type` = `'two-sided'`, the width of correlation coefficient two-sided confidence interval id required.
            - If `interval_type` = `'lower'`, the distance from the correlation coefficient to the lower one-sided confidence limit is required.
            - If `interval_type` = `'upper'`, the distance from the correlation coefficient to the upper one-sided confidence limit is required.
        conf_level:
            Confidence level.

            - If `alternative` is `'two-sided'`, a two-sided confidence interval is required.
            - If `alternative` is `'lower'` or `'upper'`, a one-sided confidence interval is required.
        interval_type:
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        bias_adj:
            Whether to adjust for bias.

    Returns:
        The required sample size.
    """

    def func(size: float) -> float:
        return _distance(correlation, size, conf_level, interval_type, bias_adj) - distance

    lower_bound = 3 + 1e-12
    upper_bound = 1e12
    if func(lower_bound) < 0:
        # func is monotonically decreasing. If func(lower_bound) < 0, it means the required sample size is less than lower_bound.
        # Considering realistic factors, the sample size should not be lower than ceil(lower_bound)
        return ceil(lower_bound)
    else:
        return ceil(brentq(func, lower_bound, upper_bound))
