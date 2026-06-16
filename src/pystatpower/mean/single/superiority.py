from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import nct, t


def _power(
    diff: float,
    margin: float,
    std: float,
    size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a superiority test of one sample mean."""

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
    null_mean: float | None,
    mean: float | None,
    diff: float | None,
    margin: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
) -> float:
    """
    Calculate the statistical power for a superiority test of one sample mean.

    Args:
        null_mean (float, optional):
            Mean under the null hypothesis.

            If `diff` is not specified, this parameter must be specified, otherwise, this parameter is ignored.
        mean (float, optional):
            Mean under the alternative hypothesis.

            If `diff` is not specified, this parameter must be specified, otherwise, this parameter is ignored.
        diff (float, optional):
            Difference between the mean under the null hypothesis and the mean under the alternative hypothesis.

            If both `null_mean` and `mean` are not provided, `diff` must be provided.
        margin (float):
            Superiority margin.

            - If `alternative` is `'greater'`, `margin` must be a positive value.
            - If `alternative` is `'less'`, `margin` must be a negative value.
        std (float):
            Standard deviation.
        size (int):
            Sample size.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis.

            - `'greater'`: upper-tailed alternative hypothesis, used when higher means are better.
            - `'less'`: lower-tailed alternative hypothesis, used when higher means are worse.
        alpha (float, optional):
            One-sided significance level.

    Returns:
        float: The calculated statistical power of the test.

    Raises:
        ValueError: If `diff` is None, and `null_mean` or `mean` is None.
    """

    if diff is None:
        if null_mean is None or mean is None:
            raise ValueError("`null_mean` and `mean` must be provided when `diff` is not provided.")
        diff = mean - null_mean

    return _power(diff, margin, std, size, alternative, alpha)


def solve_size(
    *,
    null_mean: float | None,
    mean: float | None,
    diff: float | None,
    margin: float,
    std: float,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
) -> int:
    """
    Estimate the required sample size for a superiority test of one sample mean.

    Args:
        null_mean (float, optional):
            Mean under the null hypothesis.

            If `diff` is not specified, this parameter must be specified, otherwise, this parameter is ignored.
        mean (float, optional):
            Mean under the alternative hypothesis.

            If `diff` is not specified, this parameter must be specified, otherwise, this parameter is ignored.
        diff (float, optional):
            Difference between the mean under the null hypothesis and the mean under the alternative hypothesis.

            If both `null_mean` and `mean` are not provided, `diff` must be provided.
        margin (float):
            Superiority margin.

            - If `alternative` is `'greater'`, `margin` must be a positive value.
            - If `alternative` is `'less'`, `margin` must be a negative value.
        std (float):
            Standard deviation.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis.

            - `'greater'`: upper-tailed alternative hypothesis, used when higher means are better.
            - `'less'`: lower-tailed alternative hypothesis, used when higher means are worse.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.

    Returns:
        (int): The required sample size.

    Raises:
        ValueError: If `diff` is None, and `null_mean` or `mean` is None.
    """

    if diff is None:
        if null_mean is None or mean is None:
            raise ValueError("`null_mean` and `mean` must be provided when `diff` is not provided.")
        diff = mean - null_mean

    def func(size: float) -> float:
        return _power(diff, margin, std, size, alternative, alpha) - power

    return ceil(brentq(func, 2, 1e12))


def solve_diff(
    *,
    margin: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
) -> float:
    """
    Estimete the required difference between the mean under the null hypothesis and the mean under the alternative hypothesis for a superiority test of one sample mean.

    Args:
        margin (float):
            Superiority margin.

            - If `alternative` is `'greater'`, `margin` must be a positive value.
            - If `alternative` is `'less'`, `margin` must be a negative value.
        std (float):
            Standard deviation.
        size (float):
            Sample size.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis.

            - `'greater'`: upper-tailed alternative hypothesis, used when higher means are better.
            - `'less'`: lower-tailed alternative hypothesis, used when higher means are worse.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.

    Returns:
        float: The required difference between the the mean under the null hypothesis and the mean under the alternative hypothesis.
    """

    def func(diff: float) -> float:
        return _power(diff, margin, std, size, alternative, alpha) - power

    match alternative:
        case "greater":
            return float(brentq(func, margin, 1e6))
        case "less":
            return float(brentq(func, -1e6, margin))


def solve_null_mean(
    *,
    mean: float,
    margin: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
) -> float:
    """
    Estimate the required mean under the null hypothesis for a superiority test of one sample mean.

    Args:
        mean (float):
            Mean under the alternative hypothesis.
        margin (float):
            Superiority margin.

            - If `alternative` is `'greater'`, `margin` must be a positive value.
            - If `alternative` is `'less'`, `margin` must be a negative value.
        std (float):
            Standard deviation.
        size (float):
            Sample size.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis.

            - `'greater'`: upper-tailed alternative hypothesis, used when higher means are better.
            - `'less'`: lower-tailed alternative hypothesis, used when higher means are worse.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.

    Returns:
        float: The required mean under the null hypothesis.
    """

    def func(null_mean: float) -> float:
        return _power(mean - null_mean, margin, std, size, alternative, alpha) - power

    match alternative:
        case "greater":
            return float(brentq(func, -1e8, mean - margin))
        case "less":
            return float(brentq(func, mean - margin, 1e8))


def solve_mean(
    *,
    null_mean: float,
    margin: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
) -> float:
    """
    Estimate the required mean under the alternative hypothesis for a superiority test of one sample mean.

    Args:
        null_mean (float):
            Mean under the null hypothesis.
        margin (float):
            Superiority margin.

            - If `alternative` is `'greater'`, `margin` must be a positive value.
            - If `alternative` is `'less'`, `margin` must be a negative value.
        std (float):
            Standard deviation.
        size (float):
            Sample size.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis.

            - `'greater'`: upper-tailed alternative hypothesis, used when higher means are better.
            - `'less'`: lower-tailed alternative hypothesis, used when higher means are worse.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.

    Returns:
        float: The required mean under the alternative hypothesis.
    """

    def func(mean: float) -> float:
        return _power(mean - null_mean, margin, std, size, alternative, alpha) - power

    match alternative:
        case "greater":
            return float(brentq(func, null_mean + margin, 1e8))
        case "less":
            return float(brentq(func, -1e8, null_mean + margin))


def solve_std(
    *,
    null_mean: float | None,
    mean: float | None,
    diff: float | None,
    margin: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
) -> float:
    """
    Estimate the required standard deviation for a superiority test of one sample mean.

    Args:
        null_mean (float, optional):
            Mean under the null hypothesis.

            If `diff` is not specified, this parameter must be specified, otherwise, this parameter is ignored.
        mean (float, optional):
            Mean under the alternative hypothesis.

            If `diff` is not specified, this parameter must be specified, otherwise, this parameter is ignored.
        diff (float, optional):
            Difference between the mean under the null hypothesis and the mean under the alternative hypothesis.

            If both `null_mean` and `mean` are not provided, `diff` must be provided.
        margin (float):
            Superiority margin.

            - If `alternative` is `'greater'`, `margin` must be a positive value.
            - If `alternative` is `'less'`, `margin` must be a negative value.
        size (float):
            Sample size.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis.

            - `'greater'`: upper-tailed alternative hypothesis, used when higher means are better.
            - `'less'`: lower-tailed alternative hypothesis, used when higher means are worse.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.

    Returns:
        float: The required standard deviation.

    Raises:
        ValueError: If `diff` is None, and `null_mean` or `mean` is None.
    """

    if diff is None:
        if null_mean is None or mean is None:
            raise ValueError("`null_mean` and `mean` must be provided when `diff` is not provided.")
        diff = mean - null_mean

    def func(std: float) -> float:
        return _power(diff, margin, std, size, alternative, alpha) - power

    return float(brentq(func, 1e-7, 1e12))


def solve_margin(
    *,
    null_mean: float | None = None,
    mean: float | None = None,
    diff: float | None = None,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
) -> float:
    """
    Estimate the required margin for a superiority test of one sample mean.

    Args:
        null_mean (float, optional):
            Mean under the null hypothesis.

            If `diff` is not specified, this parameter must be specified, otherwise, this parameter is ignored.
        mean (float, optional):
            Mean under the alternative hypothesis.

            If `diff` is not specified, this parameter must be specified, otherwise, this parameter is ignored.
        diff (float, optional):
            Difference between the mean under the null hypothesis and the mean under the alternative hypothesis.

            If both `null_mean` and `mean` are not provided, `diff` must be provided.
        std (float):
            Standard deviation.
        size (float):
            Sample size.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis.

            - `'greater'`: upper-tailed alternative hypothesis, used when higher means are better.
            - `'less'`: lower-tailed alternative hypothesis, used when higher means are worse.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.

    Returns:
        float: The required superiority margin.

    Raises:
        ValueError: If `diff` is None, and `null_mean` or `mean` is None.
    """

    if diff is None:
        if null_mean is None or mean is None:
            raise ValueError("`null_mean` and `mean` must be provided when `diff` is not provided.")
        diff = mean - null_mean

    def func(margin: float) -> float:
        return _power(diff, margin, std, size, alternative, alpha) - power

    match alternative:
        case "greater":
            return float(brentq(func, -1e8, diff))
        case "less":
            return float(brentq(func, diff, 1e8))
