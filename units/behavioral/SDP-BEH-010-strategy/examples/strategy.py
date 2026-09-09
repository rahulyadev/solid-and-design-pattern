"""A bounded synthetic print-batch planner; it orders jobs but never prints them."""

from collections.abc import Callable
from dataclasses import dataclass


def _bounded_int(value: int, low: int, high: int, name: str) -> None:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in {low}..{high}")


@dataclass(frozen=True)
class Job:
    job_id: int
    pages: int

    def __post_init__(self) -> None:
        _bounded_int(self.job_id, 0, 999_999, "job_id")
        _bounded_int(self.pages, 1, 100, "pages")


Jobs = tuple[Job, ...]
Order = tuple[int, ...]
OrderPolicy = Callable[[Jobs], Order]


@dataclass(frozen=True)
class Plan:
    job_ids: Order
    total_pages: int


class PolicyContractError(ValueError):
    """The policy returned a result that cannot represent this complete batch."""


def plan(jobs: Jobs, policy: OrderPolicy) -> Plan:
    """Validate input, invoke one policy once, validate its result, build a value.

    Typed tuple/Job inputs are required. No printing, retries, fallback, or I/O occurs.
    Policy exceptions propagate unchanged; no Plan is returned on failure.
    """
    if len(jobs) > 64:
        raise ValueError("a batch may contain at most 64 jobs")
    expected = {job.job_id for job in jobs}
    if len(expected) != len(jobs):
        raise ValueError("job IDs must be unique within a batch")
    order = policy(jobs)
    # Check exact integers: True compares equal to job ID 1 but is not an ID here.
    if type(order) is not tuple or any(type(item) is not int for item in order):
        raise PolicyContractError("policy must return a tuple of integer job IDs")
    if len(order) != len(jobs) or set(order) != expected:
        raise PolicyContractError("policy must return each input job ID exactly once")
    return Plan(order, sum(job.pages for job in jobs))


def arrival_order(jobs: Jobs) -> Order:
    return tuple(job.job_id for job in jobs)


def fewest_pages(jobs: Jobs) -> Order:
    """Ascending page count, with arrival order breaking ties."""
    return tuple(job.job_id for job in sorted(jobs, key=lambda job: job.pages))


def _small_order(jobs: Jobs, cutoff: int) -> Order:
    """Stable partition, not an ascending sort inside either group."""
    return tuple(job.job_id for job in jobs if job.pages <= cutoff) + tuple(
        job.job_id for job in jobs if job.pages > cutoff
    )


def small_jobs_first(cutoff: int) -> OrderPolicy:
    """Capture one validated immutable configuration value per factory call."""
    _bounded_int(cutoff, 1, 100, "cutoff")

    def order(jobs: Jobs) -> Order:
        return _small_order(jobs, cutoff)

    return order


@dataclass(frozen=True)
class SmallJobsFirst:
    """The same policy with explicit, inspectable configuration on a callable object."""

    cutoff: int

    def __post_init__(self) -> None:
        _bounded_int(self.cutoff, 1, 100, "cutoff")

    def __call__(self, jobs: Jobs) -> Order:
        return _small_order(jobs, self.cutoff)


def select_policy(name: str, *, cutoff: int = 5) -> OrderPolicy:
    """Application-boundary selection; cutoff applies only to the small policy."""
    if name == "arrival":
        return arrival_order
    if name == "fewest":
        return fewest_pages
    if name == "small":
        return small_jobs_first(cutoff)
    raise ValueError(f"unknown ordering policy: {name}")
