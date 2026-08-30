"""Consumer-owned stock boundary; no storage or framework imports."""

from typing import Protocol


class UnknownSku(LookupError):
    """The requested SKU is not known; this is different from zero stock."""


class StockUnavailable(RuntimeError):
    """A trustworthy stock reading could not be obtained; retry is not guaranteed safe/useful."""


class StockLevels(Protocol):
    def units_available(self, sku: str, /) -> int:
        """Return nonnegative stock, or raise UnknownSku / StockUnavailable.

        Reading does not reserve or change stock. Separate reads need not belong
        to one snapshot. Callers supply string SKUs; adapters own data validation.
        Programming errors are not translated into availability failures.
        """
        ...
