"""Configuration, lookup, policy, and constructor-shape tests."""

from __future__ import annotations

import pytest
from factory_method import Alert, BufferedTransport, FramedTransport
from selection import (
    ConfigurationError,
    DisallowedTransportError,
    TransportConfig,
    UnknownTransportError,
    application_factories,
    build_transport,
    select_factory,
)


@pytest.mark.parametrize(
    "raw",
    [
        {},
        {"name": ""},
        {"name": 7},
        {"name": "framed", "prefix": "lower"},
        {"name": "framed", "secret": "must-not-be-accepted"},
    ],
)
def test_configuration_is_rejected_before_lookup(raw: dict[str, object]) -> None:
    with pytest.raises(ConfigurationError):
        TransportConfig.from_mapping(raw)


def test_alternate_constructor_builds_same_config_type() -> None:
    config = TransportConfig.from_mapping({"name": "framed", "prefix": "OPS"})

    assert config == TransportConfig("framed", "OPS")


def test_unknown_and_disallowed_names_are_distinct() -> None:
    factories = application_factories([], lambda _record: None)

    with pytest.raises(UnknownTransportError, match="available: buffer, framed"):
        select_factory(TransportConfig("missing"), factories, allowed=set(factories))
    with pytest.raises(DisallowedTransportError, match="disabled"):
        select_factory(TransportConfig("buffer"), factories, allowed={"framed"})


def test_factory_function_constructs_selected_product() -> None:
    buffered: list[str] = []
    framed: list[str] = []
    factories = application_factories(buffered, framed.append)

    first = build_transport(TransportConfig("buffer"), factories, allowed={"buffer"})
    second = build_transport(TransportConfig("framed", "OPS"), factories, allowed={"framed"})

    try:
        first.send(Alert("A-9", "buffered"))
        second.send(Alert("A-10", "framed"))
    finally:
        first.close()
        second.close()

    assert isinstance(first, BufferedTransport)
    assert isinstance(second, FramedTransport)
    assert buffered == ["A-9:buffered"]
    assert framed == ["OPS|A-10|framed"]


def test_selection_is_deterministic_and_does_not_fall_back() -> None:
    factories = application_factories([], lambda _record: None)

    with pytest.raises(UnknownTransportError):
        build_transport(TransportConfig("BUFFER"), factories, allowed=set(factories))


def test_registry_is_application_owned_and_can_be_copied_per_test() -> None:
    factories = application_factories([], lambda _record: None)
    isolated = dict(factories)
    isolated.pop("buffer")

    assert set(factories) == {"buffer", "framed"}
    assert set(isolated) == {"framed"}
