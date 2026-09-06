"""A small, typed descriptor earned by repeated managed-attribute semantics.

The example is intentionally framework-free.  It keeps validation synchronous,
deterministic, and local; network or database work does not belong in attribute
lookup.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar, overload

T = TypeVar("T")


class FieldValidationError(ValueError):
    """A public value could not satisfy its managed-field contract."""


class ManagedField(Generic[T]):  # noqa: UP046 - Python 3.11 compatibility is required
    """A reusable data descriptor with private per-instance storage."""

    def __init__(
        self,
        convert: Callable[[object], T],
        *,
        validate: Callable[[T], None] | None = None,
    ) -> None:
        self._convert = convert
        self._validate = validate or (lambda _value: None)
        self._public_name: str | None = None
        self._storage_name: str | None = None

    def __set_name__(self, owner: type[object], name: str) -> None:
        if self._public_name is not None and self._public_name != name:
            raise RuntimeError("one ManagedField instance cannot manage two names")
        self._public_name = name
        self._storage_name = f"_managed_{name}"

    @overload
    def __get__(self, instance: None, owner: type[object] | None = None) -> ManagedField[T]: ...

    @overload
    def __get__(self, instance: object, owner: type[object] | None = None) -> T: ...

    def __get__(
        self,
        instance: object | None,
        owner: type[object] | None = None,
    ) -> ManagedField[T] | T:
        if instance is None:
            return self
        storage_name = self._require_storage_name()
        try:
            value = getattr(instance, storage_name)
        except AttributeError as error:
            public_name = self._public_name or "<unnamed>"
            raise AttributeError(f"{public_name} has not been assigned") from error
        return value  # type: ignore[no-any-return]

    def __set__(self, instance: object, raw_value: object) -> None:
        try:
            value = self._convert(raw_value)
            self._validate(value)
        except FieldValidationError:
            raise
        except (TypeError, ValueError) as error:
            public_name = self._public_name or "<unnamed>"
            raise FieldValidationError(f"invalid {public_name}: {error}") from error
        setattr(instance, self._require_storage_name(), value)

    def __delete__(self, instance: object) -> None:
        storage_name = self._require_storage_name()
        try:
            delattr(instance, storage_name)
        except AttributeError as error:
            public_name = self._public_name or "<unnamed>"
            raise AttributeError(f"{public_name} has not been assigned") from error

    @property
    def public_name(self) -> str:
        if self._public_name is None:
            raise RuntimeError("ManagedField is not attached to a class")
        return self._public_name

    @property
    def storage_name(self) -> str:
        return self._require_storage_name()

    def _require_storage_name(self) -> str:
        if self._storage_name is None:
            raise RuntimeError("ManagedField is not attached to a class")
        return self._storage_name


def trimmed_text(raw: object) -> str:
    if not isinstance(raw, str):
        raise TypeError("expected str")
    value = raw.strip()
    if not value:
        raise ValueError("must not be blank")
    return value


def port_number(raw: object) -> int:
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise TypeError("expected int but not bool")
    if not 1 <= raw <= 65_535:
        raise ValueError("must be between 1 and 65535")
    return raw


class ServiceEndpoint:
    """Two fields share one explicit, reusable descriptor mechanism."""

    name = ManagedField(trimmed_text)
    port = ManagedField(port_number)

    def __init__(self, name: str, port: int) -> None:
        self.name = name
        self.port = port

    def authority(self) -> str:
        return f"{self.name}:{self.port}"


class HealthCheck:
    """A second owner demonstrates why a descriptor can be earned."""

    path = ManagedField(trimmed_text)
    interval_seconds = ManagedField(port_number)

    def __init__(self, path: str, interval_seconds: int) -> None:
        self.path = path
        self.interval_seconds = interval_seconds
