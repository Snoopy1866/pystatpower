from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power
from ._verify import _verify_mean_and_get_diff, _verify_std_and_get_std


def _margin(margin: float, alternative: Literal["greater", "less"]) -> float:
    """Convert margin to standard form based on alternative hypothesis"""

    match alternative:
        case "greater":
            return -abs(margin)
        case "less":
            return abs(margin)


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
    Calculate the statistical power.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is omitted, this parameter is required along with `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is omitted, this parameter is required along with `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter is required.
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `greater`, the actual margin used internally is `-abs(margin)`.
                - If `alternative` is `less`, the actual margin used internally is `abs(margin)`.
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
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `alternative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
        The statistical power of the test.

    Raises:
        ValueError: If all of `diff`, `treatment_mean` and `reference_mean` are omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
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
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> tuple[int, int]:
    """
    Estimate the required sample size.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is omitted, this parameter is required along with `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is omitted, this parameter is required along with `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter is required.
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `greater`, the actual margin used internally is `-abs(margin)`.
                - If `alternative` is `less`, the actual margin used internally is `abs(margin)`.
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
            Ratio of sample sizes in the treatment and reference groups.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `alternative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
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
        The required sample sizes in the treatment and reference groups, respectively.

    Raises:
        ValueError: If all of `diff`, `treatment_mean` and `reference_mean` are omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
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

        lb = max(1 + 1e-12, 3 / (1 + ratio))
        ub = 1e12
        reference_size = int(ceil(brentq(func, lb, ub)))
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

        lb = max(1 + 1e-12, 3 / (1 + 1 / ratio))
        ub = 1e12
        treatment_size = ceil(brentq(func, lb, ub))
        reference_size = ceil(treatment_size / ratio)
        return treatment_size, reference_size


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
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required mean difference.

    Args:
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `greater`, the actual margin used internally is `-abs(margin)`.
                - If `alternative` is `less`, the actual margin used internally is `abs(margin)`.
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
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `alternative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
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
        The required difference between the mean in treatment and reference groups.

    Raises:
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
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
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required mean in the treatment group.

    Args:
        reference_mean:
            Mean in the reference group.
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `greater`, the actual margin used internally is `-abs(margin)`.
                - If `alternative` is `less`, the actual margin used internally is `abs(margin)`.
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
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `alternative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
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
        The required mean in the treatment group.

    Raises:
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
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
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required mean in the reference group.

    Args:
        treatment_mean:
            Mean in the treatment group.
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `greater`, the actual margin used internally is `-abs(margin)`.
                - If `alternative` is `less`, the actual margin used internally is `abs(margin)`.
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
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `alternative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
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
        The required mean in the reference group.

    Raises:
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
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
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required non-inferiority margin.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is omitted, this parameter is required along with `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is omitted, this parameter is required along with `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter is required.
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
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `alternative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
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
        The required non-inferiority margin for the test.

            - If `alternative` is `greater`, the returned value is in the range $(-\\infty, \\hat{\\mu}_1 - \\hat{\\mu}_2)$
            - If `alternative` is `less`, the returned value is in the range $(\\hat{\\mu}_1 - \\hat{\\mu}_2, +\\infty)$

    Raises:
        ValueError: If all of `diff`, `treatment_mean` and `reference_mean` are omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
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
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = True,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required standard deviation in the treatment group.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is omitted, this parameter is required along with `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is omitted, this parameter is required along with `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter is required.
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `greater`, the actual margin used internally is `-abs(margin)`.
                - If `alternative` is `less`, the actual margin used internally is `abs(margin)`.
        reference_std:
            Standard deviation in the reference group.

            - If `dist` is `z` and `equal_var` is `True`, this parameter is ignored.
            - If `dist` is `z` and `equal_var` is `False`, this parameter is required.
            - If `dist` is `t` and `equal_var` is `True`, this parameter is optional. If specified, this value is used to calculate the standard error of mean difference.
            - If `dist` is `t` and `equal_var` is `False`, this parameter is required.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `alternative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
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
        The required standard deviation in the treatment group.

    Raises:
        ValueError: If all of `diff`, `treatment_mean` and `reference_mean` are omitted.
        ValueError: If `equal_var` is `False`, and `reference_std` is omitted.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)

    if not equal_var and reference_std is None:
        raise ValueError("'reference_std' is required when 'equal_var' = False.")

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
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = True,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Estimate the required standard deviation in the reference group.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is omitted, this parameter is required along with `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is omitted, this parameter is required along with `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter is required.
        margin:
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `greater`, the actual margin used internally is `-abs(margin)`.
                - If `alternative` is `less`, the actual margin used internally is `abs(margin)`.
        treatment_std:
            Standard deviation in the treatment group.

            - If `dist` is `z` and `equal_var` is `True`, this parameter is ignored.
            - If `dist` is `z` and `equal_var` is `False`, this parameter is required.
            - If `dist` is `t` and `equal_var` is `True`, this parameter is optional. If specified, this value is used to calculate the standard error of mean difference.
            - If `dist` is `t` and `equal_var` is `False`, this parameter is required.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `greater`, the alternative hypothesis is $\\mu_1 - \\mu_2 > \\delta$ ($\\delta < 0$)
            - If `alternative` is `less`, the alternative hypothesis is $\\mu_1 - \\mu_2 < \\delta$ ($\\delta > 0$)
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
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
        The required standard deviation in the reference group.

    Raises:
        ValueError: If all of `diff`, `treatment_mean` and `reference_mean` are omitted.
        ValueError: If `equal_var` is `False`, and `treatment_std` is omitted.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)

    if not equal_var and treatment_std is None:
        raise ValueError("'treatment_std' is required when 'equal_var' = False.")

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
