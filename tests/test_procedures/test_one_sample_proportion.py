from math import ceil

import pytest
from pystatpower.exception import (
    CalculationSolutionNotFoundError,
    EnumMemberNotExistError,
    ParameterValueEmptyError,
    ParameterTypeError,
    ParameterValueNotInDomainError,
    TargetParameterNotUniqueError,
    TargetParameterNotExistError,
)
from pystatpower.procedures import one_sample_proportion as OSP


def test_calc_power():
    result = OSP.calc_power(
        n=42,
        alpha=0.05,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.ONE_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_P0,
    )
    assert round(result, 5) == 0.92528

    result = OSP.calc_power(
        n=67,
        alpha=0.05,
        nullproportion=0.78,
        proportion=0.85,
        alternative=OSP.Alternative.ONE_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_PHAT_CC,
    )
    assert round(result, 5) == 0.41634


def test_solve_n():
    # EXACT_TEST + TWO_SIDED
    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.EXACT_TEST,
    )
    assert ceil(result) == 42

    # EXACT_TEST + ONE_SIDED
    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.ONE_SIDED,
        test_type=OSP.TestType.EXACT_TEST,
    )
    assert ceil(result) == 32

    # Z_TEST_USING_S_P0 + TWO_SIDED
    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_P0,
    )
    assert ceil(result) == 42

    # Z_TEST_USING_S_P0_CC + TWO_SIDED
    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_P0_CC,
    )
    assert ceil(result) == 49

    # Z_TEST_USING_S_PHAT + TWO_SIDED
    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_PHAT,
    )
    assert ceil(result) == 17

    # Z_TEST_USING_S_PHAT_CC + TWO_SIDED
    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_PHAT_CC,
    )
    assert ceil(result) == 23


def test_solve_alpha():
    result = OSP.solve(
        n=42,
        alpha=None,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.EXACT_TEST,
    )
    assert round(result, 2) == 0.05


def test_solve_power():
    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=None,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.EXACT_TEST,
    )
    assert round(result, 5) == 0.80598

    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=None,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.ONE_SIDED,
        test_type=OSP.TestType.EXACT_TEST,
    )
    assert round(result, 5) == 0.92528

    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=None,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_P0,
    )
    assert round(result, 5) == 0.80598

    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=None,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_P0_CC,
    )
    assert round(result, 5) == 0.69469

    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=None,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_PHAT,
    )
    assert round(result, 5) == 0.99380

    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=None,
        nullproportion=0.80,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_PHAT_CC,
    )
    assert round(result, 5) == 0.98408


def test_solve_nullproportion():
    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=0.80,
        nullproportion=None,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.EXACT_TEST,
        search_direction=OSP.SearchDirection.LOWER,
    )
    assert round(result, 2) == 0.80

    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=0.80,
        nullproportion=None,
        proportion=0.95,
        alternative=OSP.Alternative.TWO_SIDED,
        test_type=OSP.TestType.EXACT_TEST,
        search_direction=OSP.SearchDirection.UPPER,
    )
    assert round(result, 2) == 1.00


def test_solve_proportion():
    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=None,
        alternative=OSP.Alternative.ONE_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_P0_CC,
        search_direction=OSP.SearchDirection.LOWER,
    )
    assert round(result, 4) == 0.6237

    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=None,
        alternative=OSP.Alternative.ONE_SIDED,
        test_type=OSP.TestType.Z_TEST_USING_S_P0_CC,
        search_direction=OSP.SearchDirection.UPPER,
    )
    assert round(result, 4) == 0.9434


def test_param_string_competible():
    # alternative
    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative="two_sided",
        test_type="exact_test",
    )
    assert ceil(result) == 42

    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative="one_sided",
        test_type="exact_test",
    )
    assert ceil(result) == 32

    # test_type
    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative="two_sided",
        test_type="z_test_using_s_p0",
    )
    assert ceil(result) == 42

    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative="two_sided",
        test_type="z_test_using_s_p0_cc",
    )
    assert ceil(result) == 49

    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative="two_sided",
        test_type="z_test_using_s_phat",
    )
    assert ceil(result) == 17

    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative="two_sided",
        test_type="z_test_using_s_phat_cc",
    )
    assert ceil(result) == 23

    result = OSP.solve(
        n=None,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=0.95,
        alternative="two_sided",
        test_type="exact_test",
    )
    assert ceil(result) == 42

    # search_direction
    result = OSP.solve(
        n=42,
        alpha=0.05,
        power=0.80,
        nullproportion=0.80,
        proportion=None,
        alternative="one_sided",
        test_type="z_test_using_s_p0_cc",
        search_direction="lower",
    )
    assert round(result, 4) == 0.6237

    result = OSP.solve(
        n=56,
        alpha=0.05,
        power=0.80,
        nullproportion=None,
        proportion=0.95,
        alternative="two_sided",
        test_type="z_test_using_s_phat_cc",
        search_direction="lower",
    )
    assert round(result, 4) == 0.8595


def test_param_type_error():
    with pytest.raises(ParameterTypeError):
        OSP.solve(
            n="123",
            alpha=0.05,
            power=0.80,
            nullproportion=0.80,
            proportion=0.95,
            alternative="two_sided",
            test_type="exact_test",
        )

    with pytest.raises(ParameterTypeError):
        OSP.solve(
            n=None,
            alpha="0.05",
            power=0.80,
            nullproportion=0.80,
            proportion=0.95,
            alternative="two_sided",
            test_type="exact_test",
        )

    with pytest.raises(ParameterTypeError):
        OSP.solve(
            n=None,
            alpha=0.05,
            power="0.80",
            nullproportion=0.80,
            proportion=0.95,
            alternative="two_sided",
            test_type="exact_test",
        )

    with pytest.raises(ParameterTypeError):
        OSP.solve(
            n=None,
            alpha=0.05,
            power=0.80,
            nullproportion="0.80",
            proportion=0.95,
            alternative="two_sided",
            test_type="exact_test",
        )

    with pytest.raises(ParameterTypeError):
        OSP.solve(
            n=None,
            alpha=0.05,
            power=0.80,
            nullproportion=0.80,
            proportion="0.95",
            alternative="two_sided",
            test_type="exact_test",
        )

    with pytest.raises(ParameterTypeError):
        OSP.solve(
            n=None,
            alpha=0.05,
            power=0.80,
            nullproportion=0.80,
            proportion=0.95,
            alternative=123,
            test_type="exact_test",
        )

    with pytest.raises(ParameterTypeError):
        OSP.solve(
            n=None,
            alpha=0.05,
            power=0.80,
            nullproportion=0.80,
            proportion=0.95,
            alternative="two_sided",
            test_type=123,
        )

    with pytest.raises(ParameterTypeError):
        OSP.solve(
            n=None,
            alpha=0.05,
            power=0.80,
            nullproportion=0.80,
            proportion=0.95,
            alternative="two_sided",
            test_type="exact_test",
            search_direction=123,
        )

    with pytest.raises(ParameterTypeError):
        OSP.solve(
            n=None,
            alpha=0.05,
            power=0.80,
            nullproportion=0.80,
            proportion=0.95,
            alternative=123,
            test_type="exact_test",
        )


def test_param_value_empty_error():
    with pytest.raises(ParameterValueEmptyError):
        OSP.solve(
            n=42,
            alpha=0.05,
            power=0.80,
            nullproportion=0.80,
            proportion=None,
            alternative=OSP.Alternative.ONE_SIDED,
            test_type=OSP.TestType.Z_TEST_USING_S_P0_CC,
            search_direction=None,
        )


def test_enum_member_not_exist_error():
    with pytest.raises(EnumMemberNotExistError):
        OSP.solve(
            n=42,
            alpha=0.05,
            power=0.80,
            nullproportion=0.80,
            proportion=None,
            alternative="one_sided",
            test_type="z_test",
        )


def test_param_value_not_in_domain_error():
    with pytest.raises(ParameterValueNotInDomainError):
        OSP.solve(
            n=42,
            alpha=0.05,
            power=0.80,
            nullproportion=1.80,
            proportion=None,
            alternative="one_sided",
            test_type="z_test_using_s_p0_cc",
        )


def test_target_param_not_exist_error():
    with pytest.raises(TargetParameterNotExistError):
        OSP.solve(
            n=42,
            alpha=0.05,
            power=0.80,
            nullproportion=0.80,
            proportion=0.95,
            alternative="one_sided",
            test_type="z_test_using_s_p0_cc",
        )


def test_target_param_not_unique_error():
    with pytest.raises(TargetParameterNotUniqueError):
        OSP.solve(
            n=None,
            alpha=0.05,
            power=None,
            nullproportion=0.80,
            proportion=0.95,
            alternative="one_sided",
            test_type="z_test_using_s_p0_cc",
        )


def test_calculation_solution_not_found_error():
    with pytest.raises(CalculationSolutionNotFoundError):
        OSP.solve(
            n=42,
            alpha=0.05,
            power=0.80,
            nullproportion=None,
            proportion=0.95,
            alternative="one_sided",
            test_type="z_test_using_s_phat_cc",
            search_direction="upper",
        )
