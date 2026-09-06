"""Static boundaries for the SDP-PYT-090 plugin example."""

from __future__ import annotations

from plugin_runtime import PluginOffer, PluginProvider, RenderedReport, ReportRequest


def build_offer(provider: PluginProvider) -> PluginOffer:
    """Narrow an application-owned provider after its runtime boundary is checked."""

    value = provider()
    if not isinstance(value, PluginOffer):
        raise TypeError("provider did not return PluginOffer")
    return value


def render_with(offer: PluginOffer, request: ReportRequest) -> RenderedReport:
    return offer.render(request)
