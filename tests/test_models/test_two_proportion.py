from math import ceil

import pytest

from pystatpower.models.two_proportion import *
from pystatpower.models.two_proportion import TwoProportion


class TestSolveForSampleSize:
    params_list = [
        # (expected_treatment_size, expected_reference_size, alpha, power, treatment_proportion, reference_proportion, alternative, test_type, group_allocation)
        # TWO_SIDED + Z_TEST_POOLED
        (
            76,
            76,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(),
        ),
        (
            70,
            79,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_treatment=70),
        ),
        (
            85,
            70,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_reference=70),
        ),
        (
            120,
            60,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(ratio_of_treatment_to_reference=2),
        ),
        (
            52,
            104,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(ratio_of_reference_to_treatment=2),
        ),
        (
            205,
            52,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(percent_of_treatment=0.8),
        ),
        (
            40,
            159,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(percent_of_reference=0.8),
        ),
        # TWO_SIDED + Z_TEST_UNPOOLED
        (
            73,
            73,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(),
        ),
        (
            70,
            82,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(size_of_treatment=70),
        ),
        (
            74,
            70,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(size_of_reference=70),
        ),
        (
            89,
            45,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(ratio_of_treatment_to_reference=2),
        ),
        (
            65,
            129,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(ratio_of_reference_to_treatment=2),
        ),
        (
            123,
            31,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(percent_of_treatment=0.8),
        ),
        (
            60,
            240,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(percent_of_reference=0.8),
        ),
        # TWO_SIDED + Z_TEST_CC_POOLED
        (
            88,
            88,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_POOLED",
            GroupAllocation(),
        ),
        (
            70,
            107,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_POOLED",
            GroupAllocation(size_of_treatment=70),
        ),
        (
            135,
            70,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_POOLED",
            GroupAllocation(size_of_reference=70),
        ),
        (
            139,
            70,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_POOLED",
            GroupAllocation(ratio_of_treatment_to_reference=2),
        ),
        (
            62,
            124,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_POOLED",
            GroupAllocation(ratio_of_reference_to_treatment=2),
        ),
        (
            237,
            60,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_POOLED",
            GroupAllocation(percent_of_treatment=0.8),
        ),
        (
            48,
            191,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_POOLED",
            GroupAllocation(percent_of_reference=0.8),
        ),
        # TWO_SIDED + Z_TEST_CC_UNPOOLED
        (
            86,
            86,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_UNPOOLED",
            GroupAllocation(),
        ),
        (
            70,
            209,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_UNPOOLED",
            GroupAllocation(size_of_treatment=70),
        ),
        (
            93,
            70,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_UNPOOLED",
            GroupAllocation(size_of_reference=70),
        ),
        (
            109,
            55,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_UNPOOLED",
            GroupAllocation(ratio_of_treatment_to_reference=2),
        ),
        (
            74,
            148,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_UNPOOLED",
            GroupAllocation(ratio_of_reference_to_treatment=2),
        ),
        (
            154,
            39,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_UNPOOLED",
            GroupAllocation(percent_of_treatment=0.8),
        ),
        (
            69,
            273,
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_CC_UNPOOLED",
            GroupAllocation(percent_of_reference=0.8),
        ),
        # ONE_SIDED + Z_TEST_POOLED
        (
            60,
            60,
            0.05,
            0.80,
            0.80,
            0.95,
            "ONE_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(),
        ),
        (
            70,
            53,
            0.05,
            0.80,
            0.80,
            0.95,
            "ONE_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_treatment=70),
        ),
        (
            49,
            70,
            0.05,
            0.80,
            0.80,
            0.95,
            "ONE_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_reference=70),
        ),
        (
            93,
            47,
            0.05,
            0.80,
            0.80,
            0.95,
            "ONE_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(ratio_of_treatment_to_reference=2),
        ),
        (
            42,
            83,
            0.05,
            0.80,
            0.80,
            0.95,
            "ONE_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(ratio_of_reference_to_treatment=2),
        ),
        (
            157,
            40,
            0.05,
            0.80,
            0.80,
            0.95,
            "ONE_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(percent_of_treatment=0.8),
        ),
        (
            32,
            128,
            0.05,
            0.80,
            0.80,
            0.95,
            "ONE_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(percent_of_reference=0.8),
        ),
        # ONE_SIDED + Z_TEST_UNPOOLED
        (
            107,
            107,
            0.05,
            0.80,
            0.80,
            0.65,
            "ONE_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(),
        ),
        (
            70,
            169,
            0.05,
            0.80,
            0.80,
            0.65,
            "ONE_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(size_of_treatment=70),
        ),
        (
            412,
            70,
            0.05,
            0.80,
            0.80,
            0.65,
            "ONE_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(size_of_reference=70),
        ),
        (
            169,
            85,
            0.05,
            0.80,
            0.80,
            0.65,
            "ONE_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(ratio_of_treatment_to_reference=2),
        ),
        (
            76,
            151,
            0.05,
            0.80,
            0.80,
            0.65,
            "ONE_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(ratio_of_reference_to_treatment=2),
        ),
        (
            295,
            74,
            0.05,
            0.80,
            0.80,
            0.65,
            "ONE_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(percent_of_treatment=0.8),
        ),
        (
            60,
            239,
            0.05,
            0.80,
            0.80,
            0.65,
            "ONE_SIDED",
            "Z_TEST_UNPOOLED",
            GroupAllocation(percent_of_reference=0.8),
        ),
    ]

    def test_solve(self):
        for (
            expected_treatment_size,
            expected_reference_size,
            alpha,
            power,
            treatment_proportion,
            reference_proportion,
            alternative,
            test_type,
            group_allocation,
        ) in TestSolveForSampleSize.params_list:
            result = solve_for_sample_size(
                alpha=alpha,
                power=power,
                treatment_proportion=treatment_proportion,
                reference_proportion=reference_proportion,
                alternative=alternative,
                test_type=test_type,
                group_allocation=group_allocation,
            )
            assert tuple(map(ceil, result)) == (expected_treatment_size, expected_reference_size)

    def test_solve_with_dropout_rate(self) -> None:
        result = solve_for_sample_size(
            alpha=0.05,
            power=0.80,
            treatment_proportion=0.80,
            reference_proportion=0.95,
            alternative="TWO_SIDED",
            test_type="Z_TEST_POOLED",
            group_allocation=GroupAllocation(),
            dropout_rate=0.10,
            full_output=True,
        )
        assert (result.treatment_size_include_dropouts, result.reference_size_include_dropouts) == (85, 85)

        result = solve_for_sample_size(
            alpha=0.05,
            power=0.80,
            treatment_proportion=0.80,
            reference_proportion=0.95,
            alternative="TWO_SIDED",
            test_type="Z_TEST_POOLED",
            group_allocation=GroupAllocation(size_of_treatment=70),
            dropout_rate=0.10,
            full_output=True,
        )
        assert (result.treatment_size_include_dropouts, result.reference_size_include_dropouts) == (78, 88)

        result = solve_for_sample_size(
            alpha=0.05,
            power=0.80,
            treatment_proportion=0.80,
            reference_proportion=0.95,
            alternative="TWO_SIDED",
            test_type="Z_TEST_POOLED",
            group_allocation=GroupAllocation(size_of_reference=70),
            dropout_rate=0.10,
            full_output=True,
        )
        assert (result.treatment_size_include_dropouts, result.reference_size_include_dropouts) == (95, 78)

        result = solve_for_sample_size(
            alpha=0.05,
            power=0.80,
            treatment_proportion=0.80,
            reference_proportion=0.95,
            alternative="TWO_SIDED",
            test_type="Z_TEST_POOLED",
            group_allocation=GroupAllocation(ratio_of_treatment_to_reference=2),
            dropout_rate=0.10,
            full_output=True,
        )
        assert (result.treatment_size_include_dropouts, result.reference_size_include_dropouts) == (134, 67)

        result = solve_for_sample_size(
            alpha=0.05,
            power=0.80,
            treatment_proportion=0.80,
            reference_proportion=0.95,
            alternative="TWO_SIDED",
            test_type="Z_TEST_POOLED",
            group_allocation=GroupAllocation(ratio_of_reference_to_treatment=2),
            dropout_rate=0.10,
            full_output=True,
        )
        assert (result.treatment_size_include_dropouts, result.reference_size_include_dropouts) == (58, 116)

        result = solve_for_sample_size(
            alpha=0.05,
            power=0.80,
            treatment_proportion=0.80,
            reference_proportion=0.95,
            alternative="TWO_SIDED",
            test_type="Z_TEST_POOLED",
            group_allocation=GroupAllocation(percent_of_treatment=0.8),
            dropout_rate=0.10,
            full_output=True,
        )
        assert (result.treatment_size_include_dropouts, result.reference_size_include_dropouts) == (228, 58)

        result = solve_for_sample_size(
            alpha=0.05,
            power=0.80,
            treatment_proportion=0.80,
            reference_proportion=0.95,
            alternative="TWO_SIDED",
            test_type="Z_TEST_POOLED",
            group_allocation=GroupAllocation(percent_of_reference=0.8),
            dropout_rate=0.10,
            full_output=True,
        )
        assert (result.treatment_size_include_dropouts, result.reference_size_include_dropouts) == (45, 177)

    def test_solve_full_output(self):
        result = solve_for_sample_size(
            0.05,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            group_allocation=GroupAllocation(),
            full_output=True,
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
    params_list = [
        # (expected_alpha, power, treatment_proportion, reference_proportion, alternative, test_type, group_allocation)
        (
            0.14752498,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_total=100),
        ),
        (
            0.01696612,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_each=100),
        ),
        (
            0.01696612,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_treatment=100),
        ),
        (
            0.01696612,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_reference=100),
        ),
        (
            0.18362176,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_total=100,
                size_of_treatment=30,
            ),
        ),
        (
            0.21624494,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_total=100,
                size_of_reference=30,
            ),
        ),
        (
            0.25704323,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_total=100,
                ratio_of_treatment_to_reference=3,
            ),
        ),
        (
            0.21840194,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_total=100,
                ratio_of_reference_to_treatment=3,
            ),
        ),
        (
            0.31499795,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_total=100,
                percent_of_treatment=0.8,
            ),
        ),
        (
            0.2719625,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_total=100,
                percent_of_reference=0.8,
            ),
        ),
        (
            0.01696612,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_each=100,
            ),
        ),
        (
            0.01696612,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_treatment=100,
                size_of_reference=100,
            ),
        ),
        (
            0.23283863,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_treatment=100,
                ratio_of_treatment_to_reference=4,
            ),
        ),
        (
            0.00014764,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_treatment=100,
                ratio_of_reference_to_treatment=4,
            ),
        ),
        (
            0.23283863,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_treatment=100,
                percent_of_treatment=0.8,
            ),
        ),
        (
            0.00014764,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_treatment=100,
                percent_of_reference=0.8,
            ),
        ),
        (
            0.00289295,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_reference=100,
                ratio_of_treatment_to_reference=4,
            ),
        ),
        (
            0.18177707,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_reference=100,
                ratio_of_reference_to_treatment=4,
            ),
        ),
        (
            0.00289295,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_reference=100,
                percent_of_treatment=0.8,
            ),
        ),
        (
            0.18177707,
            0.80,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(
                size_of_reference=100,
                percent_of_reference=0.8,
            ),
        ),
    ]

    def test_solve(self):
        for (
            expected_alpha,
            power,
            treatment_proportion,
            reference_proportion,
            alternative,
            test_type,
            group_allocation,
        ) in TestSolveForAlpha.params_list:
            result = solve_for_alpha(
                power=power,
                treatment_proportion=treatment_proportion,
                reference_proportion=reference_proportion,
                alternative=alternative,
                test_type=test_type,
                group_allocation=group_allocation,
            )
            assert round(result, 8) == expected_alpha

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

    def test_invalid_group_allocation(self):
        with pytest.raises(ValueError):
            solve_for_alpha(
                power=0.80,
                treatment_proportion=0.80,
                reference_proportion=0.95,
                alternative="TWO_SIDED",
                test_type="Z_TEST_POOLED",
                group_allocation=GroupAllocation(ratio_of_treatment_to_reference=3),
            )
        with pytest.raises(ValueError):
            solve_for_alpha(
                power=0.80,
                treatment_proportion=0.80,
                reference_proportion=0.95,
                alternative="TWO_SIDED",
                test_type="Z_TEST_POOLED",
                group_allocation=GroupAllocation(ratio_of_treatment_to_reference=3, percent_of_reference=0.25),
            )
        with pytest.raises(ValueError):
            solve_for_alpha(
                power=0.80,
                treatment_proportion=0.80,
                reference_proportion=0.95,
                alternative="TWO_SIDED",
                test_type="Z_TEST_POOLED",
                group_allocation=GroupAllocation(
                    ratio_of_treatment_to_reference=3, percent_of_reference=0.25, size_of_total=100
                ),
            )


class TestSolveForPower:
    params_list = [
        # (expected_power, alpha, treatment_proportion, reference_proportion, alternative, test_type, group_allocation)
        (
            0.62402759,
            0.05,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_total=100),
        ),
    ]

    def test_solve(self):
        for (
            expected_power,
            alpha,
            treatment_proportion,
            reference_proportion,
            alternative,
            test_type,
            group_allocation,
        ) in TestSolveForPower.params_list:
            result = solve_for_power(
                alpha=alpha,
                treatment_proportion=treatment_proportion,
                reference_proportion=reference_proportion,
                alternative=alternative,
                test_type=test_type,
                group_allocation=group_allocation,
            )
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
    params_list = [
        # (expected_treatment_proportion, alpha, power, reference_proportion, alternative, test_type, group_allocation, search_direction)
        (
            0.75312953,
            0.05,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_total=100),
            "LESS",
        ),
        (
            0.99712574,
            0.05,
            0.80,
            0.85,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_total=100),
            "GREATER",
        ),
    ]

    def test_solve(self):
        for (
            expected_treatment_proportion,
            alpha,
            power,
            reference_proportion,
            alternative,
            test_type,
            group_allocation,
            search_direction,
        ) in TestSolveForTreatmentProportion.params_list:
            result = solve_for_treatment_proportion(
                alpha=alpha,
                power=power,
                reference_proportion=reference_proportion,
                alternative=alternative,
                test_type=test_type,
                group_allocation=group_allocation,
                search_direction=search_direction,
            )
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
    params_list = [
        # (expected_reference_proportion, alpha, power, treatment_proportion, alternative, test_type, group_allocation, search_direction)
        (
            0.75312953,
            0.05,
            0.80,
            0.95,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_total=100),
            "LESS",
        ),
        (
            0.99712574,
            0.05,
            0.80,
            0.85,
            "TWO_SIDED",
            "Z_TEST_POOLED",
            GroupAllocation(size_of_total=100),
            "GREATER",
        ),
    ]

    def test_solve(self):
        for (
            expected_reference_proportion,
            alpha,
            power,
            treatment_proportion,
            alternative,
            test_type,
            group_allocation,
            search_direction,
        ) in TestSolveForReferenceProportion.params_list:
            result = solve_for_reference_proportion(
                alpha=alpha,
                power=power,
                treatment_proportion=treatment_proportion,
                alternative=alternative,
                test_type=test_type,
                group_allocation=group_allocation,
                search_direction=search_direction,
            )
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
