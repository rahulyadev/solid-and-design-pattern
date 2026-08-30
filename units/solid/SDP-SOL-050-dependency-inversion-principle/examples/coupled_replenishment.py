"""Deliberate counterexample: injected object, but a concrete source dependency."""

from collections.abc import Mapping

from sqlite_stock import SqliteStock


def injected_concrete_plan(targets: Mapping[str, int], stock: SqliteStock) -> dict[str, int]:
    """Construction moved outside; the policy module still imports infrastructure."""
    if any(target < 0 for target in targets.values()):
        raise ValueError("targets must be nonnegative")
    plan: dict[str, int] = {}
    for sku, target in targets.items():
        shortage = target - stock.units_available(sku)
        if shortage > 0:
            plan[sku] = shortage
    return plan
