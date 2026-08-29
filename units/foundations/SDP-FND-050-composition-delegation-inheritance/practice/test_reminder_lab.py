"""Characterization tests for the unsolved SDP-FND-050 reminder starter."""

from __future__ import annotations

import pytest
from reminder_lab import (
    Customer,
    ReminderReceipt,
    RenewalReminderService,
    SentMessage,
    SmsGateway,
)


def test_reminder_preserves_current_business_result_and_effects() -> None:
    audit_log: list[str] = []
    service = RenewalReminderService("ACME", audit_log)
    customer = Customer("customer-42", "Mina", "+910000000000")

    receipt = service.remind(customer, days_remaining=3)

    body = "Hello Mina, your subscription renews in 3 day(s)."
    assert receipt == ReminderReceipt(
        customer_id="customer-42",
        message_id="msg-001",
        channel="sms",
        body=body,
    )
    assert service.sent_messages == (
        SentMessage(
            message_id="msg-001",
            sender_id="ACME",
            recipient="+910000000000",
            body=body,
        ),
    )
    assert audit_log == ["renewal-reminder:customer-42:msg-001"]


def test_message_ids_advance_for_successive_reminders() -> None:
    service = RenewalReminderService("ACME", [])
    customer = Customer("customer-42", "Mina", "+910000000000")

    first = service.remind(customer, days_remaining=3)
    second = service.remind(customer, days_remaining=1)

    assert (first.message_id, second.message_id) == ("msg-001", "msg-002")


def test_invalid_days_are_rejected_before_transport_or_audit_effects() -> None:
    audit_log: list[str] = []
    service = RenewalReminderService("ACME", audit_log)
    customer = Customer("customer-42", "Mina", "+910000000000")

    with pytest.raises(ValueError, match="days_remaining must be positive"):
        service.remind(customer, days_remaining=0)

    assert service.sent_messages == ()
    assert audit_log == []


@pytest.mark.parametrize(
    ("customer_id", "name", "phone", "message"),
    [
        ("", "Mina", "+910000000000", "customer_id must not be blank"),
        ("customer-42", " ", "+910000000000", "name must not be blank"),
        ("customer-42", "Mina", "", "phone must not be blank"),
    ],
)
def test_invalid_customer_fields_are_rejected(
    customer_id: str,
    name: str,
    phone: str,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        Customer(customer_id, name, phone)


def test_service_currently_advertises_the_entire_gateway_api() -> None:
    audit_log: list[str] = []
    service = RenewalReminderService("ACME", audit_log)

    assert isinstance(service, SmsGateway)
    direct_message_id = service.send_message("+910000000001", "transport-only call")

    assert direct_message_id == "msg-001"
    assert len(service.sent_messages) == 1
    assert audit_log == []


def test_transport_failure_validation_does_not_create_partial_state() -> None:
    service = RenewalReminderService("ACME", [])

    with pytest.raises(ValueError, match="recipient must not be blank"):
        service.send_message("", "message")

    assert service.sent_messages == ()
