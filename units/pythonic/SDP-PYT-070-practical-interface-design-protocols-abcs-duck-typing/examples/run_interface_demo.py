"""Run the two structural implementations through the same client."""

from interface_design import (
    ArchiveChannelAdapter,
    AuditEvent,
    InMemoryChannel,
    VendorArchive,
    deliver_audit_event,
)


def main() -> None:
    event = AuditEvent("evt-42", "invoice.created", "amount=2500|currency=INR")
    channels = (InMemoryChannel(), ArchiveChannelAdapter(VendorArchive()))

    for channel in channels:
        receipt = deliver_audit_event(channel, event, idempotency_key="request-42")
        print(f"{receipt.channel}: event={receipt.event_id} key={receipt.idempotency_key}")


if __name__ == "__main__":
    main()
