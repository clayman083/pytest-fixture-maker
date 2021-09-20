from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from _pytest.python import Metafunc


def get_module_fixtures(metafunc: Metafunc, fixtures: Dict[str, Any]) -> Dict[str, Any]:
    """Get data for module-level fixtures.

    Args:
        metafunc: Metadata to generate parametrized calls to a test function.
        fixtures: Raw fixtures data from file.

    Returns:
        Raw data for module-level fixtures.
    """
    module_fixtures = {}

    module_name = metafunc.module.__name__
    if "." in metafunc.module.__name__:
        module_name = metafunc.module.__name__.split(".")[-1]

    if module_name in fixtures:
        module_fixtures = fixtures[module_name]

    return module_fixtures


def get_test_cases(
    metafunc: Metafunc, fixtures: Dict[str, Any], module_fixtures: Dict[str, Any]
) -> Optional[List[Dict[str, Any]]]:
    """Get test cases from fixtures.

    Args:
        metafunc: Metadata to generate parametrized calls to a test function.
        fixtures: Raw fixtures data from file.
        module_fixtures: Module-level fixtures.

    Returns:
        Raw test cases.
    """
    func_fixtures = None

    if metafunc.function.__name__ in fixtures:
        func_fixtures = fixtures[metafunc.function.__name__]

        if not isinstance(func_fixtures, list):
            raise ValueError(f"Test cases in `{metafunc.function.__name__}` should be list")

        for fixture in func_fixtures:
            for fixture_name, fixture_value in module_fixtures.items():
                fixture.setdefault(fixture_name, fixture_value)

    return func_fixtures


def generate_tests(metafunc: Metafunc, fixtures: Dict[str, Any]) -> None:
    """Generate tests for test cases.

    Args:
        metafunc: Metadata to generate parametrized calls to a test function.
        fixtures: Raw fixtures data from file.
    """
    module_fixtures = get_module_fixtures(metafunc, fixtures)
    test_cases = get_test_cases(metafunc, fixtures, module_fixtures)

    if test_cases:
        argnames: List[str] = []
        argvalues: List[List[Any]] = []
        indirect: List[str] = []
        ids: List[str] = []

        for index, test_case in enumerate(test_cases, start=1):
            if "id" in test_case:
                ids.append(test_case["id"])
            else:
                raise ValueError(f"Test case #{index} in `{metafunc.function.__name__}` should have id")

            if not argnames:
                argnames = sorted(
                    [argname for argname in test_case if argname != "id" and argname in metafunc.fixturenames]
                )
                indirect = [argname for argname in argnames if argname in metafunc.fixturenames]

            values = []
            for name in argnames:
                if name not in test_case:
                    raise ValueError(f"Test cases in `{metafunc.function.__name__}` should have same arg names")

                values.append(test_case[name])

            argvalues.append(values)

        metafunc.parametrize(argnames=argnames, argvalues=argvalues, indirect=indirect, ids=ids)


def pytest_generate_tests(metafunc: Metafunc) -> None:
    """Pytest hook to generate parametrized calls to a test function.

    Args:
        metafunc: Metadata to generate parametrized calls to a test function.
    """
    module_path = Path(metafunc.module.__file__)
    fixture_file = module_path.parent / "fixtures" / f"{module_path.stem}.yml"

    if fixture_file.exists():
        with fixture_file.open("r") as fp:
            fixtures = yaml.safe_load(fp.read())

        generate_tests(metafunc, fixtures)
