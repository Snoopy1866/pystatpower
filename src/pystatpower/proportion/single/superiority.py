from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power


def _margin(margin: float, alternative: Literal["greater", "less"]) -> float:
    """Convert margin to standard form based on alternative hypothesis"""

    match alternative:
        case "greater":
            return abs(margin)
        case "less":
            return -abs(margin)


def _verify_and_get_sup_proportion(
    null_proportion: float | None, margin: float | None, superiority_proportion: float | None
) -> float:
    """Verify provided proportions and return the superiority proportion"""

    if superiority_proportion is None:
        if null_proportion is None or margin is None:
            raise ValueError(
                "When 'superiority_proportion' is omitted, both 'null_proportion' and 'margin' are required."
            )
        superiority_proportion = null_proportion + margin

    return superiority_proportion


def solve_power(
    *,
    proportion: float,
    null_proportion: float | None = None,
    margin: float | None = None,
    superiority_proportion: float | None = None,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the statistical power.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        null_proportion:
            Proportion under the null hypothesis.

            Ignored if `superiority_proportion` is specified; otherwise, required alongside `margin`.
        margin:
            The superiority margin.

            Ignored if `superiority_proportion` is specified; otherwise, required alongside `null_proportion`.

            Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `alternative` is `'greater'`, the actual margin used internally is `abs(margin)`.
            - If `alternative` is `'less'`, the actual margin used internally is `-abs(margin)`.
        superiority_proportion:
            The superiority proportion.

            Required if either `null_proportion` or `margin` is omitted.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, and 0.025 is a commonly used significance level.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        float: The statistical power of the test.

    Raises:
        ValueError: If `superiority_proportion` is omitted, and either `null_proportion` or `margin` is missing.
    """

    margin = _margin(margin, alternative)
    superiority_proportion = _verify_and_get_sup_proportion(null_proportion, margin, superiority_proportion)

    return _power(proportion, superiority_proportion, size, alternative, alpha, method, continuity_correction)


def solve_size(
    *,
    proportion: float,
    null_proportion: float | None = None,
    margin: float | None = None,
    superiority_proportion: float | None = None,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool = False,
) -> int:
    """
    Estimate the required sample size.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        null_proportion:
            Proportion under the null hypothesis.

            Ignored if `superiority_proportion` is specified; otherwise, required alongside `margin`.
        margin:
            The superiority margin.

            Ignored if `superiority_proportion` is specified; otherwise, required alongside `null_proportion`.

            Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `alternative` is `'greater'`, the actual margin used internally is `abs(margin)`.
            - If `alternative` is `'less'`, the actual margin used internally is `-abs(margin)`.
        superiority_proportion:
            The superiority proportion.

            Required if either `null_proportion` or `margin` is omitted.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        int: The required sample size.

    Raises:
        ValueError: If `superiority_proportion` is omitted, and either `null_proportion` or `margin` is missing.
    """

    margin = _margin(margin, alternative)
    superiority_proportion = _verify_and_get_sup_proportion(null_proportion, margin, superiority_proportion)

    def func(size: float) -> float:
        return (
            _power(proportion, superiority_proportion, size, alternative, alpha, method, continuity_correction) - power
        )

    return ceil(brentq(func, 1e-12, 1e12))


def solve_proportion(
    *,
    null_proportion: float | None = None,
    margin: float | None = None,
    superiority_proportion: float | None = None,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required proportion under the alternative hypothesis.

    Args:
        null_proportion:
            Proportion under the null hypothesis.

            Ignored if `superiority_proportion` is specified; otherwise, required alongside `margin`.
        margin:
            The superiority margin.

            Ignored if `superiority_proportion` is specified; otherwise, required alongside `null_proportion`.

            Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `alternative` is `'greater'`, the actual margin used internally is `abs(margin)`.
            - If `alternative` is `'less'`, the actual margin used internally is `-abs(margin)`.
        superiority_proportion:
            The superiority proportion.

            Required if either `null_proportion` or `margin` is omitted.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        float: The required proportion under the alternative hypothesis.

    Raises:
        ValueError: If `superiority_proportion` is omitted, and either `null_proportion` or `margin` is missing.

    Notes:
        The value range of the alternative hypothesis proportion $p$ is determined by the null hypothesis proportion $p_0$ and the non-inferiority margin $\\delta$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        p > p_0 + \\delta \\\\
        0 < p < 1 \\\\
        \\delta > 0
        \\end{cases}
        \\
        \\Rightarrow p_0 + \\delta < p < 1
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        p < p_0 + \\delta \\\\
        0 < p < 1 \\\\
        \\delta < 0
        \\end{cases}
        \\
        \\Rightarrow 0 < p < p_0 + \\delta
        $$
    """

    margin = _margin(margin, alternative)
    superiority_proportion = _verify_and_get_sup_proportion(null_proportion, margin, superiority_proportion)

    def func(proportion: float) -> float:
        return (
            _power(proportion, superiority_proportion, size, alternative, alpha, method, continuity_correction) - power
        )

    eps = 1e-12
    match alternative:
        case "greater":
            return float(brentq(func, superiority_proportion + eps, 1 - eps))
        case "less":
            return float(brentq(func, eps, superiority_proportion - eps))


def solve_null_proportion(
    *,
    proportion: float,
    margin: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required proportion under the null hypothesis.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        margin:
            The superiority margin.

            Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `alternative` is `'greater'`, the actual margin used internally is `abs(margin)`.
            - If `alternative` is `'less'`, the actual margin used internally is `-abs(margin)`.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        float: The required proportion under the null hypothesis.

    Notes:
        The value range of the null hypothesis proportion $p_0$ is determined by the alternative hypothesis proportion $p$ and the non-inferiority margin $\\delta$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        p_0 < p - \\delta \\\\
        0 < p_0 < 1 \\\\
        0 < p_0 + \\delta < 1 \\\\
        \\delta > 0
        \\end{cases}
        \\
        \\Rightarrow 0 < p_0 < \\operatorname{min}(p - \\delta, 1 - \\delta)
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        p_0 > p - \\delta \\\\
        0 < p_0 < 1 \\\\
        0 < p_0 + \\delta < 1 \\\\
        \\delta < 0
        \\end{cases}
        \\
        \\Rightarrow \\operatorname{max}(p - \\delta, -\\delta) < p_0 < 1
        $$
    """

    margin = _margin(margin, alternative)

    def func(null_proportion: float) -> float:
        return (
            _power(proportion, null_proportion + margin, size, alternative, alpha, method, continuity_correction)
            - power
        )

    eps = 1e-12
    match alternative:
        case "greater":
            return float(brentq(func, eps, min(proportion - margin, 1 - margin) - eps))
        case "less":
            return float(brentq(func, max(proportion - margin, -margin) + eps, 1 - eps))


def solve_superiority_proportion(
    *,
    proportion: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required superiority proportion.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        float: The required superiority proportion.

    Notes:
        The value range of the superiority hypothesis proportion $p_{\\text{sup}}$ is determined by the alternative hypothesis proportion $p$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        p_{\\text{sup}} < p \\\\
        0 < p_{\\text{sup}} < 1 \\\\
        \\end{cases}
        \\
        \\Rightarrow 0 < p_{\\text{sup}} < p
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        p_{\\text{sup}} > p \\\\
        0 < p_{\\text{sup}} < 1 \\\\
        \\end{cases}
        \\
        \\Rightarrow p < p_{\\text{sup}} < 1
        $$
    """

    def func(superiority_proportion: float) -> float:
        return (
            _power(proportion, superiority_proportion, size, alternative, alpha, method, continuity_correction) - power
        )

    eps = 1e-12
    match alternative:
        case "greater":
            return float(brentq(func, eps, proportion - eps))
        case "less":
            return float(brentq(func, proportion + eps, 1 - eps))


def solve_margin(
    *,
    proportion: float,
    null_proportion: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required superiority margin.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        null_proportion:
            Proportion under the null hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        float: The required superiority margin.

    Notes:
        The value range of the null hypothesis proportion $p_0$ is determined by the alternative hypothesis proportion $p$ and the non-inferiority margin $\\delta$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        \\delta < p - p_0 \\\\
        0 < p_0 + \\delta < 1 \\\\
        \\delta > 0
        \\end{cases}
        \\
        \\Rightarrow 0 < \\delta < p - p_0
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        \\delta > p - p_0 \\\\
        0 < p_0 + \\delta < 1 \\\\
        \\delta < 0
        \\end{cases}
        \\
        \\Rightarrow p - p_0 < \\delta < 0
        $$

        To handle cases where the superiority margin is zero, the program computes the margin indirectly.
        It first calls [solve_superiority_proportion][pystatpower.proportion.single.superiority.solve_superiority_proportion]
        to determine the superiority proportion $p_{\\text{sup}}$, and then calculates the margin $\\delta$ using the following formula:

        $$
        \\delta = p_{\\text{sup}} - p_0
        $$
    """

    return (
        solve_superiority_proportion(
            proportion=proportion,
            size=size,
            alternative=alternative,
            alpha=alpha,
            power=power,
            method=method,
            continuity_correction=continuity_correction,
        )
        - null_proportion
    )
