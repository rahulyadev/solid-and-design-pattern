"""Run the worked SDP-PYT-040 streaming example."""

from streaming_reports import MemoryAlertSink, export_important_alerts


def main() -> None:
    lines = [
        "a-1|2|queued",
        "a-2|5|worker unavailable",
        "a-3|4|retry scheduled",
        "a-4|1|healthy",
    ]
    trace: list[str] = []
    sink = MemoryAlertSink()

    written = export_important_alerts(
        lines,
        minimum_severity=4,
        batch_size=2,
        sink_factory=lambda: sink,
        trace=trace.append,
    )

    print(f"written={written}")
    print(f"rows={tuple(sink.rows)!r}")
    print(f"closed={sink.closed}")
    print(f"trace={tuple(trace)!r}")


if __name__ == "__main__":
    main()
