"""Unsolved SDP-FND-050 starter that inherits only to reuse a transport implementation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Customer:
    """A synthetic subscription customer used by the practice scenario."""

    customer_id: str
    name: str
    phone: str

    def __post_init__(self) -> None:
        if not self.customer_id.strip():
            raise ValueError("customer_id must not be blank")
        if not self.name.strip():
            raise ValueError("name must not be blank")
        if not self.phone.strip():
            raise ValueError("phone must not be blank")


@dataclass(frozen=True, slots=True)
class SentMessage:
    """One transport-level message recorded by the deterministic fake gateway."""

    message_id: str
    sender_id: str
    recipient: str
    body: str


@dataclass(frozen=True, slots=True)
class ReminderReceipt:
    """The business-facing result of sending one renewal reminder."""

    customer_id: str
    message_id: str
    channel: str
    body: str


class SmsGateway:
    """A deterministic stand-in for a vendor SDK transport client."""

    def __init__(self, sender_id: str) -> None:
        if not sender_id.strip():
            raise ValueError("sender_id must not be blank")
        self.sender_id = sender_id
        self._sent_messages: list[SentMessage] = []

    @property
    def sent_messages(self) -> tuple[SentMessage, ...]:
        """Return the currently recorded transport calls."""

        return tuple(self._sent_messages)

    def send_message(self, recipient: str, body: str) -> str:
        """Record a transport call and return a deterministic message ID."""

        if not recipient.strip():
            raise ValueError("recipient must not be blank")
        if not body.strip():
            raise ValueError("body must not be blank")

        message_id = f"msg-{len(self._sent_messages) + 1:03d}"
        self._sent_messages.append(
            SentMessage(
                message_id=message_id,
                sender_id=self.sender_id,
                recipient=recipient,
                body=body,
            )
        )
        return message_id


class RenewalReminderService(SmsGateway):
    """Mix business policy with an inherited transport API for diagnosis."""

    def __init__(self, sender_id: str, audit_log: list[str]) -> None:
        super().__init__(sender_id)
        self.audit_log = audit_log

    def remind(self, customer: Customer, days_remaining: int) -> ReminderReceipt:
        """Build and send the current SMS reminder."""

        if days_remaining <= 0:
            raise ValueError("days_remaining must be positive")

        body = f"Hello {customer.name}, your subscription renews in {days_remaining} day(s)."
        message_id = self.send_message(customer.phone, body)
        self.audit_log.append(f"renewal-reminder:{customer.customer_id}:{message_id}")
        return ReminderReceipt(
            customer_id=customer.customer_id,
            message_id=message_id,
            channel="sms",
            body=body,
        )


def main() -> None:
    """Run the starter's deterministic happy path."""

    audit_log: list[str] = []
    service = RenewalReminderService("ACME", audit_log)
    customer = Customer("customer-42", "Mina", "+910000000000")

    print(service.remind(customer, days_remaining=3))
    print(f"sent_messages={service.sent_messages}")
    print(f"audit_log={audit_log}")


if __name__ == "__main__":
    main()
