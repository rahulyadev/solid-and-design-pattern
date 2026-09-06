"""Run the class-based and injected Factory Method examples."""

from __future__ import annotations

from functools import partial

from factory_method import (
    Alert,
    BufferedPublisher,
    BufferedTransport,
    Observation,
    publish_alert,
)
from selection import TransportConfig, application_factories, build_transport


def main() -> None:
    class_output: list[str] = []
    class_events: list[Observation] = []
    creator = BufferedPublisher(class_output, class_events.append)
    class_receipt = creator.publish(Alert("A-100", "queue depth high"))

    function_output: list[str] = []
    function_events: list[Observation] = []
    function_receipt = publish_alert(
        Alert("A-101", "worker recovered"),
        partial(BufferedTransport, function_output),
        function_events.append,
    )

    framed_output: list[str] = []
    registry = application_factories([], framed_output.append)
    configured = build_transport(
        TransportConfig.from_mapping({"name": "framed", "prefix": "OPS"}),
        registry,
        allowed={"framed"},
    )
    try:
        configured_receipt = configured.send(Alert("A-102", "probe stable"))
    finally:
        configured.close()

    print(f"class={class_receipt.transport}:{class_output[0]}")
    print(f"function={function_receipt.transport}:{function_output[0]}")
    print(f"configured={configured_receipt.transport}:{framed_output[0]}")
    print("events=" + ",".join(event.event for event in class_events))


if __name__ == "__main__":
    main()
