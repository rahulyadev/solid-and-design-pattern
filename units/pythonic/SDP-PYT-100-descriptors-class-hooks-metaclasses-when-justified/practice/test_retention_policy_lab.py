"""Behavior protection for the unsolved retention-policy starter."""

from __future__ import annotations

import pytest
from retention_policy_lab import (
    RetentionPolicy,
    UnknownPolicyError,
    build_policy,
    choose_policy,
)


@pytest.fixture
def policies() -> tuple[RetentionPolicy, ...]:
    return (
        build_policy("standard", 30),
        build_policy("archive", 365),
    )


def test_build_policy_normalizes_name() -> None:
    assert build_policy(" Standard ", 30) == RetentionPolicy("standard", 30)


@pytest.mark.parametrize("name", ["", "   "])
def test_blank_name_is_rejected(name: str) -> None:
    with pytest.raises(ValueError, match="must not be blank"):
        build_policy(name, 30)


@pytest.mark.parametrize("days", [1, 3650])
def test_boundary_days_are_accepted(days: int) -> None:
    assert build_policy("archive", days).days == days


@pytest.mark.parametrize("days", [0, 3651])
def test_out_of_range_days_are_rejected(days: int) -> None:
    with pytest.raises(ValueError, match="between 1 and 3650"):
        build_policy("archive", days)


@pytest.mark.parametrize("days", [True, 30.0, "30"])
def test_non_integer_or_boolean_days_are_rejected(days: object) -> None:
    with pytest.raises(TypeError, match="int but not bool"):
        build_policy("archive", days)  # type: ignore[arg-type]


def test_choose_policy_normalizes_request(
    policies: tuple[RetentionPolicy, ...],
) -> None:
    assert choose_policy(" STANDARD ", policies).days == 30


def test_unknown_policy_keeps_requested_name(
    policies: tuple[RetentionPolicy, ...],
) -> None:
    with pytest.raises(UnknownPolicyError, match="missing"):
        choose_policy("missing", policies)


def test_duplicate_policy_is_ambiguous() -> None:
    duplicated = (
        build_policy("standard", 30),
        build_policy("standard", 60),
    )

    with pytest.raises(UnknownPolicyError, match="standard"):
        choose_policy("standard", duplicated)


def test_input_collection_is_not_mutated(
    policies: tuple[RetentionPolicy, ...],
) -> None:
    before = tuple(policies)

    choose_policy("archive", policies)

    assert policies == before


def test_unicode_name_is_preserved_after_case_normalization() -> None:
    policy = build_policy(" संग्रह ", 90)

    assert policy.name == "संग्रह"
