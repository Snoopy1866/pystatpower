# Validation Software: PASS 15
# Module: Test for One Proportion


from math import ceil

import pytest

from pystatpower.models.proportion.single.difference import size


@pytest.mark.parametrize(
    "alpha, power, proportion, null_proportion, expected",
    [
        # alpha = 0.01 to 0.20 by 0.01, power = 0.80, proportion = 0.95, null_proportion = 0.80
        (0.01, 0.80, 0.95, 0.80, 66),
        (0.02, 0.80, 0.95, 0.80, 56),
        (0.03, 0.80, 0.95, 0.80, 50),
        (0.04, 0.80, 0.95, 0.80, 45),
        (0.05, 0.80, 0.95, 0.80, 42),
        (0.06, 0.80, 0.95, 0.80, 39),
        (0.07, 0.80, 0.95, 0.80, 37),
        (0.08, 0.80, 0.95, 0.80, 35),
        (0.09, 0.80, 0.95, 0.80, 33),
        (0.10, 0.80, 0.95, 0.80, 32),
        (0.11, 0.80, 0.95, 0.80, 31),
        (0.12, 0.80, 0.95, 0.80, 29),
        (0.13, 0.80, 0.95, 0.80, 28),
        (0.14, 0.80, 0.95, 0.80, 27),
        (0.15, 0.80, 0.95, 0.80, 26),
        (0.16, 0.80, 0.95, 0.80, 25),
        (0.17, 0.80, 0.95, 0.80, 24),
        (0.18, 0.80, 0.95, 0.80, 24),
        (0.19, 0.80, 0.95, 0.80, 23),
        (0.20, 0.80, 0.95, 0.80, 22),
    ],
)
def test_size_p0(alpha: float, power: float, proportion: float, null_proportion: float, expected: int) -> None:
    assert ceil(size(alpha, power, proportion, null_proportion, phat=False, continuity_correction=False)) == expected


@pytest.mark.parametrize(
    "alpha, power, proportion, null_proportion, expected",
    [
        # alpha = 0.01 to 0.20 by 0.01, power = 0.80, proportion = 0.95, null_proportion = 0.80
        (0.01, 0.80, 0.95, 0.80, 72),
        (0.02, 0.80, 0.95, 0.80, 62),
        (0.03, 0.80, 0.95, 0.80, 56),
        (0.04, 0.80, 0.95, 0.80, 52),
        (0.05, 0.80, 0.95, 0.80, 49),
        (0.06, 0.80, 0.95, 0.80, 46),
        (0.07, 0.80, 0.95, 0.80, 44),
        (0.08, 0.80, 0.95, 0.80, 42),
        (0.09, 0.80, 0.95, 0.80, 40),
        (0.10, 0.80, 0.95, 0.80, 38),
        (0.11, 0.80, 0.95, 0.80, 37),
        (0.12, 0.80, 0.95, 0.80, 36),
        (0.13, 0.80, 0.95, 0.80, 35),
        (0.14, 0.80, 0.95, 0.80, 33),
        (0.15, 0.80, 0.95, 0.80, 32),
        (0.16, 0.80, 0.95, 0.80, 32),
        (0.17, 0.80, 0.95, 0.80, 31),
        (0.18, 0.80, 0.95, 0.80, 30),
        (0.19, 0.80, 0.95, 0.80, 29),
        (0.20, 0.80, 0.95, 0.80, 28),
    ],
)
def test_size_p0_cc(alpha: float, power: float, proportion: float, null_proportion: float, expected: int) -> None:
    assert ceil(size(alpha, power, proportion, null_proportion, phat=False, continuity_correction=True)) == expected


@pytest.mark.parametrize(
    "alpha, power, proportion, null_proportion, expected",
    [
        # alpha = 0.01 to 0.20 by 0.01, power = 0.80, proportion = 0.95, null_proportion = 0.80
        (0.01, 0.80, 0.95, 0.80, 25),
        (0.02, 0.80, 0.95, 0.80, 22),
        (0.03, 0.80, 0.95, 0.80, 20),
        (0.04, 0.80, 0.95, 0.80, 18),
        (0.05, 0.80, 0.95, 0.80, 17),
        (0.06, 0.80, 0.95, 0.80, 16),
        (0.07, 0.80, 0.95, 0.80, 15),
        (0.08, 0.80, 0.95, 0.80, 15),
        (0.09, 0.80, 0.95, 0.80, 14),
        (0.10, 0.80, 0.95, 0.80, 14),
        (0.11, 0.80, 0.95, 0.80, 13),
        (0.12, 0.80, 0.95, 0.80, 13),
        (0.13, 0.80, 0.95, 0.80, 12),
        (0.14, 0.80, 0.95, 0.80, 12),
        (0.15, 0.80, 0.95, 0.80, 11),
        (0.16, 0.80, 0.95, 0.80, 11),
        (0.17, 0.80, 0.95, 0.80, 11),
        (0.18, 0.80, 0.95, 0.80, 11),
        (0.19, 0.80, 0.95, 0.80, 10),
        (0.20, 0.80, 0.95, 0.80, 10),
    ],
)
def test_size_phat(alpha: float, power: float, proportion: float, null_proportion: float, expected: int) -> None:
    assert ceil(size(alpha, power, proportion, null_proportion, phat=True, continuity_correction=False)) == expected


@pytest.mark.parametrize(
    "alpha, power, proportion, null_proportion, expected",
    [
        # alpha = 0.01 to 0.20 by 0.01, power = 0.80, proportion = 0.95, null_proportion = 0.80
        (0.01, 0.80, 0.95, 0.80, 31),
        (0.02, 0.80, 0.95, 0.80, 28),
        (0.03, 0.80, 0.95, 0.80, 26),
        (0.04, 0.80, 0.95, 0.80, 24),
        (0.05, 0.80, 0.95, 0.80, 23),
        (0.06, 0.80, 0.95, 0.80, 22),
        (0.07, 0.80, 0.95, 0.80, 22),
        (0.08, 0.80, 0.95, 0.80, 21),
        (0.09, 0.80, 0.95, 0.80, 20),
        (0.10, 0.80, 0.95, 0.80, 20),
        (0.11, 0.80, 0.95, 0.80, 19),
        (0.12, 0.80, 0.95, 0.80, 19),
        (0.13, 0.80, 0.95, 0.80, 18),
        (0.14, 0.80, 0.95, 0.80, 18),
        (0.15, 0.80, 0.95, 0.80, 17),
        (0.16, 0.80, 0.95, 0.80, 17),
        (0.17, 0.80, 0.95, 0.80, 17),
        (0.18, 0.80, 0.95, 0.80, 17),
        (0.19, 0.80, 0.95, 0.80, 16),
        (0.20, 0.80, 0.95, 0.80, 16),
    ],
)
def test_size_phat_cc(alpha: float, power: float, proportion: float, null_proportion: float, expected: int) -> None:
    assert ceil(size(alpha, power, proportion, null_proportion, phat=True, continuity_correction=True)) == expected


if __name__ == "__main__":
    from math import sqrt

    from scipy.stats import norm, t

    null_proportion = 0.80
    proportion = 0.95
    alpha = 0.68
    size = 4
    a = (proportion - null_proportion) / sqrt(proportion * (1 - proportion) / size) - t.ppf(1 - alpha / 2, size - 1)
    a = (proportion - null_proportion) * sqrt(size) / sqrt(proportion * (1 - proportion))
    b = t.ppf(1 - alpha / 2, size - 1)
    power = norm.cdf(a - b)
    print(power)

    # a = size(alpha=0.05, power=0.80, proportion=0.5, null_proportion=0.3, phat=True)
    # print(a)
