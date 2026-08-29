"""Unsolved SDP-FND-040 starter with a public mutable representation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class OperationUsage:
    """One operation total in an externally displayed report."""

    operation: str
    units: int


@dataclass(frozen=True, slots=True)
class UsageReport:
    """Observable report produced by the current starter."""

    tenant_id: str
    limit_units: int
    used_units: int
    remaining_units: int
    by_operation: tuple[OperationUsage, ...]


@dataclass
class QuotaAccount:
    """Deliberately leak the quota ledger so the boundary can be diagnosed."""

    tenant_id: str
    limit_units: int
    usage_entries: list[tuple[str, int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        assert self.tenant_id.strip(), "tenant_id must not be blank"
        assert self.limit_units >= 0, "limit_units must be non-negative"

    @property
    def used_units(self) -> int:
        """Derive total usage from the currently public ledger."""

        return sum(units for _, units in self.usage_entries)

    @property
    def remaining_units(self) -> int:
        """Return the current limit minus all ledger entries."""

        return self.limit_units - self.used_units

    def consume(self, operation: str, units: int) -> None:
        """Append usage after debug-only assertion checks."""

        assert operation.strip(), "operation must not be blank"
        assert units > 0, "units must be positive"
        assert units <= self.remaining_units, "quota exceeded"
        self.usage_entries.append((operation, units))


def build_usage_report(account: QuotaAccount) -> UsageReport:
    """Read the public ledger directly, coupling this client to its shape."""

    totals: dict[str, int] = {}
    for operation, units in account.usage_entries:
        totals[operation] = totals.get(operation, 0) + units

    by_operation = tuple(
        OperationUsage(operation, units) for operation, units in sorted(totals.items())
    )
    return UsageReport(
        tenant_id=account.tenant_id,
        limit_units=account.limit_units,
        used_units=account.used_units,
        remaining_units=account.remaining_units,
        by_operation=by_operation,
    )


def main() -> None:
    """Run a deterministic example for prediction and observation."""

    account = QuotaAccount("tenant-demo", limit_units=500)
    account.consume("embedding", 40)
    account.consume("generation", 120)
    account.consume("generation", 30)

    print(build_usage_report(account))
    print(f"public usage_entries={account.usage_entries}")


if __name__ == "__main__":
    main()
