from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    """定义一个区间，可指定是否包含上下限，不支持单点区间（例如：[1, 1]）。

    Parameters
    ----------
        lower (Any): 区间下限
        upper (Any): 区间上限
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
        >>> interval.pesudo_bound()
        (0, 0.9999999999)
    """

    lower: int | float
    upper: int | float
    lower_inclusive: bool = False
    upper_inclusive: bool = False

    def __contains__(self, value: int | float) -> bool:
        if not isinstance(value, (int, float)):
            raise TypeError(f"unsupported operand type(s) for in: 'Interval' and '{type(value)}'")

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

    def __eq__(self, other: "Interval") -> bool:
        if not isinstance(other, Interval):
            raise TypeError(f"unsupported operand type(s) for ==: 'Interval' and '{type(other)}'")

        return (self.lower, self.upper, self.lower_inclusive, self.upper_inclusive) == (
            other.lower,
            other.upper,
            other.lower_inclusive,
            other.upper_inclusive,
        )

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

    def pesudo_lbound(self, eps=1e-10) -> int | float:
        """区间的伪下界，用于数值计算。"""
        if self.lower_inclusive:
            return self.lower
        else:
            return self.lower + eps

    def pesudo_ubound(self, eps=1e-10) -> int | float:
        """区间的伪上界，用于数值计算。"""
        if self.upper_inclusive:
            return self.upper
        else:
            return self.upper - eps

    def pesudo_bound(self) -> tuple[int | float, int | float]:
        """区间的伪上下界，用于数值计算。"""
        return (self.pesudo_lbound(), self.pesudo_ubound())
