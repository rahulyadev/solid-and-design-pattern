"""Working SDP-SOL-010 teaching example; not the separate practice solution."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

HandlingCode = Literal["standard", "manual"]
StoreLabel = Callable[[str, str], None]


@dataclass(frozen=True)
class Parcel:
    parcel_id: str
    weight_grams: int
    fragile: bool = False

    def __post_init__(self) -> None:
        if not self.parcel_id.strip():
            raise ValueError("parcel_id must not be blank")
        if self.weight_grams <= 0:
            raise ValueError("weight_grams must be positive")


@dataclass(frozen=True)
class HandlingDecision:
    parcel_id: str
    code: HandlingCode


def mixed_label(parcel: Parcel, store: StoreLabel) -> HandlingDecision:
    """A correct baseline with handling and label policies in one operation."""
    code: HandlingCode = "manual" if parcel.fragile or parcel.weight_grams > 2000 else "standard"
    text = f"{parcel.parcel_id} | handling={code}"
    store(parcel.parcel_id, text)
    return HandlingDecision(parcel.parcel_id, code)


def decide_handling(parcel: Parcel) -> HandlingDecision:
    """Warehouse policy: fragile parcels or parcels above 2000 g need manual handling."""
    code: HandlingCode = "manual" if parcel.fragile or parcel.weight_grams > 2000 else "standard"
    return HandlingDecision(parcel.parcel_id, code)


def render_label(decision: HandlingDecision) -> str:
    """Label wording; consumes the decision without recalculating warehouse policy."""
    return f"{decision.parcel_id} | handling={decision.code}"


def publish_label(parcel: Parcel, store: StoreLabel) -> HandlingDecision:
    """Coordinate one label publication; storage errors propagate to the caller."""
    decision = decide_handling(parcel)
    store(decision.parcel_id, render_label(decision))
    return decision


def main() -> None:
    parcel = Parcel("P-17", 2400)
    before: dict[str, str] = {}
    after: dict[str, str] = {}
    mixed_label(parcel, before.__setitem__)
    decision = publish_label(parcel, after.__setitem__)
    print(f"mixed: {before[parcel.parcel_id]}")
    print(f"separated: {after[parcel.parcel_id]}")
    print(f"decision: {decision.code}")
    print(f"stored: {after}")


if __name__ == "__main__":
    main()
