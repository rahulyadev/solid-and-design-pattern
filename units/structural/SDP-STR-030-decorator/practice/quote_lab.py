"""Unsolved quote-combination lab. No charges or external effects occur."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Parcel:
    mass_grams: int

    def __post_init__(self) -> None:
        if self.mass_grams <= 0:
            raise ValueError("mass must be positive")


def basic_quote(parcel: Parcel) -> int:
    """Synthetic integer cents, for prediction and characterization only."""
    return 100 + 2 * parcel.mass_grams


def client_quote(parcel: Parcel, *, discount: bool, minimum: bool) -> int:
    cents = basic_quote(parcel)
    if discount:
        cents = cents * 9 // 10
    if minimum:
        cents = max(500, cents)
    return cents


def build_quote() -> object:
    """Replace this temporary boundary after specifying your contract."""
    raise NotImplementedError("exercise starts unsolved")


def main() -> None:
    parcel = Parcel(150)
    print(f"plain={client_quote(parcel, discount=False, minimum=False)}")
    print(f"combined={client_quote(parcel, discount=True, minimum=True)}")
    try:
        build_quote()
    except NotImplementedError:
        print("target_complete=False")


if __name__ == "__main__":
    main()
