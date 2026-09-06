"""Behavior protection for the unsolved alert-export starter."""

import json

import pytest
from alert_export_lab import Alert, ExportedAlert, UnknownExportFormatError, export_alert


@pytest.fixture
def alert() -> Alert:
    return Alert("alert-7", "catalog", 3)


def test_text_export(alert: Alert) -> None:
    assert export_alert("text", alert) == ExportedAlert("text/plain", "alert-7|catalog|severity=3")


def test_json_export(alert: Alert) -> None:
    exported = export_alert("json", alert)

    assert exported.media_type == "application/json"
    assert json.loads(exported.body) == {
        "alert_id": "alert-7",
        "service": "catalog",
        "severity": 3,
    }


@pytest.mark.parametrize("severity", [1, 5])
def test_boundary_severities_are_accepted(severity: int) -> None:
    exported = export_alert("text", Alert("alert-8", "billing", severity))

    assert exported.body.endswith(f"severity={severity}")


@pytest.mark.parametrize("severity", [0, 6])
def test_out_of_range_severity_is_rejected(severity: int) -> None:
    with pytest.raises(ValueError, match="between 1 and 5"):
        export_alert("text", Alert("alert-9", "billing", severity))


@pytest.mark.parametrize(
    "alert",
    [Alert("", "billing", 2), Alert(" alert-10", "billing", 2), Alert("alert-10", "", 2)],
)
def test_invalid_text_fields_are_rejected(alert: Alert) -> None:
    with pytest.raises(ValueError):
        export_alert("text", alert)


def test_unicode_and_literal_pipe_are_preserved() -> None:
    exported = export_alert("json", Alert("अलर्ट|11", "खोज", 4))

    assert json.loads(exported.body)["alert_id"] == "अलर्ट|11"
    assert json.loads(exported.body)["service"] == "खोज"


def test_unknown_format_fails_with_requested_name(alert: Alert) -> None:
    with pytest.raises(UnknownExportFormatError, match="yaml"):
        export_alert("yaml", alert)
