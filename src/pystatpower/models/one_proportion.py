"""单样本率检验的功效分析模块"""

from enum import Enum, unique
from math import sqrt

from scipy.stats import norm
from scipy.optimize import brentq

from pystatpower.basic import Alpha, Interval, Power, PowerAnalysisOption, Proportion, Size


__all__ = [
    "solve_for_sample_size",
    "solve_for_alpha",
    "solve_for_power",
    "solve_for_nullproportion",
    "solve_for_proportion",
]


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
    """检验类型枚举类。

    Attributes
    ----------
        EXACT_TEST : str
            精确检验
        Z_TEST_USING_S_P0 : str
            Z 检验，使用 S(P0) 作为标准差
        Z_TEST_USING_S_P0_CC : str
            Z 检验，使用 S(P0) 作为标准差，使用连续性校正
        Z_TEST_USING_S_PHAT : str
            Z 检验，使用 S(PHat) 作为标准差
        Z_TEST_USING_S_PHAT_CC : str
            Z 检验，使用 S(PHat) 作为标准差，使用连续性校正
    """

    EXACT_TEST = "Exact Test"
    Z_TEST_USING_S_P0 = "Z-Test using S(P0)"
    Z_TEST_USING_S_P0_CC = "Z-Test using S(P0) with Continuity Correction"
    Z_TEST_USING_S_PHAT = "Z-Test using S(PHat)"
    Z_TEST_USING_S_PHAT_CC = "Z-Test using S(PHat) with Continuity Correction"


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


def fun_power(
    size: float,
    alpha: float,
    nullproportion: float,
    proportion: float,
    alternative: Alternative,
    test_type: TestType,
) -> float:
    """计算检验效能。

    Parameters
    ----------
        size : int
            样本量
        alpha : float
            显著性水平
        nullproportion : float
            零假设的概率
        proportion : float
            备择假设的概率
        alternative : Alternative
            检验方法，可选值为 `Alternative.ONE_SIDED`, `Alternative.TWO_SIDED`
        test_type : TestType
            检验类型，可选值为 `TestType.EXACT_TEST`, `TestType.Z_TEST_USING_S_P0`,
                               `TestType.Z_TEST_USING_S_P0_CC`, `TestType.Z_TEST_USING_S_PHAT`,
                               `TestType.Z_TEST_USING_S_PHAT_CC`
    Returns
    -------
        power : float
            检验效能
    """

    p0 = nullproportion
    p1 = proportion

    denominator = sqrt(p1 * (1 - p1))

    gMean = sqrt(size) * (p0 - p1) / denominator

    gsd = sqrt(p0 * (1 - p0)) / denominator

    # 使用 S(Phat) 作为标准差
    if test_type in (TestType.Z_TEST_USING_S_PHAT, TestType.Z_TEST_USING_S_PHAT_CC):
        gsd = sqrt(p1 * (1 - p1)) / denominator

    # 连续性校正
    c = 0
    if test_type in (TestType.Z_TEST_USING_S_P0_CC, TestType.Z_TEST_USING_S_PHAT_CC):
        if abs(p1 - p0) > 1 / (2 * size):
            c = 1 / (2 * sqrt(size))
    gc = c / denominator

    # 计算检验效能
    if alternative == Alternative.ONE_SIDED:
        if p1 < p0:
            z = norm.ppf(1 - alpha)
            stat = gMean - gsd * z - gc
            result = norm.cdf(stat)
        elif p1 > p0:
            z = norm.ppf(1 - alpha)
            stat = gMean + gsd * z + gc
            result = 1 - norm.cdf(stat)
    elif alternative == Alternative.TWO_SIDED:
        z = norm.ppf(1 - alpha / 2)
        stat = [gMean - gsd * z - gc, gMean + gsd * z + gc]
        result = norm.cdf(stat[0]) + 1 - norm.cdf(stat[1])

    return result


class OneProportion:
    class ForSize:
        def __init__(
            self,
            alpha: Alpha,
            power: Power,
            nullproportion: Proportion,
            proportion: Proportion,
            alternative: Alternative,
            test_type: TestType,
        ):
            self.alpha = alpha
            self.power = power
            self.nullproportion = nullproportion
            self.proportion = proportion
            self.alternative = alternative
            self.test_type = test_type

        def solve(self) -> Size:
            self._eval = (
                lambda size: fun_power(
                    size,
                    alpha=self.alpha,
                    nullproportion=self.nullproportion,
                    proportion=self.proportion,
                    alternative=self.alternative,
                    test_type=self.test_type,
                )
                - self.power
            )
            try:
                size = brentq(self._eval, 1, 1e10)
            except ValueError as e:
                raise ValueError("无解") from e
            self.size = Size(size)

    class ForAlpha:
        def __init__(
            self,
            size: Size,
            power: Power,
            nullproportion: Proportion,
            proportion: Proportion,
            alternative: Alternative,
            test_type: TestType,
        ):
            self.size = size
            self.power = power
            self.nullproportion = nullproportion
            self.proportion = proportion
            self.alternative = alternative
            self.test_type = test_type

        def solve(self) -> Alpha:
            self._eval = (
                lambda alpha: fun_power(
                    self.size, alpha, self.nullproportion, self.proportion, self.alternative, self.test_type
                )
                - self.power
            )
            try:
                alpha = brentq(self._eval, 0, 1)
            except ValueError as e:
                raise ValueError("无解") from e
            self.alpha = Alpha(alpha)

    class ForPower:
        def __init__(
            self,
            size: Size,
            alpha: Alpha,
            nullproportion: Proportion,
            proportion: Proportion,
            alternative: Alternative,
            test_type: TestType,
        ):
            self.size = size
            self.alpha = alpha
            self.nullproportion = nullproportion
            self.proportion = proportion
            self.alternative = alternative
            self.test_type = test_type

        def solve(self) -> Power:
            power = fun_power(
                self.size, self.alpha, self.nullproportion, self.proportion, self.alternative, self.test_type
            )
            self.power = Power(power)

    class ForNullProportion:
        def __init__(
            self,
            size: Size,
            alpha: Alpha,
            power: Power,
            proportion: Proportion,
            alternative: Alternative,
            test_type: TestType,
            search_direction: SearchDirection,
        ):
            self.size = size
            self.alpha = alpha
            self.power = power
            self.proportion = proportion
            self.alternative = alternative
            self.test_type = test_type
            self.search_direction = search_direction

        def solve(self) -> Proportion:
            self._eval = (
                lambda nullproportion: fun_power(
                    self.size, self.alpha, nullproportion, self.proportion, self.alternative, self.test_type
                )
                - self.power
            )

            match self.search_direction:
                case SearchDirection.LESS:
                    lbound, ubound = Interval(0, self.proportion).pseudo_bound()
                    try:
                        nullproportion = brentq(self._eval, lbound, ubound)
                    except ValueError as e:
                        raise ValueError("无解") from e
                case SearchDirection.GREATER:
                    lbound, ubound = Interval(self.proportion, 1).pseudo_bound()
                    try:
                        nullproportion = brentq(self._eval, lbound, ubound)
                    except ValueError as e:
                        raise ValueError("无解") from e
                case _:
                    assert False, "未知的搜索方向"

            self.nullproportion = Proportion(nullproportion)

    class ForProportion:
        def __init__(
            self,
            size: Size,
            alpha: Alpha,
            power: Power,
            nullproportion: Proportion,
            alternative: Alternative,
            test_type: TestType,
            search_direction: SearchDirection,
        ):
            self.size = size
            self.alpha = alpha
            self.power = power
            self.nullproportion = nullproportion
            self.alternative = alternative
            self.test_type = test_type
            self.search_direction = search_direction

        def solve(self) -> Proportion:
            self._eval = (
                lambda proportion: fun_power(
                    self.size, self.alpha, self.nullproportion, proportion, self.alternative, self.test_type
                )
                - self.power
            )

            match self.search_direction:
                case SearchDirection.LESS:
                    lbound, ubound = Interval(0, self.nullproportion).pseudo_bound()
                    try:
                        proportion = brentq(self._eval, lbound, ubound)
                    except ValueError as e:
                        raise ValueError("无解") from e
                case SearchDirection.GREATER:
                    lbound, ubound = Interval(self.nullproportion, 1).pseudo_bound()
                    try:
                        proportion = brentq(self._eval, lbound, ubound)
                    except ValueError as e:
                        raise ValueError("无解") from e
                case _:
                    assert False, "未知的搜索方向"

            self.proportion = Proportion(proportion)


def solve_for_sample_size(
    alpha: float,
    power: float,
    nullproportion: float,
    proportion: float,
    alternative: str,
    test_type: str,
    full_output: bool = False,
):
    """求解样本量

    Args:
        alpha (float): 显著性水平
        power (float): 检验效能
        nullproportion (float): 零假设下的率
        proportion (float): 备择假设下的率
        alternative (str): 备择假设类型，可选值: "TWO_SIDED", "ONE_SIDED"
        test_type (str): 检验类型，可选值: "EXACT_TEST", "Z_TEST_USING_S_P0", "Z_TEST_USING_S_P0_CC", "Z_TEST_USING_S_PHAT", "Z_TEST_USING_S_PHAT_CC"
        full_output (bool, optional): 是否输出完整结果。默认值: False
    """

    model = OneProportion.ForSize(
        alpha=Alpha(alpha),
        power=Power(power),
        nullproportion=Proportion(nullproportion),
        proportion=Proportion(proportion),
        alternative=Alternative[alternative],
        test_type=TestType[test_type],
    )
    model.solve()

    if full_output:
        return model
    return model.size


def solve_for_alpha(
    size: float,
    power: float,
    nullproportion: float,
    proportion: float,
    alternative: str,
    test_type: str,
    full_output: bool = False,
):
    """求解显著性水平

    Args:
        size (float): 样本量
        power (float): 检验效能
        nullproportion (float): 零假设下的率
        proportion (float): 备择假设下的率
        alternative (str): 备择假设类型，可选值: "TWO_SIDED", "ONE_SIDED"
        test_type (str): 检验类型，可选值: "EXACT_TEST", "Z_TEST_USING_S_P0", "Z_TEST_USING_S_P0_CC", "Z_TEST_USING_S_PHAT", "Z_TEST_USING_S_PHAT_CC"
        full_output (bool, optional): 是否输出完整结果。默认值: False
    """

    model = OneProportion.ForAlpha(
        size=Size(size),
        power=Power(power),
        nullproportion=Proportion(nullproportion),
        proportion=Proportion(proportion),
        alternative=Alternative[alternative],
        test_type=TestType[test_type],
    )
    model.solve()

    if full_output:
        return model
    return model.alpha


def solve_for_power(
    size: float,
    alpha: float,
    nullproportion: float,
    proportion: float,
    alternative: str,
    test_type: str,
    full_output: bool = False,
):
    """求解检验效能

    Args:
        size (float): 样本量
        alpha (float): 显著性水平
        nullproportion (float): 零假设下的率
        proportion (float): 备择假设下的率
        alternative (str): 备择假设类型，可选值: "TWO_SIDED", "ONE_SIDED"
        test_type (str): 检验类型，可选值: "EXACT_TEST", "Z_TEST_USING_S_P0", "Z_TEST_USING_S_P0_CC", "Z_TEST_USING_S_PHAT", "Z_TEST_USING_S_PHAT_CC"
        full_output (bool, optional): 是否输出完整结果。默认值: False
    """

    model = OneProportion.ForPower(
        size=Size(size),
        alpha=Alpha(alpha),
        nullproportion=Proportion(nullproportion),
        proportion=Proportion(proportion),
        alternative=Alternative[alternative],
        test_type=TestType[test_type],
    )
    model.solve()

    if full_output:
        return model
    return model.power


def solve_for_nullproportion(
    size: float,
    alpha: float,
    power: float,
    proportion: float,
    alternative: str,
    test_type: str,
    search_direction: str,
    full_output: bool = False,
):
    """求解零假设下的率

    Args:
        size (float): 样本量
        alpha (float): 显著性水平
        power (float): 检验效能
        proportion (float): 备择假设下的率
        alternative (str): 备择假设类型，可选值: "TWO_SIDED", "ONE_SIDED"
        test_type (str): 检验类型，可选值: "EXACT_TEST", "Z_TEST_USING_S_P0", "Z_TEST_USING_S_P0_CC", "Z_TEST_USING_S_PHAT", "Z_TEST_USING_S_PHAT_CC"
        search_direction (str): 搜索方向，可选值: "LESS", "GREATER"
        full_output (bool, optional): 是否输出完整结果。默认值: False
    """

    model = OneProportion.ForNullProportion(
        size=Size(size),
        alpha=Alpha(alpha),
        power=Power(power),
        proportion=Proportion(proportion),
        alternative=Alternative[alternative],
        test_type=TestType[test_type],
        search_direction=SearchDirection[search_direction],
    )
    model.solve()

    if full_output:
        return model
    return model.nullproportion


def solve_for_proportion(
    size: float,
    alpha: float,
    power: float,
    nullproportion: float,
    alternative: str,
    test_type: str,
    search_direction: str,
    full_output: bool = False,
):
    """求解备择假设下的率

    Args:
        size (float): 样本量
        alpha (float): 显著性水平
        power (float): 检验效能
        nullproportion (float): 零假设下的率
        alternative (str): 备择假设类型，可选值: "TWO_SIDED", "ONE_SIDED"
        test_type (str): 检验类型，可选值: "EXACT_TEST", "Z_TEST_USING_S_P0", "Z_TEST_USING_S_P0_CC", "Z_TEST_USING_S_PHAT", "Z_TEST_USING_S_PHAT_CC"
        search_direction (str): 搜索方向，可选值: "LESS", "GREATER"
        full_output (bool, optional): 是否输出完整结果。默认值: False
    """

    model = OneProportion.ForProportion(
        size=Size(size),
        alpha=Alpha(alpha),
        power=Power(power),
        nullproportion=Proportion(nullproportion),
        alternative=Alternative[alternative],
        test_type=TestType[test_type],
        search_direction=SearchDirection[search_direction],
    )
    model.solve()
    if full_output:
        return model
    return model.proportion
