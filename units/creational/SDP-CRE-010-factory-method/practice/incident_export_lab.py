"""Unsolved baseline for SDP-CRE-010 predict-run-refactor practice.

Keep this file as the original attempt, or copy it before changing the design.
The current behavior is intentionally a small conditional; the target extension
and construction boundary remain for the learner to design.
"""

from __future__ import annotations

import json
from dataclasses import dataclass


class UnknownFormatError(LookupError):
    """A requested export format is not supported by this baseline."""


@dataclass(frozen=True, slots=True)
class IncidentReport:
    incident_id: str
    opened: int
    resolved: int

    def __post_init__(self) -> None:
        if not self.incident_id or not self.incident_id.isascii():
            raise ValueError("incident_id must be nonblank ASCII")
        if self.opened < 0 or self.resolved < 0:
            raise ValueError("counts must be nonnegative")
        if self.resolved > self.opened:
            raise ValueError("resolved cannot exceed opened")


def export_report(report: IncidentReport, format_name: str) -> str:
    """Working baseline whose construction/selection concern is not yet separated."""

    if format_name == "text":
        return f"incident={report.incident_id}; opened={report.opened}; resolved={report.resolved}"
    if format_name == "json":
        return json.dumps(
            {
                "incident_id": report.incident_id,
                "opened": report.opened,
                "resolved": report.resolved,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    raise UnknownFormatError(f"unknown format: {format_name!r}")


def publish_report(report: IncidentReport, format_name: str, output: list[str]) -> str:
    """Stable desired workflow: export once, append once, return the same body."""

    body = export_report(report, format_name)
    output.append(body)
    return body


TARGET_REFACTOR_COMPLETE = False


def main() -> None:
    output: list[str] = []
    body = publish_report(IncidentReport("INC-7", 3, 2), "text", output)
    print(body)
    print(f"writes={len(output)}; target_complete={TARGET_REFACTOR_COMPLETE}")


if __name__ == "__main__":
    main()
