"""Second deliberately competing registration used only by the experiment."""

from registration_target import ExternalPayload, summarize_external


@summarize_external.register
def summarize_external_beta(value: ExternalPayload) -> str:
    return f"beta:{value.payload_id}"
