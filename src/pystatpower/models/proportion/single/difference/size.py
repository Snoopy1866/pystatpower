from math import sqrt

from scipy.stats import norm


def _continuity_correction(size_not_cc: float, proportion: float, null_proportion: float) -> float:
    return size_not_cc / 4 * (1 + sqrt(1 + 2 / (abs(proportion - null_proportion) * size_not_cc))) ** 2


def _size_phat(alpha: float, power: float, proportion: float, null_proportion: float) -> float:
    size = (
        (norm.ppf(1 - alpha / 2) + norm.ppf(power)) ** 2
        * proportion
        * (1 - proportion)
        / (proportion - null_proportion) ** 2
    )
    return size


def _size_phat_cc(alpha: float, power: float, proportion: float, null_proportion: float) -> float:
    size_not_cc = _size_phat(alpha, power, proportion, null_proportion)
    size = _continuity_correction(size_not_cc, proportion, null_proportion)
    return size


def _size_p0(alpha: float, power: float, proportion: float, null_proportion: float) -> float:
    size = (
        norm.ppf(1 - alpha / 2) * sqrt(null_proportion * (1 - null_proportion))
        + norm.ppf(power) * sqrt(proportion * (1 - proportion))
    ) ** 2 / (proportion - null_proportion) ** 2
    return size


def _size_p0_cc(alpha: float, power: float, proportion: float, null_proportion: float) -> float:
    size_not_cc = _size_p0(alpha, power, proportion, null_proportion)
    size = _continuity_correction(size_not_cc, proportion, null_proportion)
    return size


def size(
    alpha: float,
    power: float,
    proportion: float,
    null_proportion: float,
    phat: bool = False,
    continuity_correction: bool = False,
) -> float:
    """单样本率差异性检验样本量计算

    Args:
        alpha (float): 显著性水平
        power (float): 检验效能
        proportion (float): 备择假设下的样本率
        null_proportion (float): 零假设下的样本率
        phat (bool, optional): 是否使用样本率计算标准差。默认为 `False`。
        continuity_correction (bool, optional): 是否进行连续性校正。默认为 `False`。

    Returns:
        size: 样本量
    """
    match (phat, continuity_correction):
        case (True, True):
            size = _size_phat_cc(alpha, power, proportion, null_proportion)
        case (True, False):
            size = _size_phat(alpha, power, proportion, null_proportion)
        case (False, True):
            size = _size_p0_cc(alpha, power, proportion, null_proportion)
        case (False, False):
            size = _size_p0(alpha, power, proportion, null_proportion)

    return size
