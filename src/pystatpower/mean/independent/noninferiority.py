from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import nct, norm, t


def _verify_mean_and_get_diff(
    treatment_mean: float | None,
    reference_mean: float | None,
    diff: float | None,
) -> float:

    if diff is None:
        if treatment_mean is None or reference_mean is None:
            raise ValueError("When 'diff' is omitted, both 'treatment_mean' and 'reference_mean' must be provided.")
        diff = treatment_mean - reference_mean

    return diff


def _verify_std_and_get_std(
    treatment_std: float | None,
    reference_std: float | None,
    std: float | None,
    dist: Literal["z", "t"],
    equal_var: bool,
) -> float:

    if dist == "z":
        if equal_var:
            if std is None:
                if treatment_std is None and reference_std is None:
                    raise ValueError(
                        "For 'z' test with equal variance, at least one of 'std', 'treatment_std', or 'reference_std' must be specified."
                    )
                elif treatment_std is not None and reference_std is not None:
                    if treatment_std != reference_std:
                        raise ValueError(
                            "For 'z' test with equal variance, when 'std' is omitted and both 'treatment_std' and 'reference_std' are supplied, they must be equal."
                        )
                    else:  # treatment_std == reference_std
                        std = treatment_std
                elif treatment_std is None and reference_std is not None:
                    std = reference_std
                else:  # treatment_std is not None and reference_std is None:
                    std = treatment_std
        else:  # equal_var == False
            if treatment_std is None or reference_std is None:
                raise ValueError(
                    "For z-test with unequal variance, both 'treatment_std' and 'reference_std' must be specified."
                )
    else:  # dist == "t"
        if treatment_std is None or reference_std is None:
            raise ValueError("For t-test, both 'treatment_std' and 'reference_std' must be specified.")

    return std


def _margin(margin: float, alternative: Literal["greater", "less"]) -> float:
    """Convert margin to standard form based on alternative hypothesis"""

    match alternative:
        case "greater":
            return -abs(margin)
        case "less":
            return abs(margin)


def _power_z_equal_var(
    diff: float,
    margin: float,
    std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a non-inferiority test of two independent means using z test with equal variance."""

    se = std * sqrt(1 / treatment_size + 1 / reference_size)

    match alternative:
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (diff - margin) / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - (diff - margin) / se)

    return float(power)


def _power_z_unequal_var(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a non-inferiority test of two independent means using z test with unequal variance."""

    se = sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)

    match alternative:
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (diff - margin) / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - (diff - margin) / se)

    return float(power)


def _power_t_equal_var(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for a non-inferiority test of two independent means using t test with equal variance."""

    df = treatment_size + reference_size - 2
    se = sqrt(
        ((treatment_size - 1) * treatment_std**2 + (reference_size - 1) * reference_std**2)
        / df
        * (1 / treatment_size + 1 / reference_size)
    )
    nc = (diff - margin) / se

    match alternative:
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return power


def _power_unequal_var_welch(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """
    Calculate the statistical power for a non-inferiority test of two independent means using t test with unequal variance, degredde of freedom adjustment is based on Welch's method.
    """

    df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
        treatment_std**4 / (treatment_size**2 * (treatment_size + 1))
        + reference_std**4 / (reference_size**2 * (reference_size + 1))
    ) - 2
    se = sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)
    nc = (diff - margin) / se

    match alternative:
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return power


def _power_unequal_var_satterthwaite(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
) -> float:
    """
    Calculate the statistical power for a non-inferiority test of two independent means using t test with unequal variance, degree of freedom adjustment is based on Satterthwaite's method.
    """

    df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
        treatment_std**4 / (treatment_size**2 * (treatment_size - 1))
        + reference_std**4 / (reference_size**2 * (reference_size - 1))
    )
    se = sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)
    nc = (diff - margin) / se

    match alternative:
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return power


def _power(
    *,
    diff: float | None = None,
    margin: float,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["greater", "less"],
    alpha: float,
    dist: Literal["z", "t"],
    equal_var: bool,
    approx_t_method: Literal["welch", "satterthwaite"],
) -> float:
    """Calculate the statistical power for a non-inferiority test of two independent means."""

    match dist:
        case "z":
            if equal_var:
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
                match approx_t_method:
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
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    margin: float,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Calculate the statistical power for a non-inferiority test of two independent means.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is not specified, this parameter must be specified along with `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is not specified, this parameter must be specified along with `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter must be specified.
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `greater` or `less`, you can alwanys specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `altarnative` is `greater`, the actual margin used internally is `-abs(margin)`.
            - If `altarnative` is `less`, the actual margin used internally is `abs(margin)`.
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        std:
            Standard deviation in both groups.

            This is a convenience parameter that will override `treatment_std` and `reference_std` when `dist` is `z` and `equal_var` is `True`.

            If you specify `dist` as `z` and `equal_var` as `True`, you can just specify `std` instead of `treatment_std` and `reference_std`.
            Internally, the value of `std` will be treated as the standard deviation of both the treatment and reference groups.
        treatment_size:
            Sample size for the treatment group.
        reference_size:
            Sample size for the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `altarnative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `altarnative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.
        equal_var:
            Whether to assume equal variances between treatment and reference groups.

            - `True`: Variances are assumed equal.
            - `False`: Variances are assumed unequal.

        approx_t_method:
            Approximate t-test method. It is used when `dist` is `'t'` and `equal_var` = `False`.

            - `'welch'`: Welch's approximate t-test (1947).
            - `'satterthwaite'`: Satterthwaite's approximate t-test (1946).

    Returns:
        float: The statistical power of the test.

    Raises:
        ValueError: If `diff` is not specified, and neither `treatment_mean` nor `reference_mean` is not specified.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and any of `treatment_std`, `reference_std` or `std` is not specified.
        ValueError: If `dist` is `z` and `equal_var` is `True` without specifying `std`: `treatment_std` and `reference_std` are not equal if both are provided.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)
    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    margin = _margin(margin, alternative)

    power = _power(
        diff=diff,
        margin=margin,
        treatment_std=treatment_std,
        reference_std=reference_std,
        std=std,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative=alternative,
        alpha=alpha,
        dist=dist,
        equal_var=equal_var,
        approx_t_method=approx_t_method,
    )
    return power


def solve_size(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    margin: float,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    ratio: float = 1,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> tuple[int, int]:
    """
    Estimate the required sample size for a non-inferiority test of two independent means.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is not specified, this parameter must be specified along with `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is not specified, this parameter must be specified along with `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter must be specified.
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `greater` or `less`, you can alwanys specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `altarnative` is `greater`, the actual margin used internally is `-abs(margin)`.
            - If `altarnative` is `less`, the actual margin used internally is `abs(margin)`.
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        std:
            Standard deviation in both groups.

            This is a convenience parameter that will override `treatment_std` and `reference_std` when `dist` is `z` and `equal_var` is `True`.

            If you specify `dist` as `z` and `equal_var` as `True`, you can just specify `std` instead of `treatment_std` and `reference_std`.
            Internally, the value of `std` will be treated as the standard deviation of both the treatment and reference groups.
        ratio:
            Ratio of sample size in the treatment and reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `altarnative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `altarnative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.
        equal_var:
            Whether to assume equal variances between treatment and reference groups.

            - `True`: Variances are assumed equal.
            - `False`: Variances are assumed unequal.
        approx_t_method:
            Approximate t-test method. It is used when `dist` is `'t'` and `equal_var` = `False`.

            - `'welch'`: Welch's approximate t-test (1947).
            - `'satterthwaite'`: Satterthwaite's approximate t-test (1946).

    Returns:
        tuple[int, int]: The required sample sizes for the treatment and reference groups, respectively.

    Raises:
        ValueError: If `diff` is not specified, and neither `treatment_mean` nor `reference_mean` is not specified.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and any of `treatment_std`, `reference_std` or `std` is not specified.
        ValueError: If `dist` is `z` and `equal_var` is `True` without specifying `std`: `treatment_std` and `reference_std` are not equal if both are provided.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)
    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    margin = _margin(margin, alternative)

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _power(
                    diff=diff,
                    margin=margin,
                    treatment_std=treatment_std,
                    reference_std=reference_std,
                    std=std,
                    treatment_size=reference_size * ratio,
                    reference_size=reference_size,
                    alternative=alternative,
                    alpha=alpha,
                    dist=dist,
                    equal_var=equal_var,
                    approx_t_method=approx_t_method,
                )
                - power
            )

        reference_size = int(ceil(brentq(func, 3 / (1 + ratio), 1e12)))
        treatment_size = int(ceil(reference_size * ratio))
        return treatment_size, reference_size
    else:

        def func(treatment_size: float) -> float:
            return (
                _power(
                    diff=diff,
                    margin=margin,
                    treatment_std=treatment_std,
                    reference_std=reference_std,
                    std=std,
                    treatment_size=treatment_size,
                    reference_size=treatment_size / ratio,
                    alternative=alternative,
                    alpha=alpha,
                    dist=dist,
                    equal_var=equal_var,
                    approx_t_method=approx_t_method,
                )
                - power
            )

        treatment_size = ceil(brentq(func, 3 / (1 + 1 / ratio), 1e12))
        reference_size = ceil(treatment_size / ratio)
        return treatment_size, reference_size


def solve_treatment_mean(
    *,
    reference_mean: float,
    margin: float,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required mean in the treatment group for a non-inferiority test of two independent means.

    Args:
        reference_mean:
            Mean in the reference group.
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `greater` or `less`, you can alwanys specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `altarnative` is `greater`, the actual margin used internally is `-abs(margin)`.
            - If `altarnative` is `less`, the actual margin used internally is `abs(margin)`.
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        std:
            Standard deviation in both groups.

            This is a convenience parameter that will override `treatment_std` and `reference_std` when `dist` is `z` and `equal_var` is `True`.

            If you specify `dist` as `z` and `equal_var` as `True`, you can just specify `std` instead of `treatment_std` and `reference_std`.
            Internally, the value of `std` will be treated as the standard deviation of both the treatment and reference groups.
        treatment_size:
            Sample size for the treatment group.
        reference_size:
            Sample size for the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `altarnative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `altarnative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.
        equal_var:
            Whether to assume equal variances between treatment and reference groups.

            - `True`: Variances are assumed equal.
            - `False`: Variances are assumed unequal.

        approx_t_method:
            Approximate t-test method. It is used when `dist` is `'t'` and `equal_var` = `False`.

            - `'welch'`: Welch's approximate t-test (1947).
            - `'satterthwaite'`: Satterthwaite's approximate t-test (1946).

    Returns:
        float: The required mean in the treatment group.

    Raises:
        ValueError: If `dist` is `z` and `equal_var` is `True`, and any of `treatment_std`, `reference_std` or `std` is not specified.
        ValueError: If `dist` is `z` and `equal_var` is `True` without specifying `std`: `treatment_std` and `reference_std` are not equal if both are provided.
    """

    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    margin = _margin(margin, alternative)

    def func(treatment_mean: float) -> float:
        return (
            _power(
                diff=treatment_mean - reference_mean,
                margin=margin,
                treatment_std=treatment_std,
                reference_std=reference_std,
                std=std,
                treatment_size=treatment_size,
                reference_size=reference_size,
                alternative=alternative,
                alpha=alpha,
                dist=dist,
                equal_var=equal_var,
                approx_t_method=approx_t_method,
            )
            - power
        )

    match alternative:
        case "greater":
            return float(brentq(func, reference_mean + margin, 1e9))
        case "less":
            return float(brentq(func, -1e9, reference_mean + margin))


def solve_reference_mean(
    *,
    treatment_mean: float,
    margin: float,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required mean in the reference group for a non-inferiority test of two independent means.

    Args:
        treatment_mean:
            Mean in the treatment group.
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `greater` or `less`, you can alwanys specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `altarnative` is `greater`, the actual margin used internally is `-abs(margin)`.
            - If `altarnative` is `less`, the actual margin used internally is `abs(margin)`.
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        std:
            Standard deviation in both groups.

            This is a convenience parameter that will override `treatment_std` and `reference_std` when `dist` is `z` and `equal_var` is `True`.

            If you specify `dist` as `z` and `equal_var` as `True`, you can just specify `std` instead of `treatment_std` and `reference_std`.
            Internally, the value of `std` will be treated as the standard deviation of both the treatment and reference groups.
        treatment_size:
            Sample size for the treatment group.
        reference_size:
            Sample size for the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `altarnative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `altarnative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.
        equal_var:
            Whether to assume equal variances between treatment and reference groups.

            - `True`: Variances are assumed equal.
            - `False`: Variances are assumed unequal.

        approx_t_method:
            Approximate t-test method. It is used when `dist` is `'t'` and `equal_var` = `False`.

            - `'welch'`: Welch's approximate t-test (1947).
            - `'satterthwaite'`: Satterthwaite's approximate t-test (1946).

    Returns:
        float: The required mean in the reference group.

    Raises:
        ValueError: If `dist` is `z` and `equal_var` is `True`, and any of `treatment_std`, `reference_std` or `std` is not specified.
        ValueError: If `dist` is `z` and `equal_var` is `True` without specifying `std`: `treatment_std` and `reference_std` are not equal if both are provided.
    """

    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    margin = _margin(margin, alternative)

    def func(reference_mean: float) -> float:
        return (
            _power(
                diff=treatment_mean - reference_mean,
                margin=margin,
                treatment_std=treatment_std,
                reference_std=reference_std,
                std=std,
                treatment_size=treatment_size,
                reference_size=reference_size,
                alternative=alternative,
                alpha=alpha,
                dist=dist,
                equal_var=equal_var,
                approx_t_method=approx_t_method,
            )
            - power
        )

    match alternative:
        case "greater":
            return float(brentq(func, -1e9, treatment_mean - margin))
        case "less":
            return float(brentq(func, treatment_mean - margin, 1e9))


def solve_diff(
    *,
    margin: float,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required difference between the mean in treatment and reference groups for a non-inferiority test of two independent means.

    Args:
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `greater` or `less`, you can alwanys specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `altarnative` is `greater`, the actual margin used internally is `-abs(margin)`.
            - If `altarnative` is `less`, the actual margin used internally is `abs(margin)`.
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        std:
            Standard deviation in both groups.

            This is a convenience parameter that will override `treatment_std` and `reference_std` when `dist` is `z` and `equal_var` is `True`.

            If you specify `dist` as `z` and `equal_var` as `True`, you can just specify `std` instead of `treatment_std` and `reference_std`.
            Internally, the value of `std` will be treated as the standard deviation of both the treatment and reference groups.
        treatment_size:
            Sample size for the treatment group.
        reference_size:
            Sample size for the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `altarnative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `altarnative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.
        equal_var:
            Whether to assume equal variances between treatment and reference groups.

            - `True`: Variances are assumed equal.
            - `False`: Variances are assumed unequal.

        approx_t_method:
            Approximate t-test method. It is used when `dist` is `'t'` and `equal_var` = `False`.

            - `'welch'`: Welch's approximate t-test (1947).
            - `'satterthwaite'`: Satterthwaite's approximate t-test (1946).

    Returns:
        float: The required difference between the mean in treatment and reference groups.

    Raises:
        ValueError: If `dist` is `z` and `equal_var` is `True`, and any of `treatment_std`, `reference_std` or `std` is not specified.
        ValueError: If `dist` is `z` and `equal_var` is `True` without specifying `std`: `treatment_std` and `reference_std` are not equal if both are provided.
    """

    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    margin = _margin(margin, alternative)

    def func(diff: float) -> float:
        return (
            _power(
                diff=diff,
                margin=margin,
                treatment_std=treatment_std,
                reference_std=reference_std,
                std=std,
                treatment_size=treatment_size,
                reference_size=reference_size,
                alternative=alternative,
                alpha=alpha,
                dist=dist,
                equal_var=equal_var,
                approx_t_method=approx_t_method,
            )
            - power
        )

    match alternative:
        case "greater":
            return float(brentq(func, margin, 1e9))
        case "less":
            return float(brentq(func, -1e9, margin))


def solve_margin(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required margin for a non-inferiority test of two independent means.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is not specified, this parameter must be specified along with `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is not specified, this parameter must be specified along with `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter must be specified.
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        std:
            Standard deviation in both groups.

            This is a convenience parameter that will override `treatment_std` and `reference_std` when `dist` is `z` and `equal_var` is `True`.

            If you specify `dist` as `z` and `equal_var` as `True`, you can just specify `std` instead of `treatment_std` and `reference_std`.
            Internally, the value of `std` will be treated as the standard deviation of both the treatment and reference groups.
        treatment_size:
            Sample size for the treatment group.
        reference_size:
            Sample size for the reference group.
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.
        equal_var:
            Whether to assume equal variances between treatment and reference groups.

            - `True`: Variances are assumed equal.
            - `False`: Variances are assumed unequal.

        approx_t_method:
            Approximate t-test method. It is used when `dist` is `'t'` and `equal_var` = `False`.

            - `'welch'`: Welch's approximate t-test (1947).
            - `'satterthwaite'`: Satterthwaite's approximate t-test (1946).

    Returns:
        float:
            The required non-inferiority margin for the test.

            - If `alternative` is `greater`, the returned value is in the range $(-\\infty, \\hat{\\mu}_1 - \\hat{\\mu}_2)$
            - If `alternative` is `less`, the returned value is in the range $(\\hat{\\mu}_1 - \\hat{\\mu}_2, +\\infty)$

    Raises:
        ValueError: If `diff` is not specified, and neither `treatment_mean` nor `reference_mean` is not specified.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and any of `treatment_std`, `reference_std` or `std` is not specified.
        ValueError: If `dist` is `z` and `equal_var` is `True` without specifying `std`: `treatment_std` and `reference_std` are not equal if both are provided.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)
    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    def func(margin: float) -> float:
        return (
            _power(
                diff=diff,
                margin=margin,
                treatment_std=treatment_std,
                reference_std=reference_std,
                std=std,
                treatment_size=treatment_size,
                reference_size=reference_size,
                alternative=alternative,
                alpha=alpha,
                dist=dist,
                equal_var=equal_var,
                approx_t_method=approx_t_method,
            )
            - power
        )

    match alternative:
        case "greater":
            return float(brentq(func, -1e9, diff))
        case "less":
            return float(brentq(func, diff, 1e9))


def solve_treatment_std(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    margin: float,
    reference_std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = True,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required standard deviation in the treatment group for a non-inferiority test of two independent means.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is not specified, this parameter must be specified along with `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is not specified, this parameter must be specified along with `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter must be specified.
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `greater` or `less`, you can alwanys specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `altarnative` is `greater`, the actual margin used internally is `-abs(margin)`.
            - If `altarnative` is `less`, the actual margin used internally is `abs(margin)`.
        reference_std:
            Standard deviation in the reference group.

            - If `dist` is `z` and `equal_var` is `True`, this parameter is ignored.
            - If `dist` is `z` and `equal_var` is `False`, this parameter is required.
            - If `dist` is `t` and `equal_var` is `True`, this parameter is optional. If specified, this value is used to calculate the standard error of mean difference.
            - If `dist` is `t` and `equal_var` is `False`, this parameter is required.
        treatment_size:
            Sample size for the treatment group.
        reference_size:
            Sample size for the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `altarnative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `altarnative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.
        equal_var:
            Whether to assume equal variances between treatment and reference groups.

            - `True`: Variances are assumed equal.
            - `False`: Variances are assumed unequal.

        approx_t_method:
            Approximate t-test method. It is used when `dist` is `'t'` and `equal_var` = `False`.

            - `'welch'`: Welch's approximate t-test (1947).
            - `'satterthwaite'`: Satterthwaite's approximate t-test (1946).

    Returns:
        float: The required standard deviation in the treatment group.

    Raises:
        ValueError: If `diff` is not specified, and neither `treatment_mean` nor `reference_mean` is not specified.
        ValueError: If `equal_var` is `False`, and `reference_std` is not specified.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)

    if not equal_var and reference_std is None:
        raise ValueError("'reference_std' must be specified when 'equal_var' = False.")

    margin = _margin(margin, alternative)

    if equal_var:
        match dist:
            case "z":

                def func(treatment_std: float) -> float:
                    return (
                        _power(
                            diff=diff,
                            margin=margin,
                            std=treatment_std,
                            treatment_size=treatment_size,
                            reference_size=reference_size,
                            alternative=alternative,
                            alpha=alpha,
                            dist=dist,
                            equal_var=equal_var,
                            approx_t_method=approx_t_method,
                        )
                        - power
                    )
            case "t":
                if reference_std is not None:

                    def func(treatment_std: float) -> float:
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
                                dist=dist,
                                equal_var=equal_var,
                                approx_t_method=approx_t_method,
                            )
                            - power
                        )
                else:

                    def func(treatment_std: float) -> float:
                        return (
                            _power(
                                diff=diff,
                                margin=margin,
                                treatment_std=treatment_std,
                                reference_std=treatment_std,
                                treatment_size=treatment_size,
                                reference_size=reference_size,
                                alternative=alternative,
                                alpha=alpha,
                                dist=dist,
                                equal_var=equal_var,
                                approx_t_method=approx_t_method,
                            )
                            - power
                        )
    else:  # equal_var == False

        def func(treatment_std: float) -> float:
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
                    dist=dist,
                    equal_var=equal_var,
                    approx_t_method=approx_t_method,
                )
                - power
            )

    return float(brentq(func, 1e-6, 1e6))


def solve_reference_std(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    margin: float,
    treatment_std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.80,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = True,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required standard deviation in the reference group for a non-inferiority test of two independent means.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is not specified, this parameter must be specified along with `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is not specified, this parameter must be specified along with `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter must be specified.
        margin:
            The non-inferiority margin.

            Regardless of whether `alternative` is specified as `greater` or `less`, you can alwanys specify this parameter to be positive or negative as you prefer.
            Internally, the value of `margin` will be converted before actual calculation.

            - If `altarnative` is `greater`, the actual margin used internally is `-abs(margin)`.
            - If `altarnative` is `less`, the actual margin used internally is `abs(margin)`.
        treatment_std:
            Standard deviation in the treatment group.

            - If `dist` is `z` and `equal_var` is `True`, this parameter is ignored.
            - If `dist` is `z` and `equal_var` is `False`, this parameter is required.
            - If `dist` is `t` and `equal_var` is `True`, this parameter is optional. If specified, this value is used to calculate the standard error of mean difference.
            - If `dist` is `t` and `equal_var` is `False`, this parameter is required.
        alternative:
            Type of the alternative hypothesis.

            - If `altarnative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `altarnative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, and 0.025 is a commonly used significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Standard normal distribution.
            - `'t'`: Student's or non-central t distribution.
        equal_var:
            Whether to assume equal variances between treatment and reference groups.

            - `True`: Variances are assumed equal.
            - `False`: Variances are assumed unequal.

        approx_t_method:
            Approximate t-test method. It is used when `dist` is `'t'` and `equal_var` = `False`.

            - `'welch'`: Welch's approximate t-test (1947).
            - `'satterthwaite'`: Satterthwaite's approximate t-test (1946).

    Returns:
        float: The required standard deviation in the reference group.

    Raises:
        ValueError: If `diff` is not specified, and neither `treatment_mean` nor `reference_mean` is not specified.
        ValueError: If `equal_var` is `False`, and `treatment_std` is not specified.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)

    if not equal_var and treatment_std is None:
        raise ValueError("'treatment_std' must be specified when 'equal_var' = False.")

    margin = _margin(margin, alternative)

    if equal_var:
        match dist:
            case "z":

                def func(reference_std: float) -> float:
                    return (
                        _power(
                            diff=diff,
                            margin=margin,
                            std=reference_std,
                            treatment_size=treatment_size,
                            reference_size=reference_size,
                            alternative=alternative,
                            alpha=alpha,
                            dist=dist,
                            equal_var=equal_var,
                            approx_t_method=approx_t_method,
                        )
                        - power
                    )
            case "t":
                if treatment_std is not None:

                    def func(reference_std: float) -> float:
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
                                dist=dist,
                                equal_var=equal_var,
                                approx_t_method=approx_t_method,
                            )
                            - power
                        )
                else:

                    def func(reference_std: float) -> float:
                        return (
                            _power(
                                diff=diff,
                                margin=margin,
                                treatment_std=reference_std,
                                reference_std=reference_std,
                                treatment_size=treatment_size,
                                reference_size=reference_size,
                                alternative=alternative,
                                alpha=alpha,
                                dist=dist,
                                equal_var=equal_var,
                                approx_t_method=approx_t_method,
                            )
                            - power
                        )

    else:  # equal_var == False

        def func(reference_std: float) -> float:
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
                    dist=dist,
                    equal_var=equal_var,
                    approx_t_method=approx_t_method,
                )
                - power
            )

    return float(brentq(func, 1e-6, 1e6))
