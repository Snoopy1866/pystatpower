import pytest

from dataclasses import asdict

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
