# Validation Software: PASS 2025
# Module: One-Sample Z-Tests for Non-Inferiority
#         One-Sample T-Tests for Non-Inferiority

from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.mean.single.noninferiority import _ParamsValidator
from pystatpower.mean.single.noninferiority import solve_power, solve_size, solve_mean, solve_null_mean, solve_margin, solve_diff, solve_noninferiority_mean, solve_offset, solve_std

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

    # validate parameter combinations against noninferiority_mean
    with pytest.raises(ValueError):
        _ParamsValidator(null_mean=None, margin=None, noninferiority_mean=None).validate("noninferiority_mean")
    with pytest.raises(ValueError):
        _ParamsValidator(null_mean=10, margin=None, noninferiority_mean=None).validate("noninferiority_mean")
    with pytest.raises(ValueError):
        _ParamsValidator(null_mean=None, margin=-5, noninferiority_mean=None).validate("noninferiority_mean")

    with pytest.warns(UserWarning):
        _ParamsValidator(null_mean=10, margin=None, noninferiority_mean=5).validate("noninferiority_mean")
    with pytest.warns(UserWarning):
        _ParamsValidator(null_mean=None, margin=-5, noninferiority_mean=5).validate("noninferiority_mean")
    with pytest.warns(UserWarning):
        _ParamsValidator(null_mean=10, margin=-5, noninferiority_mean=5).validate("noninferiority_mean")

    # validate parameter combinations against offset
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=None, margin=None, diff=None, noninferiority_mean=None, offset=None).validate(target="offset")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=12, null_mean=None, margin=None, diff=None, noninferiority_mean=None, offset=None).validate(target="offset")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=10, margin=None, diff=None, noninferiority_mean=None, offset=None).validate(target="offset")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=None, margin=-5, diff=None, noninferiority_mean=None, offset=None).validate(target="offset")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=None, margin=None, diff=2, noninferiority_mean=None, offset=None).validate(target="offset")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=None, margin=None, diff=None, noninferiority_mean=5, offset=None).validate(target="offset")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=12, null_mean=10, margin=None, diff=None, noninferiority_mean=None, offset=None).validate(target="offset")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=10, margin=-5, diff=None, noninferiority_mean=None, offset=None).validate(target="offset")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=12, null_mean=None, margin=-5, diff=None, noninferiority_mean=None, offset=None).validate(target="offset")

    with pytest.warns(UserWarning):
        _ParamsValidator(mean=None, null_mean=None, margin=-5, diff=2, noninferiority_mean=None, offset=7).validate(target="offset")
    with pytest.warns(UserWarning):
        _ParamsValidator(mean=12, null_mean=None, margin=None, diff=None, noninferiority_mean=5, offset=7).validate(target="offset")
    with pytest.warns(UserWarning):
        _ParamsValidator(mean=12, null_mean=10, margin=-5, diff=None, noninferiority_mean=None, offset=7).validate(target="offset")
    with pytest.warns(UserWarning):
        _ParamsValidator(mean=None, null_mean=None, margin=-5, diff=2, noninferiority_mean=5, offset=None).validate(target="offset")
    with pytest.warns(UserWarning):
        _ParamsValidator(mean=12, null_mean=10, margin=None, diff=None, noninferiority_mean=5, offset=None).validate(target="offset")

    _ParamsValidator(mean=12, null_mean=10, margin=-5, diff=None, noninferiority_mean=None, offset=None).validate(target="offset")


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    mean: float | None = None
    null_mean: float | None = None
    margin: float | None = None
    diff: float | None = None
    noninferiority_mean: float | None = None
    offset: float | None = None
    std: float
    size: int
    alternative: Literal["greater", "less"]
    alpha: float
    dist: Literal["z", "t"] = "t"
    power: float
    actual_power: float

    def __post_init__(self) -> None:
        self.margin = _ParamsValidator._margin(self.margin, self.alternative)

        pv = _ParamsValidator(mean=self.mean, null_mean=self.null_mean, margin=self.margin, diff=self.diff, noninferiority_mean=self.noninferiority_mean, offset=self.offset, alternative=self.alternative)
        pv.validate("diff", warning=False)
        pv.validate("noninferiority_mean", warning=False)
        pv.validate("offset", warning=False)

        self.diff = pv.diff
        self.noninferiority_mean = pv.noninferiority_mean
        self.offset = pv.offset


case_group_z = [
    # mean = 20,  null_mean = 18, margin = -18 to -3 by 0.5, std = 40, alpha = 0.025, power = 0.80, alternative = "greater", dist = "z"
    TestCase(mean=20, null_mean=18, margin=margin, std=40, size=size, alternative="greater", alpha=0.025, dist="z", power=0.80, actual_power=actual_power)
    for margin, size, actual_power in [
        (-18.0, 32, 0.807429578798747),
        (-17.5, 34, 0.811280559074981),
        (-17.0, 35, 0.802385798316682),
        (-16.5, 37, 0.803257313668525),
        (-16.0, 39, 0.802416704846465),
        (-15.5, 42, 0.809310990820384),
        (-15.0, 44, 0.804875830571654),
        (-14.5, 47, 0.807301064915486),
        (-14.0, 50, 0.807429578798748),
        (-13.5, 53, 0.805402622007928),
        (-13.0, 56, 0.801301455458812),
        (-12.5, 60, 0.801766796687869),
        (-12.0, 65, 0.805608424982718),
        (-11.5, 69, 0.800531596054328),
        (-11.0, 75, 0.803618830267023),
        (-10.5, 81, 0.803041670796890),
        (-10.0, 88, 0.803526582386345),
        (-9.5, 95, 0.800173015110702),
        (-9.0, 104, 0.800804060056704),
        (-8.5, 114, 0.800321191492937),
        (-8.0, 126, 0.801301455458812),
        (-7.5, 140, 0.802385798316682),
        (-7.0, 156, 0.802416704846465),
        (-6.5, 174, 0.800414728086098),
        (-6.0, 197, 0.801549753812365),
        (-5.5, 224, 0.801301455458812),
        (-5.0, 257, 0.801083976067046),
        (-4.5, 298, 0.801006255444267),
        (-4.0, 349, 0.800180816214511),
        (-3.5, 416, 0.800804060056704),
        (-3.0, 503, 0.800523806680340),
    ]
] + [
    # mean = 20,  null_mean = 22, margin = 3 to 18 by 0.5, std = 40, alpha = 0.025, power = 0.80, alternative = "less", dist = "z"
    TestCase(mean=20, null_mean=22, margin=margin, std=40, size=size, alternative="less", alpha=0.025, dist="z", power=0.80, actual_power=actual_power)
    for margin, size, actual_power in [
        (3.0, 503, 0.800523806680340),
        (3.5, 416, 0.800804060056704),
        (4.0, 349, 0.800180816214512),
        (4.5, 298, 0.801006255444267),
        (5.0, 257, 0.801083976067047),
        (5.5, 224, 0.801301455458812),
        (6.0, 197, 0.801549753812365),
        (6.5, 174, 0.800414728086098),
        (7.0, 156, 0.802416704846465),
        (7.5, 140, 0.802385798316683),
        (8.0, 126, 0.801301455458812),
        (8.5, 114, 0.800321191492937),
        (9.0, 104, 0.800804060056704),
        (9.5, 95, 0.800173015110702),
        (10.0, 88, 0.803526582386346),
        (10.5, 81, 0.803041670796890),
        (11.0, 75, 0.803618830267023),
        (11.5, 69, 0.800531596054328),
        (12.0, 65, 0.805608424982718),
        (12.5, 60, 0.801766796687869),
        (13.0, 56, 0.801301455458812),
        (13.5, 53, 0.805402622007929),
        (14.0, 50, 0.807429578798748),
        (14.5, 47, 0.807301064915486),
        (15.0, 44, 0.804875830571654),
        (15.5, 42, 0.809310990820385),
        (16.0, 39, 0.802416704846465),
        (16.5, 37, 0.803257313668525),
        (17.0, 35, 0.802385798316683),
        (17.5, 34, 0.811280559074982),
        (18.0, 32, 0.807429578798748),
    ]
]


case_group_t = [
    # mean = 20,  null_mean = 18, margin = -18 to -3 by 0.5, std = 40, alpha = 0.025, power = 0.80, alternative = "greater", dist = "t"
    TestCase(mean=20, null_mean=18, margin=margin, std=40, size=size, alternative="greater", alpha=0.025, dist="t", power=0.80, actual_power=actual_power)
    for margin, size, actual_power in [
        (-18.0, 34, 0.807776685543458),
        (-17.5, 35, 0.800053415357762),
        (-17.0, 37, 0.802755284947258),
        (-16.5, 39, 0.803630625012321),
        (-16.0, 41, 0.802793253337018),
        (-15.5, 43, 0.800318375321791),
        (-15.0, 46, 0.805246964828903),
        (-14.5, 49, 0.807664762496591),
        (-14.0, 52, 0.807786981876298),
        (-13.5, 55, 0.805754911453643),
        (-13.0, 58, 0.801649745808345),
        (-12.5, 62, 0.802103846807924),
        (-12.0, 67, 0.805928875992880),
        (-11.5, 71, 0.800845356552311),
        (-11.0, 77, 0.803915153395315),
        (-10.5, 83, 0.803324143346699),
        (-10.0, 90, 0.803793402006325),
        (-9.5, 97, 0.800427634167440),
        (-9.0, 106, 0.801041954704910),
        (-8.5, 116, 0.800543202426292),
        (-8.0, 128, 0.801506202603035),
        (-7.5, 142, 0.802573336713322),
        (-7.0, 157, 0.800072943709877),
        (-6.5, 176, 0.800571440584003),
        (-6.0, 199, 0.801690092470930),
        (-5.5, 226, 0.801426727506516),
        (-5.0, 259, 0.801194673157606),
        (-4.5, 300, 0.801102919330952),
        (-4.0, 351, 0.800264407800567),
        (-3.5, 418, 0.800874842237122),
        (-3.0, 505, 0.800582923601105),
    ]
] + [
    # mean = 20,  null_mean = 22, margin = 3 to 18 by 0.5, std = 40, alpha = 0.025, power = 0.80, alternative = "less", dist = "t"
    TestCase(mean=20, null_mean=22, margin=margin, std=40, size=size, alternative="less", alpha=0.025, dist="t", power=0.80, actual_power=actual_power)
    for margin, size, actual_power in [
        (3.0, 505, 0.800582923601105),
        (3.5, 418, 0.800874842237122),
        (4.0, 351, 0.800264407800567),
        (4.5, 300, 0.801102919330952),
        (5.0, 259, 0.801194673157606),
        (5.5, 226, 0.801426727506516),
        (6.0, 199, 0.801690092470930),
        (6.5, 176, 0.800571440584003),
        (7.0, 157, 0.800072943709877),
        (7.5, 142, 0.802573336713322),
        (8.0, 128, 0.801506202603035),
        (8.5, 116, 0.800543202426292),
        (9.0, 106, 0.801041954704910),
        (9.5, 97, 0.800427634167440),
        (10.0, 90, 0.803793402006325),
        (10.5, 83, 0.803324143346699),
        (11.0, 77, 0.803915153395315),
        (11.5, 71, 0.800845356552311),
        (12.0, 67, 0.805928875992880),
        (12.5, 62, 0.802103846807924),
        (13.0, 58, 0.801649745808345),
        (13.5, 55, 0.805754911453643),
        (14.0, 52, 0.807786981876298),
        (14.5, 49, 0.807664762496591),
        (15.0, 46, 0.805246964828903),
        (15.5, 43, 0.800318375321791),
        (16.0, 41, 0.802793253337018),
        (16.5, 39, 0.803630625012321),
        (17.0, 37, 0.802755284947258),
        (17.5, 35, 0.800053415357762),
        (18.0, 34, 0.807776685543458),
    ]
]

case_group = case_group_z + case_group_t


def test_solve_power(case: TestCase) -> None:

    assert round(
        solve_power(
            mean=case.mean,
            null_mean=case.null_mean,
            margin=case.margin,
            diff=case.diff,
            noninferiority_mean=case.noninferiority_mean,
            offset=case.offset,
            std=case.std,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            dist=case.dist,
        ),
        6,
    ) == round(case.actual_power, 6)


def test_solve_size(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.margin in [-18.0, -12.0, -8.0, -5.0, -3.0] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    assert (
        solve_size(
            mean=case.mean,
            null_mean=case.null_mean,
            margin=case.margin,
            diff=case.diff,
            noninferiority_mean=case.noninferiority_mean,
            offset=case.offset,
            std=case.std,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.power,
            dist=case.dist,
        )
        == case.size
    )


def test_solve_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.margin in [-12.5, -5.0] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    assert round(
        solve_mean(
            null_mean=case.null_mean,
            margin=case.margin,
            noninferiority_mean=case.noninferiority_mean,
            std=case.std,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.actual_power,
            dist=case.dist,
        ),
        2,
    ) == round(case.mean, 2)


def test_solve_null_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.margin in [-12.5, -5.0] and case.alternative == "greater" and case.dist == "t":
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
            dist=case.dist,
        ),
        2,
    ) == round(case.null_mean, 2)


def test_solve_margin(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.margin in [-12.5, -5.0] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    assert (
        round(
            solve_margin(
                mean=case.mean,
                null_mean=case.null_mean,
                diff=case.diff,
                std=case.std,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
            ),
            1,
        )
        == case.margin
    )


def test_solve_diff(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.margin in [-9.5, -9.0, -3.5] and case.alternative == "greater" and case.dist == "t":
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
                dist=case.dist,
            ),
            1,
        )
        == case.diff
    )


def test_solve_noninferiority_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.margin in [-12.0, -11.5] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    assert round(
        solve_noninferiority_mean(
            mean=case.mean,
            std=case.std,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.actual_power,
            dist=case.dist,
        ),
        2,
    ) == round(case.noninferiority_mean, 2)


def test_solve_offset(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.margin in [-15.5, -7.5] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if case.margin in [3.0, 3.5, 4.0, 4.5, 6.5, 8.5, 9.5, 10.5, 11.0, 11.5, 13.0, 14.0, 14.5, 15.0, 16.0, 18.0] and case.alternative == "less" and case.dist == "t":
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    assert round(
        solve_offset(
            std=case.std,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.actual_power,
            dist=case.dist,
        ),
        2,
    ) == round(case.offset, 2)


def test_solve_std(case: TestCase) -> None:
    assert (
        round(
            solve_std(
                mean=case.mean,
                null_mean=case.null_mean,
                margin=case.margin,
                diff=case.diff,
                noninferiority_mean=case.noninferiority_mean,
                offset=case.offset,
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
