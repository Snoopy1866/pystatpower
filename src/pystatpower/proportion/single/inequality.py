from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power as _raw_power


def _power(
    proportion: float,
    null_proportion: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool,
) -> float:
    """Wrapper that delegates to the shared `_raw_power` implementation."""

    return _raw_power(proportion, null_proportion, 0, size, alternative, alpha, method, continuity_correction)


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
    Calculate the statistical power for an inequality test of one proportion.

    Args:
        proportion:
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
    Estimate the required sample size for an inequality test of one proportion.

    Args:
        proportion:
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
    Estimate the required proportion under the alternative hypothesis for an inequality test of one proportion.

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
    Estimate the required proportion under the null hypothesis for an inequality test of one proportion.

    Args:
        proportion:
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
