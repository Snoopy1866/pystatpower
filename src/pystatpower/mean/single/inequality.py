import warnings

from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power as _raw_power


class _ParamsValidator:
    def __init__(
        self,
        *,
        mean: float | None = None,
        null_mean: float | None = None,
        diff: float | None = None,
    ) -> None:
        self.mean = mean
        self.null_mean = null_mean
        self.diff = diff

        self.params_provided = {k for k, v in self.__dict__.items() if v is not None and k != "alternative"}

    def validate(self, target: Literal["diff"], *, warning: bool = True) -> None:
        match target:
            case "diff":
                self._validate_against_diff(warning=warning)

    def _validate_against_diff(self, *, warning: bool = True) -> None:
        if self.diff is not None:
            params_used = {"diff"}
        elif self.mean is not None and self.null_mean is not None:
            self.diff = self.mean - self.null_mean
            params_used = {"mean", "null_mean"}

        if self.diff is None:
            msg = "The mean difference cannot be calculated using the specified combination of parameters. Please provide the 'diff' parameter directly, or use both 'mean' and 'null_mean'."
            raise ValueError(msg)

        if warning:
            params_redundant = self.params_provided - params_used
            if params_redundant:
                self._warn_params_redundant(params_redundant)

    def _warn_params_redundant(self, params: set[str], /) -> None:
        """Warn if parameters are redundant."""

        params_str = ", ".join(params)
        warnings.warn(
            f"Redundant parameters detected: {params_str}.",
            stacklevel=2,
        )


def _power(
    diff: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    dist: Literal["z", "t"],
) -> float:
    """Calculate the statistical power."""

    return _raw_power(diff, std, size, alternative, alpha, dist)


def solve_power(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    diff: float | None = None,
    std: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Calculate the statistical power.

    Args:
        mean:
            Mean under the alternative hypothesis.

            This parameter must be used in conjuction with `null_mean` to compute the `diff`, where `diff` = `mean` - `null_mean`.
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used in conjuction with `mean` to compute the `diff`, where `diff` = `mean` - `null_mean`.
        diff:
            Mean difference between the alternative hypothesis and the null hypothesis.

            If this parameter is specified, both `mean` and `null_mean` are ignored.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The statistical power of the test.

    Raises:
        ValueError: The given set of parameters is insufficient to determine the mean difference.
    """

    pv = _ParamsValidator(mean=mean, null_mean=null_mean, diff=diff)
    pv.validate(target="diff")
    diff = pv.diff

    return _power(diff, std, size, alternative, alpha, dist)


def solve_size(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    diff: float | None = None,
    std: float,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
) -> int:
    """
    Estimate the required sample size.

    Args:
        mean:
            Mean under the alternative hypothesis.

            This parameter must be used in conjuction with `null_mean` to compute the `diff`, where `diff` = `mean` - `null_mean`.
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used in conjuction with `mean` to compute the `diff`, where `diff` = `mean` - `null_mean`.
        diff:
            Mean difference between the alternative hypothesis and the null hypothesis.

            If this parameter is specified, both `mean` and `null_mean` are ignored.
        std:
            Standard deviation.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required sample size.

    Raises:
        ValueError: The given set of parameters is insufficient to determine the mean difference.
    """

    pv = _ParamsValidator(mean=mean, null_mean=null_mean, diff=diff)
    pv.validate(target="diff")
    diff = pv.diff

    def func(size: float) -> float:
        return _power(diff, std, size, alternative, alpha, dist) - power

    return ceil(brentq(func, 1 + 0.1, 1e12))


def solve_mean(
    *,
    null_mean: float,
    std: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimate the required mean under the alternative hypothesis.

    Args:
        null_mean:
            Mean under the null hypothesis.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.
        direction:
            The search direction for the mean under the alternative hypothesis relative to the mean under the null hypothesis.

            - `'greater'`: Search for the alternative mean that is greater than the null mean.
            - `'less'`: Search for the alternative mean that is less than the null mean.

            !!! note
                - If `alternative` is `'two-sided'`, the parameter `direction` is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.

    Returns:
        The required mean under the alternative hypothesis.

    Raises:
        ValueError: If `alternative` is `'two-sided'` and `direction` is omitted.
    """

    if alternative == "two-sided":
        if direction is None:
            msg = "'direction' is required when 'alternative' is 'two-sided'."
            raise ValueError(msg)
    elif alternative == "greater":
        direction = "greater"
    else:  # alternative == "less"
        direction = "less"

    def func(mean: float) -> float:
        return _power(mean - null_mean, std, size, alternative, alpha, dist) - power

    match direction:
        case "greater":
            return float(brentq(func, null_mean, 1e9))
        case "less":
            return float(brentq(func, -1e9, null_mean))


def solve_null_mean(
    *,
    mean: float,
    std: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimate the required mean under the null hypothesis.

    Args:
        mean:
            Mean under the alternative hypothesis.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.
        direction:
            The search direction for the mean under the null hypothesis relative to the mean under the alternative hypothesis.

            - `'greater'`: Search for the null mean that is greater than the alternative mean.
            - `'less'`: Search for the null mean that is less than the alternative mean.

            !!! note
                - If `alternative` is `'two-sided'`, the parameter `direction` is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.

    Returns:
        The required mean under the null hypothesis.

    Raises:
        ValueError: If `alternative` is `'two-sided'` and `direction` is omitted.
    """

    if alternative == "two-sided":
        if direction is None:
            msg = "'direction' is required when 'alternative' is 'two-sided'."
            raise ValueError(msg)
    elif alternative == "greater":
        direction = "less"
    else:  # alternative == "less"
        direction = "greater"

    def func(null_mean: float) -> float:
        return _power(mean - null_mean, std, size, alternative, alpha, dist) - power

    match direction:
        case "greater":
            return float(brentq(func, mean, 1e9))
        case "less":
            return float(brentq(func, -1e9, mean))


def solve_diff(
    *,
    std: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimate the required mean difference.

    Args:
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.
        direction:
            The search direction for the mean difference relative to zero.

            - `'greater'`: Search for the mean difference that is greater than zero.
            - `'less'`: Search for the mean difference that is less than zero.

            !!! note
                - If `alternative` is `'two-sided'`, the parameter `direction` is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'greater'`, and the parameter `direction` is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'less'`, and the parameter `direction` is ignored.

    Returns:
        The required mean difference between the alternative hypothesis and the null hypothesis.

    Raises:
        ValueError: If `alternative` is `'two-sided'` and `direction` is omitted.
    """

    if alternative == "two-sided":
        if direction is None:
            msg = "'direction' is required when 'alternative' is 'two-sided'."
            raise ValueError(msg)
    elif alternative == "greater":
        direction = "greater"
    else:  # alternative == "less"
        direction = "less"

    def func(diff: float) -> float:
        return _power(diff, std, size, alternative, alpha, dist) - power

    match direction:
        case "greater":
            return float(brentq(func, 0, 1e9))
        case "less":
            return float(brentq(func, -1e9, 0))


def solve_std(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    diff: float | None = None,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Estimate the required standard deviation.

    Args:
        mean:
            Mean under the alternative hypothesis.

            This parameter must be used in conjuction with `null_mean` to compute the `diff`, where `diff` = `mean` - `null_mean`.
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used in conjuction with `mean` to compute the `diff`, where `diff` = `mean` - `null_mean`.
        diff:
            Mean difference between the alternative hypothesis and the null hypothesis.

            If this parameter is specified, both `mean` and `null_mean` are ignored.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\mu \\neq \\mu_0$
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu > \\mu_0$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu < \\mu_0$
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required standard deviation.

    Raises:
        ValueError: The given set of parameters is insufficient to determine the mean difference.
    """

    pv = _ParamsValidator(mean=mean, null_mean=null_mean, diff=diff)
    pv.validate(target="diff")
    diff = pv.diff

    def func(std: float) -> float:
        return _power(diff, std, size, alternative, alpha, dist) - power

    return float(brentq(func, 1e-6, 1e12))
