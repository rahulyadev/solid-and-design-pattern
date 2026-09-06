"""Behavior and boundary tests for the SDP-CRE-020 worked example."""

from __future__ import annotations

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


def test_mixed_products_fail_before_external_write() -> None:
    observations: list[Observation] = []

    with pytest.raises(IncompatibleFamilyError, match="acknowledgement decoder"):
        deliver(Event("EVT-4", "do not send"), MixedFactory(), observations.append)

    assert [item.phase for item in observations] == ["family.selected", "delivery.failed"]
    assert observations[-1].error_type == "IncompatibleFamilyError"


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
    bundle = DeliveryBundle(
        WireFamily.JSON_V1,
        JsonEncoder(),
        JsonChannel(wire),
        JsonAcknowledgementDecoder(),
    )

    receipt = deliver_with_bundle(Event("EVT-6", "ready"), bundle)

    assert receipt.delivery_id == "json:EVT-6"
    assert len(wire) == 1


@pytest.mark.parametrize(
    ("event_id", "message"),
    [("", "ok"), ("é", "ok"), ("bad|id", "ok"), ("EVT-7", "")],
)
def test_invalid_events_fail_at_domain_boundary(event_id: str, message: str) -> None:
    with pytest.raises(ValueError):
        Event(event_id, message)
