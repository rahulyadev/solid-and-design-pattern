"""Working baseline only. Add the requirements in the brief after predicting."""

from enum import Enum


class Status(Enum):
    FREE = "free"
    HELD = "held"
    OCCUPIED = "occupied"


class Station:
    def __init__(self) -> None:
        self.status = Status.FREE
        self.owner: str | None = None

    def reserve(self, owner: str) -> None:
        if not owner.strip() or self.status is not Status.FREE:
            raise ValueError("reservation rejected")
        self.owner = owner
        self.status = Status.HELD

    def enter(self, owner: str) -> None:
        if self.status is not Status.HELD or owner != self.owner:
            raise ValueError("entry rejected")
        self.status = Status.OCCUPIED

    def leave(self, owner: str) -> None:
        if self.status is not Status.OCCUPIED or owner != self.owner:
            raise ValueError("departure rejected")
        self.owner = None
        self.status = Status.FREE


def main() -> None:
    station = Station()
    station.reserve("reader-a")
    station.enter("reader-a")
    station.leave("reader-a")
    print(f"{station.status.value}, owner={station.owner}")
    print("target_complete=False")


if __name__ == "__main__":
    main()
