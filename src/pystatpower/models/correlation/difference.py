from math import log

from scipy.stats import norm


def size(alpha: float, power: float, null_correlation: float, correlation: float) -> float:
    """相关系数差异性检验样本量计算

    Args:
        alpha (float): 显著性水平
        power (float): 检验效能
        null_correlation (float): 零假设下的样本相关系数
        correlation (float): 备择假设下的样本相关系数

    Returns:
        size(float): 样本量
    """
    size = (
        4
        * (norm.ppf(1 - alpha / 2) + norm.ppf(power)) ** 2
        / log(((1 + correlation) * (1 - null_correlation)) / ((1 - correlation) * (1 + null_correlation))) ** 2
        + 3
    )
    return float(size)
