# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

from dataclasses import asdict

import pytest

from .models import BaseTestCase


def generate_id(case: BaseTestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """
    This is a custom pytest hook which is called when collecting a test function, it can automatically finds `case_group` and inject parameters.

    Reference: https://docs.pytest.org/en/stable/how-to/parametrize.html#basic-pytest-generate-tests-example
    """

    if "case" in metafunc.fixturenames:
        case_group = getattr(metafunc.module, "case_group", None)
        if case_group is not None:
            metafunc.parametrize("case", case_group, ids=generate_id)


def pytest_configure(config: pytest.Config) -> None:
    """Mount the current OS information and Python version information to config"""

    config.is_linux = sys.platform == "linux"
    config.is_macos = sys.platform == "darwin"
    config.is_windows = sys.platform == "win32"

    config.is_py310 = sys.version_info[:2] == (3, 10)
    config.is_py311 = sys.version_info[:2] == (3, 11)
    config.is_py312 = sys.version_info[:2] == (3, 12)
    config.is_py313 = sys.version_info[:2] == (3, 13)
    config.is_py314 = sys.version_info[:2] == (3, 14)
