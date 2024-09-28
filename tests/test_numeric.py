from math import inf, nan

import pytest

from pystatpower.numeric import *


class ForwardOperatorNotImplementedNumeric(Numeric):
    def __add__(self, other):
        return NotImplemented

    def __sub__(self, other):
        return NotImplemented

    def __mul__(self, other):
        return NotImplemented

    def __truediv__(self, other):
        return NotImplemented

    def __floordiv__(self, other):
        return NotImplemented

    def __mod__(self, other):
        return NotImplemented

    def __pow__(self, base, modulo=None):
        return NotImplemented


class TestInterval:
    def test_contains(self):
        assert 0.5 in Interval(0, 1)
        assert 0 in Interval(0, 1, lower_inclusive=True)
        assert 1 in Interval(0, 1, upper_inclusive=True)
        assert 0 in Interval(0, 1, lower_inclusive=True, upper_inclusive=True)
        assert 1 in Interval(0, 1, lower_inclusive=True, upper_inclusive=True)

        with pytest.raises(TypeError):
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

        with pytest.raises(TypeError):
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


class TestNumeric:
    def test_domain(self):
        assert Numeric._domain == Interval(-MAX_FLOAT, MAX_FLOAT, lower_inclusive=True, upper_inclusive=True)

    def test_init(self):
        assert Numeric(0) == 0
        assert Numeric(0.5) == 0.5
        assert Numeric(1) == 1
        assert Numeric(-MAX_FLOAT) == -MAX_FLOAT
        assert Numeric(-MIN_FLOAT) == -MIN_FLOAT
        assert Numeric(MIN_FLOAT) == MIN_FLOAT
        assert Numeric(MAX_FLOAT) == MAX_FLOAT

        with pytest.raises(TypeError):
            Numeric("0.5")
        with pytest.raises(ValueError):
            Numeric(nan)

    def test_pseudo_domain(self):
        assert Numeric.pseudo_bound() == (-MAX_FLOAT, MAX_FLOAT)
        assert Alpha.pseudo_bound() == (0 + MIN_FLOAT, 1 - MIN_FLOAT)
        assert Power.pseudo_bound() == (0 + MIN_FLOAT, 1 - MIN_FLOAT)
        assert Mean.pseudo_bound() == (-MAX_FLOAT + MIN_FLOAT, MAX_FLOAT - MIN_FLOAT)
        assert STD.pseudo_bound() == (0 + MIN_FLOAT, MAX_FLOAT - MIN_FLOAT)
        assert Proportion.pseudo_bound() == (0 + MIN_FLOAT, 1 - MIN_FLOAT)
        assert Percent.pseudo_bound() == (0 + MIN_FLOAT, 1 - MIN_FLOAT)
        assert Ratio.pseudo_bound() == (0 + MIN_FLOAT, MAX_FLOAT - MIN_FLOAT)
        assert Size.pseudo_bound() == (0 + MIN_FLOAT, MAX_FLOAT - MIN_FLOAT)
        assert DropOutRate.pseudo_bound() == (0, 1 - MIN_FLOAT)

    def test_repr(self):
        assert repr(Numeric(0)) == f"{Numeric.__name__}(0)"
        assert repr(Numeric(0.5)) == f"{Numeric.__name__}(0.5)"
        assert repr(Numeric(1)) == f"{Numeric.__name__}(1)"
        assert repr(Numeric(-MAX_FLOAT)) == f"{Numeric.__name__}({-MAX_FLOAT})"
        assert repr(Numeric(-MIN_FLOAT)) == f"{Numeric.__name__}({-MIN_FLOAT})"
        assert repr(Numeric(MIN_FLOAT)) == f"{Numeric.__name__}({MIN_FLOAT})"
        assert repr(Numeric(MAX_FLOAT)) == f"{Numeric.__name__}({MAX_FLOAT})"

    def test_add(self):
        assert Numeric(1) + 1 == 2
        assert Numeric(1) + Numeric(1) == 2

        assert Numeric(1) + 0.5 == 1.5
        assert Numeric(1) + Numeric(0.5) == 1.5

        with pytest.raises(TypeError):
            Numeric(1) + "1"

    def test_radd(self):
        assert 1 + Numeric(1) == 2
        assert 1 + Numeric(0.5) == 1.5

        assert ForwardOperatorNotImplementedNumeric(1) + Numeric(0.5) == 1.5

        with pytest.raises(TypeError):
            "1" + Numeric(1)

    def test_sub(self):
        assert Numeric(1) - 1 == 0
        assert Numeric(1) - Numeric(1) == 0

        assert Numeric(1) - 0.5 == 0.5
        assert Numeric(1) - Numeric(0.5) == 0.5

        with pytest.raises(TypeError):
            Numeric(1) - "1"

    def test_rsub(self):
        assert 1 - Numeric(1) == 0
        assert 1 - Numeric(0.5) == 0.5

        assert ForwardOperatorNotImplementedNumeric(1) - Numeric(0.5) == 0.5

        with pytest.raises(TypeError):
            "1" - Numeric(1)

    def test_mul(self):
        assert Numeric(2) * 4 == 8
        assert Numeric(2) * Numeric(4) == 8

        assert Numeric(2) * 0.5 == 1
        assert Numeric(2) * Numeric(0.5) == 1

        with pytest.raises(TypeError):
            Numeric(2) * "4"

    def test_rmul(self):
        assert 2 * Numeric(4) == 8
        assert 2 * Numeric(0.5) == 1

        assert ForwardOperatorNotImplementedNumeric(2) * Numeric(0.5) == 1

        with pytest.raises(TypeError):
            "4" * Numeric(2)

    def test_truediv(self):
        assert Numeric(1) / 2 == 0.5
        assert Numeric(1) / Numeric(2) == 0.5

        assert Numeric(1) / 0.5 == 2
        assert Numeric(1) / Numeric(0.5) == 2

        assert Numeric(1) / 3 == 1 / 3
        assert Numeric(1) / Numeric(3) == 1 / 3

        with pytest.raises(TypeError):
            Numeric(1) / "2"

    def test_rtruediv(self):
        assert 1 / Numeric(2) == 0.5
        assert 1 / Numeric(0.5) == 2

        assert 1 / Numeric(3) == 1 / 3

        assert ForwardOperatorNotImplementedNumeric(1) / Numeric(2) == 0.5

        with pytest.raises(TypeError):
            "2" / Numeric(1)

    def test_floordiv(self):
        assert Numeric(3) // 2 == 1
        assert Numeric(3) // Numeric(2) == 1

        with pytest.raises(TypeError):
            Numeric(3) // "2"

    def test_rfloordiv(self):
        assert 3 // Numeric(2) == 1

        assert ForwardOperatorNotImplementedNumeric(3) // Numeric(2) == 1

        with pytest.raises(TypeError):
            "3" // Numeric(2)

    def test_mod(self):
        assert Numeric(5) % 3 == 2
        assert Numeric(5) % Numeric(3) == 2

        with pytest.raises(TypeError):
            Numeric(5) % "3"

    def test_rmod(self):
        assert 3 % Numeric(2) == 1

        assert ForwardOperatorNotImplementedNumeric(3) % Numeric(2) == 1

        class Person:
            pass

        with pytest.raises(TypeError):
            Person() % Numeric(2)

    def test_pow(self):
        assert Numeric(2) ** 3 == 8
        assert Numeric(2) ** Numeric(3) == 8

        assert Numeric(2) ** 0.5 == 2**0.5

        with pytest.raises(TypeError):
            Numeric(2) ** "3"

    def test_rpow(self):
        assert 2 ** Numeric(3) == 8
        assert 2 ** Numeric(0.5) == 2**0.5

        assert ForwardOperatorNotImplementedNumeric(2) ** Numeric(3) == 8

        with pytest.raises(TypeError):
            "2" ** Numeric(3)

    def test_abs(self):
        assert abs(Numeric(3)) == 3
        assert abs(Numeric(-3)) == 3

    def test_neg(self):
        assert -Numeric(3) == -3
        assert -Numeric(-3) == 3

    def test_pos(self):
        assert +Numeric(3) == 3
        assert +Numeric(-3) == -3

    def test_trunc(self):
        assert trunc(Numeric(3.14)) == 3
        assert trunc(Numeric(-3.14)) == -3

    def test_int(self):
        assert int(Numeric(3.14)) == 3
        assert int(Numeric(-3.14)) == -3

    def test_floor(self):
        assert floor(Numeric(3.14)) == 3
        assert floor(Numeric(-3.14)) == -4

    def test_ceil(self):
        assert ceil(Numeric(3.14)) == 4
        assert ceil(Numeric(-3.14)) == -3

    def test_round(self):
        assert round(Numeric(3.1415)) == 3
        assert round(Numeric(-3.1415)) == -3
        assert round(Numeric(3.1415), 3) == 3.142
        assert round(Numeric(-3.1415), 3) == -3.142

    def test_eq(self):
        assert Numeric(0) == 0
        assert Numeric(0) == Numeric(0)
        assert 0 == Numeric(0)
        assert Numeric(0.5) == 0.5
        assert Numeric(0.5) == Numeric(0.5)
        assert 0.5 == Numeric(0.5)

        with pytest.raises(TypeError):
            Numeric(0) == "0"

    def test_ne(self):
        assert Numeric(0) != 1
        assert Numeric(0) != Numeric(1)
        assert 0 != Numeric(1)
        assert Numeric(0.5) != 0.6
        assert Numeric(0.5) != Numeric(0.6)
        assert 0.5 != Numeric(0.6)

        with pytest.raises(TypeError):
            Numeric(0) != "0"

    def test_lt(self):
        assert Numeric(0) < 1
        assert Numeric(0) < Numeric(1)
        assert 0 < Numeric(1)
        assert Numeric(0.5) < 0.6
        assert Numeric(0.5) < Numeric(0.6)
        assert 0.5 < Numeric(0.6)

        with pytest.raises(TypeError):
            Numeric(0) < "1"

    def test_le(self):
        assert Numeric(0) <= 1
        assert Numeric(0) <= Numeric(1)
        assert 0 <= Numeric(1)
        assert Numeric(0.5) <= 0.5
        assert Numeric(0.5) <= Numeric(0.5)
        assert 0.5 <= Numeric(0.5)

        with pytest.raises(TypeError):
            Numeric(0) <= "1"

    def test_gt(self):
        assert Numeric(1) > 0
        assert Numeric(1) > Numeric(0)
        assert 1 > Numeric(0)
        assert Numeric(0.6) > 0.5
        assert Numeric(0.6) > Numeric(0.5)
        assert 0.6 > Numeric(0.5)

        with pytest.raises(TypeError):
            Numeric(1) > "0"

    def test_ge(self):
        assert Numeric(1) >= 0
        assert Numeric(1) >= Numeric(0)
        assert 1 >= Numeric(0)
        assert Numeric(0.6) >= 0.5
        assert Numeric(0.6) >= Numeric(0.5)
        assert 0.6 >= Numeric(0.5)

        with pytest.raises(TypeError):
            Numeric(1) >= "0"

    def test_float(self):
        assert float(Numeric(3)) == float(3.0)
        assert float(Numeric(-3)) == float(-3.0)

    def test_complex(self):
        assert complex(Numeric(3)) == complex(3.0)
        assert complex(Numeric(-3)) == complex(-3.0)

    def test_hash(self):
        assert hash(Numeric(3)) == hash(3.0)
        assert hash(Numeric(-MAX_FLOAT)) == hash(-MAX_FLOAT)
        assert hash(Numeric(-MIN_FLOAT)) == hash(-MIN_FLOAT)
        assert hash(Numeric(MIN_FLOAT)) == hash(MIN_FLOAT)
        assert hash(Numeric(MAX_FLOAT)) == hash(MAX_FLOAT)

    def test_bool(self):
        assert bool(Numeric(3)) == bool(3.0)
        assert bool(Numeric(0)) == bool(0.0)
        assert bool(Numeric(-3)) == bool(-3.0)
        assert bool(Numeric(-MAX_FLOAT)) == bool(-MAX_FLOAT)
        assert bool(Numeric(-MIN_FLOAT)) == bool(-MIN_FLOAT)
        assert bool(Numeric(MIN_FLOAT)) == bool(MIN_FLOAT)
        assert bool(Numeric(MAX_FLOAT)) == bool(MAX_FLOAT)


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
