from math import sqrt
from typing import Literal

from scipy.stats import norm


def _power_pooled(
    treatment_proportion: float,
    reference_proportion: float,
    proportion_threshold: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using z-test with pooled variance."""

    effect = treatment_proportion - proportion_threshold

    treatment_var = treatment_proportion * (1 - treatment_proportion) / treatment_size
    reference_var = reference_proportion * (1 - reference_proportion) / reference_size
    se = sqrt(treatment_var + reference_var)

    pooled_proportion = (treatment_size * treatment_proportion + reference_size * reference_proportion) / (
        treatment_size + reference_size
    )
    pooled_se = sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))

    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf((norm.ppf(1 - alpha / 2) * pooled_se - effect) / se)
                + norm.cdf((norm.ppf(alpha / 2) * pooled_se - effect) / se)
            )
        case "greater":
            power = 1 - norm.cdf((norm.ppf(1 - alpha) * pooled_se - effect) / se)
        case "less":
            power = norm.cdf((norm.ppf(alpha) * pooled_se - effect) / se)

    return float(power)


def _power_pooled_cc(
    treatment_proportion: float,
    reference_proportion: float,
    proportion_threshold: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using z-test with pooled variance and continuity correction."""

    effect = treatment_proportion - proportion_threshold

    c = 1 / 2 * (1 / treatment_size + 1 / reference_size)

    treatment_var = treatment_proportion * (1 - treatment_proportion) / treatment_size
    reference_var = reference_proportion * (1 - reference_proportion) / reference_size
    se = sqrt(treatment_var + reference_var)

    pooled_proportion = (treatment_size * treatment_proportion + reference_size * reference_proportion) / (
        treatment_size + reference_size
    )
    pooled_se = sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))

    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf((norm.ppf(1 - alpha / 2) * pooled_se - (effect - c)) / se)
                + norm.cdf((norm.ppf(alpha / 2) * pooled_se - (effect + c)) / se)
            )
        case "greater":
            power = 1 - norm.cdf((norm.ppf(1 - alpha) * pooled_se - (effect - c)) / se)
        case "less":
            power = norm.cdf((norm.ppf(alpha) * pooled_se - (effect + c)) / se)

    return float(power)


def _power_unpooled(
    treatment_proportion: float,
    reference_proportion: float,
    proportion_threshold: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using z-tes with unpooled variance."""

    effect = treatment_proportion - proportion_threshold

    treatment_var = treatment_proportion * (1 - treatment_proportion) / treatment_size
    reference_var = reference_proportion * (1 - reference_proportion) / reference_size
    se = sqrt(treatment_var + reference_var)

    match alternative:
        case "two-sided":
            power = 1 - norm.cdf(norm.ppf(1 - alpha / 2) - effect / se) + norm.cdf(norm.ppf(alpha / 2) - effect / se)
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - effect / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - effect / se)

    return float(power)


def _power_unpooled_cc(
    treatment_proportion: float,
    reference_proportion: float,
    proportion_threshold: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power, using unpooled variance and continuity correction."""

    effect = treatment_proportion - proportion_threshold

    c = 1 / 2 * (1 / treatment_size + 1 / reference_size)

    treatment_var = treatment_proportion * (1 - treatment_proportion) / treatment_size
    reference_var = reference_proportion * (1 - reference_proportion) / reference_size
    se = sqrt(treatment_var + reference_var)

    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf(norm.ppf(1 - alpha / 2) - (effect - c) / se)
                + norm.cdf(norm.ppf(alpha / 2) - (effect + c) / se)
            )
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (effect - c) / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - (effect + c) / se)

    return float(power)


def _power(
    treatment_proportion: float,
    reference_proportion: float,
    proportion_threshold: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    method: Literal["z-pooled", "z-unpooled"],
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power."""

    match method:
        case "z-pooled":
            if continuity_correction:
                return _power_pooled_cc(
                    treatment_proportion,
                    reference_proportion,
                    proportion_threshold,
                    treatment_size,
                    reference_size,
                    alternative,
                    alpha,
                )
            else:
                return _power_pooled(
                    treatment_proportion,
                    reference_proportion,
                    proportion_threshold,
                    treatment_size,
                    reference_size,
                    alternative,
                    alpha,
                )
        case "z-unpooled":
            if continuity_correction:
                return _power_unpooled_cc(
                    treatment_proportion,
                    reference_proportion,
                    proportion_threshold,
                    treatment_size,
                    reference_size,
                    alternative,
                    alpha,
                )
            else:
                return _power_unpooled(
                    treatment_proportion,
                    reference_proportion,
                    proportion_threshold,
                    treatment_size,
                    reference_size,
                    alternative,
                    alpha,
                )
