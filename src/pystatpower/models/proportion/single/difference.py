from math import ceil, sqrt
from typing import Literal, cast

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
    null_proportion: float,
    proportion: float,
    size: int,
    alternative: Literal["one-sided", "two-sided"] = "two-sided",
    alpha: float = 0.05,
    phat: bool = False,
    continuity_correction: bool = False,
) -> float:
    """Calculate the power of the difference test between one proportion and a null proportion.

    Args:
        null_proportion (float): Proportion under the null hypothesis.
        proportion (float): Proportion under the alternative hypothesis.
        size (int): Sample size.
        alternative (Literal["one-sided", "two-sided"]): Specify whether the alternative hypothesis of the test is one-sided or two-sided. Default is "two-sided".
        alpha (float): Significance level. Defaults is 0.05.
        phat (bool, optional): Whether or not to use sample proportion to calculate standard deviation. Defaults is False.
        continuity_correction (bool, optional): Whether or not to use continuity correction. Defaults is False.

    Returns:
        power(float): Power of the test.
    """

    return _power(null_proportion, proportion, size, alternative, alpha, phat, continuity_correction)


def solve_size(
    null_proportion: float,
    proportion: float,
    alternative: Literal["one-sided", "two-sided"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.80,
    phat: bool = False,
    continuity_correction: bool = False,
) -> int:
    """Estimate the sample size required for the difference test between one proportion and a null proportion.

    Args:
        null_proportion (float): Proportion under the null hypothesis.
        proportion (float): Proportion under the alternative hypothesis.
        alternative (Literal["one-sided", "two-sided"]): Specify whether the alternative hypothesis of the test is one-sided or two-sided. Default is "two-sided".
        alpha (float): Significance level. Defaults is 0.05.
        power (float): Power of the test. Defaults is 0.80.
        phat (bool, optional): Whether or not to use sample proportion to calculate standard deviation. Defaults is False
        continuity_correction (bool, optional): Whether or not to use continuity correction. Defaults is False.

    Returns:
        size(float): The required sample size.
    """

    def func(size: float) -> float:
        return _power(null_proportion, proportion, size, alternative, alpha, phat, continuity_correction) - power

    return ceil(brentq(func, 0.000001, SAMPLE_SIZE_SEARCH_MAX))


def solve_null_proportion(
    proportion: float,
    size: int,
    alternative: Literal["one-sided", "two-sided"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.80,
    phat: bool = False,
    continuity_correction: bool = False,
    proportion_selection: Literal["lower", "upper"] = "lower",
) -> float:
    """Estimate the null proportion required for the difference test between one proportion and a null proportion.

    Args:
        proportion (float): Proportion under the alternative hypothesis.
        size (int): Sample size.
        alternative (Literal["one-sided", "two-sided"]): Specify whether the alternative hypothesis of the test is one-sided or two-sided. Default is "two-sided".
        alpha (float): Significance level. Defaults is 0.05.
        power (float): Power of the test. Defaults is 0.80.
        phat (bool, optional): Whether or not to use sample proportion to calculate standard deviation. Defaults is False.
        continuity_correction (bool, optional): Whether or not to use continuity correction. Defaults is False.
        proportion_selection (Literal["lower", "upper"], optional):
            If there are two solutions that meet the requirements, specify which solution to return. Defaults is "lower".

            - `lower`: Return the null proportion in interval (0, `proportion`).
            - `upper`: Return the null proportion in interval (`proportion`, 1).

            If there is only one solution in the interval (0, 1), this parameter is ignored.

    Returns:
        null_proportion(float): The required null proportion.
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
    null_proportion: float,
    size: int,
    alternative: Literal["one-sided", "two-sided"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.80,
    phat: bool = False,
    continuity_correction: bool = False,
    proportion_selection: Literal["lower", "upper"] = "upper",
):
    """Estimate the proportion required for the difference test between one proportion and a null proportion.

    Args:
        null_proportion (float): Proportion under the null hypothesis.
        size (int): Sample size.
        alternative (Literal["one-sided", "two-sided"]): Specify whether the alternative hypothesis of the test is one-sided or two-sided. Default is "two-sided".
        alpha (float): Significance level. Defaults is 0.05.
        power (float): Power of the test. Defaults is 0.80.
        phat (bool, optional): Whether or not to use sample proportion to calculate standard deviation. Defaults is False.
        continuity_correction (bool, optional): Whether or not to use continuity correction. Defaults is False.
        proportion_selection (Literal["lower", "upper"], optional):
            If there are two solutions that meet the requirements, specify which solution to return. Defaults is "upper".

            - `lower`: Return the proportion in interval (0, `null_proportion`).
            - `upper`: Return the proportion in interval (`null_proportion`, 1).

            If there is only one solution in the interval (0, 1), this parameter is ignored.

    Returns:
        proportion(float): The required proportion.
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
