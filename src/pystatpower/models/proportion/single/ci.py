from math import sqrt

from scipy.optimize import OptimizeResult, brentq, minimize_scalar
from scipy.stats import f, norm

from ...._constant import SAMPLE_SIZE_SEARCH_MAX


def _ci_width(
    proportion: float,
    size: float,
    alpha: float = 0.05,
    method: str = "clopper_pearson",
    continuity_correction: bool = False,
) -> float:
    match method.lower():
        case "clopper_pearson":
            return _ci_width_clopper_pearson(proportion, size, alpha)
        case "wald":
            if continuity_correction:
                return _ci_width_wald_cc(proportion, size, alpha)
            else:
                return _ci_width_wald(proportion, size, alpha)
        case "wilson":
            if continuity_correction:
                return _ci_wilson_cc(proportion, size, alpha)
            else:
                return _ci_width_wilson(proportion, size, alpha)


def _ci_width_clopper_pearson(proportion: float, size: float, alpha: float = 0.05) -> float:
    ci_lower = (
        size
        * proportion
        / (
            size * proportion
            + (size - size * proportion + 1)
            * f.ppf(1 - alpha / 2, 2 * (size - size * proportion + 1), 2 * size * proportion)
        )
    )

    ci_upper = (
        (size * proportion + 1)
        * f.ppf(1 - alpha / 2, 2 * (size * proportion + 1), 2 * (size - size * proportion))
        / (
            (size - size * proportion)
            + (size * proportion + 1)
            * f.ppf(1 - alpha / 2, 2 * (size * proportion + 1), 2 * (size - size * proportion))
        )
    )

    ci_width = ci_upper - ci_lower
    return float(ci_width)


def _ci_width_wald(proportion: float, size: float, alpha: float = 0.05) -> float:
    ci_lower = proportion - norm.ppf(1 - alpha / 2) * sqrt(proportion * (1 - proportion) / size)
    ci_upper = proportion + norm.ppf(1 - alpha / 2) * sqrt(proportion * (1 - proportion) / size)
    ci_width = min(ci_upper, 1) - max(ci_lower, 0)
    return float(ci_width)


def _ci_width_wald_cc(proportion: float, size: float, alpha: float = 0.05) -> float:
    ci_width = 2 * norm.ppf(1 - alpha / 2) * sqrt(proportion * (1 - proportion) / size) + 1 / size
    return float(ci_width)


def _ci_width_wilson(proportion: float, size: float, alpha: float = 0.05) -> float:
    ci_width = (
        norm.ppf(1 - alpha / 2)
        * sqrt(norm.ppf(1 - alpha / 2) ** 2 + 4 * size * proportion * (1 - proportion))
        / (size + norm.ppf(1 - alpha / 2) ** 2)
    )

    return float(ci_width)


def _ci_wilson_cc(proportion: float, size: float, alpha: float = 0.05) -> float:
    ci_lower = (
        (2 * size * proportion + norm.ppf(1 - alpha / 2) ** 2 - 1)
        - norm.ppf(1 - alpha / 2)
        * sqrt(norm.ppf(1 - alpha / 2) ** 2 - 1 / size + 4 * size * proportion * (1 - proportion) + 4 * proportion - 2)
    ) / (2 * (size + norm.ppf(1 - alpha / 2) ** 2))

    ci_upper = (
        (2 * size * proportion + norm.ppf(1 - alpha / 2) ** 2 + 1)
        + norm.ppf(1 - alpha / 2)
        * sqrt(norm.ppf(1 - alpha / 2) ** 2 - 1 / size + 4 * size * proportion * (1 - proportion) - 4 * proportion + 2)
    ) / (2 * (size + norm.ppf(1 - alpha / 2) ** 2))
    ci_width = ci_upper - ci_lower

    return float(ci_width)


def solve_size(
    proportion: float,
    ci_width: float,
    alpha: float = 0.05,
    method: str = "clopper_pearson",
    continuity_correction: bool = False,
) -> float:
    """Estimate the sample size required to achieve a given confidence interval for one proportion.

    Args:
        proportion (float): Proportion.
        ci_width (float): Confidence interval width.
        alpha (float, optional): Significance level. Default is 0.05.
        method (str, optional): Specify the method for calculating confidence interval. Default is `clopper_pearson`.
        continuity_correction (bool, optional): Specify whether or not the continuity correction is used, only valid for `method` = `wald` or `wilson`. Default is False.

    Returns:
        size(float): The required sample size.
    """

    def func(size: float) -> float:
        return _ci_width(proportion, size, alpha, method, continuity_correction) - ci_width

    if method == "wilson" and continuity_correction:
        # wilson score 连续性校正公式中的分子可能存在对负数开算术平方根的情况，这可能会导致置信区间宽度计算失败，因此需要先缩小 brentq 搜索范围
        a = 4 * proportion * (1 - proportion)
        b = norm.ppf(1 - alpha / 2) ** 2 - 4 * proportion + 2
        c = -1
        n1 = (-b - sqrt(b**2 - 4 * a * c)) / (2 * a)
        n2 = (-b + sqrt(b**2 - 4 * a * c)) / (2 * a)
        lower_bound = max(n1, n2)
        upper_bound = SAMPLE_SIZE_SEARCH_MAX

        # wilson score 连续性校正计算出的置信区间宽度并随样本量增大而单调减小，而是在小样本区间内先增大，随着样本量继续增大，置信区间宽度逐渐减小。
        # 因此，直接使用 brentq 可能无法收敛，必须先找到置信区间的极大值点 $n'$，然后将 brentq 的搜索区间限定为 $[n', 10^6]$，才能保证收敛。
        res: OptimizeResult = minimize_scalar(lambda size: -func(size), bounds=(lower_bound, upper_bound))
        if -res.fun < ci_width:
            raise ValueError("No solution found.")
        else:
            lower_bound = max(lower_bound, res.x)

        size = brentq(func, lower_bound, upper_bound)
    else:
        size = brentq(func, 0.000001, SAMPLE_SIZE_SEARCH_MAX)

    return float(size)


def solve_ci_width(
    proportion: float,
    size: float,
    alpha: float = 0.05,
    method: str = "clopper-pearson",
    continuity_correction: bool = True,
) -> float:
    """Calculate the confidence interval width for one proportion.

    Args:
        proportion (float): Proportion.
        size (float): Sample size.
        alpha (float, optional): Significance level. Default is 0.05.
        method (str, optional): Specify the method for calculating confidence interval. Default is `clopper_pearson`.
        continuity_correction (bool, optional): Specify whether or not the continuity correction is used, only valid for `method` = `wald` or `wilson`. Default is False.

    Returns:
        ci_width(float): The confidence interval width.
    """

    return _ci_width(proportion, size, alpha, method, continuity_correction)


def solve_proportion(
    size: float,
    ci_width: float,
    alpha: float = 0.05,
    method: str = "clopper_pearson",
    continuity_correction: bool = False,
    side: str = "upper",
) -> float:
    """Estimate the proportion required to achieve a given confidence interval for one proportion.

    Args:
        size (float): Sample size.
        ci_width (float): Confidence interval width.
        alpha (float, optional): Significance level. Default is 0.05.
        method (str, optional): The method for calculating confidence interval. Default is `clopper_pearson`.
        continuity_correction (bool, optional): Whether or not the continuity correction is used, only valid for `method` = `wald` or `wilson`. Default is False.
        side (str, optional): Which root to return. Must be `lower` (proportion closer to 0) or `upper` (proportion closer to 1). Default is `upper`.

    Returns:
        ci_width(float): The confidence interval width.
    """

    def func(proportion: float) -> float:
        return _ci_width(proportion, size, alpha, method, continuity_correction) - ci_width

    match side.lower():
        case "lower":
            proportion = brentq(func, 0.000001, 0.5)
        case "upper":
            proportion = brentq(func, 0.5, 0.999999)
        case _:
            raise ValueError("side must be 'lower' or 'upper'")

    return proportion
