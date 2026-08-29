"""Characterization and experiment tests for the unsolved SDP-FND-040 starter."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from quota_lab import OperationUsage, QuotaAccount, UsageReport, build_usage_report


def test_new_account_reports_full_quota() -> None:
    account = QuotaAccount("tenant-a", limit_units=100)

    assert account.used_units == 0
    assert account.remaining_units == 100
    assert account.usage_entries == []


def test_consumption_updates_current_observable_totals() -> None:
    account = QuotaAccount("tenant-a", limit_units=100)

    account.consume("generation", 25)
    account.consume("embedding", 10)

    assert account.used_units == 35
    assert account.remaining_units == 65
    assert account.usage_entries == [("generation", 25), ("embedding", 10)]


def test_report_groups_operations_in_deterministic_order() -> None:
    account = QuotaAccount("tenant-b", limit_units=200)
    account.consume("generation", 50)
    account.consume("embedding", 20)
    account.consume("generation", 30)

    report = build_usage_report(account)

    assert report == UsageReport(
        tenant_id="tenant-b",
        limit_units=200,
        used_units=100,
        remaining_units=100,
        by_operation=(
            OperationUsage("embedding", 20),
            OperationUsage("generation", 80),
        ),
    )


@pytest.mark.parametrize(
    ("tenant_id", "limit_units", "message"),
    [
        ("", 10, "tenant_id must not be blank"),
        ("   ", 10, "tenant_id must not be blank"),
        ("tenant-a", -1, "limit_units must be non-negative"),
    ],
)
def test_invalid_construction_is_currently_assertion_guarded(
    tenant_id: str,
    limit_units: int,
    message: str,
) -> None:
    with pytest.raises(AssertionError, match=message):
        QuotaAccount(tenant_id, limit_units)


@pytest.mark.parametrize(
    ("operation", "units", "message"),
    [
        ("", 1, "operation must not be blank"),
        ("   ", 1, "operation must not be blank"),
        ("generation", 0, "units must be positive"),
        ("generation", -1, "units must be positive"),
    ],
)
def test_invalid_consumption_is_currently_assertion_guarded(
    operation: str,
    units: int,
    message: str,
) -> None:
    account = QuotaAccount("tenant-a", limit_units=10)

    with pytest.raises(AssertionError, match=message):
        account.consume(operation, units)

    assert account.usage_entries == []


def test_over_limit_attempt_is_currently_rejected_without_mutation() -> None:
    account = QuotaAccount("tenant-a", limit_units=10)
    account.consume("generation", 8)
    before = list(account.usage_entries)

    with pytest.raises(AssertionError, match="quota exceeded"):
        account.consume("generation", 3)

    assert account.usage_entries == before
    assert account.remaining_units == 2


def test_public_ledger_can_bypass_rules_and_break_the_invariant() -> None:
    account = QuotaAccount("tenant-a", limit_units=10)

    account.usage_entries.append(("manual-corruption", -7))

    assert account.used_units == -7
    assert account.remaining_units == 17


def run_experiment(*interpreter_arguments: str) -> list[str]:
    """Run the experiment in a fresh interpreter and return output lines."""

    experiment = Path(__file__).with_name("assert_contract_experiment.py")
    completed = subprocess.run(
        [sys.executable, *interpreter_arguments, str(experiment)],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip().splitlines()


def test_assert_experiment_normal_mode_rejects_invalid_usage() -> None:
    assert run_experiment() == [
        "debug=True",
        "outcome=rejected:AssertionError",
        "used_units=0",
        "remaining_units=10",
    ]


def test_assert_experiment_optimized_mode_removes_required_guard() -> None:
    assert run_experiment("-O") == [
        "debug=False",
        "outcome=accepted",
        "used_units=-3",
        "remaining_units=13",
    ]
