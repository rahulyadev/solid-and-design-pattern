"""Working starter for the unsolved SDP-PYT-090 alert-export exercise.

The current closed conditional is deliberately acceptable. Preserve its
behavior before adding the new independently installed provider requirement.
"""

from __future__ import annotations

import json
from dataclasses import dataclass


class UnknownExportFormatError(LookupError):
    """The requested built-in export format does not exist."""


@dataclass(frozen=True, slots=True)
class Alert:
    alert_id: str
    service: str
    severity: int


@dataclass(frozen=True, slots=True)
class ExportedAlert:
    media_type: str
    body: str


def _validate(alert: Alert) -> None:
    for field_name, value in (("alert_id", alert.alert_id), ("service", alert.service)):
        if not value or value != value.strip():
            raise ValueError(f"{field_name} must be non-empty and trimmed")
    if not 1 <= alert.severity <= 5:
        raise ValueError("severity must be between 1 and 5")


def export_alert(format_name: str, alert: Alert) -> ExportedAlert:
    """Export with the current closed set of application-owned formats."""

    _validate(alert)
    if format_name == "text":
        return ExportedAlert(
            "text/plain",
            f"{alert.alert_id}|{alert.service}|severity={alert.severity}",
        )
    if format_name == "json":
        return ExportedAlert(
            "application/json",
            json.dumps(
                {
                    "alert_id": alert.alert_id,
                    "service": alert.service,
                    "severity": alert.severity,
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
        )
    raise UnknownExportFormatError(f"unknown alert export format: {format_name!r}")


def main() -> None:
    alert = Alert("alert-7", "catalog", 3)
    print(export_alert("text", alert))
    print(export_alert("json", alert))


if __name__ == "__main__":
    main()
