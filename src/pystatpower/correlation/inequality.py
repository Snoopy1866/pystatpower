from math import atanh, ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm


def _power(
    null_correlation: float,
    correlation: float,
    alternative: Literal["two-sided", "greater", "less"],
    size: float,
    alpha: float,
) -> float:
    """Calculate the statistical power."""

    null_zeta = atanh(null_correlation)
    zeta = atanh(correlation)
    se_recip = sqrt(size - 3)

    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf(norm.ppf(1 - alpha / 2) - (zeta - null_zeta) * se_recip)
                + norm.cdf(norm.ppf(alpha / 2) - (zeta - null_zeta) * se_recip)
            )
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (zeta - null_zeta) * se_recip)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - (zeta - null_zeta) * se_recip)

    return float(power)


def solve_power(
    *,
    null_correlation: float,
    correlation: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
) -> float:
    """Calculate the statistical power.

    Args:
        null_correlation:
            Correlation coefficient under the null hypothesis.
        correlation:
            Correlation coefficient under the alternative hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\rho \\neq \\rho_0$.
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\rho > \\rho_0$.
            - If `alternative` is `'less'`, the alternative hypothesis is $\\rho < \\rho_0$.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.

    Returns:
        The statistical power of the test.
    """

    return _power(null_correlation, correlation, alternative, size, alpha)


def solve_size(
    *,
    null_correlation: float,
    correlation: float,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
) -> int:
    """Estimate the required sample size.

    Args:
        null_correlation:
            Correlation coefficient under the null hypothesis.
        correlation:
            Correlation coefficient under the alternative hypothesis.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\rho \\neq \\rho_0$.
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\rho > \\rho_0$.
            - If `alternative` is `'less'`, the alternative hypothesis is $\\rho < \\rho_0$.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.

    Returns:
        The required sample size.
    """

    def func(size: float) -> float:
        return _power(null_correlation, correlation, alternative, size, alpha) - power

    return ceil(brentq(func, 3, 1e12))


def solve_correlation(
    *,
    null_correlation: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimate the required correlation coefficient under the alternative hypothesis.

    Args:
        null_correlation:
            Correlation coefficient under the null hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\rho \\neq \\rho_0$.
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\rho > \\rho_0$.
            - If `alternative` is `'less'`, the alternative hypothesis is $\\rho < \\rho_0$.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        direction:
            The direction for the correlation coefficient under the alternative hypothesis relative to the correlation coefficient under the null hypothesis.

            - `'greater'`: Search for the alternative correlation coefficient greater than the null correlation coefficient.
            - `'less'`: Search for the alternative correlation coefficient less than the null correlation coefficient.

            !!! note
                - If `alternative` is `'two-sided'`, this parameter is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'greater'`, and this parameter is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'less'`, and this parameter is ignored.

    Returns:
        required correlation coefficient under the alternative hypothesis.

    Raises:
        ValueError: If `alternative` is `'two-sided'` but `direction` is not specified.
    """

    if alternative == "two-sided":
        if direction is None:
            raise ValueError("'direction' is required when 'alternative' is 'two-sided'.")
    elif alternative == "greater":
        direction = "greater"
    else:  # alternative == "less"
        direction = "less"

    def func(correlation: float) -> float:
        return _power(null_correlation, correlation, alternative, size, alpha) - power

    match direction:
        case "less":
            return float(brentq(func, -1 + 1e-12, null_correlation))
        case "greater":
            return float(brentq(func, null_correlation, 1 - 1e-12))


def solve_null_correlation(
    *,
    correlation: float,
    size: int,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    alpha: float = 0.05,
    power: float = 0.8,
    direction: Literal["greater", "less"] | None = None,
) -> float:
    """
    Estimete the required correlation coefficient under the null hypothesis.

    Args:
        correlation:
            Correlation coefficient under the alternative hypothesis.
        size:
            Sample size.
        alternative:
            Type of the alternative hypothesis.

            - If `alternative` is `'two-sided'`, the alternative hypothesis is $\\rho \\neq \\rho_0$.
            - If `alternative` is `'greater'`, the alternative hypothesis is $\\rho > \\rho_0$.
            - If `alternative` is `'less'`, the alternative hypothesis is $\\rho < \\rho_0$.
        alpha:
            Significance level.

            - If `alternative` is `'two-sided'`, `alpha` represents the two-sided significance level.
            - If `alternative` is `'greater'` or `'less'`, `alpha` represents the one-sided significance level.
        power:
            Expected statistical power.

            0.8 is a commonly used statistical power.
        direction:
            The direction for the correlation coefficient under the null hypothesis relative to the correlation coefficient under the alternative hypothesis.

            - `'greater'`: Search for the null correlation coefficient greater than the alternative correlation coefficient.
            - `'less'`: Search for the null correlation coefficient less than the alternative correlation coefficient.

            !!! note
                - If `alternative` is `'two-sided'`, this parameter is required.
                - If `alternative` is `'greater'`, the search direction is automatically inferred to be `'less'`, and this parameter is ignored.
                - If `alternative` is `'less'`, the search direction is automatically inferred to be `'greater'`, and this parameter is ignored.

    Returns:
        The required correlation coefficient under the null hypothesis.

    Raises:
        ValueError: If `alternative` is `'two-sided'` but `direction` is not specified.
    """

    if alternative == "two-sided":
        if direction is None:
            raise ValueError("'direction' is required when 'alternative' is 'two-sided'.")
    elif alternative == "greater":
        direction = "less"
    else:  # alternative == "less"
        direction = "greater"

    def func(null_correlation: float) -> float:
        return _power(null_correlation, correlation, alternative, size, alpha) - power

    match direction:
        case "greater":
            return float(brentq(func, correlation, 1 - 1e-12))
        case "less":
            return float(brentq(func, -1 + 1e-12, correlation))
