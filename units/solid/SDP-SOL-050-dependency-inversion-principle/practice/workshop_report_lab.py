"""Working baseline. The requested dependency-boundary refactoring is unsolved."""

from workshop_vendor import PlannerOffline, PlanningClient


def publishable_slots(client: PlanningClient, day: str, group_size: int) -> tuple[str, ...]:
    if group_size < 1:
        raise ValueError("group size must be positive")
    try:
        openings = client.list_openings(day)
    except PlannerOffline as error:
        raise RuntimeError("planning unavailable") from error
    return tuple(
        sorted(
            f"{opening.code}: {int(opening.free_seats_text)} seats"
            for opening in openings
            if int(opening.free_seats_text) >= group_size
        )
    )


def main() -> None:
    planner = PlanningClient({"Monday": [("PM", 8), ("AM", 3), ("EVENING", 5)]})
    print(publishable_slots(planner, "Monday", 5))


if __name__ == "__main__":
    main()
