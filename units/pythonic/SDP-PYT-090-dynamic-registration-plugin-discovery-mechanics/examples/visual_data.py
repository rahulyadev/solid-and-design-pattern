"""Runtime-backed scenario data embedded in the lifecycle explorer."""

from __future__ import annotations

from collections.abc import Callable

from plugin_runtime import (
    CandidateSource,
    FailurePolicy,
    HostPolicy,
    LifecycleEvent,
    PluginCandidate,
    PluginManifest,
    PluginOffer,
    PluginStartupError,
    RenderedReport,
    ReportRequest,
    invoke_plugin,
    start_plugins,
)

Scenario = dict[str, object]


def _offer(
    name: str,
    *,
    api_major: int = 1,
    claim: str | None = None,
    renderer: Callable[[ReportRequest], RenderedReport] | None = None,
) -> PluginOffer:
    def default_renderer(request: ReportRequest) -> RenderedReport:
        return RenderedReport("text/plain", f"rendered:{request.record_id}")

    return PluginOffer(
        PluginManifest(
            name=name,
            api_major=api_major,
            capabilities=frozenset({"format.text"}),
            claims=frozenset({claim or f"report.{name}"}),
        ),
        renderer or default_renderer,
    )


def _candidate(
    name: str,
    provider: Callable[[], object],
    *,
    distribution: str | None = None,
    loader: Callable[[], object] | None = None,
) -> PluginCandidate:
    return PluginCandidate(
        entry_name=name,
        object_ref=f"visual_{name}:provide",
        distribution=distribution or f"Visual-{name.title()}",
        version="1.0",
        source=CandidateSource.ENTRY_POINT,
        loader=loader or (lambda: provider),
    )


def _paths(events: list[LifecycleEvent]) -> list[str]:
    return [f"{event.provider}:{event.stage.value}:{event.outcome}" for event in events]


def _success() -> Scenario:
    events: list[LifecycleEvent] = []
    entry = _candidate("invoice", lambda: _offer("invoice"))
    result = start_plugins((entry,), observe=events.append)
    rendered = invoke_plugin(
        result.snapshot,
        "invoice",
        ReportRequest("invoice", "record-7"),
        observe=events.append,
    )
    return {
        "id": "success",
        "title": "Successful lifecycle",
        "policy": "fail fast",
        "candidates": "invoice from Visual-Invoice==1.0",
        "path": ["invoice:discovery:metadata only", *_paths(events)],
        "active": "invoice → report.invoice",
        "outcome": f"{rendered.media_type}; body returned but not logged",
        "decision": "Publish only after the offer passes host-owned validation.",
        "warning": "Discovery metadata did not authenticate or sandbox the provider.",
    }


def _duplicate_name() -> Scenario:
    events: list[LifecycleEvent] = []
    first = _candidate("invoice", lambda: _offer("invoice"), distribution="Visual-A")
    second = _candidate("invoice", lambda: _offer("invoice"), distribution="Visual-B")
    try:
        start_plugins((second, first), observe=events.append)
    except PluginStartupError as error:
        outcome = f"{len(error.failures)} registration failures; zero candidates loaded"
    else:
        raise AssertionError("duplicate-name scenario unexpectedly started")
    return {
        "id": "duplicate-name",
        "title": "Duplicate entry name",
        "policy": "fail fast",
        "candidates": "Visual-B and Visual-A both advertise invoice",
        "path": ["invoice:discovery:two metadata claims", *_paths(events)],
        "active": "none",
        "outcome": outcome,
        "decision": "Reject every claimant before load; order chooses no winner.",
        "warning": "Sorting makes failure deterministic, not one duplicate legitimate.",
    }


def _incompatible() -> Scenario:
    events: list[LifecycleEvent] = []
    entry = _candidate("future", lambda: _offer("future", api_major=2))
    try:
        start_plugins((entry,), observe=events.append)
    except PluginStartupError as error:
        outcome = f"{error.failures[0].stage.value}: incompatible API major"
    else:
        raise AssertionError("incompatible scenario unexpectedly started")
    return {
        "id": "incompatible",
        "title": "Compatibility failure",
        "policy": "fail fast",
        "candidates": "future declares plugin API major 2; host accepts 1",
        "path": ["future:discovery:metadata only", *_paths(events)],
        "active": "none",
        "outcome": outcome,
        "decision": (
            "Use the client contract and capabilities, not distribution version, to decide."
        ),
        "warning": "A version string is provenance input, not behavioral evidence.",
    }


def _duplicate_claim() -> Scenario:
    events: list[LifecycleEvent] = []
    alpha = _candidate("alpha", lambda: _offer("alpha", claim="report.invoice"))
    beta = _candidate("beta", lambda: _offer("beta", claim="report.invoice"))
    result = start_plugins(
        (beta, alpha),
        policy=HostPolicy(failure_policy=FailurePolicy.QUARANTINE),
        observe=events.append,
    )
    return {
        "id": "duplicate-claim",
        "title": "Duplicate semantic claim",
        "policy": "quarantine optional providers",
        "candidates": "alpha and beta have distinct names but both claim report.invoice",
        "path": ["group:discovery:two metadata entries", *_paths(events)],
        "active": ",".join(result.snapshot.names) or "none",
        "outcome": f"{len(result.quarantined)} claim failures; both excluded",
        "decision": "Validate the batch before publishing a claim index.",
        "warning": "Unique entry-point names do not imply unique business ownership.",
    }


def _load_quarantine() -> Scenario:
    events: list[LifecycleEvent] = []

    def broken_load() -> object:
        raise ImportError("synthetic import failure")

    broken = _candidate("broken", lambda: object(), loader=broken_load)
    status = _candidate("status", lambda: _offer("status"))
    result = start_plugins(
        (status, broken),
        policy=HostPolicy(failure_policy=FailurePolicy.QUARANTINE),
        observe=events.append,
    )
    return {
        "id": "load-quarantine",
        "title": "Optional load failure",
        "policy": "quarantine optional providers",
        "candidates": "broken import plus healthy status provider",
        "path": ["group:discovery:two metadata entries", *_paths(events)],
        "active": ",".join(result.snapshot.names),
        "outcome": "broken quarantined; status published",
        "decision": "Contain the optional failure without relabeling its load stage.",
        "warning": "The same outcome is unsafe if broken is required for readiness.",
    }


def _invocation_failure() -> Scenario:
    events: list[LifecycleEvent] = []

    def denied(_request: ReportRequest) -> RenderedReport:
        raise PermissionError("synthetic denial")

    entry = _candidate("restricted", lambda: _offer("restricted", renderer=denied))
    result = start_plugins((entry,), observe=events.append)
    try:
        invoke_plugin(
            result.snapshot,
            "restricted",
            ReportRequest("restricted", "secret-record"),
            observe=events.append,
        )
    except PermissionError:
        outcome = "PermissionError preserved at invocation"
    else:
        raise AssertionError("invocation-failure scenario unexpectedly succeeded")
    return {
        "id": "invocation-failure",
        "title": "Invocation failure",
        "policy": "startup succeeded",
        "candidates": "restricted is valid and active",
        "path": ["restricted:discovery:metadata only", *_paths(events)],
        "active": ",".join(result.snapshot.names),
        "outcome": outcome,
        "decision": "Preserve the handler exception and record only safe stage context.",
        "warning": "Successful activation does not prove every future call succeeds.",
    }


def lifecycle_scenarios() -> list[Scenario]:
    return [
        _success(),
        _duplicate_name(),
        _incompatible(),
        _duplicate_claim(),
        _load_quarantine(),
        _invocation_failure(),
    ]
