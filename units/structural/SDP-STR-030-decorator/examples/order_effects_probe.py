"""Deterministic observations, not a benchmark or distributed-system simulation."""

from text_components import Bracket, Label, MemoryText, Observed
from text_contract import Observation


def probe() -> tuple[str, ...]:
    base = MemoryText({"N-1": "ready"})
    events: list[Observation] = []
    rows: list[str] = []
    try:
        rows.append(f"label_outside | {Label(Bracket(base), 'note: ').render('N-1')}")
        rows.append(f"bracket_outside | {Bracket(Label(base, 'note: ')).render('N-1')}")
        inside = Bracket(Label(Observed(base, events.append), "note: "))
        outside = Observed(Bracket(Label(base, "note: ")), events.append)
        rows.append(f"observe_inside | {inside.render('N-1')} | {events[-1].characters}")
        rows.append(f"observe_outside | {outside.render('N-1')} | {events[-1].characters}")

        def broken_observer(observation: Observation) -> None:
            raise OSError("synthetic observer outage")

        degraded = Observed(base, broken_observer)
        rows.append(f"observer_failure | {degraded.render('N-1')} | dropped={degraded.dropped}")
        try:
            outside.render("missing")
        except KeyError:
            rows.append(f"source_failure | KeyError | {events[-1].outcome}")
    finally:
        base.close()
    rows.append(f"lifetime | calls={base.calls} | closes={base.close_count}")
    return tuple(rows)


if __name__ == "__main__":
    print("\n".join(probe()))
