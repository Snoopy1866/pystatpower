from collections.abc import Callable
from math import sqrt
from typing import Literal

from scipy.stats import binom, norm


def _min_nonneg(f: Callable[[int], float], *, bounds: tuple[int, int], strict: bool = False) -> int:
    """
    Return the smallest non-negative integer satisfying f(x) >= 0.

    Args:
        f:
            A discrete function whose domain is the set of positive integers.
        bounds:
            A limited boundary
        strict:
            Whether to enable strict mode. In strict mode, after finding the smallest non-negative integer that meets
            the condition, the search will continue to increase x to ensure that f(x) remains stable above 0.

            Currently, this parameter does not have any effect.

    Returns:
        Non-negative integer solutions satisfying the condition.
    """

    lb, ub = bounds

    x = lb
    step = 1
    while x < ub:
        if f(x) >= 0:
            break
        x += step

    return x


def _power_exact(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using exact test."""

    match alternative:
        case "two-sided":
            reject_L = binom.ppf(alpha / 2, size, proportion_threshold)
            if binom.cdf(reject_L, size, proportion_threshold) > alpha / 2:
                reject_L -= 1
            reject_U = binom.ppf(1 - alpha / 2, size, proportion_threshold)
            power = 1 - binom.cdf(reject_U, size, proportion) + binom.cdf(reject_L, size, proportion)
        case "greater":
            reject_U = binom.ppf(1 - alpha, size, proportion_threshold)
            power = 1 - binom.cdf(reject_U, size, proportion)
        case "less":
            reject_L = binom.ppf(alpha, size, proportion_threshold)
            if binom.cdf(reject_L, size, proportion_threshold) > alpha:
                reject_L -= 1
            power = binom.cdf(reject_L, size, proportion)

    return float(power)


def _power_p0(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using p0 to calculate the variance."""

    offset = proportion - proportion_threshold
    p0_se = sqrt(proportion_threshold * (1 - proportion_threshold) / size)
    p_se = sqrt(proportion * (1 - proportion) / size)
    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf((norm.ppf(1 - alpha / 2) * p0_se - offset) / p_se)
                + norm.cdf((norm.ppf(alpha / 2) * p0_se - offset) / p_se)
            )
        case "greater":
            power = 1 - norm.cdf((norm.ppf(1 - alpha) * p0_se - offset) / p_se)
        case "less":
            power = norm.cdf((norm.ppf(alpha) * p0_se - offset) / p_se)
    return float(power)


def _power_p0_cc(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using p0 with continuity correction to calculate the variance."""

    if abs(proportion - proportion_threshold) > 1 / (2 * size):
        c = 1 / (2 * size)
    else:
        c = 0

    offset = proportion - proportion_threshold
    p0_se = sqrt(proportion_threshold * (1 - proportion_threshold) / size)
    p_se = sqrt(proportion * (1 - proportion) / size)
    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf((norm.ppf(1 - alpha / 2) * p0_se - (offset - c)) / p_se)
                + norm.cdf((norm.ppf(alpha / 2) * p0_se - (offset + c)) / p_se)
            )
        case "greater":
            power = 1 - norm.cdf((norm.ppf(1 - alpha) * p0_se - (offset - c)) / p_se)
        case "less":
            power = norm.cdf((norm.ppf(alpha) * p0_se - (offset + c)) / p_se)
    return float(power)


def _power_phat(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using phat to calculate the variance."""

    offset = proportion - proportion_threshold
    p_se = sqrt(proportion * (1 - proportion) / size)
    match alternative:
        case "two-sided":
            power = (
                1 - norm.cdf(norm.ppf(1 - alpha / 2) - offset / p_se) + norm.cdf(norm.ppf(alpha / 2) - offset / p_se)
            )
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - offset / p_se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - offset / p_se)

    return float(power)


def _power_phat_cc(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using phat with continuity correction to calculate the variance."""

    if abs(proportion - proportion_threshold) > 1 / (2 * size):
        c = 1 / (2 * size)
    else:
        c = 0

    offset = proportion - proportion_threshold
    p_se = sqrt(proportion * (1 - proportion) / size)
    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf(norm.ppf(1 - alpha / 2) - (offset - c) / p_se)
                + norm.cdf(norm.ppf(alpha / 2) - (offset + c) / p_se)
            )
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (offset - c) / p_se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - (offset + c) / p_se)

    return float(power)


def _power(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    method: Literal["exact", "z-p0", "z-phat"],
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power."""

    match method:
        case "exact":
            return _power_exact(proportion, proportion_threshold, size, alternative, alpha)
        case "z-p0":
            if continuity_correction:
                return _power_p0_cc(proportion, proportion_threshold, size, alternative, alpha)
            else:
                return _power_p0(proportion, proportion_threshold, size, alternative, alpha)
        case "z-phat":
            if continuity_correction:
                return _power_phat_cc(proportion, proportion_threshold, size, alternative, alpha)
            else:
                return _power_phat(proportion, proportion_threshold, size, alternative, alpha)
