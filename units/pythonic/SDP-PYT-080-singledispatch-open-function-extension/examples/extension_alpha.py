"""First deliberately competing registration used only by the experiment."""

from registration_target import ExternalPayload, summarize_external


@summarize_external.register
def summarize_external_alpha(value: ExternalPayload) -> str:
    return f"alpha:{value.payload_id}"
