"""Characterization tests for the unsolved concrete-coupled starter."""

import pytest
from report_export_lab import ExportRecord, PartnerBlobClient, Report, export_report


def test_export_translates_report_to_vendor_call() -> None:
    client = PartnerBlobClient("training-archive")
    report = Report("report:हिन्दी|1", b"payload|with:punctuation")

    result = export_report(client, report, request_id="request:1|retry")

    assert result == ExportRecord(
        report_id="report:हिन्दी|1",
        location="blob://training-archive/reports/report:हिन्दी|1.bin",
    )
    assert client.calls == [
        (
            "reports/report:हिन्दी|1.bin",
            b"payload|with:punctuation",
            "request:1|retry",
        )
    ]


@pytest.mark.parametrize("report_id", ["", " leading", "trailing "])
def test_invalid_report_id_fails_before_vendor_call(report_id: str) -> None:
    client = PartnerBlobClient("training-archive")

    with pytest.raises(ValueError, match="report_id"):
        export_report(client, Report(report_id, b"payload"), request_id="request-1")

    assert client.calls == []


def test_empty_content_fails_before_vendor_call() -> None:
    client = PartnerBlobClient("training-archive")

    with pytest.raises(ValueError, match="content"):
        export_report(client, Report("report-1", b""), request_id="request-1")

    assert client.calls == []


@pytest.mark.parametrize("request_id", ["", " leading", "trailing "])
def test_invalid_request_id_does_not_record_a_call(request_id: str) -> None:
    client = PartnerBlobClient("training-archive")

    with pytest.raises(ValueError, match="request_id"):
        export_report(
            client,
            Report("report-1", b"payload"),
            request_id=request_id,
        )

    assert client.calls == []


def test_partner_failure_is_not_hidden() -> None:
    class FailingPartner(PartnerBlobClient):
        def put_blob(self, object_name: str, body: bytes, request_id: str) -> dict[str, str]:
            raise TimeoutError("synthetic timeout")

    with pytest.raises(TimeoutError, match="synthetic timeout"):
        export_report(
            FailingPartner("training-archive"),
            Report("report-1", b"payload"),
            request_id="request-1",
        )
