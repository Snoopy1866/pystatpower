# Validation Software: PASS 15
# Module: Superiority by a Margin Tests for One Mean (One-Sample or Paired T-Test)

from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.mean.single.superiority import _verify_mean_and_get_diff, solve_power, solve_size, solve_diff, solve_null_mean, solve_mean, solve_std, solve_margin

from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    mean: float | None = None
    null_mean: float | None = None
    diff: float | None = None
    margin: float
    std: float
    size: int
    alternative: Literal["greater", "less"]
    alpha: float
    power: float
    actual_power: float

    def __post_init__(self) -> None:
        self.diff = _verify_mean_and_get_diff(self.mean, self.null_mean, self.diff)

        # Set the values ​​of mean and null_mean according to diff
        if self.mean is None and self.null_mean is None and self.diff is not None:
            self.null_mean = self.size
            self.mean = self.diff + self.null_mean


case_group = [
    # diff = 15, std = 15, margin = 0 to 10 by 0.5, alpha = 0.025, power = 0.80, alternative = "greater"
    TestCase(null_mean=None, mean=None, diff=15, margin=margin, std=15, size=size, alternative="greater", alpha=0.025, power=0.80, actual_power=actual_power)
    for margin, size, actual_power in [
        (0.5, 11, 0.823125590),
        (1.0, 12, 0.836781945),
        (1.5, 12, 0.809784845),
        (2.0, 13, 0.817900777),
        (2.5, 14, 0.821564243),
        (3.0, 15, 0.821309977),
        (3.5, 16, 0.817438156),
        (4.0, 17, 0.810070484),
        (4.5, 19, 0.822546679),
        (5.0, 20, 0.807290896),
        (5.5, 22, 0.808524347),
        (6.0, 24, 0.803670529),
        (6.5, 27, 0.809008881),
        (7.0, 30, 0.806009921),
        (7.5, 34, 0.807776686),
        (8.0, 39, 0.810570919),
        (8.5, 44, 0.802257042),
        (9.0, 52, 0.807786982),
        (9.5, 61, 0.804464986),
        (10.0, 73, 0.802298026),
    ]
] + [
    # diff = -15, std = 20, margin = -10 to 0 by 0.5, alpha = 0.025, power = 0.80, alternative = "less"
    TestCase(null_mean=None, mean=None, diff=-15, margin=margin, std=20, size=size, alternative="less", alpha=0.025, power=0.80, actual_power=actual_power)
    for margin, size, actual_power in [
        (-10.0, 128, 0.801506203),
        (-9.5, 106, 0.801041955),
        (-9.0, 90, 0.803793402),
        (-8.5, 77, 0.803915153),
        (-8.0, 67, 0.805928876),
        (-7.5, 58, 0.801649746),
        (-7.0, 52, 0.807786982),
        (-6.5, 46, 0.805246965),
        (-6.0, 41, 0.802793253),
        (-5.5, 37, 0.802755285),
        (-5.0, 34, 0.807776686),
        (-4.5, 31, 0.807415274),
        (-4.0, 28, 0.801082214),
        (-3.5, 26, 0.804482491),
        (-3.0, 24, 0.803670529),
        (-2.5, 23, 0.817106721),
        (-2.0, 21, 0.808703861),
        (-1.5, 20, 0.816793619),
        (-1.0, 19, 0.822546679),
        (-0.5, 17, 0.801229726),
    ]
]


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
                diff=case.diff,
                margin=case.margin,
                std=case.std,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
            ),
            9,
        )
        == case.actual_power
    )


def test_solve_size(case: TestCase, request: pytest.FixtureRequest) -> None:

    if request.config.is_linux and request.config.is_py310:
        if case.alternative == "greater" and case.margin in [4.5, 7.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py311:
        if case.alternative == "greater" and case.margin in [4.5, 7.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py310:
        if case.alternative == "greater" and case.margin in [4.5, 7.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py311:
        if case.alternative == "greater" and case.margin in [4.5, 7.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py310:
        if case.alternative == "greater" and case.margin in [4.5, 7.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py311:
        if case.alternative == "greater" and case.margin in [4.5, 7.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    assert (
        solve_size(
            null_mean=case.null_mean,
            mean=case.mean,
            diff=case.diff,
            margin=case.margin,
            std=case.std,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.power,
        )
        == case.size
    )


def test_solve_diff(case: TestCase, request: pytest.FixtureRequest) -> None:

    if request.config.is_linux and request.config.is_py310:
        if case in [
            TestCase(diff=15, margin=1.5, std=15, size=12, alternative="greater", alpha=0.025, power=0.8, actual_power=0.809784845),
        ]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py311:
        if case in [
            TestCase(diff=15, margin=1.5, std=15, size=12, alternative="greater", alpha=0.025, power=0.8, actual_power=0.809784845),
        ]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py310:
        if case in [
            TestCase(diff=15, margin=0.0, std=15, size=10, alternative="greater", alpha=0.025, power=0.8, actual_power=0.803096209),
            TestCase(diff=15, margin=1.5, std=15, size=12, alternative="greater", alpha=0.025, power=0.8, actual_power=0.809784845),
        ]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py311:
        if case in [
            TestCase(diff=15, margin=1.5, std=15, size=12, alternative="greater", alpha=0.025, power=0.8, actual_power=0.809784845),
        ]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py311:
        if case in [
            TestCase(diff=15, margin=1.5, std=15, size=12, alternative="greater", alpha=0.025, power=0.8, actual_power=0.809784845),
        ]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    assert (
        round(
            solve_diff(
                margin=case.margin,
                std=case.std,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
            ),
            1,
        )
        == case.diff
    )


def test_solve_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if request.config.is_linux and request.config.is_py310:
        if case.alternative == "greater" and case.margin in [1.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py311:
        if case.alternative == "greater" and case.margin in [1.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py310:
        if case.alternative == "greater" and case.margin in [1.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py311:
        if case.alternative == "greater" and case.margin in [1.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py311:
        if case.alternative == "greater" and case.margin in [1.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    assert round(
        solve_mean(
            null_mean=case.null_mean,
            margin=case.margin,
            std=case.std,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.actual_power,
        ),
        2,
    ) == round(case.mean, 2)


def test_solve_null_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if request.config.is_linux and request.config.is_py310:
        if case.alternative == "greater" and case.margin in [1.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_linux and request.config.is_py311:
        if case.alternative == "greater" and case.margin in [1.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py310:
        if case.alternative == "greater" and case.margin in [1.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_macos and request.config.is_py311:
        if case.alternative == "greater" and case.margin in [1.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if request.config.is_windows and request.config.is_py311:
        if case.alternative == "greater" and case.margin in [1.5]:
            request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    assert round(
        solve_null_mean(
            mean=case.mean,
            margin=case.margin,
            std=case.std,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.actual_power,
        ),
        2,
    ) == round(case.null_mean, 2)


def test_solve_std(case: TestCase) -> None:
    assert (
        round(
            solve_std(
                null_mean=case.null_mean,
                mean=case.mean,
                diff=case.diff,
                margin=case.margin,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
            ),
            0,
        )
        == case.std
    )


def test_solve_margin(case: TestCase, request: pytest.FixtureRequest) -> None:

    assert (
        round(
            solve_margin(
                null_mean=case.null_mean,
                mean=case.mean,
                diff=case.diff,
                std=case.std,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
            ),
            1,
        )
        == case.margin
    )
