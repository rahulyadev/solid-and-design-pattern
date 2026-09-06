"""Phase-A characterization tests; they do not reveal the target refactoring."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from incident_archive_lab import Archive, Incident, export_priority_incidents


def test_filters_formats_and_preserves_order_and_duplicates() -> None:
    repeated = Incident("i-2", 5, "investigate | retry")
    incidents = [Incident("i-1", 1, "low"), repeated, repeated]
    archive = Archive()

    result = export_priority_incidents(
        incidents,
        minimum_priority=4,
        archive=archive,
    )

    assert result == (
        "i-2:5:investigate | retry",
        "i-2:5:investigate | retry",
    )
    assert archive.rows == list(result)
    assert archive.closed is True
    assert archive.close_calls == 1
    assert incidents == [Incident("i-1", 1, "low"), repeated, repeated]


def test_empty_input_still_closes_archive() -> None:
    archive = Archive()

    assert export_priority_incidents([], minimum_priority=0, archive=archive) == ()
    assert archive.closed is True
    assert archive.close_calls == 1


def test_one_pass_input_is_supported() -> None:
    source = iter([Incident("i-1", 4, "one"), Incident("i-2", 5, "two")])
    archive = Archive()

    assert export_priority_incidents(
        source,
        minimum_priority=4,
        archive=archive,
    ) == ("i-1:4:one", "i-2:5:two")
    assert tuple(source) == ()


def test_invalid_policy_is_rejected_before_input_is_consumed_or_archive_closed() -> None:
    consumed: list[str] = []
    archive = Archive()

    def source() -> Iterator[Incident]:
        consumed.append("started")
        yield Incident("i-1", 4, "one")

    with pytest.raises(ValueError, match="minimum_priority must be non-negative"):
        export_priority_incidents(
            source(),
            minimum_priority=-1,
            archive=archive,
        )

    assert consumed == []
    assert archive.closed is False
    assert archive.close_calls == 0


def test_archive_failure_propagates_and_archive_is_closed_once() -> None:
    row = "i-2:5:fail"
    archive = Archive(fail_on=row)

    with pytest.raises(OSError, match=f"synthetic archive failure: {row}"):
        export_priority_incidents(
            [Incident("i-1", 4, "ok"), Incident("i-2", 5, "fail")],
            minimum_priority=4,
            archive=archive,
        )

    assert archive.rows == ["i-1:4:ok"]
    assert archive.closed is True
    assert archive.close_calls == 1


def test_source_failure_happens_before_any_write_because_legacy_code_is_eager() -> None:
    archive = Archive()
    original = RuntimeError("source failed")

    def source() -> Iterator[Incident]:
        yield Incident("i-1", 4, "would be exported in a lazy design")
        raise original

    with pytest.raises(RuntimeError) as captured:
        export_priority_incidents(
            source(),
            minimum_priority=4,
            archive=archive,
        )

    assert captured.value is original
    assert archive.rows == []
    assert archive.closed is False
    assert archive.close_calls == 0


def test_blank_and_unicode_text_are_passed_through_without_normalization() -> None:
    archive = Archive()

    assert export_priority_incidents(
        [Incident("घटना", 4, "")],
        minimum_priority=4,
        archive=archive,
    ) == ("घटना:4:",)
