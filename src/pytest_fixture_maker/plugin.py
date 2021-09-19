from pathlib import Path

import yaml


def get_module_fixtures(metafunc, fixtures):
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


def pytest_generate_tests(metafunc) -> None:
    """Pytest hook to generate parametrized calls to a test function.

    Args:
        metafunc: Metadata to generate parametrized calls to a test function.
    """
    module_path = Path(metafunc.module.__file__)
    fixture_file = module_path.parent / "fixtures" / f"{module_path.stem}.yml"

    if fixture_file.exists():
        with fixture_file.open("r") as fp:
            fixtures = yaml.safe_load(fp.read())

        module_fixtures = get_module_fixtures(metafunc, fixtures)

        if metafunc.function.__name__ in fixtures:
            scenario = fixtures[metafunc.function.__name__]
            for fixture in scenario:
                for fixture_name, fixture_value in module_fixtures.items():
                    fixture.setdefault(fixture_name, fixture_value)

            argnames = sorted(
                [argname for argname in scenario[0] if argname != "id" and argname in metafunc.fixturenames]
            )
            argvalues = [[funcargs[name] for name in argnames if name != "id"] for funcargs in scenario]

            indirect = [fixturename for fixturename in argnames if fixturename in metafunc.fixturenames]
            ids = [funcargs["id"] for funcargs in scenario]

        metafunc.parametrize(argnames, argvalues, indirect=indirect, ids=ids)
