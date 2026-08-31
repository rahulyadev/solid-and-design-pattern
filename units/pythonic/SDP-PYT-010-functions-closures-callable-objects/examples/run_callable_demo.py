"""Run the worked examples, not the separate learner exercise."""

from dataclasses import dataclass, field
from functools import partial

from callable_tools import (
    CountingEncoder,
    direct_batch,
    encode_batch,
    make_prefix_encoder,
    make_write_action,
    prefixed_utf8,
    run_actions,
    utf8,
)


@dataclass
class MemoryWriter:
    records: list[tuple[str, bytes]] = field(default_factory=list)

    def write(self, payload: bytes, /, *, channel: str) -> None:
        self.records.append((channel, payload))


def main() -> None:
    texts = ("alpha", "beta")
    print("direct:", direct_batch(texts))
    print("function:", encode_batch(texts, utf8))
    print("closure:", encode_batch(texts, make_prefix_encoder("api/")))
    print("partial:", encode_batch(texts, partial(prefixed_utf8, "ops/")))
    counted = CountingEncoder(make_prefix_encoder("audit/"))
    print("callable object:", encode_batch(texts, counted))
    print("successful calls:", counted.successful_calls)

    writer = MemoryWriter()
    action = make_write_action(b"ready", writer.write, channel="status")
    print("before action:", writer.records)
    run_actions((action, action))
    print("after replay:", writer.records)


if __name__ == "__main__":
    main()
