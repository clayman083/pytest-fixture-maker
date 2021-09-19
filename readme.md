pytest-fixture-maker: Load fixture data from local YAML files.
============

[![Master](https://github.com/clayman083/pytest-fixture-maker/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/clayman083/pytest-fixture-maker/actions/workflows/main.yml)
<!-- [![Coverage Status](https://coveralls.io/repos/github/clayman74/pytest-postgres/badge.svg?branch=master)](https://coveralls.io/github/clayman74/pytest-postgres?branch=master) -->
[![PyPI version](https://badge.fury.io/py/pytest-fixture-maker.svg)](https://badge.fury.io/py/pytest-fixture-maker)
[![PyPI](https://img.shields.io/pypi/pyversions/pytest-fixture-maker.svg)]()

pytest-fixture-maker is a plugin for pytest, which load fixtures data from local YAML files.


Example file with fixtures:

    # fixtures/test_fetch_by_key.yml

    --- 

    test_fetch_by_key:
      storage: 
        accounts:
          - { key: 1, name: "Visa Classic" }
          - { key: 2, name: "Visa Gold"}

    test_success:
      - id: First test case
        account_key: 1
        expected: { key: 1, name: "Visa Classic" }
      - id: Second test case
        account_key: 2
        expected: { key: 2, name: "Visa Gold" }

    test_missing:
      - id: Try fetch missing account
        account_key: 3
        expected_exc: AccountNotFound


Example conftest.py file:

    # conftest.py

    from typing import Any

    import pytest

    from tests.accounts import Account, AccountRepo, Storage


    @pytest.fixture(scope="function")
    def account(request) -> Account:
        """Account entity."""
        return Account(**request.param)


    @pytest.fixture(scope="function")
    def storage(request) -> Storage:
        """Entity storage."""
        storage = Storage()

        if "accounts" in request.param:
            accounts = [Account(**account) for account in request.param["accounts"]]
            storage.accounts = AccountRepo(accounts=accounts)

        return storage


    @pytest.fixture(scope="function")
    def expected(request) -> Any:
        """Expected test case result."""
        return request.param


Example tests:

    from typing import Type

    import pytest

    from tests.accounts import Account, AccountNotFound, Storage


    @pytest.fixture
    def account_key(request) -> int:
        """Test account identifier."""
        return request.param


    @pytest.fixture
    def expected(request) -> Account:
        """Expected test case result."""
        return Account(**request.param)


    @pytest.mark.integration
    def test_success(storage: Storage, account_key: int, expected: Account) -> None:
        """Successful fetch account by key from storage."""
        result = storage.accounts.fetch_by_key(account_key)

        assert result == expected


    @pytest.fixture
    def expected_exc(request) -> Type[AccountNotFound]:
        """Expected exception when account not found in storage."""
        return AccountNotFound


    @pytest.mark.integration
    def test_missing(storage: Storage, account_key: int, expected_exc: Type[AccountNotFound]) -> None:
        """Try to fetch missing account by key from storage."""
        with pytest.raises(expected_exc):
            storage.accounts.fetch_by_key(account_key)


Installation
------------

To install pytest-fixture-maker, do:

    (env) $ python3 -m pip install pytest-fixture-maker


Changelog
---------

0.1.0 (2021-09-19)
~~~~~~~~~~~~~~~~~~
Initial release.
