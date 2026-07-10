# Validation Software: PASS 2025
# Module: One-Sample Z-Tests
#         One-Sample T-Tests

from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.mean.single.inequality import _ParamsValidator
from pystatpower.mean.single.inequality import solve_power, solve_size, solve_mean, solve_null_mean, solve_diff, solve_std

from tests.models import BaseTestCase

pytestmark = pytest.mark.filterwarnings("ignore")


def test_validate() -> None:
    # validate parameter combinations against diff
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=None, diff=None).validate(target="diff")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=4, null_mean=None, diff=None).validate(target="diff")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=2, diff=None).validate(target="diff")

    with pytest.warns(UserWarning):
        _ParamsValidator(mean=4, null_mean=None, diff=2).validate(target="diff")
    with pytest.warns(UserWarning):
        _ParamsValidator(mean=None, null_mean=2, diff=2).validate(target="diff")
    with pytest.warns(UserWarning):
        _ParamsValidator(mean=4, null_mean=2, diff=2).validate(target="diff")


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
        pv = _ParamsValidator(mean=self.mean, null_mean=self.null_mean, diff=self.diff)
        pv.validate("diff", warning=False)

        self.diff = pv.diff


case_group_z = (
    [
        # mean = 30 to 40 by 1, null_mean = 20, std = 20, alpha = 0.05, power = 0.80, alternative = "two-sided", dist = "z"
        TestCase(mean=mean, null_mean=null_mean, std=20, size=size, alternative="two-sided", alpha=0.05, power=0.80, actual_power=actual_power, dist="z")
        for mean, null_mean, size, actual_power in [
            (30, 20, 32, 0.807430419417483),
            (31, 20, 26, 0.800805007022753),
            (32, 20, 22, 0.803527484441174),
            (33, 20, 19, 0.808756568937454),
            (34, 20, 17, 0.822832188980162),
            (35, 20, 14, 0.801302394090672),
            (36, 20, 13, 0.822381633767393),
            (37, 20, 11, 0.804876711001331),
            (38, 20, 10, 0.812215152209930),
            (39, 20, 9, 0.813277480918628),
            (40, 20, 8, 0.807430419417483),
        ]
    ]
    + [
        # mean = 30 to 40 by 1, null_mean = 20, std = 20, alpha = 0.05, power = 0.80, alternative = "greater", dist = "z"
        TestCase(mean=mean, null_mean=null_mean, std=20, size=size, alternative="greater", alpha=0.05, power=0.80, actual_power=actual_power, dist="z")
        for mean, null_mean, size, actual_power in [
            (30, 20, 25, 0.803764940006850),
            (31, 20, 21, 0.809366177809150),
            (32, 20, 18, 0.816134261890907),
            (33, 20, 15, 0.808555489717706),
            (34, 20, 13, 0.810308109302267),
            (35, 20, 11, 0.800278090826271),
            (36, 20, 10, 0.811913189862654),
            (37, 20, 9, 0.817306076181989),
            (38, 20, 8, 0.816134261890907),
            (39, 20, 7, 0.807469790941388),
            (40, 20, 7, 0.841561861841659),
        ]
    ]
    + [
        # mean = 20, null_mean = 30 to 40 by 1, std = 20, alpha = 0.05, power = 0.80, alternative = "less", dist = "z"
        TestCase(mean=mean, null_mean=null_mean, std=20, size=size, alternative="less", alpha=0.05, power=0.80, actual_power=actual_power, dist="z")
        for mean, null_mean, size, actual_power in [
            (20, 30, 25, 0.803764940006850),
            (20, 31, 21, 0.809366177809151),
            (20, 32, 18, 0.816134261890908),
            (20, 33, 15, 0.808555489717707),
            (20, 34, 13, 0.810308109302268),
            (20, 35, 11, 0.800278090826272),
            (20, 36, 10, 0.811913189862655),
            (20, 37, 9, 0.817306076181989),
            (20, 38, 8, 0.816134261890908),
            (20, 39, 7, 0.807469790941389),
            (20, 40, 7, 0.841561861841660),
        ]
    ]
)


case_group_t = (
    [
        # mean = 30 to 40 by 1, null_mean = 20, std = 20, alpha = 0.05, power = 0.80, alternative = "two-sided", dist = "t"
        TestCase(mean=mean, null_mean=null_mean, std=20, size=size, alternative="two-sided", alpha=0.05, power=0.80, actual_power=actual_power, dist="t")
        for mean, null_mean, size, actual_power in [
            (30, 20, 34, 0.807777501325314),
            (31, 20, 28, 0.801083123950921),
            (32, 20, 24, 0.803671385610932),
            (33, 20, 21, 0.808704629589225),
            (34, 20, 19, 0.822547260268955),
            (35, 20, 16, 0.800556427304272),
            (36, 20, 15, 0.821310538783487),
            (37, 20, 13, 0.803064268543370),
            (38, 20, 12, 0.809785486318828),
            (39, 20, 11, 0.810039888299143),
            (40, 20, 10, 0.803096856658027),
        ]
    ]
    + [
        # mean = 30 to 40 by 1, null_mean = 20, std = 20, alpha = 0.05, power = 0.80, alternative = "greater", dist = "t"
        TestCase(mean=mean, null_mean=null_mean, std=20, size=size, alternative="greater", alpha=0.05, power=0.80, actual_power=actual_power, dist="t")
        for mean, null_mean, size, actual_power in [
            (30, 20, 27, 0.811831551748864),
            (31, 20, 22, 0.802436511114216),
            (32, 20, 19, 0.807909057442467),
            (33, 20, 17, 0.821004446753246),
            (34, 20, 15, 0.824257058512522),
            (35, 20, 13, 0.816529422328019),
            (36, 20, 12, 0.828980864043299),
            (37, 20, 11, 0.835532773963513),
            (38, 20, 10, 0.836015932397386),
            (39, 20, 9, 0.829699925077854),
            (40, 20, 8, 0.815019441564732),
        ]
    ]
    + [
        # mean = 20, null_mean = 30 to 40 by 1, std = 20, alpha = 0.05, power = 0.80, alternative = "less", dist = "t"
        TestCase(mean=mean, null_mean=null_mean, std=20, size=size, alternative="less", alpha=0.05, power=0.80, actual_power=actual_power, dist="t")
        for mean, null_mean, size, actual_power in [
            (20, 30, 27, 0.811831551748864),
            (20, 31, 22, 0.802436511114216),
            (20, 32, 19, 0.807909057442467),
            (20, 33, 17, 0.821004446753246),
            (20, 34, 15, 0.824257058512522),
            (20, 35, 13, 0.816529422328019),
            (20, 36, 12, 0.828980864043299),
            (20, 37, 11, 0.835532773963513),
            (20, 38, 10, 0.836015932397386),
            (20, 39, 9, 0.829699925077854),
            (20, 40, 8, 0.815019441564732),
        ]
    ]
)

case_group = case_group_z + case_group_t


def test_solve_power(case: TestCase) -> None:

    assert round(
        solve_power(
            null_mean=case.null_mean,
            mean=case.mean,
            std=case.std,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            dist=case.dist,
        ),
        6,
    ) == round(case.actual_power, 6)


def test_solve_size(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if case.mean in (30, 34, 40) and case.alternative == "greater" and case.dist == "t":
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


def test_solve_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if case.mean in (30, 33) and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    case.direction = "greater" if case.mean > case.null_mean else "less"
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
                direction=case.direction,
            ),
            0,
        )
        == case.mean
    )


def test_solve_mean_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_mean(null_mean=20, std=20, size=17, alternative="two-sided", alpha=0.05, power=0.8, dist="t")


def test_solve_null_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if case.mean in (33,) and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    case.direction = "greater" if case.null_mean > case.mean else "less"
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
                direction=case.direction,
            ),
            0,
        )
        == case.null_mean
    )


def test_solve_null_mean_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_null_mean(mean=20, std=20, size=17, alternative="two-sided", alpha=0.05, power=0.8, dist="t")


def test_solve_diff(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.mean in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40) and case.alternative == "two-sided" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if case.mean in (30, 33) and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    direction = "greater" if case.mean > case.null_mean else "less"
    assert (
        round(
            solve_diff(
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
        == case.diff
    )


def test_solve_diff_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_diff(std=20, size=17, alternative="two-sided", alpha=0.05, power=0.8, dist="t")


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
