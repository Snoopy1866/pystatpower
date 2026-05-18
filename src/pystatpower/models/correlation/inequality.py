from math import ceil, log, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm

from ..._constant import SAMPLE_SIZE_SEARCH_MAX


def _power(null_correlation: float, correlation: float, size: float, alpha: float, bias_adj: bool) -> float:
    """Calculate the statistical power of the difference test between two correlation coefficients."""

    null_zeta = 1 / 2 * log((1 + null_correlation) / (1 - null_correlation))
    zeta = 1 / 2 * log((1 + correlation) / (1 - correlation))

    if bias_adj:
        power = 1 - norm.cdf(
            norm.ppf(1 - alpha / 2)
            - (abs(zeta - null_zeta) + 1 / 2 * abs(correlation - null_correlation) / (size - 1)) * sqrt(size - 3)
        )
    else:
        power = 1 - norm.cdf(norm.ppf(1 - alpha / 2) - abs(zeta - null_zeta) * sqrt(size - 3))
    return float(power)


def solve_power(
    *,
    null_correlation: float,
    correlation: float,
    size: int,
    alpha: float = 0.05,
    bias_adj: bool = False,
) -> float:
    """Calculate the statistical power of the difference test between two correlation coefficients.

    Args:
        null_correlation (float):
            Correlation coefficient under the null hypothesis.
        correlation (float):
            Correlation coefficient under the alternative hypothesis.
        size (int):
            Sample size.
        alpha (float, optional):
            Two-sided significance level.
        bias_adj (bool, optional):
            Whether or not the bias adjustment is used.

    Returns:
        (float): Power of the test.
    """

    power = _power(null_correlation, correlation, size, alpha, bias_adj)

    return float(power)


def solve_size(
    *,
    null_correlation: float,
    correlation: float,
    alpha: float = 0.05,
    power: float = 0.80,
    bias_adj: bool = False,
) -> int:
    """Estimate the required sample size for the difference test between two correlation coefficients.

    Args:
        null_correlation (float):
            Correlation coefficient under the null hypothesis.
        correlation (float):
            Correlation coefficient under the alternative hypothesis.
        alpha (float, optional):
            Two sided significance level.
        power (float, optional):
            Power of the test.
        bias_adj (bool, optional):
            Whether or not the bias adjustment is used.

    Returns:
        (int): The required sample size.
    """

    def func(size: float) -> float:
        return _power(null_correlation, correlation, size, alpha, bias_adj) - power

    size = brentq(func, 3, SAMPLE_SIZE_SEARCH_MAX)

    return ceil(size)


def solve_correlation(
    *,
    null_correlation: float,
    size: int,
    alpha: float = 0.05,
    power: float = 0.80,
    bias_adj: bool = False,
    search_direction: Literal["above", "below"] = "above",
) -> float:
    """
    Estimate the required correlation coefficient under the alternative hypothesis for the difference test between two correlation coefficients.

    Args:
        null_correlation (float):
            Correlation coefficient under the null hypothesis.
        size (int):
            Sample size.
        alpha (float, optional):
            Two-sided significance level.
        power (float, optional):
            Power of the test.
        bias_adj (bool, optional):
            Whether or not the bias adjustment is used.
        search_direction (Literal["above", "below"], optional):
            Specify whether to search for the alternative correlation below or above the null correlation.

    Returns:
        (float): required correlation coefficient under the alternative hypothesis.
    """

    def func(correlation: float) -> float:
        return _power(null_correlation, correlation, size, alpha, bias_adj) - power

    match search_direction.lower():
        case "below":
            correlation = brentq(func, -0.999999, null_correlation)
        case "above":
            correlation = brentq(func, null_correlation, 0.999999)
        case _:
            raise ValueError("search_direction must be 'below' or 'above'")

    return correlation


def solve_null_correlation(
    *,
    correlation: float,
    size: int,
    alpha: float = 0.05,
    power: float = 0.80,
    bias_adj: bool = False,
    search_direction: Literal["above", "below"] = "above",
) -> float:
    """
    Estimete the required correlation coefficient under the null hypothesis for the difference test between two correlation coefficients.

    Args:
        correlation (float):
            Correlation coefficient under the alternative hypothesis.
        size (int):
            Sample size.
        alpha (float, optional):
            Two-sided significance level.
        power (float, optional):
            Power of the test.
        bias_adj (bool, optional):
            Whether or not the bias adjustment is used.
        search_direction (Literal["above", "below"], optional):
            Specify whether to search for the null correlation below or above the alternative correlation.

    Returns:
        (float): The required correlation coefficient under the null hypothesis.
    """

    def func(null_correlation: float) -> float:
        return _power(null_correlation, correlation, size, alpha, bias_adj) - power

    match search_direction.lower():
        case "below":
            null_correlation = brentq(func, -0.999999, correlation)
        case "above":
            null_correlation = brentq(func, correlation, 0.999999)
        case _:
            raise ValueError("search_direction must be 'below' or 'above'")

    return null_correlation
