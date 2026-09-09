"""Behavior and semantic contracts, including valid signatures with wrong behavior."""

import csv
import io
import json
from collections.abc import Callable
from dataclasses import FrozenInstanceError

import pytest
from bridge import (
    MAX_ITEMS,
    MAX_QUANTITY,
    Artifact,
    CsvEncoder,
    Encoder,
    InventoryReport,
    JsonEncoder,
    Report,
    ShortageReport,
    StockItem,
    Table,
    make_report,
)
from matrix_probe import Observation, RecordingEncoder, observe

ENCODERS: tuple[Encoder, ...] = (CsvEncoder(), JsonEncoder())
REPORTS: tuple[type[Report], ...] = (InventoryReport, ShortageReport)
ITEMS = (StockItem('clip,"青\n', 3, 5), StockItem("tray", 8, 8))


def decode(artifact: Artifact) -> tuple[list[str], list[list[str]]]:
    if artifact.media_type == "text/csv":
        records = list(csv.reader(io.StringIO(artifact.body, newline="")))
        return records[0], records[1:]
    value = json.loads(artifact.body)
    return value["columns"], value["rows"]


@pytest.mark.parametrize("encoder", ENCODERS)
@pytest.mark.parametrize("report_type", REPORTS)
def test_all_combinations_preserve_report_meaning(
    encoder: Encoder, report_type: type[Report]
) -> None:
    columns, rows = decode(report_type(encoder).render(ITEMS))
    if report_type is InventoryReport:
        assert columns == ["sku", "on_hand", "reorder_at"]
        assert rows == [['clip,"青\n', "3", "5"], ["tray", "8", "8"]]
    else:
        assert columns == ["sku", "deficit"]
        assert rows == [['clip,"青\n', "2"]]


@pytest.mark.parametrize("encoder", ENCODERS)
@pytest.mark.parametrize("report_type", REPORTS)
def test_empty_reports_keep_schema(encoder: Encoder, report_type: type[Report]) -> None:
    columns, rows = decode(report_type(encoder).render(()))
    assert columns == (
        ["sku", "on_hand", "reorder_at"] if report_type is InventoryReport else ["sku", "deficit"]
    )
    assert rows == []


@pytest.mark.parametrize("encoder", ENCODERS)
def test_encoder_contract_preserves_order_empty_cells_and_duplicates(encoder: Encoder) -> None:
    table = Table(("a", "b"), (("", "x"), ("", "x"), ('\r\n\t,"', "🙂")))
    first, second = encoder.encode(table), encoder.encode(table)
    assert first == second
    assert first is not second
    assert decode(first) == (list(table.columns), [list(row) for row in table.rows])


@pytest.mark.parametrize("quantity", [-1, MAX_QUANTITY + 1, True])
def test_invalid_on_hand(quantity: int) -> None:
    with pytest.raises(ValueError, match="quantities"):
        StockItem("clip", quantity, 5)


@pytest.mark.parametrize("quantity", [-1, MAX_QUANTITY + 1, False])
def test_invalid_reorder(quantity: int) -> None:
    with pytest.raises(ValueError, match="quantities"):
        StockItem("clip", 5, quantity)


@pytest.mark.parametrize("sku", ["", " \t", "x" * 41])
def test_invalid_sku(sku: str) -> None:
    with pytest.raises(ValueError, match="sku"):
        StockItem(sku, 1, 2)


def test_quantity_and_sku_bounds() -> None:
    item = StockItem("x" * 40, 0, MAX_QUANTITY)
    assert decode(ShortageReport(JsonEncoder()).render((item,)))[1] == [[item.sku, "1000000"]]


@pytest.mark.parametrize("report_type", REPORTS)
def test_validation_happens_before_encoding(report_type: type[Report]) -> None:
    recorder = RecordingEncoder(CsvEncoder())
    with pytest.raises(ValueError, match="duplicate sku"):
        report_type(recorder).render((ITEMS[0], ITEMS[0]))
    assert recorder.seen == []


@pytest.mark.parametrize("size", [MAX_ITEMS, MAX_ITEMS + 1])
def test_inventory_bound(size: int) -> None:
    recorder = RecordingEncoder(JsonEncoder())
    items = tuple(StockItem(str(i), 1, 0) for i in range(size))
    if size > MAX_ITEMS:
        with pytest.raises(ValueError, match="at most 100 stock"):
            ShortageReport(recorder).render(items)
        assert recorder.seen == []
    else:
        assert len(decode(InventoryReport(recorder).render(items))[1]) == size


@pytest.mark.parametrize(
    "factory",
    [
        lambda: Table((), ()),
        lambda: Table(("a",) * 2, ()),
        lambda: Table((" ",), ()),
        lambda: Table(("a", "b", "c", "d", "e"), ()),
        lambda: Table(("a",), (("1", "2"),)),
        lambda: Table(("a",), (("",),) * 101),
        lambda: Table(("a",), (("x" * 81,),)),
        lambda: Table(("a" * 81,), ()),
    ],
)
def test_invalid_table(factory: Callable[[], Table]) -> None:
    with pytest.raises(ValueError):
        factory()


def test_table_cell_boundary() -> None:
    table = Table(("a" * 80,), (("x" * 80,),))
    assert decode(CsvEncoder().encode(table)) == (["a" * 80], [["x" * 80]])


@pytest.mark.parametrize(
    "kind,output", [("unknown", "csv"), ("inventory", "xml"), ("Inventory", "json")]
)
def test_invalid_configuration(kind: str, output: str) -> None:
    with pytest.raises(ValueError):
        make_report(kind, output)


@pytest.mark.parametrize("kind", ["inventory", "shortage"])
@pytest.mark.parametrize("output", ["csv", "json"])
def test_explicit_configuration(kind: str, output: str) -> None:
    artifact = make_report(kind, output).render(ITEMS)
    assert artifact.media_type == ("text/csv" if output == "csv" else "application/json")
    assert len(decode(artifact)[1]) == (2 if kind == "inventory" else 1)


def test_failure_propagates_once_without_retry_or_fallback() -> None:
    failure = OSError("synthetic encoder failure")

    class FailingEncoder:
        calls = 0

        def encode(self, table: Table, /) -> Artifact:
            self.calls += 1
            raise failure

    encoder = FailingEncoder()
    with pytest.raises(OSError) as raised:
        InventoryReport(encoder).render(ITEMS)
    assert raised.value is failure
    assert encoder.calls == 1


def test_projection_failure_never_calls_encoder() -> None:
    class BrokenReport(Report):
        def project(self, items: tuple[StockItem, ...]) -> Table:
            raise ValueError("synthetic projection failure")

    encoder = RecordingEncoder(JsonEncoder())
    with pytest.raises(ValueError, match="projection"):
        BrokenReport(encoder).render(ITEMS)
    assert encoder.seen == []


def test_one_new_policy_works_with_both_existing_encoders() -> None:
    class ZeroStockReport(Report):
        def project(self, items: tuple[StockItem, ...]) -> Table:
            return Table(("sku",), tuple((item.sku,) for item in items if item.on_hand == 0))

    items = (StockItem("zero", 0, 0), *ITEMS)
    for encoder in ENCODERS:
        assert decode(ZeroStockReport(encoder).render(items)) == (["sku"], [["zero"]])


def test_new_implementor_works_with_both_policies_without_inheritance() -> None:
    class ReadableEncoder:
        def encode(self, table: Table, /) -> Artifact:
            return Artifact("text/plain", repr((table.columns, table.rows)))

    encoder: Encoder = ReadableEncoder()
    for report_type in REPORTS:
        report = report_type(encoder)
        assert report.render(ITEMS).body == repr(
            (report.project(ITEMS).columns, report.project(ITEMS).rows)
        )


def test_semantic_liar_has_valid_signature_but_fails_cell_preservation() -> None:
    class DroppingEncoder:
        def encode(self, table: Table, /) -> Artifact:
            return JsonEncoder().encode(Table(table.columns, ()))

    liar: Encoder = DroppingEncoder()
    artifact = InventoryReport(liar).render(ITEMS)
    assert decode(artifact)[1] != [
        [item.sku, str(item.on_hand), str(item.reorder_at)] for item in ITEMS
    ]
    # The client trusts the contract; this passing test demonstrates its limitation.


def test_borrowing_and_repeated_calls_do_not_leak_rows() -> None:
    encoder = JsonEncoder()
    report = InventoryReport(encoder)
    before = report.render(ITEMS)
    assert decode(report.render(()))[1] == []
    assert report.encoder is encoder
    assert report.render(ITEMS) == before
    assert ShortageReport(encoder).render(ITEMS).body != before.body


def test_normal_field_reassignment_is_blocked() -> None:
    report = InventoryReport(JsonEncoder())
    with pytest.raises(FrozenInstanceError):
        setattr(report, "encoder", CsvEncoder())  # noqa: B010 -- deliberate runtime mutation probe
    with pytest.raises(FrozenInstanceError):
        setattr(ITEMS[0], "on_hand", 99)  # noqa: B010 -- deliberate runtime mutation probe


def test_matrix_observations() -> None:
    assert observe() == (
        Observation("InventoryReport", "CsvEncoder", 2, 1),
        Observation("InventoryReport", "JsonEncoder", 2, 1),
        Observation("ShortageReport", "CsvEncoder", 1, 1),
        Observation("ShortageReport", "JsonEncoder", 1, 1),
    )
