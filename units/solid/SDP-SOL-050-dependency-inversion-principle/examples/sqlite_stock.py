"""Translate one SQLite schema into the stock contract; borrow the connection."""

import sqlite3
from contextlib import closing

from stock_contract import StockUnavailable, UnknownSku


class SqliteStock:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def units_available(self, sku: str, /) -> int:
        try:
            with closing(
                self._connection.execute("SELECT quantity FROM inventory WHERE sku = ?", (sku,))
            ) as cursor:
                row = cursor.fetchone()
        except sqlite3.OperationalError as error:
            raise StockUnavailable("stock query failed") from error
        if row is None:
            raise UnknownSku(sku)
        quantity: object = row[0]
        if type(quantity) is not int or quantity < 0:
            raise StockUnavailable("stock quantity must be a nonnegative integer")
        return quantity
