from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power


def _margin(margin: float, alternative: Literal["greater", "less"]) -> float:
    """Convert margin to standard form based on alternative hypothesis"""

    match alternative:
        case "greater":
            return -abs(margin)
        case "less":
            return abs(margin)


def _verify_and_get_noninf_proportion(
    null_proportion: float | None, margin: float | None, noninferiority_proportion: float | None
) -> float:
    """Verify provided proportions and return the non-inferiority proportion"""

    if noninferiority_proportion is None:
        if null_proportion is None or margin is None:
            raise ValueError(
                "When 'noninferiority_proportion' is omitted, both 'null_proportion' and 'margin' are required."
            )
        noninferiority_proportion = null_proportion + margin

    return noninferiority_proportion


def solve_power(
    *,
    proportion: float,
    null_proportion: float | None = None,
    margin: float | None = None,
    noninferiority_proportion: float | None = None,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    method: Literal["z-p0", "z-phat"] = "z-phat",
    continuity_correction: bool,
) -> float:
    """
    Calculate the statistical power.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        null_proportion:
            Proportion under the null hypothesis.

            Ignored if `noninferiority_proportion` is specified; otherwise, required along with `margin`.
        margin:
            The non-inferiority margin.

            Ignored if `noninferiority_proportion` is specified; otherwise, required along with `null_proportion`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        noninferiority_proportion:
            The non-inferiority proportion.

            Required if either `null_proportion` or `margin` is omitted.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        The statistical power of the test.

    Raises:
        ValueError: If `noninferiority_proportion` is omitted, and either `null_proportion` or `margin` is missing.
    """

    margin = _margin(margin, alternative)
    noninferiority_proportion = _verify_and_get_noninf_proportion(null_proportion, margin, noninferiority_proportion)

    return _power(proportion, noninferiority_proportion, size, alternative, alpha, method, continuity_correction)


def solve_size(
    *,
    proportion: float,
    null_proportion: float | None = None,
    margin: float | None = None,
    noninferiority_proportion: float | None = None,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"] = "z-phat",
    continuity_correction: bool = False,
) -> int:
    """
    Estimate the required sample size.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        null_proportion:
            Proportion under the null hypothesis.

            Ignored if `noninferiority_proportion` is specified; otherwise, required along with `margin`.
        margin:
            The non-inferiority margin.

            Ignored if `noninferiority_proportion` is specified; otherwise, required along with `null_proportion`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        noninferiority_proportion:
            The non-inferiority proportion.

            Required if either `null_proportion` or `margin` is omitted.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        The required sample size.

    Raises:
        ValueError: If `noninferiority_proportion` is omitted, and either `null_proportion` or `margin` is missing.
    """

    margin = _margin(margin, alternative)
    noninferiority_proportion = _verify_and_get_noninf_proportion(null_proportion, margin, noninferiority_proportion)

    def func(size: float) -> float:
        return (
            _power(proportion, noninferiority_proportion, size, alternative, alpha, method, continuity_correction)
            - power
        )

    return ceil(brentq(func, 1e-12, 1e12))


def solve_proportion(
    *,
    null_proportion: float | None = None,
    margin: float | None = None,
    noninferiority_proportion: float | None = None,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"] = "z-phat",
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required proportion under the alternative hypothesis.

    Args:
        null_proportion:
            Proportion under the null hypothesis.

            Ignored if `noninferiority_proportion` is specified; otherwise, required along with `margin`.
        margin:
            The non-inferiority margin.

            Ignored if `noninferiority_proportion` is specified; otherwise, required along with `margin`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        noninferiority_proportion:
            The non-inferiority proportion.

            Required if either `null_proportion` or `margin` is omitted.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        The required proportion under the alternative hypothesis.

    Raises:
        ValueError: If `noninferiority_proportion` is omitted, and either `null_proportion` or `margin` is missing.

    Notes:
        The value range of the alternative hypothesis proportion $p$ is determined by the null hypothesis proportion $p_0$ and the non-inferiority margin $\\delta$.

        If $\\delta < 0$, we have:

        $$
        \\begin{cases}
        p > p_0 + \\delta \\\\
        0 < p < 1
        \\end{cases}
        \\Rightarrow \\operatorname{max}(p_0 + \\delta, 0) < p < 1
        $$

        If $\\delta > 0$, we have:

        $$
        \\begin{cases}
        p < p_0 + \\delta \\\\
        0 < p < 1
        \\end{cases}
        \\Rightarrow 0 < p_0 < \\operatorname{min}(p_0 + \\delta, 1)
        $$
    """

    margin = _margin(margin, alternative)
    noninferiority_proportion = _verify_and_get_noninf_proportion(null_proportion, margin, noninferiority_proportion)

    def func(proportion: float) -> float:
        return (
            _power(proportion, noninferiority_proportion, size, alternative, alpha, method, continuity_correction)
            - power
        )

    eps = 1e-12
    match alternative:
        case "greater":
            return float(brentq(func, max(noninferiority_proportion, 0) + eps, 1 - eps))
        case "less":
            return float(brentq(func, eps, min(noninferiority_proportion, 1) - eps))


def solve_null_proportion(
    *,
    proportion: float,
    margin: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"] = "z-phat",
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required proportion under the null hypothesis.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        The required proportion under the null hypothesis.

    Notes:
        The value range of the null hypothesis proportion $p_0$ is determined by the alternative hypothesis proportion $p$ and the non-inferiority margin $\\delta$.

        If $\\delta < 0$, we have:

        $$
        \\begin{cases}
        p_0 < p - \\delta \\\\
        0 < p_0 < 1 \\\\
        0 < p_0 + \\delta < 1
        \\end{cases}
        \\Rightarrow -\\delta < p_0 < \\operatorname{min}(p - \\delta, 1)
        $$

        If $\\delta > 0$, we have:

        $$
        \\begin{cases}
        p_0 > p - \\delta \\\\
        0 < p_0 < 1 \\\\
        0 < p_0 + \\delta < 1
        \\end{cases}
        \\Rightarrow \\operatorname{max}(p - \\delta, 0) < p_0 < 1 - \\delta
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
            return float(brentq(func, -margin + eps, min(proportion - margin, 1) - eps))
        case "less":
            return float(brentq(func, max(proportion - margin, 1e-12) + eps, 1 - margin - eps))


def solve_noninferiority_proportion(
    *,
    proportion: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    method: Literal["z-p0", "z-phat"] = "z-phat",
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required non-inferiority proportion.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        The required non-inferiority proportion.

    Notes:
        The value range of the non-inferiority hypothesis proportion $p_{\\text{noninf}}$ is determined by the alternative hypothesis proportion $p$.

        If `alternative` is `'greater'`, that is, higher proportions are better, we have:

        $$
        \\begin{cases}
        p_{\\text{noninf}} < p \\\\
        0 < p_{\\text{noninf}} < 1 \\\\
        \\end{cases}
        \\
        \\Rightarrow 0 < p_{\\text{noninf}} < p
        $$

        If `alternative` is `'less'`, that is, higher proportions are worse, we have:

        $$
        \\begin{cases}
        p_{\\text{noninf}} > p \\\\
        0 < p_{\\text{noninf}} < 1 \\\\
        \\end{cases}
        \\
        \\Rightarrow p < p_{\\text{noninf}} < 1
        $$
    """

    def func(noninferiority_proportion: float) -> float:
        return (
            _power(proportion, noninferiority_proportion, size, alternative, alpha, method, continuity_correction)
            - power
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
    method: Literal["z-p0", "z-phat"] = "z-phat",
    continuity_correction: bool = False,
) -> float:
    """
    Estimate the required non-inferiority margin.

    Args:
        proportion:
            Proportion under the alternative hypothesis.
        null_proportion:
            Proportion under the null hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis:

            - If `alternative` is `'greater'`, the alternative hypothesis is $p - p_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $p - p_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        method:
            The method used to construct the test statistic.

            - `'z-p0'`: Standard normal distribution (large sample approximation), using p0 to calculate the variance.
            - `'z-phat'`: Standard normal distribution (large sample approximation), using phat to calculate the variance.
        continuity_correction:
            Whether to apply the continuity correction.

    Returns:
        The required non-inferiority margin.

    Notes:
        The value range of the non-inferiority margin $\\delta$ is determined by the alternative hypothesis proportion $p$ and the null hypothesis proportion $p_0$.

        If $\\delta < 0$, we have:

        $$
        \\begin{cases}
        \\delta < p - p_0 \\\\
        0 < p_0 + \\delta < 1 \\\\
        \\delta < 0
        \\end{cases}
        \\Rightarrow -p_0 < \\delta < \\operatorname{min}(p - p_0, 0)
        $$

        If $\\delta > 0$, we have:

        $$
        \\begin{cases}
        \\delta > p - p_0 \\\\
        0 < p_0 + \\delta < 1 \\\\
        \\delta > 0
        \\end{cases}
        \\Rightarrow \\operatorname{max}(p - p_0, 0) < \\delta < 1 - p_0
        $$
    """

    def func(margin: float) -> float:
        return (
            _power(proportion, null_proportion + margin, size, alternative, alpha, method, continuity_correction)
            - power
        )

    eps = 1e-12
    match alternative:
        case "greater":
            return float(brentq(func, -null_proportion + eps, min(proportion - null_proportion, 0) - eps))
        case "less":
            return float(brentq(func, max(proportion - null_proportion, 0) + eps, 1 - null_proportion - eps))
