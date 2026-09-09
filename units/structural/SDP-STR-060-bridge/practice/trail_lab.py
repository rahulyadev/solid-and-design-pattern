"""Unsolved trail-guide refactoring starter. All places are synthetic."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Stop:
    name: str
    stairs: bool


class WalkingTextGuide:
    def render(self, stops: tuple[Stop, ...]) -> str:
        return " -> ".join(stop.name for stop in stops)


def target_complete() -> bool:
    # Change this only after the new behavioral requirements and explanation exist.
    return False


if __name__ == "__main__":
    route = (Stop("Pond", False), Stop("Tower", True), Stop("Grove", False))
    print(WalkingTextGuide().render(route))
    print(f"target_complete={target_complete()}")
