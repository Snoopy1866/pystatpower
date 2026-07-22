from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power as _raw_power


def _power(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "one-sided"],
    alpha: float,
    method: Literal["z-pooled", "z-unpooled"],
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power."""

    if alternative == "one-sided":
        alternative = "greater" if treatment_proportion > reference_proportion else "less"

    return _raw_power(
        treatment_proportion,
        reference_proportion,
        reference_proportion,
        treatment_size,
        reference_size,
        alternative,
        alpha,
        method,
        continuity_correction,
    )


def solve_power(
    *,
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "one-sided"],
    alpha: float = 0.05,
    method: Literal["z-pooled", "z-unpooled"] = "z-unpooled",
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the statistical power.

    Args:
        treatment_proportion:
            Proportion in the treatment group.
        reference_proportion:
            Proportion in the reference group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $p_1 ≠ p_2$
            - If `alternative` is `'one-sided'`, the alternative hypothesis is $p_1 > p_2$ or $p_1 < p_2$, depending on the value of `treatment_proportion` and `reference_proportion`.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'one-sided'`, `alpha` represents the one-sided significance level.
        method:
            The method used to construct the test statistic.

            - `'z-pooled'`: Z-test using pooled variance.
            - `'z-unpooled'`: Z-test using unpooled variance.
        continuity_correction:
            Wether to apply Yates' continuity correction.

    Returns:
        The statistical power of the test.
    """

    return _power(
        treatment_proportion,
        reference_proportion,
        treatment_size,
        reference_size,
        alternative,
        alpha,
        method,
        continuity_correction,
    )


def solve_size(
    *,
    treatment_proportion: float,
    reference_proportion: float,
    alternative: Literal["two-sided", "one-sided"],
    ratio: float = 1,
    alpha: float = 0.05,
    power: float = 0.8,
    method: Literal["z-pooled", "z-unpooled"] = "z-unpooled",
    continuity_correction: bool = False,
) -> tuple[int, int]:
    """
    Estimate the required sample size.

    Args:
        treatment_proportion:
            Proportion in the treatment group.
        reference_proportion:
            Proportion in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $p_1 ≠ p_2$
            - If `alternative` is `'one-sided'`, the alternative hypothesis is $p_1 > p_2$ or $p_1 < p_2$, depending on the value of `treatment_proportion` and `reference_proportion`.
        ratio:
            Ratio of sample sizes in the treatment and reference groups.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'one-sided'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-pooled'`: Z-test using pooled variance.
            - `'z-unpooled'`: Z-test using unpooled variance.
        continuity_correction:
            Wether to apply Yates' continuity correction.

    Returns:
        The required sample sizes in the treatment and reference groups, respectively.
    """

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
                    method,
                    continuity_correction,
                )
                - power
            )

        reference_size = ceil(brentq(func, 1e-12, 1e12))
        treatment_size = ceil(reference_size * ratio)
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
                    method,
                    continuity_correction,
                )
                - power
            )

        treatment_size = ceil(brentq(func, 1e-12, 1e12))
        reference_size = ceil(treatment_size / ratio)
        return treatment_size, reference_size


def solve_treatment_proportion(
    *,
    reference_proportion: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "one-sided"],
    alpha: float = 0.05,
    power: float = 0.8,
    method: Literal["z-pooled", "z-unpooled"] = "z-unpooled",
    continuity_correction: bool = False,
    direction: Literal["greater", "less"],
) -> float:
    """
    Estimate the required proportion in the treatment group.

    Args:
        reference_proportion:
            Proportion in the reference group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $p_1 ≠ p_2$
            - If `alternative` is `'one-sided'`, the alternative hypothesis is $p_1 > p_2$ or $p_1 < p_2$, depending on the value of `treatment_proportion` and `reference_proportion`.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'one-sided'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-pooled'`: Z-test using pooled variance.
            - `'z-unpooled'`: Z-test using unpooled variance.
        continuity_correction:
            Wether to apply Yates' continuity correction.
        direction:
            The direction for the treatment proportion relative to the reference proportion.

            - `'greater'`: Search for the treatment proportion greater than the reference proportion.
            - `'less'`: Search for the treatment proportion less than the reference proportion.

    Returns:
        The required proportion in the treatment group.
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
                method,
                continuity_correction,
            )
            - power
        )

    match direction:
        case "greater":
            return float(brentq(func, reference_proportion, 1 - 1e-12))
        case "less":
            return float(brentq(func, 1e-12, reference_proportion))


def solve_reference_proportion(
    *,
    treatment_proportion: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "one-sided"],
    alpha: float = 0.05,
    power: float = 0.8,
    method: Literal["z-pooled", "z-unpooled"] = "z-unpooled",
    continuity_correction: bool = False,
    direction: Literal["greater", "less"],
) -> float:
    """
    Estimate the required proportion in the reference group.

    Args:
        treatment_proportion:
            Proportion in the treatment group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $p_1 ≠ p_2$
            - If `alternative` is `'one-sided'`, the alternative hypothesis is $p_1 > p_2$ or $p_1 < p_2$, depending on the value of `treatment_proportion` and `reference_proportion`.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'one-sided'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-pooled'`: Z-test using pooled variance.
            - `'z-unpooled'`: Z-test using unpooled variance.
        continuity_correction:
            Wether to apply Yates' continuity correction.
        direction:
            The direction for the treatment proportion relative to the reference proportion.

            - `'greater'`: Search for the treatment proportion greater than the reference proportion.
            - `'less'`: Search for the treatment proportion less than the reference proportion.

    Returns:
        The required proportion in the reference group.
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
                method,
                continuity_correction,
            )
            - power
        )

    match direction:
        case "greater":
            return float(brentq(func, treatment_proportion, 1 - 1e-12))
        case "less":
            return float(brentq(func, 1e-12, treatment_proportion))
