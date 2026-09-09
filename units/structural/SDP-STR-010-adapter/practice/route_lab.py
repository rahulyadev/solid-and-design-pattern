"""Working old route consumer. New requirements in README remain unsolved."""


class RouteFeed:
    def __init__(self, durations: dict[str, int]) -> None:
        self.durations = dict(durations)
        self.calls: list[str] = []

    def route_minutes(self, name: str) -> int:
        self.calls.append(name)
        return self.durations[name]


def trip_label(feed: RouteFeed, route: str) -> str:
    return f"{route}: {feed.route_minutes(route)} min"


if __name__ == "__main__":
    print(trip_label(RouteFeed({"NORTH": 7}), "NORTH"))
    print("target_complete=False")
