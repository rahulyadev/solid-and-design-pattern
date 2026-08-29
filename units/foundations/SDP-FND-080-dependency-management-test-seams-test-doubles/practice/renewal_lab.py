"""Unsolved SDP-FND-080 lab: make renewal dependencies explicit.

The module is intentionally executable and deterministic apart from the system clock. Its
application function constructs concrete collaborators internally. That is the design pressure
for the learner to refactor; it is not the recommended final design.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal

RenewalStatus = Literal["renewed", "declined"]


@dataclass(frozen=True)
class RenewalCommand:
    """A validated request to renew one account once."""

    request_id: str
    account_id: str
    amount_cents: int
    payment_token: str

    def __post_init__(self) -> None:
        for field_name in ("request_id", "account_id", "payment_token"):
            value = getattr(self, field_name)
            if not value.strip():
                raise ValueError(f"{field_name} must not be blank")
        if self.amount_cents <= 0:
            raise ValueError("amount_cents must be positive")


@dataclass(frozen=True)
class ChargeDecision:
    """The gateway result translated into application language."""

    approved: bool
    provider_reference: str | None = None
    reason: str | None = None

    def __post_init__(self) -> None:
        reference = self.provider_reference
        reason = self.reason
        if self.approved and (reference is None or not reference.strip()):
            raise ValueError("an approved charge needs a provider reference")
        if self.approved and reason is not None:
            raise ValueError("an approved charge must not contain a decline reason")
        if not self.approved and reference is not None:
            raise ValueError("a declined charge must not contain a provider reference")
        if not self.approved and (reason is None or not reason.strip()):
            raise ValueError("a declined charge needs a reason")


@dataclass(frozen=True)
class RenewalReceipt:
    """Observable result saved by the application boundary."""

    request_id: str
    account_id: str
    amount_cents: int
    status: RenewalStatus
    recorded_at: datetime
    provider_reference: str | None = None
    reason: str | None = None

    def __post_init__(self) -> None:
        if self.recorded_at.tzinfo is None:
            raise ValueError("recorded_at must be timezone-aware")
        if self.status not in ("renewed", "declined"):
            raise ValueError(f"unsupported renewal status: {self.status}")
        if self.status == "renewed":
            ChargeDecision(True, self.provider_reference, self.reason)
        else:
            ChargeDecision(False, self.provider_reference, self.reason)


class SystemClock:
    """Production-style adapter for wall-clock time."""

    def now(self) -> datetime:
        return datetime.now(UTC)


class BillingGateway:
    """Synthetic provider adapter; a real adapter would perform network I/O."""

    def charge(
        self,
        *,
        request_id: str,
        account_id: str,
        amount_cents: int,
        payment_token: str,
    ) -> ChargeDecision:
        del account_id, amount_cents
        if payment_token == "tok_declined":
            return ChargeDecision(False, reason="card declined")
        return ChargeDecision(True, provider_reference=f"charge:{request_id}")


class RenewalLedger:
    """A deliberately short-lived store created inside each use-case call."""

    def __init__(self) -> None:
        self._receipts: dict[str, RenewalReceipt] = {}

    def find(self, request_id: str) -> RenewalReceipt | None:
        return self._receipts.get(request_id)

    def save(self, receipt: RenewalReceipt) -> None:
        self._receipts[receipt.request_id] = receipt


class AuditPublisher:
    """Synthetic outgoing boundary; production would publish an audit event."""

    def publish(self, receipt: RenewalReceipt) -> None:
        del receipt


def renew_subscription(command: RenewalCommand) -> RenewalReceipt:
    """Renew once, while hiding construction and lifetime decisions inside the use case."""

    ledger = RenewalLedger()
    existing = ledger.find(command.request_id)
    if existing is not None:
        return existing

    decision = BillingGateway().charge(
        request_id=command.request_id,
        account_id=command.account_id,
        amount_cents=command.amount_cents,
        payment_token=command.payment_token,
    )
    recorded_at = SystemClock().now()
    status: RenewalStatus = "renewed" if decision.approved else "declined"
    receipt = RenewalReceipt(
        request_id=command.request_id,
        account_id=command.account_id,
        amount_cents=command.amount_cents,
        status=status,
        recorded_at=recorded_at,
        provider_reference=decision.provider_reference,
        reason=decision.reason,
    )
    ledger.save(receipt)
    AuditPublisher().publish(receipt)
    return receipt


def main() -> None:
    """Show the stable behavior and the hidden-lifetime idempotency defect."""

    command = RenewalCommand("req-42", "acct-7", 2_500, "tok_ok")
    first = renew_subscription(command)
    second = renew_subscription(command)
    print(f"first={first.status}:{first.provider_reference}")
    print(f"second={second.status}:{second.provider_reference}")
    print(f"same_receipt_object={first is second}")


if __name__ == "__main__":
    main()
