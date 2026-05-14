from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm

from ...._constant import SAMPLE_SIZE_SEARCH_MAX


def _power_p0(
    null_proportion: float, proportion: float, size: float, alternative: Literal["one-sided", "two-sided"], alpha: float
) -> float:
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
    Calculate the power for a one-sample proportion test.

    Args:
        null_proportion (float):
            The proportion specified under the null hypothesis (p0).
            Must be in the interval (0, 1).
        proportion (float):
            The expected or observed proportion under the alternative hypothesis (p1).
            Must be in the interval (0, 1).
        size (int):
            Total number of independent observations (sample size). Must be >= 1.
        alternative (Literal["one-sided", "two-sided"]):
            Direction of the test:

            - "two-sided": $H1: p1 \\neq p_0$
            - "one-sided": $H1: p1 > p_0$ or $p1 < p_0$

            Default is "two-sided".
        alpha (float):
            Significance level (Type I error rate). Defaults is 0.05.
        phat (bool, optional):
            Whether to use sample proportion to calculate standard deviation. Defaults is False.
        continuity_correction (bool, optional):
            Whether to apply continuity correction to the normal approximation. Defaults is False.

    Returns:
        power(float): The calculated power of the test, in the range [0, 1].
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
    Estimate the sample size required for a one-sample proportion test.

    Args:
        null_proportion (float):
            The proportion specified under the null hypothesis (p0).
            Must be in the interval (0, 1).
        proportion (float):
            The expected proportion under the alternative hypothesis (p1).
            Must be in the interval (0, 1).
        alternative (Literal["one-sided", "two-sided"]):
            Direction of the test:

            - "two-sided": $H1: p \\neq p_0$
            - "one-sided": $H1: p > p_0$ or $p < p_0$

            Default is "two-sided".
        alpha (float):
            Significance level (Type I error rate). Defaults is 0.05.
        power (float):
            Desired statistical power (1 - Type II error rate). Defaults is 0.80.
        phat (bool, optional):
            Whether to use sample proportion to calculate standard deviation. Defaults is False.
        continuity_correction (bool, optional):
            Whether to apply continuity correction to the normal approximation. Defaults is False.

    Returns:
        size(float): The minimum sample size (rounded up to the nearest integer) required to achieve the target power.
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
    proportion_selection: Literal["lower", "upper"] = "lower",
) -> float:
    """
    Estimate the null proportion (p0) required to achieve a target power for a one-sample proportion test.

    Args:
        proportion (float):
            The expected proportion under the alternative hypothesis (p1).
            Must be in the interval (0, 1).
        size (int):
            Total number of independent observations (sample size). Must be >= 1.
        alternative (Literal["one-sided", "two-sided"]):
            Direction of the test:

            - "two-sided": $H1: p \\neq p_0$
            - "one-sided": $H1: p > p_0$ or $p < p_0$

            Default is "two-sided".
        alpha (float):
            Significance level (Type I error rate). Defaults is 0.05.
        power (float):
            Desired statistical power (1 - Type II error rate). Defaults is 0.80.
        phat (bool, optional):
            Whether to use sample proportion to calculate standard deviation. Defaults is False.
        continuity_correction (bool, optional):
            Whether to apply continuity correction to the normal approximation. Defaults is False.
        proportion_selection (Literal["lower", "upper"], optional):
            Selection strategy when two valid null proportions exist:

            - "lower": Returns the solution where p0 < p1.
            - "upper": Returns the solution where p0 > p1.

            If only one solution exists in (0, 1), this parameter is ignored.
            Defaults is "lower".

    Returns:
        null_proportion(float): The estimated null proportion (p0).
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
        match proportion_selection.lower():
            case "lower":
                return null_proportions[0]
            case "upper":
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
    proportion_selection: Literal["lower", "upper"] = "upper",
):
    """
    Estimate the alternative proportion (p1) required to achieve a target power for a one-sample proportion test.

    Args:
        null_proportion (float):
            The proportion specified under the null hypothesis (p0).
            Must be in the interval (0, 1).
        size (int):
            Total number of independent observations (sample size). Must be >= 1.
        alternative (Literal["one-sided", "two-sided"]):
            Direction of the test:

            - "two-sided": $H1: p \\neq p_0$
            - "one-sided": $H1: p > p_0$ or $p < p_0$

            Default is "two-sided".
        alpha (float):
            Significance level (Type I error rate). Defaults is 0.05.
        power (float):
            Desired statistical power (1 - Type II error rate). Defaults is 0.80.
        phat (bool, optional):
            Whether to use sample proportion to calculate standard deviation. Defaults is False.
        continuity_correction (bool, optional):
            Whether to apply continuity correction to the normal approximation. Defaults is False.
        proportion_selection (Literal["lower", "upper"], optional):
            Selection strategy when two valid alternative proportions exist:

            - "lower": Returns the solution where p1 < p0.
            - "upper": Returns the solution where p1 > p0.

            If only one solution exists in (0, 1), this parameter is ignored.
            Defaults is "upper".

    Returns:
        proportion(float): The estimated alternative proportion (p1).
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
        match proportion_selection.lower():
            case "lower":
                return proportions[0]
            case "upper":
                return proportions[1]
    else:
        return proportions[0]
