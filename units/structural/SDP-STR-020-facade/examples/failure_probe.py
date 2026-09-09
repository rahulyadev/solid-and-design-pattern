"""Controlled fault injection, not a benchmark or a live-storage experiment."""

from report_contracts import PacketUnavailable, Snapshot
from report_facade import ReportFacade
from report_subsystem import MemoryArchive, MemoryReports, TextRenderer


def observe(scenario: str) -> tuple[str, str, int, int, str]:
    events: list[str] = []
    archive = MemoryArchive(
        events, fail_before_write=scenario == "store_before", lose_ack=scenario == "lost_ack"
    )
    reports = {} if scenario == "missing" else {"WEEK-1": Snapshot(("open=3",))}
    facade = ReportFacade(
        MemoryReports(reports, events), TextRenderer(events, fail=scenario == "render"), archive
    )
    outcome = "acknowledged"
    try:
        try:
            facade.build("WEEK-1")
        except PacketUnavailable as exc:
            outcome = f"{exc.stage.value}:{exc.write_outcome.value}"
        stored = len(archive.keys())
        return scenario, outcome, events.count("store"), stored, ",".join(events)
    finally:
        archive.close()


def main() -> None:
    for scenario in ("success", "missing", "render", "store_before", "lost_ack"):
        print(" | ".join(map(str, observe(scenario))))


if __name__ == "__main__":
    main()
