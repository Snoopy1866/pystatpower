"""两独立样本差异性检验"""

from enum import Enum


class Alternative(Enum):
    """假设检验的备择假设类型"""

    ONE_SIDED = 1
    TWO_SIDED = 2


class TestType(Enum):
    """检验类型"""

    Z_TEST_POOLED = 1
    Z_TEST_UNPOOLED = 2
    Z_TEST_CC_POOLED = 3
    Z_TEST_CC_UNPOOLED = 4


class GroupAllocation(Enum):
    """样本量分配方式"""

    EQUAL = 1
    FIX_TREATMENT_GROUP = 2
    FIX_REFERENCE_GROUP = 3
    RATIO_OF_TREATMENT_TO_REFERENCE = 4
    RATIO_OF_REFERENCE_TO_TREATMENT = 5
    PERCENT_OF_TREATMENT = 6
    PERCENT_OF_REFERENCE = 7


class TwoProportionDesigner:
    def __init__(self, solve_for: str):
        if not isinstance(solve_for, str):
            raise TypeError("solve_for must be a string")

        self._solve_for = solve_for.lower()
        if self._solve_for not in ["n", "alpha", "power", "treatment_proportion", "reference_proportion"]:
            raise ValueError(
                "solve_for must be either 'n', 'alpha', 'power', 'treatment_proportion', or 'reference_proportion'"
            )
        match self._solve_for:
            case "n":
                return TwoProportionSolveForNDesigner()
            case "alpha":
                return TwoProportionSolveForAlphaDesigner()
            case "power":
                return TwoProportionSolveForPowerDesigner()
            case "treatment_proportion":
                return TwoProportionSolveForTreatmentProportionDesigner()
            case "reference_proportion":
                return TwoProportionSolveForReferenceProportionDesigner()


class TwoProportionSolveForNDesigner(TwoProportionDesigner):

    def __init__(self):
        self._config = {}

    def set_alpha(self, alpha: float = 0.05):
        self._config["alpha"] = alpha
        return self

    def set_power(self, power: float = 0.80):
        self._config["power"] = power
        return self

    def set_alternative(self, alternative: Alternative = Alternative.TWO_SIDED):
        self._config["alternative"] = alternative
        return self

    def set_test_type(self, test_type: TestType = TestType.Z_TEST_POOLED):
        self._config["test_type"] = test_type
        return self

    def set_treatment_proportion(self, treatment_proportion: float):
        self._config["treatment_proportion"] = treatment_proportion
        return self

    def set_reference_proportion(self, reference_proportion: float):
        self._config["reference_proportion"] = reference_proportion
        return self

    def set_group_allocation(self, group_allocation: GroupAllocation = GroupAllocation.EQUAL):
        match group_allocation:
            case GroupAllocation.EQUAL:
                pass
            case GroupAllocation.FIX_TREATMENT_GROUP:
                pass
            case GroupAllocation.FIX_REFERENCE_GROUP:
                pass
            case GroupAllocation.RATIO_OF_TREATMENT_TO_REFERENCE:
                pass
            case GroupAllocation.RATIO_OF_REFERENCE_TO_TREATMENT:
                pass
            case GroupAllocation.PERCENT_OF_TREATMENT:
                pass
            case GroupAllocation.PERCENT_OF_REFERENCE:
                pass
        return self

    def set_input_type(self, input_type):
        raise NotImplementedError("这个功能还没有实现")


class TwoProportionSolveForAlphaDesigner:
    pass


class TwoProportionSolveForPowerDesigner:
    pass


class TwoProportionSolveForTreatmentProportionDesigner:
    pass


class TwoProportionSolveForReferenceProportionDesigner:
    pass
