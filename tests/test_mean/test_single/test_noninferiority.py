# Validation Software: PASS 15
# Module: Non-Inferiority Tests for One Mean

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.mean.single.noninferiority import solve_power, solve_size, solve_diff, solve_null_mean, solve_mean, solve_std, solve_margin


@dataclass
class TestCase:
    __test__ = False

    null_mean: float | None
    mean: float | None
    diff: float | None
    margin: float
    std: float
    size: int
    alternative: Literal["greater", "less"]
    alpha: float
    power: float
    actual_power: float


case_group = [
    # diff = 0, std = 10, margin = -10 to -0.5 by 0.5, alpha = 0.025, power = 0.80, alternative = "greater"
    TestCase(null_mean=None, mean=None, diff=0, margin=margin, std=10, size=size, alternative="greater", alpha=0.025, power=0.80, actual_power=actual_power)
    for margin, size, actual_power in [
        (-10.0, 10, 0.803096209),
        (-9.5, 11, 0.810039281),
        (-9.0, 12, 0.809784845),
        (-8.5, 13, 0.803063513),
        (-8.0, 15, 0.821309977),
        (-7.5, 16, 0.800555580),
        (-7.0, 19, 0.822546679),
        (-6.5, 21, 0.808703861),
        (-6.0, 24, 0.803670529),
        (-5.5, 28, 0.801082214),
        (-5.0, 34, 0.807776686),
        (-4.5, 41, 0.802793253),
        (-4.0, 52, 0.807786982),
        (-3.5, 67, 0.805928876),
        (-3.0, 90, 0.803793402),
        (-2.5, 128, 0.801506203),
        (-2.0, 199, 0.801690092),
        (-1.5, 351, 0.800264408),
        (-1.0, 786, 0.800441366),
        (-0.5, 3140, 0.800027594),
    ]
] + [
    # diff = -2, std = 15, margin = 0.5 to 10 by 0.5, alpha = 0.025, power = 0.80, alternative = "less"
    TestCase(null_mean=None, mean=None, diff=-2, margin=margin, std=15, size=size, alternative="less", alpha=0.025, power=0.80, actual_power=actual_power)
    for margin, size, actual_power in [
        (0.5, 285, 0.800711788),
        (1.0, 199, 0.801690092),
        (1.5, 147, 0.802447785),
        (2.0, 113, 0.802436332),
        (2.5, 90, 0.803793402),
        (3.0, 73, 0.802298026),
        (3.5, 61, 0.804464986),
        (4.0, 52, 0.807786982),
        (4.5, 44, 0.802257042),
        (5.0, 39, 0.810570919),
        (5.5, 34, 0.807776686),
        (6.0, 30, 0.806009921),
        (6.5, 27, 0.809008881),
        (7.0, 24, 0.803670529),
        (7.5, 22, 0.808524347),
        (8.0, 20, 0.807290896),
        (8.5, 19, 0.822546679),
        (9.0, 17, 0.810070484),
        (9.5, 16, 0.817438156),
        (10.0, 15, 0.821309977),
    ]
]


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_solve_power(case: TestCase) -> None:
    if case in [
        TestCase(null_mean=None, mean=None, diff=0, margin=-1.0, std=10, size=786, alternative="greater", alpha=0.025, power=0.80, actual_power=0.800441366),
        TestCase(null_mean=None, mean=None, diff=0, margin=-0.5, std=10, size=3140, alternative="greater", alpha=0.025, power=0.80, actual_power=0.800027594),
    ]:
        pytest.skip(reason="There may be issues with the PASS calculation results, so the test is temporarily skipped")

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


def test_solve_power_not_specify_diff() -> None:
    assert (
        round(
            solve_power(
                null_mean=20,
                mean=20,
                diff=None,
                margin=-10.0,
                std=10,
                size=10,
                alternative="greater",
                alpha=0.025,
            ),
            9,
        )
        == 0.803096209
    )


def test_solve_power_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_power(null_mean=None, mean=10, diff=None, margin=-2, std=5, size=20, alternative="greater", alpha=0.025)

    with pytest.raises(ValueError):
        solve_power(null_mean=10, mean=None, diff=None, margin=-2, std=5, size=20, alternative="greater", alpha=0.025)

    with pytest.raises(ValueError):
        solve_power(null_mean=None, mean=None, diff=None, margin=-2, std=5, size=20, alternative="greater", alpha=0.025)


def test_solve_size(case: TestCase) -> None:
    if case in [
        TestCase(null_mean=None, mean=None, diff=0, margin=-5.0, std=10, size=34, alternative="greater", alpha=0.025, power=0.80, actual_power=0.807776686),
        TestCase(null_mean=None, mean=None, diff=0, margin=-3.5, std=10, size=67, alternative="greater", alpha=0.025, power=0.80, actual_power=0.805928876),
        TestCase(null_mean=None, mean=None, diff=0, margin=-2.5, std=10, size=128, alternative="greater", alpha=0.025, power=0.80, actual_power=0.801506203),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    if case in [
        TestCase(null_mean=None, mean=None, diff=0, margin=-1.0, std=10, size=786, alternative="greater", alpha=0.025, power=0.80, actual_power=0.800441366),
        TestCase(null_mean=None, mean=None, diff=0, margin=-0.5, std=10, size=3140, alternative="greater", alpha=0.025, power=0.80, actual_power=0.800027594),
    ]:
        pytest.skip(reason="There may be issues with the PASS calculation results, so the test is temporarily skipped")
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


def test_solve_size_not_specify_diff() -> None:
    assert (
        solve_size(
            null_mean=20,
            mean=20,
            diff=None,
            margin=-10.0,
            std=10,
            alternative="greater",
            alpha=0.025,
            power=0.80,
        )
        == 10
    )


def test_solve_size_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_size(null_mean=None, mean=10, diff=None, margin=-2, std=5, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_size(null_mean=10, mean=None, diff=None, margin=-2, std=5, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_size(null_mean=None, mean=None, diff=None, margin=-2, std=5, alternative="greater", alpha=0.025, power=0.8)


def test_solve_diff(case: TestCase) -> None:
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


def test_solve_null_mean(case: TestCase) -> None:

    if case.mean is None and case.null_mean is None and case.diff is not None:
        null_mean = case.size
        mean = case.diff + null_mean

    if case in [
        TestCase(null_mean=None, mean=None, diff=0, margin=-6.0, std=10, size=24, alternative="greater", alpha=0.025, power=0.80, actual_power=0.803670529),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    assert round(
        solve_null_mean(
            mean=mean,
            margin=case.margin,
            std=case.std,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.actual_power,
        ),
        2,
    ) == round(null_mean, 2)


def test_solve_mean(case: TestCase) -> None:

    if case.mean is None and case.null_mean is None and case.diff is not None:
        null_mean = case.size
        mean = case.diff + null_mean

    if case in [
        TestCase(null_mean=None, mean=None, diff=0, margin=-6.0, std=10, size=24, alternative="greater", alpha=0.025, power=0.80, actual_power=0.803670529),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    assert round(
        solve_mean(
            null_mean=null_mean,
            margin=case.margin,
            std=case.std,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.actual_power,
        ),
        2,
    ) == round(mean, 2)


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


def test_solve_std_not_specify_diff() -> None:
    assert (
        round(
            solve_std(
                null_mean=20,
                mean=20,
                diff=None,
                margin=-10.0,
                size=10,
                alternative="greater",
                alpha=0.025,
                power=0.803096209,
            ),
            0,
        )
        == 10
    )


def test_solve_std_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_std(null_mean=None, mean=10, diff=None, margin=-2, size=20, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_std(null_mean=10, mean=None, diff=None, margin=-2, size=20, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_std(null_mean=None, mean=None, diff=None, margin=-2, size=20, alternative="greater", alpha=0.025, power=0.8)


def test_solve_margin(case: TestCase) -> None:
    if case in [
        TestCase(null_mean=None, mean=None, diff=0, margin=-7.0, std=10, size=19, alternative="greater", alpha=0.025, power=0.80, actual_power=0.822546679),
        TestCase(null_mean=None, mean=None, diff=0, margin=-6.0, std=10, size=24, alternative="greater", alpha=0.025, power=0.80, actual_power=0.803670529),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

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


def test_solve_margin_not_specify_diff() -> None:
    assert (
        round(
            solve_margin(
                null_mean=20,
                mean=20,
                diff=None,
                std=10,
                size=10,
                alternative="greater",
                alpha=0.025,
                power=0.803096209,
            ),
            0,
        )
        == -10.0
    )


def test_solve_margin_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_margin(null_mean=None, mean=10, diff=None, std=5, size=20, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_margin(null_mean=10, mean=None, diff=None, std=5, size=20, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_margin(null_mean=None, mean=None, diff=None, std=5, size=20, alternative="greater", alpha=0.025, power=0.8)
