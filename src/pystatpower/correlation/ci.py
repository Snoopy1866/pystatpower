from math import atanh, ceil, sqrt, tanh
from typing import Literal

from scipy.optimize import OptimizeResult, brentq, minimize_scalar
from scipy.stats import norm

from ..exceptions import SolutionNotFoundError


def _distance_not_adjusted(
    correlation: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the correlation coefficient confidence interval width or the distance from the correlation coefficient to the confidence bound."""

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
            # U = 1
            distance = correlation - tanh(L)
        case "upper":
            # L = -1
            U = zr + norm.ppf(1 - alpha) / se_recip
            distance = tanh(U) - correlation

    return float(distance)


def _distance_adjusted(
    correlation: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the width of correlation coefficient confidence interval or the distance from the correlation coefficient to the confidence bound, adjusted for bias."""

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
            # U = 1
            distance = correlation - tanh(L)
        case "upper":
            # L = -1
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
    """Calculate the width of correlation coefficient confidence interval or the distance from the correlation coefficient to the confidence bound."""

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
    """Calculate the width of correlation coefficient confidence interval or the distance from the correlation coefficient to the confidence bound.

    Args:
        correlation:
            Correlation coefficient.
        size:
            Sample size.
        conf_level:
            Condidence level.
        interval_type:
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        bias_adj:
            Whether to adjust for the bias.

    Returns:
        - If `interval_type` is `'two-sided'`, returns the width of correlation coefficient confidence interval
        - If `interval_type` is `'greater'` or `'less'`, returns the distance from the correlation coefficient to the confidence bound.
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
            The width of correlation coefficient confidence interval or the distance from the correlation coefficient to the confidence bound.

            - If `interval_type` = `'two-sided'`, the width of correlation coefficient two-sided confidence interval id required.
            - If `interval_type` = `'lower'`, the distance from the correlation coefficient to the lower one-sided confidence bound is required.
            - If `interval_type` = `'upper'`, the distance from the correlation coefficient to the upper one-sided confidence bound is required.
        conf_level:
            Condidence level.
        interval_type:
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        bias_adj (bool, optional):
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


def solve_correlation(
    *,
    distance: float,
    size: int,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    bias_adj: bool = False,
) -> float:
    """Estimate the required correlation coefficient.

    Args:
        distance:
            The width of correlation coefficient confidence interval or the distance from the correlation coefficient to the confidence bound.

            - If `interval_type` = `'two-sided'`, the width of correlation coefficient two-sided confidence interval is required.
            - If `interval_type` = `'lower'`, the distance from the correlation coefficient to the lower one-sided confidence bound is required.
            - If `interval_type` = `'upper'`, the distance from the correlation coefficient to the upper one-sided confidence bound is required.
        size:
            Sample size.
        conf_level:
            Condidence level.
        interval_type:
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        bias_adj:
            Whether to adjust for the bias.

    Returns:
        The required correlation coefficient.
    """

    def func(correlation: float) -> float:
        return _distance(correlation, size, conf_level, interval_type, bias_adj) - distance

    return float(brentq(func, 0, 1 - 1e-12))
