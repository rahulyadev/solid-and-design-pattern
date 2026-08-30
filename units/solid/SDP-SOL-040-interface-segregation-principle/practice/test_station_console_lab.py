"""Characterize the current console; these tests do not solve the new integration."""

import pytest
from station_console_lab import LabConsole, Station, apply_interval, temperature_report


def test_report_preserves_order_duplicates_and_zero_readings() -> None:
    console = LabConsole({"north": Station(-4), "south": Station(0)})
    assert temperature_report(console, ("south", "north", "south")) == (
        ("south", 0),
        ("north", -4),
        ("south", 0),
    )
    assert console.snapshot("north") == Station(-4)
    assert console.snapshot("south") == Station(0)


def test_empty_report_does_not_need_a_station() -> None:
    assert temperature_report(LabConsole({}), ()) == ()


def test_missing_reading_is_an_error_not_zero() -> None:
    with pytest.raises(KeyError):
        temperature_report(LabConsole({"known": Station(0)}), ("known", "missing"))


@pytest.mark.parametrize("seconds", [1, 120, 3600])
def test_configuration_updates_only_selected_station_and_restarts_once(seconds: int) -> None:
    console = LabConsole({"north": Station(18), "south": Station(0)})
    apply_interval(console, "north", seconds)
    assert console.snapshot("north") == Station(18, seconds, 1)
    assert console.snapshot("south") == Station(0)


@pytest.mark.parametrize("seconds", [-1, 0, 3601])
def test_rejected_configuration_preserves_station_and_does_not_restart(seconds: int) -> None:
    console = LabConsole({"north": Station(18)})
    with pytest.raises(ValueError, match="interval"):
        apply_interval(console, "north", seconds)
    assert console.snapshot("north") == Station(18)


def test_unknown_configuration_target_does_not_change_known_station() -> None:
    console = LabConsole({"north": Station(18)})
    with pytest.raises(KeyError):
        apply_interval(console, "unknown", 120)
    assert console.snapshot("north") == Station(18)


def test_each_successful_reconfiguration_restarts_once() -> None:
    console = LabConsole({"north": Station(18)})
    apply_interval(console, "north", 120)
    apply_interval(console, "north", 30)
    assert console.snapshot("north") == Station(18, 30, 2)


def test_console_owns_a_copy_of_input_mapping() -> None:
    stations = {"north": Station(18)}
    console = LabConsole(stations)
    stations["north"] = Station(99)
    apply_interval(console, "north", 120)
    assert console.snapshot("north") == Station(18, 120, 1)
    assert stations["north"] == Station(99)


def test_old_snapshot_remains_an_unchanged_value() -> None:
    console = LabConsole({"north": Station(18)})
    before = console.snapshot("north")
    apply_interval(console, "north", 120)
    assert before == Station(18)


def test_negative_restart_count_is_rejected() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        Station(18, restarts=-1)
