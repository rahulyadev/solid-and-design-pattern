"""Behavioral contracts, selection ownership, and bounded permutation properties."""

from collections.abc import Callable
from dataclasses import FrozenInstanceError
from typing import cast

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from object_strategy import ObjectPlanner, SmallFirstOrdering
from strategy import (
    Job,
    Jobs,
    Order,
    OrderPolicy,
    Plan,
    PolicyContractError,
    SmallJobsFirst,
    arrival_order,
    fewest_pages,
    plan,
    select_policy,
    small_jobs_first,
)

JOBS = (Job(7, 8), Job(2, 3), Job(9, 3), Job(5, 1))
POLICIES: tuple[OrderPolicy, ...] = (
    arrival_order,
    fewest_pages,
    small_jobs_first(5),
    SmallJobsFirst(5),
)


@pytest.mark.parametrize(
    ("name", "expected"),
    [("arrival", (7, 2, 9, 5)), ("fewest", (5, 2, 9, 7)), ("small", (2, 9, 5, 7))],
)
def test_demo_observations(name: str, expected: Order) -> None:
    assert plan(JOBS, select_policy(name)) == Plan(expected, 15)


@pytest.mark.parametrize("policy", POLICIES)
@pytest.mark.parametrize("jobs", [(), (Job(0, 100),), JOBS])
def test_shared_contract(policy: OrderPolicy, jobs: Jobs) -> None:
    before = tuple((job.job_id, job.pages) for job in jobs)
    first = plan(jobs, policy)
    assert len(first.job_ids) == len(jobs)
    assert set(first.job_ids) == {job.job_id for job in jobs}
    assert first.total_pages == sum(job.pages for job in jobs)
    assert tuple((job.job_id, job.pages) for job in jobs) == before
    assert plan(jobs, policy) == first


@settings(max_examples=60, derandomize=True)
@given(st.lists(st.integers(min_value=1, max_value=100), max_size=64))
def test_bounded_policy_properties(pages: list[int]) -> None:
    jobs = tuple(Job(i, count) for i, count in enumerate(pages))
    for policy in POLICIES:
        result = plan(jobs, policy)
        assert sorted(result.job_ids) == list(range(len(jobs)))
        assert result.total_pages == sum(pages)
    ordered = plan(jobs, fewest_pages).job_ids
    assert [pages[i] for i in ordered] == sorted(pages)
    for page_count in set(pages):
        assert [i for i in ordered if pages[i] == page_count] == [
            i for i, count in enumerate(pages) if count == page_count
        ]
    assert plan(jobs, small_jobs_first(5)) == plan(jobs, SmallJobsFirst(5))


@pytest.mark.parametrize("cutoff", [1, 3, 5, 100])
def test_partition_preserves_arrival_within_each_group(cutoff: int) -> None:
    result = plan(JOBS, small_jobs_first(cutoff))
    assert result.job_ids == tuple(j.job_id for j in JOBS if j.pages <= cutoff) + tuple(
        j.job_id for j in JOBS if j.pages > cutoff
    )


def test_closure_configuration_is_independent() -> None:
    cutoff = 1
    first = small_jobs_first(cutoff)
    cutoff = 100
    second = small_jobs_first(cutoff)
    assert plan(JOBS, first).job_ids == (5, 7, 2, 9)
    assert plan(JOBS, second).job_ids == (7, 2, 9, 5)
    assert plan(JOBS, first).job_ids == (5, 7, 2, 9)


@pytest.mark.parametrize("jobs", [(), JOBS])
def test_context_invokes_selected_policy_once_with_input(jobs: Jobs) -> None:
    seen: list[Jobs] = []

    def reverse(batch: Jobs) -> Order:
        seen.append(batch)
        return tuple(job.job_id for job in reversed(batch))

    assert plan(jobs, reverse).job_ids == tuple(j.job_id for j in reversed(jobs))
    assert len(seen) == 1 and seen[0] is jobs


@pytest.mark.parametrize("jobs", [(Job(1, 1), Job(1, 2)), tuple(Job(i, 1) for i in range(65))])
def test_input_failure_precedes_policy(jobs: Jobs) -> None:
    def must_not_run(batch: Jobs) -> Order:
        pytest.fail("invalid input reached policy")

    with pytest.raises(ValueError):
        plan(jobs, must_not_run)


@pytest.mark.parametrize("error", [RuntimeError("failed"), ValueError("policy failed")])
def test_policy_exception_is_preserved_without_retry(error: Exception) -> None:
    calls = 0

    def failing(jobs: Jobs) -> Order:
        nonlocal calls
        calls += 1
        raise error

    with pytest.raises(type(error)) as caught:
        plan(JOBS, failing)
    assert caught.value is error
    assert calls == 1


@pytest.mark.parametrize(
    "result",
    [(), (7, 2, 9), (7, 2, 9, 9), (7, 2, 9, 99), (7, 2, 9, 5, 5), [7, 2, 9, 5], (7, 2, 9, "5")],
)
def test_invalid_policy_output_is_rejected(result: object) -> None:
    def broken(jobs: Jobs) -> Order:
        # Deliberate runtime contract probe; static violations have independent tests.
        return cast(Order, result)

    with pytest.raises(PolicyContractError):
        plan(JOBS, broken)


def test_bool_does_not_impersonate_job_id() -> None:
    def wrong(jobs: Jobs) -> Order:
        return (True,)

    with pytest.raises(PolicyContractError):
        plan((Job(1, 2),), wrong)


@pytest.mark.parametrize(
    ("job_id", "pages"), [(-1, 1), (1_000_000, 1), (1, 0), (1, 101), (True, 1), (1, True)]
)
def test_invalid_job(job_id: int, pages: int) -> None:
    with pytest.raises(ValueError):
        Job(job_id, pages)


@pytest.mark.parametrize("factory", [small_jobs_first, SmallJobsFirst])
@pytest.mark.parametrize("cutoff", [0, 101, True])
def test_invalid_configuration(factory: Callable[[int], OrderPolicy], cutoff: int) -> None:
    with pytest.raises(ValueError):
        factory(cutoff)


def test_selection_boundary_and_unknown_name() -> None:
    assert select_policy("arrival", cutoff=0) is arrival_order
    assert select_policy("fewest") is fewest_pages
    assert plan(JOBS, select_policy("small", cutoff=1)).job_ids == (5, 7, 2, 9)
    with pytest.raises(ValueError, match="cutoff"):
        select_policy("small", cutoff=0)
    with pytest.raises(ValueError, match="unknown ordering"):
        select_policy("typo")


def test_callable_and_method_objects_use_same_semantics() -> None:
    configured = SmallJobsFirst(5)
    method = SmallFirstOrdering(configured)
    context = ObjectPlanner(method)
    for jobs in ((), JOBS, (Job(3, 99),)):
        assert context.plan(jobs) == plan(jobs, configured) == plan(jobs, method.order)


def test_independent_context_configuration() -> None:
    first = ObjectPlanner(SmallFirstOrdering(SmallJobsFirst(1)))
    second = ObjectPlanner(SmallFirstOrdering(SmallJobsFirst(100)))
    assert first.plan(JOBS).job_ids == (5, 7, 2, 9)
    assert second.plan(JOBS).job_ids == (7, 2, 9, 5)
    assert first.plan(JOBS).job_ids == (5, 7, 2, 9)


def test_normal_frozen_configuration() -> None:
    policy = SmallJobsFirst(5)
    with pytest.raises(FrozenInstanceError):
        policy.cutoff = 10  # type: ignore[misc]


def test_shape_valid_output_does_not_prove_named_policy_semantics() -> None:
    # A bug can preserve every ID while violating the advertised fewest-pages policy.
    def misleading(jobs: Jobs) -> Order:
        return arrival_order(jobs)

    assert plan(JOBS, misleading).total_pages == 15
    assert plan(JOBS, misleading).job_ids != plan(JOBS, fewest_pages).job_ids
