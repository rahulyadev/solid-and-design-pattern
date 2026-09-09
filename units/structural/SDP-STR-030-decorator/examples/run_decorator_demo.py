"""Composition root owns source lifetime; the client knows TextSource only."""

from text_components import Bracket, Label, MemoryText, Observed
from text_contract import Observation, TextSource


def preview(source: TextSource, key: str) -> str:
    return source.render(key)


def main() -> None:
    base = MemoryText({"N-1": "ready"})
    observations: list[Observation] = []
    source: TextSource = Observed(Bracket(Label(base, "note: ")), observations.append)
    try:
        print(preview(source, "N-1"))
        print(observations)
    finally:
        base.close()
    print(f"source_calls={base.calls}, closes={base.close_count}")


if __name__ == "__main__":
    main()
