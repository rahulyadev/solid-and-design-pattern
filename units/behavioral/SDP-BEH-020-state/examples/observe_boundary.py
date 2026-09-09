"""Controlled observation of callback failure and same-context reentrancy."""

from state import Event, Packet, Snapshot


class GateFailure(RuntimeError):
    pass


def observe(mode: str) -> str:
    effects: list[int] = []
    seen: list[str] = []

    def gate(proposal: Snapshot) -> None:
        seen.append(f"{packet.snapshot.phase.value}->{proposal.phase.value}")
        if mode == "fail_before":
            raise GateFailure("before effect")
        if mode == "reenter":
            packet.handle(Event.CANCEL)
        effects.append(proposal.revision)
        if mode == "fail_after":
            raise GateFailure("after effect")

    packet = Packet(gate)
    packet.handle(Event.ADD, 2)
    packet.handle(Event.SEAL)
    before = packet.snapshot
    error_name = "none"
    try:
        packet.handle(Event.RELEASE)
    except RuntimeError as error:
        error_name = type(error).__name__
    after = packet.snapshot
    return (
        f"{mode}: seen={seen}, effects={effects}, error={error_name}, "
        f"state={after.phase.value}, rev={after.revision}, same_snapshot={after is before}"
    )


def main() -> None:
    for mode in ("success", "fail_before", "fail_after", "reenter"):
        print(observe(mode))


if __name__ == "__main__":
    main()
