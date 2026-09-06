"""Behavior and mechanism tests for the worked example."""

from __future__ import annotations

from collections.abc import Callable

import pytest
from interface_design import (
    ArchiveChannelAdapter,
    AuditEvent,
    BufferedOwnedChannel,
    DeliveryReceipt,
    InMemoryChannel,
    OwnedBatchChannel,
    RegisteredLegacyChannel,
    VendorArchive,
    deliver_audit_event,
    deliver_with,
)


def make_channels() -> tuple[InMemoryChannel, ArchiveChannelAdapter]:
    return InMemoryChannel(), ArchiveChannelAdapter(VendorArchive())


@pytest.mark.parametrize("channel", make_channels())
def test_structural_implementations_preserve_receipt_contract(
    channel: InMemoryChannel | ArchiveChannelAdapter,
) -> None:
    event = AuditEvent("evt:हिन्दी|1", "invoice.created", "amount=2500")

    receipt = deliver_audit_event(channel, event, idempotency_key="req:1|retry")

    assert receipt == DeliveryReceipt(event.event_id, channel.channel_name, "req:1|retry")


def test_in_memory_channel_replays_same_request_without_duplicate() -> None:
    channel = InMemoryChannel()
    event = AuditEvent("evt-1", "invoice.created", "amount=2500")

    first = deliver_audit_event(channel, event, idempotency_key="request-1")
    second = deliver_audit_event(channel, event, idempotency_key="request-1")

    assert second is first
    assert channel.receipts == (first,)


def test_in_memory_channel_rejects_idempotency_collision() -> None:
    channel = InMemoryChannel()
    first = AuditEvent("evt-1", "invoice.created", "amount=2500")
    second = AuditEvent("evt-2", "invoice.created", "amount=3000")
    deliver_audit_event(channel, first, idempotency_key="request-1")

    with pytest.raises(ValueError, match="cannot identify two events"):
        deliver_audit_event(channel, second, idempotency_key="request-1")

    assert tuple(receipt.event_id for receipt in channel.receipts) == ("evt-1",)


@pytest.mark.parametrize("value", ["", " leading", "trailing "])
def test_event_rejects_invalid_text(value: str) -> None:
    with pytest.raises(ValueError, match="must be non-empty and trimmed"):
        AuditEvent(value, "invoice.created", "amount=2500")


def test_client_rejects_wrong_receipt_before_returning_it() -> None:
    class LyingChannel:
        @property
        def channel_name(self) -> str:
            return "liar"

        def deliver(self, event: AuditEvent, *, idempotency_key: str) -> DeliveryReceipt:
            return DeliveryReceipt("another-event", self.channel_name, idempotency_key)

    event = AuditEvent("evt-1", "invoice.created", "amount=2500")
    with pytest.raises(RuntimeError, match="another event"):
        deliver_audit_event(LyingChannel(), event, idempotency_key="request-1")


def test_callable_is_enough_for_one_operation() -> None:
    event = AuditEvent("evt-1", "invoice.created", "amount=2500")

    def send(candidate: AuditEvent) -> DeliveryReceipt:
        return DeliveryReceipt(candidate.event_id, "function", "fixed-key")

    annotated_send: Callable[[AuditEvent], DeliveryReceipt] = send
    assert deliver_with(event, annotated_send).channel == "function"


def test_owned_abc_supplies_shared_batch_algorithm() -> None:
    channel = BufferedOwnedChannel()
    events = (
        AuditEvent("evt-1", "invoice.created", "amount=2500"),
        AuditEvent("evt-2", "invoice.created", "amount=3000"),
    )

    receipts = channel.deliver_batch(events)

    assert channel.event_ids == ("evt-1", "evt-2")
    assert tuple(receipt.idempotency_key for receipt in receipts) == (
        "batch:evt-1",
        "batch:evt-2",
    )


def test_incomplete_direct_abc_subclass_cannot_be_instantiated() -> None:
    class IncompleteChannel(OwnedBatchChannel):
        pass

    with pytest.raises(TypeError, match="abstract"):
        IncompleteChannel()  # type: ignore[abstract]


def test_virtual_registration_changes_recognition_not_mro_or_methods() -> None:
    channel = RegisteredLegacyChannel()

    assert isinstance(channel, OwnedBatchChannel)
    assert OwnedBatchChannel not in type(channel).__mro__
    assert not hasattr(channel, "deliver_batch")
