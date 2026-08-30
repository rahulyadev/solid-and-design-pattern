"""Observable policy and adapter contracts, including real in-memory SQLite."""

import sqlite3
from collections.abc import Iterator
from contextlib import closing

import pytest
from coupled_replenishment import injected_concrete_plan
from memory_stock import MemoryStock
from replenishment_policy import replenishment_plan
from sqlite_stock import SqliteStock
from stock_contract import StockLevels, StockUnavailable, UnknownSku


@pytest.fixture(params=["memory", "sqlite"])
def stock(request: pytest.FixtureRequest) -> Iterator[StockLevels]:
    quantities = {"BOLT": 3, "NUT": 8, "WASHER": 0, "螺母": 2, "quote'key": 4}
    if request.param == "memory":
        yield MemoryStock(quantities)
    else:
        with closing(sqlite3.connect(":memory:")) as connection:
            connection.execute("CREATE TABLE inventory (sku TEXT PRIMARY KEY, quantity INTEGER)")
            connection.executemany("INSERT INTO inventory VALUES (?, ?)", quantities.items())
            connection.commit()
            yield SqliteStock(connection)


def test_positive_shortages_only_and_no_input_mutation(stock: StockLevels) -> None:
    targets = {"BOLT": 8, "NUT": 5, "WASHER": 0}
    assert replenishment_plan(targets, stock) == {"BOLT": 5}
    assert targets == {"BOLT": 8, "NUT": 5, "WASHER": 0}
    assert stock.units_available("BOLT") == 3


def test_zero_stock_is_a_valid_reading(stock: StockLevels) -> None:
    assert replenishment_plan({"WASHER": 6}, stock) == {"WASHER": 6}


def test_unknown_stock_is_not_zero(stock: StockLevels) -> None:
    with pytest.raises(UnknownSku):
        replenishment_plan({"MISSING": 6}, stock)


def test_unicode_and_quoted_keys(stock: StockLevels) -> None:
    assert replenishment_plan({"螺母": 4, "quote'key": 5}, stock) == {"螺母": 2, "quote'key": 1}


def test_repeated_reads_are_non_destructive(stock: StockLevels) -> None:
    assert stock.units_available("BOLT") == stock.units_available("BOLT") == 3


class UnavailableStock:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def units_available(self, sku: str, /) -> int:
        self.calls.append(sku)
        raise StockUnavailable("source offline")


def test_empty_plan_makes_no_read() -> None:
    stock = UnavailableStock()
    assert replenishment_plan({}, stock) == {}
    assert stock.calls == []


def test_all_targets_validated_before_first_read() -> None:
    stock = UnavailableStock()
    with pytest.raises(ValueError, match="nonnegative"):
        replenishment_plan({"BOLT": 5, "NUT": -1}, stock)
    assert stock.calls == []


def test_failure_is_not_silently_turned_into_a_plan() -> None:
    stock = UnavailableStock()
    with pytest.raises(StockUnavailable, match="offline"):
        replenishment_plan({"BOLT": 5}, stock)
    assert stock.calls == ["BOLT"]


def test_later_read_failure_does_not_return_partial_plan() -> None:
    class FailingSecondRead:
        def __init__(self) -> None:
            self.calls: list[str] = []

        def units_available(self, sku: str, /) -> int:
            self.calls.append(sku)
            if sku == "NUT":
                raise StockUnavailable("second read failed")
            return 0

    stock = FailingSecondRead()
    with pytest.raises(StockUnavailable, match="second read"):
        replenishment_plan({"BOLT": 5, "NUT": 4}, stock)
    assert stock.calls == ["BOLT", "NUT"]


def test_memory_adapter_copies_input() -> None:
    quantities = {"BOLT": 3}
    stock = MemoryStock(quantities)
    quantities["BOLT"] = 99
    assert stock.units_available("BOLT") == 3


def test_memory_adapter_rejects_negative_quantity() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        MemoryStock({"BOLT": -1})


@pytest.mark.parametrize("quantity", [-1, "invalid", None, 1.5])
def test_sqlite_adapter_rejects_invalid_storage_values(quantity: object) -> None:
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.execute("CREATE TABLE inventory (sku TEXT PRIMARY KEY, quantity)")
        connection.execute("INSERT INTO inventory VALUES (?, ?)", ("BOLT", quantity))
        with pytest.raises(StockUnavailable, match="nonnegative integer"):
            SqliteStock(connection).units_available("BOLT")


def test_sqlite_operational_error_is_translated_with_cause() -> None:
    with closing(sqlite3.connect(":memory:")) as connection:
        with pytest.raises(StockUnavailable) as caught:
            SqliteStock(connection).units_available("BOLT")
        assert isinstance(caught.value.__cause__, sqlite3.OperationalError)


def test_closed_connection_is_a_programming_error() -> None:
    connection = sqlite3.connect(":memory:")
    stock = SqliteStock(connection)
    connection.close()
    with pytest.raises(sqlite3.ProgrammingError):
        stock.units_available("BOLT")


def test_concrete_injection_has_same_result_without_same_source_boundary() -> None:
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.execute("CREATE TABLE inventory (sku TEXT PRIMARY KEY, quantity INTEGER)")
        connection.execute("INSERT INTO inventory VALUES ('BOLT', 3)")
        stock = SqliteStock(connection)
        assert injected_concrete_plan({"BOLT": 8}, stock) == {"BOLT": 5}
        assert replenishment_plan({"BOLT": 8}, stock) == {"BOLT": 5}


def test_concrete_counterexample_also_validates_targets() -> None:
    with (
        closing(sqlite3.connect(":memory:")) as connection,
        pytest.raises(ValueError, match="nonnegative"),
    ):
        injected_concrete_plan({"BOLT": -1}, SqliteStock(connection))
