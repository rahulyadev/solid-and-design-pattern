"""Practical interface choices for a synthetic audit-delivery boundary.

The client owns ``EventChannel``.  Implementations may satisfy it structurally;
none of the runtime calls depends on Protocol inheritance.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_id: str
    kind: str
    payload: str

    def __post_init__(self) -> None:
        for field_name, value in (
            ("event_id", self.event_id),
            ("kind", self.kind),
            ("payload", self.payload),
        ):
            if not value or value != value.strip():
                raise ValueError(f"{field_name} must be non-empty and trimmed")


@dataclass(frozen=True, slots=True)
class DeliveryReceipt:
    event_id: str
    channel: str
    idempotency_key: str


class EventChannel(Protocol):
    """Client-owned static shape; implementations need not inherit from it."""

    @property
    def channel_name(self) -> str: ...

    def deliver(self, event: AuditEvent, *, idempotency_key: str) -> DeliveryReceipt: ...


class InMemoryChannel:
    """A structural implementation and useful behavior-focused test fake."""

    def __init__(self, channel_name: str = "memory") -> None:
        self._channel_name = channel_name
        self._receipts: dict[str, DeliveryReceipt] = {}

    @property
    def channel_name(self) -> str:
        return self._channel_name

    @property
    def receipts(self) -> tuple[DeliveryReceipt, ...]:
        return tuple(self._receipts.values())

    def deliver(self, event: AuditEvent, *, idempotency_key: str) -> DeliveryReceipt:
        existing = self._receipts.get(idempotency_key)
        if existing is not None:
            if existing.event_id != event.event_id:
                raise ValueError("an idempotency key cannot identify two events")
            return existing

        receipt = DeliveryReceipt(event.event_id, self.channel_name, idempotency_key)
        self._receipts[idempotency_key] = receipt
        return receipt


class VendorArchive:
    """Foreign API whose vocabulary does not match the client's interface."""

    def put_record(self, body: str, request_token: str) -> str:
        if not request_token:
            raise ValueError("request_token is required")
        return f"archive:{request_token}:{len(body)}"


class ArchiveChannelAdapter:
    """Translate a foreign collaborator instead of making it inherit our type."""

    def __init__(self, archive: VendorArchive) -> None:
        self._archive = archive

    @property
    def channel_name(self) -> str:
        return "vendor-archive"

    def deliver(self, event: AuditEvent, *, idempotency_key: str) -> DeliveryReceipt:
        body = f"{event.event_id}|{event.kind}|{event.payload}"
        self._archive.put_record(body=body, request_token=idempotency_key)
        return DeliveryReceipt(event.event_id, self.channel_name, idempotency_key)


def deliver_audit_event(
    channel: EventChannel, event: AuditEvent, *, idempotency_key: str
) -> DeliveryReceipt:
    """Use the interface, then enforce a client-visible postcondition."""

    if not idempotency_key or idempotency_key != idempotency_key.strip():
        raise ValueError("idempotency_key must be non-empty and trimmed")

    receipt = channel.deliver(event, idempotency_key=idempotency_key)
    if receipt.event_id != event.event_id:
        raise RuntimeError("channel returned a receipt for another event")
    if receipt.idempotency_key != idempotency_key:
        raise RuntimeError("channel returned a receipt for another request")
    return receipt


DeliveryFunction = Callable[[AuditEvent], DeliveryReceipt]


def deliver_with(event: AuditEvent, send: DeliveryFunction) -> DeliveryReceipt:
    """Smallest alternative when one stateless call is the entire boundary."""

    return send(event)


class OwnedBatchChannel(ABC):
    """Owned nominal family with an enforced primitive and shared algorithm."""

    @property
    @abstractmethod
    def channel_name(self) -> str:
        """Return the stable channel label used in receipts."""

    @abstractmethod
    def deliver(self, event: AuditEvent, *, idempotency_key: str) -> DeliveryReceipt:
        """Deliver one event according to the documented behavior contract."""

    def deliver_batch(self, events: Iterable[AuditEvent]) -> tuple[DeliveryReceipt, ...]:
        return tuple(
            self.deliver(event, idempotency_key=f"batch:{event.event_id}") for event in events
        )


class BufferedOwnedChannel(OwnedBatchChannel):
    def __init__(self) -> None:
        self._event_ids: list[str] = []

    @property
    def channel_name(self) -> str:
        return "buffer"

    @property
    def event_ids(self) -> tuple[str, ...]:
        return tuple(self._event_ids)

    def deliver(self, event: AuditEvent, *, idempotency_key: str) -> DeliveryReceipt:
        self._event_ids.append(event.event_id)
        return DeliveryReceipt(event.event_id, self.channel_name, idempotency_key)


class RegisteredLegacyChannel:
    """An unrelated class deliberately trusted through virtual registration."""

    @property
    def channel_name(self) -> str:
        return "legacy"

    def deliver(self, event: AuditEvent, *, idempotency_key: str) -> DeliveryReceipt:
        return DeliveryReceipt(event.event_id, self.channel_name, idempotency_key)


OwnedBatchChannel.register(RegisteredLegacyChannel)
