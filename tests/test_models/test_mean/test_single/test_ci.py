# Validation Software: PASS 15
# Module: Confidence Intervals for One Mean

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.models.mean.single.ci import solve_half_width, solve_size, solve_std


@dataclass
class TestCase:
    __test__ = False

    target_half_width: float
    actual_half_width: float
    std: float
    size: int
    conf_level: float
    interval_type: Literal["one-sided", "twi-sided"]
    method: Literal["z", "t"]


case_group = (
    [
        # Regular Test Cases: half_width = 1 to 10 by 1, std = 10, conf_level = 0.95, interval_type = "one-sided", method = "z"
        TestCase(target_half_width=target_half_width, actual_half_width=actual_half_width, std=10, size=size, conf_level=0.95, interval_type="one-sided", method="z")
        for target_half_width, actual_half_width, size in [
            (1, 0.9992, 271),
            (2, 1.9947, 68),
            (3, 2.9542, 31),
            (4, 3.9894, 17),
            (5, 4.9594, 11),
            (6, 5.8154, 8),
            (7, 6.7151, 6),
            (8, 7.356, 5),
            (9, 8.2243, 4),
            (10, 9.4966, 3),
        ]
    ]
    + [
        # Regular Test Cases: half_width = 1 to 10 by 1, std = 10, conf_level = 0.95, interval_type = "two-sided", method = "z"
        TestCase(target_half_width=target_half_width, actual_half_width=actual_half_width, std=10, size=size, conf_level=0.95, interval_type="two-sided", method="z")
        for target_half_width, actual_half_width, size in [
            (1, 0.9989, 385),
            (2, 1.99, 97),
            (3, 2.9889, 43),
            (4, 3.9199, 25),
            (5, 4.8999, 16),
            (6, 5.9095, 11),
            (7, 6.9295, 8),
            (8, 7.408, 7),
            (9, 8.7652, 5),
            (10, 9.7998, 4),
        ]
    ]
    + [
        # Regular Test Cases: half_width = 1 to 10 by 1, std = 10, conf_level = 0.95, interval_type = "one-sided", method = "t"
        TestCase(target_half_width=target_half_width, actual_half_width=actual_half_width, std=10, size=size, conf_level=0.95, interval_type="one-sided", method="t")
        for target_half_width, actual_half_width, size in [
            (1, 0.9989, 273),
            (2, 1.9927, 70),
            (3, 2.9973, 32),
            (4, 3.9782, 19),
            (5, 4.9432, 13),
            (6, 5.7968, 10),
            (7, 6.6983, 8),
            (8, 7.3445, 7),
            (9, 8.2264, 6),
            (10, 9.5339, 5),
        ]
    ]
    + [
        # Regular Test Cases: half_width = 1 to 10 by 1, std = 10, conf_level = 0.95, interval_type = "two-sided", method = "t"
        TestCase(target_half_width=target_half_width, actual_half_width=actual_half_width, std=10, size=size, conf_level=0.95, interval_type="two-sided", method="t")
        for target_half_width, actual_half_width, size in [
            (1, 0.9994, 387),
            (2, 1.9945, 99),
            (3, 2.9696, 46),
            (4, 3.9559, 27),
            (5, 4.9729, 18),
            (6, 5.7738, 14),
            (7, 6.7181, 11),
            (8, 7.6867, 9),
            (9, 8.3602, 8),
            (10, 9.2485, 7),
        ]
    ]
)


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_solve_half_width(case: TestCase) -> None:
    assert (
        round(
            solve_half_width(std=case.std, size=case.size, conf_level=case.conf_level, interval_type=case.interval_type, method=case.method),
            4,
        )
        == case.actual_half_width
    )


def test_solve_size(case: TestCase) -> None:
    assert solve_size(half_width=case.target_half_width, std=case.std, conf_level=case.conf_level, interval_type=case.interval_type, method=case.method) == case.size


def test_std(case: TestCase) -> None:
    assert (
        round(
            solve_std(half_width=case.actual_half_width, size=case.size, conf_level=case.conf_level, interval_type=case.interval_type, method=case.method),
            0,
        )
        == case.std
    )
