"""Behavior, policy, lifecycle, and failure-boundary tests."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, replace

import pytest
from plugin_runtime import (
    CandidateSource,
    DiscoveryError,
    FailurePolicy,
    HostPolicy,
    LifecycleEvent,
    LifecycleStage,
    PluginActivationError,
    PluginCandidate,
    PluginManifest,
    PluginOffer,
    PluginStartupError,
    RegistrySnapshot,
    RenderedReport,
    ReportRequest,
    UnknownPluginError,
    candidate_from_entry_point,
    discover_entry_point_candidates,
    invoke_plugin,
    start_plugins,
    static_candidate,
)


@dataclass(frozen=True)
class FakeDistribution:
    name: str
    version: str

    @property
    def metadata(self) -> Mapping[str, str]:
        return {"Name": self.name}


@dataclass
class FakeEntryPoint:
    name: str
    value: str
    group: str
    loaded: object
    dist: FakeDistribution | None = None
    load_count: int = 0

    def load(self) -> object:
        self.load_count += 1
        if isinstance(self.loaded, Exception):
            raise self.loaded
        return self.loaded


def offer(
    name: str,
    *,
    api_major: int = 1,
    capabilities: frozenset[str] = frozenset({"format.text"}),
    claims: frozenset[str] | None = None,
    renderer: Callable[[ReportRequest], RenderedReport] | None = None,
) -> PluginOffer:
    claim_set = claims if claims is not None else frozenset({f"report.{name}"})

    def default_renderer(request: ReportRequest) -> RenderedReport:
        return RenderedReport("text/plain", f"{name}:{request.record_id}")

    return PluginOffer(
        PluginManifest(name, api_major, capabilities, claim_set),
        renderer or default_renderer,
    )


def candidate(
    name: str,
    provider: Callable[[], object],
    *,
    distribution: str | None = None,
    object_ref: str | None = None,
) -> PluginCandidate:
    return PluginCandidate(
        entry_name=name,
        object_ref=object_ref or f"fixture_{name}:provide",
        distribution=distribution or f"dist-{name}",
        version="1.0",
        source=CandidateSource.ENTRY_POINT,
        loader=lambda: provider,
    )


def assert_startup_stage(
    error: pytest.ExceptionInfo[PluginStartupError], stage: LifecycleStage
) -> None:
    assert error.value.failures[0].stage is stage


def test_discovery_reads_metadata_without_loading_and_sorts() -> None:
    zulu = FakeEntryPoint(
        "zulu",
        "zulu_runtime:provide",
        "sdp.pyt090.reporters",
        lambda: offer("zulu"),
        FakeDistribution("Zulu-Dist", "2.0"),
    )
    alpha = FakeEntryPoint(
        "alpha",
        "alpha_runtime:provide",
        "sdp.pyt090.reporters",
        lambda: offer("alpha"),
        FakeDistribution("Alpha-Dist", "1.0"),
    )

    def source(**selection: str) -> Iterable[FakeEntryPoint]:
        assert selection == {"group": "sdp.pyt090.reporters"}
        return (zulu, alpha)

    discovered = discover_entry_point_candidates(source=source)

    assert [item.entry_name for item in discovered] == ["alpha", "zulu"]
    assert [item.distribution for item in discovered] == ["Alpha-Dist", "Zulu-Dist"]
    assert zulu.load_count == alpha.load_count == 0


def test_entry_point_without_distribution_has_explicit_unknown_provenance() -> None:
    entry_point = FakeEntryPoint("alpha", "alpha:provide", "group", object())

    result = candidate_from_entry_point(entry_point)

    assert result.distribution == "<unknown-distribution>"
    assert result.version == "<unknown-version>"


def test_discovery_failure_does_not_become_a_plugin_load_failure() -> None:
    def broken_source(**_selection: str) -> Iterable[FakeEntryPoint]:
        raise OSError("metadata store unavailable")

    with pytest.raises(DiscoveryError) as error:
        discover_entry_point_candidates(source=broken_source)

    assert isinstance(error.value.__cause__, OSError)


def test_enabled_names_filter_happens_before_load() -> None:
    loaded: list[str] = []

    def provider_for(name: str) -> Callable[[], object]:
        def load_provider() -> object:
            loaded.append(name)
            return lambda: offer(name)

        return load_provider

    alpha = candidate("alpha", lambda: offer("alpha"))
    beta = candidate("beta", lambda: offer("beta"))
    alpha = replace(alpha, loader=provider_for("alpha"))
    beta = replace(beta, loader=provider_for("beta"))

    result = start_plugins((alpha, beta), policy=HostPolicy(enabled_names=frozenset({"beta"})))

    assert result.snapshot.names == ("beta",)
    assert loaded == ["beta"]


def test_duplicate_names_reject_every_claimant_before_load() -> None:
    loads: list[str] = []

    def loader(label: str) -> Callable[[], object]:
        def load() -> object:
            loads.append(label)
            return lambda: offer("same")

        return load

    first = candidate("same", lambda: offer("same"), distribution="dist-a")
    second = candidate("same", lambda: offer("same"), distribution="dist-b")
    first = PluginCandidate(
        first.entry_name,
        first.object_ref,
        first.distribution,
        first.version,
        first.source,
        loader("a"),
    )
    second = PluginCandidate(
        second.entry_name,
        second.object_ref,
        second.distribution,
        second.version,
        second.source,
        loader("b"),
    )

    with pytest.raises(PluginStartupError) as error:
        start_plugins((second, first))

    assert {failure.candidate.distribution for failure in error.value.failures} == {
        "dist-a",
        "dist-b",
    }
    assert all(failure.stage is LifecycleStage.REGISTRATION for failure in error.value.failures)
    assert loads == []


def test_distribution_allow_list_rejects_before_load() -> None:
    entry = candidate("alpha", lambda: offer("alpha"), distribution="Unexpected-Dist")

    with pytest.raises(PluginStartupError) as error:
        start_plugins((entry,), policy=HostPolicy(allowed_distributions=frozenset({"Known-Dist"})))

    assert_startup_stage(error, LifecycleStage.REGISTRATION)


def test_distribution_allow_list_uses_packaging_name_normalization() -> None:
    entry = candidate("alpha", lambda: offer("alpha"), distribution="Acme.Plugin_Name")

    result = start_plugins(
        (entry,), policy=HostPolicy(allowed_distributions=frozenset({"acme-plugin-name"}))
    )

    assert result.snapshot.names == ("alpha",)


def test_invalid_entry_name_is_rejected_before_load() -> None:
    loaded = False

    def load() -> object:
        nonlocal loaded
        loaded = True
        return lambda: offer("invalid-name")

    entry = PluginCandidate(
        entry_name="Invalid Name",
        object_ref="fixture:provide",
        distribution="Fixture",
        version="1.0",
        source=CandidateSource.ENTRY_POINT,
        loader=load,
    )

    with pytest.raises(PluginStartupError) as error:
        start_plugins((entry,))

    assert_startup_stage(error, LifecycleStage.REGISTRATION)
    assert loaded is False


def test_load_failure_keeps_its_stage_and_cause_type() -> None:
    def load() -> object:
        raise ImportError("missing optional dependency")

    entry = candidate("alpha", lambda: offer("alpha"))
    entry = PluginCandidate(
        entry.entry_name, entry.object_ref, entry.distribution, entry.version, entry.source, load
    )

    with pytest.raises(PluginStartupError) as error:
        start_plugins((entry,))

    assert_startup_stage(error, LifecycleStage.LOAD)
    assert error.value.failures[0].error_type == "ImportError"


def test_construction_failure_is_not_mislabeled_as_load() -> None:
    def provider() -> object:
        raise RuntimeError("provider configuration rejected")

    with pytest.raises(PluginStartupError) as error:
        start_plugins((candidate("alpha", provider),))

    assert_startup_stage(error, LifecycleStage.CONSTRUCTION)


@pytest.mark.parametrize(
    ("value", "reason"),
    [
        (object(), "PluginOffer"),
        (offer("wrong-name"), "does not match"),
        (offer("alpha", api_major=2), "incompatible"),
        (
            offer("alpha", capabilities=frozenset()),
            "missing required capabilities",
        ),
        (offer("alpha", claims=frozenset()), "claims"),
    ],
)
def test_validation_failures_are_distinct(value: object, reason: str) -> None:
    policy = HostPolicy(required_capabilities=frozenset({"format.text"}))

    with pytest.raises(PluginStartupError) as error:
        start_plugins((candidate("alpha", lambda: value),), policy=policy)

    assert_startup_stage(error, LifecycleStage.VALIDATION)
    assert reason in error.value.failures[0].reason


def test_semantic_duplicate_rejects_all_claimants_in_fail_fast_mode() -> None:
    shared = frozenset({"report.invoice"})
    alpha = candidate("alpha", lambda: offer("alpha", claims=shared))
    beta = candidate("beta", lambda: offer("beta", claims=shared))

    with pytest.raises(PluginStartupError) as error:
        start_plugins((beta, alpha))

    assert {failure.candidate.entry_name for failure in error.value.failures} == {"alpha", "beta"}
    assert all(failure.stage is LifecycleStage.VALIDATION for failure in error.value.failures)


def test_quarantine_excludes_invalid_and_duplicate_claimants_without_choosing_winner() -> None:
    shared = frozenset({"report.invoice"})
    alpha = candidate("alpha", lambda: offer("alpha", claims=shared))
    beta = candidate("beta", lambda: offer("beta", claims=shared))
    good = candidate("status", lambda: offer("status"))
    broken = candidate("broken", lambda: object())

    result = start_plugins(
        (beta, good, broken, alpha),
        policy=HostPolicy(failure_policy=FailurePolicy.QUARANTINE),
    )

    assert result.snapshot.names == ("status",)
    assert {failure.candidate.entry_name for failure in result.quarantined} == {
        "alpha",
        "beta",
        "broken",
    }


def test_required_plugin_failure_blocks_activation_even_in_quarantine_mode() -> None:
    broken = candidate("required", lambda: object())

    with pytest.raises(PluginActivationError, match="required"):
        start_plugins(
            (broken,),
            policy=HostPolicy(
                required_names=frozenset({"required"}),
                failure_policy=FailurePolicy.QUARANTINE,
            ),
        )


def test_snapshot_bindings_are_read_only_and_claims_are_resolvable() -> None:
    result = start_plugins((candidate("alpha", lambda: offer("alpha")),))

    assert result.snapshot.claim_owners["report.alpha"] == "alpha"
    with pytest.raises(TypeError):
        result.snapshot.claim_owners["report.beta"] = "beta"  # type: ignore[index]


def test_startup_is_idempotent_when_provider_factory_is_repeatable() -> None:
    entry = candidate("alpha", lambda: offer("alpha"))

    first = start_plugins((entry,))
    second = start_plugins((entry,))

    assert first.snapshot.names == second.snapshot.names == ("alpha",)
    assert dict(first.snapshot.claim_owners) == dict(second.snapshot.claim_owners)


def test_invocation_success_emits_safe_provenance_without_request_body() -> None:
    events: list[LifecycleEvent] = []
    result = start_plugins((candidate("alpha", lambda: offer("alpha")),))

    rendered = invoke_plugin(
        result.snapshot,
        "alpha",
        ReportRequest("alpha", "secret-record-7"),
        observe=events.append,
    )

    assert rendered.body == "alpha:secret-record-7"
    assert events == [LifecycleEvent("alpha", "dist-alpha", "1.0", LifecycleStage.INVOCATION, "ok")]
    assert "secret-record-7" not in repr(events)


def test_handler_error_keeps_identity_and_invocation_stage() -> None:
    failure = LookupError("record unavailable")

    def renderer(_request: ReportRequest) -> RenderedReport:
        raise failure

    events: list[LifecycleEvent] = []
    result = start_plugins((candidate("alpha", lambda: offer("alpha", renderer=renderer)),))

    with pytest.raises(LookupError) as error:
        invoke_plugin(
            result.snapshot,
            "alpha",
            ReportRequest("alpha", "record-7"),
            observe=events.append,
        )

    assert error.value is failure
    assert events[-1].outcome == "error:LookupError"
    assert events[-1].stage is LifecycleStage.INVOCATION


def test_wrong_result_type_fails_at_invocation_not_startup() -> None:
    def wrong_result(_request: ReportRequest) -> RenderedReport:
        return "not-a-rendered-report"  # type: ignore[return-value]

    result = start_plugins((candidate("alpha", lambda: offer("alpha", renderer=wrong_result)),))

    with pytest.raises(TypeError, match="RenderedReport"):
        invoke_plugin(result.snapshot, "alpha", ReportRequest("alpha", "record-8"))


def test_unknown_plugin_is_a_resolution_failure_before_handler_call() -> None:
    snapshot = RegistrySnapshot.publish(())

    with pytest.raises(UnknownPluginError, match="missing"):
        invoke_plugin(snapshot, "missing", ReportRequest("status", "record-9"))


def test_static_registration_does_not_need_discovery() -> None:
    def provider() -> object:
        return offer("alpha")

    entry = static_candidate(name="alpha", provider=provider)

    result = start_plugins((entry,))

    assert result.snapshot.names == ("alpha",)
    assert entry.source is CandidateSource.STATIC
