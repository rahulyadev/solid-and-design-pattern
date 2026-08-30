"""Decide what is missing without knowing where stock readings come from."""

from collections.abc import Mapping

from stock_contract import StockLevels


def replenishment_plan(targets: Mapping[str, int], stock: StockLevels) -> dict[str, int]:
    """Return positive shortages; validate all targets before the first read.

    Inputs are typed integer targets. No orders are placed and no stock is
    reserved. Failures propagate; the caller receives no partial plan.
    """
    if any(target < 0 for target in targets.values()):
        raise ValueError("targets must be nonnegative")
    plan: dict[str, int] = {}
    for sku, target in targets.items():
        shortage = target - stock.units_available(sku)
        if shortage > 0:
            plan[sku] = shortage
    return plan
