"""Factory Method and an injected-factory alternative for a synthetic alert backend.

The class hierarchy demonstrates the GoF collaboration.  The function form shows
the smaller Python design when subclassing provides no additional value.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol


class AlertValidationError(ValueError):
    """An alert violates the public domain contract."""


class ClosedTransportError(RuntimeError):
    """A transport was used after its owned lifetime ended."""


@dataclass(frozen=True, slots=True)
class Alert:
    """Validated input whose message must never be included in observations."""

    alert_id: str
    message: str

    def __post_init__(self) -> None:
        if not self.alert_id or not self.alert_id.isascii() or len(self.alert_id) > 40:
            raise AlertValidationError("alert_id must be 1..40 ASCII characters")
        if not self.message.strip():
            raise AlertValidationError("message must not be blank")


@dataclass(frozen=True, slots=True)
class Receipt:
    alert_id: str
    transport: str


@dataclass(frozen=True, slots=True)
class Observation:
    """A deliberately safe event: it contains no alert message or credentials."""

    event: str
    alert_id: str
    transport: str
    error_type: str | None = None


Observer = Callable[[Observation], None]


class Transport(Protocol):
    """Product contract used by the stable publication workflow."""

    @property
    def name(self) -> str: ...

    def send(self, alert: Alert) -> Receipt: ...

    def close(self) -> None: ...


class BufferedTransport:
    """Concrete Product that appends a normalized record to an owned buffer."""

    def __init__(self, output: list[str]) -> None:
        self._output = output
        self._closed = False

    @property
    def name(self) -> str:
        return "buffer"

    def send(self, alert: Alert) -> Receipt:
        self._require_open()
        self._output.append(f"{alert.alert_id}:{alert.message.strip()}")
        return Receipt(alert.alert_id, self.name)

    def close(self) -> None:
        self._closed = True

    def _require_open(self) -> None:
        if self._closed:
            raise ClosedTransportError("buffer transport is closed")


class FramedTransport:
    """Concrete Product that emits one framed record through a supplied callable."""

    def __init__(self, emit: Callable[[str], None], *, prefix: str = "ALERT") -> None:
        if not prefix or not prefix.isascii() or not prefix.isupper():
            raise ValueError("prefix must be nonblank uppercase ASCII")
        self._emit = emit
        self._prefix = prefix
        self._closed = False

    @property
    def name(self) -> str:
        return "framed"

    def send(self, alert: Alert) -> Receipt:
        self._require_open()
        self._emit(f"{self._prefix}|{alert.alert_id}|{alert.message.strip()}")
        return Receipt(alert.alert_id, self.name)

    def close(self) -> None:
        self._closed = True

    def _require_open(self) -> None:
        if self._closed:
            raise ClosedTransportError("framed transport is closed")


TransportFactory = Callable[[], Transport]


def _publish_once(
    alert: Alert,
    make_transport: TransportFactory,
    observe: Observer,
) -> Receipt:
    """Run business workflow around one newly owned Product lifetime."""

    transport = make_transport()
    try:
        observe(Observation("transport.created", alert.alert_id, transport.name))
        try:
            receipt = transport.send(alert)
        except Exception as error:
            observe(
                Observation(
                    "transport.failed",
                    alert.alert_id,
                    transport.name,
                    type(error).__name__,
                )
            )
            raise
        else:
            observe(Observation("transport.sent", alert.alert_id, transport.name))
            return receipt
    finally:
        transport.close()
        observe(Observation("transport.closed", alert.alert_id, transport.name))


class Publisher(ABC):
    """Creator: stable workflow plus an overridable creation decision."""

    def __init__(self, observe: Observer) -> None:
        self._observe = observe

    def publish(self, alert: Alert) -> Receipt:
        return _publish_once(alert, self.create_transport, self._observe)

    @abstractmethod
    def create_transport(self) -> Transport:
        """Factory Method: subclasses decide which Product to instantiate."""


class BufferedPublisher(Publisher):
    """Concrete Creator for BufferedTransport."""

    def __init__(self, output: list[str], observe: Observer) -> None:
        super().__init__(observe)
        self._output = output

    def create_transport(self) -> Transport:
        return BufferedTransport(self._output)


class FramedPublisher(Publisher):
    """Concrete Creator for FramedTransport."""

    def __init__(
        self,
        emit: Callable[[str], None],
        observe: Observer,
        *,
        prefix: str = "ALERT",
    ) -> None:
        super().__init__(observe)
        self._emit = emit
        self._prefix = prefix

    def create_transport(self) -> Transport:
        return FramedTransport(self._emit, prefix=self._prefix)


def publish_alert(
    alert: Alert,
    make_transport: TransportFactory,
    observe: Observer,
) -> Receipt:
    """Pythonic alternative: inject a zero-argument factory callable."""

    return _publish_once(alert, make_transport, observe)
