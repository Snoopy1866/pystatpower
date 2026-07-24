# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Power analysis for the superiority test of two independent proportions.

This module provides functions to calculate or estimate the following parameters:

- statistical power
- sample size
- proportion for the treatment group
- proportion for the reference group
- superiority margin
"""

from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power


def _margin(margin: float, alternative: Literal["greater", "less"]) -> float:
    """Convert margin to regular form based on alternative hypothesis."""
    match alternative:
        case "greater":
            return abs(margin)
        case "less":
            return -abs(margin)


def solve_power(
    *,
    treatment_proportion: float,
    reference_proportion: float,
    margin: float | None = None,
    superiority_proportion: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    method: Literal["z-pooled", "z-unpooled"] = "z-unpooled",
    continuity_correction: bool = False,
) -> float:
    r"""Calculate the statistical power.

    Args:
        treatment_proportion:
            Proportion in the treatment group.
        reference_proportion:
            Proportion in the reference group.
        margin:
            The superiority margin.

            Required if `superiority_proportion` is omitted. If `superiority_proportion` is specified, this parameter is ignored.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `-abs(margin)`.
        superiority_proportion:
            The superiority proportion.

            Required if `margin` is omitted.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta < 0)$.
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        method:
            The method used to construct the test statistic.

            - `'z-pooled'`: Z-test using pooled variance.
            - `'z-unpooled'`: Z-test using unpooled variance.
        continuity_correction:
            Wether to apply Yates' continuity correction.

    Returns:
        The statistical power of the test.

    Raises:
        ValueError: If `margin` and `superiority_proportion` are both omitted.
    """
    if superiority_proportion is None:
        if margin is None:
            msg = "at least one of 'margin' or 'superiority_proportion' is required."
            raise ValueError(msg)

        margin = _margin(margin, alternative)
        superiority_proportion = reference_proportion + margin

    return _power(
        treatment_proportion,
        reference_proportion,
        superiority_proportion,
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
    margin: float | None = None,
    superiority_proportion: float | None = None,
    alternative: Literal["greater", "less"],
    ratio: float = 1,
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-pooled", "z-unpooled"] = "z-unpooled",
    continuity_correction: bool = False,
) -> tuple[int, int]:
    r"""Estimate the required sample size.

    Args:
        treatment_proportion:
            Proportion in the treatment group.
        reference_proportion:
            Proportion in the reference group.
        margin:
            The superiority margin.

            Required if `superiority_proportion` is omitted. If `superiority_proportion` is specified, this parameter is ignored.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `-abs(margin)`.
        superiority_proportion:
            The superiority proportion.

            Required if `margin` is omitted.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta < 0)$.
        ratio:
            Ratio of sample sizes in the treatment and reference groups.
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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

    Raises:
        ValueError: If `margin` and `superiority_proportion` are both omitted.
    """
    if superiority_proportion is None:
        if margin is None:
            msg = "at least one of 'margin' or 'superiority_proportion' is required."
            raise ValueError(msg)

        margin = _margin(margin, alternative)
        superiority_proportion = reference_proportion + margin

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _power(
                    treatment_proportion,
                    reference_proportion,
                    superiority_proportion,
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
                    superiority_proportion,
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
    margin: float | None = None,
    superiority_proportion: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-pooled", "z-unpooled"] = "z-unpooled",
    continuity_correction: bool = False,
) -> float:
    r"""Estimate the required proportion in the treatment group.

    Args:
        reference_proportion:
            Proportion in the reference group.
        margin:
            The superiority margin.

            Required if `superiority_proportion` is omitted. If `superiority_proportion` is specified, this parameter is ignored.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `-abs(margin)`.
        superiority_proportion:
            The superiority proportion.

            Required if `margin` is omitted.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta < 0)$.
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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

    Raises:
        ValueError: If `margin` and `superiority_proportion` are both omitted.

    Notes:
        The value range of the treatment proportion $p_1$ is determined by the reference proportion $p_2$ and the superiority margin $\\delta$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        p_1 > p_2 + \\delta \\\\
        0 < p_1 < 1 \\\\
        \\delta > 0
        \\end{cases}
        \\
        \\Rightarrow p_2 + \\delta < p_1 < 1
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        p_1 < p_2 + \\delta \\\\
        0 < p_1 < 1 \\\\
        \\delta < 0
        \\end{cases}
        \\
        \\Rightarrow 0 < p_1 < p_2 + \\delta
        $$
    """
    if superiority_proportion is None:
        if margin is None:
            msg = "at least one of 'margin' or 'superiority_proportion' is required."
            raise ValueError(msg)

        margin = _margin(margin, alternative)
        superiority_proportion = reference_proportion + margin

    def func(treatment_proportion: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                superiority_proportion,
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
            return float(brentq(func, reference_proportion + margin, 1))
        case "less":
            return float(brentq(func, 0, reference_proportion + margin))


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
    r"""Estimate the required proportion in the reference group.

    Args:
        treatment_proportion:
            Proportion in the treatment group.
        margin:
            The superiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `-abs(margin)`.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta < 0)$.
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
        The value range of the reference proportion $p_2$ is determined by the treatment proportion $p_1$ and the superiority margin $\\delta$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        p_2 < p_1 - \\delta \\\\
        0 < p_2 < 1 \\\\
        \\delta > 0
        \\end{cases}
        \\
        \\Rightarrow 0 < p_2 < p_1 - \\delta
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        p_2 > p_1 - \\delta \\\\
        0 < p_2 < 1 \\\\
        \\delta < 0
        \\end{cases}
        \\
        \\Rightarrow p_1 - \\delta < p_2 < 1
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
            return brentq(func, 0, treatment_proportion - margin)
        case "less":
            return brentq(func, treatment_proportion - margin, 1)


def solve_superiority_proportion(
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
    r"""Estimate the required superiority proportion.

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

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta < 0)$.
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
        The required superiority proportion.

    Notes:
        The value range of the superiority proportion $p_{\\text{sup}}$ is determined by the treatment proportion $p_1$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        p_{\\text{sup}} < p_1 \\\\
        0 < p_{\\text{sup}} < 1 \\\\
        \\delta > 0
        \\end{cases}
        \\
        \\Rightarrow 0 < p_{\\text{sup}} < p_1
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        p_{\\text{sup}} > p_1 \\\\
        0 < p_{\\text{sup}} < 1 \\\\
        \\delta < 0
        \\end{cases}
        \\
        \\Rightarrow p_1 < p_{\\text{sup}} < 1
        $$
    """

    def func(superiority_proportion: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                superiority_proportion,
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
            return brentq(func, 0, treatment_proportion)
        case "less":
            return brentq(func, treatment_proportion, 1)


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
    r"""Estimate the required superiority margin.

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

            - If `alternative` is `'greater'`, the alternative hypothesis is $p_1 - p_2 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p_1 - p_2 < \\delta \\ (\\delta < 0)$.
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
        The required superiority margin.

    Notes:
        The value range of the superiority margin $\\delta$ is determined by the treatment proportion $p_1$ and the reference proportion $p_2$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        \\delta < p_1 - p_2 \\\\
        \\delta > 0
        \\end{cases}
        \\
        \\Rightarrow 0 < \\delta < p_1 - p_2
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        \\delta > p_1 - p_2 \\\\
        \\delta < 0
        \\end{cases}
        \\
        \\Rightarrow p_1 - p_2 < \\delta < 0
        $$

        To handle cases where the superiority margin is zero, the program computes the margin indirectly.
        It first calls [solve_superiority_proportion][pystatpower.proportion.independent.superiority.solve_superiority_proportion]
        to determine the superiority proportion $p_{\\text{sup}}$, and then calculates the margin $\\delta$ using the following formula:

        $$
        \\delta = p_{\\text{sup}} - p_2
        $$
    """
    return (
        solve_superiority_proportion(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative=alternative,
            alpha=alpha,
            power=power,
            method=method,
            continuity_correction=continuity_correction,
        )
        - reference_proportion
    )
