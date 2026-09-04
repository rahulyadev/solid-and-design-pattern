"""Explicit event dispatch and a controlled startup registry.

The examples are synchronous and use synthetic data. They deliberately stop
before plugin discovery, framework routing, retries, or real I/O.
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Protocol


@dataclass(frozen=True)
class Event:
    """A small event whose kind is the explicit dispatch key."""

    kind: str
    entity_id: str


class Handler(Protocol):
    """The complete calling contract shared by registered handlers."""

    def __call__(self, event: Event, /, *, trace_id: str) -> str: ...


class UnknownEventType(LookupError):
    """The dispatch key has no registered handler and no explicit fallback."""


class RegistrySealed(RuntimeError):
    """Registration was attempted after the registry was published."""


def _validate_handler_name(name: str) -> None:
    if not name or name != name.strip():
        raise ValueError("handler names must be nonblank with no surrounding whitespace")


class RegistryBuilder:
    """Collect unique handlers during startup, then publish stable bindings.

    Sealing copies the name-to-handler bindings and exposes a read-only proxy.
    It does not freeze mutable state inside a handler.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, Handler] = {}
        self._published: Mapping[str, Handler] | None = None

    @property
    def is_sealed(self) -> bool:
        return self._published is not None

    def register(self, name: str, handler: Handler) -> None:
        if self.is_sealed:
            raise RegistrySealed("registry is sealed")
        _validate_handler_name(name)
        if name in self._handlers:
            raise ValueError(f"duplicate handler: {name}")
        self._handlers[name] = handler

    def seal(self) -> Mapping[str, Handler]:
        if self._published is None:
            self._published = MappingProxyType(dict(self._handlers))
        return self._published


def build_registry(entries: Iterable[tuple[str, Handler]]) -> Mapping[str, Handler]:
    """Build a registry from one pass over ordered startup entries."""

    builder = RegistryBuilder()
    for name, handler in entries:
        builder.register(name, handler)
    return builder.seal()


def resolve_handler(
    name: str,
    handlers: Mapping[str, Handler],
    *,
    fallback: Handler | None = None,
) -> Handler:
    """Select one handler while keeping the missing-name policy explicit."""

    try:
        return handlers[name]
    except KeyError:
        if fallback is not None:
            return fallback
        raise UnknownEventType(f"unsupported event type: {name}") from None


def dispatch(
    event: Event,
    handlers: Mapping[str, Handler],
    *,
    trace_id: str,
    fallback: Handler | None = None,
) -> str:
    """Resolve first, then invoke outside the lookup exception boundary."""

    handler = resolve_handler(event.kind, handlers, fallback=fallback)
    return handler(event, trace_id=trace_id)


def dispatch_all(
    events: Iterable[Event],
    handlers: Mapping[str, Handler],
    *,
    trace_id: str,
    fallback: Handler | None = None,
) -> tuple[str, ...]:
    """Dispatch in source order and stop on the first lookup or handler failure."""

    return tuple(
        dispatch(event, handlers, trace_id=trace_id, fallback=fallback) for event in events
    )


def index_created(event: Event, /, *, trace_id: str) -> str:
    return f"{trace_id}:index:{event.entity_id}"


def archive_deleted(event: Event, /, *, trace_id: str) -> str:
    return f"{trace_id}:archive:{event.entity_id}"


def quarantine_unknown(event: Event, /, *, trace_id: str) -> str:
    return f"{trace_id}:quarantine:{event.kind}:{event.entity_id}"


def example_registry() -> Mapping[str, Handler]:
    return build_registry(
        [
            ("record.created", index_created),
            ("record.deleted", archive_deleted),
        ]
    )


def visual_observations() -> dict[str, object]:
    """Return the fixed observations embedded in the companion HTML visual."""

    handlers = example_registry()
    created = Event("record.created", "A-17")
    success = dispatch(created, handlers, trace_id="tr-8")

    try:
        dispatch(Event("record.missing", "B-4"), handlers, trace_id="tr-9")
    except UnknownEventType as error:
        unknown = {"type": type(error).__name__, "message": str(error)}
    else:  # pragma: no cover - a regression would fail the equality test first
        unknown = {"type": "none", "message": "no error"}

    failure = KeyError("required-field")

    def broken(event: Event, /, *, trace_id: str) -> str:
        del event, trace_id
        raise failure

    broken_handlers = build_registry([("record.broken", broken)])
    try:
        dispatch(Event("record.broken", "C-2"), broken_handlers, trace_id="tr-10")
    except KeyError as error:
        handler_failure = {
            "type": type(error).__name__,
            "argument": str(error.args[0]),
            "same_object": error is failure,
        }
    else:  # pragma: no cover - a regression would fail the equality test first
        handler_failure = {"type": "none", "argument": "", "same_object": False}

    builder = RegistryBuilder()
    builder.register("record.created", index_created)
    builder.register("record.deleted", archive_deleted)
    published = builder.seal()
    try:
        builder.register("record.restored", index_created)
    except RegistrySealed as error:
        sealed_error = str(error)
    else:  # pragma: no cover - a regression would fail the equality test first
        sealed_error = "no error"

    return {
        "selection": {
            "key": created.kind,
            "available": list(handlers),
            "result": success,
        },
        "unknown": unknown,
        "handler_failure": handler_failure,
        "lifecycle": {
            "published_names": list(published),
            "post_seal_registration": sealed_error,
        },
    }
