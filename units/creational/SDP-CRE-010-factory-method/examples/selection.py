"""Validated, deterministic selection for application-owned transport factories."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Set
from dataclasses import dataclass
from functools import partial
from typing import Protocol

from factory_method import BufferedTransport, FramedTransport, Transport


class ConfigurationError(ValueError):
    """Configuration is malformed before any Product is constructed."""


class UnknownTransportError(LookupError):
    """A well-formed name is not present in the application registry."""


class DisallowedTransportError(PermissionError):
    """A known factory is disabled by deployment policy."""


@dataclass(frozen=True, slots=True)
class TransportConfig:
    """Validated construction input, not a container for secret material."""

    name: str
    prefix: str = "ALERT"

    @classmethod
    def from_mapping(cls, raw: Mapping[str, object]) -> TransportConfig:
        """Alternate constructor: parse another representation of this same type."""

        unexpected = set(raw) - {"name", "prefix"}
        if unexpected:
            fields = ", ".join(sorted(unexpected))
            raise ConfigurationError(f"unknown configuration fields: {fields}")

        name = raw.get("name")
        prefix = raw.get("prefix", "ALERT")
        if not isinstance(name, str) or not name or not name.isascii():
            raise ConfigurationError("name must be nonblank ASCII text")
        if not isinstance(prefix, str) or not prefix or not prefix.isascii():
            raise ConfigurationError("prefix must be nonblank ASCII text")
        if prefix != prefix.upper():
            raise ConfigurationError("prefix must be uppercase")
        return cls(name=name, prefix=prefix)


class ConfiguredTransportFactory(Protocol):
    """A precise callable contract whose keyword name matters to static typing."""

    def __call__(self, config: TransportConfig) -> Transport: ...


def buffered_factory(config: TransportConfig, *, output: list[str]) -> Transport:
    del config
    return BufferedTransport(output)


def framed_factory(
    config: TransportConfig,
    *,
    emit: Callable[[str], None],
) -> Transport:
    return FramedTransport(emit, prefix=config.prefix)


def application_factories(
    output: list[str],
    emit: Callable[[str], None],
) -> dict[str, ConfiguredTransportFactory]:
    """Composition root: imports, binds dependencies, and exposes explicit names."""

    return {
        "buffer": partial(buffered_factory, output=output),
        "framed": partial(framed_factory, emit=emit),
    }


def select_factory(
    config: TransportConfig,
    factories: Mapping[str, ConfiguredTransportFactory],
    *,
    allowed: Set[str],
) -> ConfiguredTransportFactory:
    """Resolve only after syntax, availability, and policy are distinguished."""

    try:
        factory = factories[config.name]
    except KeyError:
        available = ", ".join(sorted(factories)) or "<none>"
        raise UnknownTransportError(
            f"unknown transport {config.name!r}; available: {available}"
        ) from None
    if config.name not in allowed:
        raise DisallowedTransportError(f"transport {config.name!r} is disabled")
    return factory


def build_transport(
    config: TransportConfig,
    factories: Mapping[str, ConfiguredTransportFactory],
    *,
    allowed: Set[str],
) -> Transport:
    """Commonly named simple factory function; not the GoF subclass pattern."""

    factory = select_factory(config, factories, allowed=allowed)
    return factory(config)
