from math import ceil, sqrt
from typing import Literal

from scipy.optimize import OptimizeResult, brentq, minimize_scalar
from scipy.stats import norm

from ..._constant import SAMPLE_SIZE_SEARCH_MAX


def _continuity_correction(proportion: float, proportion_margin: float, size: float) -> float:
    """Calculate the value of the correction term required for continuity correction"""

    if abs(proportion - proportion_margin) < 1 / (2 * size):
        c = 0
    elif proportion > proportion_margin:
        c = -1 / (2 * size)
    else:  # proportion < proportion_margin
        c = 1 / (2 * size)

    return c


def _power_p0(
    null_proportion: float,
    proportion: float,
    margin_lower: float,
    margin_upper: float,
    size: float,
    alpha: float,
) -> float:
    """Calculate the statistical power for a one-sample proportion equivalence test, using $p_0$ to calculate variance."""

    proportion_lower = null_proportion + margin_lower
    proportion_upper = null_proportion + margin_upper

    power = (
        1
        - norm.cdf(
            (
                norm.ppf(1 - alpha) * sqrt(proportion_lower * (1 - proportion_lower))
                - (proportion - proportion_lower) * sqrt(size)
            )
            / sqrt(proportion * (1 - proportion))
        )
        - norm.cdf(
            (
                norm.ppf(1 - alpha) * sqrt(proportion_upper * (1 - proportion_upper))
                + (proportion - proportion_upper) * sqrt(size)
            )
            / sqrt(proportion * (1 - proportion))
        )
    )

    return float(power)


def _power_p0_cc(
    null_proportion: float,
    proportion: float,
    margin_lower: float,
    margin_upper: float,
    size: float,
    alpha: float,
) -> float:
    """Calculate the statistical power for a one-sample proportion equivalence test with continuity correction, using $p_0$ to calculate variance."""

    proportion_lower = null_proportion + margin_lower
    proportion_upper = null_proportion + margin_upper

    c_lower = _continuity_correction(proportion, proportion_lower, size)
    c_upper = _continuity_correction(proportion, proportion_upper, size)

    power = (
        1
        - norm.cdf(
            (
                norm.ppf(1 - alpha) * sqrt(proportion_lower * (1 - proportion_lower))
                - (proportion - proportion_lower + c_lower) * sqrt(size)
            )
            / sqrt(proportion * (1 - proportion))
        )
        - norm.cdf(
            (
                norm.ppf(1 - alpha) * sqrt(proportion_upper * (1 - proportion_upper))
                + (proportion - proportion_upper + c_upper) * sqrt(size)
            )
            / sqrt(proportion * (1 - proportion))
        )
    )

    return float(power)


def _power_phat(
    null_proportion: float,
    proportion: float,
    margin_lower: float,
    margin_upper: float,
    size: float,
    alpha: float,
) -> float:
    """Calculate the statistical power for a one-sample proportion equivalence test, using $\\hat{p}$ to calculate variance."""

    proportion_lower = null_proportion + margin_lower
    proportion_upper = null_proportion + margin_upper

    power = (
        1
        - norm.cdf(
            norm.ppf(1 - alpha) - (proportion - proportion_lower) * sqrt(size) / sqrt(proportion * (1 - proportion))
        )
        - norm.cdf(
            norm.ppf(1 - alpha) + (proportion - proportion_upper) * sqrt(size) / sqrt(proportion * (1 - proportion))
        )
    )

    return float(power)


def _power_phat_cc(
    null_proportion: float,
    proportion: float,
    margin_lower: float,
    margin_upper: float,
    size: float,
    alpha: float,
) -> float:
    """Calculate the statistical power for a one-sample proportion equivalence test with continuity correction, using $\\hat{p}$ to calculate variance."""

    proportion_lower = null_proportion + margin_lower
    proportion_upper = null_proportion + margin_upper

    c_lower = _continuity_correction(proportion, proportion_lower, size)
    c_upper = _continuity_correction(proportion, proportion_upper, size)

    power = (
        1
        - norm.cdf(
            norm.ppf(1 - alpha)
            - (proportion - proportion_lower + c_lower) * sqrt(size) / sqrt(proportion * (1 - proportion))
        )
        - norm.cdf(
            norm.ppf(1 - alpha)
            + (proportion - proportion_upper + c_upper) * sqrt(size) / sqrt(proportion * (1 - proportion))
        )
    )

    return float(power)


def _power(
    null_proportion: float,
    proportion: float,
    margin_lower: float,
    margin_upper: float,
    size: float,
    alpha: float,
    phat: bool,
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power for a one-sample proportion equivalence test."""

    match (phat, continuity_correction):
        case (True, True):
            power = _power_phat_cc(null_proportion, proportion, margin_lower, margin_upper, size, alpha)
        case (True, False):
            power = _power_phat(null_proportion, proportion, margin_lower, margin_upper, size, alpha)
        case (False, True):
            power = _power_p0_cc(null_proportion, proportion, margin_lower, margin_upper, size, alpha)
        case (False, False):
            power = _power_p0(null_proportion, proportion, margin_lower, margin_upper, size, alpha)

    return power


def solve_power(
    *,
    null_proportion: float,
    proportion: float,
    margin_lower: float,
    margin_upper: float,
    size: int,
    alpha: float = 0.025,
    phat: bool = True,
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the statistical power for a one-sample proportion equivalence test.

    Args:
        null_proportion (float):
            Proportion under the null hypothesis ($p_0$).
        proportion (float):
            Proportion under the alternative hypothesis ($p$).
        margin_lower (float):
            Lower equivalence margin ($\\delta_1$), a negative value must be specified.
        margin_upper (float):
            Upper equivalence margin ($\\delta_2$), a positive value must be specified.
        size (int):
            Sample size.
        alpha (float, optional):
            One-sided significance level.
        phat (bool, optional):
            Whether to use the alternative proportion $p$ to calculate the standard deviation.
        continuity_correction (bool, optional):
            Whether to apply Yate's continuity correction.

    Returns:
        (float): The statistical power of the test.
    """

    return _power(null_proportion, proportion, margin_lower, margin_upper, size, alpha, phat, continuity_correction)


def solve_size(
    *,
    null_proportion: float,
    proportion: float,
    margin_lower: float,
    margin_upper: float,
    alpha: float = 0.025,
    power: float = 0.8,
    phat: bool = True,
    continuity_correction: bool = False,
) -> int:
    """
    Estimate the required sample size for a one-sample proportion equivalence test.

    Args:
        null_proportion (float):
            Proportion under the null hypothesis ($p_0$).
        proportion (float):
            Proportion under the alternative hypothesis ($p$).
        margin_lower (float):
            Lower equivalence margin ($\\delta_1$), a negative value must be specified.
        margin_upper (float):
            Upper equivalence margin ($\\delta_2$), a positive value must be specified.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Power of the test.
        phat (bool, optional):
            Whether to use the alternative proportion $p$ to calculate the standard deviation.
        continuity_correction (bool, optional):
            Whether to apply Yate's continuity correction.

    Returns:
        (int): The required sample size.
    """

    def func(size: float) -> float:
        return (
            _power(null_proportion, proportion, margin_lower, margin_upper, size, alpha, phat, continuity_correction)
            - power
        )

    return ceil(brentq(func, 0.000001, SAMPLE_SIZE_SEARCH_MAX))


def solve_null_proportion(
    *,
    proportion: float,
    margin_lower: float,
    margin_upper: float,
    size: int,
    alpha: float = 0.025,
    power: float = 0.8,
    phat: bool = True,
    continuity_correction: bool = False,
    search_direction: Literal["lower", "upper"] = "upper",
) -> float:
    """
    Estimate the required proportion under the null hypothesis ($p_0$) for a one-sample proportion equivalence test.

    Args:
        proportion (float):
            Proportion under the alternative hypothesis ($p$).
        margin_lower (float):
            Lower equivalence margin ($\\delta_1$), a negative value must be specified.
        margin_upper (float):
            Upper equivalence margin ($\\delta_2$), a positive value must be specified.
        size (int):
            Sample size.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Power of the test.
        phat (bool, optional):
            Whether to use the alternative proportion $p$ to calculate the standard deviation.
        continuity_correction (bool, optional):
            Whether to apply Yate's continuity correction.
        search_direction (Literal["lower", "upper"], optional):
            The direction to search for the null proportion relative to the maximum power point ($p_{\\text{argmax}}$), if two valid solutions exist.

            - `'lower'`: Search for $p_0$ in the interval below $p_{\\text{argmax}}$.
            - `'upper'`: Search for $p_0$ in the interval above $p_{\\text{argmax}}$.

            If $p$ itself satisfies the target power, this parameter is ignored and $p$ is returned directly.

    Returns:
        (float): The required proportion under the null hypothesis ($p_0$).

    Notes:
        The search interval for the null proportion ($p_0$) is constrained by the alternative proportion ($p$) and
        the equivalence margins ($\\delta_1$, $\\delta_2$) to ensure the alternative hypothesis remains plausible.

        When the target power intersects the power curve at two points, the search spaces are partitioned by the maximum power point ($p_{\\text{argmax}}$):

        - if `search_direction='lower'`: The interval is $(\\operatorname{max}(p-\\delta_2, -\\delta_1, 0), p_{\\text{argmax}})$
        - if `search_direction='upper'`: The interval is $(p_{\\text{argmax}}, \\operatorname{min}(p-\\delta_1, 1-\\delta_2, 1))$

        where $p_{\\text{argmax}}$ is the specific null proportion that maximizes the power function (or minimizes the negative power function).
    """

    def func(null_proportion: float) -> float:
        return (
            _power(null_proportion, proportion, margin_lower, margin_upper, size, alpha, phat, continuity_correction)
            - power
        )

    f_proportion = func(proportion)
    if abs(f_proportion) < 1e-7:
        null_proportion = proportion
    else:
        lower_bound = max(proportion - margin_upper, -margin_lower, 0.000001)
        upper_bound = min(proportion - margin_lower, 1 - margin_upper, 0.999999)

        if func(lower_bound) * func(upper_bound) < 0:
            null_proportion = brentq(func, lower_bound, upper_bound)
        else:
            # find the maximum value point of the power function
            res: OptimizeResult = minimize_scalar(
                lambda null_proportion: -func(null_proportion), bounds=(lower_bound, upper_bound)
            )
            if res.success:
                null_proportion_argmin = float(res.x)

            match search_direction:
                case "lower":
                    null_proportion = brentq(func, lower_bound, null_proportion_argmin)
                case "upper":
                    null_proportion = brentq(func, null_proportion_argmin, upper_bound)

    return float(null_proportion)


def solve_proportion(
    *,
    null_proportion: float,
    margin_lower: float,
    margin_upper: float,
    size: int,
    alpha: float = 0.025,
    power: float = 0.8,
    phat: bool = True,
    continuity_correction: bool = False,
    search_direction: Literal["lower", "upper"] = "upper",
) -> float:
    """
    Estimate the required proportion under the alternative hypothesis ($p$) for a one-sample proportion equivalence test.

    Args:
        null_proportion (float):
            Proportion under the null hypothesis ($p_0$).
        margin_lower (float):
            Lower equivalence margin ($\\delta_1$), a negative value must be specified.
        margin_upper (float):
            Upper equivalence margin ($\\delta_2$), a positive value must be specified.
        size (int):
            Sample size.
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Power of the test.
        phat (bool, optional):
            Whether to use the alternative proportion $p$ to calculate the standard deviation.
        continuity_correction (bool, optional):
            Whether to apply Yate's continuity correction.
        search_direction (Literal["lower", "upper"], optional):
            The direction to search for the proportion relative to the maximum power point ($p_{\\text{argmax}}$), if two valid solutions exist.

            - `lower`: Search for $p$ in the interval below $p_{\\text{argmax}}$.
            - `upper`: Search for $p$ in the interval above $p_{\\text{argmax}}$.

            If $p_0$ itself satisfies the target power, this parameter is ignored and $p_0$ is returned directly.

    Returns:
        (float): The required proportion under the alternative hypothesis ($p$).

    Notes:
        The search interval for the alternative proportion ($p$) is constrained by the null proportion ($p$) and
        the equivalence margins ($\\delta_1$, $\\delta_2$) to ensure the  alternative hypothesis remains plausible.

        When the target power intersects the power curve at two points, the search spaces are partitioned by the maximum power point ($p_{\\text{argmax}}$):

        - if `search_direction='lower'`: The interval is $(\\operatorname{max}(p_0+\\delta_1, 0), p_{\\text{argmax}})$
        - if `search_direction='upper'`: The interval is $(p_{\\text{argmax}}, \\operatorname{min}(p_0+\\delta_2, 1))$

        where $p_{\\text{argmax}}$ is the specific alternative proportion that maximizes the power function (or minimizes the negative power function).
    """

    def func(proportion: float) -> float:
        return (
            _power(null_proportion, proportion, margin_lower, margin_upper, size, alpha, phat, continuity_correction)
            - power
        )

    f_null_proportion = func(null_proportion)
    if abs(f_null_proportion) < 1e-7:
        proportion = null_proportion
    else:
        lower_bound = max(null_proportion + margin_lower, 0.000001)
        upper_bound = min(null_proportion + margin_upper, 0.999999)

        # find the maximum value point of the power function
        res: OptimizeResult = minimize_scalar(lambda proportion: -func(proportion), bounds=(lower_bound, upper_bound))
        if res.success:
            proportion_argmin = float(res.x)

        match search_direction:
            case "lower":
                proportion = brentq(func, lower_bound, proportion_argmin)
            case "upper":
                proportion = brentq(func, proportion_argmin, upper_bound)

    return float(proportion)
