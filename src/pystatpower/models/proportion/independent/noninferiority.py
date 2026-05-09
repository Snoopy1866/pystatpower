from math import ceil, sqrt
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
    """Calculate the power for a non-inferiority test of two independent proportions using pooled variance."""
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
    """Calculate the power for a non-inferiority test of two independent proportions using pooled variance and continuity correction."""
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
    """Calculate the power for a non-inferiority test of two independent proportions using unpooled variance."""
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
    """Calculate the power for a non-inferiority test of two independent proportions using unpooled variance and continuity correction."""
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
    """Calculate the power for a non-inferiority test of two independent proportions."""
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
    """
    Calculate the power for a non-inferiority test of two independent proportions.

    Args:
        treatment_proportion (float):
            Actual proportion in the treatment group ($p_1$). Must be between 0 and 1.
        reference_proportion (float):
            Actual proportion in the reference group ($p_2$). Must be between 0 and 1.
        margin (float):
            The non-inferiority margin ($\\delta$)

            - Use a **negative value** if a higher proportion is better
              (e.g., -0.10 for a -10% non-inferiority margin in cure rates)
            - Use a **negative value** if a lower proportion is better
              (e.g., 0.05 for a 5% non-inferiority margin in mortality rates)
        treatment_size (float):
            Sample size for the treatment group ($n_1$).
        reference_size (float):
            Sample size for the reference group ($n_2$).
        alpha (float, optional):
            One-sided significance level. Defaults to 0.05.
        pooled (bool, optional):
            If True, use the pooled variance estimator. Defaults to False.
        continuity_correction (bool, optional):
            If True, applies Yates' continuity correction. Defaults to False.

    Returns:
        float: Power of the test.
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
    """
    Estimate the sample size required for a non-inferiority test of two independent proportions.

    Args:
        treatment_proportion (float):
            Expected proportion in the treatment group ($p_1$). Must be between 0 and 1.
        reference_proportion (float):
            Expected proportion in the reference group ($p_2$). Must be between 0 and 1.
        margin (float):
            The non-inferiority margin ($\\delta$)

            - Use a **negative value** if a higher proportion is better
              (e.g., -0.10 for a -10% non-inferiority margin in cure rates)
            - Use a **negative value** if a lower proportion is better
              (e.g., 0.05 for a 5% non-inferiority margin in mortality rates)
        ratio (float, optional):
            Ratio of treatment sample size to reference sample size ($k = n_1 / n_2$). Defaults to 1.
        alpha (float, optional):
            One-sided significance level. Defaults to 0.05.
        power (float, optional):
            Desired statistical power. Defaults to 0.80.
        pooled (bool, optional):
            If True, use the pooled variance estimator. Defaults to False.
        continuity_correction (bool, optional):
            If True, applies Yates' continuity correction. Defaults to False.

    Returns:
        tuple[int, int]: The required sample sizes for the treatment and reference groups, respectively.

    Notes:
        If `continuity_correction` is enabled, the power function may not be monotonic at very small sample sizes.
        The function identifies a safe lower bound to ensure convergence of the root-finding algorithm (Brent's method).
    """

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
    """
    Estimate the proportion required in the treatment group for a non-inferiority test of two independent proportions.

    Args:
        reference_proportion (float):
            Expected proportion in the reference group ($p_2$). Must be between 0 and 1.
        margin (float):
            The non-inferiority margin ($\\delta$)

            - Use a **negative value** if a higher proportion is better
              (e.g., -0.10 for a -10% non-inferiority margin in cure rates)
            - Use a **negative value** if a lower proportion is better
              (e.g., 0.05 for a 5% non-inferiority margin in mortality rates)
        treatment_size (float):
            Sample size for the treatment group ($n_1$).
        reference_size (float):
            Sample size for the reference group ($n_2$).
        alpha (float, optional):
            One-sided significance level. Defaults to 0.05.
        power (float, optional):
            Desired statistical power. Defaults to 0.80.
        pooled (bool, optional):
            If True, use the pooled variance estimator. Defaults to False.
        continuity_correction (bool, optional):
            If True, applies Yates' continuity correction. Defaults to False.

    Returns:
        float: The required proportion in the treatment group.

    Notes:
        The search interval for treatment proportion ($p_1$) is constrained by the reference proportion ($p_2$) and the
        margin ($\\delta$) to ensure the alternative hypothesis remains plausible:

        $$
        \\text{Search Interval} =
        \\begin{cases}
        \\left(\\max\\left(p_2+\\delta, \\ 0\\right), 1\\right)    & , \\text{if } \\delta < 0 \\\\
        \\left(0, \\ \\min\\left(p_2+\\delta, \\ 1\\right)\\right) & , \\text{if } \\delta > 0
        \\end{cases}
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
    """
    Estimate the proportion required in the reference group for a non-inferiority test of two independent proportions.

    Args:
        treatment_proportion (float):
            Expected proportion in the treatment group ($p_1$). Must be between 0 and 1.
        margin (float):
            The non-inferiority margin ($\\delta$)

            - Use a **negative value** if a higher proportion is better
              (e.g., -0.10 for a -10% non-inferiority margin in cure rates)
            - Use a **negative value** if a lower proportion is better
              (e.g., 0.05 for a 5% non-inferiority margin in mortality rates)
        treatment_size (float):
            Sample size for the treatment group ($n_1$).
        reference_size (float):
            Sample size for the reference group ($n_2$).
        alpha (float, optional):
            One-sided significance level. Defaults to 0.05.
        power (float, optional):
            Desired statistical power. Defaults to 0.80.
        pooled (bool, optional):
            If True, use the pooled variance estimator. Defaults to False.
        continuity_correction (bool, optional):
            If True, applies Yates' continuity correction. Defaults to False.

    Returns:
        float: The required proportion in the reference group.

    Notes:
        The search interval for reference proportion ($p_2$) is constrained by the treatment proportion ($p_1$) and the
        margin ($\\delta$) to ensure the alternative hypothesis remains plausible:

        $$
        \\text{Search Interval} =
        \\begin{cases}
        (-\\delta, \\ p_1) \\cup \\left(\\max\\left(p_1, \\ -\\delta\\right), \\min\\left(p_1-\\delta, \\ 1\\right)\\right)      & , \\text{if } \\delta < 0 \\\\
        (p_1, \\ 1-\\delta) \\cup \\left(\\max\\left(p_1-\\delta, \\ 0\\right), \\ \\min\\left(p_1, \\ 1-\\delta\\right)\\right) & , \\text{if } \\delta > 0
        \\end{cases}
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
    """
    Estimate the non-inferiority margin required for a non-inferiority test of two independent proportions.

    Args:
        treatment_proportion (float):
            Expected proportion in the treatment group ($p_1$). Must be between 0 and 1.
        reference_proportion (float):
            Expected proportion in the reference group ($p_2$). Must be between 0 and 1.
        treatment_size (float):
            Sample size for the treatment group ($n_1$).
        reference_size (float):
            Sample size for the reference group ($n_2$).
        alpha (float, optional):
            One-sided significance level. Defaults to 0.05.
        power (float, optional):
            Desired statistical power. Defaults to 0.80.
        pooled (bool, optional):
            If True, use the pooled variance estimator. Defaults to False.
        continuity_correction (bool, optional):
            If True, applied continuity correction. Defaults to False.
        margin_selection (Literal["positive", "negative"], optional):
            Selection criterion when two mathematically valid solutions exist (one for "higher is better", one for "worse")

            - "positive": Returns the positive margin (typically for mortality).
            - "negative": Returns the negative margin (typically for cure rates).

            Defaults to "negative".

            Note: If only one solution exists, this parameter is ignored.

    Returns:
        float: The required non-inferiority margin.

    Notes:
        The non-inferiority margin should be negative when higher is better, otherwise positive.

        The search interval for non-inferiority margin ($\\delta$) is constrained by the treatment proportion ($p_1$) and the
        reference proportion ($p_2$) to ensure the alternative hypothesis remains plausible:

        If higher proportion is better:

        $$
        \\text{Search Interval} =
        \\begin{cases}
        (-p_2, \\ 0)       & , \\text{if } p_1 \\ge p_2 \\\\
        (-p_2, \\ p_1-p_2) & , \\text{if } p_1 \\lt p_2
        \\end{cases}
        $$

        If higher proportion is worse:

        $$
        \\text{Search Interval} =
        \\begin{cases}
        (p_1-p_2, \\ 1-p_2) & , \\text{if } p_1 \\gt p_2 \\\\
        (0, \\ 1-p_2)       & , \\text{if } p_1 \\le p_2
        \\end{cases}
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
