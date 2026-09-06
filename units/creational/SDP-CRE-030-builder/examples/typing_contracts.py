"""Positive static-typing witnesses for the Builder and Director contracts."""

from __future__ import annotations

from builder import (
    BuildManifest,
    ManifestBuilder,
    ReportPlan,
    ReportPlanBuilder,
    StandardReportBuilder,
    construct_daily_activity,
)


def make_plan(builder: StandardReportBuilder[ReportPlan]) -> ReportPlan:
    return construct_daily_activity(builder)


def make_manifest(builder: StandardReportBuilder[BuildManifest]) -> BuildManifest:
    return construct_daily_activity(builder)


PLAN = make_plan(ReportPlanBuilder())
MANIFEST = make_manifest(ManifestBuilder())
