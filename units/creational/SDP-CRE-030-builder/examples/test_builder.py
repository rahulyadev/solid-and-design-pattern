"""Behavior, invariant, reuse, and Director tests for the worked Builder."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from builder import (
    BuildManifest,
    BuildObservation,
    Column,
    Compression,
    Destination,
    EncryptionRef,
    InvalidPlanError,
    ManifestBuilder,
    MissingStepError,
    ReportFormat,
    ReportPlan,
    ReportPlanBuilder,
    construct_daily_activity,
    make_internal_report,
)
from hypothesis import given
from hypothesis import strategies as st


def valid_builder() -> ReportPlanBuilder:
    return (
        ReportPlanBuilder()
        .named("weekly-usage")
        .from_source("usage-v1")
        .include("account_id")
        .deliver_to(Destination.INTERNAL_ARCHIVE)
    )


def test_fluent_builder_returns_itself_and_builds_snapshot() -> None:
    builder = ReportPlanBuilder()

    assert builder.named("weekly-usage") is builder
    assert builder.from_source("usage-v1") is builder
    assert builder.include("account_id") is builder
    assert builder.deliver_to(Destination.INTERNAL_ARCHIVE) is builder

    product = builder.build()

    assert product == ReportPlan(
        name="weekly-usage",
        source="usage-v1",
        columns=(Column("account_id"),),
        destination=Destination.INTERNAL_ARCHIVE,
    )


def test_missing_steps_are_reported_in_stable_order() -> None:
    with pytest.raises(MissingStepError) as captured:
        ReportPlanBuilder().build()

    assert captured.value.missing == ("name", "source", "columns", "destination")


@pytest.mark.parametrize(
    ("builder", "expected"),
    [
        (
            ReportPlanBuilder()
            .from_source("source")
            .include("id")
            .deliver_to(Destination.INTERNAL_ARCHIVE),
            ("name",),
        ),
        (
            ReportPlanBuilder()
            .named("name")
            .include("id")
            .deliver_to(Destination.INTERNAL_ARCHIVE),
            ("source",),
        ),
        (
            ReportPlanBuilder()
            .named("name")
            .from_source("source")
            .deliver_to(Destination.INTERNAL_ARCHIVE),
            ("columns",),
        ),
        (ReportPlanBuilder().named("name").from_source("source").include("id"), ("destination",)),
    ],
)
def test_each_required_step_has_a_named_failure(
    builder: ReportPlanBuilder, expected: tuple[str, ...]
) -> None:
    with pytest.raises(MissingStepError) as captured:
        builder.build()

    assert captured.value.missing == expected


def test_external_destination_requires_encryption_reference_at_build() -> None:
    builder = valid_builder().deliver_to(Destination.EXTERNAL_TRANSFER)

    with pytest.raises(InvalidPlanError) as captured:
        builder.build()

    assert captured.value.code == "external_requires_encryption"
    assert captured.value.field_name == "encryption"


def test_external_destination_accepts_reference_without_exposing_it_in_repr() -> None:
    reference = EncryptionRef("kms/reporting/external")
    plan = valid_builder().deliver_to(Destination.EXTERNAL_TRANSFER, encryption=reference).build()

    assert plan.encryption == reference
    assert "kms/reporting/external" not in repr(reference)
    assert "kms/reporting/external" not in repr(plan)


@pytest.mark.parametrize("value", ["", " key", "key ", "  "])
def test_encryption_reference_must_arrive_normalized(value: str) -> None:
    with pytest.raises(InvalidPlanError) as captured:
        EncryptionRef(value)

    assert captured.value.code == "invalid_encryption_reference"
    if value:
        assert value not in str(captured.value)


def test_duplicate_columns_are_rejected_at_final_validation_boundary() -> None:
    builder = valid_builder().include("account_id")

    with pytest.raises(InvalidPlanError) as captured:
        builder.build()

    assert captured.value.code == "duplicate_columns"


def test_csv_rejects_nested_selector_but_jsonl_accepts_it() -> None:
    builder = valid_builder().include("profile.country")

    jsonl = builder.build()
    assert jsonl.report_format is ReportFormat.JSONL

    with pytest.raises(InvalidPlanError) as captured:
        builder.as_format(ReportFormat.CSV).build()
    assert captured.value.code == "nested_csv_column"


@pytest.mark.parametrize("limit", [0, -1, 1_000_001])
def test_invalid_row_limits_are_rejected(limit: int) -> None:
    with pytest.raises(InvalidPlanError) as captured:
        valid_builder().limit_rows(limit).build()

    assert captured.value.code == "invalid_row_limit"


@given(st.integers(min_value=1, max_value=1_000_000))
def test_valid_row_limit_range_round_trips(limit: int) -> None:
    assert valid_builder().limit_rows(limit).build().max_rows == limit


@pytest.mark.parametrize("field_name", ["name", "source"])
@pytest.mark.parametrize("value", ["", " value", "value ", "  "])
def test_required_text_is_validated_by_the_product(field_name: str, value: str) -> None:
    builder = valid_builder()
    if field_name == "name":
        builder.named(value)
    else:
        builder.from_source(value)

    with pytest.raises(InvalidPlanError) as captured:
        builder.build()

    assert captured.value.field_name == field_name


def test_build_is_repeatable_until_explicit_reset() -> None:
    builder = valid_builder()

    first = builder.build()
    second = builder.build()

    assert first == second
    assert first is not second

    builder.reset()
    with pytest.raises(MissingStepError):
        builder.build()


def test_previous_product_does_not_alias_mutable_builder_collections() -> None:
    builder = valid_builder()
    first = builder.build()

    builder.include("region").label("cadence", "weekly")
    second = builder.build()

    assert tuple(column.selector for column in first.columns) == ("account_id",)
    assert first.labels == ()
    assert tuple(column.selector for column in second.columns) == ("account_id", "region")
    assert second.labels == (("cadence", "weekly"),)


def test_product_and_nested_values_reject_field_rebinding() -> None:
    product = valid_builder().build()

    with pytest.raises(FrozenInstanceError):
        product.name = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        product.columns[0].selector = "changed"  # type: ignore[misc]


def test_direct_product_construction_cannot_bypass_invariants() -> None:
    with pytest.raises(InvalidPlanError) as captured:
        ReportPlan(
            name="external",
            source="usage-v1",
            columns=(Column("account_id"),),
            destination=Destination.EXTERNAL_TRANSFER,
        )

    assert captured.value.code == "external_requires_encryption"


def test_focused_factory_is_smaller_than_staged_builder_for_internal_case() -> None:
    product = make_internal_report(
        name="internal",
        source="usage-v1",
        columns=[Column("account_id")],
        labels={"team": "analytics"},
    )

    assert product.destination is Destination.INTERNAL_ARCHIVE
    assert product.labels == (("team", "analytics"),)


def test_director_builds_valid_plan_and_distinct_manifest_representation() -> None:
    plan = construct_daily_activity(ReportPlanBuilder())
    manifest = construct_daily_activity(ManifestBuilder())

    assert isinstance(plan, ReportPlan)
    assert isinstance(manifest, BuildManifest)
    assert plan.name == "daily-activity"
    assert manifest.steps == (
        "reset",
        "name",
        "source",
        "column",
        "column:sensitive",
        "format",
        "destination",
        "compression",
        "limit",
        "label",
        "build",
    )


def test_observations_are_allow_listed_and_report_safe_failure_code() -> None:
    observations: list[BuildObservation] = []
    builder = ReportPlanBuilder(observations.append).named("secret-name").include("email")

    with pytest.raises(MissingStepError):
        builder.build()

    assert observations[-1] == BuildObservation(
        phase="report-plan.build",
        step="build.rejected",
        column_count=1,
        error_code="missing_steps",
    )
    rendered = repr(observations)
    assert "secret-name" not in rendered
    assert "email" not in rendered


def test_observer_failure_does_not_change_pure_build_result() -> None:
    def broken_observer(observation: BuildObservation) -> None:
        raise RuntimeError("synthetic telemetry outage")

    product = (
        ReportPlanBuilder(broken_observer)
        .named("weekly")
        .from_source("usage-v1")
        .include("account_id")
        .deliver_to(Destination.INTERNAL_ARCHIVE)
        .build()
    )

    assert product.name == "weekly"


def test_labels_are_sorted_and_reassignment_has_last_value_semantics() -> None:
    product = (
        valid_builder()
        .label("team", "old")
        .label("cadence", "weekly")
        .label("team", "analytics")
        .build()
    )

    assert product.labels == (("cadence", "weekly"), ("team", "analytics"))


def test_compression_default_and_override_are_explicit() -> None:
    assert valid_builder().build().compression is Compression.NONE
    assert valid_builder().compress_with(Compression.GZIP).build().compression is Compression.GZIP
