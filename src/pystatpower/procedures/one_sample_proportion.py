"""单样本率检验的功效分析模块"""

from dataclasses import dataclass
from enum import Enum
from math import sqrt
from typing import Any
from scipy.stats import norm
from scipy.optimize import brenth

from pystatpower.exception import (
    CalculationSolutionNotFoundError,
    EnumMemberNotExistError,
    ParameterValueEmptyError,
    ParameterTypeError,
    ParameterValueNotInDomainError,
    TargetParameterNotUniqueError,
    TargetParameterNotExistError,
)
from pystatpower.utils import get_enum_by_name
from pystatpower.interval import Interval


# 最大样本量
N_MAX = 1e10

# 最小样本量
N_MIN = 1


class Alternative(Enum):
    """备择假设枚举类。

    Attributes
    ----------
        ONE_SIDED : str
            单侧检验
            - Upper: `H0 : p1 <= p0，H1 : p1 > p0`
            - Lower: `H0 : p1 >= p0，H1 : p1 < p0`
        TWO_SIDED : str
            双侧检验，`H0 : p1 = p0，H1 : p1 ≠ p0`
    """

    ONE_SIDED = "one.sided"
    TWO_SIDED = "two.sided"


class TestType(Enum):
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


class SearchDirection(Enum):
    """搜索方向枚举类。

    Attributes
    ----------
        LOWER : str
            向上搜索
        UPPER : str
            向下搜索
    """

    LOWER = "Lower"
    UPPER = "Upper"


@dataclass(frozen=True)
class ParamInfo:
    default: Any
    domain: Interval | Enum
    description: str
    solvable: bool


# 参数配置信息
param_info = {
    "n": ParamInfo(default=None, domain=Interval(0, N_MAX), description="样本量", solvable=True),
    "alpha": ParamInfo(default=0.05, domain=Interval(0, 1), description="显著性水平", solvable=True),
    "power": ParamInfo(default=0.80, domain=Interval(0, 1), description="检验效能", solvable=True),
    "nullproportion": ParamInfo(default=0.80, domain=Interval(0, 1), description="零假设的概率", solvable=True),
    "proportion": ParamInfo(default=0.95, domain=Interval(0, 1), description="备择假设的概率", solvable=True),
    "alternative": ParamInfo(
        default=Alternative.TWO_SIDED,
        domain=Alternative,
        description="检验方法",
        solvable=False,
    ),
    "test_type": ParamInfo(
        default=TestType.EXACT_TEST,
        domain=TestType,
        description="检验类型",
        solvable=False,
    ),
    "search_direction": ParamInfo(
        default=SearchDirection.LOWER,
        domain=SearchDirection,
        description="搜索方向",
        solvable=False,
    ),
}

# 参数的定义域
param_info_domain = {key: value.domain for key, value in param_info.items()}

# 支持的参数
supported_params = tuple(param_info.keys())

# 不可求解的参数
unsolvable_params = tuple(key for key, value in param_info.items() if not value.solvable)

# 可空的参数，即使不作为求解目标
nonable_params_even_not_target = ("search_direction",)


def calc_power(
    n: int,
    alpha: float,
    nullproportion: float,
    proportion: float,
    alternative: Alternative,
    test_type: TestType,
) -> float:
    """计算检验效能。

    Parameters
    ----------
        n : int
            样本量
        alpha : float
            显著性水平
        power : float
            检验效能
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

    gMean = sqrt(n) * (p0 - p1) / denominator

    gsd = sqrt(p0 * (1 - p0)) / denominator

    # 使用 S(Phat) 作为标准差
    if test_type in (TestType.Z_TEST_USING_S_PHAT, TestType.Z_TEST_USING_S_PHAT_CC):
        gsd = sqrt(p1 * (1 - p1)) / denominator

    # 连续性校正
    c = 0
    if test_type in (TestType.Z_TEST_USING_S_P0_CC, TestType.Z_TEST_USING_S_PHAT_CC):
        if abs(p1 - p0) > 1 / (2 * n):
            c = 1 / (2 * sqrt(n))
    gc = c / denominator

    # 计算检验效能
    if alternative == Alternative.ONE_SIDED:
        if p1 < p0:
            z = norm.ppf(1 - alpha)
            gstat = gMean - gsd * z - gc
            result = norm.cdf(gstat)
        elif p1 > p0:
            z = norm.ppf(1 - alpha)
            gstat = gMean + gsd * z + gc
            result = 1 - norm.cdf(gstat)
    elif alternative == Alternative.TWO_SIDED:
        z = norm.ppf(1 - alpha / 2)
        gstat = [gMean - gsd * z - gc, gMean + gsd * z + gc]
        result = norm.cdf(gstat[0]) + 1 - norm.cdf(gstat[1])

    return result


def solve(
    n: int | None = None,
    alpha: float | None = 0.05,
    power: float | None = 0.80,
    nullproportion: float | None = 0.80,
    proportion: float | None = 0.95,
    alternative: str | Alternative = Alternative.TWO_SIDED,
    test_type: str | TestType = TestType.EXACT_TEST,
    search_direction: str | SearchDirection | None = SearchDirection.UPPER,
) -> float | dict[str, float]:
    """求解目标参数。

    Parameters
    ----------
        n : int | None
            样本量
        alpha : float | None
            显著性水平
        power : float | None
            检验效能
        nullproportion : float | None
            零假设的概率
        proportion : float | None
            备择假设的概率
        alternative : str | Alternative
            检验方法，可选值为 `'ONE_SIDED'`, `'TWO_SIDED'`
        test_type : str | TestType
            检验类型，可选值为 `'EXACT_TEST'`, `'Z_TEST_USING_S_P0'`,
                               `'Z_TEST_USING_S_P0_CC'`, `'Z_TEST_USING_S_PHAT'`,
                               `'Z_TEST_USING_S_PHAT_CC'`
        search_direction : str | SearchDirection | None
            搜索方向，可选值为 `'LOWER'`, `'UPPER'`，仅在 `nullproportion` 或 `proportion` 作为求解目标时有效

    Returns
    -------
        result : int | float
            目标参数的解

    Raises
    ------
    - ParameterTypeError : 参数类型错误
    - ParameterValueEmptyError : 当求解目标是 `nullproportion` 或 `proportion` 时，未指定参数 `search_direction`
    - ParameterValueNotInDomainError : 参数值不在定义域内
    - EnumMemberNotExistError : 参数 `alternative`, `test_type`, `search_direction` 指定的字符串找不到对应的枚举名称
    - TergatParameterNotExistError : 目标参数不存在
    - TargetParameterNotUniqueError : 目标参数不唯一
    - CalculationSolutionNotFoundError : 未找到解

    Details
    -------
    - 当 `nullproportion` 或 `proportion` 作为求解目标时，`search_direction` 参数值决定了解的搜索方向。

      例如：`nullproportion = 0.80, proportion = None` 时, 若指定 `search_direction='LOWER'`，
      则会在区间 `(0, 0.80)` 中尝试求解满足 `power` 的 `proportion`。
    """

    # 检查参数类型和取值
    _check(n, alpha, power, nullproportion, proportion, alternative, test_type, search_direction)

    # 尝试将传入的字符串转换为枚举类型
    try:
        alternative = get_enum_by_name(Alternative, alternative)
        test_type = get_enum_by_name(TestType, test_type)
        search_direction = get_enum_by_name(SearchDirection, search_direction)
    except EnumMemberNotExistError as e:
        raise e

    # 获取局部变量
    local_vars = {**locals()}

    # 获取求解目标
    target_params = [key for key, value in local_vars.items() if value is None and key not in unsolvable_params]
    if not target_params:
        raise TargetParameterNotExistError("No target parameter to solve.")
    if len(target_params) > 1:
        raise TargetParameterNotUniqueError("More than one target parameter to solve.")
    target_param = target_params[0]

    # 检查参数是否在定义域内
    for key, value in local_vars.items():
        if key == target_param:
            continue
        if key in nonable_params_even_not_target:
            continue
        elif value not in param_info_domain[key]:
            raise ParameterValueNotInDomainError(f"Invalid value for {key}: {value}")

    # 定义求解函数，传入关于目标参数的功效函数和目标参数的上下界
    def solve_for_param(eval_func, lower_bound, upper_bound):
        try:
            return brenth(eval_func, lower_bound, upper_bound)
        except ValueError:
            raise CalculationSolutionNotFoundError(
                f"Could not find a solution for {target_param} for the given arguments {local_vars}"
            )

    # 开始求解
    result = None
    if target_param == "power":
        result = calc_power(
            n=n,
            alpha=alpha,
            nullproportion=nullproportion,
            proportion=proportion,
            test_type=test_type,
            alternative=alternative,
        )
    else:
        # 获取目标参数的有效区间
        interval = param_info_domain[target_param]

        # 为了避免求解时出现边界问题，对区间进行微调
        lower_bound, upper_bound = interval.pesudo_bound()

        if target_param == "n":

            def eval_n(x):
                return (
                    calc_power(
                        x,
                        alpha=alpha,
                        nullproportion=nullproportion,
                        proportion=proportion,
                        test_type=test_type,
                        alternative=alternative,
                    )
                    - power
                )

            result = solve_for_param(eval_n, lower_bound, upper_bound)
        elif target_param == "alpha":

            def eval_alpha(alpha):
                return (
                    calc_power(
                        n=n,
                        alpha=alpha,
                        nullproportion=nullproportion,
                        proportion=proportion,
                        test_type=test_type,
                        alternative=alternative,
                    )
                    - power
                )

            result = solve_for_param(eval_alpha, lower_bound, upper_bound)
        elif target_param == "nullproportion":

            def eval_nullproportion(nullproportion):
                return (
                    calc_power(
                        n=n,
                        alpha=alpha,
                        nullproportion=nullproportion,
                        proportion=proportion,
                        test_type=test_type,
                        alternative=alternative,
                    )
                    - power
                )

            if search_direction == SearchDirection.LOWER:
                lower_bound, upper_bound = Interval(0, proportion).pesudo_bound()
                result = solve_for_param(eval_nullproportion, lower_bound, upper_bound)
            elif search_direction == SearchDirection.UPPER:
                lower_bound, upper_bound = Interval(proportion, 1).pesudo_bound()
                result = solve_for_param(eval_nullproportion, lower_bound, upper_bound)
            else:
                raise ParameterValueEmptyError(
                    "Parameter 'search_direction' should be specified when 'nullproportion' is target."
                )
        elif target_param == "proportion":

            def eval_proportion(proportion):
                return (
                    calc_power(
                        n=n,
                        alpha=alpha,
                        nullproportion=nullproportion,
                        proportion=proportion,
                        test_type=test_type,
                        alternative=alternative,
                    )
                    - power
                )

            if search_direction == SearchDirection.LOWER:
                lower_bound, upper_bound = Interval(0, nullproportion).pesudo_bound()
                result = solve_for_param(eval_proportion, lower_bound, upper_bound)
            elif search_direction == SearchDirection.UPPER:
                lower_bound, upper_bound = Interval(nullproportion, 1).pesudo_bound()
                result = solve_for_param(eval_proportion, lower_bound, upper_bound)
            else:
                raise ParameterValueEmptyError(
                    "Parameter 'search_direction' should be specified when 'proportion' is target."
                )

    return result


def _check(n, alpha, power, nullproportion, proportion, alternative, test_type, search_direction) -> None:
    """检查参数类型和取值。"""

    if not isinstance(n, int) and n is not None:
        raise ParameterTypeError(f"Excepted 'n' to be int, but got {type(n)}")
    if not isinstance(alpha, (int | float)) and alpha is not None:
        raise ParameterTypeError(f"Excepted 'alpha' to be int or float, but got {type(alpha)}")
    if not isinstance(power, (int | float)) and power is not None:
        raise ParameterTypeError(f"Excepted 'power' to be int or float, but got {type(power)}")
    if not isinstance(nullproportion, (int | float)) and nullproportion is not None:
        raise ParameterTypeError(f"Excepted 'nullproportion' to be int or float, but got {type(nullproportion)}")
    if not isinstance(proportion, (int | float)) and proportion is not None:
        raise ParameterTypeError(f"Excepted 'proportion' to be int or float, but got {type(proportion)}")
    if not isinstance(alternative, (str, Alternative)):
        raise ParameterTypeError(f"Excepted 'alternative' to be str or Alternative, but got {type(alternative)}")
    if not isinstance(test_type, (str, TestType)):
        raise ParameterTypeError(f"Excepted 'test_type' to be str or TestType, but got {type(test_type)}")
    if not isinstance(search_direction, (str, SearchDirection)) and search_direction is not None:
        raise ParameterTypeError(
            f"Excepted 'search_direction' to be str or SearchDirection, but got {type(search_direction)}"
        )
