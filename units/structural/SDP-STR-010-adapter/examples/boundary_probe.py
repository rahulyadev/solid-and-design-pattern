"""Controlled evidence: a valid method shape need not preserve meaning."""

from typing import Protocol, runtime_checkable

from legacy_warehouse import LegacyWarehouse
from stock_contract import Stock, StockReader, availability
from warehouse_adapter import WarehouseAdapter


class CountsCases:
    def read(self, sku: str, /) -> Stock:
        return Stock(2)  # Compatible signature, wrong agreed unit for this fixture.


@runtime_checkable
class ReadShape(Protocol):
    def read(self, sku: str, /) -> Stock: ...


class WrongSignature:
    def read(self, sku: int, required: int, /) -> str:
        return "wrong"


def call_after_presence_check(candidate: object) -> None:
    if isinstance(candidate, ReadShape):
        candidate.read("BOLT")


def observations() -> dict[str, object]:
    warehouse = LegacyWarehouse({"BOLT": {"schema": 1, "item": "BOLT", "pack_size": 6, "cases": 2}})
    good: StockReader = WarehouseAdapter(warehouse)
    bad: StockReader = CountsCases()  # Static checking deliberately accepts this.
    shape = WrongSignature()
    try:
        # Static narrowing trusts a runtime check that does not check signatures.
        call_after_presence_check(shape)
    except TypeError:
        call_failed = True
    else:
        call_failed = False
    return {
        "converted_units": good.read("BOLT").units,
        "converted_decision": availability(good, "BOLT", 10),
        "signature_only_decision": availability(bad, "BOLT", 10),
        "runtime_shape_accepts_wrong_signature": isinstance(shape, ReadShape),
        "actual_call_raises_type_error": call_failed,
    }


if __name__ == "__main__":
    for key, value in observations().items():
        print(f"{key}={value}")
