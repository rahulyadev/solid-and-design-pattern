"""A bounded report-policy / text-encoding Bridge; no I/O or plugin loader."""

from __future__ import annotations

import csv
import io
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Protocol, final

MAX_ITEMS = 100
MAX_QUANTITY = 1_000_000


@dataclass(frozen=True)
class StockItem:
    sku: str
    on_hand: int
    reorder_at: int

    def __post_init__(self) -> None:
        if not self.sku.strip() or len(self.sku) > 40:
            raise ValueError("sku must contain text and have at most 40 characters")
        for quantity in (self.on_hand, self.reorder_at):
            if type(quantity) is not int or not 0 <= quantity <= MAX_QUANTITY:
                raise ValueError("quantities must be plain integers in 0..1000000")


@dataclass(frozen=True)
class Table:
    """Ordered, rectangular text cells. Typed callers supply tuples, not mutable lists."""

    columns: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]

    def __post_init__(self) -> None:
        if not 1 <= len(self.columns) <= 4 or len(set(self.columns)) != len(self.columns):
            raise ValueError("require 1..4 distinct columns")
        if any(not column.strip() for column in self.columns):
            raise ValueError("column names must contain text")
        if len(self.rows) > MAX_ITEMS:
            raise ValueError("at most 100 rows")
        if any(len(row) != len(self.columns) for row in self.rows):
            raise ValueError("rows must match column count")
        if any(len(cell) > 80 for row in (self.columns, *self.rows) for cell in row):
            raise ValueError("at most 80 characters per cell")


@dataclass(frozen=True)
class Artifact:
    media_type: str
    body: str


class Encoder(Protocol):
    """Preserve ALL ordered cells, including empty tables; perform no external I/O.

    Return a fresh complete Artifact or raise. Do not filter, aggregate or retain
    mutable request state. Static typing checks signatures, not these promises.
    """

    def encode(self, table: Table, /) -> Artifact: ...


class CsvEncoder:
    def encode(self, table: Table, /) -> Artifact:
        with io.StringIO(newline="") as stream:
            writer = csv.writer(stream, lineterminator="\r\n")
            writer.writerow(table.columns)
            writer.writerows(table.rows)
            return Artifact("text/csv", stream.getvalue())


class JsonEncoder:
    def encode(self, table: Table, /) -> Artifact:
        body = json.dumps(
            {"columns": table.columns, "rows": table.rows},
            ensure_ascii=True,
            separators=(",", ":"),
        )
        return Artifact("application/json", body)


@dataclass(frozen=True)
class Report(ABC):
    """Owns report workflow; borrows the encoder without closing or replacing it."""

    encoder: Encoder

    @final
    def render(self, items: tuple[StockItem, ...]) -> Artifact:
        if len(items) > MAX_ITEMS:
            raise ValueError("at most 100 stock items")
        if len({item.sku for item in items}) != len(items):
            raise ValueError("duplicate sku")
        table = self.project(items)
        return self.encoder.encode(table)

    @abstractmethod
    def project(self, items: tuple[StockItem, ...]) -> Table:
        """Produce ordered text cells without encoding them; render validates input first."""
        raise NotImplementedError


class InventoryReport(Report):
    def project(self, items: tuple[StockItem, ...]) -> Table:
        return Table(
            ("sku", "on_hand", "reorder_at"),
            tuple((item.sku, str(item.on_hand), str(item.reorder_at)) for item in items),
        )


class ShortageReport(Report):
    def project(self, items: tuple[StockItem, ...]) -> Table:
        return Table(
            ("sku", "deficit"),
            tuple(
                (item.sku, str(item.reorder_at - item.on_hand))
                for item in items
                if item.on_hand < item.reorder_at
            ),
        )


class ReportKind(Enum):
    INVENTORY = "inventory"
    SHORTAGE = "shortage"


class OutputFormat(Enum):
    CSV = "csv"
    JSON = "json"


def make_report(kind: str, output: str) -> Report:
    """Closed configuration vocabulary; direct constructors remain open to typed collaborators."""
    report_kind = ReportKind(kind)
    output_format = OutputFormat(output)
    encoder: Encoder = CsvEncoder() if output_format is OutputFormat.CSV else JsonEncoder()
    if report_kind is ReportKind.INVENTORY:
        return InventoryReport(encoder)
    return ShortageReport(encoder)
