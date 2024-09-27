from enum import Enum
from math import nan

import pytest

from pystatpower.basic import *


class TestInterval:
    def test_contains(self):
        assert 0.5 in Interval(0, 1)
        assert 0 in Interval(0, 1, lower_inclusive=True)
        assert 1 in Interval(0, 1, upper_inclusive=True)
        assert 0 in Interval(0, 1, lower_inclusive=True, upper_inclusive=True)
        assert 1 in Interval(0, 1, lower_inclusive=True, upper_inclusive=True)

        with pytest.raises(RuntimeError):
            assert "0.5" in Interval(0, 1)

    def test_eq(self):
        assert Interval(0, 1) == Interval(0, 1)
        assert Interval(0, 1, lower_inclusive=True) == Interval(0, 1, lower_inclusive=True)
        assert Interval(0, 1, upper_inclusive=True) == Interval(0, 1, upper_inclusive=True)
        assert Interval(0, 1, lower_inclusive=True, upper_inclusive=True) == Interval(
            0, 1, lower_inclusive=True, upper_inclusive=True
        )

        # 区间范围近似相同
        assert Interval(0, 1e10) == Interval(0, 1e10 + 1)
        # 区间范围近似相同，但另一个区间包含边界
        assert Interval(0, 1e10) != Interval(0, 1e10 + 1, lower_inclusive=True)

        with pytest.raises(RuntimeError):
            assert Interval(0, 1) == "Interval(0, 1)"

    def test_repr(self):
        assert repr(Interval(0, 1)) == "(0, 1)"
        assert repr(Interval(0, 1, lower_inclusive=True)) == "[0, 1)"
        assert repr(Interval(0, 1, upper_inclusive=True)) == "(0, 1]"
        assert repr(Interval(0, 1, lower_inclusive=True, upper_inclusive=True)) == "[0, 1]"

    def test_pseudo_lbound(self):
        assert Interval(0, 1).pseudo_lbound() == 1e-10
        assert Interval(0, 1, lower_inclusive=True).pseudo_lbound() == 0

    def test_pseudo_ubound(self):
        assert Interval(0, 1).pseudo_ubound() == 1 - 1e-10
        assert Interval(0, 1, upper_inclusive=True).pseudo_ubound() == 1

    def test_pseudo_bound(self):
        assert Interval(0, 1).pseudo_bound() == (1e-10, 1 - 1e-10)
        assert Interval(0, 1, lower_inclusive=True).pseudo_bound() == (0, 1 - 1e-10)
        assert Interval(0, 1, upper_inclusive=True).pseudo_bound() == (1e-10, 1)
        assert Interval(0, 1, lower_inclusive=True, upper_inclusive=True).pseudo_bound() == (0, 1)


class TestPowerAnalysisNumeric:
    def test_domain(self):
        assert PowerAnalysisNumeric._domain == Interval(
            MIN_NEGATIVE_FLOAT, MAX_POSITIVE_FLOAT, lower_inclusive=True, upper_inclusive=True
        )

    def test_init(self):
        assert PowerAnalysisNumeric(0) == 0
        assert PowerAnalysisNumeric(0.5) == 0.5
        assert PowerAnalysisNumeric(1) == 1
        assert PowerAnalysisNumeric(MIN_NEGATIVE_FLOAT) == MIN_NEGATIVE_FLOAT
        assert PowerAnalysisNumeric(MAX_NEGATIVE_FLOAT) == MAX_NEGATIVE_FLOAT
        assert PowerAnalysisNumeric(MIN_POSITIVE_FLOAT) == MIN_POSITIVE_FLOAT
        assert PowerAnalysisNumeric(MAX_POSITIVE_FLOAT) == MAX_POSITIVE_FLOAT

        with pytest.raises(TypeError):
            PowerAnalysisNumeric("0.5")
        with pytest.raises(ValueError):
            PowerAnalysisNumeric(nan)

    def test_pseudo_domain(self):
        assert PowerAnalysisNumeric.pseudo_bound() == (MIN_NEGATIVE_FLOAT, MAX_POSITIVE_FLOAT)
        assert Alpha.pseudo_bound() == (0 + MIN_POSITIVE_FLOAT, 1 - MIN_POSITIVE_FLOAT)
        assert Power.pseudo_bound() == (0 + MIN_POSITIVE_FLOAT, 1 - MIN_POSITIVE_FLOAT)
        assert Mean.pseudo_bound() == (MIN_NEGATIVE_FLOAT + MIN_POSITIVE_FLOAT, MAX_POSITIVE_FLOAT - MIN_POSITIVE_FLOAT)
        assert STD.pseudo_bound() == (0 + MIN_POSITIVE_FLOAT, MAX_POSITIVE_FLOAT - MIN_POSITIVE_FLOAT)
        assert Proportion.pseudo_bound() == (0 + MIN_POSITIVE_FLOAT, 1 - MIN_POSITIVE_FLOAT)
        assert Percent.pseudo_bound() == (0 + MIN_POSITIVE_FLOAT, 1 - MIN_POSITIVE_FLOAT)
        assert Ratio.pseudo_bound() == (0 + MIN_POSITIVE_FLOAT, MAX_POSITIVE_FLOAT - MIN_POSITIVE_FLOAT)
        assert Size.pseudo_bound() == (0 + MIN_POSITIVE_FLOAT, MAX_POSITIVE_FLOAT - MIN_POSITIVE_FLOAT)
        assert DropOutRate.pseudo_bound() == (0, 1 - MIN_POSITIVE_FLOAT)

    def test_repr(self):
        assert repr(PowerAnalysisNumeric(0)) == "PowerAnalysisNumeric(0)"
        assert repr(PowerAnalysisNumeric(0.5)) == "PowerAnalysisNumeric(0.5)"
        assert repr(PowerAnalysisNumeric(1)) == "PowerAnalysisNumeric(1)"
        assert repr(PowerAnalysisNumeric(MIN_NEGATIVE_FLOAT)) == f"PowerAnalysisNumeric({MIN_NEGATIVE_FLOAT})"
        assert repr(PowerAnalysisNumeric(MAX_NEGATIVE_FLOAT)) == f"PowerAnalysisNumeric({MAX_NEGATIVE_FLOAT})"
        assert repr(PowerAnalysisNumeric(MIN_POSITIVE_FLOAT)) == f"PowerAnalysisNumeric({MIN_POSITIVE_FLOAT})"
        assert repr(PowerAnalysisNumeric(MAX_POSITIVE_FLOAT)) == f"PowerAnalysisNumeric({MAX_POSITIVE_FLOAT})"

    def test_add(self):
        assert PowerAnalysisNumeric(1) + 1 == 2
        assert PowerAnalysisNumeric(1) + PowerAnalysisNumeric(1) == 2

        assert PowerAnalysisNumeric(1) + 0.5 == 1.5
        assert PowerAnalysisNumeric(1) + PowerAnalysisNumeric(0.5) == 1.5

        with pytest.raises(TypeError):
            PowerAnalysisNumeric(1) + "1"

    def test_radd(self):
        assert 1 + PowerAnalysisNumeric(1) == 2
        assert 1 + PowerAnalysisNumeric(0.5) == 1.5

        with pytest.raises(TypeError):
            "1" + PowerAnalysisNumeric(1)

    def test_sub(self):
        assert PowerAnalysisNumeric(1) - 1 == 0
        assert PowerAnalysisNumeric(1) - PowerAnalysisNumeric(1) == 0

        assert PowerAnalysisNumeric(1) - 0.5 == 0.5
        assert PowerAnalysisNumeric(1) - PowerAnalysisNumeric(0.5) == 0.5

        with pytest.raises(TypeError):
            PowerAnalysisNumeric(1) - "1"

    def test_rsub(self):
        assert 1 - PowerAnalysisNumeric(1) == 0
        assert 1 - PowerAnalysisNumeric(0.5) == 0.5

        with pytest.raises(TypeError):
            "1" - PowerAnalysisNumeric(1)

    def test_mul(self):
        assert PowerAnalysisNumeric(2) * 4 == 8
        assert PowerAnalysisNumeric(2) * PowerAnalysisNumeric(4) == 8

        assert PowerAnalysisNumeric(2) * 0.5 == 1
        assert PowerAnalysisNumeric(2) * PowerAnalysisNumeric(0.5) == 1

        with pytest.raises(TypeError):
            PowerAnalysisNumeric(2) * "4"

    def test_rmul(self):
        assert 2 * PowerAnalysisNumeric(4) == 8
        assert 2 * PowerAnalysisNumeric(0.5) == 1

        with pytest.raises(TypeError):
            "4" * PowerAnalysisNumeric(2)

    def test_truediv(self):
        assert PowerAnalysisNumeric(1) / 2 == 0.5
        assert PowerAnalysisNumeric(1) / PowerAnalysisNumeric(2) == 0.5

        assert PowerAnalysisNumeric(1) / 0.5 == 2
        assert PowerAnalysisNumeric(1) / PowerAnalysisNumeric(0.5) == 2

        assert PowerAnalysisNumeric(1) / 3 == 1 / 3
        assert PowerAnalysisNumeric(1) / PowerAnalysisNumeric(3) == 1 / 3

        with pytest.raises(TypeError):
            PowerAnalysisNumeric(1) / "2"

    def test_rtruediv(self):
        assert 1 / PowerAnalysisNumeric(2) == 0.5
        assert 1 / PowerAnalysisNumeric(0.5) == 2

        assert 1 / PowerAnalysisNumeric(3) == 1 / 3

        with pytest.raises(TypeError):
            "2" / PowerAnalysisNumeric(1)

    def test_floordiv(self):
        assert PowerAnalysisNumeric(3) // 2 == 1
        assert PowerAnalysisNumeric(3) // PowerAnalysisNumeric(2) == 1

        with pytest.raises(TypeError):
            PowerAnalysisNumeric(3) // "2"

    def test_rfloordiv(self):
        assert 3 // PowerAnalysisNumeric(2) == 1

        with pytest.raises(TypeError):
            "3" // PowerAnalysisNumeric(2)

    def test_mod(self):
        assert PowerAnalysisNumeric(5) % 3 == 2
        assert PowerAnalysisNumeric(5) % PowerAnalysisNumeric(3) == 2

        with pytest.raises(TypeError):
            PowerAnalysisNumeric(5) % "3"

    def test_rmod(self):
        assert 3 % PowerAnalysisNumeric(2) == 1

        class Person:
            pass

        with pytest.raises(TypeError):
            Person() % PowerAnalysisNumeric(2)

    def test_pow(self):
        assert PowerAnalysisNumeric(2) ** 3 == 8
        assert PowerAnalysisNumeric(2) ** PowerAnalysisNumeric(3) == 8

        assert PowerAnalysisNumeric(2) ** 0.5 == 2**0.5

        with pytest.raises(TypeError):
            PowerAnalysisNumeric(2) ** "3"

    def test_rpow(self):
        assert 2 ** PowerAnalysisNumeric(3) == 8
        assert 2 ** PowerAnalysisNumeric(0.5) == 2**0.5

        with pytest.raises(TypeError):
            "2" ** PowerAnalysisNumeric(3)

    def test_abs(self):
        assert abs(PowerAnalysisNumeric(3)) == 3
        assert abs(PowerAnalysisNumeric(-3)) == 3

    def test_neg(self):
        assert -PowerAnalysisNumeric(3) == -3
        assert -PowerAnalysisNumeric(-3) == 3

    def test_pos(self):
        assert +PowerAnalysisNumeric(3) == 3
        assert +PowerAnalysisNumeric(-3) == -3

    def test_trunc(self):
        assert trunc(PowerAnalysisNumeric(3.14)) == 3
        assert trunc(PowerAnalysisNumeric(-3.14)) == -3

    def test_int(self):
        assert int(PowerAnalysisNumeric(3.14)) == 3
        assert int(PowerAnalysisNumeric(-3.14)) == -3

    def test_floor(self):
        assert floor(PowerAnalysisNumeric(3.14)) == 3
        assert floor(PowerAnalysisNumeric(-3.14)) == -4

    def test_ceil(self):
        assert ceil(PowerAnalysisNumeric(3.14)) == 4
        assert ceil(PowerAnalysisNumeric(-3.14)) == -3

    def test_round(self):
        assert round(PowerAnalysisNumeric(3.1415)) == 3
        assert round(PowerAnalysisNumeric(-3.1415)) == -3
        assert round(PowerAnalysisNumeric(3.1415), 3) == 3.142
        assert round(PowerAnalysisNumeric(-3.1415), 3) == -3.142

    def test_eq(self):
        assert PowerAnalysisNumeric(0) == 0
        assert PowerAnalysisNumeric(0) == PowerAnalysisNumeric(0)
        assert 0 == PowerAnalysisNumeric(0)
        assert PowerAnalysisNumeric(0.5) == 0.5
        assert PowerAnalysisNumeric(0.5) == PowerAnalysisNumeric(0.5)
        assert 0.5 == PowerAnalysisNumeric(0.5)

        with pytest.raises(RuntimeError):
            PowerAnalysisNumeric(0) == "0"

    def test_ne(self):
        assert PowerAnalysisNumeric(0) != 1
        assert PowerAnalysisNumeric(0) != PowerAnalysisNumeric(1)
        assert 0 != PowerAnalysisNumeric(1)
        assert PowerAnalysisNumeric(0.5) != 0.6
        assert PowerAnalysisNumeric(0.5) != PowerAnalysisNumeric(0.6)
        assert 0.5 != PowerAnalysisNumeric(0.6)

        with pytest.raises(RuntimeError):
            PowerAnalysisNumeric(0) != "0"

    def test_lt(self):
        assert PowerAnalysisNumeric(0) < 1
        assert PowerAnalysisNumeric(0) < PowerAnalysisNumeric(1)
        assert 0 < PowerAnalysisNumeric(1)
        assert PowerAnalysisNumeric(0.5) < 0.6
        assert PowerAnalysisNumeric(0.5) < PowerAnalysisNumeric(0.6)
        assert 0.5 < PowerAnalysisNumeric(0.6)

        with pytest.raises(RuntimeError):
            PowerAnalysisNumeric(0) < "1"

    def test_le(self):
        assert PowerAnalysisNumeric(0) <= 1
        assert PowerAnalysisNumeric(0) <= PowerAnalysisNumeric(1)
        assert 0 <= PowerAnalysisNumeric(1)
        assert PowerAnalysisNumeric(0.5) <= 0.5
        assert PowerAnalysisNumeric(0.5) <= PowerAnalysisNumeric(0.5)
        assert 0.5 <= PowerAnalysisNumeric(0.5)

        with pytest.raises(RuntimeError):
            PowerAnalysisNumeric(0) <= "1"

    def test_gt(self):
        assert PowerAnalysisNumeric(1) > 0
        assert PowerAnalysisNumeric(1) > PowerAnalysisNumeric(0)
        assert 1 > PowerAnalysisNumeric(0)
        assert PowerAnalysisNumeric(0.6) > 0.5
        assert PowerAnalysisNumeric(0.6) > PowerAnalysisNumeric(0.5)
        assert 0.6 > PowerAnalysisNumeric(0.5)

        with pytest.raises(RuntimeError):
            PowerAnalysisNumeric(1) > "0"

    def test_ge(self):
        assert PowerAnalysisNumeric(1) >= 0
        assert PowerAnalysisNumeric(1) >= PowerAnalysisNumeric(0)
        assert 1 >= PowerAnalysisNumeric(0)
        assert PowerAnalysisNumeric(0.6) >= 0.5
        assert PowerAnalysisNumeric(0.6) >= PowerAnalysisNumeric(0.5)
        assert 0.6 >= PowerAnalysisNumeric(0.5)

        with pytest.raises(RuntimeError):
            PowerAnalysisNumeric(1) >= "0"

    def test_float(self):
        assert float(PowerAnalysisNumeric(3)) == float(3.0)
        assert float(PowerAnalysisNumeric(-3)) == float(-3.0)

    def test_complex(self):
        assert complex(PowerAnalysisNumeric(3)) == complex(3.0)
        assert complex(PowerAnalysisNumeric(-3)) == complex(-3.0)

    def test_hash(self):
        assert hash(PowerAnalysisNumeric(3)) == hash(3.0)
        assert hash(PowerAnalysisNumeric(MIN_NEGATIVE_FLOAT)) == hash(MIN_NEGATIVE_FLOAT)
        assert hash(PowerAnalysisNumeric(MAX_NEGATIVE_FLOAT)) == hash(MAX_NEGATIVE_FLOAT)
        assert hash(PowerAnalysisNumeric(MIN_POSITIVE_FLOAT)) == hash(MIN_POSITIVE_FLOAT)
        assert hash(PowerAnalysisNumeric(MAX_POSITIVE_FLOAT)) == hash(MAX_POSITIVE_FLOAT)

    def test_bool(self):
        assert bool(PowerAnalysisNumeric(3)) == bool(3.0)
        assert bool(PowerAnalysisNumeric(0)) == bool(0.0)
        assert bool(PowerAnalysisNumeric(-3)) == bool(-3.0)
        assert bool(PowerAnalysisNumeric(MIN_NEGATIVE_FLOAT)) == bool(MIN_NEGATIVE_FLOAT)
        assert bool(PowerAnalysisNumeric(MAX_NEGATIVE_FLOAT)) == bool(MAX_NEGATIVE_FLOAT)
        assert bool(PowerAnalysisNumeric(MIN_POSITIVE_FLOAT)) == bool(MIN_POSITIVE_FLOAT)
        assert bool(PowerAnalysisNumeric(MAX_POSITIVE_FLOAT)) == bool(MAX_POSITIVE_FLOAT)


class TestPowerAnalysisOption:
    def test_getitem(self):
        class TestEnum(Enum, metaclass=PowerAnalysisOption):
            A = 1
            B = 2

        assert TestEnum["A"] == TestEnum.A
        assert TestEnum["a"] == TestEnum.A
        assert TestEnum["B"] == TestEnum.B
        assert TestEnum["b"] == TestEnum.B

        with pytest.raises(KeyError):
            TestEnum["C"]
        with pytest.raises(KeyError):
            TestEnum[TestEnum.A]


def test_alpha():
    assert Alpha(0.05) == 0.05

    with pytest.raises(ValueError):
        Alpha(-1)
    with pytest.raises(ValueError):
        Alpha(0)
    with pytest.raises(ValueError):
        Alpha(1)

    assert repr(Alpha(0.05)) == "Alpha(0.05)"


def test_power():
    assert Power(0.05) == 0.05

    with pytest.raises(ValueError):
        Power(-1)
    with pytest.raises(ValueError):
        Power(0)
    with pytest.raises(ValueError):
        Power(1)

    assert repr(Power(0.05)) == "Power(0.05)"


def test_mean():
    assert Mean(0) == 0

    with pytest.raises(ValueError):
        Mean(-inf)
    with pytest.raises(ValueError):
        Mean(inf)

    assert repr(Mean(0)) == "Mean(0)"


def test_std():
    assert STD(10) == 10

    with pytest.raises(ValueError):
        STD(-10)
    with pytest.raises(ValueError):
        STD(0)
    with pytest.raises(ValueError):
        STD(inf)

    assert repr(STD(10)) == "STD(10)"


def test_proportion():
    assert Proportion(0.5) == 0.5

    with pytest.raises(ValueError):
        Proportion(-1)
    with pytest.raises(ValueError):
        Proportion(0)
    with pytest.raises(ValueError):
        Proportion(1)

    assert repr(Proportion(0.5)) == "Proportion(0.5)"


def test_percent():
    assert Percent(0.5) == 0.5

    with pytest.raises(ValueError):
        Percent(-1)
    with pytest.raises(ValueError):
        Percent(0)
    with pytest.raises(ValueError):
        Percent(1)

    assert repr(Percent(0.5)) == "Percent(0.5)"


def test_ratio():
    assert Ratio(0.5) == 0.5

    with pytest.raises(ValueError):
        Ratio(-1)
    with pytest.raises(ValueError):
        Ratio(0)
    with pytest.raises(ValueError):
        Ratio(inf)

    assert repr(Ratio(0.5)) == "Ratio(0.5)"


def test_size():
    assert Size(20) == 20
    assert Size(20.142857) == 20.142857

    with pytest.raises(ValueError):
        Size(-1)
    with pytest.raises(ValueError):
        Size(0)
    with pytest.raises(ValueError):
        Size(inf)

    assert repr(Size(20)) == "Size(20)"


def test_dropout_rate():
    assert DropOutRate(0) == 0
    assert DropOutRate(0.5) == 0.5

    with pytest.raises(ValueError):
        DropOutRate(-1)
    with pytest.raises(ValueError):
        DropOutRate(1)

    assert repr(DropOutRate(0.5)) == "DropOutRate(0.5)"


def test_mix():
    alpha = Alpha(0.05)
    power = Power(0.8)
    mean = Mean(0)
    std = STD(10)
    proportion = Proportion(0.5)
    percent = Percent(0.5)
    ratio = Ratio(0.5)
    size = Size(7)
    dropout_rate = DropOutRate(0.5)

    assert alpha + power == 0.8 + 0.05
    assert alpha - mean == 0.05 - 0
    assert power * std == 0.8 * 10
    assert std / proportion == 10 / 0.5
    assert power // percent == 0.8 // 0.5
    assert ratio % size == 0.5 % 7
    assert std**dropout_rate == 3.1622776601683795
