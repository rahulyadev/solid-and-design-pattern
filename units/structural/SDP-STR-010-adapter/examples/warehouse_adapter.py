"""One explicit schema-v1 boundary, with no cache or retry policy."""

from legacy_warehouse import LegacyWarehouse, WarehouseTimeout
from stock_contract import InvalidStock, Stock, StockUnavailable, validate_sku


def decode_stock(payload: object, expected_sku: str) -> Stock:
    """Accept decoded JSON shapes only; preserve unknown rather than invent zero."""
    if payload is None:
        return Stock(None)
    if not isinstance(payload, dict):
        raise InvalidStock("expected a warehouse record")
    if type(payload.get("schema")) is not int or payload.get("schema") != 1:
        raise InvalidStock("unsupported warehouse schema")
    if payload.get("item") != expected_sku:
        raise InvalidStock("warehouse item mismatch")
    pack = payload.get("pack_size")
    if type(pack) is not int or not 1 <= pack <= 1000:
        raise InvalidStock("invalid pack size")
    if "cases" not in payload:
        raise InvalidStock("missing case count")
    cases = payload["cases"]
    if cases is None:
        return Stock(None)
    if type(cases) is not int or not 0 <= cases <= 1_000_000:
        raise InvalidStock("invalid case count")
    return Stock(cases * pack)


class WarehouseAdapter:
    def __init__(self, warehouse: LegacyWarehouse) -> None:
        self._warehouse = warehouse  # Borrowed; the composition root owns close().

    def read(self, sku: str, /) -> Stock:
        validate_sku(sku)
        try:
            payload = self._warehouse.fetch_cases(item_code=sku)
        except WarehouseTimeout as error:
            raise StockUnavailable("stock provider unavailable") from error
        return decode_stock(payload, sku)
