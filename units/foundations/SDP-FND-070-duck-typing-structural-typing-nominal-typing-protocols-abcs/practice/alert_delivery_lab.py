"""Unsolved SDP-FND-070 starter with a deliberately nominal client boundary."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

VALID_SEVERITIES = frozenset({"info", "warning", "critical"})


@dataclass(frozen=True, slots=True)
class Alert:
    """A validated alert value shared by every delivery channel."""

    event_id: str
    message: str
    severity: str

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id must not be blank")
        if not self.message.strip():
            raise ValueError("message must not be blank")
        if self.severity not in VALID_SEVERITIES:
            raise ValueError(f"unsupported severity: {self.severity}")


@dataclass(frozen=True, slots=True)
class DeliveryReceipt:
    """Represent either delivery or an explicit business non-delivery."""

    channel_code: str
    delivered: bool
    provider_reference: str | None
    reason: str | None = None

    def __post_init__(self) -> None:
        if not self.channel_code.strip():
            raise ValueError("channel_code must not be blank")

        if self.delivered:
            if self.provider_reference is None or not self.provider_reference.strip():
                raise ValueError("a delivered receipt needs a provider reference")
            if self.reason is not None:
                raise ValueError("a delivered receipt must not contain a reason")
            return

        if self.provider_reference is not None:
            raise ValueError("a non-delivery must not contain a provider reference")
        if self.reason is None or not self.reason.strip():
            raise ValueError("a non-delivery needs a reason")


class AlertChannel(ABC):
    """A nominal family used by the starter's client gate."""

    code = "unspecified"

    @abstractmethod
    def deliver(self, alert: Alert) -> DeliveryReceipt:
        """Deliver one validated alert and return one coherent receipt."""


class EmailChannel(AlertChannel):
    """A first-party nominal implementation."""

    code = "email"

    def deliver(self, alert: Alert) -> DeliveryReceipt:
        return DeliveryReceipt(
            channel_code=self.code,
            delivered=True,
            provider_reference=f"email:{alert.event_id}",
        )


class SmsChannel(AlertChannel):
    """A first-party channel with an explicit business limitation."""

    code = "sms"

    def deliver(self, alert: Alert) -> DeliveryReceipt:
        if alert.severity == "info":
            return DeliveryReceipt(
                channel_code=self.code,
                delivered=False,
                provider_reference=None,
                reason="SMS is reserved for warning and critical alerts",
            )
        return DeliveryReceipt(
            channel_code=self.code,
            delivered=True,
            provider_reference=f"sms:{alert.event_id}",
        )


class PartnerWebhookChannel:
    """An unrelated provider class with the exact client-required operation."""

    code = "partner-webhook"

    def deliver(self, alert: Alert) -> DeliveryReceipt:
        return DeliveryReceipt(
            channel_code=self.code,
            delivered=True,
            provider_reference=f"webhook:{alert.event_id}",
        )


class LegacyPager:
    """An incompatible API that will need an adapter if the client must use it."""

    def push(self, text: str, priority: int) -> str:
        return f"pager:{priority}:{len(text)}"


def deliver_alert(alert: Alert, channel: AlertChannel) -> DeliveryReceipt:
    """Deliver through a deliberately restrictive nominal preflight check."""

    if not isinstance(channel, AlertChannel):
        raise TypeError(f"unsupported alert channel: {type(channel).__name__}")
    return channel.deliver(alert)


def deliver_batch(
    alert: Alert,
    channels: tuple[AlertChannel, ...],
) -> tuple[DeliveryReceipt, ...]:
    """Preserve channel order while applying the same restrictive boundary."""

    return tuple(deliver_alert(alert, channel) for channel in channels)


def main() -> None:
    """Expose the current behaviour and the third-party compatibility gap."""

    alert = Alert("evt-42", "Payment queue is delayed", "critical")
    current = deliver_batch(alert, (EmailChannel(), SmsChannel()))
    print(f"current={current}")

    partner = PartnerWebhookChannel()
    print(f"partner_direct={partner.deliver(alert)}")
    try:
        deliver_alert(alert, partner)  # type: ignore[arg-type]
    except TypeError as error:
        print(f"partner_boundary={type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
