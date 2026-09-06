"""Runnable Abstract Factory example for SDP-CRE-020.

The synthetic delivery domain makes one family choice produce an encoder,
channel, and acknowledgement decoder that share a wire-family invariant.
"""

from __future__ import annotations

import base64
import json
from collections.abc import Callable, Mapping
from contextlib import AbstractContextManager
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class WireFamily(StrEnum):
    JSON_V1 = "json-v1"
    PIPE_V1 = "pipe-v1"


class FamilyConfigurationError(ValueError):
    """Base class for configuration-boundary failures."""


class MalformedFamilyNameError(FamilyConfigurationError):
    """The configured name is blank or requires implicit normalization."""


class UnknownFamilyError(FamilyConfigurationError, LookupError):
    """The configured family is not installed in this application."""


class DisallowedFamilyError(FamilyConfigurationError, PermissionError):
    """The family exists but policy forbids it in this deployment."""


class IncompatibleFamilyError(RuntimeError):
    """A factory returned products from different wire families."""


class ChannelClosedError(RuntimeError):
    """A caller tried to use a channel after its owned lifetime ended."""


class InvalidAcknowledgementError(ValueError):
    """A channel acknowledgement violated the selected family contract."""


@dataclass(frozen=True, slots=True)
class Event:
    event_id: str
    message: str

    def __post_init__(self) -> None:
        if not self.event_id or not self.event_id.isascii() or "|" in self.event_id:
            raise ValueError("event_id must be nonblank ASCII without '|'")
        if not self.message:
            raise ValueError("message must be nonblank")


@dataclass(frozen=True, slots=True)
class Payload:
    family: WireFamily
    body: bytes


@dataclass(frozen=True, slots=True)
class Receipt:
    family: WireFamily
    delivery_id: str
    accepted: bool


@dataclass(frozen=True, slots=True)
class Observation:
    phase: str
    event_id: str
    family: str
    error_type: str | None = None


class Encoder(Protocol):
    @property
    def family(self) -> WireFamily: ...

    def encode(self, event: Event) -> Payload: ...


class Channel(Protocol):
    @property
    def family(self) -> WireFamily: ...

    def send(self, payload: Payload) -> bytes: ...


class AcknowledgementDecoder(Protocol):
    @property
    def family(self) -> WireFamily: ...

    def decode(self, raw: bytes) -> Receipt: ...


class DeliveryFamilyFactory(Protocol):
    """Abstract Factory contract: one family choice creates all product roles."""

    @property
    def family(self) -> WireFamily: ...

    def create_encoder(self) -> Encoder: ...

    def open_channel(self) -> AbstractContextManager[Channel]: ...

    def create_acknowledgement_decoder(self) -> AcknowledgementDecoder: ...


Observer = Callable[[Observation], None]
FactoryBuilder = Callable[[], DeliveryFamilyFactory]


def ignore_observation(observation: Observation) -> None:
    """Default observer: deliberately does nothing."""


@dataclass(frozen=True, slots=True)
class JsonEncoder:
    @property
    def family(self) -> WireFamily:
        return WireFamily.JSON_V1

    def encode(self, event: Event) -> Payload:
        body = json.dumps(
            {"event_id": event.event_id, "message": event.message},
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return Payload(self.family, body)


@dataclass(slots=True)
class JsonChannel:
    wire: list[bytes]
    _closed: bool = False

    @property
    def family(self) -> WireFamily:
        return WireFamily.JSON_V1

    def __enter__(self) -> Channel:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self._closed = True

    def send(self, payload: Payload) -> bytes:
        if self._closed:
            raise ChannelClosedError("json channel is closed")
        _require_family(self.family, payload.family, "json channel payload")
        self.wire.append(payload.body)
        event_id = str(json.loads(payload.body)["event_id"])
        return json.dumps(
            {"accepted": True, "delivery_id": f"json:{event_id}"},
            separators=(",", ":"),
            sort_keys=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class JsonAcknowledgementDecoder:
    @property
    def family(self) -> WireFamily:
        return WireFamily.JSON_V1

    def decode(self, raw: bytes) -> Receipt:
        try:
            document = json.loads(raw)
            delivery_id = document["delivery_id"]
            accepted = document["accepted"]
        except (KeyError, TypeError, ValueError) as exc:
            raise InvalidAcknowledgementError("invalid json-v1 acknowledgement") from exc
        if not isinstance(delivery_id, str) or not isinstance(accepted, bool):
            raise InvalidAcknowledgementError("invalid json-v1 acknowledgement fields")
        return Receipt(self.family, delivery_id, accepted)


@dataclass(frozen=True, slots=True)
class PipeEncoder:
    @property
    def family(self) -> WireFamily:
        return WireFamily.PIPE_V1

    def encode(self, event: Event) -> Payload:
        encoded_message = base64.urlsafe_b64encode(event.message.encode("utf-8")).decode("ascii")
        return Payload(self.family, f"{event.event_id}|{encoded_message}".encode("ascii"))


@dataclass(slots=True)
class PipeChannel:
    wire: list[bytes]
    _closed: bool = False

    @property
    def family(self) -> WireFamily:
        return WireFamily.PIPE_V1

    def __enter__(self) -> Channel:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self._closed = True

    def send(self, payload: Payload) -> bytes:
        if self._closed:
            raise ChannelClosedError("pipe channel is closed")
        _require_family(self.family, payload.family, "pipe channel payload")
        self.wire.append(payload.body)
        event_id, _separator, _message = payload.body.partition(b"|")
        return b"OK|pipe:" + event_id


@dataclass(frozen=True, slots=True)
class PipeAcknowledgementDecoder:
    @property
    def family(self) -> WireFamily:
        return WireFamily.PIPE_V1

    def decode(self, raw: bytes) -> Receipt:
        status, separator, delivery_id = raw.partition(b"|")
        if separator != b"|" or status not in {b"OK", b"REJECTED"} or not delivery_id:
            raise InvalidAcknowledgementError("invalid pipe-v1 acknowledgement")
        try:
            decoded_id = delivery_id.decode("ascii")
        except UnicodeDecodeError as exc:
            raise InvalidAcknowledgementError("non-ASCII pipe-v1 delivery id") from exc
        return Receipt(self.family, decoded_id, status == b"OK")


@dataclass(frozen=True, slots=True)
class JsonDeliveryFactory:
    wire: list[bytes]

    @property
    def family(self) -> WireFamily:
        return WireFamily.JSON_V1

    def create_encoder(self) -> Encoder:
        return JsonEncoder()

    def open_channel(self) -> AbstractContextManager[Channel]:
        return JsonChannel(self.wire)

    def create_acknowledgement_decoder(self) -> AcknowledgementDecoder:
        return JsonAcknowledgementDecoder()


@dataclass(frozen=True, slots=True)
class PipeDeliveryFactory:
    wire: list[bytes]

    @property
    def family(self) -> WireFamily:
        return WireFamily.PIPE_V1

    def create_encoder(self) -> Encoder:
        return PipeEncoder()

    def open_channel(self) -> AbstractContextManager[Channel]:
        return PipeChannel(self.wire)

    def create_acknowledgement_decoder(self) -> AcknowledgementDecoder:
        return PipeAcknowledgementDecoder()


@dataclass(frozen=True, slots=True)
class DeliveryBundle:
    """Simpler DI alternative when callers only need one prebuilt family."""

    family: WireFamily
    encoder: Encoder
    channel: Channel
    acknowledgement_decoder: AcknowledgementDecoder


def select_factory(
    configured_name: str,
    *,
    allowed_names: frozenset[str],
    registry: Mapping[str, FactoryBuilder],
) -> DeliveryFamilyFactory:
    """Resolve configuration at the composition root, never in policy code."""

    if not configured_name or configured_name != configured_name.strip():
        raise MalformedFamilyNameError("family name must be nonblank and already normalized")
    try:
        builder = registry[configured_name]
    except KeyError as exc:
        raise UnknownFamilyError(f"unknown delivery family: {configured_name!r}") from exc
    if configured_name not in allowed_names:
        raise DisallowedFamilyError(f"delivery family is not allowed: {configured_name!r}")
    factory = builder()
    if factory.family.value != configured_name:
        raise IncompatibleFamilyError("registry name and factory family disagree")
    return factory


def deliver(
    event: Event, factory: DeliveryFamilyFactory, observe: Observer = ignore_observation
) -> Receipt:
    """Stable policy workflow using only Abstract Factory and Product contracts."""

    observe(Observation("family.selected", event.event_id, factory.family.value))
    try:
        encoder = factory.create_encoder()
        decoder = factory.create_acknowledgement_decoder()
        _require_coherent_products(factory, encoder, decoder)
        with factory.open_channel() as channel:
            _require_family(factory.family, channel.family, "factory channel")
            observe(Observation("family.products_created", event.event_id, factory.family.value))
            payload = encoder.encode(event)
            raw_acknowledgement = channel.send(payload)
            receipt = decoder.decode(raw_acknowledgement)
            _require_family(factory.family, receipt.family, "decoded receipt")
    except Exception as exc:
        observe(
            Observation(
                "delivery.failed",
                event.event_id,
                factory.family.value,
                type(exc).__name__,
            )
        )
        raise
    observe(Observation("delivery.succeeded", event.event_id, factory.family.value))
    return receipt


def deliver_with_bundle(
    event: Event,
    bundle: DeliveryBundle,
    observe: Observer = ignore_observation,
) -> Receipt:
    """Ordinary dependency injection: useful when repeatable creation is unnecessary."""

    _require_family(bundle.family, bundle.encoder.family, "bundle encoder")
    _require_family(
        bundle.family,
        bundle.acknowledgement_decoder.family,
        "bundle acknowledgement decoder",
    )
    _require_family(bundle.family, bundle.channel.family, "bundle channel")
    observe(Observation("bundle.selected", event.event_id, bundle.family.value))
    payload = bundle.encoder.encode(event)
    receipt = bundle.acknowledgement_decoder.decode(bundle.channel.send(payload))
    _require_family(bundle.family, receipt.family, "bundle receipt")
    return receipt


def _require_coherent_products(
    factory: DeliveryFamilyFactory,
    encoder: Encoder,
    decoder: AcknowledgementDecoder,
) -> None:
    _require_family(factory.family, encoder.family, "factory encoder")
    _require_family(factory.family, decoder.family, "factory acknowledgement decoder")


def _require_family(expected: WireFamily, actual: WireFamily, role: str) -> None:
    if actual is not expected:
        raise IncompatibleFamilyError(
            f"{role} belongs to {actual.value!r}; expected {expected.value!r}"
        )
