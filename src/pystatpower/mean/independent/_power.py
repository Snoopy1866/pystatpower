from math import sqrt
from typing import Literal

from scipy.stats import nct
from scipy.stats import norm
from scipy.stats import t


def _power_z_equal_var(
    diff: float,
    margin: float,
    std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the power of two independent mean difference test, using z test, assuming equal variances."""

    se = std * sqrt(1 / treatment_size + 1 / reference_size)

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


def _power_z_unequal_var(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the power of two independent mean difference test, using z test, assuming unequal variances."""

    se = sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)

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


def _power_t_equal_var(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the power of two independent mean difference test, using t test, assuming equal variances."""

    df = treatment_size + reference_size - 2
    se = sqrt(
        ((treatment_size - 1) * treatment_std**2 + (reference_size - 1) * reference_std**2)
        / df
        * (1 / treatment_size + 1 / reference_size)
    )
    nc = (diff - margin) / se

    match alternative:
        case "two-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha / 2, df), df, nc) + nct.cdf(t.ppf(alpha / 2, df), df, nc)
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return power


def _power_t_unequal_var_welch(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the power of two independent mean difference test, using Welch's approximate t test."""

    df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
        treatment_std**4 / (treatment_size**2 * (treatment_size + 1))
        + reference_std**4 / (reference_size**2 * (reference_size + 1))
    ) - 2
    se = sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)
    nc = (diff - margin) / se

    match alternative:
        case "two-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha / 2, df), df, nc) + nct.cdf(t.ppf(alpha / 2, df), df, nc)
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return power


def _power_t_unequal_var_satterthwaite(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
) -> float:
    """Calculate the power of two independent mean difference test, using Satterthwaite's approximate t test."""

    df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
        treatment_std**4 / (treatment_size**2 * (treatment_size - 1))
        + reference_std**4 / (reference_size**2 * (reference_size - 1))
    )
    se = sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)
    nc = (diff - margin) / se

    match alternative:
        case "two-sided":
            power = 1 - nct.cdf(t.ppf(1 - alpha / 2, df), df, nc) + nct.cdf(t.ppf(alpha / 2, df), df, nc)
        case "greater":
            power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
        case "less":
            power = nct.cdf(t.ppf(alpha, df), df, nc)

    return power


def _power(
    *,
    diff: float | None = None,
    margin: float,
    treatment_std: float | None = None,
    reference_std: float | None = None,
    std: float | None = None,
    treatment_size: float,
    reference_size: float,
    alternative: Literal["two-sided", "greater", "less"],
    alpha: float,
    dist: Literal["z", "t"],
    equal_var: bool,
    approx_t_method: Literal["welch", "satterthwaite"],
) -> float:
    """Calculate the power of two independent mean difference test."""

    match dist:
        case "z":
            if equal_var:
                power = _power_z_equal_var(diff, margin, std, treatment_size, reference_size, alternative, alpha)
            else:
                power = _power_z_unequal_var(
                    diff, margin, treatment_std, reference_std, treatment_size, reference_size, alternative, alpha
                )
        case "t":
            if equal_var:
                power = _power_t_equal_var(
                    diff, margin, treatment_std, reference_std, treatment_size, reference_size, alternative, alpha
                )
            else:
                match approx_t_method:
                    case "welch":
                        power = _power_t_unequal_var_welch(
                            diff,
                            margin,
                            treatment_std,
                            reference_std,
                            treatment_size,
                            reference_size,
                            alternative,
                            alpha,
                        )
                    case "satterthwaite":
                        power = _power_t_unequal_var_satterthwaite(
                            diff,
                            margin,
                            treatment_std,
                            reference_std,
                            treatment_size,
                            reference_size,
                            alternative,
                            alpha,
                        )

    return power
