# Validation Software: PASS 2025
# Module: One-Sample Z-Tests for Superiority by a Margin
#         One-Sample T-Tests for Superiority by a Margin


from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.mean.single.superiority import _margin
from pystatpower.mean.single.superiority import _ParamsValidator
from pystatpower.mean.single.superiority import solve_diff
from pystatpower.mean.single.superiority import solve_margin
from pystatpower.mean.single.superiority import solve_mean
from pystatpower.mean.single.superiority import solve_null_mean
from pystatpower.mean.single.superiority import solve_offset
from pystatpower.mean.single.superiority import solve_power
from pystatpower.mean.single.superiority import solve_size
from pystatpower.mean.single.superiority import solve_std
from pystatpower.mean.single.superiority import solve_superiority_mean
from tests.models import BaseTestCase

pytestmark = pytest.mark.filterwarnings("ignore")


def test_margin() -> None:
    assert _margin(5, alternative="greater") == 5
    assert _margin(-5, alternative="greater") == 5
    assert _margin(5, alternative="less") == -5
    assert _margin(-5, alternative="less") == -5


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

    # validate parameter combinations against superiority_mean
    with pytest.raises(ValueError):
        _ParamsValidator(null_mean=None, margin=None, superiority_mean=None).validate("superiority_mean")
    with pytest.raises(ValueError):
        _ParamsValidator(null_mean=10, margin=None, superiority_mean=None).validate("superiority_mean")
    with pytest.raises(ValueError):
        _ParamsValidator(null_mean=None, margin=-5, superiority_mean=None).validate("superiority_mean")

    with pytest.warns(UserWarning):
        _ParamsValidator(null_mean=10, margin=None, superiority_mean=5).validate("superiority_mean")
    with pytest.warns(UserWarning):
        _ParamsValidator(null_mean=None, margin=-5, superiority_mean=5).validate("superiority_mean")
    with pytest.warns(UserWarning):
        _ParamsValidator(null_mean=10, margin=-5, superiority_mean=5).validate("superiority_mean")

    # validate parameter combinations against offset
    with pytest.raises(ValueError):
        _ParamsValidator(
            mean=None, null_mean=None, margin=None, diff=None, superiority_mean=None, offset=None
        ).validate(target="offset")
    with pytest.raises(ValueError):
        _ParamsValidator(mean=12, null_mean=None, margin=None, diff=None, superiority_mean=None, offset=None).validate(
            target="offset"
        )
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=10, margin=None, diff=None, superiority_mean=None, offset=None).validate(
            target="offset"
        )
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=None, margin=-5, diff=None, superiority_mean=None, offset=None).validate(
            target="offset"
        )
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=None, margin=None, diff=2, superiority_mean=None, offset=None).validate(
            target="offset"
        )
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=None, margin=None, diff=None, superiority_mean=5, offset=None).validate(
            target="offset"
        )
    with pytest.raises(ValueError):
        _ParamsValidator(mean=12, null_mean=10, margin=None, diff=None, superiority_mean=None, offset=None).validate(
            target="offset"
        )
    with pytest.raises(ValueError):
        _ParamsValidator(mean=None, null_mean=10, margin=-5, diff=None, superiority_mean=None, offset=None).validate(
            target="offset"
        )
    with pytest.raises(ValueError):
        _ParamsValidator(mean=12, null_mean=None, margin=-5, diff=None, superiority_mean=None, offset=None).validate(
            target="offset"
        )

    with pytest.warns(UserWarning):
        _ParamsValidator(mean=None, null_mean=None, margin=-5, diff=2, superiority_mean=None, offset=7).validate(
            target="offset"
        )
    with pytest.warns(UserWarning):
        _ParamsValidator(mean=12, null_mean=None, margin=None, diff=None, superiority_mean=5, offset=7).validate(
            target="offset"
        )
    with pytest.warns(UserWarning):
        _ParamsValidator(mean=12, null_mean=10, margin=-5, diff=None, superiority_mean=None, offset=7).validate(
            target="offset"
        )
    with pytest.warns(UserWarning):
        _ParamsValidator(mean=None, null_mean=None, margin=-5, diff=2, superiority_mean=5, offset=None).validate(
            target="offset"
        )
    with pytest.warns(UserWarning):
        _ParamsValidator(mean=12, null_mean=10, margin=None, diff=None, superiority_mean=5, offset=None).validate(
            target="offset"
        )

    _ParamsValidator(mean=12, null_mean=10, margin=-5, diff=None, superiority_mean=None, offset=None).validate(
        target="offset"
    )


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    mean: float | None = None
    null_mean: float | None = None
    margin: float | None = None
    diff: float | None = None
    superiority_mean: float | None = None
    offset: float | None = None
    std: float
    size: int
    alternative: Literal["greater", "less"]
    alpha: float
    dist: Literal["z", "t"] = "t"
    power: float
    actual_power: float

    def __post_init__(self) -> None:
        self.margin = _margin(self.margin, self.alternative)

        pv = _ParamsValidator(
            mean=self.mean,
            null_mean=self.null_mean,
            margin=self.margin,
            diff=self.diff,
            superiority_mean=self.superiority_mean,
            offset=self.offset,
            alternative=self.alternative,
        )
        pv.validate("diff", warning=False)
        pv.validate("superiority_mean", warning=False)
        pv.validate("offset", warning=False)

        self.diff = pv.diff
        self.superiority_mean = pv.superiority_mean
        self.offset = pv.offset


case_group_z = [
    # mean = 40, null_mean = 18, margin = 2 to 17 by 0.5, std = 40, alpha = 0.025, power = 0.80, alternative = "greater", dist = "z"
    TestCase(
        mean=40,
        null_mean=18,
        margin=margin,
        std=40,
        size=size,
        alternative="greater",
        alpha=0.025,
        dist="z",
        power=0.80,
        actual_power=actual_power,
    )
    for margin, size, actual_power in [
        (2.0, 32, 0.807429578798747),
        (2.5, 34, 0.811280559074981),
        (3.0, 35, 0.802385798316682),
        (3.5, 37, 0.803257313668525),
        (4.0, 39, 0.802416704846465),
        (4.5, 42, 0.809310990820384),
        (5.0, 44, 0.804875830571654),
        (5.5, 47, 0.807301064915486),
        (6.0, 50, 0.807429578798748),
        (6.5, 53, 0.805402622007928),
        (7.0, 56, 0.801301455458812),
        (7.5, 60, 0.801766796687869),
        (8.0, 65, 0.805608424982718),
        (8.5, 69, 0.800531596054328),
        (9.0, 75, 0.803618830267023),
        (9.5, 81, 0.803041670796890),
        (10.0, 88, 0.803526582386345),
        (10.5, 95, 0.800173015110702),
        (11.0, 104, 0.800804060056704),
        (11.5, 114, 0.800321191492937),
        (12.0, 126, 0.801301455458812),
        (12.5, 140, 0.802385798316682),
        (13.0, 156, 0.802416704846465),
        (13.5, 174, 0.800414728086098),
        (14.0, 197, 0.801549753812365),
        (14.5, 224, 0.801301455458812),
        (15.0, 257, 0.801083976067046),
        (15.5, 298, 0.801006255444267),
        (16.0, 349, 0.800180816214511),
        (16.5, 416, 0.800804060056704),
        (17.0, 503, 0.800523806680340),
    ]
] + [
    # mean = 8, null_mean = 30, margin = -17 to -2 by 0.5, std = 40, alpha = 0.025, power = 0.80, alternative = "less", dist = "z"
    TestCase(
        mean=8,
        null_mean=30,
        margin=margin,
        std=40,
        size=size,
        alternative="less",
        alpha=0.025,
        dist="z",
        power=0.80,
        actual_power=actual_power,
    )
    for margin, size, actual_power in [
        (-17.0, 503, 0.800523806680340),
        (-16.5, 416, 0.800804060056704),
        (-16.0, 349, 0.800180816214512),
        (-15.5, 298, 0.801006255444267),
        (-15.0, 257, 0.801083976067047),
        (-14.5, 224, 0.801301455458812),
        (-14.0, 197, 0.801549753812365),
        (-13.5, 174, 0.800414728086098),
        (-13.0, 156, 0.802416704846465),
        (-12.5, 140, 0.802385798316683),
        (-12.0, 126, 0.801301455458812),
        (-11.5, 114, 0.800321191492937),
        (-11.0, 104, 0.800804060056704),
        (-10.5, 95, 0.800173015110702),
        (-10.0, 88, 0.803526582386346),
        (-9.5, 81, 0.803041670796890),
        (-9.0, 75, 0.803618830267023),
        (-8.5, 69, 0.800531596054328),
        (-8.0, 65, 0.805608424982718),
        (-7.5, 60, 0.801766796687869),
        (-7.0, 56, 0.801301455458812),
        (-6.5, 53, 0.805402622007929),
        (-6.0, 50, 0.807429578798748),
        (-5.5, 47, 0.807301064915486),
        (-5.0, 44, 0.804875830571654),
        (-4.5, 42, 0.809310990820385),
        (-4.0, 39, 0.802416704846465),
        (-3.5, 37, 0.803257313668525),
        (-3.0, 35, 0.802385798316683),
        (-2.5, 34, 0.811280559074982),
        (-2.0, 32, 0.807429578798748),
    ]
]


case_group_t = [
    # mean = 40, null_mean = 18, margin = 2 to 17 by 0.5, std = 40, alpha = 0.025, power = 0.80, alternative = "greater", dist = "t"
    TestCase(
        mean=40,
        null_mean=18,
        margin=margin,
        std=40,
        size=size,
        alternative="greater",
        alpha=0.025,
        dist="t",
        power=0.80,
        actual_power=actual_power,
    )
    for margin, size, actual_power in [
        (2.0, 34, 0.807776685543458),
        (2.5, 35, 0.800053415357762),
        (3.0, 37, 0.802755284947258),
        (3.5, 39, 0.803630625012321),
        (4.0, 41, 0.802793253337018),
        (4.5, 43, 0.800318375321791),
        (5.0, 46, 0.805246964828903),
        (5.5, 49, 0.807664762496591),
        (6.0, 52, 0.807786981876298),
        (6.5, 55, 0.805754911453643),
        (7.0, 58, 0.801649745808345),
        (7.5, 62, 0.802103846807924),
        (8.0, 67, 0.805928875992880),
        (8.5, 71, 0.800845356552311),
        (9.0, 77, 0.803915153395315),
        (9.5, 83, 0.803324143346699),
        (10.0, 90, 0.803793402006325),
        (10.5, 97, 0.800427634167440),
        (11.0, 106, 0.801041954704910),
        (11.5, 116, 0.800543202426292),
        (12.0, 128, 0.801506202603035),
        (12.5, 142, 0.802573336713322),
        (13.0, 157, 0.800072943709877),
        (13.5, 176, 0.800571440584003),
        (14.0, 199, 0.801690092470930),
        (14.5, 226, 0.801426727506516),
        (15.0, 259, 0.801194673157606),
        (15.5, 300, 0.801102919330952),
        (16.0, 351, 0.800264407800567),
        (16.5, 418, 0.800874842237122),
        (17.0, 505, 0.800582923601105),
    ]
] + [
    # mean = 8, null_mean = 30, margin = -17 to -2 by 0.5, std = 40, alpha = 0.025, power = 0.80, alternative = "less", dist = "t"
    TestCase(
        mean=8,
        null_mean=30,
        margin=margin,
        std=40,
        size=size,
        alternative="less",
        alpha=0.025,
        dist="t",
        power=0.80,
        actual_power=actual_power,
    )
    for margin, size, actual_power in [
        (-17.0, 505, 0.800582923601105),
        (-16.5, 418, 0.800874842237122),
        (-16.0, 351, 0.800264407800567),
        (-15.5, 300, 0.801102919330952),
        (-15.0, 259, 0.801194673157606),
        (-14.5, 226, 0.801426727506516),
        (-14.0, 199, 0.801690092470930),
        (-13.5, 176, 0.800571440584003),
        (-13.0, 157, 0.800072943709877),
        (-12.5, 142, 0.802573336713322),
        (-12.0, 128, 0.801506202603035),
        (-11.5, 116, 0.800543202426292),
        (-11.0, 106, 0.801041954704910),
        (-10.5, 97, 0.800427634167440),
        (-10.0, 90, 0.803793402006325),
        (-9.5, 83, 0.803324143346699),
        (-9.0, 77, 0.803915153395315),
        (-8.5, 71, 0.800845356552311),
        (-8.0, 67, 0.805928875992880),
        (-7.5, 62, 0.802103846807924),
        (-7.0, 58, 0.801649745808345),
        (-6.5, 55, 0.805754911453643),
        (-6.0, 52, 0.807786981876298),
        (-5.5, 49, 0.807664762496591),
        (-5.0, 46, 0.805246964828903),
        (-4.5, 43, 0.800318375321791),
        (-4.0, 41, 0.802793253337018),
        (-3.5, 39, 0.803630625012321),
        (-3.0, 37, 0.802755284947258),
        (-2.5, 35, 0.800053415357762),
        (-2.0, 34, 0.807776685543458),
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
            superiority_mean=case.superiority_mean,
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

    if case.margin in [2.0, 8.0, 12.0, 17.0] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(
            pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470")
        )

    assert (
        solve_size(
            mean=case.mean,
            null_mean=case.null_mean,
            margin=case.margin,
            diff=case.diff,
            superiority_mean=case.superiority_mean,
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

    if case.margin in [7.5, 15.0] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(
            pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470")
        )

    assert round(
        solve_mean(
            null_mean=case.null_mean,
            margin=case.margin,
            superiority_mean=case.superiority_mean,
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

    if case.margin in [7.5, 15.0] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(
            pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470")
        )

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


def test_solve_margin(case: TestCase) -> None:

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

    if case.margin in [10.5, 11.0, 16.5] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(
            pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470")
        )

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


def test_solve_superiority_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.margin in [8.0, 8.5] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(
            pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470")
        )

    assert round(
        solve_superiority_mean(
            mean=case.mean,
            std=case.std,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.actual_power,
            dist=case.dist,
        ),
        2,
    ) == round(case.superiority_mean, 2)


def test_solve_offset(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case.margin in [4.5, 12.5] and case.alternative == "greater" and case.dist == "t":
        request.node.add_marker(
            pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470")
        )

    if (
        case.margin
        in [
            -17.0,
            -16.5,
            -16.0,
            -15.5,
            -13.5,
            -12.5,
            -11.5,
            -10.5,
            -9.5,
            -9.0,
            -8.5,
            -7.0,
            -6.0,
            -5.5,
            -5.0,
            -4.0,
            -2.0,
        ]
        and case.alternative == "less"
        and case.dist == "t"
    ):
        request.node.add_marker(
            pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470")
        )

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
                superiority_mean=case.superiority_mean,
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
