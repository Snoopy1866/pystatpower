# Validation Software: PASS 15
# Module: Superiority by a Margin Tests for One Mean (One-Sample or Paired T-Test)

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.mean.single.superiority import solve_power, solve_size, solve_diff, solve_null_mean, solve_mean, solve_std, solve_margin


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
    # diff = 15, std = 15, margin = 0 to 10 by 0.5, alpha = 0.025, power = 0.80, alternative = "greater"
    TestCase(null_mean=None, mean=None, diff=15, margin=margin, std=15, size=size, alternative="greater", alpha=0.025, power=0.80, actual_power=actual_power)
    for margin, size, actual_power in [
        (0.0, 10, 0.803096209),
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
        (0.0, 16, 0.800555580),
    ]
]


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


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


def test_solve_power_not_specify_diff() -> None:
    assert (
        round(
            solve_power(
                null_mean=20,
                mean=35,
                diff=None,
                margin=0.5,
                std=15,
                size=11,
                alternative="greater",
                alpha=0.025,
            ),
            9,
        )
        == 0.823125590
    )


def test_solve_power_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_power(null_mean=None, mean=10, diff=None, margin=2, std=5, size=20, alternative="greater", alpha=0.025)

    with pytest.raises(ValueError):
        solve_power(null_mean=10, mean=None, diff=None, margin=2, std=5, size=20, alternative="greater", alpha=0.025)

    with pytest.raises(ValueError):
        solve_power(null_mean=None, mean=None, diff=None, margin=2, std=5, size=20, alternative="greater", alpha=0.025)


def test_solve_size(case: TestCase) -> None:
    if case in [
        TestCase(null_mean=None, mean=None, diff=15, margin=7.5, std=15, size=34, alternative="greater", alpha=0.025, power=0.80, actual_power=0.807776686),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    # if (
    #     case
    #     in [
    #         TestCase(null_mean=None, mean=None, diff=0, margin=-10.0, std=10, size=10, alternative="greater", alpha=0.025, power=0.80, actual_power=0.803096209),
    #     ]
    #     and sys.platform == "darwin"
    # ):
    #     pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

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
            mean=35,
            diff=None,
            margin=0.5,
            std=15,
            alternative="greater",
            alpha=0.025,
            power=0.80,
        )
        == 11
    )


def test_solve_size_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_size(null_mean=None, mean=10, diff=None, margin=2, std=5, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_size(null_mean=10, mean=None, diff=None, margin=2, std=5, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_size(null_mean=None, mean=None, diff=None, margin=2, std=5, alternative="greater", alpha=0.025, power=0.8)


def test_solve_diff(case: TestCase) -> None:
    if case in [
        TestCase(null_mean=None, mean=None, diff=15, margin=1.5, std=15, size=12, alternative="greater", alpha=0.025, power=0.80, actual_power=0.809784845),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

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
        TestCase(null_mean=None, mean=None, diff=15, margin=9.5, std=15, size=61, alternative="greater", alpha=0.025, power=0.80, actual_power=0.804464986),
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
        TestCase(null_mean=None, mean=None, diff=15, margin=9.5, std=15, size=61, alternative="greater", alpha=0.025, power=0.80, actual_power=0.804464986),
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
                mean=35,
                diff=None,
                margin=0.5,
                size=11,
                alternative="greater",
                alpha=0.025,
                power=0.823125590,
            ),
            0,
        )
        == 15
    )


def test_solve_std_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_std(null_mean=None, mean=10, diff=None, margin=2, size=20, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_std(null_mean=10, mean=None, diff=None, margin=2, size=20, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_std(null_mean=None, mean=None, diff=None, margin=2, size=20, alternative="greater", alpha=0.025, power=0.8)


def test_solve_margin(case: TestCase) -> None:
    if case in [
        TestCase(null_mean=None, mean=None, diff=15, margin=9.5, std=15, size=61, alternative="greater", alpha=0.025, power=0.80, actual_power=0.804464986),
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
                mean=35,
                diff=None,
                std=15,
                size=11,
                alternative="greater",
                alpha=0.025,
                power=0.823125590,
            ),
            1,
        )
        == 0.5
    )


def test_solve_margin_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_margin(null_mean=None, mean=10, diff=None, std=5, size=20, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_margin(null_mean=10, mean=None, diff=None, std=5, size=20, alternative="greater", alpha=0.025, power=0.8)

    with pytest.raises(ValueError):
        solve_margin(null_mean=None, mean=None, diff=None, std=5, size=20, alternative="greater", alpha=0.025, power=0.8)
