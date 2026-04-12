from math import ceil, sqrt

from scipy.optimize import brentq
from scipy.stats import norm

from ...._constant import SAMPLE_SIZE_SEARCH_MAX


def _power_pooled(
    treatment_proportion: float,
    reference_proportion: float,
    magin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
) -> float:
    pooled_proportion = (treatment_size * treatment_proportion + reference_size * reference_proportion) / (
        treatment_size + reference_size
    )
    power = 1 - norm.cdf(
        (
            norm.ppf(1 - alpha)
            * sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))
            - abs(treatment_proportion - reference_proportion - magin)
        )
        / sqrt(
            treatment_proportion * (1 - treatment_proportion) / treatment_size
            + reference_proportion * (1 - reference_proportion) / reference_size
        )
    )
    return float(power)


def _power_pooled_cc(
    treatment_proportion: float,
    reference_proportion: float,
    magin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
) -> float:
    pooled_proportion = (treatment_size * treatment_proportion + reference_size * reference_proportion) / (
        treatment_size + reference_size
    )
    power = 1 - norm.cdf(
        (
            norm.ppf(1 - alpha)
            * sqrt(pooled_proportion * (1 - pooled_proportion) * (1 / treatment_size + 1 / reference_size))
            - abs(
                treatment_proportion - reference_proportion - magin - 1 / 2 * (1 / treatment_size + 1 / reference_size)
            )
        )
        / sqrt(
            treatment_proportion * (1 - treatment_proportion) / treatment_size
            + reference_proportion * (1 - reference_proportion) / reference_size
        )
    )
    return float(power)


def _power_unpooled(
    treatment_proportion: float,
    reference_proportion: float,
    magin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
) -> float:
    power = 1 - norm.cdf(
        norm.ppf(1 - alpha)
        - abs(treatment_proportion - reference_proportion - magin)
        / sqrt(
            treatment_proportion * (1 - treatment_proportion) / treatment_size
            + reference_proportion * (1 - reference_proportion) / reference_size
        )
    )
    return float(power)


def _power_unpooled_cc(
    treatment_proportion: float,
    reference_proportion: float,
    magin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
) -> float:
    power = 1 - norm.cdf(
        norm.ppf(1 - alpha)
        - abs(treatment_proportion - reference_proportion - magin - 1 / 2 * (1 / treatment_size + 1 / reference_size))
        / sqrt(
            treatment_proportion * (1 - treatment_proportion) / treatment_size
            + reference_proportion * (1 - reference_proportion) / reference_size
        )
    )
    return float(power)


def _power(
    treatment_proportion: float,
    reference_proportion: float,
    magin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> float:
    if pooled:
        if continuity_correction:
            return _power_pooled_cc(
                treatment_proportion, reference_proportion, magin, treatment_size, reference_size, alpha
            )
        else:
            return _power_pooled(
                treatment_proportion, reference_proportion, magin, treatment_size, reference_size, alpha
            )
    else:
        if continuity_correction:
            return _power_unpooled_cc(
                treatment_proportion, reference_proportion, magin, treatment_size, reference_size, alpha
            )
        else:
            return _power_unpooled(
                treatment_proportion, reference_proportion, magin, treatment_size, reference_size, alpha
            )


def solve_power(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> float:
    """Calculate the power of the non-inferiority test between two independent proportions.

    Args:
        treatment_proportion (float): Treatment proportion.
        reference_proportion (float): Reference proportion.
        margin (float): Non-inferiority margin, which should be negative when higher is better, otherwise positive.
        treatment_size (float): Treatment sample size.
        reference_size (float): Reference sample size.
        alpha (float, optional): One-sided significance level. Default is 0.05.
        pooled (bool, optional): Whether or not the pooled method is used. Default is False.
        continuity_correction (bool, optional): Whether or not the continuity correction is used. Default is False.

    Returns:
        power(float): Power of the test.
    """

    power = _power(
        treatment_proportion,
        reference_proportion,
        margin,
        treatment_size,
        reference_size,
        alpha,
        pooled,
        continuity_correction,
    )
    return power


def solve_size(
    treatment_proportion: float,
    reference_proportion: float,
    margin: float,
    ratio: float = 1,
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> tuple[int, int]:
    """Estimate the sample size required for the non-inferiority test between two independent proportions.

    Args:
        treatment_proportion (float): Treatment proportion.
        reference_proportion (float): Reference proportion.
        margin (float): Non-inferiority margin, which should be negative when higher is better, otherwise positive.
        ratio (float, optional): Ratio of the sample size of the treatment group to the reference group. Default is 1.
        alpha (float, optional): One-sided significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.80.
        pooled (bool, optional): Whether or not the pooled method is used. Default is False.
        continuity_correction (bool, optional): Whether or not the continuity correction is used. Default is False.

    Returns:
        size(tuple[int, int]): The required sample size.
    """

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _power(
                    treatment_proportion,
                    reference_proportion,
                    margin,
                    reference_size * ratio,
                    reference_size,
                    alpha,
                    pooled,
                    continuity_correction,
                )
                - power
            )

        reference_size = int(ceil(brentq(func, 0.000001, SAMPLE_SIZE_SEARCH_MAX)))
        treatment_size = int(ceil(reference_size * ratio))
        return treatment_size, reference_size
    else:

        def func(treatment_size: float) -> float:
            return (
                _power(
                    treatment_proportion,
                    reference_proportion,
                    margin,
                    treatment_size,
                    treatment_size * (1 / ratio),
                    alpha,
                    pooled,
                    continuity_correction,
                )
                - power
            )

        treatment_size = ceil(brentq(func, 0.000001, SAMPLE_SIZE_SEARCH_MAX))
        reference_size = ceil(treatment_size * (1 / ratio))
        return float(treatment_size), float(reference_size)


def solve_treatment_proportion(
    reference_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> float:
    """Estimate the treatment proportion required for the non-inferiority test between two independent proportions.

    Args:
        reference_proportion (float): Reference proportion.
        margin (float): Non-inferiority margin, which should be negative when higher is better, otherwise positive.
        treatment_size (float): Treatment sample size.
        reference_size (float): Reference sample size.
        alpha (float, optional): One-sided significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.80.
        pooled (bool, optional): Whether or not the pooled method is used. Default is False.
        continuity_correction (bool, optional): Whether or not the continuity correction is used. Default is False.

    Returns:
        treatment_proportion(float): The required treatment proportion.
    """

    def func(treatment_proportion: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                margin,
                treatment_size,
                reference_size,
                alpha,
                pooled,
                continuity_correction,
            )
            - power
        )

    treatment_proportion = brentq(func, max(reference_proportion + margin, 0), 1)
    return treatment_proportion


def solve_reference_proportion(
    treatment_proportion: float,
    margin: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> float:
    """Estimate the reference proportion required for the non-inferiority test between two independent proportions.

    Args:
        treatment_proportion (float): Treatment proportion.
        margin (float): Non-inferiority margin, which should be negative when higher is better, otherwise positive.
        treatment_size (float): Treatment sample size.
        reference_size (float): Reference sample size.
        alpha (float, optional): One-sided significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.80.
        pooled (bool, optional): Whether or not the pooled method is used. Default is False.
        continuity_correction (bool, optional): Whether or not the continuity correction is used. Default is False.

    Returns:
        reference_proportion(float): The required reference proportion.
    """

    def func(reference_proportion: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                margin,
                treatment_size,
                reference_size,
                alpha,
                pooled,
                continuity_correction,
            )
            - power
        )

    reference_proportion = brentq(func, 0, min(treatment_proportion - margin, 1))
    return reference_proportion


def solve_margin(
    treatment_proportion: float,
    reference_proportion: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.05,
    power: float = 0.80,
    pooled: bool = False,
    continuity_correction: bool = False,
) -> float:
    """Estimate the non-inferiority margin required for the non-inferiority test between two independent proportions.

    Args:
        treatment_proportion (float): Treatment proportion.
        reference_proportion (float): Reference proportion.
        treatment_size (float): Treatment sample size.
        reference_size (float): Reference sample size.
        alpha (float, optional): One-sided significance level. Default is 0.05.
        power (float, optional): Power of the test. Default is 0.80.
        pooled (bool, optional): Whether or not the pooled method is used. Default is False.
        continuity_correction (bool, optional): Whether or not the continuity correction is used. Default is False.

    Returns:
        margin(float): The required non-inferiority margin.

    Notes:
        The non-inferiority margin should be negative when higher is better, otherwise positive.

        The range of the non-inferiority margin $(\delta)$ is determined by the treatment proportion $(p_1)$ and reference proportion $(p_2)$:

        $$
        \\begin{cases}
        (-p_1, \ 0) \cup (p_1-p_2, \ 1-p_2) & , \\text{if } p_1 > p_2 \\\\
        (-p_2, \ p_1-p_2) \cup (0, \ 1-p_2) & , \\text{if } p_1 < p_2 \\\\
        (-p_1, \ 0) \cup (0, \ 1-p_2)       & , \\text{if } p_1 = p_2
        \end{cases}
        $$
    """

    def func(margin: float) -> float:
        return (
            _power(
                treatment_proportion,
                reference_proportion,
                margin,
                treatment_size,
                reference_size,
                alpha,
                pooled,
                continuity_correction,
            )
            - power
        )

    if treatment_proportion > reference_proportion:
        if func(-treatment_proportion) * func(0) < 0:
            margin = brentq(func, -treatment_proportion, 0)
        elif func(treatment_proportion - reference_proportion) * func(1 - reference_proportion) < 0:
            margin = brentq(func, treatment_proportion - reference_proportion, 1 - reference_proportion)
    elif treatment_proportion < reference_proportion:
        if func(-reference_proportion) * func(treatment_proportion - reference_proportion) < 0:
            margin = brentq(func, -reference_proportion, treatment_proportion - reference_proportion)
        elif func(0) * func(1 - reference_proportion) < 0:
            margin = brentq(func, 0, 1 - reference_proportion)
    elif treatment_proportion == reference_proportion:
        if func(-treatment_proportion) * func(0) < 0:
            margin = brentq(func, -treatment_proportion, 0)
        elif func(0) * func(1 - reference_proportion) < 0:
            margin = brentq(func, 0, 1 - reference_proportion)

    return float(margin)


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
    """估算定性指标两独立样本非劣效检验的样本量

    Args:
        alpha (float): 显著性水平
        power (float): 检验效能
        treatment_proportion (float): 试验组指标值
        reference_proportion (float): 对照组指标值
        margin (float): 非劣界值
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
