"""Run the worked Builder comparison without external services."""

from __future__ import annotations

from builder import (
    BuildObservation,
    Compression,
    Destination,
    EncryptionRef,
    ManifestBuilder,
    ReportFormat,
    ReportPlanBuilder,
    construct_daily_activity,
)


def main() -> None:
    observations: list[BuildObservation] = []
    fluent = (
        ReportPlanBuilder(observations.append)
        .named("customer-export")
        .from_source("customers-v2")
        .include("customer_id")
        .include("email", sensitive=True)
        .as_format(ReportFormat.JSONL)
        .deliver_to(
            Destination.EXTERNAL_TRANSFER,
            encryption=EncryptionRef("kms/reporting/customer-export"),
        )
        .compress_with(Compression.GZIP)
        .build()
    )

    directed_plan = construct_daily_activity(ReportPlanBuilder())
    manifest = construct_daily_activity(ManifestBuilder())

    print(
        "fluent:",
        fluent.name,
        f"{len(fluent.columns)} columns",
        fluent.report_format.value,
        fluent.destination.value,
    )
    print(
        "director:",
        directed_plan.name,
        f"{len(directed_plan.columns)} columns",
        directed_plan.compression.value,
    )
    print("manifest:", f"{len(manifest.steps)} entries", manifest.steps[-1])
    print("observations:", observations[-1].step, observations[-1].column_count)


if __name__ == "__main__":
    main()
