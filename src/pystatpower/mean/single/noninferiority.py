import warnings

from math import ceil
from typing import Literal

from scipy.optimize import brentq

from ._power import _power


def _margin(margin: float, alternative: Literal["greater", "less"]) -> float:
    """Convert the margin to its standard form according to the alternative hypothesis"""

    match alternative:
        case "greater":
            return -abs(margin)
        case "less":
            return abs(margin)


class _ParamsValidator:
    def __init__(
        self,
        *,
        mean: float | None = None,
        null_mean: float | None = None,
        margin: float | None = None,
        diff: float | None = None,
        noninferiority_mean: float | None = None,
        offset: float | None = None,
    ) -> None:
        self.mean = mean
        self.null_mean = null_mean
        self.margin = margin
        self.diff = diff
        self.noninferiority_mean = noninferiority_mean
        self.offset = offset

        self.params_provided = {k for k, v in self.__dict__.items() if v is not None}

    def validate(self, target: Literal["diff", "noninferiority_mean", "offset"], *, warning: bool = True) -> None:
        match target:
            case "diff":
                self._validate_against_diff(warning=warning)
            case "noninferiority_mean":
                self._validate_against_noninferiority_mean(warning=warning)
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

    def _validate_against_noninferiority_mean(self, *, warning: bool = True) -> None:
        if self.noninferiority_mean is not None:
            params_used = {"noninferiority_mean"}
        elif self.null_mean is not None and self.margin is not None:
            self.noninferiority_mean = self.null_mean + self.margin
            params_used = {"null_mean", "margin"}

        if self.noninferiority_mean is None:
            raise ValueError(
                "The non-inferiority mean cannot be calculated using the specified combination of parameters. Please provide the 'noninferiority_mean' parameter directly, or use both 'null_mean' and 'margin'."
            )

        if warning:
            params_redundant = self.params_provided - params_used
            if params_redundant:
                self._warn_params_redundant(params_redundant)

    def _validate_against_offset(self, *, warning: bool = True) -> None:
        if self.offset is not None:
            params_used = {"offset"}
        elif self.mean is not None and self.noninferiority_mean is not None:
            self.offset = self.mean - self.noninferiority_mean
            params_used = {"mean", "noninferiority_mean"}
        elif self.diff is not None and self.margin is not None:
            self.offset = self.diff - self.margin
            params_used = {"diff", "margin"}
        elif self.mean is not None and self.null_mean is not None and self.margin is not None:
            self.offset = self.mean - self.null_mean - self.margin
            params_used = {"mean", "null_mean", "margin"}

        if self.offset is None:
            raise ValueError(
                "The offset cannot be calculated using the specified combination of parameters. Please provide the 'offset' parameter directly, or use one of the following parameter combinations:\n"
                "1. 'mean' and 'noninferiority_mean'\n"
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
            UserWarning,
            stacklevel=2,
        )


def solve_power(
    *,
    mean: float | None = None,
    null_mean: float | None = None,
    margin: float | None = None,
    diff: float | None = None,
    noninferiority_mean: float | None = None,
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

            This parameter must be used together with `noninferiority_mean`, or alternatively, in conjunction with `null_mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `noninferiority_mean`, the `offset` is calculated as `mean` - `noninferiority_mean`.
            - If you specify this parameter along with `null_mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used together with `mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        margin:
            The non-inferiority margin.

            This parameter must be used together with `diff`, or alternatively, in conjunction with `mean` and `null_mean` to calculate the `offset`.

            - If you specify this parameter along with `diff`, the `offset` is calculated as `diff` - `margin`.
            - If you specify this parameter along with `mean` and `null_mean`, the `offset` is calculated as `mean` - `null_mean` - `margin`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        diff:
            Difference between the mean under the alternative hypothesis and the null hypothesis.

            This parameter must be used together with `margin` to calculate the `offset`.

            - If you specify this parameter along with `margin`, the `offset` if calculated as `diff` - `margin`.
        noninferiority_mean:
            The non-inferiority mean.

            - If `alternative` is `'greater'`, the non-inferiority mean is defined as the smallest mean that is less
              than the null hypothesis mean yet still considered non-inferior.
            - If `alternative` is `'less'`, the non-inferiority mean is defined as the largest mean that is greater than
              the null hypothesis mean yet still considered non-inferior.

            This parameter must be used together with `mean` to calculate the `offset`.

            - If you specify this parameter along with `mean`, the `offset` if calculated as `mean` - `noninferiority_mean`.
        offset:
            The offset, defined as the difference between the mean under the alternative hypothesis and the non-inferiority mean.

            If you specify this parameter, all of `mean`, `null_mean`, `margin`, `diff`, `noninferiority_mean` are ignored.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The statistical power of the test.

    Raises:
        ValueError: The given set of parameters is insufficient to determine the offset.
    """

    margin = _margin(margin, alternative)

    pv = _ParamsValidator(
        mean=mean, null_mean=null_mean, margin=margin, diff=diff, noninferiority_mean=noninferiority_mean, offset=offset
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
    noninferiority_mean: float | None = None,
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

            This parameter must be used together with `noninferiority_mean`, or alternatively, in conjunction with `null_mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `noninferiority_mean`, the `offset` is calculated as `mean` - `noninferiority_mean`.
            - If you specify this parameter along with `null_mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used together with `mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        margin:
            The non-inferiority margin.

            This parameter must be used together with `diff`, or alternatively, in conjunction with `mean` and `null_mean` to calculate the `offset`.

            - If you specify this parameter along with `diff`, the `offset` is calculated as `diff` - `margin`.
            - If you specify this parameter along with `mean` and `null_mean`, the `offset` is calculated as `mean` - `null_mean` - `margin`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        diff:
            Difference between the mean under the alternative hypothesis and the null hypothesis.

            This parameter must be used together with `margin` to calculate the `offset`.

            - If you specify this parameter along with `margin`, the `offset` if calculated as `diff` - `margin`.
        noninferiority_mean:
            The non-inferiority mean.

            - If `alternative` is `'greater'`, the non-inferiority mean is defined as the smallest mean that is less
              than the null hypothesis mean yet still considered non-inferior.
            - If `alternative` is `'less'`, the non-inferiority mean is defined as the largest mean that is greater than
              the null hypothesis mean yet still considered non-inferior.

            This parameter must be used together with `mean` to calculate the `offset`.

            - If you specify this parameter along with `mean`, the `offset` if calculated as `mean` - `noninferiority_mean`.
        offset:
            The offset, defined as the difference between the mean under the alternative hypothesis and the non-inferiority mean.

            If you specify this parameter, all of `mean`, `null_mean`, `margin`, `diff`, `noninferiority_mean` are ignored.
        std:
            Standard deviation.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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

    margin = _margin(margin, alternative)

    pv = _ParamsValidator(
        mean=mean, null_mean=null_mean, margin=margin, diff=diff, noninferiority_mean=noninferiority_mean, offset=offset
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
    noninferiority_mean: float | None = None,
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

            This parameter must be used together with `margin` to calculate the `noninferiority_mean`

            - If you specify this parameter along with `margin`, the `noninferiority_mean` is calculated as `null_mean` + `margin`.
        margin:
            The non-inferiority margin.

            This parameter must be used together with `null_mean` to calculate the `noninferiority_mean`

            - If you specify this parameter along with `null_mean`, the `noninferiority_mean` is calculated as `null_mean` + `margin`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        noninferiority_mean:
            The non-inferiority mean.

            - If `alternative` is `'greater'`, the non-inferiority mean is defined as the smallest mean that is less
              than the null hypothesis mean yet still considered non-inferior.
            - If `alternative` is `'less'`, the non-inferiority mean is defined as the largest mean that is greater than
              the null hypothesis mean yet still considered non-inferior.

            If you specify this parameter, both `null_mean` and `mean` are ignored.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
        ValueError: The given set of parameters is insufficient to determine the noninferiority mean.
    """

    margin = _margin(margin, alternative)

    pv = _ParamsValidator(null_mean=null_mean, margin=margin, noninferiority_mean=noninferiority_mean)
    pv.validate(target="noninferiority_mean")
    noninferiority_mean = pv.noninferiority_mean

    def func(mean: float) -> float:
        return _power(mean - noninferiority_mean, std, size, alternative, alpha, dist) - power

    match alternative:
        case "greater":
            return float(brentq(func, noninferiority_mean, 1e6))
        case "less":
            return float(brentq(func, -1e6, noninferiority_mean))


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
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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
    Estimate the required non-inferiority margin.

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

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required non-inferiority margin.

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
            return float(brentq(func, -1e6, diff))
        case "less":
            return float(brentq(func, diff, 1e6))


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
            The non-inferiority margin.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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


def solve_noninferiority_mean(
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
    Estimate the required non-inferiority mean.

    - If `alternative` is `'greater'`, the non-inferiority mean is defined as the smallest mean that is less than the
      null hypothesis mean yet still considered non-inferior.
    - If `alternative` is `'less'`, the non-inferiority mean is defined as the largest mean that is greater than the
      null hypothesis mean yet still considered non-inferior.

    Args:
        mean:
            Mean under the alternative hypothesis.
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required non-inferiority mean.
    """

    def func(noninferiority_mean: float) -> float:
        return _power(mean - noninferiority_mean, std, size, alternative, alpha, dist) - power

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

    The offset is defined as the difference between the mean under the alternative hypothesis and the non-inferiority mean.

    Args:
        std:
            Standard deviation.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
        power:
            Expected statistical power.

            0.8 is a commonly used value for statistical power.
        dist:
            The distribution used for the test.

            - `'z'`: Normal distribution.
            - `'t'`: Student's t distribution.

    Returns:
        The required non-inferiority mean.
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
    noninferiority_mean: float | None = None,
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

            This parameter must be used together with `noninferiority_mean`, or alternatively, in conjunction with `null_mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `noninferiority_mean`, the `offset` is calculated as `mean` - `noninferiority_mean`.
            - If you specify this parameter along with `null_mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        null_mean:
            Mean under the null hypothesis.

            This parameter must be used together with `mean` and `margin` to calculate the `offset`.

            - If you specify this parameter along with `mean` and `margin`, the `offset` is calculated as `mean` - `null_mean` - `margin`.
        margin:
            The non-inferiority margin.

            This parameter must be used together with `diff`, or alternatively, in conjunction with `mean` and `null_mean` to calculate the `offset`.

            - If you specify this parameter along with `diff`, the `offset` is calculated as `diff` - `margin`.
            - If you specify this parameter along with `mean` and `null_mean`, the `offset` is calculated as `mean` - `null_mean` - `margin`.

            !!! tip

                Regardless of whether `alternative` is specified as `'greater'` or `'less'`, you can always specify this
                parameter as either positive or negative, as you prefer. Internally, the value of `margin` is converted
                before actual calculation takes place.

                - If `alternative` is `'greater'`, the internally used margin is `-abs(margin)`.
                - If `alternative` is `'less'`, the internally used margin is `abs(margin)`.
        diff:
            Difference between the mean under the alternative hypothesis and the null hypothesis.

            This parameter must be used together with `margin` to calculate the `offset`.

            - If you specify this parameter along with `margin`, the `offset` if calculated as `diff` - `margin`.
        noninferiority_mean:
            The non-inferiority mean.

            - If `alternative` is `'greater'`, the non-inferiority mean is defined as the smallest mean that is less
              than the null hypothesis mean yet still considered non-inferior.
            - If `alternative` is `'less'`, the non-inferiority mean is defined as the largest mean that is greater than
              the null hypothesis mean yet still considered non-inferior.

            This parameter must be used together with `mean` to calculate the `offset`.

            - If you specify this parameter along with `mean`, the `offset` if calculated as `mean` - `noninferiority_mean`.
        offset:
            The offset, defined as the difference between the mean under the alternative hypothesis and the non-inferiority mean.

            If you specify this parameter, all of `mean`, `null_mean`, `margin`, `diff`, `noninferiority_mean` are ignored.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'greater'`, the alternative hypothesis is $\\mu - \\mu_0 > \\delta \\ (\\delta < 0)$
            - If `alternative` is `'less'`, the alternative hypothesis is $\\mu - \\mu_0 < \\delta \\ (\\delta > 0)$
        alpha:
            Significance level.

            The non-inferiority test is a one-sided test, with a significance level of 0.025 being commonly used.
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

    margin = _margin(margin, alternative)

    pv = _ParamsValidator(
        mean=mean, null_mean=null_mean, margin=margin, diff=diff, noninferiority_mean=noninferiority_mean, offset=offset
    )
    pv.validate(target="offset")
    offset = pv.offset

    def func(std: float) -> float:
        return _power(offset, std, size, alternative, alpha, dist) - power

    return float(brentq(func, 1e-6, 1e12))
