from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm


def _power_p0(
    proportion: float,
    null_proportion: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an equality test of one proportion, using p0 to calculate the variance."""

    h1_z_mean = (proportion - null_proportion) / sqrt(null_proportion * (1 - null_proportion) / size)
    h1_z_std = sqrt(proportion * (1 - proportion) / (null_proportion * (1 - null_proportion)))
    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf((norm.ppf(1 - alpha / 2) - h1_z_mean) / h1_z_std)
                + norm.cdf((norm.ppf(alpha / 2) - h1_z_mean) / h1_z_std)
            )
        case "greater":
            power = 1 - norm.cdf((norm.ppf(1 - alpha) - h1_z_mean) / h1_z_std)
        case "less":
            power = norm.cdf((norm.ppf(alpha) - h1_z_mean) / h1_z_std)
    return float(power)


def _power_p0_cc(
    proportion: float,
    null_proportion: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an equality test of one proportion, using p0 with continuity correction to calculate the variance."""

    if abs(proportion - null_proportion) <= 1 / (2 * size):
        c = 0
    elif proportion > null_proportion:
        c = -1 / (2 * size)
    else:  # proportion < null_proportion
        c = 1 / (2 * size)

    h1_z_mean = (proportion - null_proportion + c) / sqrt(null_proportion * (1 - null_proportion) / size)
    h1_z_std = sqrt(proportion * (1 - proportion) / (null_proportion * (1 - null_proportion)))
    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf((norm.ppf(1 - alpha / 2) - h1_z_mean) / h1_z_std)
                + norm.cdf((norm.ppf(alpha / 2) - h1_z_mean) / h1_z_std)
            )
        case "greater":
            power = 1 - norm.cdf((norm.ppf(1 - alpha) - h1_z_mean) / h1_z_std)
        case "less":
            power = norm.cdf((norm.ppf(alpha) - h1_z_mean) / h1_z_std)
    return float(power)


def _power_phat(
    proportion: float,
    null_proportion: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an equality test of one proportion, using phat to calculate the variance."""

    h1_z_mean = (proportion - null_proportion) / sqrt(proportion * (1 - proportion) / size)
    match alternative:
        case "two-sided":
            power = 1 - norm.cdf(norm.ppf(1 - alpha / 2) - h1_z_mean) + norm.cdf(norm.ppf(alpha / 2) - h1_z_mean)
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - h1_z_mean)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - h1_z_mean)

    return float(power)


def _power_phat_cc(
    proportion: float,
    null_proportion: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an equality test of one proportion, using phat with continuity correction to calculate the variance."""

    if abs(proportion - null_proportion) <= 1 / (2 * size):
        c = 0
    elif proportion > null_proportion:
        c = -1 / (2 * size)
    else:  # proportion < null_proportion
        c = 1 / (2 * size)

    h1_z_mean = (proportion - null_proportion + c) / sqrt(proportion * (1 - proportion) / size)
    match alternative:
        case "two-sided":
            power = 1 - norm.cdf(norm.ppf(1 - alpha / 2) - h1_z_mean) + norm.cdf(norm.ppf(alpha / 2) - h1_z_mean)
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - h1_z_mean)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - h1_z_mean)

    return float(power)


def _power(
    proportion: float,
    null_proportion: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power for an equality test of one proportion."""

    match method:
        case "z-p0":
            if continuity_correction:
                return _power_p0_cc(proportion, null_proportion, size, alternative, alpha)
            else:
                return _power_p0(proportion, null_proportion, size, alternative, alpha)
        case "z-phat":
            if continuity_correction:
                return _power_phat_cc(proportion, null_proportion, size, alternative, alpha)
            else:
                return _power_phat(proportion, null_proportion, size, alternative, alpha)


def solve_power(
    *,
    proportion: float,
    null_proportion: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    method: Literal["z-p0", "z-phat"] = "z-phat",
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the statistical power for an equality test of one proportion.

    Args:
        proportion (float):
            Proportion under the alternative hypothesis.
        null_proportion:
            Proportion under the null hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $p ≠ p_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $p > p_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $p < p_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        float: The statistical power of the test.
    """

    return _power(proportion, null_proportion, size, alternative, alpha, method, continuity_correction)


def solve_size(
    *,
    proportion: float,
    null_proportion: float,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"] = "z-phat",
    continuity_correction: bool = False,
) -> int:
    """
    Estimate the required sample size for an equality test of one proportion.

    Args:
        proportion (float):
            Proportion under the alternative hypothesis.
        null_proportion:
            Proportion under the null hypothesis.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $p ≠ p_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $p > p_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $p < p_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        int: The required sample size.
    """

    def func(size: float) -> float:
        return _power(proportion, null_proportion, size, alternative, alpha, method, continuity_correction) - power

    return ceil(brentq(func, 1e-12, 1e12))


def solve_proportion(
    *,
    null_proportion: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"] = "z-phat",
    continuity_correction: bool = False,
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimate the required proportion under the alternative hypothesis for an equality test of one proportion.

    Args:
        null_proportion:
            Proportion under the null hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $p ≠ p_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $p > p_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $p < p_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.
        direction:
            The direction for the proportion under the alternative hypothesis relative to the proportion under the null hypothesis.

            - `'greater'`: Search for the alternative proportion greater than the null proportion.
            - `'less'`: Search for the alternative proportion less than the null proportion.

            !!! note
                - If `alternative` is `'two-sided'`, this parameter is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'greater'`, and this parameter is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'less'`, and this parameter is ignored.

    Returns:
        float: The required proportion under the alternative hypothesis.

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

    def func(proportion: float) -> float:
        return _power(proportion, null_proportion, size, alternative, alpha, method, continuity_correction) - power

    match direction:
        case "greater":
            return float(brentq(func, null_proportion, 1 - 1e-12))
        case "less":
            return float(brentq(func, 1e-12, null_proportion))


def solve_null_proportion(
    *,
    proportion: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"] = "z-phat",
    continuity_correction: bool = False,
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimate the required proportion under the null hypothesis for an equality test of one proportion.

    Args:
        proportion (float):
            Proportion under the alternative hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $p ≠ p_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $p > p_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $p < p_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.
        direction:
            The direction for the proportion under the null hypothesis relative to the proportion under the alternative hypothesis.

            - `'greater'`: Search for the null proportion greater than the alternative proportion.
            - `'less'`: Search for the null proportion less than the alternative proportion.

            !!! note
                - If `alternative` is `'two-sided'`, this parameter is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'less'`, and this parameter is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'greater'`, and this parameter is ignored.

    Returns:
        float: The required proportion under the null hypothesis.

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

    def func(null_proportion: float) -> float:
        return _power(proportion, null_proportion, size, alternative, alpha, method, continuity_correction) - power

    match direction:
        case "greater":
            return float(brentq(func, proportion, 1 - 1e-12))
        case "less":
            return float(brentq(func, 1e-12, proportion))
