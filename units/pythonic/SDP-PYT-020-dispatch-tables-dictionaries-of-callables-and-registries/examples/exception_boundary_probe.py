"""Compare a broad KeyError catch with a lookup-only exception boundary."""

from collections.abc import Mapping

from dispatch_tools import Event, Handler, UnknownEventType, build_registry, dispatch


def broad_dispatch(
    event: Event,
    handlers: Mapping[str, Handler],
    *,
    trace_id: str,
) -> str:
    """Intentionally flawed: it catches failures from lookup and execution."""

    try:
        return handlers[event.kind](event, trace_id=trace_id)
    except KeyError:
        raise UnknownEventType(f"unsupported event type: {event.kind}") from None


def observations() -> dict[str, str]:
    failure = KeyError("payload.customer_id")

    def broken(event: Event, /, *, trace_id: str) -> str:
        del event, trace_id
        raise failure

    handlers = build_registry([("record.broken", broken)])
    event = Event("record.broken", "E-1")

    try:
        broad_dispatch(event, handlers, trace_id="probe")
    except Exception as error:
        broad = f"{type(error).__name__}: {error}"
    else:  # pragma: no cover - fixed input always raises
        broad = "no error"

    try:
        dispatch(event, handlers, trace_id="probe")
    except Exception as error:
        controlled = f"{type(error).__name__}: {error}; same={error is failure}"
    else:  # pragma: no cover - fixed input always raises
        controlled = "no error"

    return {"broad": broad, "controlled": controlled}


def main() -> None:
    result = observations()
    print(f"broad catch: {result['broad']}")
    print(f"lookup-only catch: {result['controlled']}")


if __name__ == "__main__":
    main()
