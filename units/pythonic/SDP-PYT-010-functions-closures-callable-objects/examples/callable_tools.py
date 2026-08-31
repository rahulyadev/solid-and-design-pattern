"""Small, synchronous callable collaborations; independent of the practice lab."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Protocol

Encoder = Callable[[str], bytes]
Action = Callable[[], None]


def utf8(text: str) -> bytes:
    return text.encode("utf-8")


def direct_batch(texts: Iterable[str]) -> tuple[bytes, ...]:
    """A sensible starting point when UTF-8 is the only required behaviour."""
    return tuple(text.encode("utf-8") for text in texts)


def encode_batch(texts: Iterable[str], encode: Encoder) -> tuple[bytes, ...]:
    """Call once per item, in order. Stop and propagate the first exception."""
    return tuple(encode(text) for text in texts)


def prefixed_utf8(prefix: str, text: str) -> bytes:
    return utf8(prefix + text)


def make_prefix_encoder(prefix: str) -> Encoder:
    """Each factory call owns a separate binding to its immutable prefix."""

    def encode(text: str) -> bytes:
        return prefixed_utf8(prefix, text)

    return encode


@dataclass
class CountingEncoder:
    """Useful when successful-call state needs a name and direct inspection.

    Sequential use only. Failed encodings do not increase the counter.
    """

    encode: Encoder
    successful_calls: int = field(default=0, init=False)

    def __call__(self, text: str) -> bytes:
        payload = self.encode(text)
        self.successful_calls += 1
        return payload


class ByteSink(Protocol):
    """The keyword-only channel is part of the calling contract."""

    def __call__(self, payload: bytes, /, *, channel: str) -> None: ...


def make_write_action(payload: bytes, sink: ByteSink, *, channel: str) -> Action:
    """Capture a bytes value and a sink reference without performing a write.

    This does not own or extend the validity of an external resource. The caller
    must keep the sink usable until execution. Replaying the action writes again.
    """

    def write() -> None:
        sink(payload, channel=channel)

    return write


def run_actions(actions: Iterable[Action]) -> None:
    """Run sequentially until failure; provide no retry, undo, or transaction."""
    for action in actions:
        action()
