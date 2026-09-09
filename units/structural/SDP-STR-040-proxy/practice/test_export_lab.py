import pytest
from export_lab import CountingExporter, ExportRequest, build_preview, eager_preview


def test_baseline_success() -> None:
    source = CountingExporter()
    request = ExportRequest("orchard", "weekly", 1, "en")
    assert eager_preview(source, request, True) == b"orchard/weekly@1:en"
    assert source.calls == 1


def test_baseline_exposes_work_before_denial() -> None:
    source = CountingExporter()
    with pytest.raises(PermissionError):
        eager_preview(source, ExportRequest("orchard", "weekly", 1, "en"), False)
    assert source.calls == 1


def test_target_is_deliberately_unsolved() -> None:
    with pytest.raises(NotImplementedError):
        build_preview(CountingExporter())
