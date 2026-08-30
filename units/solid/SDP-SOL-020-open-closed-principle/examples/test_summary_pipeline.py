"""Observable contracts for the solved reporting example, not the learner exercise."""

from collections.abc import Callable

import pytest
from run_summary_demo import compact_summary, publish_by_name
from summary_core import Renderer, RunSummary, publish_summary
from summary_formats import LabeledText, json_summary, text_summary
from summary_registry import UnknownRenderer, build_renderers, select_renderer


@pytest.mark.parametrize("counts", [(-1, 0), (0, -1), (-1, -1)])
def test_negative_counts_are_invalid(counts: tuple[int, int]) -> None:
    with pytest.raises(ValueError, match="counts must be nonnegative"):
        RunSummary(*counts)


@pytest.mark.parametrize(
    ("render", "expected"),
    [
        (text_summary, "completed=4; failed=1"),
        (json_summary, '{"completed":4,"failed":1}'),
        (compact_summary, "ok:4/error:1"),
        (LabeledText("finished", "errors"), "finished=4; errors=1"),
        (LabeledText("done", "bad").__call__, "done=4; bad=1"),
    ],
)
def test_functions_objects_and_bound_methods_publish(render: Renderer, expected: str) -> None:
    summary = RunSummary(4, 1)
    writes: list[str] = []
    assert publish_summary(summary, render, writes.append) == expected
    assert writes == [expected]
    assert summary == RunSummary(4, 1)


@pytest.mark.parametrize("summary", [RunSummary(0, 0), RunSummary(11, 7), RunSummary(10**9, 0)])
@pytest.mark.parametrize("name", ["text", "json"])
def test_refactoring_preserves_baseline_outputs(summary: RunSummary, name: str) -> None:
    renderers = build_renderers([("text", text_summary), ("json", json_summary)])
    before: list[str] = []
    after: list[str] = []
    assert publish_by_name(summary, name, before.append) == publish_summary(
        summary, select_renderer(name, renderers), after.append
    )
    assert before == after


def test_custom_renderer_is_called_before_writer_exactly_once() -> None:
    events: list[str] = []

    def render(summary: RunSummary) -> str:
        events.append("render")
        return f"{summary.completed} completed and {summary.failed} failed"

    def write(body: str) -> None:
        events.append(f"write:{body}")

    publish_summary(RunSummary(2, 3), render, write)
    assert events == ["render", "write:2 completed and 3 failed"]


@pytest.mark.parametrize("body", ["", " ", "\n\t"])
def test_blank_renderer_output_never_reaches_writer(body: str) -> None:
    writes: list[str] = []

    def blank(summary: RunSummary) -> str:
        return body

    with pytest.raises(ValueError, match="blank output"):
        publish_summary(RunSummary(0, 0), blank, writes.append)
    assert writes == []


def test_renderer_key_error_is_not_misreported_as_an_unknown_name() -> None:
    writes: list[str] = []
    failure = KeyError("missing renderer configuration")

    def broken(summary: RunSummary) -> str:
        raise failure

    selected = select_renderer("broken", build_renderers([("broken", broken)]))
    with pytest.raises(KeyError) as caught:
        publish_summary(RunSummary(4, 1), selected, writes.append)
    assert caught.value is failure
    assert writes == []


def test_writer_error_propagates_without_retry_or_rollback_claim() -> None:
    writes: list[str] = []
    failure = OSError("writer failed after accepting the body")

    def write_then_fail(body: str) -> None:
        writes.append(body)
        raise failure

    with pytest.raises(OSError) as caught:
        publish_summary(RunSummary(2, 0), text_summary, write_then_fail)
    assert caught.value is failure
    assert writes == ["completed=2; failed=0"]


@pytest.mark.parametrize("name", ["", " ", " text", "text "])
def test_registry_rejects_ambiguous_names(name: str) -> None:
    with pytest.raises(ValueError, match="renderer names"):
        build_renderers([(name, text_summary)])


@pytest.mark.parametrize("second", [text_summary, json_summary])
def test_duplicate_registration_is_rejected_even_for_same_function(second: Renderer) -> None:
    with pytest.raises(ValueError, match="duplicate renderer: text"):
        build_renderers([("text", text_summary), ("text", second)])


@pytest.mark.parametrize("name", ["missing", "TEXT", " text", ""])
def test_registry_lookup_has_no_implicit_fallback(name: str) -> None:
    with pytest.raises(UnknownRenderer, match="unsupported renderer"):
        select_renderer(name, build_renderers([("text", text_summary)]))


def test_empty_registry_rejects_selection() -> None:
    with pytest.raises(UnknownRenderer):
        select_renderer("text", build_renderers([]))


def test_registry_owns_its_name_bindings() -> None:
    source: dict[str, Renderer] = {"text": text_summary}
    renderers = build_renderers(source.items())
    source["text"] = json_summary
    source["json"] = json_summary
    assert select_renderer("text", renderers)(RunSummary(1, 0)) == "completed=1; failed=0"
    with pytest.raises(UnknownRenderer):
        select_renderer("json", renderers)


@pytest.mark.parametrize("labels", [("", "failed"), ("done", " ")])
def test_labels_must_be_nonblank(labels: tuple[str, str]) -> None:
    with pytest.raises(ValueError, match="labels must be nonblank"):
        LabeledText(*labels)


def test_baseline_rejects_unknown_name_before_writing() -> None:
    writes: list[str] = []
    with pytest.raises(ValueError, match="unsupported format"):
        publish_by_name(RunSummary(0, 0), "missing", writes.append)
    assert writes == []


def test_a_callable_annotation_is_a_simpler_equivalent_here() -> None:
    render: Callable[[RunSummary], str] = text_summary
    writes: list[str] = []
    assert publish_summary(RunSummary(0, 0), render, writes.append) == "completed=0; failed=0"
