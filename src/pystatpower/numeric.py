from dataclasses import dataclass
from math import ceil, floor, isclose, trunc

MIN_FLOAT: float = 1e-10
MAX_FLOAT: float = 1e10


@dataclass(frozen=True)
class Interval:
    """定义一个区间，可指定是否包含上下限，不支持单点区间（例如：[1, 1]）。

    Parameters
    ----------
        lower (float): 区间下限
        upper (float): 区间上限
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

    lower: int | float
    upper: int | float
    lower_inclusive: bool = False
    upper_inclusive: bool = False

    def __contains__(self, value: int | float) -> bool:
        if isinstance(value, (int, float)):
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

        raise TypeError(f"Interval.__contains__ only supports real numbers, but you passed in a {type(value)}.")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Interval):
            return (
                isclose(self.lower, other.lower)
                and isclose(self.upper, other.upper)
                and self.lower_inclusive == other.lower_inclusive
                and self.upper_inclusive == other.upper_inclusive
            )

        raise TypeError(f"Interval.__eq__ only supports Interval, but you passed in a {type(other)}.")

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

    def pseudo_lbound(self, eps: float = MIN_FLOAT) -> float:
        """区间的伪下界，用于数值计算。"""

        if self.lower_inclusive:
            return self.lower
        else:
            return self.lower + eps

    def pseudo_ubound(self, eps: float = MIN_FLOAT) -> float:
        """区间的伪上界，用于数值计算。"""

        if self.upper_inclusive:
            return self.upper
        else:
            return self.upper - eps

    def pseudo_bound(self, eps: float = MIN_FLOAT) -> tuple[float, float]:
        """区间的伪上下界，用于数值计算。"""

        return (self.pseudo_lbound(eps), self.pseudo_ubound(eps))


class Numeric:
    """自定义功效分析数值类型"""

    _domain = Interval(-MAX_FLOAT, MAX_FLOAT, lower_inclusive=True, upper_inclusive=True)

    def __new__(cls, value):
        if value is None:
            return None
        if isinstance(value, Numeric):
            return cls(value._value)

        if not isinstance(value, (int, float)):
            raise TypeError(f"{value} is not an int or float number.")
        if value not in cls._domain:
            raise ValueError(f"{value} is not in {cls._domain}.")

        return super().__new__(cls)

    def __init__(self, value):
        if isinstance(value, (int, float)):
            self._value = value

    @classmethod
    def pseudo_bound(cls) -> tuple[float, float]:
        """伪区间，用于数值计算。"""

        return cls._domain.pseudo_bound()

    def __repr__(self):
        return f"{type(self).__name__}({self._value})"

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self._value + other
        if isinstance(other, Numeric):
            return self._value + other._value
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self._value - other
        if isinstance(other, Numeric):
            return self._value - other._value
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self._value * other
        if isinstance(other, Numeric):
            return self._value * other._value
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self._value / other
        if isinstance(other, Numeric):
            return self._value / other._value
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, (int, float)):
            return self._value // other
        if isinstance(other, Numeric):
            return self._value // other._value
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, (int, float)):
            return self._value % other
        if isinstance(other, Numeric):
            return self._value % other._value
        return NotImplemented

    def __pow__(self, other, modulo=None):
        if isinstance(other, (int, float)):
            return pow(self._value, other, modulo)
        if isinstance(other, Numeric):
            return pow(self._value, other._value, modulo)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (int, float)):
            return other + self._value
        if isinstance(other, Numeric):
            return other._value + self._value
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return other - self._value
        if isinstance(other, Numeric):
            return other._value - self._value
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return other * self._value
        if isinstance(other, Numeric):
            return other._value * self._value
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return other / self._value
        if isinstance(other, Numeric):
            return other._value / self._value
        return NotImplemented

    def __rfloordiv__(self, other):
        if isinstance(other, (int, float)):
            return other // self._value
        if isinstance(other, Numeric):
            return other._value // self._value
        return NotImplemented

    def __rmod__(self, other):
        if isinstance(other, (int, float)):
            return other % self._value
        if isinstance(other, Numeric):
            return other._value % self._value
        return NotImplemented

    def __rpow__(self, base, modulo=None):
        if isinstance(base, (int, float)):
            return pow(base, self._value, modulo)
        if isinstance(base, Numeric):
            return pow(base._value, self._value, modulo)
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
        if isinstance(other, (int, float)):
            return self._value < other
        if isinstance(other, Numeric):
            return self._value < other._value
        raise TypeError(f"{type(self)}.__lt__ only supports float numbers, but you passed in a {type(other)}.")

    def __le__(self, other):
        if isinstance(other, (int, float)):
            return self._value <= other
        if isinstance(other, Numeric):
            return self._value <= other._value
        raise TypeError(f"{type(self)}.__le__ only supports float numbers, but you passed in a {type(other)}.")

    def __eq__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return self._value == other
        if isinstance(other, Numeric):
            return self._value == other._value
        raise TypeError(f"{type(self)}.__eq__ only supports float numbers, but you passed in a {type(other)}.")

    def __ne__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return self._value != other
        if isinstance(other, Numeric):
            return self._value != other._value
        raise TypeError(f"{type(self)}.__ne__ only supports float numbers, but you passed in a {type(other)}.")

    def __gt__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return self._value > other
        if isinstance(other, Numeric):
            return self._value > other._value
        raise TypeError(f"{type(self)}.__gt__ only supports float numbers, but you passed in a {type(other)}.")

    def __ge__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return self._value >= other
        if isinstance(other, Numeric):
            return self._value >= other._value
        raise TypeError(f"{type(self)}.__ge__ only supports float numbers, but you passed in a {type(other)}.")

    def __hash__(self):
        return hash(self._value)

    def __bool__(self):
        return bool(self._value)


class Alpha(Numeric):
    """显著性水平"""

    _domain = Interval(0, 1)


class Power(Numeric):
    """检验效能"""

    _domain = Interval(0, 1)


class Mean(Numeric):
    """均值"""

    _domain = Interval(-MAX_FLOAT, MAX_FLOAT)


class STD(Numeric):
    """标准差"""

    _domain = Interval(0, MAX_FLOAT)


class Proportion(Numeric):
    """率"""

    _domain = Interval(0, 1)


class Percent(Numeric):
    """百分比"""

    _domain = Interval(0, 1)


class Ratio(Numeric):
    """比例"""

    _domain = Interval(0, MAX_FLOAT)


class Size(Numeric):
    """样本量"""

    _domain = Interval(0, MAX_FLOAT)


class DropOutRate(Numeric):
    """脱落率"""

    _domain = Interval(0, 1, lower_inclusive=True)


class DropOutSize(Numeric):
    """脱落样本量"""

    _domain = Interval(0, MAX_FLOAT, lower_inclusive=True)
