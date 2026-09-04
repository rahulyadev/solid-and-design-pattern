"""Runnable legacy notification router for the independent SDP-PYT-020 lab.

This is deliberately an if/elif design. It preserves a small existing contract;
it is not the target registry implementation.
"""

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    recipient: str
    body: str


def _email_receipt(notification: Notification) -> str:
    return f"email:{notification.recipient}:{notification.body}"


def _sms_receipt(notification: Notification) -> str:
    return f"sms:{notification.recipient}:{notification.body}"


def route_notifications(
    notifications: Iterable[Notification],
    channel: str,
) -> tuple[str, ...]:
    """Return synthetic receipts in order; reject unknown channels before iteration."""

    if channel not in {"email", "sms"}:
        raise ValueError(f"unsupported channel: {channel}")

    receipts: list[str] = []
    for notification in notifications:
        if channel == "email":
            receipt = _email_receipt(notification)
        elif channel == "sms":
            receipt = _sms_receipt(notification)
        else:  # pragma: no cover - guarded above; retained to show the branching shape
            raise AssertionError("validated channel became unsupported")
        receipts.append(receipt)
    return tuple(receipts)


def main() -> None:
    sample = (
        Notification("learner@example.test", "review ready"),
        Notification("+10000000000", "build finished"),
    )
    print(route_notifications(sample, "email"))
    print(route_notifications(sample, "sms"))


if __name__ == "__main__":
    main()
