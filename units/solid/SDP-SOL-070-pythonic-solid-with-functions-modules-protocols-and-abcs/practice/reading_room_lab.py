"""Runnable concrete baseline. The new catalogue integration is unsolved."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class ReadingCard:
    code: str
    title: str
    available: bool


class ShelfCatalog:
    def __init__(self, titles: Mapping[str, str]) -> None:
        self._titles = dict(titles)

    def lookup(self, code: str) -> str:
        """Return a title or raise KeyError for an unknown code."""
        return self._titles[code]

    def replace(self, code: str, title: str) -> None:
        self._titles[code] = title

    def remove(self, code: str) -> None:
        del self._titles[code]


def build_reading_cards(codes: Sequence[str], catalog: ShelfCatalog) -> tuple[ReadingCard, ...]:
    """Preserve order/duplicates. Missing is data; other lookup errors propagate."""
    if any(not code.strip() for code in codes):
        raise ValueError("reading codes must be nonblank")
    cards: list[ReadingCard] = []
    for code in codes:
        try:
            title = catalog.lookup(code)
        except KeyError:
            cards.append(ReadingCard(code, "Not on this shelf", False))
        else:
            cards.append(ReadingCard(code, title, True))
    return tuple(cards)


def main() -> None:
    catalog = ShelfCatalog({"garden": "Small Gardens", "night": "Night Skies"})
    for card in build_reading_cards(("night", "absent", "night"), catalog):
        print(f"{card.code}: {card.title}; available={card.available}")


if __name__ == "__main__":
    main()
