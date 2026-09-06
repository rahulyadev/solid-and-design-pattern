"""Behavior tests for the unsolved Factory Method lab baseline."""

from __future__ import annotations

import json

import pytest
from incident_export_lab import (
    TARGET_REFACTOR_COMPLETE,
    IncidentReport,
    UnknownFormatError,
    export_report,
    publish_report,
)


def test_text_baseline() -> None:
    assert export_report(IncidentReport("INC-1", 4, 3), "text") == (
        "incident=INC-1; opened=4; resolved=3"
    )


def test_json_baseline_is_deterministic() -> None:
    body = export_report(IncidentReport("INC-2", 4, 3), "json")

    assert json.loads(body) == {"incident_id": "INC-2", "opened": 4, "resolved": 3}
    assert body == '{"incident_id":"INC-2","opened":4,"resolved":3}'


@pytest.mark.parametrize(
    "report",
    [
        pytest.param(IncidentReport("INC-3", 0, 0), id="zero-counts"),
        pytest.param(IncidentReport("INC-4", 5, 5), id="all-resolved"),
    ],
)
def test_valid_boundaries(report: IncidentReport) -> None:
    assert report.resolved <= report.opened


@pytest.mark.parametrize(
    ("incident_id", "opened", "resolved"),
    [("", 1, 0), ("é", 1, 0), ("INC-5", -1, 0), ("INC-6", 1, -1), ("INC-7", 1, 2)],
)
def test_invalid_reports(incident_id: str, opened: int, resolved: int) -> None:
    with pytest.raises(ValueError):
        IncidentReport(incident_id, opened, resolved)


def test_unknown_name_has_no_write_side_effect() -> None:
    output: list[str] = []

    with pytest.raises(UnknownFormatError, match="missing"):
        publish_report(IncidentReport("INC-8", 2, 1), "missing", output)

    assert output == []


def test_workflow_writes_once_and_returns_same_body() -> None:
    output: list[str] = []

    body = publish_report(IncidentReport("INC-9", 2, 1), "text", output)

    assert output == [body]


def test_target_design_work_remains_unsolved() -> None:
    assert TARGET_REFACTOR_COMPLETE is False
