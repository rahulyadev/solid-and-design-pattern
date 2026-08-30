"""Composition root: select adapters, own resources, and invoke the policy."""

import sqlite3
from contextlib import closing

from coupled_replenishment import injected_concrete_plan
from memory_stock import MemoryStock
from replenishment_policy import replenishment_plan
from sqlite_stock import SqliteStock
from stock_contract import StockLevels, UnknownSku


def main() -> None:
    quantities = {"BOLT": 3, "NUT": 8, "WASHER": 0}
    targets = {"BOLT": 8, "NUT": 5, "WASHER": 0}
    memory: StockLevels = MemoryStock(quantities)
    print("DIP with memory:", replenishment_plan(targets, memory))
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.execute("CREATE TABLE inventory (sku TEXT PRIMARY KEY, quantity INTEGER)")
        connection.executemany("INSERT INTO inventory VALUES (?, ?)", quantities.items())
        connection.commit()
        sqlite_adapter = SqliteStock(connection)
        database: StockLevels = sqlite_adapter
        print("DI with concrete type:", injected_concrete_plan(targets, sqlite_adapter))
        print("DIP with SQLite:", replenishment_plan(targets, database))
        try:
            replenishment_plan({"MISSING": 5}, database)
        except UnknownSku:
            print("Unknown SKU: rejected; no order was placed")


if __name__ == "__main__":
    main()
