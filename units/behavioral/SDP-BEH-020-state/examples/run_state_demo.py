"""Print the same events changing meaning as one packet moves through states."""

from state import Event, InvalidTransition, Packet


def main() -> None:
    packet = Packet()
    for event, pages in (
        (Event.ADD, 2),
        (Event.SEAL, 0),
        (Event.ADD, 1),
        (Event.REOPEN, 0),
        (Event.ADD, 1),
        (Event.SEAL, 0),
        (Event.RELEASE, 0),
        (Event.CANCEL, 0),
    ):
        try:
            result = packet.handle(event, pages)
        except InvalidTransition as error:
            print(str(error))
        else:
            print(
                f"{event.value}: {result.phase.value}, pages={result.pages}, rev={result.revision}"
            )


if __name__ == "__main__":
    main()
