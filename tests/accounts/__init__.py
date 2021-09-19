from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Account:
    """Account entity."""

    key: int
    name: str


class AccountNotFound(Exception):
    """Account entity not found."""

    def __init__(self, key: int) -> None:
        self._key = key

    @property
    def key(self) -> int:
        """Account entity key."""
        return self._key


class AccountRepo:
    """Repo to work with accounts."""

    _accounts: List[Account]

    def __init__(self, accounts: Optional[List[Account]] = None) -> None:
        self._accounts = accounts or []

    def fetch_by_key(self, key: int) -> Account:
        """Fetch account by key.

        Args:
            key: Account identifier.

        Returns:
            Account entity.
        """
        for account in self._accounts:
            if account.key == key:
                return account
        else:
            raise AccountNotFound(key=key)


class Storage:
    """Storage for entities."""

    def __init__(self) -> None:
        self.accounts = AccountRepo()
