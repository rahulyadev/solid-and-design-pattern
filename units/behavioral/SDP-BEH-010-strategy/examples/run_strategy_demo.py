"""Deterministic policy observations, not a scheduling benchmark."""

from object_strategy import ObjectPlanner, SmallFirstOrdering
from strategy import Job, SmallJobsFirst, plan, select_policy


def main() -> None:
    jobs = (Job(7, 8), Job(2, 3), Job(9, 3), Job(5, 1))
    for name in ("arrival", "fewest", "small"):
        result = plan(jobs, select_policy(name))
        print(f"{name}: ids={result.job_ids}; pages={result.total_pages}")
    configured = SmallJobsFirst(5)
    object_result = ObjectPlanner(SmallFirstOrdering(configured)).plan(jobs)
    print(f"callable object == method object: {plan(jobs, configured) == object_result}")


if __name__ == "__main__":
    main()
