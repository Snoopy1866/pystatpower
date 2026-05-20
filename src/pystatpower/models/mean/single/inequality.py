from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import nct, norm, t

from ...._constant import SAMPLE_SIZE_SEARCH_MAX


def _power_z(
    null_mean: float,
    mean: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "lower one-sided", "upper one-sided"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an inequality test of one mean using z-test."""

    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf(norm.ppf(1 - alpha / 2) - sqrt(size) * (mean - null_mean) / std)
                + norm.cdf(norm.ppf(alpha / 2) - sqrt(size) * (mean - null_mean) / std)
            )
        case "lower one-sided":
            power = norm.cdf(norm.ppf(alpha) - sqrt(size) * (mean - null_mean) / std)
        case "upper one-sided":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - sqrt(size) * (mean - null_mean) / std)

    return float(power)


def _power_t(
    null_mean: float,
    mean: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "lower one-sided", "upper one-sided"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an inequality test of one mean using t-test."""

    df = size - 1
    nc = sqrt(size) * (mean - null_mean) / std

    match alternative:
        case "two-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha / 2, df), df, nc) + nct.cdf(t.ppf(alpha / 2, df), df, nc)
        case "lower one-sided":
            power = nct.cdf(t.ppf(alpha, df), df, nc)
        case "upper one-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)

    return float(power)


def _power(
    null_mean: float,
    mean: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "lower one-sided", "upper one-sided"],
    alpha: float,
    method: Literal["z", "t"],
) -> float:
    """Calculate the statistical power for an inequality test of one mean."""

    match method:
        case "z":
            power = _power_z(null_mean, mean, std, size, alternative, alpha)
        case "t":
            power = _power_t(null_mean, mean, std, size, alternative, alpha)

    return power


def solve_power(
    *,
    null_mean: float,
    mean: float,
    std: float,
    size: int,
    alternative: Literal["two-sided", "lower one-sided", "upper one-sided"],
    alpha: float,
    method: Literal["z", "t"],
) -> float:
    """
    Calculate the statistical power for an inequality test of one mean.

    Args:
        null_mean (float, optional):
            Mean under the null hypothesis ($\\mu_0$).
        mean (float, optional):
            Mean under the alternative hypothesis ($\\mu_1$).
        std (float, optional):
            Standard deviation ($\\sigma$).

            - If `method='t'`, provide the sample standard deviation ($S$).
        size (int):
            Sample size ($n$).
        alternative (Literal["two-sided", "lower one-sided", "upper one-sided"], optional):
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_0$
            - `'lower one-sided'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_0$
            - `'upper one-sided'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_0$
        alpha (float, optional):
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'lower one-sided'` or `'upper one-sided'`, provide the one-sided significance level.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's *t* distribution.

    Returns:
        (float): The calculated statistical power of the test.
    """

    power = _power(null_mean, mean, std, size, alternative, alpha, method)
    return power


def solve_size(
    *,
    null_mean: float,
    mean: float,
    std: float,
    alternative: Literal["two-sided", "lower one-sided", "upper one-sided"],
    alpha: float,
    power: float,
    method: Literal["z", "t"],
) -> int:
    """
    Estimate the required sample size for an inequality test of one mean.

    Args:
        null_mean (float, optional):
            Mean under the null hypothesis ($\\mu_0$).
        mean (float, optional):
            Mean under the alternative hypothesis ($\\mu_1$).
        std (float, optional):
            Standard deviation ($\\sigma$).

            - If `method='t'`, provide the sample standard deviation ($S$).
        alternative (Literal["two-sided", "lower one-sided", "upper one-sided"], optional):
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_0$
            - `'lower one-sided'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_0$
            - `'upper one-sided'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_0$
        alpha (float, optional):
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'lower one-sided'` or `'upper one-sided'`, provide the one-sided significance level.
        power (float, optional):
            Desired statistical power.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's *t* distribution.

    Returns:
        (int): The required sample size.
    """

    def func(size: float) -> float:
        return _power(null_mean, mean, std, size, alternative, alpha, method) - power

    size = ceil(brentq(func, 1.1, SAMPLE_SIZE_SEARCH_MAX))
    return size


def solve_null_mean(
    *,
    mean: float,
    std: float,
    size: int,
    alternative: Literal["two-sided", "lower one-sided", "upper one-sided"],
    alpha: float,
    power: float,
    method: Literal["z", "t"],
    search_direction: Literal["below", "above"] = "below",
) -> float:
    """
    Estimate the required mean under the null hypothesis for an inequality test of one mean.

    Args:
        mean (float, optional):
            Mean under the alternative hypothesis ($\\mu_1$).
        std (float, optional):
            Standard deviation ($\\sigma$).

            - If `method='t'`, provide the sample standard deviation ($S$).
        size (int):
            Sample size ($n$).
        alternative (Literal["two-sided", "lower one-sided", "upper one-sided"], optional):
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_0$
            - `'lower one-sided'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_0$
            - `'upper one-sided'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_0$
        alpha (float, optional):
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'lower one-sided'` or `'upper one-sided'`, provide the one-sided significance level.
        power (float, optional):
            Desired statistical power.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's *t* distribution.
        search_direction (Literal["below", "above"], optional):
            Specify whether to search for the null mean below or above the alternative mean.

            - `'below'`: Search the null mean below the alternative mean.
            - `'above'`: Search the null mean above the alternative mean.

    Returns:
        (float): The required mean under the null hypothesis.
    """

    def func(null_mean: float) -> float:
        return _power(null_mean, mean, std, size, alternative, alpha, method) - power

    NULL_MEAN_SEARCH_MIN = -1000000
    NULL_MEAN_SEARCH_MAX = 1000000

    match search_direction:
        case "below":
            return float(brentq(func, NULL_MEAN_SEARCH_MIN, mean))
        case "above":
            return float(brentq(func, mean, NULL_MEAN_SEARCH_MAX))


def solve_mean(
    *,
    null_mean: float,
    std: float,
    size: int,
    alternative: Literal["two-sided", "lower one-sided", "upper one-sided"],
    alpha: float,
    power: float,
    method: Literal["z", "t"],
    search_direction: Literal["below", "above"] = "above",
) -> float:
    """
    Estimate the required mean under the alternative hypothesis for an inequality test of one mean.

    Args:
        null_mean (float, optional):
            Mean under the null hypothesis ($\\mu_0$).
        std (float, optional):
            Standard deviation ($\\sigma$).

            - If `method='t'`, provide the sample standard deviation ($S$).
        size (int):
            Sample size ($n$).
        alternative (Literal["two-sided", "lower one-sided", "upper one-sided"], optional):
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_0$
            - `'lower one-sided'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_0$
            - `'upper one-sided'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_0$
        alpha (float, optional):
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'lower one-sided'` or `'upper one-sided'`, provide the one-sided significance level.
        power (float, optional):
            Desired statistical power.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's *t* distribution.
        search_direction (Literal["below", "above"], optional):
            Specify whether to search for the alternative mean below or above the null mean.

            - `'below'`: Search the alternative mean below the null mean.
            - `'above'`: Search the alternative mean above the null mean.

    Returns:
        (float): The required mean under the alternative hypothesis.
    """

    def func(mean: float) -> float:
        return _power(null_mean, mean, std, size, alternative, alpha, method) - power

    MEAN_SEARCH_MIN = -1000000
    MEAN_SEARCH_MAX = 1000000

    match search_direction:
        case "below":
            return float(brentq(func, MEAN_SEARCH_MIN, null_mean))
        case "above":
            return float(brentq(func, null_mean, MEAN_SEARCH_MAX))
