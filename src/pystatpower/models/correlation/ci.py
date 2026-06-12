from math import atanh, ceil, sqrt, tanh
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm


def _distance_not_adjusted(
    correlation: float, size: float, conf_level: float, interval_type: Literal["two-sided", "upper", "lower"]
) -> float:
    """Calculate the correlation coefficient confidence interval width or the distance from the correlation coefficient to the confidence bound"""

    alpha = 1 - conf_level
    zr = atanh(correlation)

    match interval_type:
        case "two-sided":
            L = zr - norm.ppf(1 - alpha / 2) / sqrt(size - 3)
            U = zr + norm.ppf(1 - alpha / 2) / sqrt(size - 3)
            distance = tanh(U) - tanh(L)
        case "upper":
            # L = -1
            U = zr + norm.ppf(1 - alpha) / sqrt(size - 3)
            distance = tanh(U) - correlation
        case "lower":
            L = zr - norm.ppf(1 - alpha) / sqrt(size - 3)
            # U = 1
            distance = correlation - tanh(L)

    return float(distance)


def _distance_adjusted(
    correlation: float, size: float, conf_level: float, interval_type: Literal["two-sided", "upper", "lower"]
) -> float:
    """Calculate the correlation coefficient confidence interval width or the distance from the correlation coefficient to the confidence bound, adjusted for bias."""

    alpha = 1 - conf_level
    zr = atanh(correlation)
    bias = 0.5 * correlation / (size - 1)

    match interval_type:
        case "two-sided":
            L = zr - bias - norm.ppf(1 - alpha / 2) / sqrt(size - 3)
            U = zr - bias + norm.ppf(1 - alpha / 2) / sqrt(size - 3)
            distance = tanh(U) - tanh(L)
        case "upper":
            # L = -1
            U = zr - bias + norm.ppf(1 - alpha) / sqrt(size - 3)
            distance = tanh(U) - correlation
        case "lower":
            L = zr - bias - norm.ppf(1 - alpha) / sqrt(size - 3)
            # U = 1
            distance = correlation - tanh(L)

    return float(distance)


def _distance(
    correlation: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "upper", "lower"],
    bias_adj: bool,
) -> float:
    """Calculate the correlation coefficient confidence interval width or the distance from the correlation coefficient to the confidence bound"""

    if bias_adj:
        return _distance_adjusted(correlation, size, conf_level, interval_type)
    else:  # bias_adj == False
        return _distance_not_adjusted(correlation, size, conf_level, interval_type)


def solve_distance(
    *,
    correlation: float,
    size: int,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "upper", "lower"] = "two-sided",
    bias_adj: bool = False,
) -> float:
    """Calculate the correlation coefficient confidence interval width or the distance from the correlation coefficient to the confidence bound

    Args:
        correlation (float):
            Actual correlation coefficient ($r$). Must be between -1 and 1.
        size (int):
            Sample size $n$.
        conf_level (float, optional):
            Condidence level.
        interval_type (Literal["two-sided", "upper", "lower"], optional):
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
        bias_adj (bool, optional):
            Whether to adjust for bias.

    Returns:
        (float): The correlation coefficient confidence interval width or the distance from the correlation coefficient to the confidence bound.
    """

    return float(_distance(correlation, size, conf_level, interval_type, bias_adj))


def solve_size(
    *,
    correlation: float,
    distance: float,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "upper", "lower"] = "two-sided",
    bias_adj: bool = False,
) -> int:
    """Estimate the required sample size, given the correlation coefficient confidence interval width or the distance from the correlation coefficient to the confidence bound

    Args:
        correlation (float):
            Actual correlation coefficient ($r$). Must be between -1 and 1.
        distance (float):
            Correlation coefficient confidence interval width or the distance from the correlation coefficient to the confidence bound.

            - If `interval_type = 'two-sided'`, specify the correlation coefficient two-sided confidence interval width.
            - If `interval_type = 'upper'`, specify the distance from the correlation coefficient to the upper one-sided confidence bound.
            - If `interval_type = 'lower'`, specify the distance from the correlation coefficient to the lower one-sided confidence bound.
        conf_level (float, optional):
            Condidence level.
        interval_type (Literal["two-sided", "upper", "lower"], optional):
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
        bias_adj (bool, optional):
            Whether to adjust for bias.

    Returns:
        (float): The required sample size.
    """

    def func(size: float) -> float:
        return _distance(correlation, size, conf_level, interval_type, bias_adj) - distance

    return ceil(brentq(func, 3 + 1e-12, 1e12))
