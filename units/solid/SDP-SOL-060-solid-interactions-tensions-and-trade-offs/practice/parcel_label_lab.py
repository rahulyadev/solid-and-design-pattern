"""Working synchronous baseline. The queued-partner requirement remains unsolved."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Parcel:
    reference: str
    destination: str
    grams: int


@dataclass(frozen=True)
class DispatchNote:
    reference: str
    label: str


class LocalLabelDesk:
    """Synthetic local provider with more capabilities than dispatch currently needs."""

    def __init__(self, *, offline: bool = False) -> None:
        self.offline = offline
        self.issued: list[str] = []

    def make_label(self, parcel: Parcel) -> str:
        if self.offline:
            raise ConnectionError("local label desk offline")
        label = f"LABEL {parcel.reference} / {parcel.destination} / {parcel.grams}g"
        self.issued.append(label)
        return label

    def void_label(self, label: str) -> None:
        self.issued.remove(label)

    def daily_total(self) -> int:
        return len(self.issued)


def prepare_dispatch(parcel: Parcel, desk: LocalLabelDesk) -> DispatchNote:
    """Return a ready label, or fail visibly. Never return an acknowledgement as a label."""
    if not parcel.reference.strip() or not parcel.destination.strip():
        raise ValueError("reference and destination must not be blank")
    if parcel.grams <= 0:
        raise ValueError("grams must be positive")
    try:
        label = desk.make_label(parcel)
    except ConnectionError as error:
        raise RuntimeError("label unavailable") from error
    return DispatchNote(parcel.reference, label)


def main() -> None:
    desk = LocalLabelDesk()
    note = prepare_dispatch(Parcel("PK-7", "North", 250), desk)
    print(note.label)
    print(f"issued: {desk.daily_total()}")


if __name__ == "__main__":
    main()
