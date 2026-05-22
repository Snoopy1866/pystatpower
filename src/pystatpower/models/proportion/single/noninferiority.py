from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm

from ...._constant import SAMPLE_SIZE_SEARCH_MAX


def _power_p0(
    null_proportion: float, proportion: float, size: float, alternative: Literal["one-sided", "two-sided"], alpha: float
) -> float:
    """Calculate the statistical power for a one-sample proportion test, using $p_0$ to calculate variance."""

    match alternative.lower():
        case "one-sided":
            power = 1 - norm.cdf(
                (
                    norm.ppf(1 - alpha) * sqrt(null_proportion * (1 - null_proportion))
                    - sqrt(size) * abs(proportion - null_proportion)
                )
                / sqrt(proportion * (1 - proportion))
            )
        case "two-sided":
            power = 2 - (
                norm.cdf(
                    (
                        norm.ppf(1 - alpha / 2) * sqrt(null_proportion * (1 - null_proportion))
                        - sqrt(size) * (proportion - null_proportion)
                    )
                    / sqrt(proportion * (1 - proportion))
                )
                + norm.cdf(
                    (
                        norm.ppf(1 - alpha / 2) * sqrt(null_proportion * (1 - null_proportion))
                        + sqrt(size) * (proportion - null_proportion)
                    )
                    / sqrt(proportion * (1 - proportion))
                )
            )
    return float(power)


def _power_p0_cc(
    null_proportion: float, proportion: float, size: float, alternative: Literal["one-sided", "two-sided"], alpha: float
) -> float:
    """Calculate the statistical power for a one-sample proportion test with continuity correction, using $p_0$ to calculate variance."""

    match alternative.lower():
        case "one-sided":
            power = 1 - norm.cdf(
                (
                    norm.ppf(1 - alpha) * sqrt(null_proportion * (1 - null_proportion))
                    - sqrt(size) * (abs(proportion - null_proportion) - 1 / (2 * size))
                )
                / sqrt(proportion * (1 - proportion))
            )
        case "two-sided":
            power = 2 - (
                norm.cdf(
                    (
                        norm.ppf(1 - alpha / 2) * sqrt(null_proportion * (1 - null_proportion))
                        - sqrt(size) * (proportion - null_proportion - 1 / (2 * size))
                    )
                    / sqrt(proportion * (1 - proportion))
                )
                + norm.cdf(
                    (
                        norm.ppf(1 - alpha / 2) * sqrt(null_proportion * (1 - null_proportion))
                        + sqrt(size) * (proportion - null_proportion + 1 / (2 * size))
                    )
                    / sqrt(proportion * (1 - proportion))
                )
            )
    return float(power)


def _power_phat(
    null_proportion: float, proportion: float, size: float, alternative: Literal["one-sided", "two-sided"], alpha: float
) -> float:
    """Calculate the statistical power for a one-sample proportion test, using $\\hat{p}_0$ to calculate variance."""

    match alternative:
        case "one-sided":
            power = 1 - norm.cdf(
                norm.ppf(1 - alpha)
                - sqrt(size) * abs(proportion - null_proportion) / sqrt(proportion * (1 - proportion))
            )
        case "two-sided":
            power = 2 - (
                norm.cdf(
                    norm.ppf(1 - alpha / 2)
                    - sqrt(size) * (proportion - null_proportion) / sqrt(proportion * (1 - proportion))
                )
                + norm.cdf(
                    norm.ppf(1 - alpha / 2)
                    + sqrt(size) * (proportion - null_proportion) / sqrt(proportion * (1 - proportion))
                )
            )

    return float(power)


def _power_phat_cc(
    null_proportion: float, proportion: float, size: float, alternative: Literal["one-sided", "two-sided"], alpha: float
) -> float:
    """Calculate the statistical power for a one-sample proportion test with continuity correction, using $\\hat{p}_0$ to calculate variance."""

    match alternative:
        case "one-sided":
            power = 1 - norm.cdf(
                norm.ppf(1 - alpha)
                - sqrt(size)
                * (abs(proportion - null_proportion) - 1 / (2 * size))
                / sqrt(proportion * (1 - proportion))
            )
        case "two-sided":
            power = 2 - (
                norm.cdf(
                    norm.ppf(1 - alpha / 2)
                    - sqrt(size) * (proportion - null_proportion - 1 / (2 * size)) / sqrt(proportion * (1 - proportion))
                )
                + norm.cdf(
                    norm.ppf(1 - alpha / 2)
                    + sqrt(size) * (proportion - null_proportion + 1 / (2 * size)) / sqrt(proportion * (1 - proportion))
                )
            )
    return float(power)


def _power(
    null_proportion: float,
    proportion: float,
    size: float,
    alternative: Literal["one-sided", "two-sided"],
    alpha: float,
    phat: bool,
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power for a one-sample proportion test."""

    match (phat, continuity_correction):
        case (True, True):
            power = _power_phat_cc(null_proportion, proportion, size, alternative, alpha)
        case (True, False):
            power = _power_phat(null_proportion, proportion, size, alternative, alpha)
        case (False, True):
            power = _power_p0_cc(null_proportion, proportion, size, alternative, alpha)
        case (False, False):
            power = _power_p0(null_proportion, proportion, size, alternative, alpha)
    return power


def solve_power(
    *,
    null_proportion: float,
    proportion: float,
    size: int,
    alternative: Literal["one-sided", "two-sided"] = "two-sided",
    alpha: float = 0.05,
    phat: bool = False,
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the statistical power for a one-sample proportion test.

    Args:
        null_proportion (float):
            The proportion specified under the null hypothesis ($p_0$).
            Must be in the interval (0, 1).
        proportion (float):
            The expected or observed proportion under the alternative hypothesis ($p_1$).
            Must be in the interval (0, 1).
        size (int):
            Total number of independent observations (sample size). Must be >= 1.
        alternative (Literal["one-sided", "two-sided"]):
            Type iof the alternative hypothesis:

            - `'two-sided'`: $H_1: p_1 \\neq p_0$
            - `'one-sided'`: $H_1: p_1 > p_0$ or $p_1 < p_0$
        alpha (float):
            Significance level.
        phat (bool, optional):
            Whether or not to use sample proportion to calculate standard deviation.
        continuity_correction (bool, optional):
            Whether or not to apply Yate's continuity correction.

    Returns:
        (float): The calculated power of the test.
    """

    return _power(null_proportion, proportion, size, alternative, alpha, phat, continuity_correction)


def solve_size(
    *,
    null_proportion: float,
    proportion: float,
    alternative: Literal["one-sided", "two-sided"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.80,
    phat: bool = False,
    continuity_correction: bool = False,
) -> int:
    """
    Estimate the required sample size for a one-sample proportion test.

    Args:
        null_proportion (float):
            The proportion specified under the null hypothesis ($p_0$).
            Must be in the interval (0, 1).
        proportion (float):
            The expected proportion under the alternative hypothesis ($p_1$).
            Must be in the interval (0, 1).
        alternative (Literal["one-sided", "two-sided"]):
            Type of the alternative hypothesis:

            - `'two-sided'`: $H_1: p \\neq p_0$
            - `'one-sided'`: $H_1: p > p_0$ or $p < p_0$
        alpha (float):
            Significance level.
        power (float):
            Desired statistical power (1 - Type II error rate).
        phat (bool, optional):
            Whether or not to use sample proportion to calculate standard deviation.
        continuity_correction (bool, optional):
            Whether or not to apply Yate's continuity correction.

    Returns:
        (int): The required sample size.
    """

    def func(size: float) -> float:
        return _power(null_proportion, proportion, size, alternative, alpha, phat, continuity_correction) - power

    return ceil(brentq(func, 0.000001, SAMPLE_SIZE_SEARCH_MAX))


def solve_null_proportion(
    *,
    proportion: float,
    size: int,
    alternative: Literal["one-sided", "two-sided"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.80,
    phat: bool = False,
    continuity_correction: bool = False,
    search_direction: Literal["below", "above"] = "below",
) -> float:
    """
    Estimate the required proportion under the null hypothesis ($p_0$) for a one-sample proportion test.

    Args:
        proportion (float):
            The expected proportion under the alternative hypothesis ($p_1$).
            Must be in the interval (0, 1).
        size (int):
            Total number of independent observations (sample size). Must be >= 1.
        alternative (Literal["one-sided", "two-sided"]):
            Type of the alternative hypothesis:

            - `'two-sided'`: $H_1: p \\neq p_0$
            - `'one-sided'`: $H_1: p > p_0$ or $p < p_0$
        alpha (float):
            Significance level.
        power (float):
            Desired statistical power (1 - Type II error rate).
        phat (bool, optional):
            Whether or not to use sample proportion to calculate standard deviation.
        continuity_correction (bool, optional):
            Whether or not to apply Yate's continuity correction.
        search_direction (Literal["below", "above"], optional):
            Selection strategy when two valid null proportions exist:

            - "below": Returns the solution where $p_0 < p_1$.
            - "above": Returns the solution where $p_0 > p_1$.

            If only one solution exists in (0, 1), this parameter is ignored.

    Returns:
        (float): The estimated null proportion ($p_0$).
    """

    def func(null_proportion: float) -> float:
        return _power(null_proportion, proportion, size, alternative, alpha, phat, continuity_correction) - power

    null_proportions: list[float] = []
    lower_bound, upper_bound = 0.000001, proportion
    if func(lower_bound) * func(upper_bound) < 0:
        null_proportions.append(brentq(func, lower_bound, upper_bound))

    lower_bound, upper_bound = proportion, 0.999999
    if func(lower_bound) * func(upper_bound) < 0:
        null_proportions.append(brentq(func, lower_bound, upper_bound))

    if len(null_proportions) == 2:
        match search_direction.lower():
            case "below":
                return null_proportions[0]
            case "above":
                return null_proportions[1]
    else:
        return null_proportions[0]


def solve_proportion(
    *,
    null_proportion: float,
    size: int,
    alternative: Literal["one-sided", "two-sided"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.80,
    phat: bool = False,
    continuity_correction: bool = False,
    search_direction: Literal["below", "above"] = "above",
) -> float:
    """
    Estimate the required proportion under the alternative hypothesis ($p_1$) for a one-sample proportion test.

    Args:
        null_proportion (float):
            The proportion specified under the null hypothesis ($p_0$).
            Must be in the interval (0, 1).
        size (int):
            Total number of independent observations (sample size). Must be >= 1.
        alternative (Literal["one-sided", "two-sided"]):
            Type of the alternative hypothesis:

            - `'two-sided'`: $H_1: p \\neq p_0$
            - `'one-sided'`: $H_1: p > p_0$ or $p < p_0$
        alpha (float):
            Significance level.
        power (float):
            Desired statistical power (1 - Type II error rate).
        phat (bool, optional):
            Whether or not to use sample proportion to calculate standard deviation.
        continuity_correction (bool, optional):
            Whether or not to apply Yate's continuity correction.
        search_direction (Literal["below", "above"], optional):
            Selection strategy when two valid alternative proportions exist:

            - "below": Returns the solution where $p_1 < p_0$.
            - "above": Returns the solution where $p_1 > p_0$.

            If only one solution exists in (0, 1), this parameter is ignored.

    Returns:
        (float): The estimated alternative proportion ($p_1$).
    """

    def func(proportion: float) -> float:
        return _power(null_proportion, proportion, size, alternative, alpha, phat, continuity_correction) - power

    proportions: list[float] = []
    lower_bound, upper_bound = 0.000001, null_proportion
    if func(lower_bound) * func(upper_bound) < 0:
        proportions.append(float(brentq(func, lower_bound, upper_bound)))

    lower_bound, upper_bound = null_proportion, 0.999999
    if func(lower_bound) * func(upper_bound) < 0:
        proportions.append(float(brentq(func, lower_bound, upper_bound)))

    if len(proportions) == 2:
        match search_direction.lower():
            case "below":
                return proportions[0]
            case "above":
                return proportions[1]
    else:
        return proportions[0]
