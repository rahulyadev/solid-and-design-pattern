"""Optional method-based Strategy comparison, using the same validation core."""

from dataclasses import dataclass
from typing import Protocol

from strategy import Jobs, Order, Plan, SmallJobsFirst, plan


class Ordering(Protocol):
    def order(self, jobs: Jobs, /) -> Order: ...


@dataclass(frozen=True)
class SmallFirstOrdering:
    """A named operation around configured behavior, without inheritance."""

    policy: SmallJobsFirst

    def order(self, batch: Jobs, /) -> Order:
        return self.policy(batch)


@dataclass(frozen=True)
class ObjectPlanner:
    ordering: Ordering

    def plan(self, jobs: Jobs) -> Plan:
        return plan(jobs, self.ordering.order)
