# Validation Software: PASS 15
# Module: Tests for One Mean

from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.mean.single.inequality import _verify_mean_and_get_diff, solve_power, solve_size, solve_null_mean, solve_mean, solve_std

from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    mean: float | None = None
    null_mean: float | None = None
    diff: float | None = None
    std: float
    size: int
    alternative: Literal["two-sided", "greater", "less"]
    alpha: float
    power: float
    actual_power: float
    dist: Literal["z", "t"]
    direction: Literal["greater", "less"] | None = None

    def __post_init__(self) -> None:
        self.diff = _verify_mean_and_get_diff(self.mean, self.null_mean, self.diff)

        # Set the values ​​of mean and null_mean according to diff
        if self.mean is None and self.null_mean is None and self.diff is not None:
            self.null_mean = self.size
            self.mean = self.diff + self.null_mean


case_group_z = (
    [
        # null_mean = 20, mean = 30 to 40 by 1, std = 20, alpha = 0.05, power = 0.80, alternative = "two-sided", dist = "z"
        TestCase(null_mean=20, mean=mean, std=20, size=size, alternative="two-sided", alpha=0.05, power=0.80, actual_power=actual_power, dist="z")
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
        # null_mean = 20, mean = 30 to 40 by 1, std = 20, alpha = 0.05, power = 0.80, alternative = "greater", dist = "z"
        TestCase(null_mean=20, mean=mean, std=20, size=size, alternative="greater", alpha=0.05, power=0.80, actual_power=actual_power, dist="z")
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
        # null_mean = 30 to 40 by 1, mean = 20, std = 20, alpha = 0.05, power = 0.80, alternative = "less", dist = "z"
        TestCase(null_mean=null_mean, mean=20, std=20, size=size, alternative="less", alpha=0.05, power=0.80, actual_power=actual_power, dist="z")
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
)


case_group_t = (
    [
        # null_mean = 20, mean = 30 to 40 by 1, std = 20, alpha = 0.05, power = 0.80, alternative = "two-sided", dist = "t"
        TestCase(null_mean=20, mean=mean, std=20, size=size, alternative="two-sided", alpha=0.05, power=0.80, actual_power=actual_power, dist="t")
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
    + [
        # null_mean = 20, mean = 30 to 40 by 1, std = 20, alpha = 0.05, power = 0.80, alternative = "greater", dist = "t"
        TestCase(null_mean=20, mean=mean, std=20, size=size, alternative="greater", alpha=0.05, power=0.80, actual_power=actual_power, dist="t")
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
        # null_mean = 30 to 40 by 1, mean = 20, std = 20, alpha = 0.05, power = 0.80, alternative = "less", dist = "t"
        TestCase(null_mean=null_mean, mean=20, std=20, size=size, alternative="less", alpha=0.05, power=0.80, actual_power=actual_power, dist="t")
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
)

case_group = case_group_z + case_group_t


def test_verify_mean_and_get_diff() -> None:
    with pytest.raises(ValueError):
        _verify_mean_and_get_diff(mean=None, null_mean=None, diff=None)

    with pytest.raises(ValueError):
        _verify_mean_and_get_diff(mean=None, null_mean=10, diff=None)

    with pytest.raises(ValueError):
        _verify_mean_and_get_diff(mean=20, null_mean=None, diff=None)

    _verify_mean_and_get_diff(mean=20, null_mean=10, diff=None)
    _verify_mean_and_get_diff(mean=None, null_mean=None, diff=10)
    _verify_mean_and_get_diff(mean=None, null_mean=10, diff=10)
    _verify_mean_and_get_diff(mean=20, null_mean=None, diff=10)
    _verify_mean_and_get_diff(mean=20, null_mean=10, diff=10)


def test_solve_power(case: TestCase) -> None:
    assert (
        round(
            solve_power(
                null_mean=case.null_mean,
                mean=case.mean,
                std=case.std,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                dist=case.dist,
            ),
            4,
        )
        == case.actual_power
    )


def test_solve_size(case: TestCase, request: pytest.FixtureRequest) -> None:

    if request.config.is_linux and request.config.is_py310:
        if (case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t") or (case.mean in (34,) and case.alternative == "greater" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py311:
        if case in [
            TestCase(null_mean=20, mean=34, std=20, size=15, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8243, dist="t"),
        ] or (case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py312:
        if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py313:
        if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py314:
        if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py310:
        if case in [
            TestCase(null_mean=20, mean=30, std=20, size=27, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8118, dist="t"),
            TestCase(null_mean=20, mean=34, std=20, size=15, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8243, dist="t"),
            TestCase(null_mean=20, mean=40, std=20, size=8, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8150, dist="t"),
        ] or (case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py311:
        if (case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t") or (case.mean in (30, 34) and case.alternative == "greater" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py312:
        if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py313:
        if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py314:
        if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py310:
        if (case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t") or (case.mean in (34, 40) and case.alternative == "greater" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py311:
        if (case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t") or (case.mean in (30, 34) and case.alternative == "greater" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py312:
        if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py313:
        if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py314:
        if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    assert (
        solve_size(
            null_mean=case.null_mean,
            mean=case.mean,
            std=case.std,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.power,
            dist=case.dist,
        )
        == case.size
    )


def test_solve_null_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if request.config.is_linux and request.config.is_py310:
        if (case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t") or (case.mean in (33,) and case.alternative == "greater" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py311:
        if case.mean in (31, 33, 34, 35, 36, 37) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py312:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py313:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py314:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py310:
        if case.mean in (32, 33, 34, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py311:
        if case.mean in (31, 34, 35, 36, 37) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py312:
        if case.mean in (31, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py313:
        if case.mean in (31, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py314:
        if case.mean in (31, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py310:
        if case in [
            TestCase(null_mean=20, mean=33, std=20, size=17, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8210, dist="t"),
        ] or (case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py311:
        if case in [
            TestCase(null_mean=20, mean=33, std=20, size=17, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8210, dist="t"),
        ] or (case.mean in (30, 31, 33, 34, 35, 36, 37, 38) and case.alternative == "two-sided" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py312:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py313:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py314:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    direction = "greater" if case.null_mean > case.mean else "less"
    assert (
        round(
            solve_null_mean(
                mean=case.mean,
                std=case.std,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                direction=direction,
            ),
            0,
        )
        == case.null_mean
    )


def test_solve_null_mean_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_null_mean(mean=20, std=20, size=17, alternative="two-sided", alpha=0.05, power=0.8, dist="t")


def test_solve_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if request.config.is_linux and request.config.is_py310:
        if (case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t") or (case.mean in (33,) and case.alternative == "greater" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py311:
        if case.mean in (31, 33, 34, 35, 36, 37) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py312:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py313:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py314:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py310:
        if case.mean in (32, 33, 34, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py311:
        if case.mean in (31, 34, 35, 36, 37) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py312:
        if case.mean in (31, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py313:
        if case.mean in (31, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py314:
        if case.mean in (31, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py310:
        if case in [
            TestCase(null_mean=20, mean=33, std=20, size=17, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8210, dist="t"),
        ] or (case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py311:
        if case in [
            TestCase(null_mean=20, mean=33, std=20, size=17, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8210, dist="t"),
        ] or (case.mean in (30, 31, 33, 34, 35, 36, 37, 38) and case.alternative == "two-sided" and case.dist == "t"):
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py312:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py313:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py314:
        if case.mean in (31, 33, 34, 35, 36) and case.alternative == "two-sided" and case.dist == "t":
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    direction = "greater" if case.mean > case.null_mean else "less"
    assert (
        round(
            solve_mean(
                null_mean=case.null_mean,
                std=case.std,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                direction=direction,
            ),
            0,
        )
        == case.mean
    )


def test_solve_mean_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_mean(null_mean=20, std=20, size=17, alternative="two-sided", alpha=0.05, power=0.8, dist="t")


def test_solve_std(case: TestCase, request: pytest.FixtureRequest) -> None:
    assert (
        round(
            solve_std(
                null_mean=case.null_mean,
                mean=case.mean,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
            ),
            0,
        )
        == case.std
    )
