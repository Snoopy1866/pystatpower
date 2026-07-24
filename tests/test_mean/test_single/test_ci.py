# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Validation Software: PASS 15
# Module: Confidence Intervals for One Mean

from dataclasses import dataclass
from typing import Literal

from pystatpower.mean.single.ci import solve_precision
from pystatpower.mean.single.ci import solve_size
from pystatpower.mean.single.ci import solve_std
from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    std: float
    size: int
    conf_level: float
    interval_type: Literal["two-sided", "one-sided", "lower", "upper"]
    dist: Literal["z", "t"]
    precision: float
    actual_precision: float


case_group_z = [
    # precision = 1 to 10 by 1, std = 10, conf_level = 0.95, interval_type = "one-sided", dist = "z"
    TestCase(
        precision=precision,
        actual_precision=actual_precision,
        std=10,
        size=size,
        conf_level=0.95,
        interval_type="one-sided",
        dist="z",
    )
    for precision, actual_precision, size in [
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
] + [
    # precision = 1 to 10 by 1, std = 10, conf_level = 0.95, interval_type = "two-sided", dist = "z"
    TestCase(
        precision=precision,
        actual_precision=actual_precision,
        std=10,
        size=size,
        conf_level=0.95,
        interval_type="two-sided",
        dist="z",
    )
    for precision, actual_precision, size in [
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
case_group_t = [
    # precision = 1 to 10 by 1, std = 10, conf_level = 0.95, interval_type = "one-sided", dist = "t"
    TestCase(
        precision=precision,
        actual_precision=actual_precision,
        std=10,
        size=size,
        conf_level=0.95,
        interval_type="one-sided",
        dist="t",
    )
    for precision, actual_precision, size in [
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
] + [
    # precision = 1 to 10 by 1, std = 10, conf_level = 0.95, interval_type = "two-sided", dist = "t"
    TestCase(
        precision=precision,
        actual_precision=actual_precision,
        std=10,
        size=size,
        conf_level=0.95,
        interval_type="two-sided",
        dist="t",
    )
    for precision, actual_precision, size in [
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

case_group = case_group_z + case_group_t


def test_solve_precision(case: TestCase) -> None:
    assert (
        round(
            solve_precision(
                std=case.std,
                size=case.size,
                conf_level=case.conf_level,
                interval_type=case.interval_type,
                dist=case.dist,
            ),
            4,
        )
        == case.actual_precision
    )


def test_solve_size(case: TestCase) -> None:
    assert (
        solve_size(
            precision=case.precision,
            std=case.std,
            conf_level=case.conf_level,
            interval_type=case.interval_type,
            dist=case.dist,
        )
        == case.size
    )


def test_std(case: TestCase) -> None:
    assert (
        round(
            solve_std(
                precision=case.actual_precision,
                size=case.size,
                conf_level=case.conf_level,
                interval_type=case.interval_type,
                dist=case.dist,
            ),
            0,
        )
        == case.std
    )


def test_interval_type_lower_upper(case: TestCase) -> None:
    assert (
        round(
            solve_precision(
                std=case.std, size=case.size, conf_level=case.conf_level, interval_type="one-sided", dist=case.dist
            ),
            9,
        )
        == round(
            solve_precision(
                std=case.std, size=case.size, conf_level=case.conf_level, interval_type="lower", dist=case.dist
            ),
            9,
        )
        == round(
            solve_precision(
                std=case.std, size=case.size, conf_level=case.conf_level, interval_type="upper", dist=case.dist
            ),
            9,
        )
    )

    assert (
        solve_size(
            precision=case.actual_precision,
            std=case.std,
            conf_level=case.conf_level,
            interval_type="one-sided",
            dist=case.dist,
        )
        == solve_size(
            precision=case.actual_precision,
            std=case.std,
            conf_level=case.conf_level,
            interval_type="lower",
            dist=case.dist,
        )
        == solve_size(
            precision=case.actual_precision,
            std=case.std,
            conf_level=case.conf_level,
            interval_type="upper",
            dist=case.dist,
        )
    )

    assert (
        round(
            solve_std(
                precision=case.actual_precision,
                size=case.size,
                conf_level=case.conf_level,
                interval_type="one-sided",
                dist=case.dist,
            ),
            9,
        )
        == round(
            solve_std(
                precision=case.actual_precision,
                size=case.size,
                conf_level=case.conf_level,
                interval_type="lower",
                dist=case.dist,
            ),
            9,
        )
        == round(
            solve_std(
                precision=case.actual_precision,
                size=case.size,
                conf_level=case.conf_level,
                interval_type="upper",
                dist=case.dist,
            ),
            9,
        )
    )
