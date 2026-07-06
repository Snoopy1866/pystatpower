from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import nct, norm, t

from ..._constant import SAMPLE_SIZE_SEARCH_MAX


def _power_z_equal_var(
    diff: float,
    std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using z-test with equal variance."""

    se = std * sqrt(1 / treatment_size + 1 / reference_size)
    match alternative:
        case "two-sided":
            power = 1 - norm.cdf(norm.ppf(1 - alpha / 2) - (diff) / se) + norm.cdf(norm.ppf(alpha / 2) - (diff) / se)
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (diff) / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - (diff) / se)

    return float(power)


def _power_z_unequal_var(
    diff: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using z-test with unequal variance."""

    se = sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)
    match alternative:
        case "two-sided":
            power = 1 - norm.cdf(norm.ppf(1 - alpha / 2) - (diff) / se) + norm.cdf(norm.ppf(alpha / 2) - (diff) / se)
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (diff) / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - (diff) / se)

    return float(power)


def _power_t_equal_var(
    diff: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using t-test with equal variance."""

    df = treatment_size + reference_size - 2
    var_c = ((treatment_size - 1) * treatment_std**2 + (reference_size - 1) * reference_std**2) / df
    nc = (diff) / sqrt(var_c * (1 / treatment_size + 1 / reference_size))

    match alternative:
        case "two-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha / 2, df), df, nc) + nct.cdf(t.ppf(alpha / 2, df), df, nc)
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return float(power)


def _power_unequal_var_satterthwaite(
    diff: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """
    Calculate the statistical power, using t-test with unequal variance,
    degree of freedom adjustment is based on Satterthwaite method.
    """

    df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
        treatment_std**4 / (treatment_size**2 * (treatment_size - 1))
        + reference_std**4 / (reference_size**2 * (reference_size - 1))
    )
    nc = (diff) / sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)

    match alternative:
        case "two-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha / 2, df), df, nc) + nct.cdf(t.ppf(alpha / 2, df), df, nc)
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return float(power)


def _power_unequal_var_welch(
    diff: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """
    Calculate the statistical power, using t-test with unequal variance,
    degree of freedom adjustment is based on Welch method.
    """

    df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
        treatment_std**4 / (treatment_size**2 * (treatment_size + 1))
        + reference_std**4 / (reference_size**2 * (reference_size + 1))
    ) - 2
    nc = (diff) / sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)

    match alternative:
        case "two-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha / 2, df), df, nc) + nct.cdf(t.ppf(alpha / 2, df), df, nc)
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return float(power)


def _power(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    method: Literal["z", "t"],
    equal_var: bool,
    df_adjust: Literal["satterthwaite", "welch"],
) -> float:
    """Calculate the statistical power."""

    if diff is None:
        if treatment_mean is None or reference_mean is None:
            raise ValueError("If 'diff' is not provided, both 'treatment_mean' and 'reference_mean' must be specified.")
        diff = treatment_mean - reference_mean

    if method == "z" and equal_var and treatment_std != reference_std:
        raise ValueError("If `method`='z' and `equal_var`=True, `treatment_std` must equal `reference_std`.")

    match method:
        case "z":
            if equal_var:
                assert treatment_std == reference_std
                std = treatment_std
                power = _power_z_equal_var(diff, std, treatment_size, reference_size, alternative, alpha)
            else:
                power = _power_z_unequal_var(
                    diff, treatment_std, reference_std, treatment_size, reference_size, alternative, alpha
                )
        case "t":
            if equal_var:
                power = _power_t_equal_var(
                    diff, treatment_std, reference_std, treatment_size, reference_size, alternative, alpha
                )
            else:
                match df_adjust:
                    case "satterthwaite":
                        power = _power_unequal_var_satterthwaite(
                            diff, treatment_std, reference_std, treatment_size, reference_size, alternative, alpha
                        )
                    case "welch":
                        power = _power_unequal_var_welch(
                            diff, treatment_std, reference_std, treatment_size, reference_size, alternative, alpha
                        )

    return power


def solve_power(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    treatment_std: float,
    reference_std: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    method: Literal["z", "t"] = "t",
    equal_var: bool = False,
    df_adjust: Literal["satterthwaite", "welch"] = "satterthwaite",
) -> float:
    """
    Calculate the statistical power.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If provided together with `reference_mean`, `diff` is ignored.
        reference_mean:
            Mean in the reference group.

            If provided together with `treatment_mean`, `diff` is ignored.
        diff:
            Mean difference between treatment and reference group.

            If provided, `treatment_mean` and `reference_mean` will be ignored.
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_2$
            - `'greater'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_2$
            - `'less'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, provide the one-sided significance level.

        method:
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central *t* distribution.

        equal_var:
            Whether to assume equal variances between groups.

            - If `True`: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom $df = n_1 + n_2 - 2$.

            - If `False`: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If `method='z'` and `equal_var`=`True`, the standard deviation of the two groups must be equal.
        df_adjust:
            Degree of freedom adjustment method when `method="t"` and `equal_var=False`.

            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).
            - `'welch'`: Adjustment based on Welch (1947).

    Returns:
        The calculated statistical power of the test.

    Raises:
        ValueError: If `diff` is not provided, and both `treatment_mean` and `reference_mean` are not provided.
        ValueError: If `method='z'` and `equal_var`=`True` but `treatment_std` does not equal to `reference_std`.
    """

    power = _power(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
        diff=diff,
        treatment_std=treatment_std,
        reference_std=reference_std,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative=alternative,
        alpha=alpha,
        method=method,
        equal_var=equal_var,
        df_adjust=df_adjust,
    )
    return power


def solve_size(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    treatment_std: float,
    reference_std: float,
    ratio: float = 1,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = False,
    df_adjust: Literal["satterthwaite", "welch"] = "satterthwaite",
) -> tuple[int, int]:
    """
    Estimate the required sample size.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If provided together with `reference_mean`, `diff` is ignored.
        reference_mean:
            Mean in the reference group.

            If provided together with `treatment_mean`, `diff` is ignored.
        diff:
            Mean difference between treatment and reference group.

            If provided, `treatment_mean` and `reference_mean` will be ignored.
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        ratio:
            Ratio of treatment sample size to reference sample size.
        alternative:
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_2$
            - `'greater'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_2$
            - `'less'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, provide the one-sided significance level.
        power:
            Desired statistical power.
        method:
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central *t* distribution.

        equal_var:
            Whether to assume equal variances between groups.

            - If True: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method="t"`, degree of freedom $df = n_1 + n_2 - 2$.

            - If False: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method="t"`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If `method='z'` and `equal_var`=`True`, the standard deviation of the two groups must be equal.
        df_adjust:
            Degree of freedom adjustment method when `method="t"` and `equal_var=False`.

            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).
            - `'welch'`: Adjustment based on Welch (1947).

    Returns:
        The required sample sizes in the treatment and reference groups, respectively.

    Raises:
        ValueError: If `diff` is not provided, and both `treatment_mean` and `reference_mean` are not provided.
        ValueError: If `method='z'` and `equal_var`=`True` but `treatment_std` does not equal to `reference_std`.
    """

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _power(
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    diff=diff,
                    treatment_std=treatment_std,
                    reference_std=reference_std,
                    treatment_size=reference_size * ratio,
                    reference_size=reference_size,
                    alternative=alternative,
                    alpha=alpha,
                    method=method,
                    equal_var=equal_var,
                    df_adjust=df_adjust,
                )
                - power
            )

        lower_bound = max(3 / (1 + ratio), 1) + 0.1
        upper_bound = SAMPLE_SIZE_SEARCH_MAX
        reference_size = ceil(brentq(func, lower_bound, upper_bound))
        treatment_size = ceil(reference_size * ratio)
        return treatment_size, reference_size
    else:

        def func(treatment_size: float) -> float:
            return (
                _power(
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    diff=diff,
                    treatment_std=treatment_std,
                    reference_std=reference_std,
                    treatment_size=treatment_size,
                    reference_size=treatment_size / ratio,
                    alternative=alternative,
                    alpha=alpha,
                    method=method,
                    equal_var=equal_var,
                    df_adjust=df_adjust,
                )
                - power
            )

        lower_bound = max(3 / (1 + 1 / ratio), 1) + 0.1
        upper_bound = SAMPLE_SIZE_SEARCH_MAX
        treatment_size = ceil(brentq(func, lower_bound, upper_bound))
        reference_size = ceil(treatment_size / ratio)
        return treatment_size, reference_size


def solve_diff(
    *,
    treatment_std: float,
    reference_std: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    search_direction: Literal["above", "below"] = "above",
    alpha: float = 0.05,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = False,
    df_adjust: Literal["satterthwaite", "welch"] = "satterthwaite",
) -> float:
    """
    Estimate the required mean difference.

    Args:
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_2$
            - `'greater'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_2$
            - `'less'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_2$
        search_direction:
            Specify whether to search for the mean difference above or below 0.

            - `'above'`: Search the difference above 0.
            - `'below'`: Search the difference below 0.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, provide the one-sided significance level.
        power:
            Desired statistical power.
        method:
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central *t* distribution.

        equal_var:
            Whether to assume equal variances between groups.

            - If `True`: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, degree of freedom $df = n_1 + n_2 - 2$.

            - If `False`: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If `method='z'` and `equal_var`=`True`, the standard deviation of the two groups must be equal.
        df_adjust:
            Degree of freedom adjustment method when `method='t'` and `equal_var=False`.

            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).
            - `'welch'`: Adjustment based on Welch (1947).

    Returns:
        The required difference between the treatment and reference means.

    Raises:
        ValueError: If `diff` is not provided, and both `treatment_mean` and `reference_mean` are not provided.
        ValueError: If `method='z'` and `equal_var`=`True` but `treatment_std` does not equal to `reference_std`.
    """

    def func(diff: float) -> float:
        return (
            _power(
                diff=diff,
                treatment_std=treatment_std,
                reference_std=reference_std,
                treatment_size=treatment_size,
                reference_size=reference_size,
                alternative=alternative,
                alpha=alpha,
                method=method,
                equal_var=equal_var,
                df_adjust=df_adjust,
            )
            - power
        )

    DIFF_SEARCH_MIN = -1000000
    DIFF_SEARCH_MAX = 1000000

    match search_direction:
        case "above":
            return float(brentq(func, 0, DIFF_SEARCH_MAX))
        case "below":
            return float(brentq(func, DIFF_SEARCH_MIN, 0))


def solve_treatment_mean(
    *,
    reference_mean: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    search_direction: Literal["above", "below"] = "above",
    alpha: float = 0.05,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = False,
    df_adjust: Literal["satterthwaite", "welch"] = "satterthwaite",
) -> float:
    """
    Estimate the required mean in the treatment group.

    Args:
        reference_mean:
            Mean in the reference group.
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_2$
            - `'greater'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_2$
            - `'less'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_2$
        search_direction:
            Specify whether to search for the treatment mean above or below the reference mean.

            - `'above'`: Search the treatment mean above the reference mean.
            - `'below'`: Search the treatment mean below the reference mean.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, provide the one-sided significance level.
        power:
            Desired statistical power.
        method:
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central *t* distribution.

        equal_var:
            Whether to assume equal variances between groups.

            - If `True`: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, degree of freedom $df = n_1 + n_2 - 2$.

            - If `False`: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If `method='z'` and `equal_var`=`True`, the standard deviation of the two groups must be equal.
        df_adjust:
            Degree of freedom adjustment method when `method='t'` and `equal_var=False`.

            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).
            - `'welch'`: Adjustment based on Welch (1947).

    Returns:
        The required mean in the treatment group.

    Raises:
        ValueError: If `method='z'` and `equal_var`=`True` but `treatment_std` does not equal to `reference_std`.
    """

    def func(treatment_mean: float) -> float:
        return (
            _power(
                treatment_mean=treatment_mean,
                reference_mean=reference_mean,
                treatment_std=treatment_std,
                reference_std=reference_std,
                treatment_size=treatment_size,
                reference_size=reference_size,
                alternative=alternative,
                alpha=alpha,
                method=method,
                equal_var=equal_var,
                df_adjust=df_adjust,
            )
            - power
        )

    DIFF_SEARCH_MIN = -1000000
    DIFF_SEARCH_MAX = 1000000

    match search_direction:
        case "above":
            return float(brentq(func, reference_mean, DIFF_SEARCH_MAX))
        case "below":
            return float(brentq(func, DIFF_SEARCH_MIN, reference_mean))


def solve_reference_mean(
    *,
    treatment_mean: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    search_direction: Literal["above", "below"] = "below",
    alpha: float = 0.05,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = False,
    df_adjust: Literal["satterthwaite", "welch"] = "satterthwaite",
) -> float:
    """
    Estimate the required mean in the reference group.

    Args:
        treatment_mean:
            Mean in the treatment group.
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_2$
            - `'less'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_2$
            - `'greater'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_2$
        search_direction:
            Specify whether to search for the reference mean above or below the treatment mean.

            - `'above'`: Search the reference mean above the treatment mean.
            - `'below'`: Search the reference mean below the treatment mean.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, provide the one-sided significance level.
        power:
            Desired statistical power.
        method:
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central *t* distribution.

        equal_var:
            Whether to assume equal variances between groups.

            - If `True`: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, degree of freedom $df = n_1 + n_2 - 2$.

            - If `False`: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If `method='z'` and `equal_var`=`True`, the standard deviation of the two groups must be equal.
        df_adjust:
            Degree of freedom adjustment method when `method='t'` and `equal_var=False`.

            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).
            - `'welch'`: Adjustment based on Welch (1947).

    Returns:
        The required mean in the treatment group.

    Raises:
        ValueError: If `method='z'` and `equal_var`=`True` but `treatment_std` does not equal to `reference_std`.
    """

    def func(reference_mean: float) -> float:
        return (
            _power(
                treatment_mean=treatment_mean,
                reference_mean=reference_mean,
                treatment_std=treatment_std,
                reference_std=reference_std,
                treatment_size=treatment_size,
                reference_size=reference_size,
                alternative=alternative,
                alpha=alpha,
                method=method,
                equal_var=equal_var,
                df_adjust=df_adjust,
            )
            - power
        )

    DIFF_SEARCH_MIN = -1000000
    DIFF_SEARCH_MAX = 1000000

    match search_direction:
        case "above":
            return float(brentq(func, treatment_mean, DIFF_SEARCH_MAX))
        case "below":
            return float(brentq(func, DIFF_SEARCH_MIN, treatment_mean))


def solve_treatment_std(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = True,
    reference_std: float | None = None,
    df_adjust: Literal["satterthwaite", "welch"] = "satterthwaite",
) -> float:
    """
    Estimate the required standard deviation in the treatment group.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If provided together with `reference_mean`, `diff` is ignored.
        reference_mean:
            Mean in the reference group.

            If provided together with `treatment_mean`, `diff` is ignored.
        diff:
            Mean difference between treatment and reference group.

            If provided, `treatment_mean` and `reference_mean` will be ignored.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_2$
            - `'greater'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_2$
            - `'less'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, provide the one-sided significance level.
        power:
            Desired statistical power.
        method:
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central t distribution.

        equal_var:
            Whether to assume equal variances between groups.

            - If `True`: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, degree of freedom $df = n_1 + n_2 - 2$.

            - If `False`: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If Z test is used and `equal_var` is True, the standard deviation of the two groups must be equal.
        reference_std:
            Standard deviation in the reference group.

            If `equal_var`=`True`, this parameter is ignored, otherwise, you must specify this parameter.
        df_adjust:
            Degree of freedom adjustment method when `method='t'` and `equal_var=False`.

            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).
            - `'welch'`: Adjustment based on Welch (1947).

    Returns:
        The required standard deviation in the treatment group.

    Raises:
        ValueError: If `diff` is not provided, and both `treatment_mean` and `reference_mean` are not provided.
        ValueError: If `equal_var=False` but `reference_std` is not provided.
    """

    if equal_var:

        def func(treatment_std: float) -> float:
            return (
                _power(
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    diff=diff,
                    treatment_std=treatment_std,
                    reference_std=treatment_std,
                    treatment_size=treatment_size,
                    reference_size=reference_size,
                    alternative=alternative,
                    alpha=alpha,
                    method=method,
                    equal_var=equal_var,
                    df_adjust=df_adjust,
                )
                - power
            )
    else:  # equal_var=False
        if reference_std is None:
            raise ValueError("If equal_var=False, reference_std must be provided.")

        def func(treatment_std: float) -> float:
            return (
                _power(
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    diff=diff,
                    treatment_std=treatment_std,
                    reference_std=reference_std,
                    treatment_size=treatment_size,
                    reference_size=reference_size,
                    alternative=alternative,
                    alpha=alpha,
                    method=method,
                    equal_var=equal_var,
                    df_adjust=df_adjust,
                )
                - power
            )

    STD_SEARCH_MAX = 1000000

    return float(brentq(func, 0.000001, STD_SEARCH_MAX))


def solve_reference_std(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = True,
    treatment_std: float | None = None,
    df_adjust: Literal["satterthwaite", "welch"] = "satterthwaite",
) -> float:
    """
    Estimate the required standard deviation in the reference group.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If provided together with `reference_mean`, `diff` is ignored.
        reference_mean:
            Mean in the reference group.

            If provided together with `treatment_mean`, `diff` is ignored.
        diff:
            Mean difference between treatment and reference group.

            If provided, `treatment_mean` and `reference_mean` will be ignored.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - `'two-sided'`: Two-sided alternative hypothesis: $\\mu_1 \\neq \\mu_2$
            - `'less'`: Lower one-sided alternative hypothesis: $\\mu_1 < \\mu_2$
            - `'greater'`: Upper one-sided alternative hypothesis: $\\mu_1 > \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, provide the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, provide the one-sided significance level.
        power:
            Desired statistical power.
        method:
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central t distribution.

        equal_var:
            Whether to assume equal variances between groups.

            - If True: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, degree of freedom $df = n_1 + n_2 - 2$.

            - If False: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If Z test is used and `equal_var` is True, the standard deviation of the two groups must be equal.
        treatment_std:
            Standard deviation in the treatment group.

            If `equal_var`=`True`, this parameter is ignored, otherwise, you must specify this parameter.
        df_adjust:
            Degree of freedom adjustment method when `method="t"` and `equal_var=False`.

            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).
            - `'welch'`: Adjustment based on Welch (1947).

    Returns:
        The required standard deviation in the reference group.

    Raises:
        ValueError: If `diff` is not provided, and both `treatment_mean` and `reference_mean` are not provided.
        ValueError: If `equal_var=False` but `treatment_std` is not provided.
    """
    if equal_var:

        def func(reference_std: float) -> float:
            return (
                _power(
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    diff=diff,
                    treatment_std=reference_std,
                    reference_std=reference_std,
                    treatment_size=treatment_size,
                    reference_size=reference_size,
                    alternative=alternative,
                    alpha=alpha,
                    method=method,
                    equal_var=equal_var,
                    df_adjust=df_adjust,
                )
                - power
            )
    else:  # equal_var == False
        if treatment_std is None:
            raise ValueError("If equal_var=False, treatment_std must be provided.")

        def func(reference_std: float) -> float:
            return (
                _power(
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    diff=diff,
                    treatment_std=treatment_std,
                    reference_std=reference_std,
                    treatment_size=treatment_size,
                    reference_size=reference_size,
                    alternative=alternative,
                    alpha=alpha,
                    method=method,
                    equal_var=equal_var,
                    df_adjust=df_adjust,
                )
                - power
            )

    STD_SEARCH_MAX = 1000000

    return float(brentq(func, 0.000001, STD_SEARCH_MAX))
