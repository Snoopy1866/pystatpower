from math import ceil

import pytest

from pystatpower.models.two_proportion import *
from pystatpower.models.two_proportion import TwoProportion


class TestSolveForSampleSize:
    test_data = [
        # TWO_SIDED + Z_TEST_POOLED
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation()), (76, 76)),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_treatment=70)), (70, 79)),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_reference=70)), (85, 70)),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(ratio_of_treatment_to_reference=2)),
            (120, 60),
        ),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(ratio_of_reference_to_treatment=2)),
            (52, 104),
        ),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(percent_of_treatment=0.8)), (205, 52)),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(percent_of_reference=0.8)),
            (40, 159),
        ),
        # TWO_SIDED + Z_TEST_UNPOOLED
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_UNPOOLED", GroupAllocation()), (73, 73)),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_UNPOOLED", GroupAllocation(size_of_treatment=70)), (70, 82)),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_UNPOOLED", GroupAllocation(size_of_reference=70)), (74, 70)),
        (
            (
                0.05,
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_UNPOOLED",
                GroupAllocation(ratio_of_treatment_to_reference=2),
            ),
            (89, 45),
        ),
        (
            (
                0.05,
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_UNPOOLED",
                GroupAllocation(ratio_of_reference_to_treatment=2),
            ),
            (65, 129),
        ),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_UNPOOLED", GroupAllocation(percent_of_treatment=0.8)),
            (123, 31),
        ),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_UNPOOLED", GroupAllocation(percent_of_reference=0.8)),
            (60, 240),
        ),
        # TWO_SIDED + Z_TEST_CC_POOLED
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_CC_POOLED", GroupAllocation()), (88, 88)),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_CC_POOLED", GroupAllocation(size_of_treatment=70)), (70, 107)),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_CC_POOLED", GroupAllocation(size_of_reference=70)),
            (135, 70),
        ),
        (
            (
                0.05,
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_CC_POOLED",
                GroupAllocation(ratio_of_treatment_to_reference=2),
            ),
            (139, 70),
        ),
        (
            (
                0.05,
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_CC_POOLED",
                GroupAllocation(ratio_of_reference_to_treatment=2),
            ),
            (62, 124),
        ),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_CC_POOLED", GroupAllocation(percent_of_treatment=0.8)),
            (237, 60),
        ),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_CC_POOLED", GroupAllocation(percent_of_reference=0.8)),
            (48, 191),
        ),
        # TWO_SIDED + Z_TEST_CC_UNPOOLED
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_CC_UNPOOLED", GroupAllocation()), (86, 86)),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_CC_UNPOOLED", GroupAllocation(size_of_treatment=70)), (70, 209)),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_CC_UNPOOLED", GroupAllocation(size_of_reference=70)), (93, 70)),
        (
            (
                0.05,
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_CC_UNPOOLED",
                GroupAllocation(ratio_of_treatment_to_reference=2),
            ),
            (109, 55),
        ),
        (
            (
                0.05,
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_CC_UNPOOLED",
                GroupAllocation(ratio_of_reference_to_treatment=2),
            ),
            (74, 148),
        ),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_CC_UNPOOLED", GroupAllocation(percent_of_treatment=0.8)),
            (154, 39),
        ),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_CC_UNPOOLED", GroupAllocation(percent_of_reference=0.8)),
            (69, 273),
        ),
        # ONE_SIDED + Z_TEST_POOLED
        ((0.05, 0.80, 0.80, 0.95, "ONE_SIDED", "Z_TEST_POOLED", GroupAllocation()), (60, 60)),
        ((0.05, 0.80, 0.80, 0.95, "ONE_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_treatment=70)), (70, 53)),
        ((0.05, 0.80, 0.80, 0.95, "ONE_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_reference=70)), (49, 70)),
        (
            (0.05, 0.80, 0.80, 0.95, "ONE_SIDED", "Z_TEST_POOLED", GroupAllocation(ratio_of_treatment_to_reference=2)),
            (93, 47),
        ),
        (
            (0.05, 0.80, 0.80, 0.95, "ONE_SIDED", "Z_TEST_POOLED", GroupAllocation(ratio_of_reference_to_treatment=2)),
            (42, 83),
        ),
        ((0.05, 0.80, 0.80, 0.95, "ONE_SIDED", "Z_TEST_POOLED", GroupAllocation(percent_of_treatment=0.8)), (157, 40)),
        ((0.05, 0.80, 0.80, 0.95, "ONE_SIDED", "Z_TEST_POOLED", GroupAllocation(percent_of_reference=0.8)), (32, 128)),
        # ONE_SIDED + Z_TEST_UNPOOLED
        ((0.05, 0.80, 0.80, 0.65, "ONE_SIDED", "Z_TEST_UNPOOLED", GroupAllocation()), (107, 107)),
        ((0.05, 0.80, 0.80, 0.65, "ONE_SIDED", "Z_TEST_UNPOOLED", GroupAllocation(size_of_treatment=70)), (70, 169)),
        ((0.05, 0.80, 0.80, 0.65, "ONE_SIDED", "Z_TEST_UNPOOLED", GroupAllocation(size_of_reference=70)), (412, 70)),
        (
            (
                0.05,
                0.80,
                0.80,
                0.65,
                "ONE_SIDED",
                "Z_TEST_UNPOOLED",
                GroupAllocation(ratio_of_treatment_to_reference=2),
            ),
            (169, 85),
        ),
        (
            (
                0.05,
                0.80,
                0.80,
                0.65,
                "ONE_SIDED",
                "Z_TEST_UNPOOLED",
                GroupAllocation(ratio_of_reference_to_treatment=2),
            ),
            (76, 151),
        ),
        (
            (0.05, 0.80, 0.80, 0.65, "ONE_SIDED", "Z_TEST_UNPOOLED", GroupAllocation(percent_of_treatment=0.8)),
            (295, 74),
        ),
        (
            (0.05, 0.80, 0.80, 0.65, "ONE_SIDED", "Z_TEST_UNPOOLED", GroupAllocation(percent_of_reference=0.8)),
            (60, 239),
        ),
    ]

    @pytest.mark.parametrize(("params", "expected_result"), test_data)
    def test_solve(self, params, expected_result):
        result = solve_for_sample_size(*params)
        assert tuple(map(ceil, result)) == expected_result

    test_data_with_dropout_rate = [
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(), 0.10), (85, 85)),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_treatment=70), 0.10), (78, 88)),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_reference=70), 0.10), (95, 78)),
        (
            (
                0.05,
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(ratio_of_treatment_to_reference=2),
                0.10,
            ),
            (134, 67),
        ),
        (
            (
                0.05,
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(ratio_of_reference_to_treatment=2),
                0.10,
            ),
            (58, 116),
        ),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(percent_of_treatment=0.8), 0.10),
            (228, 58),
        ),
        (
            (0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(percent_of_reference=0.8), 0.10),
            (45, 177),
        ),
    ]

    @pytest.mark.parametrize(("params", "expected_result"), test_data_with_dropout_rate)
    def test_solve_with_dropout_rate(self, params, expected_result) -> None:
        result = solve_for_sample_size(*params, full_output=True)
        assert (result.treatment_size_include_dropouts, result.reference_size_include_dropouts) == expected_result

    def test_solve_full_output(self):
        result = solve_for_sample_size(
            0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", group_allocation=GroupAllocation(), full_output=True
        )
        assert isinstance(result, TwoProportion.ForSize)

    def test_invalid_group_allocation(self):
        with pytest.raises(ValueError):
            solve_for_sample_size(
                alpha=0.08,
                power=0.80,
                treatment_proportion=0.80,
                reference_proportion=0.95,
                alternative="TWO_SIDED",
                test_type="Z_TEST_POOLED",
                group_allocation=GroupAllocation(size_of_treatment=100, size_of_reference=100),
            )

    def test_no_solution(self):
        with pytest.raises(ValueError):
            solve_for_sample_size(
                alpha=0.0000000001,
                power=0.9999999999,
                treatment_proportion=0.50,
                reference_proportion=0.49999999999,
                alternative="TWO_SIDED",
                test_type="Z_TEST_POOLED",
                group_allocation=GroupAllocation(),
            )


class TestSolveForAlpha:
    test_data = [
        ((0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_total=100)), 0.14752498),
        ((0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_each=100)), 0.01696612),
        ((0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_treatment=100)), 0.01696612),
        ((0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_reference=100)), 0.01696612),
        (
            (0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_total=100, size_of_treatment=30)),
            0.18362176,
        ),
        (
            (0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_total=100, size_of_reference=30)),
            0.21624494,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_total=100, ratio_of_treatment_to_reference=3),
            ),
            0.25704323,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_total=100, ratio_of_reference_to_treatment=3),
            ),
            0.21840194,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_total=100, percent_of_treatment=0.8),
            ),
            0.31499795,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_total=100, percent_of_reference=0.8),
            ),
            0.2719625,
        ),
        ((0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_each=100)), 0.01696612),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_treatment=100, size_of_reference=100),
            ),
            0.01696612,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_treatment=100, ratio_of_treatment_to_reference=4),
            ),
            0.23283863,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_treatment=100, ratio_of_reference_to_treatment=4),
            ),
            0.00014764,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_treatment=100, percent_of_treatment=0.8),
            ),
            0.23283863,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_treatment=100, percent_of_reference=0.8),
            ),
            0.00014764,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_reference=100, ratio_of_treatment_to_reference=4),
            ),
            0.00289295,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_reference=100, ratio_of_reference_to_treatment=4),
            ),
            0.18177707,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_reference=100, percent_of_treatment=0.8),
            ),
            0.00289295,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_reference=100, percent_of_reference=0.8),
            ),
            0.18177707,
        ),
    ]

    @pytest.mark.parametrize(("params", "expected_alpha"), test_data)
    def test_solve(self, params, expected_alpha):
        result = solve_for_alpha(*params)
        assert round(result, 8) == expected_alpha

    test_data_with_dropout_rate = [
        ((0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_each=100), 0.10), (112, 112)),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(size_of_total=100, ratio_of_treatment_to_reference=2),
                0.10,
            ),
            (75, 38),
        ),
    ]

    @pytest.mark.parametrize(("params", "expected_result"), test_data_with_dropout_rate)
    def test_solve_with_dropout_rate(self, params, expected_result) -> None:
        result = solve_for_alpha(*params, full_output=True)
        assert (result.treatment_size_include_dropouts, result.reference_size_include_dropouts) == expected_result

    def test_solve_full_output(self):
        result = solve_for_alpha(
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            group_allocation=GroupAllocation(size_of_each=100),
            full_output=True,
        )
        assert isinstance(result, TwoProportion.ForAlpha)

    test_data_raise_error = [
        (
            (0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(ratio_of_treatment_to_reference=3)),
            ValueError,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(ratio_of_treatment_to_reference=3, percent_of_reference=0.25),
            ),
            ValueError,
        ),
        (
            (
                0.80,
                0.80,
                0.95,
                "TWO_SIDED",
                "Z_TEST_POOLED",
                GroupAllocation(ratio_of_treatment_to_reference=3, percent_of_reference=0.25, size_of_total=100),
            ),
            ValueError,
        ),
    ]

    @pytest.mark.parametrize(("params", "expected_error"), test_data_raise_error)
    def test_invalid_group_allocation(self, params, expected_error):
        with pytest.raises(expected_error):
            solve_for_alpha(*params)


class TestSolveForPower:
    test_data = [
        ((0.05, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_total=100)), 0.62402759),
    ]

    @pytest.mark.parametrize(("params", "expected_power"), test_data)
    def test_solve(self, params, expected_power):
        result = solve_for_power(*params)
        assert round(result, 8) == expected_power

    def test_solve_full_output(self):
        result = solve_for_power(
            0.05,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            group_allocation=GroupAllocation(size_of_each=100),
            full_output=True,
        )
        assert isinstance(result, TwoProportion.ForPower)


class TestSolveForTreatmentProportion:
    test_data = [
        ((0.05, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_total=100), "LESS"), 0.75312953),
        ((0.05, 0.80, 0.85, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_total=100), "GREATER"), 0.99712574),
    ]

    @pytest.mark.parametrize(("params", "expected_treatment_proportion"), test_data)
    def test_solve(self, params, expected_treatment_proportion):
        result = solve_for_treatment_proportion(*params)
        assert round(result, 8) == expected_treatment_proportion

    def test_solve_full_output(self):
        result = solve_for_treatment_proportion(
            0.05,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            group_allocation=GroupAllocation(size_of_each=100),
            search_direction="LESS",
            full_output=True,
        )
        assert isinstance(result, TwoProportion.ForTreatmentProportion)

    def test_no_solution(self):
        with pytest.raises(ValueError):
            solve_for_treatment_proportion(
                alpha=0.05,
                power=0.80,
                reference_proportion=0.95,
                alternative="TWO_SIDED",
                test_type="Z_TEST_POOLED",
                group_allocation=GroupAllocation(size_of_total=100),
                search_direction="GREATER",
            )


class TestSolveForReferenceProportion:
    test_data = [
        ((0.05, 0.80, 0.95, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_total=100), "LESS"), 0.75312953),
        ((0.05, 0.80, 0.85, "TWO_SIDED", "Z_TEST_POOLED", GroupAllocation(size_of_total=100), "GREATER"), 0.99712574),
    ]

    @pytest.mark.parametrize(("params", "expected_reference_proportion"), test_data)
    def test_solve(self, params, expected_reference_proportion):
        result = solve_for_reference_proportion(*params)
        assert round(result, 8) == expected_reference_proportion

    def test_solve_full_output(self):
        result = solve_for_reference_proportion(
            0.05,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            group_allocation=GroupAllocation(size_of_each=100),
            search_direction="LESS",
            full_output=True,
        )
        assert isinstance(result, TwoProportion.ForReferenceProportion)

    def test_no_solution(self):
        with pytest.raises(ValueError):
            solve_for_reference_proportion(
                alpha=0.05,
                power=0.80,
                treatment_proportion=0.95,
                alternative="TWO_SIDED",
                test_type="Z_TEST_POOLED",
                group_allocation=GroupAllocation(size_of_total=100),
                search_direction="GREATER",
            )
