"""Observe a fake drifting from a production adapter's observable contract."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Protocol


class DuplicateEmailError(ValueError):
    """Application-level meaning shared by repository implementations."""


@dataclass(frozen=True)
class Account:
    account_id: str
    email: str


class AccountRepository(Protocol):
    def add(self, account: Account) -> None: ...

    def find_by_email(self, email: str) -> Account | None: ...


class SqliteAccountRepository:
    """Small real adapter whose uniqueness rule is case-insensitive."""

    def __init__(self) -> None:
        self._connection = sqlite3.connect(":memory:")
        self._connection.execute(
            """
            CREATE TABLE accounts (
                account_id TEXT PRIMARY KEY,
                email TEXT COLLATE NOCASE UNIQUE NOT NULL
            )
            """
        )

    def add(self, account: Account) -> None:
        try:
            self._connection.execute(
                "INSERT INTO accounts(account_id, email) VALUES (?, ?)",
                (account.account_id, account.email),
            )
            self._connection.commit()
        except sqlite3.IntegrityError as error:
            raise DuplicateEmailError(account.email) from error

    def find_by_email(self, email: str) -> Account | None:
        row = self._connection.execute(
            "SELECT account_id, email FROM accounts WHERE email = ?",
            (email,),
        ).fetchone()
        return None if row is None else Account(str(row[0]), str(row[1]))

    def close(self) -> None:
        self._connection.close()


class NaiveFakeAccountRepository:
    """Working shortcut that accidentally implements case-sensitive uniqueness."""

    def __init__(self) -> None:
        self._by_email: dict[str, Account] = {}

    def add(self, account: Account) -> None:
        if account.email in self._by_email:
            raise DuplicateEmailError(account.email)
        self._by_email[account.email] = account

    def find_by_email(self, email: str) -> Account | None:
        return self._by_email.get(email)


class ContractFaithfulFakeAccountRepository:
    """Still a shortcut, but it preserves the case-insensitive contract under test."""

    def __init__(self) -> None:
        self._by_email: dict[str, Account] = {}

    def add(self, account: Account) -> None:
        key = account.email.casefold()
        if key in self._by_email:
            raise DuplicateEmailError(account.email)
        self._by_email[key] = account

    def find_by_email(self, email: str) -> Account | None:
        return self._by_email.get(email.casefold())


def preserves_case_insensitive_email_contract(repository: AccountRepository) -> bool:
    """Run the same observable contract against any repository implementation."""

    original = Account("acct-1", "Rahul@Example.test")
    repository.add(original)
    if repository.find_by_email("rahul@example.test") != original:
        return False
    try:
        repository.add(Account("acct-2", "RAHUL@example.test"))
    except DuplicateEmailError:
        return True
    return False


def observe_fake_contract() -> dict[str, bool]:
    sqlite_repository = SqliteAccountRepository()
    try:
        sqlite_preserves_contract = preserves_case_insensitive_email_contract(sqlite_repository)
    finally:
        sqlite_repository.close()

    return {
        "sqlite_adapter": sqlite_preserves_contract,
        "naive_fake": preserves_case_insensitive_email_contract(NaiveFakeAccountRepository()),
        "contract_faithful_fake": preserves_case_insensitive_email_contract(
            ContractFaithfulFakeAccountRepository()
        ),
    }


def main() -> None:
    for name, result in observe_fake_contract().items():
        print(f"{name}={result}")


if __name__ == "__main__":
    main()
