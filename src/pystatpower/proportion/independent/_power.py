from math import sqrt
from typing import Literal

from scipy.stats import norm


def _power_pooled(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for two independent proportions using z-test with pooled variance."""

    diff = treatment_proportion - reference_proportion

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
                - norm.cdf((norm.ppf(1 - alpha / 2) * pooled_se - (diff - margin)) / se)
                + norm.cdf((norm.ppf(alpha / 2) * pooled_se - (diff - margin)) / se)
            )
        case "greater":
            power = 1 - norm.cdf((norm.ppf(1 - alpha) * pooled_se - (diff - margin)) / se)
        case "less":
            power = norm.cdf((norm.ppf(alpha) * pooled_se - (diff - margin)) / se)

    return float(power)


def _power_pooled_cc(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for two independent proportions using z-test with pooled variance and continuity correction."""

    diff = treatment_proportion - reference_proportion

    treatment_var = treatment_proportion * (1 - treatment_proportion) / treatment_size
    reference_var = reference_proportion * (1 - reference_proportion) / reference_size
    se = sqrt(treatment_var + reference_var)

    pooled_proportion = (treatment_size * treatment_proportion + reference_size * reference_proportion) / (
        treatment_size + reference_size
    )
    pooled_se = sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))

    c = 1 / 2 * (1 / treatment_size + 1 / reference_size)

    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf((norm.ppf(1 - alpha / 2) * pooled_se - (diff - margin - c)) / se)
                + norm.cdf((norm.ppf(alpha / 2) * pooled_se - (diff - margin + c)) / se)
            )
        case "greater":
            power = 1 - norm.cdf((norm.ppf(1 - alpha) * pooled_se - (diff - margin - c)) / se)
        case "less":
            power = norm.cdf((norm.ppf(alpha) * pooled_se - (diff - margin + c)) / se)

    return float(power)


def _power_unpooled(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for two independent proportions using z-tes with unpooled variance."""

    diff = treatment_proportion - reference_proportion

    treatment_var = treatment_proportion * (1 - treatment_proportion) / treatment_size
    reference_var = reference_proportion * (1 - reference_proportion) / reference_size
    se = sqrt(treatment_var + reference_var)

    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf(norm.ppf(1 - alpha / 2) - (diff - margin) / se)
                + norm.cdf(norm.ppf(alpha / 2) - (diff - margin) / se)
            )
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (diff - margin) / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - (diff - margin) / se)

    return float(power)


def _power_unpooled_cc(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the statistical power for two independent proportions using unpooled variance and continuity correction."""

    c = 1 / 2 * (1 / treatment_size + 1 / reference_size)

    diff = treatment_proportion - reference_proportion

    treatment_var = treatment_proportion * (1 - treatment_proportion) / treatment_size
    reference_var = reference_proportion * (1 - reference_proportion) / reference_size
    se = sqrt(treatment_var + reference_var)

    match alternative:
        case "two-sided":
            power = (
                1
                - norm.cdf(norm.ppf(1 - alpha / 2) - (diff - margin - c) / se)
                + norm.cdf(norm.ppf(alpha / 2) - (diff - margin + c) / se)
            )
        case "greater":
            power = 1 - norm.cdf(norm.ppf(1 - alpha) - (diff - margin - c) / se)
        case "less":
            power = norm.cdf(norm.ppf(alpha) - (diff - margin + c) / se)

    return float(power)


def _power(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    method: Literal["z-pooled", "z-unpooled"],
    continuity_correction: bool,
) -> float:
    """Calculate the statistical power for two independent proportions."""

    match method:
        case "z-pooled":
            if continuity_correction:
                return _power_pooled_cc(
                    treatment_proportion,
                    reference_proportion,
                    margin,
                    treatment_size,
                    reference_size,
                    alternative,
                    alpha,
                )
            else:
                return _power_pooled(
                    treatment_proportion,
                    reference_proportion,
                    margin,
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
                    margin,
                    treatment_size,
                    reference_size,
                    alternative,
                    alpha,
                )
            else:
                return _power_unpooled(
                    treatment_proportion,
                    reference_proportion,
                    margin,
                    treatment_size,
                    reference_size,
                    alternative,
                    alpha,
                )
