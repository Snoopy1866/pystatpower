from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import nct, norm, t


def _power_z(
    null_mean: float,
    mean: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an inequality test of one mean, using z-test."""

    se = std / sqrt(size)

    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf(norm.ppf(1 - alpha / 2) - (mean - null_mean) / se)
                + norm.cdf(norm.ppf(alpha / 2) - (mean - null_mean) / se)
            )
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (mean - null_mean) / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - (mean - null_mean) / se)

    return float(power)


def _power_t(
    null_mean: float,
    mean: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an inequality test of one mean, using t-test."""

    df = size - 1
    se = std / sqrt(size)
    nc = (mean - null_mean) / se

    match alternative:
        case "two-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha / 2, df), df, nc) + nct.cdf(t.ppf(alpha / 2, df), df, nc)
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return float(power)


def _power(
    null_mean: float,
    mean: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    dist: Literal["z", "t"],
) -> float:
    """Calculate the statistical power for an inequality test of one mean."""

    match dist:
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
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Calculate the statistical power for an inequality test of one mean.

    Args:
        null_mean:
            Mean under the null hypothesis.
        mean:
            Mean under the alternative hypothesis.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `two-sided`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `greater`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `less`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, a two-sided significance level is required.
            - If `alternative` is `'greater'` or `'less'`, a one-sided significance level is required.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.

    Returns:
        float: The statistical power of the test.
    """

    power = _power(null_mean, mean, std, size, alternative, alpha, dist)
    return power


def solve_size(
    *,
    null_mean: float,
    mean: float,
    std: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    power: float = 0.80,
    dist: Literal["z", "t"] = "t",
) -> int:
    """
    Estimate the required sample size for an inequality test of one mean.

    Args:
        null_mean:
            Mean under the null hypothesis.
        mean:
            Mean under the alternative hypothesis.
        std:
            Standard deviation.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `two-sided`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `greater`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `less`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, a two-sided significance level is required.
            - If `alternative` is `'greater'` or `'less'`, a one-sided significance level is required.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.

    Returns:
        int: The required sample size.
    """

    def func(size: float) -> float:
        return _power(null_mean, mean, std, size, alternative, alpha, dist) - power

    return ceil(brentq(func, 1 + 0.1, 1e12))


def solve_null_mean(
    *,
    mean: float,
    std: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    power: float = 0.80,
    dist: Literal["z", "t"] = "t",
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimate the required mean under the null hypothesis for an inequality test of one mean.

    Args:
        mean:
            Mean under the alternative hypothesis.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `two-sided`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `greater`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `less`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, a two-sided significance level is required.
            - If `alternative` is `'greater'` or `'less'`, a one-sided significance level is required.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.
        direction:
            The search direction for the mean under the null hypothesis relative to the mean under the alternative hypothesis.

            - `'greater'`: Search for the null mean that is greater than the alternative mean.
            - `'less'`: Search for the null mean that is less than the alternative mean.

    Returns:
        float: The required mean under the null hypothesis.

    Raises:
        ValueError: If `alternative` is `two-sided` but `direction` is not specified.

    Notes:
        - If `alternative` is `two-sided`, the parameter `direction` is required.
        - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.
        - If `alternative` is `'less'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.
    """

    if alternative == "two-sided":
        if direction is None:
            raise ValueError("'direction' is required when 'alternative' is 'two-sided'.")
    elif alternative == "greater":
        direction = "less"
    else:  # alternative == "less"
        direction = "greater"

    def func(null_mean: float) -> float:
        return _power(null_mean, mean, std, size, alternative, alpha, dist) - power

    match direction:
        case "greater":
            return float(brentq(func, mean, 1e9))
        case "less":
            return float(brentq(func, -1e9, mean))


def solve_mean(
    *,
    null_mean: float,
    std: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    power: float,
    dist: Literal["z", "t"],
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimate the required mean under the alternative hypothesis for an inequality test of one mean.

    Args:
        null_mean:
            Mean under the null hypothesis.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `two-sided`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `greater`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `less`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, a two-sided significance level is required.
            - If `alternative` is `'greater'` or `'less'`, a one-sided significance level is required.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.
        direction:
            The search direction for the mean under the alternative hypothesis relative to the mean under the null hypothesis.

            - `'greater'`: Search for the alternative mean that is greater than the null mean.
            - `'less'`: Search for the alternative mean that is less than the null mean.

    Returns:
        float: The required mean under the alternative hypothesis.

    Raises:
        ValueError: If `alternative` is `two-sided` but `direction` is not specified.

    Notes:
        - If `alternative` is `two-sided`, the parameter `direction` is required.
        - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.
        - If `alternative` is `'less'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.
    """

    if alternative == "two-sided":
        if direction is None:
            raise ValueError("'direction' is required when 'alternative' is 'two-sided'.")
    elif alternative == "greater":
        direction = "greater"
    else:  # alternative == "less"
        direction = "less"

    def func(mean: float) -> float:
        return _power(null_mean, mean, std, size, alternative, alpha, dist) - power

    match direction:
        case "greater":
            return float(brentq(func, null_mean, 1e9))
        case "less":
            return float(brentq(func, -1e9, null_mean))


def solve_std(
    *,
    null_mean: float,
    mean: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    power: float,
    dist: Literal["z", "t"],
) -> float:
    """
    Estimate the required standard deviation for an inequality test of one mean.

    Args:
        null_mean:
            Mean under the null hypothesis.
        mean:
            Mean under the alternative hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `two-sided`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `greater`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `less`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, a two-sided significance level is required.
            - If `alternative` is `'greater'` or `'less'`, a one-sided significance level is required.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.

    Returns:
        float: The required standard deviation.
    """

    def func(std: float) -> float:
        return _power(null_mean, mean, std, size, alternative, alpha, dist) - power

    return float(brentq(func, 1e-6, 1e12))
