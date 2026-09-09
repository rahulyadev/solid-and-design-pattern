"""Run from the repository root or this directory; no network access."""

from contextlib import closing

from legacy_warehouse import LegacyWarehouse
from stock_contract import StockReader, availability
from warehouse_adapter import WarehouseAdapter


def main() -> None:
    row = {"schema": 1, "item": "BOLT", "pack_size": 6, "cases": 2}
    with closing(LegacyWarehouse({"BOLT": row})) as warehouse:
        reader: StockReader = WarehouseAdapter(warehouse)
        print(availability(reader, "BOLT", 10))
        print(availability(reader, "UNKNOWN", 1))
        row["cases"] = 0
        print(availability(reader, "BOLT", 1))
        print(f"queries={len(warehouse.calls)}")
    print(f"closes={warehouse.close_count}")


if __name__ == "__main__":
    main()
