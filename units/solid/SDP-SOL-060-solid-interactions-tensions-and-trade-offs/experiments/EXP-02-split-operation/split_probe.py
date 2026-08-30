"""A deterministic schedule exposes a split invariant; this is not a thread test."""

from dataclasses import dataclass


class SplitQuota:
    """Deliberately unsafe collaboration: callers separate checking from consumption."""

    def __init__(self, tokens: int) -> None:
        if tokens < 0:
            raise ValueError("tokens must be nonnegative")
        self.tokens = tokens

    def available(self) -> bool:
        return self.tokens > 0

    def consume(self) -> None:
        self.tokens -= 1


class CohesiveQuota:
    """One state transition for serial callers, with no claim of thread safety."""

    def __init__(self, tokens: int) -> None:
        if tokens < 0:
            raise ValueError("tokens must be nonnegative")
        self.tokens = tokens

    def try_consume(self) -> bool:
        if self.tokens == 0:
            return False
        self.tokens -= 1
        return True


@dataclass(frozen=True)
class QuotaObservation:
    accepted: tuple[bool, bool]
    remaining: int


def split_schedule(tokens: int = 1) -> QuotaObservation:
    quota = SplitQuota(tokens)
    first_allowed = quota.available()
    second_allowed = quota.available()
    if first_allowed:
        quota.consume()
    if second_allowed:
        quota.consume()
    return QuotaObservation((first_allowed, second_allowed), quota.tokens)


def cohesive_schedule(tokens: int = 1) -> QuotaObservation:
    quota = CohesiveQuota(tokens)
    first_allowed = quota.try_consume()
    second_allowed = quota.try_consume()
    return QuotaObservation((first_allowed, second_allowed), quota.tokens)


def main() -> None:
    for name, run in (("split", split_schedule), ("cohesive", cohesive_schedule)):
        result = run()
        print(f"{name}: accepted={result.accepted}; remaining={result.remaining}")
    print("schedule: calls interleave; method bodies do not")


if __name__ == "__main__":
    main()
