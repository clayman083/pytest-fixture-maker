from typing import Any, Dict

import pytest

from pytest_fixture_maker.plugin import get_module_fixtures


@pytest.fixture()
def metafunc(mocker):
    """Fake metadata to generate parametrized calls to a test function."""
    fake_metafunc = mocker.Mock()

    fake_metafunc.function = mocker.Mock()
    fake_metafunc.function.__name__ = mocker.Mock(new_callable=mocker.PropertyMock, return_value="test_success")

    fake_metafunc.module = mocker.MagicMock()
    fake_metafunc.module.__name__ = mocker.Mock(new_callable=mocker.PropertyMock, return_value="tests.test_plugin")

    return fake_metafunc


@pytest.mark.unit
@pytest.mark.parametrize("raw_fixtures, expected", (({}, {}),))
def test_get_module_fixtures(metafunc, raw_fixtures: Dict[str, Any], expected: Dict[str, Any]) -> None:
    """Successful test get module-level fixtures."""
    result = get_module_fixtures(metafunc, raw_fixtures)

    assert result == expected
