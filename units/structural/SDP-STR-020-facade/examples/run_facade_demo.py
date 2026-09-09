"""Composition root owns the archive. Run directly from any directory."""

from report_contracts import PacketBuilder, Receipt, Snapshot
from report_facade import ReportFacade
from report_subsystem import MemoryArchive, MemoryReports, TextRenderer


def request_packet(builder: PacketBuilder) -> Receipt:
    return builder.build("WEEK-1")


def main() -> None:
    events: list[str] = []
    archive = MemoryArchive(events)
    try:
        facade = ReportFacade(
            MemoryReports({"WEEK-1": Snapshot(("open=3",))}, events), TextRenderer(events), archive
        )
        receipt = request_packet(facade)
        print(f"packet={receipt.key}; bytes={receipt.byte_count}")
        print(f"steps={','.join(events)}")
        print(f"maintenance_keys={len(archive.keys())}")
    finally:
        archive.close()
    print(f"closes={archive.close_count}")


if __name__ == "__main__":
    main()
