"""两独立样本差异性检验"""

from enum import Enum, Flag, auto, unique
from math import asin, sqrt

from scipy.stats import norm
from scipy.optimize import brentq

from pystatpower.basic import Alpha, Interval, Power, PowerAnalysisOption, Proportion, Size


@unique
class Alternative(Enum, metaclass=PowerAnalysisOption):
    """备择假设类型

    Attributes
    ----------
        TWO_SIDED : (int)
            双侧检验
        ONE_SIDED : (int)
            单侧检验
    """

    TWO_SIDED = 1
    ONE_SIDED = 2


@unique
class TestType(Enum, metaclass=PowerAnalysisOption):
    """检验类型

    Attributes
    ----------
        Z_TEST_POOLED : (int)
            Z 检验（合并方差）
        Z_TEST_UNPOOLED : (int)
            Z 检验（独立方差）
        Z_TEST_CC_POOLED : (int)
            Z 检验（连续性校正，合并方差）
        Z_TEST_CC_UNPOOLED : (int)
            Z 检验（连续性校正，独立方差）
    """

    Z_TEST_POOLED = 1
    Z_TEST_UNPOOLED = 2
    Z_TEST_CC_POOLED = 3
    Z_TEST_CC_UNPOOLED = 4


@unique
class SearchDirection(Enum, metaclass=PowerAnalysisOption):
    """搜索方向

    Attributes
    ----------
        LESS : (int)
            向下搜索
        GREATER : (int)
            向上搜索
    """

    LESS = 1
    GREATER = 2


class GroupAllocationOption(Flag, metaclass=PowerAnalysisOption):
    """样本量分配类型（求解目标：样本量）

    Attributes
    ----------
        EQUAL
            等量分配
        SIZE_OF_TOTAL
            总样本量
        SIZE_OF_EACH
            单组样本量
        SIZE_OF_TREATMENT
            试验组样本量
        SIZE_OF_REFERENCE
            对照组样本量
        RATIO_OF_TREATMENT_TO_REFERENCE
            试验组与对照组样本量比例
        RATIO_OF_REFERENCE_TO_TREATMENT
            对照组与试验组样本量比例
        PERCENT_OF_TREATMENT
            试验组样本百分比
        PERCENT_OF_REFERENCE
            对照组样本百分比
    """

    EQUAL = auto()
    SIZE_OF_TOTAL = auto()
    SIZE_OF_EACH = auto()
    SIZE_OF_TREATMENT = auto()
    SIZE_OF_REFERENCE = auto()
    RATIO_OF_TREATMENT_TO_REFERENCE = auto()
    RATIO_OF_REFERENCE_TO_TREATMENT = auto()
    PERCENT_OF_TREATMENT = auto()
    PERCENT_OF_REFERENCE = auto()


class GroupAllocation:
    class ForSize:
        def __init__(
            self,
            group_allocation_option: GroupAllocationOption = GroupAllocationOption.EQUAL,
            size_of_treatment: float = None,
            size_of_reference: float = None,
            ratio_of_treatment_to_reference: float = None,
            ratio_of_reference_to_treatment: float = None,
            percent_of_treatment: float = None,
            percent_of_reference: float = None,
        ):
            self.group_allocation_option = group_allocation_option
            match group_allocation_option:
                case GroupAllocationOption.EQUAL:
                    self.treatment_size_formula = lambda n: n
                    self.reference_size_formula = lambda n: n
                case GroupAllocationOption.SIZE_OF_TREATMENT:
                    self.treatment_size_formula = lambda n: size_of_treatment
                    self.reference_size_formula = lambda n: n
                case GroupAllocationOption.SIZE_OF_REFERENCE:
                    self.treatment_size_formula = lambda n: n
                    self.reference_size_formula = lambda n: size_of_reference
                case GroupAllocationOption.RATIO_OF_TREATMENT_TO_REFERENCE:
                    self.treatment_size_formula = lambda n: ratio_of_treatment_to_reference * n
                    self.reference_size_formula = lambda n: n
                case GroupAllocationOption.RATIO_OF_REFERENCE_TO_TREATMENT:
                    self.treatment_size_formula = lambda n: n
                    self.reference_size_formula = lambda n: ratio_of_reference_to_treatment * n
                case GroupAllocationOption.PERCENT_OF_TREATMENT:
                    self.treatment_size_formula = lambda n: n
                    self.reference_size_formula = lambda n: (1 - percent_of_treatment) / percent_of_treatment * n
                case GroupAllocationOption.PERCENT_OF_REFERENCE:
                    self.treatment_size_formula = lambda n: (1 - percent_of_reference) / percent_of_reference * n
                    self.reference_size_formula = lambda n: n
                case _:
                    raise ValueError("未知的样本量分配类型")

    class ForNotSize:
        def __init__(
            self,
            group_allocation_option: GroupAllocationOption,
            size_of_total: float = None,
            size_of_each: float = None,
            size_of_treatment: float = None,
            size_of_reference: float = None,
            ratio_of_treatment_to_reference: float = None,
            ratio_of_reference_to_treatment: float = None,
            percent_of_treatment: float = None,
            percent_of_reference: float = None,
        ):
            match group_allocation_option:
                case x if x == GroupAllocationOption.EQUAL | GroupAllocationOption.SIZE_OF_TOTAL:
                    self.treatment_size_formula = lambda: size_of_total / 2
                    self.reference_size_formula = lambda: size_of_total / 2
                case x if x == GroupAllocationOption.EQUAL | GroupAllocationOption.SIZE_OF_EACH:
                    self.treatment_size_formula = lambda: size_of_each
                    self.reference_size_formula = lambda: size_of_each
                case x if x == GroupAllocationOption.EQUAL | GroupAllocationOption.SIZE_OF_TREATMENT:
                    self.treatment_size_formula = lambda: size_of_treatment
                    self.reference_size_formula = lambda: size_of_treatment
                case x if x == GroupAllocationOption.EQUAL | GroupAllocationOption.SIZE_OF_REFERENCE:
                    self.treatment_size_formula = lambda: size_of_reference
                    self.reference_size_formula = lambda: size_of_reference
                case x if x == GroupAllocationOption.SIZE_OF_TOTAL | GroupAllocationOption.SIZE_OF_TREATMENT:
                    self.treatment_size_formula = lambda: size_of_treatment
                    self.reference_size_formula = lambda: size_of_total - size_of_treatment
                case x if x == GroupAllocationOption.SIZE_OF_TOTAL | GroupAllocationOption.SIZE_OF_REFERENCE:
                    self.treatment_size_formula = lambda: size_of_total - size_of_reference
                    self.reference_size_formula = lambda: size_of_reference
                case (
                    x
                ) if x == GroupAllocationOption.SIZE_OF_TOTAL | GroupAllocationOption.RATIO_OF_TREATMENT_TO_REFERENCE:
                    self.treatment_size_formula = (
                        lambda: size_of_total * ratio_of_treatment_to_reference / (1 + ratio_of_treatment_to_reference)
                    )
                    self.reference_size_formula = lambda: size_of_total / (1 + ratio_of_treatment_to_reference)
                case (
                    x
                ) if x == GroupAllocationOption.SIZE_OF_TOTAL | GroupAllocationOption.RATIO_OF_REFERENCE_TO_TREATMENT:
                    self.treatment_size_formula = lambda: size_of_total / (1 + ratio_of_reference_to_treatment)
                    self.reference_size_formula = lambda: (
                        size_of_total * ratio_of_reference_to_treatment / (1 + ratio_of_reference_to_treatment)
                    )
                case x if x == GroupAllocationOption.SIZE_OF_TOTAL | GroupAllocationOption.PERCENT_OF_TREATMENT:
                    self.treatment_size_formula = lambda: size_of_total * percent_of_treatment
                    self.reference_size_formula = lambda: size_of_total * (1 - percent_of_treatment)
                case x if x == GroupAllocationOption.SIZE_OF_TOTAL | GroupAllocationOption.PERCENT_OF_REFERENCE:
                    self.treatment_size_formula = lambda: size_of_total * (1 - percent_of_reference)
                    self.reference_size_formula = lambda: size_of_total * percent_of_reference
                case x if x == GroupAllocationOption.SIZE_OF_EACH:
                    self.treatment_size_formula = lambda: size_of_each
                    self.reference_size_formula = lambda: size_of_each
                case x if x == GroupAllocationOption.SIZE_OF_TREATMENT | GroupAllocationOption.SIZE_OF_REFERENCE:
                    self.treatment_size_formula = lambda: size_of_treatment
                    self.reference_size_formula = lambda: size_of_reference
                case (
                    x
                ) if x == GroupAllocationOption.SIZE_OF_TREATMENT | GroupAllocationOption.RATIO_OF_TREATMENT_TO_REFERENCE:
                    self.treatment_size_formula = lambda: size_of_treatment
                    self.reference_size_formula = lambda: size_of_treatment / ratio_of_treatment_to_reference
                case (
                    x
                ) if x == GroupAllocationOption.SIZE_OF_TREATMENT | GroupAllocationOption.RATIO_OF_REFERENCE_TO_TREATMENT:
                    self.treatment_size_formula = lambda: size_of_treatment
                    self.reference_size_formula = lambda: size_of_treatment * ratio_of_reference_to_treatment
                case x if x == GroupAllocationOption.SIZE_OF_TREATMENT | GroupAllocationOption.PERCENT_OF_TREATMENT:
                    self.treatment_size_formula = lambda: size_of_treatment
                    self.reference_size_formula = (
                        lambda: size_of_treatment * (1 - percent_of_treatment) / percent_of_treatment
                    )
                case x if x == GroupAllocationOption.SIZE_OF_TREATMENT | GroupAllocationOption.PERCENT_OF_REFERENCE:
                    self.treatment_size_formula = lambda: size_of_treatment
                    self.reference_size_formula = (
                        lambda: size_of_treatment * percent_of_reference / (1 - percent_of_reference)
                    )
                case (
                    x
                ) if x == GroupAllocationOption.SIZE_OF_REFERENCE | GroupAllocationOption.RATIO_OF_TREATMENT_TO_REFERENCE:
                    self.treatment_size_formula = lambda: size_of_reference * ratio_of_treatment_to_reference
                    self.reference_size_formula = lambda: size_of_reference
                case (
                    x
                ) if x == GroupAllocationOption.SIZE_OF_REFERENCE | GroupAllocationOption.RATIO_OF_REFERENCE_TO_TREATMENT:
                    self.treatment_size_formula = lambda: size_of_reference / ratio_of_reference_to_treatment
                    self.reference_size_formula = lambda: size_of_reference
                case x if x == GroupAllocationOption.SIZE_OF_REFERENCE | GroupAllocationOption.PERCENT_OF_TREATMENT:
                    self.treatment_size_formula = (
                        lambda: size_of_reference * percent_of_treatment / (1 - percent_of_treatment)
                    )
                    self.reference_size_formula = lambda: size_of_reference
                case x if x == GroupAllocationOption.SIZE_OF_REFERENCE | GroupAllocationOption.PERCENT_OF_REFERENCE:
                    self.treatment_size_formula = (
                        lambda: size_of_reference * (1 - percent_of_reference) / percent_of_reference
                    )
                    self.reference_size_formula = lambda: size_of_reference
                case _:
                    raise ValueError("未知的样本量分配类型")

    ForAlpha = ForNotSize
    ForPower = ForNotSize
    ForTreatmentProportion = ForNotSize
    ForReferenceProportion = ForNotSize


def fun_power(
    alpha: float,
    treatment_n: float,
    reference_n: float,
    treatment_proportion: float,
    reference_proportion: float,
    alternative: Alternative,
    test_type: TestType,
):
    n1 = treatment_n
    n2 = reference_n
    p1 = treatment_proportion
    p2 = reference_proportion
    q1 = 1 - p1
    q2 = 1 - p2

    p_bar = (n1 * p1 + n2 * p2) / (n1 + n2)
    q_bar = 1 - p_bar

    se_p = sqrt(p_bar * q_bar * (1 / n1 + 1 / n2))
    se_u = sqrt(p1 * q1 / n1 + p2 * q2 / n2)

    # 计算标准误
    match test_type:
        case TestType.Z_TEST_POOLED | TestType.Z_TEST_CC_POOLED:
            se = se_p
        case TestType.Z_TEST_UNPOOLED | TestType.Z_TEST_CC_UNPOOLED:
            se = se_u
        case _:
            assert False, "未知的检验类型"

    # 连续性校正
    c = 0
    if test_type in [TestType.Z_TEST_CC_POOLED, TestType.Z_TEST_CC_UNPOOLED]:
        c = (1 / 2) * (1 / n1 + 1 / n2)

    # 计算检验效能
    match alternative:
        case Alternative.TWO_SIDED:
            z_alpha = norm.ppf(1 - alpha / 2)
            power = (
                norm.cdf((-z_alpha * se - c - (p1 - p2)) / se_u) + 1 - norm.cdf((z_alpha * se + c - (p1 - p2)) / se_u)
            )
        case Alternative.ONE_SIDED:
            z_alpha = norm.ppf(1 - alpha)
            if p1 > p2:
                power = 1 - norm.cdf((z_alpha * se + c - (p1 - p2)) / se_u)
            elif p1 <= p2:
                power = norm.cdf((-z_alpha * se - c - (p1 - p2)) / se_u)
        case _:
            assert False, "未知的备择假设类型"

    return power


class TwoProportion:
    class ForSize:
        def __init__(
            self,
            alpha: Alpha,
            power: Power,
            treatment_proportion: Proportion,
            reference_proportion: Proportion,
            alternative: Alternative,
            test_type: TestType,
            group_allocation: GroupAllocation.ForSize,
        ):
            self.alpha = alpha
            self.power = power
            self.treatment_proportion = treatment_proportion
            self.reference_proportion = reference_proportion
            self.alternative = alternative
            self.test_type = test_type
            self.group_allocation = group_allocation

        def solve(self):
            self._eval = (
                lambda n: fun_power(
                    self.alpha,
                    self.group_allocation.treatment_size_formula(n),
                    self.group_allocation.reference_size_formula(n),
                    self.treatment_proportion,
                    self.reference_proportion,
                    self.alternative,
                    self.test_type,
                )
                - self.power
            )
            try:
                n = brentq(self._eval, 1, 1e10)
            except ValueError as e:
                raise ValueError("无解") from e
            self.treatment_size = Size(self.group_allocation.treatment_size_formula(n))
            self.reference_size = Size(self.group_allocation.reference_size_formula(n))

    class ForAlpha:
        def __init__(
            self,
            power: Power,
            treatment_proportion: Proportion,
            reference_proportion: Proportion,
            alternative: Alternative,
            test_type: TestType,
            group_allocation: GroupAllocation.ForAlpha,
        ):
            self.power = power
            self.treatment_proportion = treatment_proportion
            self.reference_proportion = reference_proportion
            self.alternative = alternative
            self.test_type = test_type
            self.group_allocation = group_allocation

        def solve(self):
            self._eval = (
                lambda alpha: fun_power(
                    alpha,
                    self.group_allocation.treatment_size_formula(),
                    self.group_allocation.reference_size_formula(),
                    self.treatment_proportion,
                    self.reference_proportion,
                    self.alternative,
                    self.test_type,
                )
                - self.power
            )
            try:
                alpha = brentq(self._eval, 0, 1)
            except ValueError as e:
                raise ValueError("无解") from e
            self.alpha = Alpha(alpha)
            self.treatment_size = Size(self.group_allocation.treatment_size_formula())
            self.reference_size = Size(self.group_allocation.reference_size_formula())

    class ForPower:
        def __init__(
            self,
            alpha: Alpha,
            treatment_proportion: Proportion,
            reference_proportion: Proportion,
            alternative: Alternative,
            test_type: TestType,
            group_allocation: GroupAllocation.ForPower,
        ):
            self.alpha = alpha
            self.treatment_proportion = treatment_proportion
            self.reference_proportion = reference_proportion
            self.alternative = alternative
            self.test_type = test_type
            self.group_allocation = group_allocation

        def solve(self):
            power = fun_power(
                self.alpha,
                self.group_allocation.treatment_size_formula(),
                self.group_allocation.reference_size_formula(),
                self.treatment_proportion,
                self.reference_proportion,
                self.alternative,
                self.test_type,
            )
            self.power = Power(power)
            self.treatment_size = Size(self.group_allocation.treatment_size_formula())
            self.reference_size = Size(self.group_allocation.reference_size_formula())

    class ForTreatmentProportion:
        def __init__(
            self,
            alpha: Alpha,
            power: Power,
            reference_proportion: Proportion,
            alternative: Alternative,
            test_type: TestType,
            group_allocation: GroupAllocation.ForTreatmentProportion,
            search_direction: SearchDirection,
        ):
            self.alpha = alpha
            self.power = power
            self.reference_proportion = reference_proportion
            self.alternative = alternative
            self.test_type = test_type
            self.group_allocation = group_allocation
            self.search_direction = search_direction

        def solve(self):
            self._eval = (
                lambda treatment_proportion: fun_power(
                    self.alpha,
                    self.group_allocation.treatment_size_formula(),
                    self.group_allocation.reference_size_formula(),
                    treatment_proportion,
                    self.reference_proportion,
                    self.alternative,
                    self.test_type,
                )
                - self.power
            )

            match self.search_direction:
                case SearchDirection.LESS:
                    lbound, ubound = Interval(0, self.reference_proportion).pseudo_bound()
                    try:
                        treatment_proportion = brentq(self._eval, lbound, ubound)
                    except ValueError as e:
                        raise ValueError("无解") from e
                case SearchDirection.GREATER:
                    lbound, ubound = Interval(self.reference_proportion, 1).pseudo_bound()
                    try:
                        treatment_proportion = brentq(self._eval, lbound, ubound)
                    except ValueError as e:
                        raise ValueError("无解") from e
                case _:
                    assert False, "未知的搜索方向"

            self.treatment_proportion = Proportion(treatment_proportion)
            self.treatment_size = Size(self.group_allocation.treatment_size_formula())
            self.reference_size = Size(self.group_allocation.reference_size_formula())

    class ForReferenceProportion:
        def __init__(
            self,
            alpha: Alpha,
            power: Power,
            treatment_proportion: Proportion,
            alternative: Alternative,
            test_type: TestType,
            group_allocation: GroupAllocation.ForReferenceProportion,
            search_direction: SearchDirection,
        ):
            self.alpha = alpha
            self.power = power
            self.treatment_proportion = treatment_proportion
            self.alternative = alternative
            self.test_type = test_type
            self.group_allocation = group_allocation
            self.search_direction = search_direction

        def solve(self):
            self._eval = (
                lambda reference_proportion: fun_power(
                    self.alpha,
                    self.group_allocation.treatment_size_formula(),
                    self.group_allocation.reference_size_formula(),
                    self.treatment_proportion,
                    reference_proportion,
                    self.alternative,
                    self.test_type,
                )
                - self.power
            )
            match self.search_direction:
                case SearchDirection.LESS:
                    lbound, ubound = Interval(0, self.treatment_proportion).pseudo_bound()
                    try:
                        reference_proportion = brentq(self._eval, lbound, ubound)
                    except ValueError as e:
                        raise ValueError("无解") from e
                case SearchDirection.GREATER:
                    lbound, ubound = Interval(self.treatment_proportion, 1).pseudo_bound()
                    try:
                        reference_proportion = brentq(self._eval, lbound, ubound)
                    except ValueError as e:
                        raise ValueError("无解") from e
                case _:
                    assert False, "未知的搜索方向"
            self.reference_proportion = Proportion(reference_proportion)
            self.treatment_size = Size(self.group_allocation.treatment_size_formula())
            self.reference_size = Size(self.group_allocation.reference_size_formula())


def solve_for_sample_size(
    alpha: float,
    power: float,
    treatment_proportion: float,
    reference_proportion: float,
    alternative: str,
    test_type: str,
    group_allocation: GroupAllocation.ForSize = GroupAllocation.ForSize(GroupAllocationOption.EQUAL),
    full_output: bool = False,
):
    model = TwoProportion.ForSize(
        alpha=Alpha(alpha),
        power=Power(power),
        alternative=Alternative[alternative],
        test_type=TestType[test_type],
        treatment_proportion=Proportion(treatment_proportion),
        reference_proportion=Proportion(reference_proportion),
        group_allocation=group_allocation,
    )
    model.solve()

    if full_output:
        return model
    return model.treatment_size, model.reference_size


def solve_for_alpha(
    power: float,
    treatment_proportion: float,
    reference_proportion: float,
    alternative: str,
    test_type: str,
    group_allocation: GroupAllocation.ForAlpha,
    full_output: bool = False,
):
    model = TwoProportion.ForAlpha(
        power=Power(power),
        alternative=Alternative[alternative],
        test_type=TestType[test_type],
        treatment_proportion=Proportion(treatment_proportion),
        reference_proportion=Proportion(reference_proportion),
        group_allocation=group_allocation,
    )
    model.solve()

    if full_output:
        return model
    return model.alpha


def solve_for_power(
    alpha: float,
    treatment_proportion: float,
    reference_proportion: float,
    alternative: str,
    test_type: str,
    group_allocation: GroupAllocation.ForPower,
    full_output: bool = False,
):
    model = TwoProportion.ForPower(
        alpha=Alpha(alpha),
        alternative=Alternative[alternative],
        test_type=TestType[test_type],
        treatment_proportion=Proportion(treatment_proportion),
        reference_proportion=Proportion(reference_proportion),
        group_allocation=group_allocation,
    )
    model.solve()

    if full_output:
        return model
    return model.power


def solve_for_treatment_proportion(
    alpha: float,
    power: float,
    reference_proportion: float,
    alternative: str,
    test_type: str,
    group_allocation: GroupAllocation.ForTreatmentProportion,
    search_direction: SearchDirection,
    full_output: bool = False,
):
    model = TwoProportion.ForTreatmentProportion(
        alpha=Alpha(alpha),
        power=Power(power),
        alternative=Alternative[alternative],
        test_type=TestType[test_type],
        reference_proportion=Proportion(reference_proportion),
        group_allocation=group_allocation,
        search_direction=SearchDirection[search_direction],
    )
    model.solve()

    if full_output:
        return model
    return model.treatment_proportion


def solve_for_reference_proportion(
    alpha: float,
    power: float,
    treatment_proportion: float,
    alternative: str,
    test_type: str,
    group_allocation: GroupAllocation.ForReferenceProportion,
    search_direction: str,
    full_output: bool = False,
):
    model = TwoProportion.ForReferenceProportion(
        alpha=Alpha(alpha),
        power=Power(power),
        alternative=Alternative[alternative],
        test_type=TestType[test_type],
        treatment_proportion=Proportion(treatment_proportion),
        group_allocation=group_allocation,
        search_direction=SearchDirection[search_direction],
    )
    model.solve()

    if full_output:
        return model
    return model.reference_proportion
