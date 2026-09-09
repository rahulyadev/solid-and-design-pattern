"""Unsolved dispatch-profile refactor. Baseline does ordinary reconstruction."""

from dataclasses import dataclass, field

TARGET_REFACTOR_COMPLETE = False


@dataclass(kw_only=True)
class DispatchProfile:
    channel: str
    destinations: list[str]
    attempts: list[str] = field(default_factory=list)


def prepare_dispatch(*, channel: str, destinations: list[str]) -> DispatchProfile:
    if channel not in {"internal", "partner"}:
        raise ValueError("unsupported_channel")
    if not destinations:
        raise ValueError("destinations_required")
    return DispatchProfile(channel=channel, destinations=list(destinations))


if __name__ == "__main__":
    result = prepare_dispatch(channel="internal", destinations=["synthetic-queue"])
    print(f"channel={result.channel} destinations={len(result.destinations)}")
    print(f"target_complete={TARGET_REFACTOR_COMPLETE}")
