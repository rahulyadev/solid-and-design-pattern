"""Positive static conformance witnesses for the worked boundary."""

from interface_design import (
    ArchiveChannelAdapter,
    EventChannel,
    InMemoryChannel,
    VendorArchive,
)

memory_channel: EventChannel = InMemoryChannel()
archive_channel: EventChannel = ArchiveChannelAdapter(VendorArchive())


class IncompatibleChannel:
    def deliver(self, payload: bytes) -> str:
        return payload.decode()


# Uncommenting this line is expected to produce a static-checker error:
# incompatible_channel: EventChannel = IncompatibleChannel()
