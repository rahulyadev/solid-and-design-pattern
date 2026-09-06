"""Runtime observations that static interface declarations do not imply."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from interface_design import AuditEvent, DeliveryReceipt


@runtime_checkable
class RuntimeChannel(Protocol):
    def deliver(self, event: AuditEvent, *, idempotency_key: str) -> DeliveryReceipt: ...


class WrongSignatureChannel:
    """Has the required name, but not the required call or result contract."""

    def deliver(self) -> str:
        return "not a receipt"


def observe_runtime_protocol() -> tuple[bool, str]:
    candidate = WrongSignatureChannel()
    recognized = isinstance(candidate, RuntimeChannel)

    try:
        candidate.deliver(  # type: ignore[call-arg]
            AuditEvent("evt-1", "invoice.created", "amount=2500"),
            idempotency_key="req-1",
        )
    except TypeError as error:
        failure = type(error).__name__
    else:  # pragma: no cover - documents the expected failure branch
        failure = "no failure"

    return recognized, failure


def main() -> None:
    recognized, failure = observe_runtime_protocol()
    print(f"runtime protocol recognized wrong signature: {recognized}")
    print(f"real call result: {failure}")


if __name__ == "__main__":
    main()
