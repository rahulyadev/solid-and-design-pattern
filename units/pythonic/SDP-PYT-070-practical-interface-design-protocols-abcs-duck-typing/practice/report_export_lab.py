"""Concrete-coupled starter for the independent SDP-PYT-070 lab.

The dependency direction and broad vendor-shaped result are deliberate design smells.
Preserve observable behavior before changing the collaboration boundary.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Report:
    report_id: str
    content: bytes


@dataclass(frozen=True, slots=True)
class ExportRecord:
    report_id: str
    location: str


class PartnerBlobClient:
    """Synthetic stand-in for a vendor SDK client."""

    def __init__(self, bucket: str) -> None:
        self.bucket = bucket
        self.calls: list[tuple[str, bytes, str]] = []

    def put_blob(self, object_name: str, body: bytes, request_id: str) -> dict[str, str]:
        if not request_id or request_id != request_id.strip():
            raise ValueError("request_id must be non-empty and trimmed")
        self.calls.append((object_name, body, request_id))
        return {
            "bucket": self.bucket,
            "object": object_name,
            "etag": f"etag-{len(body)}",
        }


def export_report(client: PartnerBlobClient, report: Report, *, request_id: str) -> ExportRecord:
    """Export one report through a concrete, vendor-shaped dependency."""

    if not report.report_id or report.report_id != report.report_id.strip():
        raise ValueError("report_id must be non-empty and trimmed")
    if not report.content:
        raise ValueError("content must not be empty")

    object_name = f"reports/{report.report_id}.bin"
    response = client.put_blob(object_name, report.content, request_id)
    return ExportRecord(
        report_id=report.report_id,
        location=f"blob://{response['bucket']}/{response['object']}",
    )


def main() -> None:
    client = PartnerBlobClient("training-archive")
    result = export_report(
        client,
        Report("report:हिन्दी|1", b"synthetic-data"),
        request_id="request-1",
    )
    print(result)


if __name__ == "__main__":
    main()
