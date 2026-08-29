"""Characterization tests for the unsolved SDP-FND-080 renewal lab."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
import renewal_lab
from renewal_lab import (
    AuditPublisher,
    ChargeDecision,
    RenewalCommand,
    RenewalReceipt,
    renew_subscription,
)

FIXED_NOW = datetime(2026, 8, 29, 12, 30, tzinfo=UTC)


class FixedClock:
    """Stub: return one canned time."""

    def now(self) -> datetime:
        return FIXED_NOW


class GatewaySpy:
    """Stub plus call recording: control a decision and expose received requests."""

    def __init__(self, decision: ChargeDecision) -> None:
        self.decision = decision
        self.calls: list[dict[str, str | int]] = []

    def charge(self, **request: str | int) -> ChargeDecision:
        self.calls.append(request)
        return self.decision


class PublisherSpy(AuditPublisher):
    """Spy: record the observable audit boundary calls."""

    def __init__(self) -> None:
        self.published: list[RenewalReceipt] = []

    def publish(self, receipt: RenewalReceipt) -> None:
        self.published.append(receipt)


def install_hidden_collaborators(
    monkeypatch: pytest.MonkeyPatch,
    gateway: GatewaySpy,
    publisher: PublisherSpy,
) -> None:
    """Patch names at the current lookup site—the coupling the learner should remove."""

    monkeypatch.setattr(renewal_lab, "BillingGateway", lambda: gateway)
    monkeypatch.setattr(renewal_lab, "SystemClock", FixedClock)
    monkeypatch.setattr(renewal_lab, "AuditPublisher", lambda: publisher)


def test_approved_renewal_returns_and_publishes_a_stable_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gateway = GatewaySpy(ChargeDecision(True, provider_reference="pay-7"))
    publisher = PublisherSpy()
    install_hidden_collaborators(monkeypatch, gateway, publisher)
    command = RenewalCommand("req-42", "acct-7", 2_500, "tok_ok")

    receipt = renew_subscription(command)

    assert receipt == RenewalReceipt(
        "req-42",
        "acct-7",
        2_500,
        "renewed",
        FIXED_NOW,
        provider_reference="pay-7",
    )
    assert gateway.calls == [
        {
            "request_id": "req-42",
            "account_id": "acct-7",
            "amount_cents": 2_500,
            "payment_token": "tok_ok",
        }
    ]
    assert publisher.published == [receipt]


def test_decline_is_an_expected_result_not_an_infrastructure_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gateway = GatewaySpy(ChargeDecision(False, reason="insufficient funds"))
    publisher = PublisherSpy()
    install_hidden_collaborators(monkeypatch, gateway, publisher)

    receipt = renew_subscription(RenewalCommand("req-decline", "acct-8", 4_000, "tok_declined"))

    assert receipt.status == "declined"
    assert receipt.reason == "insufficient funds"
    assert receipt.provider_reference is None
    assert publisher.published == [receipt]


def test_repeating_a_request_recharges_because_the_ledger_lifetime_is_hidden(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gateway = GatewaySpy(ChargeDecision(True, provider_reference="pay-repeat"))
    publisher = PublisherSpy()
    install_hidden_collaborators(monkeypatch, gateway, publisher)
    command = RenewalCommand("req-repeat", "acct-9", 1_500, "tok_ok")

    first = renew_subscription(command)
    second = renew_subscription(command)

    assert first == second
    assert first is not second
    assert len(gateway.calls) == 2
    assert publisher.published == [first, second]


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        (
            {
                "request_id": "",
                "account_id": "acct-1",
                "amount_cents": 100,
                "payment_token": "tok_ok",
            },
            "request_id must not be blank",
        ),
        (
            {
                "request_id": "req-1",
                "account_id": " ",
                "amount_cents": 100,
                "payment_token": "tok_ok",
            },
            "account_id must not be blank",
        ),
        (
            {
                "request_id": "req-1",
                "account_id": "acct-1",
                "amount_cents": 0,
                "payment_token": "tok_ok",
            },
            "amount_cents must be positive",
        ),
        (
            {
                "request_id": "req-1",
                "account_id": "acct-1",
                "amount_cents": 100,
                "payment_token": " ",
            },
            "payment_token must not be blank",
        ),
    ],
)
def test_invalid_commands_fail_before_the_use_case(
    kwargs: dict[str, Any],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        RenewalCommand(**kwargs)


def test_approved_decision_needs_a_provider_reference() -> None:
    with pytest.raises(ValueError, match="an approved charge needs a provider reference"):
        ChargeDecision(True)


def test_receipt_rejects_naive_time() -> None:
    with pytest.raises(ValueError, match="recorded_at must be timezone-aware"):
        RenewalReceipt(
            "req-1",
            "acct-1",
            100,
            "renewed",
            datetime(2026, 8, 29),
            provider_reference="pay-1",
        )


def test_receipt_rejects_an_unknown_status_at_runtime() -> None:
    with pytest.raises(ValueError, match="unsupported renewal status: pending"):
        RenewalReceipt(
            "req-1",
            "acct-1",
            100,
            "pending",  # type: ignore[arg-type]
            FIXED_NOW,
            provider_reference="pay-1",
        )
