"""Behavioural contracts for the worked examples, not a lab solution."""

from collections.abc import Iterator
from functools import partial

import pytest
from callable_tools import (
    CountingEncoder,
    direct_batch,
    encode_batch,
    make_prefix_encoder,
    make_write_action,
    prefixed_utf8,
    run_actions,
    utf8,
)
from run_callable_demo import MemoryWriter


@pytest.mark.parametrize(
    ("texts", "expected"),
    [
        ((), ()),
        (("",), (b"",)),
        (("alpha", "alpha"), (b"alpha", b"alpha")),
        (
            ("é", "पानी"),
            (b"\xc3\xa9", b"\xe0\xa4\xaa\xe0\xa4\xbe\xe0\xa4\xa8\xe0\xa5\x80"),
        ),
    ],
)
def test_direct_and_injected_function_keep_original_contract(
    texts: tuple[str, ...], expected: tuple[bytes, ...]
) -> None:
    assert direct_batch(texts) == expected
    assert encode_batch(iter(texts), utf8) == expected


def test_swapping_callable_forms_preserves_the_calling_contract() -> None:
    closure = make_prefix_encoder("tag/")
    configured = partial(prefixed_utf8, "tag/")
    counted = CountingEncoder(closure)
    expected = (b"tag/a", b"tag/", b"tag/a")
    for encode in (closure, configured, counted):
        assert encode_batch(("a", "", "a"), encode) == expected
    assert counted.successful_calls == 3


def test_each_factory_configuration_stays_independent() -> None:
    left = make_prefix_encoder("left/")
    right = make_prefix_encoder("right/")
    assert left("x") == b"left/x"
    assert right("x") == b"right/x"
    assert left("x") == b"left/x"


def test_encoding_order_and_exactly_one_call_per_input() -> None:
    seen: list[str] = []

    def record(text: str) -> bytes:
        seen.append(text)
        return utf8(text)

    assert encode_batch(iter(("b", "a", "b")), record) == (b"b", b"a", b"b")
    assert seen == ["b", "a", "b"]


def test_encoder_failure_preserves_identity_effects_and_unconsumed_tail() -> None:
    seen: list[str] = []
    failure = ValueError("synthetic encoding failure")

    def record(text: str) -> bytes:
        seen.append(text)
        if text == "bad":
            raise failure
        return utf8(text)

    source = iter(("good", "bad", "later"))
    with pytest.raises(ValueError) as caught:
        encode_batch(source, record)
    assert caught.value is failure
    assert seen == ["good", "bad"]
    assert next(source) == "later"


def test_source_failure_is_not_swallowed_or_retried() -> None:
    failure = OSError("synthetic source failure")
    counted = CountingEncoder(utf8)

    def source() -> Iterator[str]:
        yield "first"
        raise failure

    with pytest.raises(OSError) as caught:
        encode_batch(source(), counted)
    assert caught.value is failure
    assert counted.successful_calls == 1


def test_counts_include_success_only_and_are_per_instance() -> None:
    first = CountingEncoder(utf8)
    alias = first
    second = CountingEncoder(utf8)
    first("x")
    alias("")
    with pytest.raises(UnicodeEncodeError):
        first("\ud800")
    assert first.successful_calls == 2
    assert second.successful_calls == 0
    second("y")
    assert second.successful_calls == 1


def test_empty_input_never_calls_encoder() -> None:
    def forbidden(text: str) -> bytes:
        raise AssertionError(f"unexpected call for {text}")

    assert encode_batch((), forbidden) == ()


def test_bound_method_sink_and_deferred_action_replay() -> None:
    writer = MemoryWriter()
    action = make_write_action(b"one", writer.write, channel="A")
    assert writer.records == []
    run_actions((action, action))
    assert writer.records == [("A", b"one"), ("A", b"one")]


def test_command_factory_configurations_are_independent() -> None:
    writer = MemoryWriter()
    first = make_write_action(b"one", writer.write, channel="A")
    second = make_write_action(b"two", writer.write, channel="B")
    run_actions((second, first))
    assert writer.records == [("B", b"two"), ("A", b"one")]


@pytest.mark.parametrize("effect_before_failure", [False, True])
def test_action_failure_stops_later_actions_without_undo(effect_before_failure: bool) -> None:
    records: list[bytes] = []
    failure = OSError("synthetic failure")

    def sink(payload: bytes, /, *, channel: str) -> None:
        if payload == b"bad":
            if effect_before_failure:
                records.append(payload)
            raise failure
        records.append(payload)

    actions = tuple(
        make_write_action(payload, sink, channel="test") for payload in (b"one", b"bad", b"later")
    )
    with pytest.raises(OSError) as caught:
        run_actions(iter(actions))
    assert caught.value is failure
    assert records == ([b"one", b"bad"] if effect_before_failure else [b"one"])


def test_empty_action_sequence_is_accepted() -> None:
    run_actions(())


def test_partial_keyword_binding_is_overridable() -> None:
    configured = partial(prefixed_utf8, prefix="default/")
    assert configured(text="x") == b"default/x"
    assert configured(text="x", prefix="override/") == b"override/x"
