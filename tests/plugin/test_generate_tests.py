from typing import Any, Dict

import pytest
from _pytest.python import Metafunc

from pytest_fixture_maker.plugin import generate_tests


@pytest.fixture()
def metafunc(mocker) -> Metafunc:
    """Fake metadata to generate parametrized calls to a test function."""
    fake_metafunc = mocker.Mock()

    fake_metafunc.module.__name__ = "tests.test_plugin"
    fake_metafunc.function.__name__ = "test_success"
    fake_metafunc.parametrize = mocker.Mock()

    return fake_metafunc


@pytest.mark.unit
@pytest.mark.parametrize(
    "fixtures", ({}, {"test_plugin": {"storage": {"user": {"id": 1, "name": "foo@bar.example.com"}}}})
)
def test_missing(metafunc, fixtures: Dict[str, Any]) -> None:
    """Test function not found among fixtures, don't parametrize."""
    generate_tests(metafunc, fixtures)  # act

    metafunc.parametrize.assert_not_called()


@pytest.mark.unit
@pytest.mark.parametrize(
    "fixturenames, fixtures, expected",
    (
        (
            ["foo"],
            {"test_success": [{"id": "First test case", "foo": "bar"}]},
            {"argnames": ["foo"], "argvalues": [["bar"]], "indirect": ["foo"], "ids": ["First test case"]},
        ),
        (
            ["foo", "storage"],
            {
                "test_plugin": {"storage": {"user": {"id": 1, "name": "foo@bar.example.com"}}},
                "test_success": [{"id": "First test case", "foo": "bar"}],
            },
            {
                "argnames": ["foo", "storage"],
                "argvalues": [["bar", {"user": {"id": 1, "name": "foo@bar.example.com"}}]],
                "indirect": ["foo", "storage"],
                "ids": ["First test case"],
            },
        ),
    ),
    ids=("wo_module_fixtures", "w_module_fixtures"),
)
def test_success(metafunc, fixturenames, fixtures, expected) -> None:
    """Parametrize test cases successfully."""
    metafunc.fixturenames = fixturenames

    generate_tests(metafunc, fixtures)  # act

    metafunc.parametrize.assert_called_once_with(**expected)


@pytest.mark.unit
@pytest.mark.parametrize(
    "fixtures, expected",
    (
        ({"test_success": {"id": "First test case", "foo": "bar"}}, "Test cases in `test_success` should be list"),
        (
            {"test_success": [{"id": "First test case", "foo": "bar"}, {"foo": "bar"}]},
            "Test case #2 in `test_success` should have id",
        ),
        (
            {"test_success": [{"id": "First test case", "foo": 1}, {"id": "Second test case", "bar": 2}]},
            "Test cases in `test_success` should have same arg names",
        ),
    ),
)
def test_failure(metafunc, fixtures: Dict[str, Any], expected: str) -> None:
    """Broken test cases for test func."""
    metafunc.fixturenames = ["foo"]

    with pytest.raises(ValueError) as excinfo:
        generate_tests(metafunc, fixtures)  # act

    assert expected in str(excinfo.value)
