from math import ceil, sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm, t

from ...._constant import SAMPLE_SIZE_SEARCH_MAX


def _ci_half_width_z(
    std: float, size: float, conf_level: float, interval_type: Literal["one-sided", "two-sided"]
) -> float:
    """Calculate the half-width of the confidence interval for one mean using z-test."""

    match interval_type:
        case "one-sided":
            ci_half_width = norm.ppf(conf_level) * std / sqrt(size)
        case "two-sided":
            ci_half_width = norm.ppf((1 + conf_level) / 2) * std / sqrt(size)

    return float(ci_half_width)


def _ci_half_width_t(
    std: float, size: float, conf_level: float, interval_type: Literal["one-sided", "two-sided"]
) -> float:
    """Calculate the half-width of the confidence interval for one mean using t-test."""

    match interval_type:
        case "one-sided":
            ci_half_width = t.ppf(conf_level, size - 1) * std / sqrt(size)
        case "two-sided":
            ci_half_width = t.ppf((1 + conf_level) / 2, size - 1) * std / sqrt(size)

    return float(ci_half_width)


def _ci_half_width(
    std: float,
    size: float,
    conf_level: float,
    interval_type: Literal["one-sided", "two-sided"],
    method: Literal["z", "t"],
) -> float:
    """Calculate the half-width of the confidence interval for one mean."""

    match method:
        case "z":
            ci_half_width = _ci_half_width_z(std, size, conf_level, interval_type)
        case "t":
            ci_half_width = _ci_half_width_t(std, size, conf_level, interval_type)

    return float(ci_half_width)


def solve_half_width(
    *,
    std: float,
    size: int,
    conf_level: float = 0.95,
    interval_type: Literal["one-sided", "two-sided"] = "two-sided",
    method: Literal["z", "t"] = "t",
) -> float:
    """
    Calculate the half-width of the confidence interval for one mean.

    Args:
        std (float):
            Standard deviation ($\\sigma$). If `method='t'`, provide the sample standard deviation ($S$).
        size (int):
            Sample size ($n$).
        conf_level (float, Optional):
            Confidence level.
        interval_type (Literal["one-sided", "two-sided"], optional):
            The type of confidence interval.
        method (Literal["z", "t"], optional):
            The distribution used to construct the confidence interval.

    Returns:
        (float): The half-width of the confidence interval for one mean.
    """

    half_width = _ci_half_width(std, size, conf_level, interval_type, method)
    return float(half_width)


def solve_size(
    *,
    half_width: float,
    std: float,
    conf_level: float = 0.95,
    interval_type: Literal["one-sided", "two-sided"] = "two-sided",
    method: Literal["z", "t"] = "t",
) -> int:
    """
    Calculate the required sample size for the half-width of one mean confidence interval.

    Args:
        half_width (float):
            Half-width of the confidence interval ($d$).
        std (float):
            Standard deviation ($\\sigma$). If `method='t'`, provide the sample standard deviation ($S$).
        conf_level (float, Optional):
            Confidence level.
        interval_type (Literal["one-sided", "two-sided"], optional):
            The type of confidence interval.
        method (Literal["z", "t"], optional):
            The distribution used to construct the confidence interval.

    Returns:
        (int): The required sample size.
    """

    def func(size: float) -> float:
        return _ci_half_width(std, size, conf_level, interval_type, method) - half_width

    size = ceil(brentq(func, 1.1, SAMPLE_SIZE_SEARCH_MAX))
    return size


def solve_std(
    *,
    half_width: float,
    size: int,
    conf_level: float = 0.95,
    interval_type: Literal["one-sided", "two-sided"] = "two-sided",
    method: Literal["z", "t"] = "t",
) -> float:
    """
    Calculate the required standard deviation for the half-width of one mean confidence interval.

    Args:
        half_width (float):
            Half-width of the confidence interval ($d$).
        size (int):
            Sample size ($n$).
        conf_level (float, Optional):
            Confidence level.
        interval_type (Literal["one-sided", "two-sided"], optional):
            The type of confidence interval.
        method (Literal["z", "t"], optional):
            The distribution used to construct the confidence interval.

    Returns:
        (float): The required standard deviation.
    """

    multiplier = _ci_half_width(1, size, conf_level, interval_type, method)
    std = half_width / multiplier

    return float(std)
