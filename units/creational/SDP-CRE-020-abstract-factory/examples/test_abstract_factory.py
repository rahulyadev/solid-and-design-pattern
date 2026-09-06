"""Behavior and boundary tests for the SDP-CRE-020 worked example."""

from __future__ import annotations

from collections.abc import Callable
from contextlib import AbstractContextManager
from dataclasses import dataclass

import pytest
from abstract_factory import (
    AcknowledgementDecoder,
    Channel,
    ChannelClosedError,
    DeliveryBundle,
    DeliveryFamilyFactory,
    DisallowedFamilyError,
    Encoder,
    Event,
    IncompatibleFamilyError,
    InvalidAcknowledgementError,
    JsonAcknowledgementDecoder,
    JsonChannel,
    JsonDeliveryFactory,
    JsonEncoder,
    MalformedFamilyNameError,
    Observation,
    PipeAcknowledgementDecoder,
    PipeChannel,
    PipeDeliveryFactory,
    PipeEncoder,
    UnknownFamilyError,
    WireFamily,
    deliver,
    deliver_with_bundle,
    select_factory,
)
from hypothesis import given
from hypothesis import strategies as st


@pytest.mark.parametrize(
    ("factory", "delivery_id"),
    [
        pytest.param(JsonDeliveryFactory([]), "json:EVT-1", id="json-family"),
        pytest.param(PipeDeliveryFactory([]), "pipe:EVT-1", id="pipe-family"),
    ],
)
def test_complete_family_delivers(factory: DeliveryFamilyFactory, delivery_id: str) -> None:
    receipt = deliver(Event("EVT-1", "ready"), factory)

    assert receipt.family is factory.family
    assert receipt.delivery_id == delivery_id
    assert receipt.accepted is True


def test_each_delivery_gets_a_new_owned_channel() -> None:
    wire: list[bytes] = []
    factory = JsonDeliveryFactory(wire)

    deliver(Event("EVT-1", "one"), factory)
    deliver(Event("EVT-2", "two"), factory)

    assert len(wire) == 2


def test_channel_rejects_cross_family_payload() -> None:
    channel = JsonChannel([])
    payload = PipeEncoder().encode(Event("EVT-2", "wrong family"))

    with channel, pytest.raises(IncompatibleFamilyError, match="json channel payload"):
        channel.send(payload)


def test_channel_is_closed_after_owned_context() -> None:
    channel = JsonChannel([])
    payload = JsonEncoder().encode(Event("EVT-3", "once"))

    with channel:
        channel.send(payload)

    with pytest.raises(ChannelClosedError):
        channel.send(payload)


@dataclass(frozen=True, slots=True)
class MixedFactory:
    @property
    def family(self) -> WireFamily:
        return WireFamily.JSON_V1

    def create_encoder(self) -> Encoder:
        return JsonEncoder()

    def open_channel(self) -> AbstractContextManager[Channel]:
        return PipeChannel([])

    def create_acknowledgement_decoder(self) -> AcknowledgementDecoder:
        return PipeAcknowledgementDecoder()


@dataclass(slots=True)
class FailingSendChannel:
    trace: list[str]

    @property
    def family(self) -> WireFamily:
        return WireFamily.JSON_V1

    def __enter__(self) -> Channel:
        self.trace.append("channel.open")
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.trace.append("channel.close")

    def send(self, payload: object) -> bytes:
        self.trace.append("channel.send")
        raise OSError("synthetic send failure")


@dataclass(frozen=True, slots=True)
class FailingSendFactory:
    channel: FailingSendChannel

    @property
    def family(self) -> WireFamily:
        return WireFamily.JSON_V1

    def create_encoder(self) -> Encoder:
        return JsonEncoder()

    def open_channel(self) -> AbstractContextManager[Channel]:
        return self.channel

    def create_acknowledgement_decoder(self) -> AcknowledgementDecoder:
        return JsonAcknowledgementDecoder()


def test_mixed_products_fail_before_external_write() -> None:
    observations: list[Observation] = []

    with pytest.raises(IncompatibleFamilyError, match="acknowledgement decoder"):
        deliver(Event("EVT-4", "do not send"), MixedFactory(), observations.append)

    assert [item.phase for item in observations] == ["family.selected", "delivery.failed"]
    assert observations[-1].error_type == "IncompatibleFamilyError"


def test_owned_channel_closes_when_send_fails() -> None:
    trace: list[str] = []
    observations: list[Observation] = []

    with pytest.raises(OSError, match="synthetic send failure"):
        deliver(
            Event("EVT-FAIL", "cleanup still runs"),
            FailingSendFactory(FailingSendChannel(trace)),
            observations.append,
        )

    assert trace == ["channel.open", "channel.send", "channel.close"]
    assert observations[-1].phase == "delivery.failed"
    assert observations[-1].error_type == "OSError"


def test_observations_allow_list_fields_and_omit_message() -> None:
    observations: list[Observation] = []
    secret_like_message = "token=never-log-this"

    deliver(Event("EVT-5", secret_like_message), JsonDeliveryFactory([]), observations.append)

    rendered = repr(observations)
    assert secret_like_message not in rendered
    assert [item.phase for item in observations] == [
        "family.selected",
        "family.products_created",
        "delivery.succeeded",
    ]


def test_exact_selection_distinguishes_malformed_unknown_and_disallowed() -> None:
    registry = {
        "json-v1": lambda: JsonDeliveryFactory([]),
        "pipe-v1": lambda: PipeDeliveryFactory([]),
    }

    with pytest.raises(MalformedFamilyNameError):
        select_factory(" json-v1", allowed_names=frozenset(registry), registry=registry)
    with pytest.raises(UnknownFamilyError):
        select_factory("yaml-v1", allowed_names=frozenset(registry), registry=registry)
    with pytest.raises(DisallowedFamilyError):
        select_factory("pipe-v1", allowed_names=frozenset({"json-v1"}), registry=registry)


def test_registry_alias_must_match_factory_family() -> None:
    with pytest.raises(IncompatibleFamilyError, match="registry name"):
        select_factory(
            "json-v1",
            allowed_names=frozenset({"json-v1"}),
            registry={"json-v1": lambda: PipeDeliveryFactory([])},
        )


def test_ready_bundle_is_a_smaller_dependency_injection_seam() -> None:
    wire: list[bytes] = []
    borrowed_channel = JsonChannel(wire)
    bundle = DeliveryBundle(
        WireFamily.JSON_V1,
        JsonEncoder(),
        borrowed_channel,
        JsonAcknowledgementDecoder(),
    )

    first = deliver_with_bundle(Event("EVT-6", "ready"), bundle)
    second = deliver_with_bundle(Event("EVT-7", "still borrowed"), bundle)

    assert first.delivery_id == "json:EVT-6"
    assert second.delivery_id == "json:EVT-7"
    assert len(wire) == 2


def test_ready_bundle_rejects_mixed_channel_before_write() -> None:
    pipe_wire: list[bytes] = []
    bundle = DeliveryBundle(
        WireFamily.JSON_V1,
        JsonEncoder(),
        PipeChannel(pipe_wire),
        JsonAcknowledgementDecoder(),
    )

    with pytest.raises(IncompatibleFamilyError, match="bundle channel"):
        deliver_with_bundle(Event("EVT-8", "do not write"), bundle)

    assert pipe_wire == []


def test_decoders_reject_wrong_acknowledgement_shapes() -> None:
    with pytest.raises(InvalidAcknowledgementError):
        JsonAcknowledgementDecoder().decode(b'{"accepted":"yes"}')
    with pytest.raises(InvalidAcknowledgementError):
        PipeAcknowledgementDecoder().decode(b"MAYBE|pipe:EVT-9")


def test_disallowed_selection_does_not_construct_factory() -> None:
    calls = 0

    def build() -> DeliveryFamilyFactory:
        nonlocal calls
        calls += 1
        return PipeDeliveryFactory([])

    with pytest.raises(DisallowedFamilyError):
        select_factory(
            "pipe-v1",
            allowed_names=frozenset({"json-v1"}),
            registry={"pipe-v1": build},
        )

    assert calls == 0


def test_observer_error_propagates_before_construction() -> None:
    class ObserverFailure(RuntimeError):
        pass

    def fail(_observation: Observation) -> None:
        raise ObserverFailure("telemetry policy is fail-closed")

    wire: list[bytes] = []
    with pytest.raises(ObserverFailure):
        deliver(Event("EVT-10", "not sent"), JsonDeliveryFactory(wire), fail)

    assert wire == []


@pytest.mark.parametrize(
    "factory_builder",
    [
        pytest.param(lambda: JsonDeliveryFactory([]), id="json-v1"),
        pytest.param(lambda: PipeDeliveryFactory([]), id="pipe-v1"),
    ],
)
@given(
    event_id=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-", min_size=1, max_size=20),
    message=st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=1,
        max_size=60,
    ),
)
def test_family_contract_accepts_valid_unicode_messages(
    factory_builder: Callable[[], DeliveryFamilyFactory],
    event_id: str,
    message: str,
) -> None:
    factory = factory_builder()

    receipt = deliver(Event(event_id, message), factory)

    assert receipt.family is factory.family
    assert receipt.delivery_id.endswith(event_id)
    assert receipt.accepted is True


@pytest.mark.parametrize(
    ("event_id", "message"),
    [("", "ok"), ("é", "ok"), ("bad|id", "ok"), ("EVT-7", "")],
)
def test_invalid_events_fail_at_domain_boundary(event_id: str, message: str) -> None:
    with pytest.raises(ValueError):
        Event(event_id, message)
