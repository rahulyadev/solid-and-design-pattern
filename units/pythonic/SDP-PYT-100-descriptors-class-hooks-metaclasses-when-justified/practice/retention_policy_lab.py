"""Unsolved baseline for choosing the least powerful class mechanism."""

from __future__ import annotations

from dataclasses import dataclass


class UnknownPolicyError(LookupError):
    """A requested retention policy does not exist."""


@dataclass(frozen=True)
class RetentionPolicy:
    name: str
    days: int


def build_policy(name: str, days: int) -> RetentionPolicy:
    normalized_name = name.strip().lower()
    if not normalized_name:
        raise ValueError("name must not be blank")
    if isinstance(days, bool) or not isinstance(days, int):
        raise TypeError("days must be an int but not bool")
    if not 1 <= days <= 3650:
        raise ValueError("days must be between 1 and 3650")
    return RetentionPolicy(normalized_name, days)


def choose_policy(
    requested_name: str,
    policies: tuple[RetentionPolicy, ...],
) -> RetentionPolicy:
    normalized_name = requested_name.strip().lower()
    matches = [policy for policy in policies if policy.name == normalized_name]
    if len(matches) != 1:
        raise UnknownPolicyError(f"unknown retention policy: {requested_name!r}")
    return matches[0]


def main() -> None:
    policies = (
        build_policy(" standard ", 30),
        build_policy("archive", 365),
    )
    selected = choose_policy("STANDARD", policies)
    print(f"selected={selected.name}; days={selected.days}")


if __name__ == "__main__":
    main()
