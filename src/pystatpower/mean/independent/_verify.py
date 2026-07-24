# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Literal


def _verify_mean_and_get_diff(
    treatment_mean: float | None,
    reference_mean: float | None,
    diff: float | None,
) -> float:

    if diff is None:
        if treatment_mean is None or reference_mean is None:
            msg = "When 'diff' is omitted, both 'treatment_mean' and 'reference_mean' must be provided."
            raise ValueError(msg)
        diff = treatment_mean - reference_mean

    return diff


def _verify_std_and_get_std(
    treatment_std: float | None,
    reference_std: float | None,
    std: float | None,
    dist: Literal["z", "t"],
    equal_var: bool,
) -> float:

    if dist == "z":
        if equal_var:
            if std is None:
                if treatment_std is None and reference_std is None:
                    msg = "For z-test with equal variance, at least one of 'std', 'treatment_std', or 'reference_std' is required."
                    raise ValueError(msg)
                elif treatment_std is not None and reference_std is not None:
                    if treatment_std != reference_std:
                        msg = "For z-test with equal variance, if 'std' is omitted and you provide both 'treatment_std' and 'reference_std', they must be equal."
                        raise ValueError(msg)
                    else:  # treatment_std == reference_std
                        std = treatment_std
                elif treatment_std is None and reference_std is not None:
                    std = reference_std
                else:  # treatment_std is not None and reference_std is None:
                    std = treatment_std
        else:  # equal_var == False
            if treatment_std is None or reference_std is None:
                msg = "For z-test with unequal variance, both 'treatment_std' and 'reference_std' is required."
                raise ValueError(msg)
    else:  # dist == "t"
        if treatment_std is None or reference_std is None:
            msg = "For t-test, both 'treatment_std' and 'reference_std' is required."
            raise ValueError(msg)

    return std
