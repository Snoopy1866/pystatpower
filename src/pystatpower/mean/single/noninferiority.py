from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import nct, t


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


def _margin(margin: float, alternative: Literal["greater", "less"]) -> float:
    """Convert margin to standard form based on alternative hypothesis"""

    match alternative:
        case "greater":
            return -abs(margin)
        case "less":
            return abs(margin)


def _power(
    diff: float,
    margin: float,
    std: float,
    size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a non-inferiority test of one sample mean."""

    df = size - 1
    nc = (diff - margin) * sqrt(size) / std
    match alternative:
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return float(power)


def solve_power(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    diff: float | None = None,
    margin: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
) -> float:
    """
    Calculate the statistical power for a non-inferiority test of one sample mean.

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
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `alternative` is `'greater'`, the actual margin used internally is `-abs(margin)`.
            - If `alternative` is `'less'`, the actual margin used internally is `abs(margin)`.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.

    Returns:
        float: The statistical power of the test.

    Raises:
        ValueError: If `diff` is not specified, and either `mean` or `null_mean` is not specified.
    """

    diff = _verify_mean_and_get_diff(mean, null_mean, diff)

    margin = _margin(margin, alternative)

    return _power(diff, margin, std, size, alternative, alpha)


def solve_size(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    diff: float | None = None,
    margin: float,
    std: float,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
) -> int:
    """
    Estimate the required sample size for a non-inferiority test of one sample mean.

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
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `alternative` is `'greater'`, the actual margin used internally is `-abs(margin)`.
            - If `alternative` is `'less'`, the actual margin used internally is `abs(margin)`.
        std:
            Standard deviation.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.

    Returns:
        int: The required sample size.

    Raises:
        ValueError: If `diff` is not specified, and either `mean` or `null_mean` is not specified.
    """

    diff = _verify_mean_and_get_diff(mean, null_mean, diff)

    margin = _margin(margin, alternative)

    def func(size: float) -> float:
        return _power(diff, margin, std, size, alternative, alpha) - power

    return ceil(brentq(func, 1 + 0.1, 1e12))


def solve_diff(
    *,
    margin: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
) -> float:
    """
    Estimete the required mean difference between the alternative hypothesis and the null hypothesis for a non-inferiority test of one sample mean.

    Args:
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `alternative` is `'greater'`, the actual margin used internally is `-abs(margin)`.
            - If `alternative` is `'less'`, the actual margin used internally is `abs(margin)`.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.

    Returns:
        float: The required mean difference between the alternative hypothesis and the null hypothesis.
    """

    margin = _margin(margin, alternative)

    def func(diff: float) -> float:
        return _power(diff, margin, std, size, alternative, alpha) - power

    match alternative:
        case "greater":
            return float(brentq(func, margin, 1e8))
        case "less":
            return float(brentq(func, -1e8, margin))


def solve_mean(
    *,
    null_mean: float,
    margin: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
) -> float:
    """
    Estimate the required mean under the alternative hypothesis for a non-inferiority test of one sample mean.

    Args:
        null_mean:
            Mean under the null hypothesis.

            If `diff` is not specified, this parameter and `mean` are required.
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `alternative` is `'greater'`, the actual margin used internally is `-abs(margin)`.
            - If `alternative` is `'less'`, the actual margin used internally is `abs(margin)`.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.

    Returns:
        float: The required mean under the alternative hypothesis.
    """

    margin = _margin(margin, alternative)

    def func(mean: float) -> float:
        return _power(mean - null_mean, margin, std, size, alternative, alpha) - power

    match alternative:
        case "greater":
            return float(brentq(func, null_mean + margin, 1e6))
        case "less":
            return float(brentq(func, -1e6, null_mean + margin))


def solve_null_mean(
    *,
    mean: float,
    margin: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
) -> float:
    """
    Estimate the required mean under the null hypothesis for a non-inferiority test of one sample mean.

    Args:
        mean:
            Mean under the alternative hypothesis.

            If `diff` is not specified, this parameter and `null_mean` are required.
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `alternative` is `'greater'`, the actual margin used internally is `-abs(margin)`.
            - If `alternative` is `'less'`, the actual margin used internally is `abs(margin)`.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.

    Returns:
        float: The required mean under the null hypothesis.
    """

    def func(null_mean: float) -> float:
        return _power(mean - null_mean, margin, std, size, alternative, alpha) - power

    match alternative:
        case "greater":
            return float(brentq(func, -1e6, mean - margin))
        case "less":
            return float(brentq(func, mean - margin, 1e6))


def solve_std(
    *,
    null_mean: float | None = None,
    mean: float | None = None,
    diff: float | None = None,
    margin: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
) -> float:
    """
    Estimate the required standard deviation for a non-inferiority test of one sample mean.

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
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `alternative` is `'greater'`, the actual margin used internally is `-abs(margin)`.
            - If `alternative` is `'less'`, the actual margin used internally is `abs(margin)`.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.

    Returns:
        float: The required standard deviation.

    Raises:
        ValueError: If `diff` is not specified, and either `mean` or `null_mean` is not specified.
    """

    diff = _verify_mean_and_get_diff(mean, null_mean, diff)

    margin = _margin(margin, alternative)

    def func(std: float) -> float:
        return _power(diff, margin, std, size, alternative, alpha) - power

    return float(brentq(func, 1e-6, 1e12))


def solve_margin(
    *,
    null_mean: float | None = None,
    mean: float | None = None,
    diff: float | None = None,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
) -> float:
    """
    Estimate the required margin for a non-inferiority test of one sample mean.

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

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.

    Returns:
        float:
            The required non-inferiority margin.

            - If `alternative` is `'greater'`, the returned value is in the range $(-\\infty, \\hat{\\mu} - \\hat{\\mu}_0)$
            - If `alternative` is `'less'`, the returned value is in the range $(\\hat{\\mu} - \\hat{\\mu}_0, +\\infty)$

    Raises:
        ValueError: If `diff` is not specified, and either `mean` or `null_mean` is not specified.
    """

    diff = _verify_mean_and_get_diff(mean, null_mean, diff)

    def func(margin: float) -> float:
        return _power(diff, margin, std, size, alternative, alpha) - power

    match alternative:
        case "greater":
            return float(brentq(func, -1e6, diff))
        case "less":
            return float(brentq(func, diff, 1e6))
