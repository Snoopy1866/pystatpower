from math import acos, ceil, copysign, cos, isclose, pi, sqrt
from typing import Literal

from scipy.optimize import OptimizeResult, brentq, minimize_scalar
from scipy.stats import norm

from ...exceptions import SolutionNotFoundError


def _distance_chisq(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the confidence interval width or the distance from the proportion difference to the confidence limit, using Pearson's chi-square method."""

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
        case "lower":
            z = norm.ppf(1 - alpha)
            L = diff - z * sd
            # U = 1
            distance = diff - max(L, -1)
        case "upper":
            z = norm.ppf(1 - alpha)
            # L = -1
            U = diff + z * sd
            distance = min(U, 1) - diff

    return float(distance)


def _distance_chisq_cc(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the confidence interval width or the distance from the proportion difference to the confidence limit, using Yate's chi-square with continuity correction method."""

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
        case "lower":
            z = norm.ppf(1 - alpha)
            L = diff - z * sd - c
            # U = 1
            distance = diff - max(L, -1)
        case "upper":
            z = norm.ppf(1 - alpha)
            # L = -1
            U = diff + z * sd + c
            distance = min(U, 1) - diff

    return float(distance)


def _distance_wilson(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the confidence interval width or the distance from the proportion difference to the confidence limit, using Newcombe-Wilson method."""

    alpha = 1 - conf_level
    diff = treatment_proportion - reference_proportion

    def _wilson_ci(proportion: float, size: float, alpha: float) -> tuple[float, float]:
        """Internal function to calculate Wilson confidence interval"""

        z = norm.ppf(1 - alpha)

        a = 2 * size * proportion + z**2
        b = z**2 + 4 * size * proportion * (1 - proportion)
        c = 2 * (size + z**2)
        L = (a - z * sqrt(b)) / c
        U = (a + z * sqrt(b)) / c

        return L, U

    match interval_type:
        case "two-sided":
            L1, U1 = _wilson_ci(treatment_proportion, treatment_size, alpha / 2)
            L2, U2 = _wilson_ci(reference_proportion, reference_size, alpha / 2)

            L = (
                treatment_proportion
                - reference_proportion
                - sqrt((treatment_proportion - L1) ** 2 + (U2 - reference_proportion) ** 2)
            )
            U = (
                treatment_proportion
                - reference_proportion
                + sqrt((U1 - treatment_proportion) ** 2 + (reference_proportion - L2) ** 2)
            )
            distance = U - L
        case "lower":
            L1, _ = _wilson_ci(treatment_proportion, treatment_size, alpha)
            _, U2 = _wilson_ci(reference_proportion, reference_size, alpha)

            L = (
                treatment_proportion
                - reference_proportion
                - sqrt((treatment_proportion - L1) ** 2 + (U2 - reference_proportion) ** 2)
            )
            # U = 1
            distance = diff - L
        case "upper":
            _, U1 = _wilson_ci(treatment_proportion, treatment_size, alpha)
            L2, _ = _wilson_ci(reference_proportion, reference_size, alpha)

            # L = -1
            U = (
                treatment_proportion
                - reference_proportion
                + sqrt((U1 - treatment_proportion) ** 2 + (reference_proportion - L2) ** 2)
            )
            distance = U - diff

    return float(distance)


def _distance_wilson_cc(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the confidence interval width or the distance from the proportion difference to the confidence limit, using Newcombe-Wilson with continuity correction method."""

    alpha = 1 - conf_level
    diff = treatment_proportion - reference_proportion

    def _wilson_cc_ci(proportion: float, size: float, alpha: float) -> tuple[float, float]:
        """Internal function to calculate Wilson confidence interval with continuity correction"""

        z = norm.ppf(1 - alpha)

        a = 2 * size * proportion + z**2
        b = z**2 + 4 * size * proportion * (1 - proportion)
        c = 2 * (size + z**2)
        L = (a - 1 - z * sqrt(b - 1 / size + 4 * proportion - 2)) / c
        U = (a + 1 + z * sqrt(b - 1 / size - 4 * proportion + 2)) / c

        return max(L, 0), min(U, 1)

    match interval_type:
        case "two-sided":
            L1, U1 = _wilson_cc_ci(treatment_proportion, treatment_size, alpha / 2)
            L2, U2 = _wilson_cc_ci(reference_proportion, reference_size, alpha / 2)

            L = (
                treatment_proportion
                - reference_proportion
                - sqrt((treatment_proportion - L1) ** 2 + (U2 - reference_proportion) ** 2)
            )
            U = (
                treatment_proportion
                - reference_proportion
                + sqrt((U1 - treatment_proportion) ** 2 + (reference_proportion - L2) ** 2)
            )
            distance = U - L
        case "lower":
            L1, _ = _wilson_cc_ci(treatment_proportion, treatment_size, alpha)
            _, U2 = _wilson_cc_ci(reference_proportion, reference_size, alpha)

            L = (
                treatment_proportion
                - reference_proportion
                - sqrt((treatment_proportion - L1) ** 2 + (U2 - reference_proportion) ** 2)
            )
            # U = 1
            distance = diff - L
        case "upper":
            _, U1 = _wilson_cc_ci(treatment_proportion, treatment_size, alpha)
            L2, _ = _wilson_cc_ci(reference_proportion, reference_size, alpha)

            # L = -1
            U = (
                treatment_proportion
                - reference_proportion
                + sqrt((U1 - treatment_proportion) ** 2 + (reference_proportion - L2) ** 2)
            )
            distance = U - diff

    return float(distance)


def _distance_farrington_manning(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the confidence interval width or the distance from the proportion difference to the confidence limit, using Farrington and Manning's score method."""

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
            L = brentq(lambda delta: func(delta) - norm.ppf(1 - alpha / 2), -1 + eps, diff)
            U = brentq(lambda delta: func(delta) - norm.ppf(alpha / 2), diff, 1 - eps)
            distance = U - L
        case "lower":
            L = brentq(lambda delta: func(delta) - norm.ppf(1 - alpha), -1 + eps, diff)
            # U = 1
            distance = diff - L
        case "upper":
            # L = -1
            U = brentq(lambda delta: func(delta) - norm.ppf(alpha), diff, 1 - eps)
            distance = U - diff

    return float(distance)


def _distance_miettinen_nurminen(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the confidence interval width or the distance from the proportion difference to the confidence limit, using Miettinen and Nurminen's score method."""

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
            L = brentq(lambda delta: func(delta) - norm.ppf(1 - alpha / 2), -1 + eps, diff)
            U = brentq(lambda delta: func(delta) - norm.ppf(alpha / 2), diff, 1 - eps)
            distance = U - L
        case "lower":
            L = brentq(lambda delta: func(delta) - norm.ppf(1 - alpha), -1 + eps, diff)
            # U = 1
            distance = diff - L
        case "upper":
            # L = -1
            U = brentq(lambda delta: func(delta) - norm.ppf(alpha), diff, 1 - eps)
            distance = U - diff

    return float(distance)


def _distance(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
    method: Literal["chisq", "wilson", "farrington_manning", "fm", "miettinen_nurminen", "mn"],
    continuity_correction: bool = False,
) -> float:
    """Calculate the confidence interval width or the distance from the proportion difference to the confidence limit."""

    match method:
        case "chisq":
            if continuity_correction:
                return _distance_chisq_cc(
                    treatment_proportion,
                    reference_proportion,
                    treatment_size,
                    reference_size,
                    conf_level,
                    interval_type,
                )
            else:
                return _distance_chisq(
                    treatment_proportion,
                    reference_proportion,
                    treatment_size,
                    reference_size,
                    conf_level,
                    interval_type,
                )
        case "wilson":
            if continuity_correction:
                return _distance_wilson_cc(
                    treatment_proportion,
                    reference_proportion,
                    treatment_size,
                    reference_size,
                    conf_level,
                    interval_type,
                )
            else:
                return _distance_wilson(
                    treatment_proportion,
                    reference_proportion,
                    treatment_size,
                    reference_size,
                    conf_level,
                    interval_type,
                )
        case "fm" | "farrington_manning":
            return _distance_farrington_manning(
                treatment_proportion, reference_proportion, treatment_size, reference_size, conf_level, interval_type
            )
        case "mn" | "miettinen_nurminen":
            return _distance_miettinen_nurminen(
                treatment_proportion, reference_proportion, treatment_size, reference_size, conf_level, interval_type
            )


def solve_distance(
    *,
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: int,
    reference_size: int,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    method: Literal["chisq", "wilson", "farrington_manning", "fm", "miettinen_nurminen", "mn"],
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the confidence interval width or the distance from the proportion difference to the confidence limit.

    Args:
        treatment_proportion:
            Proportion in the treatment group.
        reference_proportion:
            Proportion in the reference group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        conf_level:
            Confidence level.

            - If `interval_type` is `'two-sided'`, a two-sided confidence level is required.
            - If `interval_type` is `'lower'` or `'upper'`, a one-sided confidence level is required.
        interval_type:
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        method:
            The method used to construct the confidence interval.

            - `'chisq'`: Pearson's chi-square method.
            - `'wilson'`: Newcombe-Wilson method.
            - `'farrington_manning'`, `'fm'`: Farrington and Manning's score method.
            - `'miettinen_nurminen'`, `'mn'`: Miettinen and Nurminen's score method.
        continuity_correction:
            Whether to apply the continuity correction, only takes effect when `method` is specified as `'chisq'` or `'wilson'`


    Returns:
        The confidence interval width or the distance from the proportion difference to the confidence limit.

            - If `interval_type` is `'two-sided'`, the confidence interval width is returned.
            - If `interval_type` is `'lower'` or `'upper'`, the distance from the proportion difference to the confidence limit is returned.

    """

    return _distance(
        treatment_proportion,
        reference_proportion,
        treatment_size,
        reference_size,
        conf_level,
        interval_type,
        method,
        continuity_correction,
    )


def solve_size(
    *,
    treatment_proportion: float,
    reference_proportion: float,
    distance: float,
    ratio: float = 1,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    method: Literal["chisq", "wilson", "farrington_manning", "fm", "miettinen_nurminen", "mn"],
    continuity_correction: bool = False,
) -> tuple[int, int]:
    """
    Estimate the required sample size.

    Args:
        treatment_proportion:
            Proportion in the treatment group.
        reference_proportion:
            Proportion in the reference group.
        distance:
            Confidence interval width or distance from the proportion to the confidence limit.

            - If `interval_type` = `'two-sided'`, specify the confidence interval width.
            - If `interval_type` = `'lower'` or `'upper'`, specify the distance from the proportion difference to the confidence limit.
        ratio:
            Ratio of sample sizes in the treatment and reference group.
        conf_level:
            Confidence level.

            - If `interval_type` is `'two-sided'`, specify the two-sided confidence level.
            - If `interval_type` is `'lower'` or `'upper'`, specify the one-sided confidence level.
        interval_type:
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        method:
            The method used to construct the confidence interval.

            - `'chisq'`: Pearson's chi-square method.
            - `'wilson'`: Newcombe-Wilson method.
            - `'farrington_manning'`, `'fm'`: Farrington and Manning's score method.
            - `'miettinen_nurminen'`, `'mn'`: Miettinen and Nurminen's score method.
        continuity_correction:
            Whether to apply the continuity correction, only takes effect when `method` is specified as `'chisq'` or `'wilson'`


    Returns:
        The required sample sizes in treatment and reference groups, respectively.
    """

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _distance(
                    treatment_proportion,
                    reference_proportion,
                    reference_size * ratio,
                    reference_size,
                    conf_level,
                    interval_type,
                    method,
                    continuity_correction,
                )
                - distance
            )

        reference_size = ceil(brentq(func, 1, 1e12))
        treatment_size = ceil(reference_size * ratio)
    else:  # ratio < 1

        def func(treatment_size: float) -> float:
            return (
                _distance(
                    treatment_proportion,
                    reference_proportion,
                    treatment_size,
                    treatment_size / ratio,
                    conf_level,
                    interval_type,
                    method,
                    continuity_correction,
                )
                - distance
            )

        treatment_size = ceil(brentq(func, 1, 1e12))
        reference_size = ceil(treatment_size / ratio)

    return treatment_size, reference_size


def solve_treatment_proportion(
    *,
    reference_proportion: float,
    treatment_size: int,
    reference_size: int,
    distance: float,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    method: Literal["chisq", "wilson", "farrington_manning", "fm", "miettinen_nurminen", "mn"],
    continuity_correction: bool = False,
    direction: Literal["greater", "less"],
) -> float:
    """
    Estimate the required proportion in the treatment group.

    Args:
        reference_proportion:
            Proportion in the reference group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        distance:
            Confidence interval width or distance from the proportion to the confidence limit.

            - If `interval_type` = `'two-sided'`, specify the confidence interval width.
            - If `interval_type` = `'lower'` or `'upper'`, specify the distance from the proportion difference to the confidence limit.
        conf_level:
            Confidence level.

            - If `interval_type` is `'two-sided'`, a two-sided confidence level is required.
            - If `interval_type` is `'lower'` or `'upper'`, a one-sided confidence level is required.
        interval_type:
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        method:
            The method used to construct the confidence interval.

            - `'chisq'`: Pearson's chi-square method.
            - `'wilson'`: Newcombe-Wilson method.
            - `'farrington_manning'`, `'fm'`: Farrington and Manning's score method.
            - `'miettinen_nurminen'`, `'mn'`: Miettinen and Nurminen's score method.
        continuity_correction:
            Whether to apply the continuity correction, only takes effect when `method` is specified as `'chisq'` or `'wilson'`
        direction:
            Controls which of the two potential solutions for the treatment proportion is selected.

            Since the confidence interval distance constraint typically yields two valid roots, this parameter
            determines whether to return the higher or lower proportion.

            - `'greater'`: Returns the larger (higher) of the two treatment proportion solutions.
            - `'less'`: Returns the smaller (lower) of the two treatment proportion solutions.

    Returns:
        The required proportion in the treatment group.

    Raises:
        SolutionNotFoundError: If the solution cannot be found.
    """

    def func(treatment_proportion: float) -> float:
        return (
            _distance(
                treatment_proportion,
                reference_proportion,
                treatment_size,
                reference_size,
                conf_level,
                interval_type,
                method,
                continuity_correction,
            )
            - distance
        )

    eps = 1e-12
    lb = eps
    ub = 1 - eps
    res: OptimizeResult = minimize_scalar(lambda treatment_proportion: -func(treatment_proportion), bounds=(lb, ub))
    if not res.success:
        raise SolutionNotFoundError("Solution not found.")

    if abs(func(res.x)) < 1e-9:
        return float(res.x)

    match direction:
        case "greater":
            if func(res.x) * func(ub) > 0:
                raise SolutionNotFoundError("Solution not found.")
            else:
                return float(brentq(func, res.x, ub))
        case "less":
            if func(res.x) * func(lb) > 0:
                raise SolutionNotFoundError("Solution not found.")
            else:
                return float(brentq(func, lb, res.x))


def solve_reference_proportion(
    *,
    treatment_proportion: float,
    treatment_size: int,
    reference_size: int,
    distance: float,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    method: Literal["chisq", "wilson", "farrington_manning", "fm", "miettinen_nurminen", "mn"],
    continuity_correction: bool = False,
    direction: Literal["greater", "less"],
) -> float:
    """
    Estimate the required proportion in the reference group.

    Args:
        treatment_proportion:
            Proportion in the treatment group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        distance:
            Confidence interval width or distance from the proportion to the confidence limit.

            - If `interval_type` = `'two-sided'`, specify the confidence interval width.
            - If `interval_type` = `'lower'` or `'upper'`, specify the distance from the proportion difference to the confidence limit.
        conf_level:
            Confidence level.

            - If `interval_type` is `'two-sided'`, a two-sided confidence level is required.
            - If `interval_type` is `'lower'` or `'upper'`, a one-sided confidence level is required.
        interval_type:
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        method:
            The method used to construct the confidence interval.

            - `'chisq'`: Pearson's chi-square method.
            - `'wilson'`: Newcombe-Wilson method.
            - `'farrington_manning'`, `'fm'`: Farrington and Manning's score method.
            - `'miettinen_nurminen'`, `'mn'`: Miettinen and Nurminen's score method.
        continuity_correction:
            Whether to apply the continuity correction, only takes effect when `method` is specified as `'chisq'` or `'wilson'`
        direction:
            Controls which of the two potential solutions for the reference proportion is selected.

            Since the confidence interval distance constraint typically yields two valid roots, this parameter
            determines whether to return the higher or lower proportion.

            - `'greater'`: Returns the larger (higher) of the two reference proportion solutions.
            - `'less'`: Returns the smaller (lower) of the two reference proportion solutions.

    Returns:
        The required proportion in the reference group.

    Raises:
        SolutionNotFoundError: If the solution cannot be found.
    """

    def func(reference_proportion: float) -> float:
        return (
            _distance(
                treatment_proportion,
                reference_proportion,
                treatment_size,
                reference_size,
                conf_level,
                interval_type,
                method,
                continuity_correction,
            )
            - distance
        )

    eps = 1e-12
    lb = eps
    ub = 1 - eps
    res: OptimizeResult = minimize_scalar(lambda reference_proportion: -func(reference_proportion), bounds=(lb, ub))
    if not res.success:
        raise SolutionNotFoundError("Solution not found.")

    if abs(func(res.x)) < 1e-9:
        return float(res.x)

    match direction:
        case "greater":
            if func(res.x) * func(ub) > 0:
                raise SolutionNotFoundError("Solution not found.")
            else:
                return float(brentq(func, res.x, ub))
        case "less":
            if func(res.x) * func(lb) > 0:
                raise SolutionNotFoundError("Solution not found.")
            else:
                return float(brentq(func, lb, res.x))
