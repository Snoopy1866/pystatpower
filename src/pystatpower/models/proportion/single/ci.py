from math import ceil, sqrt
from typing import Literal

from scipy.optimize import OptimizeResult, brentq, minimize_scalar
from scipy.stats import f, norm

from ...._constant import SAMPLE_SIZE_SEARCH_MAX


def _distance_wald(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """Calculate the confidence interval width for one proportion or the distance from the proportion to the confidence bound using the Wald method."""

    match interval_type:
        case "two-sided":
            lower_limit = proportion - norm.ppf((1 + conf_level) / 2) * sqrt(proportion * (1 - proportion) / size)
            upper_limit = proportion + norm.ppf((1 + conf_level) / 2) * sqrt(proportion * (1 - proportion) / size)
            distance = min(upper_limit, 1) - max(lower_limit, 0)
        case "lower one-sided":
            lower_limit = proportion - norm.ppf(conf_level) * sqrt(proportion * (1 - proportion) / size)
            distance = proportion - max(lower_limit, 0)
        case "upper one-sided":
            upper_limit = proportion + norm.ppf(conf_level) * sqrt(proportion * (1 - proportion) / size)
            distance = min(upper_limit, 1) - proportion

    return float(distance)


def _distance_wald_cc(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """Calculate the confidence interval width for one proportion or the distance from the proportion to the confidence bound using the Wald method with continuity correction."""

    match interval_type:
        case "two-sided":
            lower_limit = (
                proportion
                - norm.ppf((1 + conf_level) / 2) * sqrt(proportion * (1 - proportion) / size)
                - 1 / (2 * size)
            )
            upper_limit = (
                proportion
                + norm.ppf((1 + conf_level) / 2) * sqrt(proportion * (1 - proportion) / size)
                + 1 / (2 * size)
            )
            distance = min(upper_limit, 1) - max(lower_limit, 0)
        case "lower one-sided":
            lower_limit = (
                proportion - norm.ppf(conf_level) * sqrt(proportion * (1 - proportion) / size) - 1 / (2 * size)
            )
            distance = proportion - max(lower_limit, 0)
        case "upper one-sided":
            upper_limit = (
                proportion + norm.ppf(conf_level) * sqrt(proportion * (1 - proportion) / size) + 1 / (2 * size)
            )
            distance = min(upper_limit, 1) - proportion

    return float(distance)


def _distance_wilson(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """Calculate the confidence interval width for one proportion or the distance from the proportion to the confidence bound using the Wilson method."""

    match interval_type:
        case "two-sided":
            lower_limit = (
                (2 * size * proportion + norm.ppf((1 + conf_level) / 2) ** 2)
                - norm.ppf((1 + conf_level) / 2)
                * sqrt(norm.ppf((1 + conf_level) / 2) ** 2 + 4 * size * proportion * (1 - proportion))
            ) / (2 * (size + norm.ppf((1 + conf_level) / 2) ** 2))
            upper_limit = (
                (2 * size * proportion + norm.ppf((1 + conf_level) / 2) ** 2)
                + norm.ppf((1 + conf_level) / 2)
                * sqrt(norm.ppf((1 + conf_level) / 2) ** 2 + 4 * size * proportion * (1 - proportion))
            ) / (2 * (size + norm.ppf((1 + conf_level) / 2) ** 2))
            distance = upper_limit - lower_limit
        case "lower one-sided":
            lower_limit = (
                (2 * size * proportion + norm.ppf(conf_level) ** 2)
                - norm.ppf(conf_level) * sqrt(norm.ppf(conf_level) ** 2 + 4 * size * proportion * (1 - proportion))
            ) / (2 * (size + norm.ppf(conf_level) ** 2))
            distance = proportion - lower_limit
        case "upper one-sided":
            upper_limit = (
                (2 * size * proportion + norm.ppf(conf_level) ** 2)
                + norm.ppf(conf_level) * sqrt(norm.ppf(conf_level) ** 2 + 4 * size * proportion * (1 - proportion))
            ) / (2 * (size + norm.ppf(conf_level) ** 2))
            distance = upper_limit - proportion

    return float(distance)


def _distance_wilson_cc(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """Calculate the confidence interval width for one proportion or the distance from the proportion to the confidence bound using the Wilson method, with continuity correction."""

    match interval_type:
        case "two-sided":
            lower_limit = (
                (2 * size * proportion + norm.ppf((1 + conf_level) / 2) ** 2 - 1)
                - norm.ppf((1 + conf_level) / 2)
                * sqrt(
                    norm.ppf((1 + conf_level) / 2) ** 2
                    - 1 / size
                    + 4 * size * proportion * (1 - proportion)
                    + 4 * proportion
                    - 2
                )
            ) / (2 * (size + norm.ppf((1 + conf_level) / 2) ** 2))

            upper_limit = (
                (2 * size * proportion + norm.ppf((1 + conf_level) / 2) ** 2 + 1)
                + norm.ppf((1 + conf_level) / 2)
                * sqrt(
                    norm.ppf((1 + conf_level) / 2) ** 2
                    - 1 / size
                    + 4 * size * proportion * (1 - proportion)
                    - 4 * proportion
                    + 2
                )
            ) / (2 * (size + norm.ppf((1 + conf_level) / 2) ** 2))
            distance = upper_limit - lower_limit
        case "lower one-sided":
            lower_limit = (
                (2 * size * proportion + norm.ppf(conf_level) ** 2 - 1)
                - norm.ppf(conf_level)
                * sqrt(
                    norm.ppf(conf_level) ** 2 - 1 / size + 4 * size * proportion * (1 - proportion) + 4 * proportion - 2
                )
            ) / (2 * (size + norm.ppf(conf_level) ** 2))
            distance = proportion - lower_limit
        case "upper one-sided":
            upper_limit = (
                (2 * size * proportion + norm.ppf(conf_level) ** 2 + 1)
                + norm.ppf(conf_level)
                * sqrt(
                    norm.ppf(conf_level) ** 2 - 1 / size + 4 * size * proportion * (1 - proportion) - 4 * proportion + 2
                )
            ) / (2 * (size + norm.ppf(conf_level) ** 2))
            distance = upper_limit - proportion

    return float(distance)


def _distance_clopper_pearson(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
) -> float:
    """Calculate the confidence interval width for one proportion or the distance from the proportion to the confidence bound using the Clopper-Pearson method."""

    match interval_type:
        case "two-sided":
            lower_limit = 1 / (
                1
                + (size * (1 - proportion) + 1)
                / (
                    size
                    * proportion
                    * f.ppf((1 - conf_level) / 2, 2 * size * proportion, 2 * (size * (1 - proportion) + 1))
                )
            )
            upper_limit = 1 / (
                1
                + size
                * (1 - proportion)
                / (
                    (size * proportion + 1)
                    * f.ppf((1 + conf_level) / 2, 2 * (size * proportion + 1), 2 * size * (1 - proportion))
                )
            )
            distance = upper_limit - lower_limit
        case "lower one-sided":
            lower_limit = 1 / (
                1
                + (size * (1 - proportion) + 1)
                / (size * proportion * f.ppf(1 - conf_level, 2 * size * proportion, 2 * (size * (1 - proportion) + 1)))
            )
            distance = proportion - lower_limit
        case "upper one-sided":
            upper_limit = 1 / (
                1
                + size
                * (1 - proportion)
                / (
                    (size * proportion + 1)
                    * f.ppf(conf_level, 2 * (size * proportion + 1), 2 * size * (1 - proportion))
                )
            )
            distance = upper_limit - proportion

    return float(distance)


def _distance(
    proportion: float,
    size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"],
    method: Literal["clopper-pearson", "wald", "wilson"],
    continuity_correction: bool = False,
) -> float:
    """Calculate the confidence interval width for one proportion or the distance from the proportion to the confidence bound."""

    match method:
        case "clopper-pearson":
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
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"] = "two-sided",
    method: Literal["clopper-pearson", "wald", "wilson"] = "clopper-pearson",
    continuity_correction: bool = False,
) -> float:
    """
    Calculate the confidence interval width for one proportion or the distance from the proportion to the confidence bound.

    Args:
        proportion (float):
            Proportion.
        size (int):
            Sample size.
        conf_level (float, optional):
            Confidence level.
        interval_type (Literal["two-sided", "lower one-sided", "upper one-sided"], optional):
            Type of the confidence interval.

            - `two-sided`: Two-sided confidence interval $(L, U)$.
            - `lower one-sided`: Lower one-sided confidence interval $(L, +\\infty)$.
            - `upper one-sided`: Upper one-sided confidence interval $(-\\infty, U)$.
        method (Literal["clopper-pearson", "wald", "wilson"], optional):
            Method used in calculation of the confidence interval.
        continuity_correction (bool | None, optional):
            Whether or not to apply Yate's continuity correction. Only valid for `method='wald'` or `method='wilson'`.

    Returns:
        (float): The confidence interval width.

    Raises:
        ValueError: If `method='wald'` or `method='wilson'`, and `continuity_correction=None`.
    """

    return _distance(proportion, size, conf_level, interval_type, method, continuity_correction)


def solve_size(
    *,
    proportion: float,
    distance: float,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"] = "two-sided",
    method: Literal["clopper-pearson", "wald", "wilson"] = "clopper-pearson",
    continuity_correction: bool = False,
) -> int:
    """
    Estimate the required sample size, given either a desired confidence interval width or a desired distance from the proportion to the confidence bound.

    Args:
        proportion (float):
            Proportion.
        distance (float):
            - if `interval_type='two-sided'`, provide confidence interval width.
            - if `interval_type='lower one-sided'` or `interval_type='upper one-sided'`, provide the distance from the proportion to the confidence bound.
        conf_level (float, optional):
            Confidence level.
        interval_type (Literal["two-sided", "lower one-sided", "upper one-sided"], optional):
            Type of the confidence interval.

            - `two-sided`: Two-sided confidence interval $(L, U)$.
            - `lower one-sided`: Lower one-sided confidence interval $(L, +\\infty)$.
            - `upper one-sided`: Upper one-sided confidence interval $(-\\infty, U)$.
        method (Literal["clopper-pearson", "wald", "wilson"], optional):
            Method used in calculation of the confidence interval.
        continuity_correction (bool | None, optional):
            Whether or not to apply Yate's continuity correction. Only valid for `method='wald'` or `method='wilson'`.

    Returns:
        (int): The required sample size.

    Raises:
        ValueError: If `method='wald'` or `method='wilson'`, and `continuity_correction=None`.
    """

    def func(size: float) -> float:
        return _distance(proportion, size, conf_level, interval_type, method, continuity_correction) - distance

    if method == "wilson" and continuity_correction:
        # wilson score 连续性校正公式中的分子可能存在对负数开算术平方根的情况，这可能会导致置信区间宽度计算失败，因此需要先求出根号下的定义域，缩小 brentq 搜索范围

        z = norm.ppf((1 + conf_level) / 2) if interval_type == "two-sided" else norm.ppf(conf_level)

        a = 4 * proportion * (1 - proportion)
        b1 = z**2 + 4 * proportion - 2
        b2 = z**2 - 4 * proportion + 2
        c = -1

        # 对 Lower Limit 求根号下的定义域
        n1 = (-b1 - sqrt(b1**2 - 4 * a * c)) / (2 * a)
        n2 = (-b1 + sqrt(b1**2 - 4 * a * c)) / (2 * a)

        # 对 Upper Limit 求根号下的定义域
        n3 = (-b2 - sqrt(b2**2 - 4 * a * c)) / (2 * a)
        n4 = (-b2 + sqrt(b2**2 - 4 * a * c)) / (2 * a)

        match interval_type:
            case "two-sided":
                lower_bound = max(n1, n2, n3, n4)
            case "lower one-sided":
                lower_bound = max(n3, n4)
            case "upper one-sided":
                lower_bound = max(n1, n2)

        upper_bound = SAMPLE_SIZE_SEARCH_MAX

        # wilson score 连续性校正计算出的置信区间宽度并随样本量增大而单调减小，而是在小样本区间内先增大，随着样本量继续增大，置信区间宽度逐渐减小。
        # 因此，直接使用 brentq 可能无法收敛，必须先找到置信区间的极大值点 $n'$，然后将 brentq 的搜索区间限定为 $[n', [SAMPLE_SIZE_SEARCH_MAX]]$，才能保证收敛。
        res: OptimizeResult = minimize_scalar(lambda size: -func(size), bounds=(lower_bound, upper_bound))
        if -res.fun < 0:
            raise ValueError("No solution found.")
        else:
            lower_bound = max(lower_bound, res.x)

        size = brentq(func, lower_bound, upper_bound)
    else:
        size = brentq(func, 0.000001, SAMPLE_SIZE_SEARCH_MAX)

    return ceil(size)


def solve_proportion(
    *,
    size: int,
    distance: float,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"] = "two-sided",
    method: Literal["clopper-pearson", "wald", "wilson"] = "clopper-pearson",
    continuity_correction: bool = False,
    search_direction: Literal["below", "above"] = "above",
) -> float:
    """Estimate the required proportion, given either a desired confidence interval width or a desired distance from the proportion to the confidence bound.

    Args:
        size (int):
            Sample size.
        distance (float):
            - if `interval_type='two-sided'`, provide confidence interval width.
            - if `interval_type='lower one-sided'` or `interval_type='upper one-sided'`, provide the distance from the proportion to the confidence bound.
        conf_level (float, optional):
            Confidence level.
        interval_type (Literal["two-sided", "lower one-sided", "upper one-sided"], optional):
            Type of the confidence interval.

            - `two-sided`: Two-sided confidence interval $(L, U)$.
            - `lower one-sided`: Lower one-sided confidence interval $(L, +\\infty)$.
            - `upper one-sided`: Upper one-sided confidence interval $(-\\infty, U)$.
        method (Literal["clopper-pearson", "wald", "wilson"], optional):
            Method used in calculation of the confidence interval.
        continuity_correction (bool | None, optional):
            Whether or not to apply Yate's continuity correction. Only valid for `method='wald'` or `method='wilson'`.
        search_direction (Literal["below", "above"], optional):
            Direction of the search.

            - `'below'`: search for the proportion in range (0, 0.5]
            - `'above'`: search for the proportion in range [0.5, 1)

    Returns:
        (float): The required proportion.
    """

    def func(proportion: float) -> float:
        return _distance(proportion, size, conf_level, interval_type, method, continuity_correction) - distance

    match search_direction.lower():
        case "below":
            proportion = brentq(func, 0.000001, 0.5 + 0.000001)
        case "above":
            proportion = brentq(func, 0.5 - 0.000001, 0.999999)

    return proportion
