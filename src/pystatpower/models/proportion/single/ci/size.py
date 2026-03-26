"""定性指标、单样本、置信区间"""

from math import sqrt

from scipy.optimize import brentq
from scipy.stats import f, norm

from .....constant import LOWER_LIMIT_OF_SAMPLE_SIZE


def _size_wald(alpha: float, proportion: float, ci_width: float):
    if 2 * (1 - proportion) <= ci_width < 2 * proportion:
        size = norm.ppf(1 - alpha / 2) ** 2 * proportion * (1 - proportion) / (proportion + ci_width - 1) ** 2
    elif ci_width < 2 * min(proportion, 1 - proportion):
        size = 4 * norm.ppf(1 - alpha / 2) ** 2 * proportion * (1 - proportion) / ci_width**2
    elif 2 * proportion <= ci_width < 2 * (1 - proportion):
        size = norm.ppf(1 - alpha / 2) ** 2 * proportion * (1 - proportion) / (proportion - ci_width) ** 2
    elif ci_width == 1:
        size = LOWER_LIMIT_OF_SAMPLE_SIZE
    return size


def _size_wald_cc(alpha: float, proportion: float, ci_width: float):
    A = norm.ppf(1 - alpha / 2) * sqrt(proportion * (1 - proportion))
    if 2 * (1 - proportion) <= ci_width < 1:
        size = 1 / (-A + sqrt(A**2 + 2 * (proportion + ci_width - 1))) ** 2
    elif ci_width < 2 * min(proportion, 1 - proportion):
        size = 1 / (-A + sqrt(A**2 + ci_width)) ** 2
    elif 2 * proportion <= ci_width < 1:
        size = 1 / (-A + sqrt(A**2 - 2 * (proportion - ci_width))) ** 2
    elif ci_width == 1:
        size = LOWER_LIMIT_OF_SAMPLE_SIZE
    return size


def _size_wilson(alpha: float, proportion: float, ci_width: float):
    A = ci_width**2
    B = (2 * ci_width**2 - 4 * proportion * (1 - proportion)) * norm.ppf(1 - alpha / 2) ** 2
    C = (ci_width**2 - 1) * norm.ppf(1 - alpha / 2) ** 4

    size = (-B + sqrt(B**2 - 4 * A * C)) / (2 * A)
    return size


def _size_wilson_cc(alpha: float, proportion: float, ci_width: float, maximum: float = 1e10):
    def ci_half_width(size: float, alpha: float, proportion: float):
        ci_lower = (
            (2 * size * proportion + norm.ppf(1 - alpha / 2) ** 2 - 1)
            - norm.ppf(1 - alpha / 2)
            * sqrt(
                norm.ppf(1 - alpha / 2) ** 2 - 1 / size + 4 * size * proportion * (1 - proportion) + 4 * proportion - 2
            )
        ) / (2 * (size + norm.ppf(1 - alpha / 2) ** 2))

        ci_upper = (
            (2 * size * proportion + norm.ppf(1 - alpha / 2) ** 2 + 1)
            + norm.ppf(1 - alpha / 2)
            * sqrt(
                norm.ppf(1 - alpha / 2) ** 2 - 1 / size + 4 * size * proportion * (1 - proportion) - 4 * proportion + 2
            )
        ) / (2 * (size + norm.ppf(1 - alpha / 2) ** 2))

        return ci_upper - ci_lower

    def f(size: float):
        return ci_half_width(size, alpha, proportion) - ci_width

    # 函数 f(x) 在 [0, +infinity] 内的函数值从 -infinity -> maximum -> -infinity，如果存在根，则大概率存在两个根，需要取最大的那个根
    if f(LOWER_LIMIT_OF_SAMPLE_SIZE) <= 0:
        return LOWER_LIMIT_OF_SAMPLE_SIZE
    else:
        size = brentq(f, LOWER_LIMIT_OF_SAMPLE_SIZE, maximum)
        return float(size)


def _size_clopper_pearson(alpha: float, proportion: float, ci_width: float):
    def ci_half_width(size: float, alpha: float, proportion: float):
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

        return ci_upper - ci_lower

    return brentq(lambda size: ci_half_width(size, alpha, proportion) - ci_width, 1e-10, 1e10)


def size(
    alpha: float,
    proportion: float,
    ci_width: float,
    method: str = "clopper_pearson",
    continuity_correction: bool = False,
):
    """估算定性指标单样本置信区间的样本量

    Args:
        alpha (float): 显著性水平
        proportion (float): 样本指标值
        ci_width (float): 置信区间宽度
        method (str, optional): 置信区间估计方法，可选 "wald", "wilson", "clopper_pearson"，默认为 "clopper_pearson"
        continuity_correction (bool, optional): 是否进行连续性校正，仅在 method 为 "wald" 和 "wilson" 时可用，默认为 False
    """

    match method:
        case "clopper_pearson":
            size = _size_clopper_pearson(alpha, proportion, ci_width)
        case "wald":
            if continuity_correction:
                size = _size_wald_cc(alpha, proportion, ci_width)
            else:
                size = _size_wald(alpha, proportion, ci_width)
        case "wilson":
            if continuity_correction:
                size = _size_wilson_cc(alpha, proportion, ci_width)
            else:
                size = _size_wilson(alpha, proportion, ci_width)
        case _:
            raise ValueError("method must be wald, wilson or clopper_pearson")

    return max(size, LOWER_LIMIT_OF_SAMPLE_SIZE)
