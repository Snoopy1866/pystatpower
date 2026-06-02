from math import sqrt
from typing import Literal

from scipy.stats import norm


def _distance_chisq(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """
    Calculate the confidence interval width or the distance from the proportion to the confidence bound for the difference between two independent proportions,
    for difference between two independent proportions, using Pearson's chi-square method.
    """

    alpha = 1 - conf_level
    diff = treatment_proportion - reference_proportion
    sd = sqrt(
        treatment_proportion * (1 - treatment_proportion) / treatment_size
        + reference_proportion * (1 - reference_proportion) / reference_size
    )

    match interval_type:
        case "two-sided":
            z = norm.ppf(1 - alpha / 2)
            L = diff - z * sd
            U = diff + z * sd
            distance = min(U, 1) - max(L, -1)
        case "lower one-sided":
            z = norm.ppf(1 - alpha)
            U = diff + z * sd
            distance = min(U, 1) - diff
        case "upper one-sided":
            z = norm.ppf(1 - alpha)
            L = diff - z * sd
            distance = diff - max(L, -1)

    return distance


def _distance_chisq_cc(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """
    Calculate the confidence interval width or the distance from the proportion to the confidence bound for the difference between two independent proportions,
    using Yate's chi-square with continuity correction method.
    """

    alpha = 1 - conf_level
    diff = treatment_proportion - reference_proportion
    sd = sqrt(
        treatment_proportion * (1 - treatment_proportion) / treatment_size
        + reference_proportion * (1 - reference_proportion) / reference_size
    )
    c = 1 / 2 * (1 / treatment_size + 1 / reference_size)

    match interval_type:
        case "two-sided":
            z = norm.ppf(1 - alpha / 2)
            L = diff - z * sd - c
            U = diff + z * sd + c
            distance = min(U, 1) - max(L, -1)
        case "lower one-sided":
            z = norm.ppf(1 - alpha)
            U = diff + z * sd + c
            distance = min(U, 1) - diff
        case "upper one-sided":
            z = norm.ppf(1 - alpha)
            L = diff - z * sd - c
            distance = diff - max(L, -1)

    return distance


def _distance(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
    method: Literal["chisq", "chisq_cc"],
) -> float:
    """Calculate the confidence interval width or the distance from the proportion to the confidence bound for the difference between two independent proportions."""

    match method:
        case "chisq":
            distance = _distance_chisq(
                treatment_proportion, reference_proportion, treatment_size, reference_size, conf_level, interval_type
            )
        case "chisq_cc":
            distance = _distance_chisq_cc(
                treatment_proportion, reference_proportion, treatment_size, reference_size, conf_level, interval_type
            )

    return distance


def solve_distance(
    *,
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: int,
    reference_size: int,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"] = "two-sided",
    method: Literal["chisq", "chisq_cc"] = "chisq",
) -> float:
    """
    Calculate the confidence interval width or the distance from the proportion to the confidence bound for the difference between two independent proportions.

    Args:
        treatment_proportion (float):
            Actual proportion in the treatment group ($p_1$). Must be between 0 and 1.
        reference_proportion (float):
            Actual proportion in the reference group ($p_2$). Must be between 0 and 1.
        treatment_size (float):
            Sample size in the treatment group ($n_1$). Must be greater than 0.
        reference_size (float):
            Sample size in the reference group ($n_2$). Must be greater than 0.
        conf_level (float, optional):
            Confidence level.
        interval_type (Literal["two-sided", "lower one-sided", "upper one-sided"], optional):
            Type of the confidence interval.

            - `two-sided`: Two-sided confidence interval.
            - `lower one-sided`: Lower one-sided confidence interval.
            - `upper one-sided`: Upper one-sided confidence interval.
        method (Literal["chisq", "chisq_cc"], optional):
            Method to calculate the confidence interval width or the distance from the proportion to the confidence bound.

            - `chisq`: Pearson's chi-square method.
            - `chisq_cc`: Yate's chi-square with continuity correction method.


    Returns:
        (float): The confidence interval width or the distance from the proportion to the confidence bound.
    """

    distance = _distance(
        treatment_proportion, reference_proportion, treatment_size, reference_size, conf_level, interval_type, method
    )

    return distance
