from math import ceil, copysign, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm

from ...._constant import SAMPLE_SIZE_SEARCH_MAX


def _power_pooled(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
) -> float:
    pooled_proportion = (treatment_size * treatment_proportion + reference_size * reference_proportion) / (
        treatment_size + reference_size
    )
    power = 1 - norm.cdf(
        (
            norm.ppf(1 - alpha)
            * sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))
            - abs(treatment_proportion - reference_proportion - margin)
        )
        / sqrt(
            treatment_proportion * (1 - treatment_proportion) / treatment_size
            + reference_proportion * (1 - reference_proportion) / reference_size
        )
    )
    return float(power)


def _power_pooled_cc(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
) -> float:
    pooled_proportion = (treatment_size * treatment_proportion + reference_size * reference_proportion) / (
        treatment_size + reference_size
    )
    power = 1 - norm.cdf(
        (
            norm.ppf(1 - alpha)
            * sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))
            - abs(treatment_proportion - reference_proportion - margin)
            + 1 / 2 * (1 / treatment_size + 1 / reference_size)
        )
        / sqrt(
            treatment_proportion * (1 - treatment_proportion) / treatment_size
            + reference_proportion * (1 - reference_proportion) / reference_size
        )
    )
    return float(power)


def _power_unpooled(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
) -> float:
    power = 1 - norm.cdf(
        norm.ppf(1 - alpha)
        - abs(treatment_proportion - reference_proportion - margin)
        / sqrt(
            treatment_proportion * (1 - treatment_proportion) / treatment_size
            + reference_proportion * (1 - reference_proportion) / reference_size
        )
    )
    return float(power)


def _power_unpooled_cc(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
) -> float:
    power = 1 - norm.cdf(
        norm.ppf(1 - alpha)
        - (
            abs(treatment_proportion - reference_proportion - margin)
            - 1 / 2 * (1 / treatment_size + 1 / reference_size)
        )
        / sqrt(
            treatment_proportion * (1 - treatment_proportion) / treatment_size
            + reference_proportion * (1 - reference_proportion) / reference_size
        )
    )
    return float(power)


def _power(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> float:
    if pooled:
        if continuity_correction:
            return _power_pooled_cc(
                treatment_proportion, reference_proportion, margin, treatment_size, reference_size, alpha
            )
        else:
            return _power_pooled(
                treatment_proportion, reference_proportion, margin, treatment_size, reference_size, alpha
            )
    else:
        if continuity_correction:
            return _power_unpooled_cc(
                treatment_proportion, reference_proportion, margin, treatment_size, reference_size, alpha
            )
        else:
            return _power_unpooled(
                treatment_proportion, reference_proportion, margin, treatment_size, reference_size, alpha
            )


def solve_power(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> float:
    """Calculate the power of the non-inferiority test between two independent proportions.

    Args:
        treatment_proportion (float): Treatment proportion.
        reference_proportion (float): Reference proportion.
        margin (float): Non-inferiority margin, which should be negative when higher is better, otherwise positive.
        treatment_size (float): Treatment sample size.
        reference_size (float): Reference sample size.
        alpha (float, optional): One-sided significance level. Default is 0.05.
        pooled (bool, optional): Whether or not the pooled method is used. Default is False.
        continuity_correction (bool, optional): Whether or not the continuity correction is used. Default is False.

    Returns:
        power(float): Power of the test.
    """

    power = _power(
        treatment_proportion,
        reference_proportion,
        margin,
        treatment_size,
        reference_size,
        alpha,
        pooled,
        continuity_correction,
    )
    return power


def solve_size(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    ratio: float = 1,
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> tuple[int, int]:
    """Estimate the sample size required for the non-inferiority test between two independent proportions.

    Args:
        treatment_proportion (float): Treatment proportion.
        reference_proportion (float): Reference proportion.
        margin (float): Non-inferiority margin, which should be negative when higher is better, otherwise positive.
        ratio (float, optional): Ratio of the sample size of the treatment group to the reference group. Default is 1.
        alpha (float, optional): One-sided significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.80.
        pooled (bool, optional): Whether or not the pooled method is used. Default is False.
        continuity_correction (bool, optional): Whether or not the continuity correction is used. Default is False.

    Returns:
        size(tuple[int, int]): The required sample size.
    """

    # If continuity correction is applied, in the case of small sample size, the power decreases with the increase of sample size, and then as the sample size continues to increase, the power gradually increases,
    # so there is a minimum value point in the power function, when using brentq to search, the minimum value point x0 must be found first, and then the search interval of brentq must be limited to (x0, 10^6) to ensure convergence.
    if continuity_correction:
        lower_bound = 1 / 2 * (1 / ratio + 1) / abs(treatment_proportion - reference_proportion - margin)
    else:
        lower_bound = 0.000001

    upper_bound = SAMPLE_SIZE_SEARCH_MAX

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _power(
                    treatment_proportion,
                    reference_proportion,
                    margin,
                    reference_size * ratio,
                    reference_size,
                    alpha,
                    pooled,
                    continuity_correction,
                )
                - power
            )

        reference_size = int(ceil(brentq(func, lower_bound, upper_bound)))
        treatment_size = int(ceil(reference_size * ratio))
        return treatment_size, reference_size
    else:

        def func(treatment_size: float) -> float:
            return (
                _power(
                    treatment_proportion,
                    reference_proportion,
                    margin,
                    treatment_size,
                    treatment_size * (1 / ratio),
                    alpha,
                    pooled,
                    continuity_correction,
                )
                - power
            )

        treatment_size = ceil(brentq(func, lower_bound, upper_bound))
        reference_size = ceil(treatment_size * (1 / ratio))
        return float(treatment_size), float(reference_size)


def solve_treatment_proportion(
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> float:
    """Estimate the treatment proportion required for the non-inferiority test between two independent proportions.

    Args:
        reference_proportion (float): Reference proportion.
        margin (float): Non-inferiority margin, which should be negative when higher is better, otherwise positive.
        treatment_size (float): Treatment sample size.
        reference_size (float): Reference sample size.
        alpha (float, optional): One-sided significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.80.
        pooled (bool, optional): Whether or not the pooled method is used. Default is False.
        continuity_correction (bool, optional): Whether or not the continuity correction is used. Default is False.

    Returns:
        treatment_proportion(float): The required treatment proportion.

    Notes:
        The range of the treatment proportion $(p_1)$ is determined by the reference proportion $(p_2)$ and non-inferiority margin $(\delta)$:

        $$
        \\begin{cases}
        \left(\max\left(p_2+\delta, \ 0\\right), 1\\right)   & , \\text{if } \delta < 0 \\\\
        \left(0, \ \min\left(p_2+\delta, \ 1\\right)\\right) & , \\text{if } \delta > 0
        \end{cases}
        $$
    """

    def func(treatment_proportion: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                margin,
                treatment_size,
                reference_size,
                alpha,
                pooled,
                continuity_correction,
            )
            - power
        )

    if margin < 0:
        lower_bound, upper_bound = max(reference_proportion + margin, 0), 1
        return float(brentq(func, lower_bound, upper_bound))
    else:
        lower_bound, upper_bound = 0, min(reference_proportion + margin, 1)
        return float(brentq(func, lower_bound, upper_bound))


def solve_reference_proportion(
    treatment_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> float:
    """Estimate the reference proportion required for the non-inferiority test between two independent proportions.

    Args:
        treatment_proportion (float): Treatment proportion.
        margin (float): Non-inferiority margin, which should be negative when higher is better, otherwise positive.
        treatment_size (float): Treatment sample size.
        reference_size (float): Reference sample size.
        alpha (float, optional): One-sided significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.80.
        pooled (bool, optional): Whether or not the pooled method is used. Default is False.
        continuity_correction (bool, optional): Whether or not the continuity correction is used. Default is False.

    Returns:
        reference_proportion(float): The required reference proportion.

    Notes:
        The range of the reference proportion $(p_2)$ is determined by the treatment proportion $(p_1)$ and non-inferiority margin $(\delta)$:

        $$
        \\begin{cases}
        (-\delta, \ p_1) \cup \left(\max\left(p_1, \ -\delta\\right), \min\left(p_1-\delta, \ 1\\right)\\right)     & , \\text{if } \delta < 0 \\\\
        (p_1, \ 1-\delta) \cup \left(\max\left(p_1-\delta, \ 0\\right), \ \min\left(p_1, \ 1-\delta\\right)\\right) & , \\text{if } \delta > 0
        \end{cases}
        $$
    """

    def func(reference_proportion: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                margin,
                treatment_size,
                reference_size,
                alpha,
                pooled,
                continuity_correction,
            )
            - power
        )

    if margin < 0:
        lower_bound, upper_bound = -margin, treatment_proportion
        if func(lower_bound) * func(upper_bound) < 0:
            return float(brentq(func, lower_bound, upper_bound))

        lower_bound, upper_bound = max(treatment_proportion, -margin), min(treatment_proportion - margin, 1)
        if func(lower_bound) * func(upper_bound) < 0:
            return float(brentq(func, lower_bound, upper_bound))
    else:
        lower_bound, upper_bound = treatment_proportion, 1 - margin
        if func(lower_bound) * func(upper_bound) < 0:
            return float(brentq(func, lower_bound, upper_bound))

        lower_bound, upper_bound = max(treatment_proportion - margin, 0), min(treatment_proportion, 1 - margin)
        if func(lower_bound) * func(upper_bound) < 0:
            return float(brentq(func, lower_bound, upper_bound))


def solve_margin(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
    margin_selection: Literal["positive", "negative"] = "negative",
) -> float:
    """Estimate the non-inferiority margin required for the non-inferiority test between two independent proportions.

    Args:
        treatment_proportion (float): Treatment proportion.
        reference_proportion (float): Reference proportion.
        treatment_size (float): Treatment sample size.
        reference_size (float): Reference sample size.
        alpha (float, optional): One-sided significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.80.
        pooled (bool, optional): Whether or not the pooled method is used. Default is False.
        continuity_correction (bool, optional): Whether or not the continuity correction is used. Default is False.
        margin_selection (Literal["positive", "negative"], optional): selection criterion when two margin solutions exist. Default is "negative".

            - If `positive`, the positive margin is returned.
            - If `negative`, the negative margin is returned.

            Note: If only one solution exists, this parameter is ignored.

    Returns:
        margin(float): The required non-inferiority margin.

    Notes:
        The non-inferiority margin should be negative when higher is better, otherwise positive.

        The range of the non-inferiority margin $(\delta)$ is determined by the treatment proportion $(p_1)$ and reference proportion $(p_2)$:

        If higher proportion is better:

        $$
        \delta \in
        \\begin{cases}
        (-p_2, \ 0)       & , \\text{if } p_1 \ge p_2 \\\\
        (-p_2, \ p_1-p_2) & , \\text{if } p_1 \lt p_2
        \end{cases}
        $$

        If higher proportion is worse:

        $$
        \delta \in
        \\begin{cases}
        (p_1-p_2, \ 1-p_2) & , \\text{if } p_1 \gt p_2 \\\\
        (0, \ 1-p_2)       & , \\text{if } p_1 \le p_2
        \end{cases}
        $$
    """

    def func(margin: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                margin,
                treatment_size,
                reference_size,
                alpha,
                pooled,
                continuity_correction,
            )
            - power
        )

    margins: list[float] = []
    if treatment_proportion > reference_proportion:
        lower_bound, upper_bound = -reference_proportion, 0
        if func(lower_bound) * func(upper_bound) < 0:
            margins.append(brentq(func, lower_bound, upper_bound))

        lower_bound, upper_bound = treatment_proportion - reference_proportion, 1 - reference_proportion
        if func(lower_bound) * func(upper_bound) < 0:
            margins.append(brentq(func, lower_bound, upper_bound))
    elif treatment_proportion < reference_proportion:
        lower_bound, upper_bound = -reference_proportion, treatment_proportion - reference_proportion
        if func(lower_bound) * func(upper_bound) < 0:
            margins.append(brentq(func, lower_bound, upper_bound))

        lower_bound, upper_bound = 0, 1 - reference_proportion
        if func(lower_bound) * func(upper_bound) < 0:
            margins.append(brentq(func, lower_bound, upper_bound))
    else:
        lower_bound, upper_bound = -reference_proportion, 0
        if func(lower_bound) * func(upper_bound) < 0:
            margins.append(brentq(func, lower_bound, upper_bound))

        lower_bound, upper_bound = 0, 1 - reference_proportion
        if func(lower_bound) * func(upper_bound) < 0:
            margins.append(brentq(func, lower_bound, upper_bound))

    if len(margins) == 2:
        match margin_selection.lower():
            case "negative":
                return margins[0] if margins[0] < 0 else margins[1]
            case "positive":
                return margins[0] if margins[0] > 0 else margins[1]
    else:
        return margins[0]
