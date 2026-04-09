from math import log, sqrt

from scipy.optimize import brentq
from scipy.stats import norm

from ..._constant import SAMPLE_SIZE_SEARCH_MAX


def _power(
    null_correlation: float, correlation: float, size: float, alpha: float = 0.05, bias_adj: bool = False
) -> float:
    """Calculate the power of the difference test between two correlation coefficients.

    Args:
        null_correlation (float): Correlation coefficient under the null hypothesis.
        correlation (float): Correlation coefficient under the alternative hypothesis.
        size (float): Sample size.
        alpha (float, optional): Significance level. Default is 0.05.
        bias_adj (bool, optional): Specify whether or not the bias adjustment is used. Default is False.

    Returns:
        power(float): Power of the test.
    """

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
    null_correlation: float, correlation: float, size: float, alpha: float = 0.05, bias_adj: bool = False
) -> float:
    """Calculate the power of the difference test between two correlation coefficients.

    Args:
        null_correlation (float): Correlation coefficient under the null hypothesis.
        correlation (float): Correlation coefficient under the alternative hypothesis.
        size (float): Sample size.
        alpha (float, optional): Significance level. Default is 0.05.
        bias_adj (bool, optional): Specify whether or not the bias adjustment is used. Default is False.

    Returns:
        power(float): Power of the test.
    """

    power = _power(null_correlation, correlation, size, alpha, bias_adj)

    return float(power)


def solve_size(
    null_correlation: float, correlation: float, alpha: float = 0.05, power: float = 0.80, bias_adj: bool = False
) -> float:
    """Estimate the sample size required for the difference test between two correlation coefficients.

    Args:
        null_correlation (float): Correlation coefficient under the null hypothesis.
        correlation (float): Correlation coefficient under the alternative hypothesis.
        alpha (float, optional): Significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.80.
        bias_adj (bool, optional): Specify whether or not the bias adjustment is used. Default is False.

    Returns:
        size(float): The required sample size.
    """

    def func(size: float) -> float:
        return _power(null_correlation, correlation, size, alpha, bias_adj) - power

    size = brentq(func, 3, SAMPLE_SIZE_SEARCH_MAX)

    return float(size)


def solve_correlation(
    null_correlation: float,
    size: float,
    alpha: float = 0.05,
    power: float = 0.80,
    bias_adj: bool = False,
    search_direction: str = "upper",
) -> float:
    """
    Estimate the alternative correlation coefficient required for the difference test between two correlation coefficients.

    Args:
        nnull_correlation (float): Correlation coefficient under the null hypothesis.
        size(float): Sample size.
        alpha (float, optional): Significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.80.
        bias_adj(bool): Specify whether or not the bias adjustment is used. Default is False.
        search_direction(str): Specify the search direction relative to the null correlation. Default is 'upper'.

    Returns:
        correlation(float): The required alternative correlation.
    """

    def func(correlation: float) -> float:
        return _power(null_correlation, correlation, size, alpha, bias_adj) - power

    match search_direction.lower():
        case "lower":
            correlation = brentq(func, -0.999999, null_correlation)
        case "upper":
            correlation = brentq(func, null_correlation, 0.999999)
        case _:
            raise ValueError("search_direction must be 'lower' or 'upper'")

    return correlation


def solve_null_correlation(
    correlation: float,
    size: int,
    alpha: float = 0.05,
    power: float = 0.05,
    bias_adj: bool = False,
    search_direction: str = "lower",
) -> float:
    """
    Estimeta the null correlation coefficient required for the difference test between two correlation coefficients.

    Args:
        correlation (float): Correlation coefficient under the alternative hypothesis.
        size (int): Sample size.
        alpha (float, optional): Significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.05.
        bias_adj (bool, optional): Specify whether or not the bias adjustment is used. Default is False.
        search_direction(str): Specify the search direction relative to the alternative correlation. Default is 'lower'.

    Returns:
        null_correlation(float): The required null correlation.
    """

    def func(null_correlation: float) -> float:
        return _power(null_correlation, correlation, size, alpha, bias_adj) - power

    match search_direction.lower():
        case "lower":
            null_correlation = brentq(func, -0.999999, correlation)
        case "upper":
            null_correlation = brentq(func, correlation, 0.999999)
        case _:
            raise ValueError("search_direction must be 'lower' or 'upper'")

    return null_correlation
