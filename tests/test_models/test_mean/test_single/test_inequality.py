# Validation Software: PASS 15
# Module: Tests for One Mean

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.mean.single.inequality import solve_power, solve_size, solve_null_mean, solve_mean


@dataclass
class TestCase:
    __test__ = False

    null_mean: float
    mean: float
    std: float
    size: int
    alternative: Literal["two-sided", "lower one-sided", "upper one-sided"]
    alpha: float
    power: float
    actual_power: float
    method: Literal["z", "t"]


case_group = (
    [
        # Regular Test Cases: null_mean = 30 to 40 by 1, mean = 20, std = 20, alpha = 0.05, power = 0.80, alternative = "lower one-sided", method = "z"
        TestCase(null_mean=null_mean, mean=20, std=20, size=size, alternative="lower one-sided", alpha=0.05, power=0.80, actual_power=actual_power, method="z")
        for null_mean, size, actual_power in [
            (30, 25, 0.8038),
            (31, 21, 0.8094),
            (32, 18, 0.8161),
            (33, 15, 0.8086),
            (34, 13, 0.8103),
            (35, 11, 0.8003),
            (36, 10, 0.8119),
            (37, 9, 0.8173),
            (38, 8, 0.8161),
            (39, 7, 0.8075),
            (40, 7, 0.8416),
        ]
    ]
    + [
        # Regular Test Cases: null_mean = 20, mean = 30 to 40 by 1, std = 20, alpha = 0.05, power = 0.80, alternative = "upper one-sided", method = "z"
        TestCase(null_mean=20, mean=mean, std=20, size=size, alternative="upper one-sided", alpha=0.05, power=0.80, actual_power=actual_power, method="z")
        for mean, size, actual_power in [
            (30, 25, 0.8038),
            (31, 21, 0.8094),
            (32, 18, 0.8161),
            (33, 15, 0.8086),
            (34, 13, 0.8103),
            (35, 11, 0.8003),
            (36, 10, 0.8119),
            (37, 9, 0.8173),
            (38, 8, 0.8161),
            (39, 7, 0.8075),
            (40, 7, 0.8416),
        ]
    ]
    + [
        # Regular Test Cases: null_mean = 20, mean = 30 to 40 by 1, std = 20, alpha = 0.05, power = 0.80, alternative = "two-sided", method = "z"
        TestCase(null_mean=20, mean=mean, std=20, size=size, alternative="two-sided", alpha=0.05, power=0.80, actual_power=actual_power, method="z")
        for mean, size, actual_power in [
            (30, 32, 0.8074),
            (31, 26, 0.8008),
            (32, 22, 0.8035),
            (33, 19, 0.8088),
            (34, 17, 0.8228),
            (35, 14, 0.8013),
            (36, 13, 0.8224),
            (37, 11, 0.8049),
            (38, 10, 0.8122),
            (39, 9, 0.8133),
            (40, 8, 0.8074),
        ]
    ]
    + [
        # Regular Test Cases: null_mean = 30 to 40 by 1, mean = 20, std = 20, alpha = 0.05, power = 0.80, alternative = "lower one-sided", method = "t"
        TestCase(null_mean=null_mean, mean=20, std=20, size=size, alternative="lower one-sided", alpha=0.05, power=0.80, actual_power=actual_power, method="t")
        for null_mean, size, actual_power in [
            (30, 27, 0.8118),
            (31, 22, 0.8024),
            (32, 19, 0.8079),
            (33, 17, 0.8210),
            (34, 15, 0.8243),
            (35, 13, 0.8165),
            (36, 12, 0.8290),
            (37, 11, 0.8355),
            (38, 10, 0.8360),
            (39, 9, 0.8297),
            (40, 8, 0.8150),
        ]
    ]
    + [
        # Regular Test Cases: null_mean = 20, mean = 30 to 40 by 1, std = 20, alpha = 0.05, power = 0.80, alternative = "upper one-sided", method = "t"
        TestCase(null_mean=20, mean=mean, std=20, size=size, alternative="upper one-sided", alpha=0.05, power=0.80, actual_power=actual_power, method="t")
        for mean, size, actual_power in [
            (30, 27, 0.8118),
            (31, 22, 0.8024),
            (32, 19, 0.8079),
            (33, 17, 0.8210),
            (34, 15, 0.8243),
            (35, 13, 0.8165),
            (36, 12, 0.8290),
            (37, 11, 0.8355),
            (38, 10, 0.8360),
            (39, 9, 0.8297),
            (40, 8, 0.8150),
        ]
    ]
    + [
        # Regular Test Cases: null_mean = 20, mean = 30 to 40 by 1, std = 20, alpha = 0.05, power = 0.80, alternative = "two-sided", method = "t"
        TestCase(null_mean=20, mean=mean, std=20, size=size, alternative="two-sided", alpha=0.05, power=0.80, actual_power=actual_power, method="t")
        for mean, size, actual_power in [
            (30, 34, 0.8078),
            (31, 28, 0.8011),
            (32, 24, 0.8037),
            (33, 21, 0.8087),
            (34, 19, 0.8225),
            (35, 16, 0.8006),
            (36, 15, 0.8213),
            (37, 13, 0.8031),
            (38, 12, 0.8098),
            (39, 11, 0.8100),
            (40, 10, 0.8031),
        ]
    ]
)


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_solve_power(case: TestCase) -> None:
    assert (
        round(
            solve_power(null_mean=case.null_mean, mean=case.mean, std=case.std, size=case.size, alternative=case.alternative, alpha=case.alpha, method=case.method),
            4,
        )
        == case.actual_power
    )


def test_solve_size(case: TestCase) -> None:
    if case in [
        TestCase(null_mean=20, mean=40, std=20, size=8, alternative="upper one-sided", alpha=0.05, power=0.8, actual_power=0.815, method="t"),
        TestCase(null_mean=20, mean=30, std=20, size=34, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8078, method="t"),
        TestCase(null_mean=20, mean=31, std=20, size=28, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8011, method="t"),
        TestCase(null_mean=20, mean=32, std=20, size=24, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8037, method="t"),
        TestCase(null_mean=20, mean=33, std=20, size=21, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8087, method="t"),
        TestCase(null_mean=20, mean=34, std=20, size=19, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8225, method="t"),
        TestCase(null_mean=20, mean=35, std=20, size=16, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8006, method="t"),
        TestCase(null_mean=20, mean=36, std=20, size=15, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8213, method="t"),
        TestCase(null_mean=20, mean=37, std=20, size=13, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8031, method="t"),
        TestCase(null_mean=20, mean=38, std=20, size=12, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8098, method="t"),
        TestCase(null_mean=20, mean=39, std=20, size=11, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.81, method="t"),
        TestCase(null_mean=20, mean=40, std=20, size=10, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8031, method="t"),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")
    assert solve_size(null_mean=case.null_mean, mean=case.mean, std=case.std, alternative=case.alternative, alpha=case.alpha, power=case.power, method=case.method) == case.size


def test_solve_null_mean(case: TestCase) -> None:
    if case in [
        TestCase(null_mean=20, mean=33, std=20, size=17, alternative="upper one-sided", alpha=0.05, power=0.8, actual_power=0.821, method="t"),
        TestCase(null_mean=20, mean=34, std=20, size=15, alternative="upper one-sided", alpha=0.05, power=0.8, actual_power=0.8243, method="t"),
        TestCase(null_mean=20, mean=40, std=20, size=8, alternative="upper one-sided", alpha=0.05, power=0.8, actual_power=0.815, method="t"),
        TestCase(null_mean=20, mean=30, std=20, size=34, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8078, method="t"),
        TestCase(null_mean=20, mean=31, std=20, size=28, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8011, method="t"),
        TestCase(null_mean=20, mean=32, std=20, size=24, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8037, method="t"),
        TestCase(null_mean=20, mean=33, std=20, size=21, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8087, method="t"),
        TestCase(null_mean=20, mean=34, std=20, size=19, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8225, method="t"),
        TestCase(null_mean=20, mean=35, std=20, size=16, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8006, method="t"),
        TestCase(null_mean=20, mean=36, std=20, size=15, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8213, method="t"),
        TestCase(null_mean=20, mean=37, std=20, size=13, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8031, method="t"),
        TestCase(null_mean=20, mean=38, std=20, size=12, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8098, method="t"),
        TestCase(null_mean=20, mean=39, std=20, size=11, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.81, method="t"),
        TestCase(null_mean=20, mean=40, std=20, size=10, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8031, method="t"),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    search_direction = "below" if case.null_mean < case.mean else "above"
    assert (
        round(
            solve_null_mean(mean=case.mean, std=case.std, size=case.size, alternative=case.alternative, alpha=case.alpha, power=case.actual_power, method=case.method, search_direction=search_direction),
            0,
        )
        == case.null_mean
    )


def test_solve_mean(case: TestCase) -> None:
    if case in [
        TestCase(null_mean=20, mean=33, std=20, size=17, alternative="upper one-sided", alpha=0.05, power=0.8, actual_power=0.821, method="t"),
        TestCase(null_mean=20, mean=34, std=20, size=15, alternative="upper one-sided", alpha=0.05, power=0.8, actual_power=0.8243, method="t"),
        TestCase(null_mean=20, mean=40, std=20, size=8, alternative="upper one-sided", alpha=0.05, power=0.8, actual_power=0.815, method="t"),
        TestCase(null_mean=20, mean=30, std=20, size=34, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8078, method="t"),
        TestCase(null_mean=20, mean=31, std=20, size=28, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8011, method="t"),
        TestCase(null_mean=20, mean=32, std=20, size=24, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8037, method="t"),
        TestCase(null_mean=20, mean=33, std=20, size=21, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8087, method="t"),
        TestCase(null_mean=20, mean=34, std=20, size=19, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8225, method="t"),
        TestCase(null_mean=20, mean=35, std=20, size=16, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8006, method="t"),
        TestCase(null_mean=20, mean=36, std=20, size=15, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8213, method="t"),
        TestCase(null_mean=20, mean=37, std=20, size=13, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8031, method="t"),
        TestCase(null_mean=20, mean=38, std=20, size=12, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8098, method="t"),
        TestCase(null_mean=20, mean=39, std=20, size=11, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.81, method="t"),
        TestCase(null_mean=20, mean=40, std=20, size=10, alternative="two-sided", alpha=0.05, power=0.8, actual_power=0.8031, method="t"),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    search_direction = "below" if case.mean < case.null_mean else "above"
    assert (
        round(
            solve_mean(null_mean=case.null_mean, std=case.std, size=case.size, alternative=case.alternative, alpha=case.alpha, power=case.actual_power, method=case.method, search_direction=search_direction),
            0,
        )
        == case.mean
    )
