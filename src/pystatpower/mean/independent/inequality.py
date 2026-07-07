from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power as _raw_power
from ._verify import _verify_mean_and_get_diff, _verify_std_and_get_std


def _power(
    *,
    diff: float,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    dist: Literal["z", "t"],
    equal_var: bool,
    approx_t_method: Literal["welch", "satterthwaite"],
) -> float:

    return _raw_power(
        diff=diff,
        margin=0,
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


def solve_power(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Calculate the statistical power.

    Args:
        treatment_mean:
            Mean in the treatment group.

            If `diff` is omitted, this parameter is required alongside `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is omitted, this parameter is required alongside `treatment_mean`.
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

            - If `alternative` is `'two-sided'`, the alternative hypothesis $\\mu_1 \\neq \\mu_2$
            - If `alternative` is `'greater'`, the alternative hypothesis $\\mu_1 > \\mu_2$
            - If `alternative` is `'less'`, the alternative hypothesis $\\mu_1 < \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
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
        The calculated statistical power of the test.

    Raises:
        ValueError: If `diff` is omitted, and neither `treatment_mean` nor `reference_mean` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)
    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    return _power(
        diff=diff,
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


def solve_size(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    ratio: float = 1,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
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

            If `diff` is omitted, this parameter is required alongside `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is omitted, this parameter is required alongside `treatment_mean`.
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
        ratio:
            Ratio of sample sizes in the treatment and reference groups.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis $\\mu_1 \\neq \\mu_2$
            - If `alternative` is `'greater'`, the alternative hypothesis $\\mu_1 > \\mu_2$
            - If `alternative` is `'less'`, the alternative hypothesis $\\mu_1 < \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Desired statistical power.
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
        ValueError: If `diff` is omitted, and neither `treatment_mean` nor `reference_mean` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)
    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _power(
                    diff=diff,
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

        lb = max(1 + 0.1, 3 / (1 + ratio))
        ub = 1e12
        reference_size = ceil(brentq(func, lb, ub))
        treatment_size = ceil(reference_size * ratio)
        return treatment_size, reference_size
    else:

        def func(treatment_size: float) -> float:
            return (
                _power(
                    diff=diff,
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

        lb = max(1 + 0.1, 3 / (1 + 1 / ratio))
        ub = 1e12

        treatment_size = ceil(brentq(func, lb, ub))
        reference_size = ceil(treatment_size / ratio)
        return treatment_size, reference_size


def solve_diff(
    *,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimate the required mean difference.

    Args:
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

            - If `alternative` is `'two-sided'`, the alternative hypothesis $\\mu_1 \\neq \\mu_2$
            - If `alternative` is `'greater'`, the alternative hypothesis $\\mu_1 > \\mu_2$
            - If `alternative` is `'less'`, the alternative hypothesis $\\mu_1 < \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
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
        direction:
            The search direction for the mean difference relative to zero.

            - `'greater'`: Search for the mean difference that is greater than zero.
            - `'less'`: Search for the mean difference that is less than zero.

            !!! note
                - If `alternative` is `'two-sided'`, the parameter `direction` is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.

    Returns:
        The required difference between the treatment and reference means.

    Raises:
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
        ValueError: If `alternative` is `'two-sided'` but `direction` is omiited.
    """

    if alternative == "two-sided":
        if direction is None:
            raise ValueError("'direction' is required when 'alternative' is 'two-sided'.")
    elif alternative == "greater":
        direction = "greater"
    else:  # alternative == "less"
        direction = "less"

    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    def func(diff: float) -> float:
        return (
            _power(
                diff=diff,
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

    match direction:
        case "greater":
            return float(brentq(func, 0, 1e9))
        case "less":
            return float(brentq(func, -1e9, 0))


def solve_treatment_mean(
    *,
    reference_mean: float,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
    direction: Literal["greater", "less"] | None = None,
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

            - If `alternative` is `'two-sided'`, the alternative hypothesis $\\mu_1 \\neq \\mu_2$
            - If `alternative` is `'greater'`, the alternative hypothesis $\\mu_1 > \\mu_2$
            - If `alternative` is `'less'`, the alternative hypothesis $\\mu_1 < \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
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
        direction:
            The search direction for the treatment mean relative to the reference mean.

            - `'greater'`: Search for the treatment mean that is greater than the reference mean.
            - `'less'`: Search for the treatment mean that is less than the reference mean.

            !!! note
                - If `alternative` is `'two-sided'`, the parameter `direction` is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.

    Returns:
        The required mean in the treatment group.

    Raises:
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
        ValueError: If `alternative` is `'two-sided'` but `direction` is omiited.
    """

    if alternative == "two-sided":
        if direction is None:
            raise ValueError("'direction' is required when 'alternative' is 'two-sided'.")
    elif alternative == "greater":
        direction = "greater"
    else:  # alternative == "less"
        direction = "less"

    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    def func(treatment_mean: float) -> float:
        return (
            _power(
                diff=treatment_mean - reference_mean,
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

    match direction:
        case "greater":
            return float(brentq(func, reference_mean, 1e9))
        case "less":
            return float(brentq(func, -1e9, reference_mean))


def solve_reference_mean(
    *,
    treatment_mean: float,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    equal_var: bool = False,
    approx_t_method: Literal["welch", "satterthwaite"] = "welch",
    direction: Literal["greater", "less"] | None = None,
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

            - If `alternative` is `'two-sided'`, the alternative hypothesis $\\mu_1 \\neq \\mu_2$
            - If `alternative` is `'greater'`, the alternative hypothesis $\\mu_1 > \\mu_2$
            - If `alternative` is `'less'`, the alternative hypothesis $\\mu_1 < \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
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
        direction:
            The search direction for the reference mean relative to the treatment mean.

            - `'greater'`: Search for the reference mean that is greater than the treatment mean.
            - `'less'`: Search for the reference mean that is less than the treatment mean.

            !!! note
                - If `alternative` is `'two-sided'`, the parameter `direction` is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.

    Returns:
        The required mean in the treatment group.

    Raises:
        ValueError: If `dist` is `z` and `equal_var` is `True`, and all `treatment_std`, `reference_std` and `std` is omitted.
        ValueError: If `dist` is `z` and `equal_var` is `True`, and both `treatment_std` and `reference_std` are provided, but they are not equal.
        ValueError: If `alternative` is `'two-sided'` but `direction` is omiited.
    """

    if alternative == "two-sided":
        if direction is None:
            raise ValueError("'direction' is required when 'alternative' is 'two-sided'.")
    elif alternative == "greater":
        direction = "less"
    else:  # alternative == "less"
        direction = "greater"

    std = _verify_std_and_get_std(treatment_std, reference_std, std, dist, equal_var)

    def func(reference_mean: float) -> float:
        return (
            _power(
                diff=treatment_mean - reference_mean,
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

    match direction:
        case "greater":
            return float(brentq(func, treatment_mean, 1e9))
        case "less":
            return float(brentq(func, -1e9, treatment_mean))


def solve_treatment_std(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    reference_std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
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

            If `diff` is omitted, this parameter is required alongside `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is omitted, this parameter is required alongside `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter is required.
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

            - If `alternative` is `'two-sided'`, the alternative hypothesis $\\mu_1 \\neq \\mu_2$
            - If `alternative` is `'greater'`, the alternative hypothesis $\\mu_1 > \\mu_2$
            - If `alternative` is `'less'`, the alternative hypothesis $\\mu_1 < \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
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
        The required standard deviation in the treatment group.

    Raises:
        ValueError: If `diff` is omitted, and neither `treatment_mean` nor `reference_mean` is omitted.
        ValueError: If `equal_var` is `False`, and `reference_std` is omitted.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)

    if not equal_var and reference_std is None:
        raise ValueError("'reference_std' is required when 'equal_var' = False.")

    if equal_var:
        match dist:
            case "z":

                def func(treatment_std: float) -> float:
                    return (
                        _power(
                            diff=diff,
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
    treatment_std: float | None = None,
    treatment_size: int,
    reference_size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
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

            If `diff` is omitted, this parameter is required alongside `reference_mean`.
        reference_mean:
            Mean in the reference group.

            If `diff` is omitted, this parameter is required alongside `treatment_mean`.
        diff:
            Mean difference between treatment and reference group.

            If both `treatment_mean` and `reference_mean` are not specified, this parameter is required.
        treatment_std:
            Standard deviation in the treatment group.

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

            - If `alternative` is `'two-sided'`, the alternative hypothesis $\\mu_1 \\neq \\mu_2$
            - If `alternative` is `'greater'`, the alternative hypothesis $\\mu_1 > \\mu_2$
            - If `alternative` is `'less'`, the alternative hypothesis $\\mu_1 < \\mu_2$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
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
        The required standard deviation in the reference group.

    Raises:
        ValueError: If `diff` is omitted, and neither `treatment_mean` nor `reference_mean` is omitted.
        ValueError: If `equal_var` is `False`, and `treatment_std` is omitted.
    """

    diff = _verify_mean_and_get_diff(treatment_mean, reference_mean, diff)

    if not equal_var and treatment_std is None:
        raise ValueError("'treatment_std' is required when 'equal_var' = False.")

    if equal_var:
        match dist:
            case "z":

                def func(reference_std: float) -> float:
                    return (
                        _power(
                            diff=diff,
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
