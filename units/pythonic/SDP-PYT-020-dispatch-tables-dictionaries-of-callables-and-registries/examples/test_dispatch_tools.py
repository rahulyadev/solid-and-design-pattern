"""Observable contracts for the solved dispatch example."""

from collections.abc import Iterator, Mapping
from typing import cast

import pytest
from dispatch_tools import (
    Event,
    Handler,
    RegistryBuilder,
    RegistrySealed,
    UnknownEventType,
    archive_deleted,
    build_registry,
    dispatch,
    dispatch_all,
    index_created,
    quarantine_unknown,
    resolve_handler,
)


def test_build_registry_preserves_registration_order() -> None:
    handlers = build_registry(
        [("record.deleted", archive_deleted), ("record.created", index_created)]
    )
    assert tuple(handlers) == ("record.deleted", "record.created")


@pytest.mark.parametrize("name", ["", " ", "\t", " record.created", "record.created "])
def test_registration_rejects_ambiguous_names(name: str) -> None:
    with pytest.raises(ValueError, match="handler names"):
        build_registry([(name, index_created)])


@pytest.mark.parametrize("second", [index_created, archive_deleted])
def test_duplicate_registration_is_rejected_instead_of_last_write_wins(second: Handler) -> None:
    with pytest.raises(ValueError, match=r"duplicate handler: record\.created"):
        build_registry([("record.created", index_created), ("record.created", second)])


def test_build_registry_consumes_entries_once() -> None:
    consumed: list[str] = []

    def entries() -> Iterator[tuple[str, Handler]]:
        consumed.append("first")
        yield "record.created", index_created
        consumed.append("second")
        yield "record.deleted", archive_deleted

    handlers = build_registry(entries())
    assert consumed == ["first", "second"]
    assert tuple(handlers) == ("record.created", "record.deleted")


def test_published_registry_rejects_mapping_writes() -> None:
    handlers = build_registry([("record.created", index_created)])
    with pytest.raises(TypeError):
        cast(dict[str, Handler], handlers)["record.deleted"] = archive_deleted


def test_builder_rejects_registration_after_seal() -> None:
    builder = RegistryBuilder()
    builder.register("record.created", index_created)
    published = builder.seal()

    with pytest.raises(RegistrySealed, match="registry is sealed"):
        builder.register("record.deleted", archive_deleted)

    assert tuple(published) == ("record.created",)


def test_repeated_seal_returns_the_same_published_mapping() -> None:
    builder = RegistryBuilder()
    builder.register("record.created", index_created)
    assert builder.seal() is builder.seal()


def test_separate_builders_have_separate_registration_state() -> None:
    first = RegistryBuilder()
    second = RegistryBuilder()
    first.register("record.created", index_created)
    second.register("record.deleted", archive_deleted)
    assert tuple(first.seal()) == ("record.created",)
    assert tuple(second.seal()) == ("record.deleted",)


def test_resolve_is_an_exact_key_lookup() -> None:
    handlers = build_registry([("record.created", index_created)])
    assert resolve_handler("record.created", handlers) is index_created
    with pytest.raises(UnknownEventType, match=r"unsupported event type: RECORD\.CREATED"):
        resolve_handler("RECORD.CREATED", handlers)


@pytest.mark.parametrize("name", ["missing", "", " record.created", "record.created "])
def test_unknown_name_is_rejected_without_implicit_normalization(name: str) -> None:
    with pytest.raises(UnknownEventType, match="unsupported event type"):
        resolve_handler(name, build_registry([("record.created", index_created)]))


def test_explicit_fallback_is_returned_only_for_a_missing_name() -> None:
    handlers = build_registry([("record.created", index_created)])
    assert resolve_handler("record.created", handlers, fallback=quarantine_unknown) is index_created
    assert (
        resolve_handler("record.other", handlers, fallback=quarantine_unknown) is quarantine_unknown
    )


def test_dispatch_selects_then_calls_once_with_the_original_event() -> None:
    calls: list[tuple[Event, str]] = []

    def observe(event: Event, /, *, trace_id: str) -> str:
        calls.append((event, trace_id))
        return "accepted"

    event = Event("record.observed", "X-2")
    result = dispatch(
        event,
        build_registry([("record.observed", observe)]),
        trace_id="trace-44",
    )
    assert result == "accepted"
    assert calls == [(event, "trace-44")]
    assert calls[0][0] is event


def test_handler_key_error_is_not_misreported_as_unknown_dispatch_key() -> None:
    failure = KeyError("payload.customer_id")

    def broken(event: Event, /, *, trace_id: str) -> str:
        del event, trace_id
        raise failure

    with pytest.raises(KeyError) as caught:
        dispatch(
            Event("record.broken", "X-7"),
            build_registry([("record.broken", broken)]),
            trace_id="trace-45",
        )
    assert caught.value is failure


def test_dispatch_all_preserves_order_and_duplicates() -> None:
    handlers = build_registry(
        [("record.created", index_created), ("record.deleted", archive_deleted)]
    )
    events = [
        Event("record.created", "A"),
        Event("record.deleted", "B"),
        Event("record.created", "A"),
    ]
    assert dispatch_all(events, handlers, trace_id="t") == (
        "t:index:A",
        "t:archive:B",
        "t:index:A",
    )
    assert events == [
        Event("record.created", "A"),
        Event("record.deleted", "B"),
        Event("record.created", "A"),
    ]


def test_dispatch_all_stops_after_first_handler_failure() -> None:
    visited: list[str] = []
    failure = RuntimeError("handler failed")

    def source() -> Iterator[Event]:
        for entity_id in ("one", "two", "three"):
            visited.append(entity_id)
            yield Event("record.created", entity_id)

    def handler(event: Event, /, *, trace_id: str) -> str:
        del trace_id
        if event.entity_id == "two":
            raise failure
        return event.entity_id

    with pytest.raises(RuntimeError) as caught:
        dispatch_all(source(), build_registry([("record.created", handler)]), trace_id="t")
    assert caught.value is failure
    assert visited == ["one", "two"]


def test_fallback_receives_the_unknown_event_without_changing_its_kind() -> None:
    event = Event("record.restored", "Z-9")
    assert (
        dispatch(
            event,
            build_registry([]),
            trace_id="trace-fallback",
            fallback=quarantine_unknown,
        )
        == "trace-fallback:quarantine:record.restored:Z-9"
    )


def test_mapping_contract_can_be_supplied_without_concrete_dict_dependency() -> None:
    class OneHandler(Mapping[str, Handler]):
        def __getitem__(self, key: str) -> Handler:
            if key != "record.created":
                raise KeyError(key)
            return index_created

        def __iter__(self) -> Iterator[str]:
            yield "record.created"

        def __len__(self) -> int:
            return 1

    assert dispatch(Event("record.created", "M-1"), OneHandler(), trace_id="t") == "t:index:M-1"
