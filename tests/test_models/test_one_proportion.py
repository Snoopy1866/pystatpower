from math import ceil

import pytest

from pystatpower.models import one_proportion


class TestSolveForSampleSize:
    test_data = [
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "EXACT_TEST"), 42),
        ((0.05, 0.80, 0.80, 0.95, "ONE_SIDED", "EXACT_TEST"), 32),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_USING_S_P0"), 42),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_USING_S_P0_CC"), 49),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_USING_S_PHAT"), 17),
        ((0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "Z_TEST_USING_S_PHAT_CC"), 23),
    ]

    test_data_raise_error = [
        ((0.05, 0.80, 0.80, 0.80, "TWO_SIDED", "EXACT_TEST"), ValueError),
    ]

    @pytest.mark.parametrize(("params", "expected_result"), test_data)
    def test_solve(self, params, expected_result):
        result = one_proportion.solve_for_sample_size(*params)
        assert ceil(result) == expected_result

    @pytest.mark.parametrize(("params", "expected_error"), test_data_raise_error)
    def test_solve_raise_error(self, params, expected_error):
        with pytest.raises(expected_error):
            one_proportion.solve_for_sample_size(*params)

    def test_solve_full_output(self):
        result = one_proportion.solve_for_sample_size(
            0.05, 0.80, 0.80, 0.95, "TWO_SIDED", "EXACT_TEST", full_output=True
        )
        assert isinstance(result, one_proportion.OneProportion.ForSize)


class TestSolveForAlpha:
    test_data = [
        ((42, 0.80, 0.80, 0.95, "TWO_SIDED", "EXACT_TEST"), 0.05),
    ]

    @pytest.mark.parametrize(("params", "expected_result"), test_data)
    def test_solve(self, params, expected_result):
        result = one_proportion.solve_for_alpha(*params)
        assert round(result, 2) == expected_result

    def test_solve_full_output(self):
        result = one_proportion.solve_for_alpha(70, 0.80, 0.80, 0.95, "TWO_SIDED", "EXACT_TEST", full_output=True)
        assert isinstance(result, one_proportion.OneProportion.ForAlpha)


class TestSolveForPower:
    test_data = [
        ((42, 0.05, 0.80, 0.95, "TWO_SIDED", "EXACT_TEST"), 0.80598),
        ((42, 0.05, 0.80, 0.95, "ONE_SIDED", "EXACT_TEST"), 0.92528),
        ((42, 0.05, 0.80, 0.95, "TWO_SIDED", "Z_TEST_USING_S_P0"), 0.80598),
        ((42, 0.05, 0.80, 0.95, "TWO_SIDED", "Z_TEST_USING_S_P0_CC"), 0.69469),
        ((42, 0.05, 0.80, 0.95, "TWO_SIDED", "Z_TEST_USING_S_PHAT"), 0.99380),
        ((42, 0.05, 0.80, 0.95, "TWO_SIDED", "Z_TEST_USING_S_PHAT_CC"), 0.98408),
    ]

    @pytest.mark.parametrize(("params", "expected_result"), test_data)
    def test_solve(self, params, expected_result):
        result = one_proportion.solve_for_power(*params)
        assert round(result, 5) == expected_result

    def test_solve_full_output(self):
        result = one_proportion.solve_for_power(70, 0.05, 0.80, 0.95, "TWO_SIDED", "EXACT_TEST", full_output=True)
        assert isinstance(result, one_proportion.OneProportion.ForPower)


class TestSolveForNullProportion:
    test_data = [
        ((42, 0.05, 0.80, 0.95, "TWO_SIDED", "EXACT_TEST", "LESS"), 0.80),
        ((42, 0.05, 0.80, 0.95, "TWO_SIDED", "EXACT_TEST", "GREATER"), 1.00),
    ]

    test_data_raise_error = [
        ((42, 0.05, 0.80, 0.05, "TWO_SIDED", "Z_TEST_USING_S_PHAT_CC", "LESS"), ValueError),
        ((42, 0.05, 0.80, 0.95, "TWO_SIDED", "Z_TEST_USING_S_PHAT_CC", "GREATER"), ValueError),
    ]

    @pytest.mark.parametrize(("params", "expected_result"), test_data)
    def test_solve(self, params, expected_result):
        result = one_proportion.solve_for_nullproportion(*params)
        assert round(result, 2) == expected_result

    @pytest.mark.parametrize(("params", "expected_error"), test_data_raise_error)
    def test_solve_raise_error(self, params, expected_error):
        with pytest.raises(expected_error):
            one_proportion.solve_for_nullproportion(*params)

    def test_solve_full_output(self):
        result = one_proportion.solve_for_nullproportion(
            70, 0.05, 0.80, 0.95, "TWO_SIDED", "EXACT_TEST", "LESS", full_output=True
        )
        assert isinstance(result, one_proportion.OneProportion.ForNullProportion)


class TestSolveForProportion:
    test_data = [
        ((42, 0.05, 0.80, 0.80, "ONE_SIDED", "Z_TEST_USING_S_P0_CC", "LESS"), 0.6237),
        ((42, 0.05, 0.80, 0.80, "ONE_SIDED", "Z_TEST_USING_S_P0_CC", "GREATER"), 0.9434),
    ]

    test_data_raise_error = [
        ((4, 0.05, 0.80, 0.00001, "TWO_SIDED", "Z_TEST_USING_S_PHAT_CC", "LESS"), ValueError),
        ((4, 0.05, 0.80, 0.99999, "TWO_SIDED", "Z_TEST_USING_S_PHAT_CC", "GREATER"), ValueError),
    ]

    @pytest.mark.parametrize(("params", "expected_result"), test_data)
    def test_solve(self, params, expected_result):
        result = one_proportion.solve_for_proportion(*params)
        assert round(result, 4) == expected_result

    @pytest.mark.parametrize(("params", "expected_error"), test_data_raise_error)
    def test_solve_raise_error(self, params, expected_error):
        with pytest.raises(expected_error):
            one_proportion.solve_for_proportion(*params)

    def test_solve_full_output(self):
        result = one_proportion.solve_for_proportion(
            70, 0.05, 0.80, 0.95, "TWO_SIDED", "EXACT_TEST", "LESS", full_output=True
        )
        assert isinstance(result, one_proportion.OneProportion.ForProportion)
