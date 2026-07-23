from math import ceil
from math import sqrt
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import t


def _precision(
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    conf_level: float,
    interval_type: Literal["two-sided", "lower", "upper"],
    equal_var: bool,
) -> float:
    """Calculate the distance from the mean difference to the confidence limit."""

    alpha = 1 - conf_level

    if equal_var:
        df = treatment_size + reference_size - 2
        se = sqrt(
            ((treatment_size - 1) * treatment_std**2 + (reference_size - 1) * reference_std**2)
            / df
            * (1 / treatment_size + 1 / reference_size)
        )
    else:  # unequal std
        df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
            treatment_std**4 / (treatment_size**2 * (treatment_size - 1))
            + reference_std**4 / (reference_size**2 * (reference_size - 1))
        )
        se = sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)

    match interval_type:
        case "two-sided":
            prcision = t.ppf(1 - alpha / 2, df) * se
        case "lower":
            prcision = t.ppf(1 - alpha, df) * se
        case "upper":
            prcision = t.ppf(1 - alpha, df) * se

    return float(prcision)


def solve_precision(
    *,
    treatment_std: float,
    reference_std: float,
    treatment_size: int,
    reference_size: int,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    equal_var: bool = False,
) -> float:
    """
    Calculate the distance from the mean difference to the confidence limit.

    Args:
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        treatment_size:
            Sample size in the treatment group.
        reference_size:
            Sample size in the reference group.
        conf_level:
            Confidence level.
        interval_type:
            The type of confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        equal_var:
            Specify whether the variances are assumed to be equal.

            - `True`: The variances are assumed to be equal. In this case, the standard t-test is used.
            - `False`: The variances are not assumed to be equal. In this case, Welch-Satterthwaite's approximate t-test is used.

    Returns:
        The distance from the mean difference to the confidence limit.
    """

    return _precision(
        treatment_std, reference_std, treatment_size, reference_size, conf_level, interval_type, equal_var
    )


def solve_size(
    *,
    treatment_std: float,
    reference_std: float,
    precision: float,
    ratio: float = 1,
    conf_level: float = 0.95,
    interval_type: Literal["two-sided", "lower", "upper"] = "two-sided",
    equal_var: bool = False,
) -> tuple[int, int]:
    """
    Estimate the required sample size.

    Args:
        treatment_std:
            Standard deviation in the treatment group.
        reference_std:
            Standard deviation in the reference group.
        precision:
            The distance from the mean difference to the confidence limit.
        ratio:
            The ratio of the sample size in the treatment group to the sample size in the reference group.
        conf_level:
            Confidence level.
        interval_type:
            The type of confidence interval.

            - `'two-sided'`: Two-sided confidence interval.
            - `'lower'`: Lower one-sided confidence interval.
            - `'upper'`: Upper one-sided confidence interval.
        equal_var:
            Specify whether the variances are assumed to be equal.

            - `True`: The variances are assumed to be equal. In this case, the standard t-test is used.
            - `False`: The variances are not assumed to be equal. In this case, Welch-Satterthwaite's approximate t-test is used.

    Returns:
        The required sample sizes in the treatment and reference groups, respectively.
    """

    if ratio >= 1:

        def func(reference_size: float) -> float:
            return (
                _precision(
                    treatment_std,
                    reference_std,
                    reference_size * ratio,
                    reference_size,
                    conf_level,
                    interval_type,
                    equal_var,
                )
                - precision
            )

        reference_size = ceil(brentq(func, 1, 1e12))
        treatment_size = ceil(reference_size * ratio)
    else:  # ratio < 1

        def func(treatment_size: float) -> float:
            return (
                _precision(
                    treatment_size,
                    treatment_size / ratio,
                    treatment_std,
                    reference_std,
                    conf_level,
                    interval_type,
                    equal_var,
                )
                - precision
            )

        treatment_size = ceil(brentq(func, 1, 1e12))
        reference_size = ceil(treatment_size / ratio)

    return treatment_size, reference_size
