"""Unsolved exercise: deciding when export bytes may be shared is learner work."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ExportRequest:
    team: str
    report: str
    revision: int
    locale: str


class Exporter(Protocol):
    def export(self, request: ExportRequest, /) -> bytes: ...


class CountingExporter:
    def __init__(self) -> None:
        self.calls = 0

    def export(self, request: ExportRequest, /) -> bytes:
        self.calls += 1
        return (f"{request.team}/{request.report}@{request.revision}:{request.locale}").encode()


def eager_preview(exporter: Exporter, request: ExportRequest, permitted: bool) -> bytes:
    data = exporter.export(request)
    if not permitted:
        raise PermissionError("preview denied")
    return data


def build_preview(exporter: Exporter) -> Exporter:
    """Choose and defend the final API in your own attempt; see the brief."""
    raise NotImplementedError("Complete the predict/run/observe/explain stages first")


if __name__ == "__main__":
    source = CountingExporter()
    request = ExportRequest("orchard", "weekly", 1, "en")
    try:
        eager_preview(source, request, False)
    except PermissionError:
        print(f"denied=True, exports={source.calls}")
    try:
        build_preview(source)
    except NotImplementedError:
        print("target_complete=False")
