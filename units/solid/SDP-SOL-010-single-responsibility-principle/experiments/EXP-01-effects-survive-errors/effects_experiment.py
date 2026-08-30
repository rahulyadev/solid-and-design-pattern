"""Controlled Python exception observation, not a database or network simulation."""

from dataclasses import dataclass, field
from typing import Literal

Failure = Literal["none", "save", "before_notify", "after_notify"]
Style = Literal["mixed", "split"]


@dataclass
class Effects:
    saved: list[str] = field(default_factory=list)
    delivered: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Observation:
    saved: tuple[str, ...]
    delivered: tuple[str, ...]
    error: bool


def mixed_publication(pickup_id: str, effects: Effects, failure: Failure) -> None:
    if failure == "save":
        raise RuntimeError("save failed before changing state")
    effects.saved.append(pickup_id)
    if failure == "before_notify":
        raise RuntimeError("notify failed before delivery")
    effects.delivered.append(pickup_id)
    if failure == "after_notify":
        raise RuntimeError("notify failed after delivery")


def save_pickup(pickup_id: str, effects: Effects, failure: Failure) -> None:
    if failure == "save":
        raise RuntimeError("save failed before changing state")
    effects.saved.append(pickup_id)


def notify_pickup(pickup_id: str, effects: Effects, failure: Failure) -> None:
    if failure == "before_notify":
        raise RuntimeError("notify failed before delivery")
    effects.delivered.append(pickup_id)
    if failure == "after_notify":
        raise RuntimeError("notify failed after delivery")


def split_publication(pickup_id: str, effects: Effects, failure: Failure) -> None:
    save_pickup(pickup_id, effects, failure)
    notify_pickup(pickup_id, effects, failure)


def observe(style: Style, failure: Failure, effects: Effects | None = None) -> Observation:
    state = effects if effects is not None else Effects()
    publish = mixed_publication if style == "mixed" else split_publication
    error = False
    try:
        publish("PICKUP-17", state, failure)
    except RuntimeError:
        error = True
    return Observation(tuple(state.saved), tuple(state.delivered), error)


def retry_after_error(style: Style) -> Observation:
    state = Effects()
    observe(style, "after_notify", state)
    return observe(style, "none", state)


def main() -> None:
    styles: tuple[Style, ...] = ("mixed", "split")
    failures: tuple[Failure, ...] = ("none", "save", "before_notify", "after_notify")
    for style in styles:
        for failure in failures:
            result = observe(style, failure)
            print(
                f"{style} fault={failure} saved={len(result.saved)} "
                f"delivered={len(result.delivered)} error={result.error}"
            )
        retried = retry_after_error(style)
        print(
            f"{style} retry-after-delivery saved={len(retried.saved)} "
            f"delivered={len(retried.delivered)} error={retried.error}"
        )


if __name__ == "__main__":
    main()
