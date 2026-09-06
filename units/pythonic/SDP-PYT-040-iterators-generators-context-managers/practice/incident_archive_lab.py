"""Runnable legacy starter for the independent SDP-PYT-040 practice lab.

The eager list and handwritten try/finally are intentional.  Preserve their
observable behavior before introducing a lazy traversal and managed lifetime.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Incident:
    incident_id: str
    priority: int
    summary: str


class Archive:
    """Synthetic closeable archive; it performs no file or network operation."""

    def __init__(self, *, fail_on: str | None = None) -> None:
        self.rows: list[str] = []
        self.closed = False
        self.close_calls = 0
        self._fail_on = fail_on

    def write(self, row: str) -> None:
        if self.closed:
            raise RuntimeError("archive is closed")
        if row == self._fail_on:
            raise OSError(f"synthetic archive failure: {row}")
        self.rows.append(row)

    def close(self) -> None:
        self.close_calls += 1
        self.closed = True


def export_priority_incidents(
    incidents: Iterable[Incident],
    *,
    minimum_priority: int,
    archive: Archive,
) -> tuple[str, ...]:
    """Eager legacy behavior to characterize before the learner refactors it."""

    if minimum_priority < 0:
        raise ValueError("minimum_priority must be non-negative")

    materialized = list(incidents)
    exported: list[str] = []
    try:
        for incident in materialized:
            if incident.priority >= minimum_priority:
                row = f"{incident.incident_id}:{incident.priority}:{incident.summary}"
                archive.write(row)
                exported.append(row)
        return tuple(exported)
    finally:
        archive.close()


def main() -> None:
    archive = Archive()
    rows = export_priority_incidents(
        [
            Incident("i-1", 1, "low"),
            Incident("i-2", 5, "investigate"),
        ],
        minimum_priority=4,
        archive=archive,
    )
    print(rows)
    print(f"closed={archive.closed}")


if __name__ == "__main__":
    main()
