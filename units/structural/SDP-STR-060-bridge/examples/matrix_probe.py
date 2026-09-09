"""Count real delegation calls for four combinations; not a timing benchmark."""

from dataclasses import dataclass, field

from bridge import (
    Artifact,
    CsvEncoder,
    Encoder,
    InventoryReport,
    JsonEncoder,
    ShortageReport,
    StockItem,
    Table,
)


@dataclass
class RecordingEncoder:
    delegate: Encoder
    seen: list[Table] = field(default_factory=list)

    def encode(self, table: Table, /) -> Artifact:
        self.seen.append(table)
        return self.delegate.encode(table)


@dataclass(frozen=True)
class Observation:
    policy: str
    output: str
    rows: int
    calls: int


def observe() -> tuple[Observation, ...]:
    items = (StockItem("clip", 3, 5), StockItem("tray", 8, 8))
    observations: list[Observation] = []
    for report_type in (InventoryReport, ShortageReport):
        for encoder_type in (CsvEncoder, JsonEncoder):
            encoder = RecordingEncoder(encoder_type())
            report_type(encoder).render(items)
            observations.append(
                Observation(
                    report_type.__name__,
                    encoder_type.__name__,
                    len(encoder.seen[0].rows),
                    len(encoder.seen),
                )
            )
    return tuple(observations)


if __name__ == "__main__":
    for observation in observe():
        print(
            f"{observation.policy}/{observation.output}: "
            f"rows={observation.rows}, calls={observation.calls}"
        )
