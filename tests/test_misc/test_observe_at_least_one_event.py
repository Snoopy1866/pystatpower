# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import Literal

from pystatpower.misc.observe_at_least_one_event import solve_power
from pystatpower.misc.observe_at_least_one_event import solve_proportion
from pystatpower.misc.observe_at_least_one_event import solve_size
from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    proportion: float
    size: int
    dist: Literal["bin", "poisson"]
    power: float
    actual_power: float | None = None

    def __post_init__(self) -> None:
        self.actual_power = solve_power(proportion=self.proportion, size=self.size, dist=self.dist)


case_group_bin = [
    # Reference: 郑青山,孙瑞元,陈志扬.新药临床试验最低例数规定的安全性评价[J].中国临床药理学与治疗学,2003,(3)354-355.
    TestCase(proportion=proportion, size=size, power=power, dist="bin")
    for proportion, size, power in [
        (0.01, 161, 0.80),
        (0.01, 189, 0.85),
        (0.01, 230, 0.90),
        (0.01, 299, 0.95),
        (0.01, 459, 0.99),
        (0.02, 80, 0.80),
        (0.02, 94, 0.85),
        (0.02, 114, 0.90),
        (0.02, 149, 0.95),
        (0.02, 228, 0.99),
    ]
] + [
    # Reference: 可吸收止血产品注册审查指导原则 (2024年修订版)
    TestCase(proportion=proportion, size=size, power=power, dist="bin")
    for proportion, size, power in [
        (0.001, 100, 0.095),
        (0.001, 150, 0.139),
        (0.001, 200, 0.181),
        (0.002, 100, 0.181),
        (0.002, 150, 0.259),
        (0.002, 201, 0.330),
        (0.005, 100, 0.394),
        (0.005, 151, 0.529),
        (0.005, 200, 0.633),
        (0.008, 100, 0.552),
        (0.008, 150, 0.700),
        (0.008, 200, 0.799),
        (0.010, 101, 0.634),
        (0.010, 151, 0.779),
        (0.010, 200, 0.866),
    ]
]


case_group_poisson = [
    # Reference: 可吸收止血产品注册审查指导原则 (2024年修订版)
    TestCase(proportion=proportion, size=size, power=power, dist="poisson")
    for proportion, size, power in [
        (0.001, 100, 0.095),
        (0.001, 150, 0.139),
        (0.001, 200, 0.181),
        (0.002, 100, 0.181),
        (0.002, 150, 0.259),
        (0.002, 201, 0.330),
        (0.005, 100, 0.393),
        (0.005, 151, 0.528),
        (0.005, 200, 0.632),
        (0.008, 101, 0.551),
        (0.008, 151, 0.699),
        (0.008, 200, 0.798),
        (0.010, 100, 0.632),
        (0.010, 151, 0.777),
        (0.010, 201, 0.865),
    ]
]


case_group = case_group_bin + case_group_poisson


def test_solve_power(case: TestCase) -> None:

    assert round(
        solve_power(
            proportion=case.proportion,
            size=case.size,
            dist=case.dist,
        ),
        6,
    ) == round(case.actual_power, 6)


def test_solve_size(case: TestCase) -> None:

    assert (
        solve_size(
            proportion=case.proportion,
            power=case.power,
            dist=case.dist,
        )
        == case.size
    )


def test_solve_proportion(case: TestCase) -> None:

    assert round(
        solve_proportion(
            size=case.size,
            power=case.actual_power,
            dist=case.dist,
        ),
        3,
    ) == round(case.proportion, 3)
