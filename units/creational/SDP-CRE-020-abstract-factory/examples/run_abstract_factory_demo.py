"""Deterministic command-line demonstration for SDP-CRE-020."""

from __future__ import annotations

from abstract_factory import (
    Event,
    JsonDeliveryFactory,
    Observation,
    PipeDeliveryFactory,
    deliver,
)


def main() -> None:
    observations: list[Observation] = []
    for factory in (JsonDeliveryFactory([]), PipeDeliveryFactory([])):
        receipt = deliver(Event("EVT-7", "inventory reserved"), factory, observations.append)
        print(
            f"family={receipt.family.value}; delivery_id={receipt.delivery_id}; "
            f"accepted={receipt.accepted}"
        )
    print("phases=" + ",".join(item.phase for item in observations))


if __name__ == "__main__":
    main()
