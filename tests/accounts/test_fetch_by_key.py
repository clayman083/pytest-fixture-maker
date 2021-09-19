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
