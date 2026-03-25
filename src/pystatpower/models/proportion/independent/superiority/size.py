"""定性指标、两独立样本、优效性检验"""

from math import sqrt

from scipy.stats import norm

from .....constant import LOWER_LIMIT_OF_SAMPLE_SIZE
from .....restrict import Restrict


def _continuity_correction(
    original_size: float,
    alpha: float,
    power: float,
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    ratio: float,
) -> float:
    if alpha < power:
        corrected_size = (
            original_size
            / 4
            * (
                1
                + sqrt(
                    1
                    + 2 * (ratio + 1) / (ratio * (treatment_proportion - reference_proportion - margin) * original_size)
                )
            )
            ** 2
        )
    elif alpha > power:
        corrected_size = (
            original_size
            / 4
            * (
                -1
                + sqrt(
                    1
                    + 2 * (ratio + 1) / (ratio * (treatment_proportion - reference_proportion - margin) * original_size)
                )
            )
            ** 2
        )
    elif alpha == power:
        corrected_size = (ratio + 1) / (2 * ratio * (treatment_proportion - reference_proportion - margin))

    return float(corrected_size)


def _size_pooled(
    alpha: float,
    power: float,
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    ratio: float = 1,
    skip_restrict: bool = False,
) -> tuple[float, float]:
    if not skip_restrict and Restrict.is_power_lt_alpha(alpha, power):
        reference_size = LOWER_LIMIT_OF_SAMPLE_SIZE
    else:
        p_bar = (ratio * treatment_proportion + reference_proportion) / (ratio + 1)
        reference_size = (
            norm.ppf(1 - alpha) * sqrt(p_bar * (1 - p_bar) * (1 / ratio + 1))
            + norm.ppf(power)
            * sqrt(
                1 / ratio * treatment_proportion * (1 - treatment_proportion)
                + reference_proportion * (1 - reference_proportion)
            )
        ) ** 2 / (treatment_proportion - reference_proportion - margin) ** 2

    treatment_size = reference_size * ratio

    return float(treatment_size), float(reference_size)


def _size_pooled_cc(
    alpha: float,
    power: float,
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    ratio: float = 1,
) -> tuple[float, float]:
    original_size = _size_pooled(
        alpha, power, treatment_proportion, reference_proportion, margin, ratio, skip_restrict=True
    )[1]
    reference_size = _continuity_correction(
        original_size, alpha, power, treatment_proportion, reference_proportion, margin, ratio
    )
    treatment_proportion = reference_size * ratio

    return treatment_proportion, reference_size


def _size_unpooled(
    alpha: float,
    power: float,
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    ratio: float = 1,
    skip_restrict: bool = False,
) -> tuple[float, float]:
    if not skip_restrict and Restrict.is_power_lt_alpha(alpha, power):
        reference_size = LOWER_LIMIT_OF_SAMPLE_SIZE
    else:
        reference_size = (
            (norm.ppf(1 - alpha) + norm.ppf(power)) ** 2
            * (
                1 / ratio * treatment_proportion * (1 - treatment_proportion)
                + reference_proportion * (1 - reference_proportion)
            )
            / (treatment_proportion - reference_proportion - margin) ** 2
        )

    treatment_size = reference_size * ratio

    return float(treatment_size), float(reference_size)


def _size_unpooled_cc(
    alpha: float,
    power: float,
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    ratio: float = 1,
) -> tuple[float, float]:
    original_size = _size_unpooled(
        alpha, power, treatment_proportion, reference_proportion, margin, ratio, skip_restrict=True
    )[1]
    reference_size = _continuity_correction(
        original_size, alpha, power, treatment_proportion, reference_proportion, margin, ratio
    )
    treatment_size = reference_size * ratio

    return float(treatment_size), float(reference_size)


def size(
    alpha: float,
    power: float,
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    ratio: float = 1,
    pooled: bool = False,
    continuity_correction: bool = False,
):
    """估算定性指标两独立样本优效性检验的样本量

    Args:
        alpha (float): 显著性水平
        power (float): 检验效能
        treatment_proportion (float): 试验组指标值
        reference_proportion (float): 对照组指标值
        margin (float): 优效界值
        ratio (float): 样本量分配比例，试验组：对照组
        pooled (bool): 是否使用合并方差
        continuity_correction (bool): 是否使用连续性校正
    """

    if Restrict.is_alpha_gt_one_half(alpha):
        alpha = 1 - alpha

    if pooled:
        if continuity_correction:
            size_tuple = _size_pooled_cc(alpha, power, treatment_proportion, reference_proportion, margin, ratio)
        else:
            size_tuple = _size_pooled(alpha, power, treatment_proportion, reference_proportion, margin, ratio)
    else:
        if continuity_correction:
            size_tuple = _size_unpooled_cc(alpha, power, treatment_proportion, reference_proportion, margin, ratio)
        else:
            size_tuple = _size_unpooled(alpha, power, treatment_proportion, reference_proportion, margin, ratio)

    size_tuple = tuple(map(lambda size: max(size, LOWER_LIMIT_OF_SAMPLE_SIZE), size_tuple))

    return size_tuple
