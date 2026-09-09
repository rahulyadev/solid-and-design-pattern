"""Positive structural assignments; no I/O or live resources are acquired."""

from lifetimes import MemoryReader, OwnedReader, Reader, ReportService


class FixedReader:
    def lookup(self, key: str) -> str:
        return "synthetic"


reader: Reader = FixedReader()
owned: OwnedReader = MemoryReader({}, revision="r1")
service = ReportService(reader)
