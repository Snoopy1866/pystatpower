from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import nct, norm, t

from ...._constant import SAMPLE_SIZE_SEARCH_MAX


def _power_z_equal_var(
    diff: float,
    margin: float,
    std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["lower", "upper"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a superiority test of two independent means using z-test with equal variance."""

    se = std * sqrt(1 / treatment_size + 1 / reference_size)
    match alternative:
        case "lower":
            power = norm.cdf(norm.ppf(alpha) - (diff - margin) / se)
        case "upper":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (diff - margin) / se)
    return float(power)


def _power_z_unequal_var(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["lower", "upper"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a superiority test of two independent means using z-test with unequal variance."""

    se = sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)
    match alternative:
        case "lower":
            power = norm.cdf(norm.ppf(alpha) - (diff - margin) / se)
        case "upper":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (diff - margin) / se)
    return float(power)


def _power_t_equal_var(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["lower", "upper"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a superiority test of two independent means using t-test with equal variance."""

    df = treatment_size + reference_size - 2
    var_c = ((treatment_size - 1) * treatment_std**2 + (reference_size - 1) * reference_std**2) / df
    nc = (diff - margin) / sqrt(var_c * (1 / treatment_size + 1 / reference_size))

    match alternative:
        case "lower":
            power = nct.cdf(t.ppf(alpha, df), df, nc)
        case "upper":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)

    return power


def _power_unequal_var_welch(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["lower", "upper"],
    alpha: float,
) -> float:
    """
    Calculate the statistical power for a superiority test of two independent means using t-test with unequal variance,
    degree of freedom adjustment is based on Welch's method.
    """

    df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
        treatment_std**4 / (treatment_size**2 * (treatment_size + 1))
        + reference_std**4 / (reference_size**2 * (reference_size + 1))
    ) - 2
    nc = (diff - margin) / sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)

    match alternative:
        case "lower":
            power = nct.cdf(t.ppf(alpha, df), df, nc)
        case "upper":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)

    return power


def _power_unequal_var_satterthwaite(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["lower", "upper"],
    alpha: float,
) -> float:
    """
    Calculate the statistical power for a superiority test of two independent means using t-test with unequal variance,
    degree of freedom adjustment is based on Satterthwaite's method.
    """

    df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
        treatment_std**4 / (treatment_size**2 * (treatment_size - 1))
        + reference_std**4 / (reference_size**2 * (reference_size - 1))
    )
    nc = (diff - margin) / sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)

    match alternative:
        case "lower":
            power = nct.cdf(t.ppf(alpha, df), df, nc)
        case "upper":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)

    return power


def _power(
    *,
    diff: float | None = None,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["lower", "upper"],
    alpha: float,
    method: Literal["z", "t"],
    equal_var: bool,
    df_adjust: Literal["welch", "satterthwaite"],
) -> float:
    """Calculate the statistical power for a superiority test of two independent means."""

    if diff is None:
        if treatment_mean is None or reference_mean is None:
            raise ValueError("If 'diff' is not provided, both 'treatment_mean' and 'reference_mean' must be specified.")
        diff = treatment_mean - reference_mean

    match method:
        case "z":
            if equal_var:
                assert treatment_std == reference_std
                std = treatment_std
                power = _power_z_equal_var(diff, margin, std, treatment_size, reference_size, alternative, alpha)
            else:
                power = _power_z_unequal_var(
                    diff, margin, treatment_std, reference_std, treatment_size, reference_size, alternative, alpha
                )
        case "t":
            if equal_var:
                power = _power_t_equal_var(
                    diff, margin, treatment_std, reference_std, treatment_size, reference_size, alternative, alpha
                )
            else:
                match df_adjust:
                    case "welch":
                        power = _power_unequal_var_welch(
                            diff,
                            margin,
                            treatment_std,
                            reference_std,
                            treatment_size,
                            reference_size,
                            alternative,
                            alpha,
                        )
                    case "satterthwaite":
                        power = _power_unequal_var_satterthwaite(
                            diff,
                            margin,
                            treatment_std,
                            reference_std,
                            treatment_size,
                            reference_size,
                            alternative,
                            alpha,
                        )

    return power


def solve_power(
    *,
    diff: float | None = None,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["lower", "upper"] = "upper",
    alpha: float = 0.025,
    method: Literal["z", "t"] = "t",
    equal_var: bool = False,
    df_adjust: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Calculate the statistical power for a superiority test of two independent means.

    Args:
        diff (float, optional):
            Mean difference between treatment and reference group ($\\mu_1 - \\mu_2$).

            If provided, `treatment_mean` and `reference_mean` will be ignored.
        treatment_mean (float, optional):
            Mean in the treatment group ($\\mu_1$).

            If `diff` is not provided, this must be specified along with `reference_mean`.
        reference_mean (float, optional):
            Mean in the reference group ($\\mu_2$).

            If `diff` is not provided, this must be specified along with `treatment_mean`.
        margin (float):
            The superiority margin ($\\delta$)

            - provide a positive value if a higher mean is better
            - provide a negative value if a higher mean is worse
        treatment_std (float):
            Standard deviation in the treatment group ($\\sigma_1$).
        reference_std (float):
            Standard deviation in the reference group ($\\sigma_2$).
        treatment_size (int):
            Sample size in the treatment group ($n_1$).
        reference_size (int):
            Sample size in the reference group ($n_2$).
        alternative (Literal["lower", "upper"], optional):
            Type of the alternative hypothesis.

            - `'lower'`: lower-tailed alternative hypothesis: $\\mu_1 - \\mu_2 < \\delta$
            - `'upper'`: upper-tailed alternative hypothesis: $\\mu_1 - \\mu_2 > \\delta$
        alpha (float, optional):
            One-sided significance level.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central *t* distribution.

        equal_var (bool, optional):
            Whether to assume equal variances between groups.

            - `True`: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom $df = n_1 + n_2 - 2$.

            - `False`: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If `method='z'` and `equal_var=True`, the standard deviation of the two groups must be equal.
        df_adjust (Literal["welch", "satterthwaite"], optional):
            Degree of freedom adjustment method when `method="t"` and `equal_var=False`.

            - `'welch'`: Adjustment based on Welch (1947).
            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).

    Returns:
        (float): The calculated statistical power of the test.

    Raises:
        ValueError: If `diff` is not provided, and both `treatment_mean` and `reference_mean` are not provided.
        ValueError: If `method='z'` and `equal_var=True` but `treatment_std` does not equal to `reference_std`.
    """

    if method == "z" and equal_var and treatment_std != reference_std:
        raise ValueError("If method='z' and equal_var=True, treatment_std must equal reference_std.")

    power = _power(
        diff=diff,
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
        margin=margin,
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
    diff: float | None = None,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    margin: float,
    treatment_std: float,
    reference_std: float,
    ratio: float = 1,
    alternative: Literal["lower", "upper"] = "upper",
    alpha: float = 0.025,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = False,
    df_adjust: Literal["welch", "satterthwaite"] = "welch",
) -> tuple[int, int]:
    """
    Estimate the required sample size for a superiority test of two independent means.

    Args:
        diff (float, optional):
            Mean difference between treatment and reference group ($\\mu_1 - \\mu_2$).

            If provided, `treatment_mean` and `reference_mean` will be ignored.
        treatment_mean (float, optional):
            Mean in the treatment group ($\\mu_1$).

            If `diff` is not provided, this must be specified along with `reference_mean`.
        reference_mean (float, optional):
            Mean in the reference group ($\\mu_2$).

            If `diff` is not provided, this must be specified along with `treatment_mean`.
        margin (float):
            The superiority margin ($\\delta$)

            - provide a positive value if a higher mean is better
            - provide a negative value if a higher mean is worse
        treatment_std (float):
            Standard deviation in the treatment group ($\\sigma_1$).
        reference_std (float):
            Standard deviation in the reference group ($\\sigma_2$).
        ratio (float, optional):
            Ratio of treatment sample size to reference sample size ($k = n_1 / n_2$).
        alternative (Literal["lower", "upper"], optional):
            Type of the alternative hypothesis.

            - `'lower'`: lower-tailed alternative hypothesis: $\\mu_1 - \\mu_2 < \\delta$
            - `'upper'`: upper-tailed alternative hypothesis: $\\mu_1 - \\mu_2 > \\delta$
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central *t* distribution.

        equal_var (bool, optional):
            Whether to assume equal variances between groups.

            - `True`: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method="t"`, degree of freedom $df = n_1 + n_2 - 2$.

            - `False`: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method="t"`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If `method='z'` and `equal_var=True`, the standard deviation of the two groups must be equal.
        df_adjust (Literal["welch", "satterthwaite"], optional):
            Degree of freedom adjustment method when `method="t"` and `equal_var=False`.

            - `'welch'`: Adjustment based on Welch (1947).
            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).

    Returns:
        (tuple[int, int]): The required sample sizes for the treatment and reference groups, respectively.

    Raises:
        ValueError: If `diff` is not provided, and both `treatment_mean` and `reference_mean` are not provided.
        ValueError: If `method='z'` and `equal_var=True` but `treatment_std` does not equal to `reference_std`.
    """

    if method == "z" and equal_var and treatment_std != reference_std:
        raise ValueError("If method='z' and equal_var=True, treatment_std must equal reference_std.")

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _power(
                    diff=diff,
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    margin=margin,
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

        lower_bound = max(3 / (1 + ratio), 1) + 0.000001
        upper_bound = SAMPLE_SIZE_SEARCH_MAX
        reference_size = int(ceil(brentq(func, lower_bound, upper_bound)))
        treatment_size = int(ceil(reference_size * ratio))
        return treatment_size, reference_size
    else:

        def func(treatment_size: float) -> float:
            return (
                _power(
                    diff=diff,
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    margin=margin,
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

        lower_bound = max(3 / (1 + 1 / ratio), 1) + 0.000001
        upper_bound = SAMPLE_SIZE_SEARCH_MAX
        treatment_size = ceil(brentq(func, lower_bound, upper_bound))
        reference_size = ceil(treatment_size / ratio)
        return treatment_size, reference_size


def solve_diff(
    *,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["lower", "upper"] = "upper",
    alpha: float = 0.025,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = False,
    df_adjust: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required difference for a superiority test of two independent means.

    Args:
        margin (float):
            The superiority margin ($\\delta$)

            - provide a positive value if a higher mean is better
            - provide a negative value if a higher mean is worse
        treatment_std (float):
            Standard deviation in the treatment group ($\\sigma_1$).
        reference_std (float):
            Standard deviation in the reference group ($\\sigma_2$).
        treatment_size (int):
            Sample size for the treatment group ($n_1$).
        reference_size (int):
            Sample size for the reference group ($n_2$).
        alternative (Literal["lower", "upper"], optional):
            Type of the alternative hypothesis.

            - `'lower'`: lower-tailed alternative hypothesis: $H_1: \\mu_1 - \\mu_2 < \\delta$
            - `'upper'`: upper-tailed alternative hypothesis: $H_1: \\mu_1 - \\mu_2 > \\delta$
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central *t* distribution.

        equal_var (bool, optional):
            Whether to assume equal variances between groups.

            - `True`: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, degree of freedom $df = n_1 + n_2 - 2$.

            - `False`: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If `method='z'` and `equal_var=True`, the standard deviation of the two groups must be equal.
        df_adjust (Literal["welch", "satterthwaite"], optional):
            Degree of freedom adjustment method when `method='t'` and `equal_var=False`.

            - `'welch'`: Adjustment based on Welch (1947).
            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).

    Returns:
        (float): The required difference between the treatment and reference means.

    Raises:
        ValueError: If `method='z'` and `equal_var=True` but `treatment_std` does not equal to `reference_std`.

    Notes:
        The search interval for mean difference ($\\mu_1 - \\mu_2$) is constrained by the superiority margin ($\\delta$) to ensure the alternative hypothesis remains plausible.

        $$
        \\text{Search Interval} =
        \\begin{cases}
        (\\delta, \\ +\\infty)  & , \\text{if alternative is upper} \\\\
        (-\\infty, \\ \\delta)  & , \\text{if alternative is lower} \\\\
        \\end{cases}
        $$
    """

    if method == "z" and equal_var and treatment_std != reference_std:
        raise ValueError("If method='z' and equal_var=True, treatment_std must equal reference_std.")

    def func(diff: float) -> float:
        return (
            _power(
                diff=diff,
                margin=margin,
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

    match alternative:
        case "lower":
            return float(brentq(func, DIFF_SEARCH_MIN, margin))
        case "upper":
            return float(brentq(func, margin, DIFF_SEARCH_MAX))


def solve_margin(
    *,
    diff: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["lower", "upper"] = "upper",
    alpha: float = 0.025,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = False,
    df_adjust: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required margin for a superiority test of two independent means.

    Args:
        diff (float):
            Mean difference between treatment and reference group ($\\mu_1 - \\mu_2$).
        treatment_std (float):
            Standard deviation in the treatment group ($\\sigma_1$).
        reference_std (float):
            Standard deviation in the reference group ($\\sigma_2$).
        treatment_size (int):
            Sample size for the treatment group ($n_1$).
        reference_size (int):
            Sample size for the reference group ($n_2$).
        alternative (Literal["lower", "upper"], optional):
            Type of the alternative hypothesis.

            - `'lower'`: lower-tailed alternative hypothesis: $H_1: \\mu_1 - \\mu_2 < \\delta$
            - `'upper'`: upper-tailed alternative hypothesis: $H_1: \\mu_1 - \\mu_2 > \\delta$
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central t distribution.

        equal_var (bool, optional):
            Whether to assume equal variances between groups.

            - `True`: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, degree of freedom $df = n_1 + n_2 - 2$.

            - `False`: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If `method='z'` and `equal_var=True`, the standard deviation of the two groups must be equal.
        df_adjust (Literal["welch", "satterthwaite"], optional):
            Degree of freedom adjustment method when `method='t'` and `equal_var=False`.

            - `'welch'`: Adjustment based on Welch (1947).
            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).

    Returns:
        (float): The required superiority margin.

    Raises:
        ValueError: If `method='z'` and `equal_var=True` but `treatment_std` does not equal to `reference_std`.

    Notes:
        The search interval for superiority margin ($\\delta$) is constrained by the mean difference ($\\mu_1 - \\mu_2$) to ensure the alternative hypothesis remains plausible.

        $$
        \\text{Search Interval} =
        \\begin{cases}
        [0, \\ \\mu_1 - \\mu_2) & , \\text{if alternative is upper} \\\\
        (\\mu_1 - \\mu_2, \\ 0] & , \\text{if alternative is lower} \\\\
        \\end{cases}
        $$
    """

    if method == "z" and equal_var and treatment_std != reference_std:
        raise ValueError("If method='z' and equal_var=True, treatment_std must equal reference_std.")

    def func(margin: float) -> float:
        return (
            _power(
                diff=diff,
                margin=margin,
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

    match alternative:
        case "lower":
            return brentq(func, diff, 0.000001)
        case "upper":
            return brentq(func, -0.000001, diff)


def solve_treatment_std(
    *,
    diff: float | None = None,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    margin: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["lower", "upper"] = "upper",
    alpha: float = 0.025,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = True,
    reference_std: float | None = None,
    df_adjust: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required standard deviation in the treatment group for a superiority test of two independent means.

    Args:
        diff (float, optional):
            Mean difference between treatment and reference group ($\\mu_1 - \\mu_2$).

            If provided, `treatment_mean` and `reference_mean` will be ignored.
        treatment_mean (float, optional):
            Mean in the treatment group ($\\mu_1$).

            If `diff` is not provided, this must be specified along with `reference_mean`.
        reference_mean (float, optional):
            Mean in the reference group ($\\mu_2$).

            If `diff` is not provided, this must be specified along with `treatment_mean`.
        margin (float):
            The superiority margin ($\\delta$)

            - provide a positive value if a higher mean is better
            - provide a negative value if a higher mean is worse
        treatment_size (int):
            Sample size for the treatment group ($n_1$).
        reference_size (int):
            Sample size for the reference group ($n_2$).
        alternative (Literal["lower", "upper"], optional):
            Type of the alternative hypothesis.

            - `'lower'`: lower-tailed alternative hypothesis: $H_1: \\mu_1 - \\mu_2 < \\delta$
            - `'upper'`: upper-tailed alternative hypothesis: $H_1: \\mu_1 - \\mu_2 > \\delta$
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central t distribution.

        equal_var (bool, optional):
            Whether to assume equal variances between groups.

            - `True`: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, degree of freedom $df = n_1 + n_2 - 2$.

            - `False`: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If Z test is used and `equal_var` is True, the standard deviation of the two groups must be equal.
        reference_std (float | None, optional):
            Standard deviation in the reference group ($\\sigma_2$).

            If `equal_var=True`, this parameter is ignored, otherwise, you must specify this parameter.
        df_adjust (Literal["welch", "satterthwaite"], optional):
            Degree of freedom adjustment method when `method='t'` and `equal_var=False`.

            - `'welch'`: Adjustment based on Welch (1947).
            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).

    Returns:
        (float): The required standard deviation in the treatment group.

    Raises:
        ValueError: If `diff` is not provided, and both `treatment_mean` and `reference_mean` are not provided.
        ValueError: If `equal_var=False` and `reference_std=None`.
    """

    if not equal_var and reference_std is None:
        raise ValueError("reference_std must be provided when equal_var=False.")

    if equal_var:

        def func(treatment_std: float) -> float:
            return (
                _power(
                    diff=diff,
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    margin=margin,
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
    else:  # equal_var == False

        def func(treatment_std: float) -> float:
            return (
                _power(
                    diff=diff,
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    margin=margin,
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
    diff: float | None = None,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    margin: float,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["lower", "upper"] = "upper",
    alpha: float = 0.025,
    power: float = 0.80,
    method: Literal["z", "t"] = "t",
    equal_var: bool = True,
    treatment_std: float | None = None,
    df_adjust: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required standard deviation in the reference group for a superiority test of two independent means.

    Args:
        diff (float, optional):
            Mean difference between treatment and reference group ($\\mu_1 - \\mu_2$).

            If provided, `treatment_mean` and `reference_mean` will be ignored.
        treatment_mean (float, optional):
            Mean in the treatment group ($\\mu_1$).

            If `diff` is not provided, this must be specified along with `reference_mean`.
        reference_mean (float, optional):
            Mean in the reference group ($\\mu_2$).

            If `diff` is not provided, this must be specified along with `treatment_mean`.
        margin (float):
            The superiority margin ($\\delta$)

            - provide a positive value if a higher mean is better
            - provide a negative value if a higher mean is worse
        treatment_size (int):
            Sample size for the treatment group ($n_1$).
        reference_size (int):
            Sample size for the reference group ($n_2$).
        alternative (Literal["lower", "upper"], optional):
            Type of the alternative hypothesis.

            - `'lower'`: lower-tailed alternative hypothesis: $H_1: \\mu_1 - \\mu_2 < \\delta$
            - `'upper'`: upper-tailed alternative hypothesis: $H_1: \\mu_1 - \\mu_2 > \\delta$
        alpha (float, optional):
            One-sided significance level.
        power (float, optional):
            Desired statistical power.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - `'z'`: Standard normal distribution (large sample approximation).
            - `'t'`: Student's or non-central t distribution.

        equal_var (bool, optional):
            Whether to assume equal variances between groups.

            - If True: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method='t'`, degree of freedom $df = n_1 + n_2 - 2$.

            - If False: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method='t'`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            If Z test is used and `equal_var` is True, the standard deviation of the two groups must be equal.
        treatment_std (float | None, optional):
            Standard deviation in the treatment group ($\\sigma_2$).

            If `equal_var=True`, this parameter is ignored, otherwise, you must specify this parameter.
        df_adjust (Literal["welch", "satterthwaite"], optional):
            Degree of freedom adjustment method when `method="t"` and `equal_var=False`.

            - `'welch'`: Adjustment based on Welch (1947).
            - `'satterthwaite'`: Adjustment based on Satterthwaite (1946).

    Returns:
        (float): The required standard deviation in the reference group.

    Raises:
        ValueError: If `diff` is not provided, and both `treatment_mean` and `reference_mean` are not provided.
        ValueError: If `equal_var=False` and `treatment_std=None`.
    """

    if not equal_var and treatment_std is None:
        raise ValueError("treatment_std must be provided when equal_var=False.")

    if equal_var:

        def func(reference_std: float) -> float:
            return (
                _power(
                    diff=diff,
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    margin=margin,
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

        def func(reference_std: float) -> float:
            return (
                _power(
                    diff=diff,
                    treatment_mean=treatment_mean,
                    reference_mean=reference_mean,
                    margin=margin,
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
