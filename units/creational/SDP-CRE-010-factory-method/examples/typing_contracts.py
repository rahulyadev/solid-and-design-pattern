"""Positive static-typing witnesses for callable and Product contracts."""

from __future__ import annotations

from functools import partial

from factory_method import BufferedTransport, Transport, TransportFactory
from selection import ConfiguredTransportFactory, TransportConfig, buffered_factory


def accept_transport(product: Transport) -> Transport:
    return product


def accept_factory(factory: TransportFactory) -> TransportFactory:
    return factory


def accept_configured_factory(
    factory: ConfiguredTransportFactory,
) -> ConfiguredTransportFactory:
    return factory


output: list[str] = []
product = accept_transport(BufferedTransport(output))
factory = accept_factory(partial(BufferedTransport, output))
configured = accept_configured_factory(partial(buffered_factory, output=output))
configured_product = configured(TransportConfig("buffer"))

assert product.name == factory().name == configured_product.name
