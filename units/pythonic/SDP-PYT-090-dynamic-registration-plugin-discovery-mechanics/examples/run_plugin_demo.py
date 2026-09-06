"""Run the explicit, governed plugin startup path."""

from example_plugins import status_provider
from plugin_runtime import (
    HostPolicy,
    LifecycleEvent,
    ReportRequest,
    configured_import_candidate,
    invoke_plugin,
    start_plugins,
    static_candidate,
)


def main() -> None:
    observations: list[LifecycleEvent] = []
    configured = (
        configured_import_candidate(
            name="invoice-json",
            module="example_plugins",
            attribute="invoice_provider",
        ),
        static_candidate(name="status-text", provider=status_provider),
    )
    result = start_plugins(configured, policy=HostPolicy(), observe=observations.append)
    rendered = invoke_plugin(
        result.snapshot,
        "invoice-json",
        ReportRequest("invoice", "inv-example-7"),
        observe=observations.append,
    )

    print(f"active={','.join(result.snapshot.names)}")
    print(f"claims={dict(result.snapshot.claim_owners)}")
    print(f"rendered={rendered.media_type}:{rendered.body}")
    for event in observations:
        print(
            "event="
            f"{event.provider}|{event.distribution}|{event.version}|"
            f"{event.stage.value}|{event.outcome}"
        )


if __name__ == "__main__":
    main()
