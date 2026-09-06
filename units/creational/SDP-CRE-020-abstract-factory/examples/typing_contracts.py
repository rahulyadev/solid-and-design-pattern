"""Positive static-typing assignments for the Abstract Factory contracts."""

from __future__ import annotations

from abstract_factory import (
    AcknowledgementDecoder,
    DeliveryFamilyFactory,
    Encoder,
    JsonAcknowledgementDecoder,
    JsonDeliveryFactory,
    JsonEncoder,
)

encoder: Encoder = JsonEncoder()
decoder: AcknowledgementDecoder = JsonAcknowledgementDecoder()
factory: DeliveryFamilyFactory = JsonDeliveryFactory([])
