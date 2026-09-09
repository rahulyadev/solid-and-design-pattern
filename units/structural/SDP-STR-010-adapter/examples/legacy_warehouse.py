"""Synthetic external SDK. Its shape deliberately differs from StockReader."""


class WarehouseTimeout(Exception):
    pass


class LegacyWarehouse:
    def __init__(self, rows: dict[str, object]) -> None:
        self.rows = dict(rows)
        self.calls: list[str] = []
        self.closed = False
        self.close_count = 0
        self.fail_next = False

    def fetch_cases(self, *, item_code: str) -> object:
        if self.closed:
            raise RuntimeError("warehouse is closed")
        self.calls.append(item_code)
        if self.fail_next:
            self.fail_next = False
            raise WarehouseTimeout("synthetic vendor diagnostic")
        return self.rows.get(item_code)

    def close(self) -> None:
        self.closed = True
        self.close_count += 1
