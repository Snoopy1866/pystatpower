from math import sqrt
from typing import Literal

from scipy.stats import norm


def _power_p0(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for one proportion test, using p0 to calculate the variance."""

    h1_z_mean = (proportion - proportion_threshold) / sqrt(proportion_threshold * (1 - proportion_threshold) / size)
    h1_z_std = sqrt(proportion * (1 - proportion) / (proportion_threshold * (1 - proportion_threshold)))
    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf((norm.ppf(1 - alpha / 2) - h1_z_mean) / h1_z_std)
                + norm.cdf((norm.ppf(alpha / 2) - h1_z_mean) / h1_z_std)
            )
        case "greater":
            power = 1 - norm.cdf((norm.ppf(1 - alpha) - h1_z_mean) / h1_z_std)
        case "less":
            power = norm.cdf((norm.ppf(alpha) - h1_z_mean) / h1_z_std)
    return float(power)


def _power_p0_cc(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for one proportion test, using p0 with continuity correction to calculate the variance."""

    if abs(proportion - proportion_threshold) <= 1 / (2 * size):
        c = 0
    elif proportion > proportion_threshold:
        c = -1 / (2 * size)
    else:  # proportion < proportion_threshold
        c = 1 / (2 * size)

    h1_z_mean = (proportion - proportion_threshold + c) / sqrt(proportion_threshold * (1 - proportion_threshold) / size)
    h1_z_std = sqrt(proportion * (1 - proportion) / (proportion_threshold * (1 - proportion_threshold)))
    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf((norm.ppf(1 - alpha / 2) - h1_z_mean) / h1_z_std)
                + norm.cdf((norm.ppf(alpha / 2) - h1_z_mean) / h1_z_std)
            )
        case "greater":
            power = 1 - norm.cdf((norm.ppf(1 - alpha) - h1_z_mean) / h1_z_std)
        case "less":
            power = norm.cdf((norm.ppf(alpha) - h1_z_mean) / h1_z_std)
    return float(power)


def _power_phat(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for one proportion test, using phat to calculate the variance."""

    h1_z_mean = (proportion - proportion_threshold) / sqrt(proportion * (1 - proportion) / size)
    match alternative:
        case "two-sided":
            power = 1 - norm.cdf(norm.ppf(1 - alpha / 2) - h1_z_mean) + norm.cdf(norm.ppf(alpha / 2) - h1_z_mean)
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - h1_z_mean)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - h1_z_mean)

    return float(power)


def _power_phat_cc(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for one proportion test, using phat with continuity correction to calculate the variance."""

    if abs(proportion - proportion_threshold) <= 1 / (2 * size):
        c = 0
    elif proportion > proportion_threshold:
        c = -1 / (2 * size)
    else:  # proportion < proportion_threshold
        c = 1 / (2 * size)

    h1_z_mean = (proportion - proportion_threshold + c) / sqrt(proportion * (1 - proportion) / size)
    match alternative:
        case "two-sided":
            power = 1 - norm.cdf(norm.ppf(1 - alpha / 2) - h1_z_mean) + norm.cdf(norm.ppf(alpha / 2) - h1_z_mean)
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - h1_z_mean)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - h1_z_mean)

    return float(power)


def _power(
    proportion: float,
    proportion_threshold: float,
    size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    method: Literal["z-p0", "z-phat"],
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power for one proportion test."""

    match method:
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
