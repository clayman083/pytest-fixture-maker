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
