"""Unsolved legacy baseline. Keep the two public report contracts during phase A."""

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class RepairJob:
    job_id: str
    title: str
    minutes: int | None
    closed: bool = False


@dataclass(frozen=True)
class ReportOptions:
    include_closed: bool
    strip_title: bool
    uppercase: bool
    include_id: bool
    missing_minutes: str
    separator: str


class LegacyReportEngine:
    def __init__(self, options: ReportOptions) -> None:
        self.options = options

    def render(self, jobs: Sequence[RepairJob]) -> tuple[str, ...]:
        lines: list[str] = []
        for job in jobs:
            if job.closed and not self.options.include_closed:
                continue
            title = job.title.strip() if self.options.strip_title else job.title
            if self.options.uppercase:
                title = title.upper()
            duration = str(job.minutes or self.options.missing_minutes)
            pieces = [title, duration]
            if self.options.include_id:
                pieces.insert(0, job.job_id)
            lines.append(self.options.separator.join(pieces))
        return tuple(lines)


class ReportFactory:
    def for_board(self) -> LegacyReportEngine:
        return LegacyReportEngine(ReportOptions(False, True, True, False, "?", " / "))

    def for_archive(self) -> LegacyReportEngine:
        return LegacyReportEngine(ReportOptions(True, False, False, True, "unknown", "::"))


def board_report(jobs: Sequence[RepairJob]) -> tuple[str, ...]:
    return ReportFactory().for_board().render(jobs)


def archive_report(jobs: Sequence[RepairJob]) -> tuple[str, ...]:
    return ReportFactory().for_archive().render(jobs)


def main() -> None:
    jobs = (
        RepairJob("J-1", " wheel ", 15),
        RepairJob("J-2", "lamp", 0),
        RepairJob("J-3", "radio", None, closed=True),
    )
    print(f"board: {board_report(jobs)!r}")
    print(f"archive: {archive_report(jobs)!r}")


if __name__ == "__main__":
    main()
