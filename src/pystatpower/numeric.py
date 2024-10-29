from dataclasses import dataclass
from math import isclose

#: The minimum meaningful float number.
MIN_FLOAT: float = 1e-10

#: The maximum meaningful float number.
MAX_FLOAT: float = 1e10


@dataclass(frozen=True)
class Interval:
    """Dataclass of interval, single point (eg. [1, 1]) is not supported.

    Parameters
    ----------
    lower : float
        The lower bound of the interval.
    upper : float
        The upper bound of the interval.
    lower_inclusive : bool
        True to include the lower bound. False otherwise. Defaults to False.
    upper_inclusive : bool
        True to include the upper bound. False otherwise. Defaults to False.

    Examples
    --------
    >>> itv= Interval(0, 1, lower_inclusive=True, upper_inclusive=False)
    >>> itv
    [0, 1)
    >>> 0.5 in itv
    True
    >>> 1 in itv
    False
    >>> 0 in itv
    False
    >>> itv.pseudo_bound()
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
        """Return the pseudo lower bound of the interval for numerical calculation.

        Parameters
        ----------
        eps : float
            The epsilon used to calculate the pseudo bound. Defaults to `MIN_FLOAT`.

        Returns
        -------
        float
            The pseudo lower bound of the interval.
        """

        if self.lower_inclusive:
            return self.lower
        else:
            return self.lower + eps

    def pseudo_ubound(self, eps: float = MIN_FLOAT) -> float:
        """Return the pseudo upper bound of the interval for numerical calculation.

        Parameters
        ----------
        eps : float
            The epsilon used to calculate the pseudo bound. Defaults to `MIN_FLOAT`.

        Returns
        -------
        float
            The pseudo upper bound of the interval.
        """

        if self.upper_inclusive:
            return self.upper
        else:
            return self.upper - eps

    def pseudo_bound(self, eps: float = MIN_FLOAT) -> tuple[float, float]:
        """Return the pseudo two-bounds tuple for numerical calculation.

        Parameters
        ----------
        eps : float
            The epsilon used to calculate the pseudo bound. Defaults to `MIN_FLOAT`.

        Returns
        -------
        tuple[float, float]
            The pseudo interval for numerical calculation.
        """

        return (self.pseudo_lbound(eps), self.pseudo_ubound(eps))


class PowerAnalysisFloat(float):
    """Base class for all numeric types in power analysis.

    - if an `int` or `float` numeric is passed to create an instance, it will be checked if it is in the domain.
      if not, a `ValueError` will be raised, else a new float object is returned, whose behaviour is the same as the built-in float object.
    - if `None` is passed to create an instance, `None` will be returned.
    - if any other type is passed to create an instance, a `TypeError` will be raised.

    Examples
    --------
    >>> PowerAnalysisFloat(0.5)
    0.5
    >>> PowerAnalysisFloat(0.5) * PowerAnalysisFloat(0.5)
    0.25
    >>> isinstance(PowerAnalysisFloat(0.5), float)
    True
    """

    #: An :class:`Interval` object that limits the range of values for a specific numerical type.
    #: Tryting to create an instance with a value outside the domain will raise a ValueError.
    domain = Interval(-MAX_FLOAT, MAX_FLOAT, lower_inclusive=True, upper_inclusive=True)

    def __new__(cls, obj):
        if isinstance(obj, (int, float)):
            if obj not in cls.domain:
                raise ValueError(f"{obj} is not in {cls.domain}.")
            return super().__new__(cls, obj)
        elif obj is None:
            return None
        else:
            raise TypeError(f"{obj} must be either an int, float, or None.")

    @classmethod
    def pseudo_bound(cls) -> tuple[float, float]:
        """Return the pseudo two-bounds tuple for numerical calculation."""

        return cls.domain.pseudo_bound()


class Alpha(PowerAnalysisFloat):
    """Significance level"""

    #: See :attr:`PowerAnalysisFloat.domain`.
    domain = Interval(0, 1)


class Power(PowerAnalysisFloat):
    """Power"""

    #: See :attr:`PowerAnalysisFloat.domain`.
    domain = Interval(0, 1)


class Mean(PowerAnalysisFloat):
    """Mean"""

    #: See :attr:`PowerAnalysisFloat.domain`.
    domain = Interval(-MAX_FLOAT, MAX_FLOAT)


class STD(PowerAnalysisFloat):
    """Standard deviation"""

    #: See :attr:`PowerAnalysisFloat.domain`.
    domain = Interval(0, MAX_FLOAT)


class Proportion(PowerAnalysisFloat):
    """Proportion"""

    #: See :attr:`PowerAnalysisFloat.domain`.
    domain = Interval(0, 1)


class Percent(PowerAnalysisFloat):
    """Percent"""

    #: See :attr:`PowerAnalysisFloat.domain`.
    domain = Interval(0, 1)


class Ratio(PowerAnalysisFloat):
    """Ratio"""

    #: See :attr:`PowerAnalysisFloat.domain`.
    domain = Interval(0, MAX_FLOAT)


class Size(PowerAnalysisFloat):
    """Sample size"""

    #: See :attr:`PowerAnalysisFloat.domain`.
    domain = Interval(0, MAX_FLOAT)


class DropOutRate(PowerAnalysisFloat):
    """Dropout rate"""

    #: See :attr:`PowerAnalysisFloat.domain`.
    domain = Interval(0, 1, lower_inclusive=True)


class DropOutSize(PowerAnalysisFloat):
    """Dropout-inflated enrollment sample size"""

    #: See :attr:`PowerAnalysisFloat.domain`.
    domain = Interval(0, MAX_FLOAT, lower_inclusive=True)
