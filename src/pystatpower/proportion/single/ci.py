from math import ceil, sqrt
from typing import Literal

from scipy.optimize import OptimizeResult, brentq, minimize_scalar
from scipy.stats import f, norm

from ..._math_utils import _domain_square_root_of_quad


def _distance_wald(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the width of the confidence interval or the distance from the proportion to the confidence limit, using the Wald method."""

    alpha = 1 - conf_level

    se = sqrt(proportion * (1 - proportion) / size)

    match interval_type:
        case "two-sided":
            z = norm.ppf(1 - alpha / 2)
            L = proportion - z * se
            U = proportion + z * se
            distance = min(U, 1) - max(L, 0)
        case "lower":
            z = norm.ppf(1 - alpha)
            L = proportion - z * se
            # U = 1
            distance = proportion - max(L, 0)
        case "upper":
            z = norm.ppf(1 - alpha)
            # L = 0
            U = proportion + z * se
            distance = min(U, 1) - proportion

    return float(distance)


def _distance_wald_cc(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the width of the confidence interval or the distance from the proportion to the confidence limit, using the Wald method with continuity correction."""

    alpha = 1 - conf_level

    se = sqrt(proportion * (1 - proportion) / size)
    c = 1 / (2 * size)

    match interval_type:
        case "two-sided":
            z = norm.ppf(1 - alpha / 2)
            L = proportion - z * se - c
            U = proportion + z * se + c
            distance = min(U, 1) - max(L, 0)
        case "lower":
            z = norm.ppf(1 - alpha)
            L = proportion - z * se - c
            # U = 1
            distance = proportion - max(L, 0)
        case "upper":
            z = norm.ppf(1 - alpha)
            # L = 0
            U = proportion + z * se + c
            distance = min(U, 1) - proportion

    return float(distance)


def _distance_wilson(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the width of the confidence interval or the distance from the proportion to the confidence limit, using the Wilson method."""

    alpha = 1 - conf_level

    match interval_type:
        case "two-sided":
            z = norm.ppf(1 - alpha / 2)
            a = 2 * (size + z**2)
            b = 2 * size * proportion + z**2
            c = z**2 + 4 * size * proportion * (1 - proportion)

            L = (b - z * sqrt(c)) / a
            U = (b + z * sqrt(c)) / a
            distance = U - L
        case "lower":
            z = norm.ppf(1 - alpha)
            a = 2 * (size + z**2)
            b = 2 * size * proportion + z**2
            c = z**2 + 4 * size * proportion * (1 - proportion)

            L = (b - z * sqrt(c)) / a
            # U = 1
            distance = proportion - L
        case "upper":
            z = norm.ppf(1 - alpha)
            a = 2 * (size + z**2)
            b = 2 * size * proportion + z**2
            c = z**2 + 4 * size * proportion * (1 - proportion)

            # L = 0
            U = (b + z * sqrt(c)) / a
            distance = U - proportion

    return float(distance)


def _distance_wilson_cc(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the width of the confidence interval or the distance from the proportion to the confidence limit, using the Wilson method with continuity correction."""

    alpha = 1 - conf_level

    match interval_type:
        case "two-sided":
            z = norm.ppf(1 - alpha / 2)
            a = 2 * (size + z**2)
            b = 2 * size * proportion + z**2
            c1 = z**2 - 1 / size + 4 * size * proportion * (1 - proportion)
            c2 = 4 * proportion - 2

            L = ((b - 1) - z * sqrt(c1 + c2)) / a
            U = ((b + 1) + z * sqrt(c1 - c2)) / a
            distance = U - L
        case "lower":
            z = norm.ppf(1 - alpha)
            a = 2 * (size + z**2)
            b = 2 * size * proportion + z**2
            c1 = z**2 - 1 / size + 4 * size * proportion * (1 - proportion)
            c2 = 4 * proportion - 2

            L = ((b - 1) - z * sqrt(c1 + c2)) / a
            # U = 1
            distance = proportion - L
        case "upper":
            z = norm.ppf(1 - alpha)
            a = 2 * (size + z**2)
            b = 2 * size * proportion + z**2
            c1 = z**2 - 1 / size + 4 * size * proportion * (1 - proportion)
            c2 = 4 * proportion - 2

            # L = 0
            U = ((b + 1) + z * sqrt(c1 - c2)) / a
            distance = U - proportion

    return float(distance)


def _distance_clopper_pearson(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
) -> float:
    """Calculate the width of the confidence interval or the distance from the proportion to the confidence limit, using the Clopper-Pearson method."""

    alpha = 1 - conf_level

    n = size
    p = proportion
    q = 1 - p

    match interval_type:
        case "two-sided":
            L = 1 / (1 + (n * q + 1) / (n * p * f.ppf(alpha / 2, 2 * n * p, 2 * (n * q + 1))))
            U = 1 / (1 + n * q / ((n * p + 1) * f.ppf(1 - alpha / 2, 2 * (n * p + 1), 2 * n * q)))
            distance = U - L
        case "lower":
            L = 1 / (1 + (n * q + 1) / (n * p * f.ppf(alpha, 2 * n * p, 2 * (n * q + 1))))
            # U = 1
            distance = proportion - L
        case "upper":
            # L = 0
            U = 1 / (1 + n * q / ((n * p + 1) * f.ppf(1 - alpha, 2 * (n * p + 1), 2 * n * q)))
            distance = U - proportion

    return float(distance)


def _distance(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
    method: Literal["wald", "wilson", "clopper-pearson", "cp"],
    continuity_correction: bool = False,
) -> float:
    """Calculate the width of the confidence interval or the distance from the proportion to the confidence limit"""

    match method:
        case "clopper-pearson" | "cp":
            return _distance_clopper_pearson(proportion, size, conf_level, interval_type)
        case "wald":
            if continuity_correction:
                return _distance_wald_cc(proportion, size, conf_level, interval_type)
            else:
                return _distance_wald(proportion, size, conf_level, interval_type)
        case "wilson":
            if continuity_correction:
                return _distance_wilson_cc(proportion, size, conf_level, interval_type)
            else:
                return _distance_wilson(proportion, size, conf_level, interval_type)


def solve_distance(
    *,
    proportion: float,
    size: int,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    method: Literal["wald", "wilson", "clopper-pearson", "cp"] = "cp",
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the confidence interval width or the distance from the proportion to the confidence limit.

    Args:
        proportion:
            Proportion.
        size:
            Sample size.
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

            - `'wald'`: Wald method.
            - `'wilson'`: Wilson method.
            - `'clopper-pearson'`, `'cp'`: Clopper-Pearson method.
        continuity_correction:
            Whether to apply the continuity correction, only takes effect when `method` is specified as `'wald'` or `'wilson'`

    Returns:
        The confidence interval width or the distance from the proportion to the confidence limit.

            - If `alternative` is `'two-sided'`, the confidence interval width is returned.
            - If `alternative` is `'less'`, the distance from the proportion to the confidence limit is returned.
    """

    return _distance(proportion, size, conf_level, interval_type, method, continuity_correction)


def solve_size(
    *,
    proportion: float,
    distance: float,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    method: Literal["wald", "wilson", "clopper-pearson", "cp"] = "cp",
    continuity_correction: bool = False,
) -> int:
    """
    Estimate the required sample size.

    For two-sided confidence interval, the confidence interval width is required.

    For one-sided confidence interval, the distance from the proportion to the confidence limit is required.

    Args:
        proportion:
            Proportion.
        distance:
            - If `interval_type` is `'two-sided'`, a confidence interval width is required.
            - If `interval_type` is `'lower'` or `'upper'`, a distance from the proportion to the confidence limit is required.
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

            - `'wald'`: Wald method.
            - `'wilson'`: Wilson method.
            - `'clopper-pearson'`, `'cp'`: Clopper-Pearson method.
        continuity_correction:
            Whether to apply the continuity correction, only takes effect when `method` is specified as `'wald'` or `'wilson'`

    Returns:
        int: The required sample size.
    """

    def func(size: float) -> float:
        return _distance(proportion, size, conf_level, interval_type, method, continuity_correction) - distance

    if method == "wilson" and continuity_correction:
        # The numerator in the wilson score continuity correction formula may take the arithmetic square root of a
        # negative number,which may cause the confidence interval width calculation to fail. Therefore, it is necessary
        # to first find the domain under the root sign and narrow the brentq search range.
        alpha = 1 - conf_level
        match interval_type:
            case "two-sided":
                z = norm.ppf(1 - alpha / 2)

                a = 4 * proportion * (1 - proportion)
                b1 = z**2 + (4 * proportion - 2)
                b2 = z**2 - (4 * proportion - 2)
                c = -1
                lb = max(_domain_square_root_of_quad(a, b1, c)[1][0], _domain_square_root_of_quad(a, b2, c)[1][0])
            case "lower":
                z = norm.ppf(1 - alpha)

                a = 4 * proportion * (1 - proportion)
                b = z**2 + (4 * proportion - 2)
                c = -1
                lb = _domain_square_root_of_quad(a, b, c)[1][0]
            case "upper":
                z = norm.ppf(1 - alpha)

                a = 4 * proportion * (1 - proportion)
                b = z**2 - (4 * proportion - 2)
                c = -1
                lb = _domain_square_root_of_quad(a, b, c)[1][0]

        ub = 1e12

        # The width of the confidence interval calculated by wilson score continuity correction does not decreases
        # monotonically as the sample size increases. Instead, it first increases in the small sample range, and as
        # the sample size continues to increase, the width of the confidence interval gradually decreases. Therefore,
        # using brentq directly may not converge. You must first find the maximum value point $n'$ of the confidence
        # interval, and then limit the search interval of brentq to $(n', 1e12)$ to ensure convergence.
        res: OptimizeResult = minimize_scalar(lambda size: -func(size), bounds=(lb, ub))
        if -res.fun < 0:
            return 2  # Any sample size can meet the requirements, and the minimum allowed sample size 2 is directly returned.
        else:
            lb = max(lb, res.x)
            return ceil(brentq(func, lb, ub))
    else:
        return ceil(brentq(func, 1e-12, 1e12))


def solve_proportion(
    *,
    size: int,
    distance: float,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    method: Literal["wald", "wilson", "clopper-pearson", "cp"] = "cp",
    continuity_correction: bool = False,
    direction: Literal["greater", "less"] = "greater",
) -> float:
    """
    Estimate the required proportion.

    For two-sided confidence interval, the confidence interval width is required.

    For one-sided confidence interval, the distance from the proportion to the confidence limit is required.

    Args:
        size:
            Sample size.
        distance:
            - If `interval_type` is `'two-sided'`, a confidence interval width is required.
            - If `interval_type` is `'lower'` or `'upper'`, a distance from the proportion to the confidence limit is required.
        conf_level:
            Confidence level.

            - If `interval_type` is `'two-sided'`, a two-sided confidence level should is required.
            - If `interval_type` is `'lower'` or `'upper'`, a one-sided confidence level is required.
        interval_type:
            Type of the confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        method:
            The method used to construct the confidence interval.

            - `'wald'`: Wald method.
            - `'wilson'`: Wilson method.
            - `'clopper-pearson'`, `'cp'`: Clopper-Pearson method.
        continuity_correction:
            Whether to apply the continuity correction, only takes effect when `method` is specified as `'wald'` or `'wilson'`
        direction:
            The search direction for the proportion relative to the 0.5.

            - `'greater'`: Search for the proportion greater than 0.5.
            - `'less'`: Search for the proportion less than 0.5.

    Returns:
        float: The required proportion.
    """

    def func(proportion: float) -> float:
        return _distance(proportion, size, conf_level, interval_type, method, continuity_correction) - distance

    if abs(func(0.5)) < 1e-9:
        return 0.5
    else:
        match direction:
            case "greater":
                return float(brentq(func, 0.5, 1 - 1e-12))
            case "less":
                return float(brentq(func, 1e-12, 0.5))
