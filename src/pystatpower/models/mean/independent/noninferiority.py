from math import sqrt
from typing import Literal

from scipy.stats import nct, norm, t


def _power_z_equal_var(
    diff: float,
    margin: float,
    std: float,
    treatment_size: float,
    reference_size: float,
    alpha: float,
) -> float:
    power = 1 - norm.cdf(
        norm.ppf(1 - alpha) - abs(diff - margin) / (std * sqrt(1 / treatment_size + 1 / reference_size))
    )
    return float(power)


def _power_z_unequal_var(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alpha: float,
) -> float:
    power = 1 - norm.cdf(
        norm.ppf(1 - alpha)
        - abs(diff - margin) / sqrt(treatment_std**2 / treatment_size + reference_std**2 / reference_size)
    )
    return float(power)


def _power_t(
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
    method: Literal["z", "t"],
    equal_var: bool,
    df_adjust: Literal["welch", "satterthwaite"],
) -> float:
    match method:
        case "z":
            if equal_var:
                assert treatment_std == reference_std
                std = treatment_std
                power = _power_z_equal_var(diff, margin, std, treatment_size, reference_size, alpha)
            else:
                power = _power_z_unequal_var(
                    diff, margin, treatment_std, reference_std, treatment_size, reference_size, alpha
                )
        case "t":
            if equal_var:
                power = _power_t(diff, margin, treatment_std, reference_std, treatment_size, reference_size, alpha)
            else:
                match df_adjust:
                    case "welch":
                        power = _power_welch(
                            diff, margin, treatment_std, reference_std, treatment_size, reference_size, alpha
                        )
                    case "satterthwaite":
                        power = _power_satterthwaite(
                            diff, margin, treatment_std, reference_std, treatment_size, reference_size, alpha
                        )

    return power


def solve_power(
    diff: float,
    margin: float,
    treatment_std: float,
    reference_std: float,
    treatment_size: float,
    reference_size: float,
    alpha: float = 0.025,
    method: Literal["z", "t"] = "t",
    equal_var: bool = False,
    df_adjust: Literal["welch", "satterthwaite"] = "welch",
) -> float:
    """
    Calculate the statistical power for a non-inferiority test of two independent means.

    Args:
        diff (float):
            Mean difference between treatment and reference group ($\\mu_1 - \\mu_2$).
        margin (float):
            The non-inferiority margin ($\\delta$)

            - Use a **negative** value if a higher mean indicates a better outcome
            - Use a **positive** value if a lower mean indicates a better outcome
        treatment_std (float):
            Standard deviation in the treatment group ($\\sigma_1$).
        reference_std (float):
            Standard deviation in the reference group ($\\sigma_2$).
        treatment_size (float):
            Sample size for the treatment group ($n_1$).
        reference_size (float):
            Sample size for the reference group ($n_2$).
        alpha (float, optional):
            One-sided significance level. Defaults to 0.025.
        method (Literal["z", "t"], optional):
            The distribution used for the test.

            - "z": Standard normal distribution (large sample approximation).
            - "t": Student's or non-central t distribution.

            Defaults to "t".
        equal_var (bool, optional):
            Whether to assume equal variances between groups.

            - If **True**: Assume $\\sigma_1^2 = \\sigma_2^2$. Use *Pooled Variance* to calculate SE.
              If `method="t"`, degree of freedom $df = n_1 + n_2 - 2$.

            - If **False**: Assume $\\sigma_1^2 \\neq \\sigma_2^2$. Use *Unpooled Variance* to calculate SE.
              If `method="t"`, the degree of freedom is adjusted based on the `df_adjust` parameter.

            Defaults to False.

            If Z test is used and `equal_var` is True, the standard deviation of the two groups must be equal.
        df_adjust (Literal["welch", "satterthwaite"], optional):
            Degree of freedom adjustment method when `method="t"` and `equal_var=False`.

            - "welch": Adjustment based on Welch (1947).
            - "satterthwaite": Adjustment based on Satterthwaite (1946).

            Defaults to "welch".

    Returns:
        float: The calculated power of the test.

    Raises:
        ValueError: If `method="z"` and `equal=True` but `treatment_std` does not equal `reference_std`.
    """

    if method == "z" and equal_var and treatment_std != reference_std:
        raise ValueError("If method='z' and equal_var=True, treatment_std must equal reference_std.")

    power = _power(
        diff, margin, treatment_std, reference_std, treatment_size, reference_size, alpha, method, equal_var, df_adjust
    )
    return power
