from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import nct, norm, t


def _verify_mean_and_get_diff(
    mean: float | None,
    null_mean: float | None,
    diff: float | None,
) -> float:

    if diff is None:
        if mean is None or null_mean is None:
            raise ValueError("When 'diff' is omitted, both 'mean' and 'null_mean' are required.")
        diff = mean - null_mean

    return diff


def _power_z(
    diff: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using z-test."""

    se = std / sqrt(size)

    match alternative:
        case "two-sided":
            power = 1 - norm.cdf(norm.ppf(1 - alpha / 2) - diff / se) + norm.cdf(norm.ppf(alpha / 2) - diff / se)
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - diff / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - diff / se)

    return float(power)


def _power_t(
    diff: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using t-test."""

    df = size - 1
    se = std / sqrt(size)
    nc = diff / se

    match alternative:
        case "two-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha / 2, df), df, nc) + nct.cdf(t.ppf(alpha / 2, df), df, nc)
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return float(power)


def _power(
    diff: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    dist: Literal["z", "t"],
) -> float:
    """Calculate the statistical power."""

    match dist:
        case "z":
            power = _power_z(diff, std, size, alternative, alpha)
        case "t":
            power = _power_t(diff, std, size, alternative, alpha)

    return power


def solve_power(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    diff: float | None = None,
    std: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Calculate the statistical power.

    Args:
        mean:
            Mean under the alternative hypothesis.

            If `diff` is not specified, this parameter and `null_mean` are required.
        null_mean:
            Mean under the null hypothesis.

            If `diff` is not specified, this parameter and `mean` are required.
        diff:
            Mean difference between the alternative hypothesis and the null hypothesis.

            If both `mean` and `null_mean` are not specified, this parameter is required.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        float: The statistical power of the test.

    Raises:
        ValueError: If `diff` is not specified, and either `mean` or `null_mean` is not specified.
    """

    diff = _verify_mean_and_get_diff(mean, null_mean, diff)

    return _power(diff, std, size, alternative, alpha, dist)


def solve_size(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    diff: float | None = None,
    std: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    power: float = 0.80,
    dist: Literal["z", "t"] = "t",
) -> int:
    """
    Estimate the required sample size.

    Args:
        mean:
            Mean under the alternative hypothesis.

            If `diff` is not specified, this parameter and `null_mean` are required.
        null_mean:
            Mean under the null hypothesis.

            If `diff` is not specified, this parameter and `mean` are required.
        diff:
            Mean difference between the alternative hypothesis and the null hypothesis.

            If both `mean` and `null_mean` are not specified, this parameter is required.
        std:
            Standard deviation.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        int: The required sample size.

    Raises:
        ValueError: If `diff` is not specified, and either `mean` or `null_mean` is not specified.
    """

    diff = _verify_mean_and_get_diff(mean, null_mean, diff)

    def func(size: float) -> float:
        return _power(diff, std, size, alternative, alpha, dist) - power

    return ceil(brentq(func, 1 + 0.1, 1e12))


def solve_diff(
    *,
    std: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    power: float,
    dist: Literal["z", "t"],
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimate the required mean difference.

    Args:
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.
        direction:
            The search direction for the mean difference relative to zero.

            - `'greater'`: Search for the mean difference that is greater than zero.
            - `'less'`: Search for the mean difference that is less than zero.

            !!! note
                - If `alternative` is `'two-sided'`, the parameter `direction` is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.

    Returns:
        float: The required mean difference between the alternative hypothesis and the null hypothesis.

    Raises:
        ValueError: If `alternative` is `'two-sided'` but `direction` is not specified.
    """

    if alternative == "two-sided":
        if direction is None:
            raise ValueError("'direction' is required when 'alternative' is 'two-sided'.")
    elif alternative == "greater":
        direction = "greater"
    else:  # alternative == "less"
        direction = "less"

    def func(diff: float) -> float:
        return _power(diff, std, size, alternative, alpha, dist) - power

    match direction:
        case "greater":
            return float(brentq(func, 0, 1e9))
        case "less":
            return float(brentq(func, -1e9, 0))


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
    Estimate the required mean under the alternative hypothesis.

    Args:
        null_mean:
            Mean under the null hypothesis.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.
        direction:
            The search direction for the mean under the alternative hypothesis relative to the mean under the null hypothesis.

            - `'greater'`: Search for the alternative mean that is greater than the null mean.
            - `'less'`: Search for the alternative mean that is less than the null mean.

            !!! note
                - If `alternative` is `'two-sided'`, the parameter `direction` is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.

    Returns:
        float: The required mean under the alternative hypothesis.

    Raises:
        ValueError: If `alternative` is `'two-sided'` but `direction` is not specified.
    """

    if alternative == "two-sided":
        if direction is None:
            raise ValueError("'direction' is required when 'alternative' is 'two-sided'.")
    elif alternative == "greater":
        direction = "greater"
    else:  # alternative == "less"
        direction = "less"

    def func(mean: float) -> float:
        return _power(mean - null_mean, std, size, alternative, alpha, dist) - power

    match direction:
        case "greater":
            return float(brentq(func, null_mean, 1e9))
        case "less":
            return float(brentq(func, -1e9, null_mean))


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
    Estimate the required mean under the null hypothesis.

    Args:
        mean:
            Mean under the alternative hypothesis.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.
        direction:
            The search direction for the mean under the null hypothesis relative to the mean under the alternative hypothesis.

            - `'greater'`: Search for the null mean that is greater than the alternative mean.
            - `'less'`: Search for the null mean that is less than the alternative mean.

            !!! note
                - If `alternative` is `'two-sided'`, the parameter `direction` is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.

    Returns:
        float: The required mean under the null hypothesis.

    Raises:
        ValueError: If `alternative` is `'two-sided'` but `direction` is not specified.
    """

    if alternative == "two-sided":
        if direction is None:
            raise ValueError("'direction' is required when 'alternative' is 'two-sided'.")
    elif alternative == "greater":
        direction = "less"
    else:  # alternative == "less"
        direction = "greater"

    def func(null_mean: float) -> float:
        return _power(mean - null_mean, std, size, alternative, alpha, dist) - power

    match direction:
        case "greater":
            return float(brentq(func, mean, 1e9))
        case "less":
            return float(brentq(func, -1e9, mean))


def solve_std(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    diff: float | None = None,
    size: int,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    power: float,
    dist: Literal["z", "t"],
) -> float:
    """
    Estimate the required standard deviation.

    Args:
        mean:
            Mean under the alternative hypothesis.

            If `diff` is not specified, this parameter and `null_mean` are required.
        null_mean:
            Mean under the null hypothesis.

            If `diff` is not specified, this parameter and `mean` are required.
        diff:
            Mean difference between the alternative hypothesis and the null hypothesis.

            If both `mean` and `null_mean` are not specified, this parameter is required.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        float: The required standard deviation.

    Raises:
        ValueError: If `diff` is not specified, and either `mean` or `null_mean` is not specified.
    """

    diff = _verify_mean_and_get_diff(mean, null_mean, diff)

    def func(std: float) -> float:
        return _power(diff, std, size, alternative, alpha, dist) - power

    return float(brentq(func, 1e-6, 1e12))
