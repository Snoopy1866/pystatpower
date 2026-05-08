from math import sqrt
from typing import Literal

from scipy.stats import nct, t


def _power_general(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alpha: float,
) -> float:
    df = treatment_size + reference_size - 2
    var_c = ((treatment_size - 1) * treatment_std**2 + (reference_size - 1) * reference_std**2) / df
    nc = (diff - margin) / sqrt(var_c * (1 / treatment_size + 1 / reference_size))

    if margin < 0:
        power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
    else:  # margin > 0
        power = nct.cdf(t.ppf(alpha, df), df, nc)

    return power


def _power_welch(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alpha: float,
) -> float:
    df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
        treatment_std**4 / (treatment_size**2 * (treatment_size + 1))
        + reference_std**4 / (reference_size**2 * (reference_size + 1))
    ) - 2
    nc = (diff - margin) / sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)

    if margin < 0:
        power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
    else:  # margin > 0
        power = nct.cdf(t.ppf(alpha, df), df, nc)

    return power


def _power_satterthwaite(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alpha: float,
) -> float:
    df = (treatment_std**2 / treatment_size + reference_std**2 / reference_size) ** 2 / (
        treatment_std**4 / (treatment_size**2 * (treatment_size - 1))
        + reference_std**4 / (reference_size**2 * (reference_size - 1))
    )
    nc = (diff - margin) / sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)

    if margin < 0:
        power = 1 - nct.cdf(t.ppf(1 - alpha, df), df, nc)
    else:  # margin > 0
        power = nct.cdf(t.ppf(alpha, df), df, nc)

    return power


def _power(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alpha: float,
    df_method: Literal["welch", "satterthwaite"],
) -> float:
    if treatment_std == reference_std:
        power = _power_general(diff, margin, treatment_std, reference_std, treatment_size, reference_size, alpha)
    else:
        match df_method:
            case "welch":
                power = _power_welch(
                    diff,
                    margin,
                    treatment_std,
                    reference_std,
                    treatment_size,
                    reference_size,
                    alpha,
                )
            case "satterthwaite":
                power = _power_satterthwaite(
                    diff,
                    margin,
                    treatment_std,
                    reference_std,
                    treatment_size,
                    reference_size,
                    alpha,
                )

    return power


def solve_power(
    *,
    treatment_mean: float | None = None,
    reference_mean: float | None = None,
    diff: float | None = None,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.025,
    df_method: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Calculate the power for a non-inferiority test of two independent means.

    Args:
        treatment_mean (float):
            Actual mean in the treatment group ($\\mu_1$).
        reference_mean (float):
            Actual mean in the reference group ($\\mu_2$).
        margin (float):
            The non-inferiority margin ($\\delta$)

            - Use a **negative value** if a higher proportion is better
            - Use a **positive value** if a lower proportion is better
        treatment_std (float):
            Actual standard deviation in the treatment group ($\\sigma_1$).
        reference_std (float):
            Actual standard deviation in the reference group ($\\sigma_2$).
        treatment_size (float):
            Sample size for the treatment group ($n_1$).
        reference_size (float):
            Sample size for the reference group ($n_2$).
        alpha (float, optional):
            One-sided significance level. Defaults to 0.025.
        df_method (Literal["welch", "satterthwaite"], optional):
            The approximation method for adjusting degrees of freedom when variances are unequal ($\\sigma_1 \\neq \\sigma_2$). Defaults to "welch".

    Returns:
        float: Power of the test.
    """

    if diff is None:
        if treatment_mean is not None and reference_mean is not None:
            actual_diff = treatment_mean - reference_mean
        else:
            raise ValueError("Either `diff` or `treatment_mean` and `reference_mean` must be provided.")
    else:
        actual_diff = diff
    return _power(
        actual_diff,
        margin,
        treatment_std,
        reference_std,
        treatment_size,
        reference_size,
        alpha,
        df_method,
    )
