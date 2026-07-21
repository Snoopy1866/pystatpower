from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power as _raw_power


def _power(
    proportion: float,
    null_proportion: float,
    margin_lower: float,
    margin_upper: float,
    size: float,
    alpha: float,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power."""

    return (
        _raw_power(proportion, null_proportion + margin_lower, size, "greater", alpha, method, continuity_correction)
        + _raw_power(proportion, null_proportion + margin_upper, size, "less", alpha, method, continuity_correction)
        - 1
    )


def solve_power(
    *,
    proportion: float,
    null_proportion: float,
    margin_lower: float,
    margin_upper: float,
    size: int,
    alpha: float = 0.025,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the statistical power.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        null_proportion:
            Proportion under the null hypothesis.
        margin_lower:
            The lower equivalence margin, must be a negative value.
        margin_upper:
            The upper equivalence margin, must be a positive value.
        size:
            Sample size.
        alpha:
            Significance level.

            The equivalence test is a two one-sided test, with a significance level of 0.025 being commonly used.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        The statistical power of the test.
    """

    return _power(proportion, null_proportion, margin_lower, margin_upper, size, alpha, method, continuity_correction)


def solve_size(
    *,
    proportion: float,
    null_proportion: float,
    margin_lower: float,
    margin_upper: float,
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool = False,
) -> int:
    """
    Estimate the required sample size.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        null_proportion:
            Proportion under the null hypothesis.
        margin_lower:
            The lower equivalence margin, must be a negative value.
        margin_upper:
            The upper equivalence margin, must be a positive value.
        alpha:
            Significance level.

            The equivalence test is a two one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        The required sample size.
    """

    def func(size: float) -> float:
        return (
            _power(proportion, null_proportion, margin_lower, margin_upper, size, alpha, method, continuity_correction)
            - power
        )

    return ceil(brentq(func, 1e-12, 1e12))
