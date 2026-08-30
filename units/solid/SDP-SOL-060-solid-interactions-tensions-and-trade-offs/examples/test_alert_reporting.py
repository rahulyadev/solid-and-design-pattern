"""Observe selection, extension, compatibility, and failure contracts."""

import json
from collections.abc import Callable

import pytest
from alert_formats import json_format, text_format
from alert_policy import Reading, build_report, select_alerts
from coupled_alerts import text_report
from run_alert_demo import legacy_format


def test_cutoff_order_duplicates_and_input_preservation() -> None:
    readings = [Reading("z", 31), Reading("a", 30), Reading("cold", 29), Reading("a", 30)]
    original = list(readings)
    assert select_alerts(readings, 30) == (Reading("z", 31), Reading("a", 30), Reading("a", 30))
    assert readings == original


@pytest.mark.parametrize("readings", [[], [Reading("cool", 9)]])
def test_empty_selection(readings: list[Reading]) -> None:
    assert select_alerts(readings, 10) == ()
    assert build_report(readings, 10, text_format) == ""
    assert json.loads(build_report(readings, 10, json_format)) == []


def test_negative_temperatures_are_valid() -> None:
    assert select_alerts([Reading("freezer", -4), Reading("cold", -10)], -4) == (
        Reading("freezer", -4),
    )


@pytest.mark.parametrize("station", ["", " ", "\t\n"])
def test_blank_station_is_rejected(station: str) -> None:
    with pytest.raises(ValueError, match="blank"):
        Reading(station, 20)


def test_text_format_has_the_documented_order_and_units() -> None:
    rows = (Reading("roof", 35), Reading("west", 30))
    assert text_format(rows) == "roof: 35 C\nwest: 30 C"


def test_json_preserves_unicode_quotes_and_newlines() -> None:
    station = 'कक्ष "A"\nupper'
    assert json.loads(json_format((Reading(station, 30),))) == [{"station": station, "celsius": 30}]


@pytest.mark.parametrize(
    "formatter", [text_format, json_format, legacy_format], ids=["text", "json", "legacy"]
)
def test_repeated_reports_do_not_change_inputs(
    formatter: Callable[[tuple[Reading, ...]], str],
) -> None:
    readings = [Reading("z", 40), Reading("a", 30), Reading("z", 40)]
    original = list(readings)
    first = build_report(readings, 30, formatter)
    assert build_report(readings, 30, formatter) == first
    assert readings == original


def test_new_callable_receives_only_selected_data() -> None:
    observed: list[tuple[Reading, ...]] = []

    def station_names(rows: tuple[Reading, ...]) -> str:
        observed.append(rows)
        return ",".join(row.station for row in rows)

    assert build_report([Reading("low", 4), Reading("high", 5)], 5, station_names) == "high"
    assert observed == [(Reading("high", 5),)]


def test_formatter_is_called_even_for_empty_input() -> None:
    def empty_marker(rows: tuple[Reading, ...]) -> str:
        assert rows == ()
        return "no alerts"

    assert build_report([], 30, empty_marker) == "no alerts"


def test_formatter_failure_is_not_reported_as_no_alerts() -> None:
    failure = RuntimeError("formatter unavailable")

    def failing_format(rows: tuple[Reading, ...]) -> str:
        raise failure

    with pytest.raises(RuntimeError) as caught:
        build_report([Reading("roof", 35)], 30, failing_format)
    assert caught.value is failure


@pytest.mark.parametrize(
    "readings,cutoff",
    [([], 0), ([Reading("a", 3), Reading("b", 4)], 4), ([Reading("cold", -5)], -5)],
)
def test_refactoring_preserves_the_legacy_contract(readings: list[Reading], cutoff: int) -> None:
    assert build_report(readings, cutoff, legacy_format) == text_report(readings, cutoff)
