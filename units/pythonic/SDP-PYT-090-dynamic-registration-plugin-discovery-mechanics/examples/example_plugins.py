"""Synthetic providers used by the SDP-PYT-090 worked example."""

from __future__ import annotations

import json

from plugin_runtime import PluginManifest, PluginOffer, RenderedReport, ReportRequest


def _require_kind(request: ReportRequest, expected: str) -> None:
    if request.report_kind != expected:
        raise ValueError(f"expected report kind {expected!r}")


def invoice_provider() -> PluginOffer:
    """A configured-import provider; construction is intentionally cheap."""

    def render(request: ReportRequest) -> RenderedReport:
        _require_kind(request, "invoice")
        body = json.dumps(
            {"record_id": request.record_id, "report_kind": request.report_kind},
            sort_keys=True,
            separators=(",", ":"),
        )
        return RenderedReport("application/json", body)

    return PluginOffer(
        manifest=PluginManifest(
            name="invoice-json",
            api_major=1,
            capabilities=frozenset({"format.json"}),
            claims=frozenset({"report.invoice"}),
        ),
        render=render,
    )


def status_provider() -> PluginOffer:
    """An already imported provider suitable for static registration."""

    def render(request: ReportRequest) -> RenderedReport:
        _require_kind(request, "status")
        return RenderedReport("text/plain", f"status:{request.record_id}")

    return PluginOffer(
        manifest=PluginManifest(
            name="status-text",
            api_major=1,
            capabilities=frozenset({"format.text"}),
            claims=frozenset({"report.status"}),
        ),
        render=render,
    )
