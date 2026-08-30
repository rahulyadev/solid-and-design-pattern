"""Phase-A characterization only; no phase-B implementation or hints are supplied."""

from collections.abc import Callable, Sequence

import pytest
from workshop_reports_lab import RepairJob, archive_report, board_report

Report = Callable[[Sequence[RepairJob]], tuple[str, ...]]


def test_board_baseline_keeps_order_duplicates_and_filters_closed_jobs() -> None:
    jobs = (
        RepairJob("J-2", " wheel ", 15),
        RepairJob("J-1", "radio", 20, closed=True),
        RepairJob("J-2", " wheel ", 15),
        RepairJob("J-3", "Écran", None),
    )
    assert board_report(jobs) == ("WHEEL / 15", "WHEEL / 15", "ÉCRAN / ?")


def test_archive_baseline_preserves_ids_closed_jobs_and_exact_titles() -> None:
    jobs = (
        RepairJob("J-2", " wheel ", 15),
        RepairJob("J-1", "Radio", 20, closed=True),
        RepairJob("J-2", " wheel ", 15),
    )
    assert archive_report(jobs) == (
        "J-2:: wheel ::15",
        "J-1::Radio::20",
        "J-2:: wheel ::15",
    )


@pytest.mark.parametrize("minutes", [None, 0])
def test_existing_zero_and_unknown_minute_quirk(minutes: int | None) -> None:
    jobs = (RepairJob("J-1", "Lamp", minutes),)
    assert board_report(jobs) == ("LAMP / ?",)
    assert archive_report(jobs) == ("J-1::Lamp::unknown",)


@pytest.mark.parametrize("report", [board_report, archive_report])
def test_empty_input_returns_tuple(report: Report) -> None:
    assert report(()) == ()


@pytest.mark.parametrize("report", [board_report, archive_report])
def test_input_list_is_unchanged_and_reusable(report: Report) -> None:
    job = RepairJob("J-1", "wheel", 10)
    jobs = [job, job, RepairJob("J-2", "lamp", 5, closed=True)]
    before = jobs.copy()
    first = report(jobs)
    assert report(jobs) == first
    assert jobs == before
    assert jobs[0] is job and jobs[1] is job


def test_blank_titles_and_negative_minutes_are_existing_behaviour() -> None:
    jobs = (RepairJob("", "  ", -5), RepairJob("J-2", "", 2))
    assert board_report(jobs) == (" / -5", " / 2")
    assert archive_report(jobs) == ("::  ::-5", "J-2::::2")


def test_separator_and_newline_characters_are_not_escaped() -> None:
    jobs = (RepairJob("J::1", "A::B\nC", 7),)
    assert board_report(jobs) == ("A::B\nC / 7",)
    assert archive_report(jobs) == ("J::1::A::B\nC::7",)


def test_all_closed_jobs_only_appear_in_archive() -> None:
    jobs = (RepairJob("J-1", "radio", None, closed=True),)
    assert board_report(jobs) == ()
    assert archive_report(jobs) == ("J-1::radio::unknown",)
