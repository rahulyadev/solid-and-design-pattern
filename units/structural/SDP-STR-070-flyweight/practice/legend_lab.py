"""Working per-row legend starter. The requested batch redesign remains unsolved."""

from dataclasses import dataclass


@dataclass
class LegendRow:
    row_id: int
    text: str
    legend: dict[str, str]

    def describe(self) -> str:
        return f"{self.row_id}: {self.text} [{self.legend['label']}]"


def build_rows(texts: tuple[str, ...], label: str) -> list[LegendRow]:
    return [LegendRow(i, text, {"label": label}) for i, text in enumerate(texts)]


def target_complete() -> bool:
    return False


if __name__ == "__main__":
    for row in build_rows(("Check hinge", "Check seal"), "Inspection"):
        print(row.describe())
    print(f"target_complete={target_complete()}")
