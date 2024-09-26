from enum import Enum, EnumMeta
from math import ceil, floor, inf, isclose, trunc
from numbers import Real


from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    """定义一个区间，可指定是否包含上下限，不支持单点区间（例如：[1, 1]）。

    Parameters
    ----------
        lower (Real): 区间下限
        upper (Real): 区间上限
        lower_inclusive (bool): 是否包含区间下限
        upper_inclusive (bool): 是否包含区间上限

    Examples
    --------
    >>> interval = Interval(0, 1, lower_inclusive=True, upper_inclusive=False)
    >>> 0.5 in interval
    True
    >>> 1 in interval
    False
    >>> 0 in interval
    False
    >>> interval.pseudo_bound()
    (0, 0.9999999999)
    """

    lower: Real
    upper: Real
    lower_inclusive: bool = False
    upper_inclusive: bool = False

    def __contains__(self, value: Real) -> bool:
        if isinstance(value, Real):
            if self.lower_inclusive:
                if self.upper_inclusive:
                    return self.lower <= value <= self.upper
                else:
                    return self.lower <= value < self.upper
            else:
                if self.upper_inclusive:
                    return self.lower < value <= self.upper
                else:
                    return self.lower < value < self.upper

        raise RuntimeError(f"Interval.__contains__ only supports real numbers, but you passed in a {type(value)}.")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Interval):
            return (
                isclose(self.lower, other.lower)
                and isclose(self.upper, other.upper)
                and self.lower_inclusive == other.lower_inclusive
                and self.upper_inclusive == other.upper_inclusive
            )

        raise RuntimeError(f"Interval.__eq__ only supports Interval, but you passed in a {type(other)}.")

    def __repr__(self) -> str:
        if self.lower_inclusive:
            if self.upper_inclusive:
                return f"[{self.lower}, {self.upper}]"
            else:
                return f"[{self.lower}, {self.upper})"
        else:
            if self.upper_inclusive:
                return f"({self.lower}, {self.upper}]"
            else:
                return f"({self.lower}, {self.upper})"

    def pseudo_lbound(self, eps: Real = 1e-10) -> Real:
        """区间的伪下界，用于数值计算。"""
        if self.lower_inclusive:
            return self.lower
        else:
            return self.lower + eps

    def pseudo_ubound(self, eps: Real = 1e-10) -> Real:
        """区间的伪上界，用于数值计算。"""
        if self.upper_inclusive:
            return self.upper
        else:
            return self.upper - eps

    def pseudo_bound(self, eps: Real = 1e-10) -> tuple[Real, Real]:
        """区间的伪上下界，用于数值计算。"""
        return (self.pseudo_lbound(eps), self.pseudo_ubound(eps))


class PowerAnalysisNumeric(Real):
    """自定义功效分析数值类型"""

    _domain = Interval(-inf, inf, lower_inclusive=True, upper_inclusive=True)

    def __new__(cls, value: Real):
        if value is None:
            return None
        if not isinstance(value, Real):
            raise TypeError(f"{value} is not a real number.")
        if value not in cls._domain:
            raise ValueError(f"{value} is not in {cls._domain}.")
        return super().__new__(cls)

    def __init__(self, value: Real):
        self._value = value

    def __repr__(self):
        return f"{type(self).__name__}({self._value})"

    def __add__(self, other):
        if isinstance(other, Real):
            return self._value + other
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Real):
            return self._value - other
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Real):
            return self._value * other
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Real):
            return self._value / other
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, Real):
            return self._value // other
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, Real):
            return self._value % other
        return NotImplemented

    def __pow__(self, other, modulo=None):
        if isinstance(other, Real):
            return pow(self._value, other, modulo)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, Real):
            return other + self._value
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Real):
            return other - self._value
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Real):
            return other * self._value
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Real):
            return other / self._value
        return NotImplemented

    def __rfloordiv__(self, other):
        if isinstance(other, Real):
            return other // self._value
        return NotImplemented

    def __rmod__(self, other):
        if isinstance(other, Real):
            return other % self._value
        return NotImplemented

    def __rpow__(self, base, modulo=None):
        if isinstance(base, Real):
            return pow(base, self._value, modulo)
        return NotImplemented

    def __neg__(self):
        return -self._value

    def __pos__(self):
        return +self._value

    def __abs__(self):
        return abs(self._value)

    def __complex__(self):
        return complex(self._value)

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return float(self._value)

    def __round__(self, ndigits=None):
        return round(self._value, ndigits)

    def __trunc__(self):
        return trunc(self._value)

    def __floor__(self):
        return floor(self._value)

    def __ceil__(self):
        return ceil(self._value)

    def __lt__(self, other):
        if isinstance(other, Real):
            return self._value < other
        raise RuntimeError(f"{type(self)}.__lt__ only supports real numbers, but you passed in a {type(other)}.")

    def __le__(self, other):
        if isinstance(other, Real):
            return self._value <= other
        raise RuntimeError(f"{type(self)}.__le__ only supports real numbers, but you passed in a {type(other)}.")

    def __eq__(self, other):
        if isinstance(other, Real):
            return self._value == other
        raise RuntimeError(f"{type(self)}.__eq__ only supports real numbers, but you passed in a {type(other)}.")

    def __ne__(self, other):
        if isinstance(other, Real):
            return self._value != other
        raise RuntimeError(f"{type(self)}.__ne__ only supports real numbers, but you passed in a {type(other)}.")

    def __gt__(self, other):
        if isinstance(other, Real):
            return self._value > other
        raise RuntimeError(f"{type(self)}.__gt__ only supports real numbers, but you passed in a {type(other)}.")

    def __ge__(self, other):
        if isinstance(other, Real):
            return self._value >= other
        raise RuntimeError(f"{type(self)}.__ge__ only supports real numbers, but you passed in a {type(other)}.")

    def __hash__(self):
        return hash(self._value)

    def __bool__(self):
        return bool(self._value)


class PowerAnalysisOption(EnumMeta):
    """自定义功效分析选项的枚举元类，用于支持大小写不敏感的枚举值访问。"""

    def __getitem__(self, name):
        if isinstance(name, str):
            return super().__getitem__(name.upper())
        else:
            return super().__getitem__(name)


class Alpha(PowerAnalysisNumeric):
    """显著性水平"""

    _domain = Interval(0, 1)


class Power(PowerAnalysisNumeric):
    """检验效能"""

    _domain = Interval(0, 1)


class Mean(PowerAnalysisNumeric):
    """均值"""

    _domain = Interval(-inf, inf)


class STD(PowerAnalysisNumeric):
    """标准差"""

    _domain = Interval(0, inf)


class Proportion(PowerAnalysisNumeric):
    """率"""

    _domain = Interval(0, 1)


class Percent(PowerAnalysisNumeric):
    """百分比"""

    _domain = Interval(0, 1)


class Ratio(PowerAnalysisNumeric):
    """比例"""

    _domain = Interval(0, inf)


class Size(PowerAnalysisNumeric):
    """样本量"""

    _domain = Interval(0, inf)


class DropOutRate(PowerAnalysisNumeric):
    """脱落率"""

    _domain = Interval(0, 1, lower_inclusive=True)
