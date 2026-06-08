from math import acos, copysign, cos, isclose, pi, sqrt
from typing import Literal

from scipy.optimize import brentq
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
            L = diff - z * sd
            distance = diff - max(L, -1)
        case "upper one-sided":
            z = norm.ppf(1 - alpha)
            U = diff + z * sd
            distance = min(U, 1) - diff

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
            L = diff - z * sd - c
            distance = diff - max(L, -1)
        case "upper one-sided":
            z = norm.ppf(1 - alpha)
            U = diff + z * sd + c
            distance = min(U, 1) - diff

    return distance


def _distance_newcombe_wilson(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """
    Calculate the confidence interval width or the distance from the proportion to the confidence bound for the difference between two independent proportions,
    using Newcombe-Wilson method.
    """

    alpha = 1 - conf_level
    diff = treatment_proportion - reference_proportion

    match interval_type:
        case "two-sided":
            z = norm.ppf(1 - alpha / 2)

            # calculate the wilson interval of the treatment proportion
            A1 = 2 * treatment_size * treatment_proportion + z**2
            B1 = z**2 + 4 * treatment_size * treatment_proportion * (1 - treatment_proportion)
            C1 = 2 * (treatment_size + z**2)
            L_1 = (A1 - z * sqrt(B1)) / C1
            U_1 = (A1 + z * sqrt(B1)) / C1

            # calculate the wilson interval of the reference proportion
            A2 = 2 * reference_size * reference_proportion + z**2
            B2 = z**2 + 4 * reference_size * reference_proportion * (1 - reference_proportion)
            C2 = 2 * (reference_size + z**2)
            L_2 = (A2 - z * sqrt(B2)) / C2
            U_2 = (A2 + z * sqrt(B2)) / C2

            # calculate the newcombe interval of the proportion difference
            L = (
                treatment_proportion
                - reference_proportion
                - sqrt((treatment_proportion - L_1) ** 2 + (U_2 - reference_proportion) ** 2)
            )
            U = (
                treatment_proportion
                - reference_proportion
                + sqrt((U_1 - treatment_proportion) ** 2 + (reference_proportion - L_2) ** 2)
            )
            distance = U - L
        case "lower one-sided":
            z = norm.ppf(1 - alpha)

            # calculate the wilson interval of the treatment proportion
            A1 = 2 * treatment_size * treatment_proportion + z**2
            B1 = z**2 + 4 * treatment_size * treatment_proportion * (1 - treatment_proportion)
            C1 = 2 * (treatment_size + z**2)
            L_1 = (A1 - z * sqrt(B1)) / C1
            # U_1 = (A1 + B1) / C1

            # calculate the wilson interval of the reference proportion
            A2 = 2 * reference_size * reference_proportion + z**2
            B2 = z**2 + 4 * reference_size * reference_proportion * (1 - reference_proportion)
            C2 = 2 * (reference_size + z**2)
            # L_2 = (A2 - B2) / C2
            U_2 = (A2 + z * sqrt(B2)) / C2

            # calculate the newcombe interval of the proportion difference
            L = (
                treatment_proportion
                - reference_proportion
                - sqrt((treatment_proportion - L_1) ** 2 + (U_2 - reference_proportion) ** 2)
            )
            # U = 1
            distance = diff - L
        case "upper one-sided":
            z = norm.ppf(1 - alpha)

            # calculate the wilson interval of the treatment proportion
            A1 = 2 * treatment_size * treatment_proportion + z**2
            B1 = z**2 + 4 * treatment_size * treatment_proportion * (1 - treatment_proportion)
            C1 = 2 * (treatment_size + z**2)
            # L_1 = (A1 - B1) / C1
            U_1 = (A1 + z * sqrt(B1)) / C1

            # calculate the wilson interval of the reference proportion
            A2 = 2 * reference_size * reference_proportion + z**2
            B2 = z**2 + 4 * reference_size * reference_proportion * (1 - reference_proportion)
            C2 = 2 * (reference_size + z**2)
            L_2 = (A2 - z * sqrt(B2)) / C2
            # U_2 = (A2 + B2) / C2

            # calculate the newcombe interval of the proportion difference
            # L = -1
            U = (
                treatment_proportion
                - reference_proportion
                + sqrt((U_1 - treatment_proportion) ** 2 + (reference_proportion - L_2) ** 2)
            )
            distance = U - diff

    return distance


def _distance_newcombe_wilson_cc(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """
    Calculate the confidence interval width or the distance from the proportion to the confidence bound for the difference between two independent proportions,
    using Newcombe-Wilson with continuity correction method.
    """

    alpha = 1 - conf_level
    diff = treatment_proportion - reference_proportion

    match interval_type:
        case "two-sided":
            z = norm.ppf(1 - alpha / 2)

            # calculate the wilson interval of the treatment proportion
            A1 = 2 * treatment_size * treatment_proportion + z**2
            B1 = z**2 + 4 * treatment_size * treatment_proportion * (1 - treatment_proportion)
            C1 = 2 * (treatment_size + z**2)
            L_1 = (A1 - 1 - z * sqrt(B1 - 1 / treatment_size + 4 * treatment_proportion - 2)) / C1
            U_1 = (A1 + 1 + z * sqrt(B1 - 1 / treatment_size - 4 * treatment_proportion + 2)) / C1
            L_1 = max(0, L_1)
            U_1 = min(1, U_1)

            # calculate the wilson interval of the reference proportion
            A2 = 2 * reference_size * reference_proportion + z**2
            B2 = z**2 + 4 * reference_size * reference_proportion * (1 - reference_proportion)
            C2 = 2 * (reference_size + z**2)
            L_2 = (A2 - 1 - z * sqrt(B2 - 1 / reference_size + 4 * reference_proportion - 2)) / C2
            U_2 = (A2 + 1 + z * sqrt(B2 - 1 / reference_size - 4 * reference_proportion + 2)) / C2
            L_2 = max(0, L_2)
            U_2 = min(1, U_2)

            # calculate the newcombe interval of the proportion difference
            L = (
                treatment_proportion
                - reference_proportion
                - sqrt((treatment_proportion - L_1) ** 2 + (U_2 - reference_proportion) ** 2)
            )
            U = (
                treatment_proportion
                - reference_proportion
                + sqrt((U_1 - treatment_proportion) ** 2 + (reference_proportion - L_2) ** 2)
            )
            distance = U - L
        case "lower one-sided":
            z = norm.ppf(1 - alpha)

            # calculate the wilson interval of the treatment proportion
            A1 = 2 * treatment_size * treatment_proportion + z**2
            B1 = z**2 + 4 * treatment_size * treatment_proportion * (1 - treatment_proportion)
            C1 = 2 * (treatment_size + z**2)
            L_1 = (A1 - 1 - z * sqrt(B1 - 1 / treatment_size + 4 * treatment_proportion - 2)) / C1
            # U_1 = (A1 + 1 + z * sqrt(B1 - 1 / treatment_size - 4 * treatment_proportion + 2)) / C1
            L_1 = max(0, L_1)
            # U_1 = min(1, U_1)

            # calculate the wilson interval of the reference proportion
            A2 = 2 * reference_size * reference_proportion + z**2
            B2 = z**2 + 4 * reference_size * reference_proportion * (1 - reference_proportion)
            C2 = 2 * (reference_size + z**2)
            # L_2 = (A2 - 1 - z * sqrt(B2 - 1 / reference_size + 4 * reference_proportion - 2)) / C2
            U_2 = (A2 + 1 + z * sqrt(B2 - 1 / reference_size - 4 * reference_proportion + 2)) / C2
            # L_2 = max(0, L_2)
            U_2 = min(1, U_2)

            # calculate the newcombe interval of the proportion difference
            L = (
                treatment_proportion
                - reference_proportion
                - sqrt((treatment_proportion - L_1) ** 2 + (U_2 - reference_proportion) ** 2)
            )
            # U = 1
            distance = diff - L
        case "upper one-sided":
            z = norm.ppf(1 - alpha)

            # calculate the wilson interval of the treatment proportion
            A1 = 2 * treatment_size * treatment_proportion + z**2
            B1 = z**2 + 4 * treatment_size * treatment_proportion * (1 - treatment_proportion)
            C1 = 2 * (treatment_size + z**2)
            # L_1 = (A1 - 1 - z * sqrt(B1 - 1 / treatment_size + 4 * treatment_proportion - 2)) / C1
            U_1 = (A1 + 1 + z * sqrt(B1 - 1 / treatment_size - 4 * treatment_proportion + 2)) / C1
            # L_1 = max(0, L_1)
            U_1 = min(1, U_1)

            # calculate the wilson interval of the reference proportion
            A2 = 2 * reference_size * reference_proportion + z**2
            B2 = z**2 + 4 * reference_size * reference_proportion * (1 - reference_proportion)
            C2 = 2 * (reference_size + z**2)
            L_2 = (A2 - 1 - z * sqrt(B2 - 1 / reference_size + 4 * reference_proportion - 2)) / C2
            # U_2 = (A2 + 1 + z * sqrt(B2 - 1 / reference_size - 4 * reference_proportion + 2)) / C2
            L_2 = max(0, L_2)
            # U_2 = min(1, U_2)

            # calculate the newcombe interval of the proportion difference
            # L = -1
            U = (
                treatment_proportion
                - reference_proportion
                + sqrt((U_1 - treatment_proportion) ** 2 + (reference_proportion - L_2) ** 2)
            )
            distance = U - diff

    return distance


def _distance_farrington_manning(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """
    Calculate the confidence interval width or the distance from the proportion to the confidence bound for the difference between two independent proportions,
    using Farrington and Manning's score method.
    """

    alpha = 1 - conf_level
    diff = treatment_proportion - reference_proportion

    x11 = treatment_size * treatment_proportion
    x21 = reference_size * reference_proportion
    m_1 = x11 + x21
    N = treatment_size + reference_size

    def func(delta: float) -> float:
        L3 = N
        L2 = (N + reference_size) * delta - N - m_1
        L1 = (reference_size * delta - N - 2 * x21) * delta + m_1
        L0 = x21 * delta * (1 - delta)
        C = L2**3 / (27 * L3**3) - L1 * L2 / (6 * L3**2) + L0 / (2 * L3)
        if isclose(C, 0, abs_tol=1e-12):
            p2 = -L2 / (3 * L3)
        else:
            B = copysign(1, C) * sqrt(L2**2 / (9 * L3**2) - L1 / (3 * L3))
            A = 1 / 3 * (pi + acos(C / B**3))
            p2 = 2 * B * cos(A) - L2 / (3 * L3)

        p1 = p2 + delta

        variance = p1 * (1 - p1) / treatment_size + p2 * (1 - p2) / reference_size

        return (diff - delta) / sqrt(variance)

    eps = 1e-12

    match interval_type:
        case "two-sided":
            # z = norm.ppf(1 - alpha / 2)
            L = brentq(lambda delta: func(delta) - norm.ppf(1 - alpha / 2), -1 + eps, diff)
            U = brentq(lambda delta: func(delta) - norm.ppf(alpha / 2), diff, 1 - eps)
            distance = U - L
        case "lower one-sided":
            # z = norm.ppf(1 - alpha)
            L = brentq(lambda delta: func(delta) - norm.ppf(1 - alpha), -1 + eps, diff)
            distance = diff - L
        case "upper one-sided":
            # z = norm.ppf(1 - alpha)
            U = brentq(lambda delta: func(delta) - norm.ppf(alpha), diff, 1 - eps)
            distance = U - diff

    return distance


def _distance_miettinen_nurminen(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """
    Calculate the confidence interval width or the distance from the proportion to the confidence bound for the difference between two independent proportions,
    using Miettinen and Nurminen's score method.
    """

    alpha = 1 - conf_level
    diff = treatment_proportion - reference_proportion

    x11 = treatment_size * treatment_proportion
    x21 = reference_size * reference_proportion
    m_1 = x11 + x21
    N = treatment_size + reference_size

    def func(delta: float) -> float:
        L3 = N
        L2 = (N + reference_size) * delta - N - m_1
        L1 = (reference_size * delta - N - 2 * x21) * delta + m_1
        L0 = x21 * delta * (1 - delta)
        C = L2**3 / (27 * L3**3) - L1 * L2 / (6 * L3**2) + L0 / (2 * L3)
        if isclose(C, 0, abs_tol=1e-12):
            p2 = -L2 / (3 * L3)
        else:
            B = copysign(1, C) * sqrt(L2**2 / (9 * L3**2) - L1 / (3 * L3))
            A = 1 / 3 * (pi + acos(C / B**3))
            p2 = 2 * B * cos(A) - L2 / (3 * L3)

        p1 = p2 + delta

        variance = (p1 * (1 - p1) / treatment_size + p2 * (1 - p2) / reference_size) * (N / (N - 1))

        return (diff - delta) / sqrt(variance)

    eps = 1e-12

    match interval_type:
        case "two-sided":
            # z = norm.ppf(1 - alpha / 2)
            L = brentq(lambda delta: func(delta) - norm.ppf(1 - alpha / 2), -1 + eps, diff)
            U = brentq(lambda delta: func(delta) - norm.ppf(alpha / 2), diff, 1 - eps)
            distance = U - L
        case "lower one-sided":
            # z = norm.ppf(1 - alpha)
            L = brentq(lambda delta: func(delta) - norm.ppf(1 - alpha), -1 + eps, diff)
            distance = diff - L
        case "upper one-sided":
            # z = norm.ppf(1 - alpha)
            U = brentq(lambda delta: func(delta) - norm.ppf(alpha), diff, 1 - eps)
            distance = U - diff

    return distance


def _distance(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
    method: Literal[
        "chisq", "chisq_cc", "newcombe_wilson", "newcombe_wilson_cc", "farrington_manning", "miettinen_nurminen"
    ],
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
        case "newcombe_wilson":
            distance = _distance_newcombe_wilson(
                treatment_proportion, reference_proportion, treatment_size, reference_size, conf_level, interval_type
            )
        case "newcombe_wilson_cc":
            distance = _distance_newcombe_wilson_cc(
                treatment_proportion, reference_proportion, treatment_size, reference_size, conf_level, interval_type
            )
        case "farrington_manning":
            distance = _distance_farrington_manning(
                treatment_proportion, reference_proportion, treatment_size, reference_size, conf_level, interval_type
            )
        case "miettinen_nurminen":
            distance = _distance_miettinen_nurminen(
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
    method: Literal[
        "chisq", "chisq_cc", "newcombe_wilson", "newcombe_wilson_cc", "farrington_manning", "miettinen_nurminen"
    ] = "chisq",
) -> float:
    """
    Calculate the confidence interval width or the distance from the proportion to the confidence bound for the difference between two independent proportions.

    Args:
        treatment_proportion (float):
            Actual proportion in the treatment group ($p_1$). Must be between 0 and 1.
        reference_proportion (float):
            Actual proportion in the reference group ($p_2$). Must be between 0 and 1.
        treatment_size (int):
            Sample size in the treatment group ($n_1$). Must be greater than 0.
        reference_size (int):
            Sample size in the reference group ($n_2$). Must be greater than 0.
        conf_level (float, optional):
            Confidence level.
        interval_type (Literal["two-sided", "lower one-sided", "upper one-sided"], optional):
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower one-sided'`: Lower one-sided confidence interval.
            - `'upper one-sided'`: Upper one-sided confidence interval.
        method (Literal["chisq", "chisq_cc"], optional):
            Method to calculate the confidence interval width or the distance from the proportion to the confidence bound.

            - `'chisq'`: Pearson's chi-square method.
            - `'chisq_cc'`: Yate's chi-square with continuity correction method.
            - `'newcombe_wilson'`: Newcombe-Wilson method.
            - `'newcombe_wilson_cc'`: Newcombe-Wilson with continuity correction method.
            - `'farrington_manning'`: Farrington and Manning's score method.
            - `'miettinen_nurminen'`: Miettinen and Nurminen's score method.


    Returns:
        (float): The confidence interval width or the distance from the proportion to the confidence bound.
    """

    distance = _distance(
        treatment_proportion, reference_proportion, treatment_size, reference_size, conf_level, interval_type, method
    )

    return distance
