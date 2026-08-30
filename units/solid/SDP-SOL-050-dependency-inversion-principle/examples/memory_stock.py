"""A snapshot adapter for the consumer's stock contract."""

from collections.abc import Mapping

from stock_contract import UnknownSku


class MemoryStock:
    def __init__(self, quantities: Mapping[str, int]) -> None:
        if any(quantity < 0 for quantity in quantities.values()):
            raise ValueError("quantities must be nonnegative")
        self._quantities = dict(quantities)

    def units_available(self, sku: str, /) -> int:
        try:
            return self._quantities[sku]
        except KeyError as error:
            raise UnknownSku(sku) from error
