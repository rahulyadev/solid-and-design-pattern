"""Run the solved synthetic dispatch example."""

from dispatch_tools import Event, dispatch, dispatch_all, example_registry, quarantine_unknown


def main() -> None:
    handlers = example_registry()
    events = (
        Event("record.created", "A-17"),
        Event("record.deleted", "B-04"),
        Event("record.created", "A-17"),
    )

    for result in dispatch_all(events, handlers, trace_id="trace-demo"):
        print(result)

    fallback_result = dispatch(
        Event("record.restored", "C-09"),
        handlers,
        trace_id="trace-demo",
        fallback=quarantine_unknown,
    )
    print(fallback_result)


if __name__ == "__main__":
    main()
