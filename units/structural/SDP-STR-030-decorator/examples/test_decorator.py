from collections.abc import Callable

import pytest
from hypothesis import given
from hypothesis import strategies as st
from order_effects_probe import probe
from run_decorator_demo import preview
from text_components import Bracket, Label, MemoryText, Observed
from text_contract import Observation, SourceClosed, TextSource


@pytest.mark.parametrize("text", ["", "ready", "नमस्ते", "a\nb\n", "[raw]"])
def test_order_and_one_delegation(text: str) -> None:
    base = MemoryText({"N-1": text})
    assert Label(Bracket(base), "note: ").render("N-1") == "note: [" + text + "]"
    assert base.calls == 1
    assert Bracket(Label(base, "note: ")).render("N-1") == "[note: " + text + "]"
    assert base.calls == 2
    assert base.render("N-1") == text


@given(text=st.text(), label=st.text())
def test_composition_preserves_original_characters(text: str, label: str) -> None:
    source = MemoryText({"": text})
    assert Bracket(Label(source, label)).render("") == "[" + label + text + "]"
    assert source.calls == 1


def test_stacking_same_behavior_twice() -> None:
    base = MemoryText({"N-1": "ready"})
    assert preview(Bracket(Bracket(base)), "N-1") == "[[ready]]"
    assert base.calls == 1


def test_clients_can_share_source_with_independent_presentations() -> None:
    data = {"N-1": "ready"}
    base = MemoryText(data)
    left = Label(base, "left: ")
    right = Bracket(base)
    data["N-1"] = "changed outside snapshot"
    assert preview(left, "N-1") == "left: ready"
    assert preview(right, "N-1") == "[ready]"
    assert base.close_count == 0
    base.close()
    base.close()
    for source in (left, right):
        with pytest.raises(SourceClosed):
            source.render("N-1")
    assert base.close_count == 1


def test_identity_and_extra_capability_are_not_forwarded() -> None:
    base = MemoryText({"N-1": "ready"})
    source = Bracket(base)
    assert source.inner is base
    assert id(source) != id(base)
    assert source != Bracket(base)
    assert not hasattr(source, "close")


@pytest.mark.parametrize("inside", [True, False])
def test_observation_position_defines_what_is_measured(inside: bool) -> None:
    events: list[Observation] = []
    base = MemoryText({"N-1": "ready"})
    source: TextSource
    if inside:
        source = Bracket(Label(Observed(base, events.append), "note: "))
    else:
        source = Observed(Bracket(Label(base, "note: ")), events.append)
    assert source.render("N-1") == "[note: ready]"
    assert events == [Observation("ok", 5 if inside else 13)]
    assert base.calls == 1


def test_observation_counts_code_points_not_utf8_bytes() -> None:
    events: list[Observation] = []
    source = Observed(MemoryText({"N-1": "é"}), events.append)
    assert source.render("N-1") == "é"
    assert events == [Observation("ok", 1)]
    assert len("é".encode()) == 2


def test_observation_returns_same_object() -> None:
    text = "".join(["original", " result"])
    source = Observed(MemoryText({"N-1": text}), lambda event: None)
    assert source.render("N-1") is text


@pytest.mark.parametrize("failure", [KeyError("N-1"), SourceClosed("closed"), OSError("read")])
@pytest.mark.parametrize("observer_fails", [False, True])
def test_original_failure_preserved_without_retry(failure: Exception, observer_fails: bool) -> None:
    class FailingSource:
        calls = 0

        def render(self, key: str, /) -> str:
            self.calls += 1
            raise failure

    events: list[Observation] = []

    def observe(event: Observation) -> None:
        events.append(event)
        if observer_fails:
            raise RuntimeError("observer failed")

    base = FailingSource()
    source = Observed(Label(Bracket(base), "note: "), observe)
    with pytest.raises(type(failure)) as caught:
        source.render("N-1")
    assert caught.value is failure
    assert events == [Observation("error", None)]
    assert base.calls == 1
    assert source.dropped == int(observer_fails)


@pytest.mark.parametrize("failure", [OSError("sink"), ValueError("sink bug")])
def test_optional_observer_failure_does_not_erase_success(failure: Exception) -> None:
    def observe(event: Observation) -> None:
        raise failure

    base = MemoryText({"N-1": "ready"})
    source = Observed(base, observe)
    assert source.render("N-1") == "ready"
    assert source.render("N-1") == "ready"
    assert source.dropped == 2
    assert base.calls == 2


@pytest.mark.parametrize("at_observer", [False, True])
def test_control_flow_exceptions_are_not_swallowed(at_observer: bool) -> None:
    class Stop(BaseException):
        pass

    failure = Stop()
    events: list[Observation] = []

    class Source:
        def render(self, key: str, /) -> str:
            if not at_observer:
                raise failure
            return "ready"

    def observe(event: Observation) -> None:
        events.append(event)
        raise failure

    source = Observed(Source(), observe)
    with pytest.raises(Stop) as caught:
        source.render("N-1")
    assert caught.value is failure
    assert len(events) == int(at_observer)
    assert source.dropped == 0


@pytest.mark.parametrize(
    "wrap",
    [
        lambda source: source,
        lambda source: Label(source, ""),
        lambda source: Bracket(source),
        lambda source: Observed(source, lambda event: None),
    ],
)
def test_common_source_error_and_lifetime_contract(
    wrap: Callable[[TextSource], TextSource],
) -> None:
    base = MemoryText({"": ""})
    source = wrap(base)
    assert isinstance(source.render(""), str)
    with pytest.raises(KeyError) as missing:
        source.render("missing")
    assert missing.value.args == ("missing",)
    assert base.calls == 2
    assert base.close_count == 0
    base.close()
    with pytest.raises(SourceClosed):
        source.render("")


def test_probe_matches_documented_observations() -> None:
    assert probe() == (
        "label_outside | note: [ready]",
        "bracket_outside | [note: ready]",
        "observe_inside | [note: ready] | 5",
        "observe_outside | [note: ready] | 13",
        "observer_failure | ready | dropped=1",
        "source_failure | KeyError | error",
        "lifetime | calls=6 | closes=1",
    )


def test_wiring_has_no_render_or_observation_effects() -> None:
    base = MemoryText({"N-1": "ready"})
    events: list[Observation] = []
    source: TextSource = Observed(Bracket(Label(base, "note: ")), events.append)
    assert base.calls == 0
    assert base.close_count == 0
    assert events == []
    assert source.render("N-1") == "[note: ready]"


def test_self_calls_stay_on_inner_receiver() -> None:
    class Base:
        def render(self, key: str, /) -> str:
            return self.description()

        def description(self) -> str:
            return "from base"

    class Wrapper:
        def __init__(self, inner: Base) -> None:
            self.inner = inner

        def description(self) -> str:
            return "from wrapper"

        def render(self, key: str, /) -> str:
            return self.inner.render(key)

    source: TextSource = Wrapper(Base())
    assert source.render("N-1") == "from base"


def test_observer_side_effect_before_failure_is_not_rolled_back() -> None:
    events: list[Observation] = []

    def partly_failing_sink(event: Observation) -> None:
        events.append(event)
        raise OSError("acknowledgement failed after append")

    base = MemoryText({"N-1": "ready"})
    source = Observed(base, partly_failing_sink)
    assert source.render("N-1") == "ready"
    assert source.dropped == 1
    assert events == [Observation("ok", 5)]
    assert base.calls == 1


def test_root_cleanup_runs_when_render_fails() -> None:
    base = MemoryText({})
    source = Bracket(Label(base, "note: "))
    with pytest.raises(KeyError):
        try:
            preview(source, "missing")
        finally:
            base.close()
    assert base.close_count == 1
    with pytest.raises(SourceClosed):
        preview(source, "missing")


def test_observer_can_inspect_result_without_receiving_key_or_content() -> None:
    events: list[Observation] = []
    source = Observed(MemoryText({"synthetic-private-key": "synthetic body"}), events.append)
    source.render("synthetic-private-key")
    assert events == [Observation("ok", 14)]
    assert set(vars(events[0])) == {"outcome", "characters"}
