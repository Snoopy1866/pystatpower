from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm

from ..._constant import SAMPLE_SIZE_SEARCH_MAX


def _power_p0(
    null_proportion: float,
    proportion: float,
    margin: float,
    size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a one-sample proportion superiority test, using $p_0$ to calculate variance."""

    proportion_sup = null_proportion + margin

    match alternative:
        case "greater":
            power = 1 - norm.cdf(
                (
                    norm.ppf(1 - alpha) * sqrt(proportion_sup * (1 - proportion_sup))
                    - (proportion - proportion_sup) * sqrt(size)
                )
                / sqrt(proportion * (1 - proportion))
            )
        case "less":
            power = 1 - norm.cdf(
                (
                    norm.ppf(1 - alpha) * sqrt(proportion_sup * (1 - proportion_sup))
                    + (proportion - proportion_sup) * sqrt(size)
                )
                / sqrt(proportion * (1 - proportion))
            )

    return float(power)


def _power_p0_cc(
    null_proportion: float,
    proportion: float,
    margin: float,
    size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a one-sample proportion superiority test with continuity correction, using $p_0$ to calculate variance."""

    proportion_sup = null_proportion + margin

    if abs(proportion - proportion_sup) < 1 / (2 * size):
        c = 0
    elif proportion > proportion_sup:
        c = -1 / (2 * size)
    else:  # proportion < proportion_noninf
        c = 1 / (2 * size)

    match alternative:
        case "greater":
            power = 1 - norm.cdf(
                (
                    norm.ppf(1 - alpha) * sqrt(proportion_sup * (1 - proportion_sup))
                    - (proportion - proportion_sup + c) * sqrt(size)
                )
                / sqrt(proportion * (1 - proportion))
            )
        case "less":
            power = 1 - norm.cdf(
                (
                    norm.ppf(1 - alpha) * sqrt(proportion_sup * (1 - proportion_sup))
                    + (proportion - proportion_sup + c) * sqrt(size)
                )
                / sqrt(proportion * (1 - proportion))
            )

    return float(power)


def _power_phat(
    null_proportion: float,
    proportion: float,
    margin: float,
    size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a one-sample proportion superiority test, using $\\hat{p}$ to calculate variance."""

    proportion_sup = null_proportion + margin

    match alternative:
        case "greater":
            power = 1 - norm.cdf(
                norm.ppf(1 - alpha) - (proportion - proportion_sup) * sqrt(size) / sqrt(proportion * (1 - proportion))
            )
        case "less":
            power = 1 - norm.cdf(
                norm.ppf(1 - alpha) + (proportion - proportion_sup) * sqrt(size) / sqrt(proportion * (1 - proportion))
            )

    return float(power)


def _power_phat_cc(
    null_proportion: float,
    proportion: float,
    margin: float,
    size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a one-sample proportion superiority test with continuity correction, using $\\hat{p}$ to calculate variance."""

    proportion_sup = null_proportion + margin

    if abs(proportion - proportion_sup) < 1 / (2 * size):
        c = 0
    elif proportion > proportion_sup:
        c = -1 / (2 * size)
    else:  # proportion < proportion_noninf
        c = 1 / (2 * size)

    match alternative:
        case "greater":
            power = 1 - norm.cdf(
                norm.ppf(1 - alpha)
                - (proportion - proportion_sup + c) * sqrt(size) / sqrt(proportion * (1 - proportion))
            )
        case "less":
            power = 1 - norm.cdf(
                norm.ppf(1 - alpha)
                + (proportion - proportion_sup + c) * sqrt(size) / sqrt(proportion * (1 - proportion))
            )

    return float(power)


def _power(
    null_proportion: float,
    proportion: float,
    margin: float,
    size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
    phat: bool,
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power for a one-sample proportion superiority test."""

    match (phat, continuity_correction):
        case (True, True):
            power = _power_phat_cc(null_proportion, proportion, margin, size, alternative, alpha)
        case (True, False):
            power = _power_phat(null_proportion, proportion, margin, size, alternative, alpha)
        case (False, True):
            power = _power_p0_cc(null_proportion, proportion, margin, size, alternative, alpha)
        case (False, False):
            power = _power_p0(null_proportion, proportion, margin, size, alternative, alpha)

    return power


def solve_power(
    *,
    null_proportion: float,
    proportion: float,
    margin: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    phat: bool = True,
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the statistical power for a one-sample proportion superiority test.

    Args:
        null_proportion (float):
            Proportion under the null hypothesis ($p_0$).
        proportion (float):
            Proportion under the alternative hypothesis ($p$).
        margin (float):
            superiority margin ($\\delta$).

            - If `alternative` is `lower`, a negative value must be specified.
            - If `alternative` is `upper`, a positive value must be specified.
        size (int):
            Sample size.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis:

            - `'greater'`: Upper one-tailed test ($p - p_0 > \\delta$), usually used when higher proportions are better.
            - `'less'`: Lower one-tailed test ($p - p_0 < \\delta$), usually used when higher proportions are worse.
        alpha (float, optional):
            One-sided significance level.
        phat (bool, optional):
            Specify whether to use the value of $p$ to calculate the standard deviation or not.
        continuity_correction (bool, optional):
            Specify whether to apply Yate's continuity correction or not.

    Returns:
        (float): The statistical power of the test.
    """

    return _power(null_proportion, proportion, margin, size, alternative, alpha, phat, continuity_correction)


def solve_size(
    *,
    null_proportion: float,
    proportion: float,
    margin: float,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    phat: bool = True,
    continuity_correction: bool = False,
) -> int:
    """
    Estimate the required sample size for a one-sample proportion superiority test.

    Args:
        null_proportion (float):
            Proportion under the null hypothesis ($p_0$).
        proportion (float):
            Proportion under the alternative hypothesis ($p$).
        margin (float):
            superiority margin ($\\delta$).

            - If `alternative` is `greater`, a positive value must be specified.
            - If `alternative` is `less`, a negative value must be specified.
        alternative (Literal["lower", "upper"], optional):
            Type of the alternative hypothesis:

            - `'greater'`: Upper one-tailed test ($p - p_0 > \\delta$), usually used when higher proportions are better.
            - `'less'`: Lower one-tailed test ($p - p_0 < \\delta$), usually used when higher proportions are worse.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Power of the test.
        phat (bool, optional):
            Specify whether to use the value of $p$ to calculate the standard deviation or not.
        continuity_correction (bool, optional):
            Specify whether to apply Yate's continuity correction or not.

    Returns:
        (int): The required sample size.
    """

    def func(size: float) -> float:
        return (
            _power(null_proportion, proportion, margin, size, alternative, alpha, phat, continuity_correction) - power
        )

    return ceil(brentq(func, 0.000001, SAMPLE_SIZE_SEARCH_MAX))


def solve_null_proportion(
    *,
    proportion: float,
    margin: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    phat: bool = True,
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required proportion under the null hypothesis ($p_0$) for a one-sample proportion superiority test.

    Args:
        proportion (float):
            Proportion under the alternative hypothesis ($p$).
        margin (float):
            superiority margin ($\\delta$).

            - If `alternative` is `greater`, a positive value must be specified.
            - If `alternative` is `less`, a negative value must be specified.
        size (int):
            Sample size.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis:

            - `'greater'`: Upper one-tailed test ($p - p_0 > \\delta$), usually used when higher proportions are better.
            - `'less'`: Lower one-tailed test ($p - p_0 < \\delta$), usually used when higher proportions are worse.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Power of the test.
        phat (bool, optional):
            Specify whether to use the value of $p$ to calculate the standard deviation or not.
        continuity_correction (bool, optional):
            Specify whether to apply Yate's continuity correction or not.

    Returns:
        (float): The required proportion under the null hypothesis ($p_0$).

    Notes:
        The search interval for the null proportion ($p_0$) is constrained by the alternative proportion ($p$) and the margin ($\\delta$) to ensure the alternative hypothesis remains plausible:

        $$
        \\text{Search Interval} =
        \\begin{cases}
        (\\operatorname{max}(p-\\delta, -\\delta), 1)  &, \\text{if lower one-tailed test} \\\\
        (0, \\operatorname{min}(p-\\delta, 1-\\delta)) &, \\text{if upper one-tailed test}
        \\end{cases}
        $$
    """

    def func(null_proportion: float) -> float:
        return (
            _power(null_proportion, proportion, margin, size, alternative, alpha, phat, continuity_correction) - power
        )

    match alternative:
        case "greater":
            null_proportion = brentq(func, 0.000001, min(proportion - margin, 1 - margin))
        case "less":
            null_proportion = brentq(func, max(proportion - margin, -margin), 0.999999)

    return float(null_proportion)


def solve_proportion(
    *,
    null_proportion: float,
    margin: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    phat: bool = True,
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required proportion under the alternative hypothesis ($p$) for a one-sample proportion superiority test.

    Args:
        null_proportion (float):
            Proportion under the null hypothesis ($p_0$).
        margin (float):
            superiority margin ($\\delta$).

            - If `alternative` is `greater`, a positive value must be specified.
            - If `alternative` is `less`, a negative value must be specified.
        size (int):
            Sample size.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis:

            - `'greater'`: Upper one-tailed test ($p - p_0 > \\delta$), usually used when higher proportions are better.
            - `'less'`: Lower one-tailed test ($p - p_0 < \\delta$), usually used when higher proportions are worse.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Power of the test.
        phat (bool, optional):
            Specify whether to use the value of $p$ to calculate the standard deviation or not.
        continuity_correction (bool, optional):
            Specify whether to apply Yate's continuity correction or not.

    Returns:
        (float): The required proportion under the alternative hypothesis ($p$).

    Notes:
        The search interval for the alternative proportion ($p$) is constrained by the null proportion ($p_0$) and the margin ($\\delta$) to ensure the alternative hypothesis remains plausible:

        $$
        \\text{Search Interval} =
        \\begin{cases}
        (0, p_0+\\delta) &, \\text{if lower one-tailed test} \\\\
        (p_0+\\delta, 1) &, \\text{if upper one-tailed test}
        \\end{cases}
        $$
    """

    def func(proportion: float) -> float:
        return (
            _power(null_proportion, proportion, margin, size, alternative, alpha, phat, continuity_correction) - power
        )

    match alternative:
        case "greater":
            proportion = brentq(func, null_proportion + margin, 0.999999)
        case "less":
            proportion = brentq(func, 0.000001, null_proportion + margin)

    return float(proportion)


def solve_margin(
    *,
    null_proportion: float,
    proportion: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    phat: bool = True,
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required margin ($\\delta$) for a one-sample proportion superiority test.

    Args:
        null_proportion (float):
            Proportion under the null hypothesis ($p_0$).
        proportion (float):
            Proportion under the alternative hypothesis ($p$).
        size (int):
            Sample size.
        alternative (Literal["greater", "less"]):
            Type of the alternative hypothesis:

            - `'greater'`: Upper one-tailed test ($p - p_0 > \\delta$), usually used when higher proportions are better.
            - `'less'`: Lower one-tailed test ($p - p_0 < \\delta$), usually used when higher proportions are worse.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Power of the test.
        phat (bool, optional):
            Specify whether to use the value of $p$ to calculate the standard deviation or not.
        continuity_correction (bool, optional):
            Specify whether to apply Yate's continuity correction or not.

    Returns:
        (float): The required margin ($\\delta$).

    Notes:
        The search interval for the margin ($\\delta$) is constrained by the null proportion ($p_0$) and the alternative proportion ($p$) to ensure the alternative hypothesis remains plausible:

        $$
        \\text{Search Interval} =
        \\begin{cases}
        (p-p_0, 0] &, \\text{if lower one-tailed test} \\\\
        [0, p-p_0) &, \\text{if upper one-tailed test}
        \\end{cases}
        $$
    """

    def func(margin: float) -> float:
        return (
            _power(null_proportion, proportion, margin, size, alternative, alpha, phat, continuity_correction) - power
        )

    f_zero = func(0)
    if abs(f_zero) <= 1e-7:
        margin = 0
    else:
        match alternative:
            case "greater":
                margin = brentq(func, 0, proportion - null_proportion)
            case "less":
                margin = brentq(func, proportion - null_proportion, 0)

    return float(margin)
