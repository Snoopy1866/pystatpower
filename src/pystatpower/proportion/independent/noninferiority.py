from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power


def _margin(margin: float, alternative: Literal["greater", "less"]) -> float:
    """Convert margin to regular form based on alternative hypothesis"""

    match alternative:
        case "greater":
            return -abs(margin)
        case "less":
            return abs(margin)


def solve_power(
    *,
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
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
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta > 0)$.
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        method:
            The method used to construct the test statistic.

            - `'z-pooled'`: Z-test using pooled variance.
            - `'z-unpooled'`: Z-test using unpooled variance.
        continuity_correction:
            Wether to apply Yates' continuity correction.

    Returns:
        The statistical power of the test.
    """

    margin = _margin(margin, alternative)

    return _power(
        treatment_proportion,
        reference_proportion,
        reference_proportion + margin,
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
    margin: float,
    alternative: Literal["greater", "less"],
    ratio: float = 1,
    alpha: float = 0.025,
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
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta > 0)$.
        ratio:
            Ratio of sample sizes in the treatment and reference groups.
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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

    margin = _margin(margin, alternative)

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _power(
                    treatment_proportion,
                    reference_proportion,
                    reference_proportion + margin,
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
                    reference_proportion + margin,
                    treatment_size,
                    treatment_size * (1 / ratio),
                    alternative,
                    alpha,
                    method,
                    continuity_correction,
                )
                - power
            )

        treatment_size = ceil(brentq(func, 1e-12, 1e12))
        reference_size = ceil(treatment_size * (1 / ratio))
        return treatment_size, reference_size


def solve_treatment_proportion(
    *,
    reference_proportion: float,
    margin: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-pooled", "z-unpooled"] = "z-unpooled",
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required proportion in the treatment group.

    Args:
        reference_proportion:
            Proportion in the reference group.
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta > 0)$.
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
        The required proportion in the treatment group.

    Notes:
        The value range of the treatment proportion $p_1$ is determined by the reference proportion $p_2$ and the non-inferiority margin $\\delta$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        p_1 > p_0 + \\delta \\\\
        0 < p_1 < 1 \\\\
        \\delta < 0
        \\end{cases}
        \\
        \\Rightarrow \\operatorname{max}(p_2 + \\delta, 0) < p_1 < 1
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        p_1 < p_2 + \\delta \\\\
        0 < p_1 < 1 \\\\
        \\delta > 0
        \\end{cases}
        \\
        \\Rightarrow 0 < p_1 < \\operatorname{min}(p_2 + \\delta, 1)
        $$
    """

    margin = _margin(margin, alternative)

    def func(treatment_proportion: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                reference_proportion + margin,
                treatment_size,
                reference_size,
                alternative,
                alpha,
                method,
                continuity_correction,
            )
            - power
        )

    match alternative:
        case "greater":
            return float(brentq(func, max(reference_proportion + margin, 0), 1))
        case "less":
            return float(brentq(func, 0, min(reference_proportion + margin, 1)))


def solve_reference_proportion(
    *,
    treatment_proportion: float,
    margin: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-pooled", "z-unpooled"] = "z-unpooled",
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required proportion in the reference group.

    Args:
        treatment_proportion:
            Proportion in the treatment group.
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta > 0)$.
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
        The required proportion in the reference group.

    Notes:
        The value range of the reference proportion $p_2$ is determined by the treatment proportion $p_1$ and the non-inferiority margin $\\delta$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        p_2 < p_1 - \\delta \\\\
        0 < p_2 < 1 \\\\
        \\delta < 0
        \\end{cases}
        \\
        \\Rightarrow 0 < p_2 < \\operatorname{min}(p_1 - \\delta, 1)
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        p_2 > p_1 - \\delta \\\\
        0 < p_2 < 1 \\\\
        \\delta > 0
        \\end{cases}
        \\
        \\Rightarrow \\operatorname{max}(p_1 - \\delta, 0) < p_2 < 1
        $$
    """

    margin = _margin(margin, alternative)

    def func(reference_proportion: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                reference_proportion + margin,
                treatment_size,
                reference_size,
                alternative,
                alpha,
                method,
                continuity_correction,
            )
            - power
        )

    match alternative:
        case "greater":
            return brentq(func, 0, min(treatment_proportion - margin, 1))
        case "less":
            return brentq(func, max(treatment_proportion - margin, 0), 1)


def solve_margin(
    *,
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-pooled", "z-unpooled"] = "z-unpooled",
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required non-inferiority margin.

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

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta > 0)$.
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
        The required non-inferiority margin.

    Notes:
        The value range of the non-inferiority margin $\\delta$ is determined by the treatment proportion $p_1$ and the reference proportion $p_2$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        \\delta < p_1 - p_2 \\\\
        \\delta < 0
        \\end{cases}
        \\
        \\Rightarrow -1 < \\delta < \\operatorname{min}(p_1 - p_2, 0)
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        \\delta > p_1 - p_2 \\\\
        \\delta > 0
        \\end{cases}
        \\
        \\Rightarrow \\operatorname{max}(p_1 - \\delta, 0) < \\delta < 1
        $$
    """

    def func(margin: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                reference_proportion + margin,
                treatment_size,
                reference_size,
                alternative,
                alpha,
                method,
                continuity_correction,
            )
            - power
        )

    match alternative:
        case "greater":
            return float(brentq(func, -1, min(treatment_proportion - reference_proportion, 0)))
        case "less":
            return float(brentq(func, max(treatment_proportion - reference_proportion, 0), 1))
