import warnings

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


class _ParamsValidator:
    def __init__(
        self,
        *,
        mean: float | None = None,
        null_mean: float | None = None,
        margin: float | None = None,
        diff: float | None = None,
        superiority_mean: float | None = None,
        offset: float | None = None,
        alternative: Literal["greater", "less"] | None = None,
    ) -> None:
        self.mean = mean
        self.null_mean = null_mean
        self.margin = margin
        self.diff = diff
        self.superiority_mean = superiority_mean
        self.offset = offset
        self.alternative = alternative

        self.params_provided = {k for k, v in self.__dict__.items() if v is not None and k != "alternative"}

        if self.margin is not None and self.alternative is not None:
            self.margin = _margin(self.margin, self.alternative)

    def validate(self, target: Literal["diff", "superiority_mean", "offset"], *, warning: bool = True) -> None:
        match target:
            case "diff":
                self._validate_against_diff(warning=warning)
            case "superiority_mean":
                self._validate_against_superiority_mean(warning=warning)
            case "offset":
                self._validate_against_offset(warning=warning)

    def _validate_against_diff(self, *, warning: bool = True) -> None:
        if self.diff is not None:
            params_used = {"diff"}
        elif self.mean is not None and self.null_mean is not None:
            self.diff = self.mean - self.null_mean
            params_used = {"mean", "null_mean"}

        if self.diff is None:
            raise ValueError(
                "The mean difference cannot be calculated using the specified combination of parameters. Please provide the 'diff' parameter directly, or use both 'mean' and 'null_mean'."
            )

        if warning:
            params_redundant = self.params_provided - params_used
            if params_redundant:
                self._warn_params_redundant(params_redundant)

    def _validate_against_superiority_mean(self, *, warning: bool = True) -> None:
        if self.superiority_mean is not None:
            params_used = {"superiority_mean"}
        elif self.null_mean is not None and self.margin is not None:
            self.superiority_mean = self.null_mean + self.margin
            params_used = {"null_mean", "margin"}

        if self.superiority_mean is None:
            raise ValueError(
                "The superiority mean cannot be calculated using the specified combination of parameters. Please provide the 'superiority_mean' parameter directly, or use both 'null_mean' and 'margin'."
            )

        if warning:
            params_redundant = self.params_provided - params_used
            if params_redundant:
                self._warn_params_redundant(params_redundant)

    def _validate_against_offset(self, *, warning: bool = True) -> None:
        if self.offset is not None:
            params_used = {"offset"}
        elif self.mean is not None and self.superiority_mean is not None:
            self.offset = self.mean - self.superiority_mean
            params_used = {"mean", "superiority_mean"}
        elif self.diff is not None and self.margin is not None:
            self.offset = self.diff - self.margin
            params_used = {"diff", "margin"}
        elif self.mean is not None and self.null_mean is not None and self.margin is not None:
            self.offset = self.mean - self.null_mean - self.margin
            params_used = {"mean", "null_mean", "margin"}

        if self.offset is None:
            raise ValueError(
                "The offset cannot be calculated using the specified combination of parameters. Please provide the 'offset' parameter directly, or use one of the following parameter combinations:\n"
                "1. 'mean' and 'superiority_mean'\n"
                "2. 'diff' and 'margin'\n"
                "3. 'mean', 'null_mean' and 'margin'"
            )

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


def solve_power(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    margin: float | None = None,
    diff: float | None = None,
    superiority_mean: float | None = None,
    offset: float | None = None,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Calculate the statistical power.

    Args:
        mean:
            Mean under the alternative hypothesis.

            This parameter must be used together with `superiority_mean`, or alternatively, in conjunction with `null_mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `superiority_mean`, the `offset` is calculated as `mean` - `superiority_mean`.
            - If you specify this parameter along with `null_mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used together with `mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        margin:
            The superiority margin.

            This parameter must be used together with `diff`, or alternatively, in conjunction with `mean` and `null_mean` to calculate the `offset`.

            - If you specify this parameter along with `diff`, the `offset` is calculated as `diff` - `margin`.
            - If you specify this parameter along with `mean` and `null_mean`, the `offset` is calculated as `mean` - `null_mean` - `margin`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `-abs(margin)`.
        diff:
            Difference between the mean under the alternative hypothesis and the mean under the null hypothesis.

            This parameter must be used together with `margin` to calculate the `offset`.

            - If you specify this parameter along with `margin`, the `offset` if calculated as `diff` - `margin`.
        superiority_mean:
            The superiority mean.

            - If `alternative` is `'greater'`, the superiority mean is defined as the smallest mean that exceeds the
              null hypothesis mean and is considered superior.
            - If `alternative` is `'less'`, the superiority mean is defined as the largest mean that falls below the
              null hypothesis mean and is considered superior.

            This parameter must be used together with `mean` to calculate the `offset`.

            - If you specify this parameter along with `mean`, the `offset` if calculated as `mean` - `superiority_mean`.
        offset:
            The offset, defined as the difference between the mean under the alternative hypothesis and the superiority mean.

            If you specify this parameter, all of `mean`, `null_mean`, `margin`, `diff`, `superiority_mean` are ignored.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The statistical power of the test.

    Raises:
        ValueError: The given set of parameters is insufficient to determine the offset.
    """

    pv = _ParamsValidator(
        mean=mean,
        null_mean=null_mean,
        margin=margin,
        diff=diff,
        superiority_mean=superiority_mean,
        offset=offset,
        alternative=alternative,
    )
    pv.validate(target="offset")
    offset = pv.offset

    return _power(offset, std, size, alternative, alpha, dist)


def solve_size(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    margin: float | None = None,
    diff: float | None = None,
    superiority_mean: float | None = None,
    offset: float | None = None,
    std: float,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
) -> int:
    """
    Estimate the required sample size.

    Args:
        mean:
            Mean under the alternative hypothesis.

            This parameter must be used together with `superiority_mean`, or alternatively, in conjunction with `null_mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `superiority_mean`, the `offset` is calculated as `mean` - `superiority_mean`.
            - If you specify this parameter along with `null_mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used together with `mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        margin:
            The superiority margin.

            This parameter must be used together with `diff`, or alternatively, in conjunction with `mean` and `null_mean` to calculate the `offset`.

            - If you specify this parameter along with `diff`, the `offset` is calculated as `diff` - `margin`.
            - If you specify this parameter along with `mean` and `null_mean`, the `offset` is calculated as `mean` - `null_mean` - `margin`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `-abs(margin)`.
        diff:
            Difference between the mean under the alternative hypothesis and the mean under the null hypothesis.

            This parameter must be used together with `margin` to calculate the `offset`.

            - If you specify this parameter along with `margin`, the `offset` if calculated as `diff` - `margin`.
        superiority_mean:
            The superiority mean.

            - If `alternative` is `'greater'`, the superiority mean is defined as the smallest mean that exceeds the
              null hypothesis mean and is considered superior.
            - If `alternative` is `'less'`, the superiority mean is defined as the largest mean that falls below the
              null hypothesis mean and is considered superior.

            This parameter must be used together with `mean` to calculate the `offset`.

            - If you specify this parameter along with `mean`, the `offset` if calculated as `mean` - `superiority_mean`.
        offset:
            The offset, defined as the difference between the mean under the alternative hypothesis and the superiority mean.

            If you specify this parameter, all of `mean`, `null_mean`, `margin`, `diff`, `superiority_mean` are ignored.
        std:
            Standard deviation.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
        ValueError: The given set of parameters is insufficient to determine the offset.
    """

    pv = _ParamsValidator(
        mean=mean,
        null_mean=null_mean,
        margin=margin,
        diff=diff,
        superiority_mean=superiority_mean,
        offset=offset,
        alternative=alternative,
    )
    pv.validate(target="offset")
    offset = pv.offset

    def func(size: float) -> float:
        return _power(offset, std, size, alternative, alpha, dist) - power

    return ceil(brentq(func, 1 + 0.1, 1e12))


def solve_mean(
    *,
    null_mean: float | None = None,
    margin: float | None = None,
    superiority_mean: float | None = None,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Estimate the required mean under the alternative hypothesis.

    Args:
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used together with `margin` to calculate the `superiority_mean`

            - If you specify this parameter along with `margin`, the `superiority_mean` is calculated as `null_mean` + `margin`.
        margin:
            The superiority margin.

            This parameter must be used together with `null_mean` to calculate the `superiority_mean`

            - If you specify this parameter along with `null_mean`, the `superiority_mean` is calculated as `null_mean` + `margin`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `-abs(margin)`.
        superiority_mean:
            The superiority mean.

            - If `alternative` is `'greater'`, the superiority mean is defined as the smallest mean that exceeds the
              null hypothesis mean and is considered superior.
            - If `alternative` is `'less'`, the superiority mean is defined as the largest mean that falls below the
              null hypothesis mean and is considered superior.

            If you specify this parameter, both `null_mean` and `mean` are ignored.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required mean under the alternative hypothesis.

    Raises:
        ValueError: The given set of parameters is insufficient to determine the superiority mean.
    """

    pv = _ParamsValidator(
        null_mean=null_mean, margin=margin, superiority_mean=superiority_mean, alternative=alternative
    )
    pv.validate(target="superiority_mean")
    superiority_mean = pv.superiority_mean

    def func(mean: float) -> float:
        return _power(mean - superiority_mean, std, size, alternative, alpha, dist) - power

    match alternative:
        case "greater":
            return float(brentq(func, superiority_mean, 1e6))
        case "less":
            return float(brentq(func, -1e6, superiority_mean))


def solve_null_mean(
    *,
    mean: float,
    margin: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Estimate the required mean under the null hypothesis.

    Args:
        mean:
            Mean under the alternative hypothesis.
        margin:
            The superiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `-abs(margin)`.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required mean under the null hypothesis.
    """

    margin = _margin(margin, alternative)

    def func(null_mean: float) -> float:
        return _power(mean - null_mean - margin, std, size, alternative, alpha, dist) - power

    match alternative:
        case "greater":
            return float(brentq(func, -1e6, mean - margin))
        case "less":
            return float(brentq(func, mean - margin, 1e6))


def solve_margin(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    diff: float | None = None,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Estimate the required superiority margin.

    Args:
        mean:
            Mean under the alternative hypothesis.

            This parameter must be used together with `null_mean` to calculate the `diff`.

            - If you specify this parameter along with `null_mean`, the `diff` is calculated as `mean` - `null_mean`.
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used together with `mean` to calculate the `diff`.

            - If you specify this parameter along with `mean`, the `diff` is calculated as `mean` - `null_mean`.
        diff:
            Mean difference between the alternative hypothesis and the null hypothesis.

            If you specify this parameter, both `mean` and `null_mean` are ignored.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required superiority margin.

            - If `alternative` is `'greater'`, the returned value is in the range $(-\\infty, \\hat{\\mu} - \\hat{\\mu}_0)$
            - If `alternative` is `'less'`, the returned value is in the range $(\\hat{\\mu} - \\hat{\\mu}_0, +\\infty)$

    Raises:
        ValueError: The given set of parameters is insufficient to determine the mean difference.
    """

    pv = _ParamsValidator(mean=mean, null_mean=null_mean, diff=diff)
    pv.validate(target="diff")
    diff = pv.diff

    def func(margin: float) -> float:
        return _power(diff - margin, std, size, alternative, alpha, dist) - power

    match alternative:
        case "greater":
            return float(brentq(func, 0, diff))
        case "less":
            return float(brentq(func, diff, 0))


def solve_diff(
    *,
    margin: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Estimate the required mean difference.

    Args:
        margin:
            The superiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `-abs(margin)`.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required mean difference between the alternative hypothesis and the null hypothesis.
    """

    margin = _margin(margin, alternative)

    def func(diff: float) -> float:
        return _power(diff - margin, std, size, alternative, alpha, dist) - power

    match alternative:
        case "greater":
            return float(brentq(func, margin, 1e8))
        case "less":
            return float(brentq(func, -1e8, margin))


def solve_superiority_mean(
    *,
    mean: float,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Estimate the required superiority mean.

    - If `alternative` is `'greater'`, the superiority mean is defined as the smallest mean that exceeds the
      null hypothesis mean and is considered superior.
    - If `alternative` is `'less'`, the superiority mean is defined as the largest mean that falls below the
      null hypothesis mean and is considered superior.

    Args:
        mean:
            Mean under the alternative hypothesis.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required superiority mean.
    """

    def func(superiority_mean: float) -> float:
        return _power(mean - superiority_mean, std, size, alternative, alpha, dist) - power

    match alternative:
        case "greater":
            return float(brentq(func, -1e9, mean))
        case "less":
            return float(brentq(func, mean, 1e9))


def solve_offset(
    *,
    std: float,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Estimate the required offset.

    The offset is defined as the difference between the mean under the alternative hypothesis and the superiority mean.

    Args:
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required offset.
    """

    def func(offset: float) -> float:
        return _power(offset, std, size, alternative, alpha, dist) - power

    return float(brentq(func, -1e9, 1e9))


def solve_std(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    margin: float | None = None,
    diff: float | None = None,
    superiority_mean: float | None = None,
    offset: float | None = None,
    size: int,
    alternative: Literal["greater", "less"],
    alpha: float = 0.025,
    power: float = 0.8,
    dist: Literal["z", "t"] = "t",
) -> float:
    """
    Estimate the required standard deviation.

    Args:
        mean:
            Mean under the alternative hypothesis.

            This parameter must be used together with `superiority_mean`, or alternatively, in conjunction with `null_mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `superiority_mean`, the `offset` is calculated as `mean` - `superiority_mean`.
            - If you specify this parameter along with `null_mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used together with `mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        margin:
            The superiority margin.

            This parameter must be used together with `diff`, or alternatively, in conjunction with `mean` and `null_mean` to calculate the `offset`.

            - If you specify this parameter along with `diff`, the `offset` is calculated as `diff` - `margin`.
            - If you specify this parameter along with `mean` and `null_mean`, the `offset` is calculated as `mean` - `null_mean` - `margin`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `-abs(margin)`.
        diff:
            Difference between the mean under the alternative hypothesis and the mean under the null hypothesis.

            This parameter must be used together with `margin` to calculate the `offset`.

            - If you specify this parameter along with `margin`, the `offset` if calculated as `diff` - `margin`.
        superiority_mean:
            The superiority mean.

            - If `alternative` is `'greater'`, the superiority mean is defined as the smallest mean that exceeds the
              null hypothesis mean and is considered superior.
            - If `alternative` is `'less'`, the superiority mean is defined as the largest mean that falls below the
              null hypothesis mean and is considered superior.

            This parameter must be used together with `mean` to calculate the `offset`.

            - If you specify this parameter along with `mean`, the `offset` if calculated as `mean` - `superiority_mean`.
        offset:
            The offset, defined as the difference between the mean under the alternative hypothesis and the superiority mean.

            If you specify this parameter, all of `mean`, `null_mean`, `margin`, `diff`, `superiority_mean` are ignored.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta > 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta < 0)$
        alpha:
            Significance level.

            The superiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
        ValueError: The given set of parameters is insufficient to determine the offset.
    """

    pv = _ParamsValidator(
        mean=mean,
        null_mean=null_mean,
        margin=margin,
        diff=diff,
        superiority_mean=superiority_mean,
        offset=offset,
        alternative=alternative,
    )
    pv.validate(target="offset")
    offset = pv.offset

    def func(std: float) -> float:
        return _power(offset, std, size, alternative, alpha, dist) - power

    return float(brentq(func, 1e-6, 1e12))
