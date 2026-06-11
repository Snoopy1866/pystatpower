from math import ceil, exp, log, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm


def _fisher_z(r: float) -> float:
    """Fisher's z-transformation"""

    return 0.5 * log((1 + r) / (1 - r))


def _fisher_z_inverse(z: float) -> float:
    """Inverse of Fisher's z-transformation"""

    return (exp(2 * z) - 1) / (exp(2 * z) + 1)


def _distance_not_adjusted(
    correlation: float, size: float, conf_level: float, alternative: Literal["two-sided", "greater", "less"]
) -> float:
    """Calculate the correlation confidence interval width or the distance from the correlation coefficient to the confidence bound"""

    alpha = 1 - conf_level
    zr = _fisher_z(correlation)

    match alternative:
        case "two-sided":
            L = zr - norm.ppf(1 - alpha / 2) / sqrt(size - 3)
            U = zr + norm.ppf(1 - alpha / 2) / sqrt(size - 3)
            distance = _fisher_z_inverse(U) - _fisher_z_inverse(L)
        case "greater":
            L = zr - norm.ppf(1 - alpha) / sqrt(size - 3)
            distance = correlation - _fisher_z_inverse(L)
        case "less":
            U = zr + norm.ppf(1 - alpha) / sqrt(size - 3)
            distance = _fisher_z_inverse(U) - correlation

    return float(distance)


def _distance_adjusted(
    correlation: float, size: float, conf_level: float, alternative: Literal["two-sided", "greater", "less"]
) -> float:
    """Calculate the correlation confidence interval width or the distance from the correlation coefficient to the confidence bound, adjusted for bias."""

    alpha = 1 - conf_level
    zr = _fisher_z(correlation)
    bias = 0.5 * correlation / (size - 1)

    match alternative:
        case "two-sided":
            L = zr - bias - norm.ppf(1 - alpha / 2) / sqrt(size - 3)
            U = zr - bias + norm.ppf(1 - alpha / 2) / sqrt(size - 3)
            distance = _fisher_z_inverse(U) - _fisher_z_inverse(L)
        case "greater":
            L = zr - bias - norm.ppf(1 - alpha) / sqrt(size - 3)
            distance = correlation - _fisher_z_inverse(L)
        case "less":
            U = zr - bias + norm.ppf(1 - alpha) / sqrt(size - 3)
            distance = _fisher_z_inverse(U) - correlation

    return float(distance)


def _distance(
    correlation: float,
    size: float,
    conf_level: float,
    alternative: Literal["two-sided", "greater", "less"],
    bias_adj: bool,
) -> float:
    """Calculate the correlation confidence interval width or the distance from the correlation coefficient to the confidence bound"""

    if bias_adj:
        return _distance_adjusted(correlation, size, conf_level, alternative)
    else:  # bias_adj == False
        return _distance_not_adjusted(correlation, size, conf_level, alternative)


def solve_distance(
    *,
    correlation: float,
    size: int,
    conf_level: float = 0.95,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    bias_adj: bool = False,
) -> float:
    """Calculate the correlation confidence interval width or the distance from the correlation coefficient to the confidence bound

    Args:
        correlation (float):
            Actual correlation coefficient ($r$). Must be between -1 and 1.
        size (int):
            Sample size $n$.
        conf_level (float, optional):
            Condidence level.
        alternative (Literal[&quot;two, optional):
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'greater'`: Upper one-sided confidence interval.
            - `'less'`: Lower one-sided confidence interval.
        bias_adj (bool, optional):
            Whether to adjust for bias.

    Returns:
        (float): The correlation confidence interval width or the distance from the correlation coefficient to the confidence bound.
    """

    return float(_distance(correlation, size, conf_level, alternative, bias_adj))


def solve_size(
    *,
    correlation: float,
    distance: float,
    conf_level: float = 0.95,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
    bias_adj: bool = False,
) -> int:
    """Calculate the correlation confidence interval width or the distance from the correlation coefficient to the confidence bound

    Args:
        correlation (float):
            Actual correlation coefficient ($r$). Must be between -1 and 1.
        size (int):
            Sample size $n$.
        conf_level (float, optional):
            Condidence level.
        alternative (Literal[&quot;two, optional):
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'greater'`: Upper one-sided confidence interval.
            - `'less'`: Lower one-sided confidence interval.
        bias_adj (bool, optional):
            Whether to adjust for bias.

    Returns:
        (float): The correlation confidence interval width or the distance from the correlation coefficient to the confidence bound.
    """

    return float(_distance(correlation, size, conf_level, alternative, bias_adj))
