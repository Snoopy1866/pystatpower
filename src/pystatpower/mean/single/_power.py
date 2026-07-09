from math import sqrt
from typing import Literal

from scipy.stats import nct, norm, t


def _power_z(
    offset: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power based on z-distribution."""

    se = std / sqrt(size)
    match alternative:
        case "two-sided":
            power = 1 - norm.cdf(norm.ppf(1 - alpha / 2) - offset / se) + norm.cdf(norm.ppf(alpha / 2) - offset / se)
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - offset / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - offset / se)

    return float(power)


def _power_t(
    offset: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power based on t-distribution."""

    df = size - 1
    nc = offset * sqrt(size) / std
    match alternative:
        case "two-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha / 2, df), df, nc) + nct.cdf(t.ppf(alpha / 2, df), df, nc)
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return float(power)


def _power(
    offset: float,
    std: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    dist: Literal["z", "t"] = "t",
) -> float:
    """Calculate the statistical power."""

    match dist:
        case "z":
            return _power_z(offset, std, size, alternative, alpha)
        case "t":
            return _power_t(offset, std, size, alternative, alpha)
