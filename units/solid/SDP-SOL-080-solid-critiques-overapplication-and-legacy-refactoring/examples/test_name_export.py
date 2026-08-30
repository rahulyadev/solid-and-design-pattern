"""Characterize public results and externally visible effects, not helper calls."""

from collections.abc import Callable, Iterable, Iterator

import pytest
from hypothesis import given
from hypothesis import strategies as st
from name_export import export_legacy, export_overbuilt, export_refactored, preview_names

Exporter = Callable[[Iterable[str], Callable[[str], None]], int]
EXPORTERS = (export_legacy, export_refactored, export_overbuilt)


@pytest.mark.parametrize("export", EXPORTERS)
def test_exact_text_order_duplicates_and_input_ownership(export: Exporter) -> None:
    names = ["Mira", " Omar ", "Mira", "Éva", " "]
    before = names.copy()
    lines: list[str] = []

    assert export(names, lines.append) == 5
    assert lines == ["[MIRA]", "[ OMAR ]", "[MIRA]", "[ÉVA]", "[ ]"]
    assert names == before


@pytest.mark.parametrize("export", EXPORTERS)
def test_empty_input_makes_no_write(export: Exporter) -> None:
    lines: list[str] = []
    assert export(iter(()), lines.append) == 0
    assert lines == []


@pytest.mark.parametrize("export", EXPORTERS)
def test_invalid_first_name_makes_no_write(export: Exporter) -> None:
    lines: list[str] = []
    with pytest.raises(ValueError, match=r"^empty name$"):
        export(("", "Mira"), lines.append)
    assert lines == []


@pytest.mark.parametrize("export", EXPORTERS)
def test_invalid_later_name_keeps_prefix_and_leaves_tail_unconsumed(export: Exporter) -> None:
    names = iter(("Mira", "", "Omar"))
    lines: list[str] = []
    with pytest.raises(ValueError, match=r"^empty name$"):
        export(names, lines.append)
    assert lines == ["[MIRA]"]
    assert next(names) == "Omar"


@pytest.mark.parametrize("export", EXPORTERS)
def test_source_failure_is_preserved_after_prior_effect(export: Exporter) -> None:
    failure = RuntimeError("source unavailable")

    def names() -> Iterator[str]:
        yield "Mira"
        raise failure

    lines: list[str] = []
    with pytest.raises(RuntimeError) as caught:
        export(names(), lines.append)
    assert caught.value is failure
    assert lines == ["[MIRA]"]


@pytest.mark.parametrize("export", EXPORTERS)
@pytest.mark.parametrize("fail_at", [0, 1])
@pytest.mark.parametrize("save_before_error", [False, True])
def test_writer_failure_does_not_retry_or_read_ahead(
    export: Exporter, fail_at: int, save_before_error: bool
) -> None:
    names = iter(("Mira", "Omar", "Asha"))
    attempts: list[str] = []
    saved: list[str] = []
    failure = OSError("writer unavailable")

    def emit(line: str) -> None:
        attempts.append(line)
        if len(attempts) - 1 == fail_at:
            if save_before_error:
                saved.append(line)
            raise failure
        saved.append(line)

    with pytest.raises(OSError) as caught:
        export(names, emit)
    assert caught.value is failure
    assert attempts == ["[MIRA]", "[OMAR]"][: fail_at + 1]
    saved_count = fail_at + int(save_before_error)
    assert saved == ["[MIRA]", "[OMAR]"][:saved_count]
    assert next(names) == ("Omar" if fail_at == 0 else "Asha")


@given(st.lists(st.text(min_size=1), max_size=20))
def test_refactoring_matches_existing_success_contract(names: list[str]) -> None:
    before = names.copy()
    old_lines: list[str] = []
    new_lines: list[str] = []
    assert export_legacy(iter(names), old_lines.append) == len(names)
    assert export_refactored(iter(names), new_lines.append) == len(names)
    assert new_lines == old_lines
    assert names == before


def test_separate_preview_feature_has_no_output_dependency() -> None:
    assert preview_names(iter(("Mira", " Omar ", "Mira"))) == (
        "[MIRA]",
        "[ OMAR ]",
        "[MIRA]",
    )
    assert preview_names(()) == ()
    with pytest.raises(ValueError, match=r"^empty name$"):
        preview_names(("Mira", ""))
