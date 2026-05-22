from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm

from ...._constant import SAMPLE_SIZE_SEARCH_MAX


def _power_pooled(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["one-sided", "two-sided"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an inequality test of two independent proportions using pooled variance."""

    pooled_proportion = (treatment_size * treatment_proportion + reference_size * reference_proportion) / (
        treatment_size + reference_size
    )
    match alternative:
        case "one-sided":
            power = 1 - norm.cdf(
                (
                    norm.ppf(1 - alpha)
                    * sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))
                    - abs(treatment_proportion - reference_proportion)
                )
                / sqrt(
                    treatment_proportion * (1 - treatment_proportion) / treatment_size
                    + reference_proportion * (1 - reference_proportion) / reference_size
                )
            )
        case "two-sided":
            power = (
                1
                - norm.cdf(
                    (
                        norm.ppf(1 - alpha / 2)
                        * sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))
                        - (treatment_proportion - reference_proportion)
                    )
                    / sqrt(
                        treatment_proportion * (1 - treatment_proportion) / treatment_size
                        + reference_proportion * (1 - reference_proportion) / reference_size
                    )
                )
                + norm.cdf(
                    (
                        norm.ppf(alpha / 2)
                        * sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))
                        - (treatment_proportion - reference_proportion)
                    )
                    / sqrt(
                        treatment_proportion * (1 - treatment_proportion) / treatment_size
                        + reference_proportion * (1 - reference_proportion) / reference_size
                    )
                )
            )

    return float(power)


def _power_pooled_cc(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["one-sided", "two-sided"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an inequality test of two independent proportions using pooled variance and continuity correction."""

    pooled_proportion = (treatment_size * treatment_proportion + reference_size * reference_proportion) / (
        treatment_size + reference_size
    )
    match alternative:
        case "one-sided":
            power = 1 - norm.cdf(
                (
                    norm.ppf(1 - alpha)
                    * sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))
                    - abs(treatment_proportion - reference_proportion)
                    + 1 / 2 * (1 / treatment_size + 1 / reference_size)
                )
                / sqrt(
                    treatment_proportion * (1 - treatment_proportion) / treatment_size
                    + reference_proportion * (1 - reference_proportion) / reference_size
                )
            )
        case "two-sided":
            power = (
                1
                - norm.cdf(
                    (
                        norm.ppf(1 - alpha / 2)
                        * sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))
                        - (treatment_proportion - reference_proportion)
                        + 1 / 2 * (1 / treatment_size + 1 / reference_size)
                    )
                    / sqrt(
                        treatment_proportion * (1 - treatment_proportion) / treatment_size
                        + reference_proportion * (1 - reference_proportion) / reference_size
                    )
                )
                + norm.cdf(
                    (
                        norm.ppf(alpha / 2)
                        * sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))
                        - (treatment_proportion - reference_proportion)
                        - 1 / 2 * (1 / treatment_size + 1 / reference_size)
                    )
                    / sqrt(
                        treatment_proportion * (1 - treatment_proportion) / treatment_size
                        + reference_proportion * (1 - reference_proportion) / reference_size
                    )
                )
            )
    return float(power)


def _power_unpooled(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["one-sided", "two-sided"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an inequality test of two independent proportions using unpooled variance."""

    match alternative:
        case "one-sided":
            power = 1 - norm.cdf(
                norm.ppf(1 - alpha)
                - abs(treatment_proportion - reference_proportion)
                / sqrt(
                    treatment_proportion * (1 - treatment_proportion) / treatment_size
                    + reference_proportion * (1 - reference_proportion) / reference_size
                )
            )
        case "two-sided":
            power = (
                1
                - norm.cdf(
                    norm.ppf(1 - alpha / 2)
                    - (treatment_proportion - reference_proportion)
                    / sqrt(
                        treatment_proportion * (1 - treatment_proportion) / treatment_size
                        + reference_proportion * (1 - reference_proportion) / reference_size
                    )
                )
                + norm.cdf(
                    norm.ppf(alpha / 2)
                    - (treatment_proportion - reference_proportion)
                    / sqrt(
                        treatment_proportion * (1 - treatment_proportion) / treatment_size
                        + reference_proportion * (1 - reference_proportion) / reference_size
                    )
                )
            )

    return float(power)


def _power_unpooled_cc(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["one-sided", "two-sided"],
    alpha: float,
) -> float:
    """Calculate the statistical power for an inequality test of two independent proportions using unpooled variance and continuity correction."""

    match alternative:
        case "one-sided":
            power = 1 - norm.cdf(
                norm.ppf(1 - alpha)
                - (abs(treatment_proportion - reference_proportion) - 1 / 2 * (1 / treatment_size + 1 / reference_size))
                / sqrt(
                    treatment_proportion * (1 - treatment_proportion) / treatment_size
                    + reference_proportion * (1 - reference_proportion) / reference_size
                )
            )
        case "two-sided":
            power = (
                1
                - norm.cdf(
                    norm.ppf(1 - alpha / 2)
                    - (treatment_proportion - reference_proportion - 1 / 2 * (1 / treatment_size + 1 / reference_size))
                    / sqrt(
                        treatment_proportion * (1 - treatment_proportion) / treatment_size
                        + reference_proportion * (1 - reference_proportion) / reference_size
                    )
                )
                + norm.cdf(
                    norm.ppf(alpha / 2)
                    - (treatment_proportion - reference_proportion + 1 / 2 * (1 / treatment_size + 1 / reference_size))
                    / sqrt(
                        treatment_proportion * (1 - treatment_proportion) / treatment_size
                        + reference_proportion * (1 - reference_proportion) / reference_size
                    )
                )
            )
    return float(power)


def _power(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["one-sided", "two-sided"],
    alpha: float,
    pooled: bool,
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power for an inequality test of two independent proportions."""

    if pooled:
        if continuity_correction:
            return _power_pooled_cc(
                treatment_proportion, reference_proportion, treatment_size, reference_size, alternative, alpha
            )
        else:
            return _power_pooled(
                treatment_proportion, reference_proportion, treatment_size, reference_size, alternative, alpha
            )
    else:
        if continuity_correction:
            return _power_unpooled_cc(
                treatment_proportion, reference_proportion, treatment_size, reference_size, alternative, alpha
            )
        else:
            return _power_unpooled(
                treatment_proportion, reference_proportion, treatment_size, reference_size, alternative, alpha
            )


def solve_power(
    *,
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["one-sided", "two-sided"],
    alpha: float = 0.05,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the statistical power for an inequality test of two independent proportions.

    Args:
        treatment_proportion (float):
            Actual proportion in the treatment group ($p_1$). Must be between 0 and 1.
        reference_proportion (float):
            Actual proportion in the reference group ($p_2$). Must be between 0 and 1.
        alternative (Literal["one-sided", "two-sided"]):
            Type of the alternative hypothesis.

            - `'one-sided'`: Tests for a difference in one direction (uses $\\alpha$).
            - `'two-sided'`: Tests for any difference (uses $\\alpha/2$ per tail).
        treatment_size (int):
            Sample size for the treatment group ($n_1$).
        reference_size (int):
            Sample size for the reference group ($n_2$).
        alpha (float, optional):
            Significance level.
        pooled (bool, optional):
            If True, use the pooled variance estimator ($\\bar{p}$) under the null hypothesis.
        continuity_correction (bool, optional):
            If True, applies Yates' continuity correction.

    Returns:
        (float): Power of the test.
    """

    power = _power(
        treatment_proportion,
        reference_proportion,
        treatment_size,
        reference_size,
        alternative,
        alpha,
        pooled,
        continuity_correction,
    )
    return power


def solve_size(
    *,
    treatment_proportion: float,
    reference_proportion: float,
    alternative: Literal["one-sided", "two-sided"],
    ratio: float = 1,
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> tuple[int, int]:
    """
    Estimate the required sample size for an inequality test of two independent proportions.

    Args:
        treatment_proportion (float):
            Expected proportion in the treatment group ($p_1$). Must be between 0 and 1.
        reference_proportion (float):
            Expected proportion in the reference group ($p_2$). Must be between 0 and 1.
        alternative (Literal["one-sided", "two-sided"]):
            Type of the alternative hypothesis.

            - `'one-sided'`: Tests for a difference in one direction (uses $\\alpha$).
            - `'two-sided'`: Tests for any difference (uses $\\alpha/2$ per tail).
        ratio (float, optional):
            Ratio of treatment sample size to reference sample size ($k = n_1 / n_2$).
        alpha (float, optional):
            Significance level.
        power (float, optional):
            Desired statistical power.
        pooled (bool, optional):
            If True, use the pooled variance estimator ($\\bar{p}$) under the null hypothesis.
        continuity_correction (bool, optional):
            If True, applies Yates' continuity correction.

    Returns:
        (tuple[int, int]): The required sample sizes for the treatment and reference groups, respectively.
    """

    lower_bound = 0.000001
    upper_bound = SAMPLE_SIZE_SEARCH_MAX

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _power(
                    treatment_proportion,
                    reference_proportion,
                    reference_size * ratio,
                    reference_size,
                    alternative,
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
                    treatment_size,
                    treatment_size / ratio,
                    alternative,
                    alpha,
                    pooled,
                    continuity_correction,
                )
                - power
            )

        treatment_size = ceil(brentq(func, lower_bound, upper_bound))
        reference_size = ceil(treatment_size / ratio)
        return float(treatment_size), float(reference_size)


def solve_treatment_proportion(
    *,
    reference_proportion: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["one-sided", "two-sided"],
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
    search_direction: Literal["lower", "upper"] = "upper",
) -> float:
    """
    Estimate the required proportion in the treatment group for an inequality test of two independent proportions.

    Args:
        reference_proportion (float):
            Expected proportion in the reference group ($p_2$). Must be between 0 and 1.
        treatment_size (int):
            Sample size for the treatment group ($n_1$).
        reference_size (int):
            Sample size for the reference group ($n_2$).
        alternative (Literal["one-sided", "two-sided"]):
            Type of the alternative hypothesis.

            - `'one-sided'`: Tests for a difference in one direction (uses $\\alpha$).
            - `'two-sided'`: Tests for any difference (uses $\\alpha/2$ per tail).
        alpha (float, optional):
            Significance level.
        power (float, optional):
            Desired statistical power.
        pooled (bool, optional):
            If True, use the pooled variance estimator ($\\bar{p}$) under the null hypothesis.
        continuity_correction (bool, optional):
            If True, applies Yates' continuity correction.
        search_direction:
            Which solution to search for relative to $p_2$.

            - "lower": Finds $p_1$ where $p_1 < p_2$.
            - "upper": Finds $p_1$ where $p_1 > p_2$.

    Returns:
        (float): The required proportion in the treatment group.
    """

    def func(treatment_proportion: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                treatment_size,
                reference_size,
                alternative,
                alpha,
                pooled,
                continuity_correction,
            )
            - power
        )

    match search_direction.lower():
        case "lower":
            return float(brentq(func, 0.000001, reference_proportion))
        case "upper":
            return float(brentq(func, reference_proportion, 0.999999))


def solve_reference_proportion(
    *,
    treatment_proportion: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["one-sided", "two-sided"],
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
    search_direction: Literal["lower", "upper"] = "lower",
) -> float:
    """
    Estimate the required proportion in the reference group for an inequality test of two independent proportions.

    Args:
        treatment_proportion (float):
            Expected proportion in the treatment group ($p_1$). Must be between 0 and 1.
        treatment_size (int):
            Sample size for the treatment group ($n_1$).
        reference_size (int):
            Sample size for the reference group ($n_2$).
        alternative (Literal["one-sided", "two-sided"]):
            Type of the alternative hypothesis.

            - `'one-sided'`: Tests for a difference in one direction (uses $\\alpha$).
            - `'two-sided'`: Tests for any difference (uses $\\alpha/2$ per tail).
        alpha (float, optional):
            If True, use the pooled variance estimator ($\\bar{p}$) under the null hypothesis.
        power (float, optional):
            Desired statistical power.
        pooled (bool, optional):
            If True, use the pooled variance estimator.
        continuity_correction (bool, optional):
            If True, applies Yates' continuity correction.
        search_direction:
            Which solution to search for relative to $p_1$.

            - "lower": Finds $p_2$ where $p_2 < p_1$.
            - "upper": Finds $p_2$ where $p_2 > p_1$.

    Returns:
        (float): The required proportion in the reference group.
    """

    def func(reference_proportion: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                treatment_size,
                reference_size,
                alternative,
                alpha,
                pooled,
                continuity_correction,
            )
            - power
        )

    match search_direction.lower():
        case "lower":
            return float(brentq(func, 0.000001, treatment_proportion))
        case "upper":
            return float(brentq(func, treatment_proportion, 0.999999))
