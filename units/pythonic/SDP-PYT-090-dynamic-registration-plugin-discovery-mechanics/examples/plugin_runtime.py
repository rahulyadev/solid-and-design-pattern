"""Small, governed plugin startup pipeline for SDP-PYT-090.

The module deliberately keeps registration, discovery, loading, construction,
validation, activation, and invocation visible as separate boundaries.  It is
an instructional application component, not a general-purpose plugin framework.
"""

from __future__ import annotations

import importlib
import re
from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from importlib import metadata
from types import MappingProxyType
from typing import Protocol, cast

ENTRY_POINT_GROUP = "sdp.pyt090.reporters"
_NAME_PATTERN = re.compile(r"[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*\Z")


class LifecycleStage(StrEnum):
    REGISTRATION = "registration"
    DISCOVERY = "discovery"
    LOAD = "load"
    CONSTRUCTION = "construction"
    VALIDATION = "validation"
    ACTIVATION = "activation"
    INVOCATION = "invocation"


class FailurePolicy(StrEnum):
    FAIL_FAST = "fail_fast"
    QUARANTINE = "quarantine"


class CandidateSource(StrEnum):
    CONFIGURED_IMPORT = "configured_import"
    STATIC = "static"
    ENTRY_POINT = "entry_point"


@dataclass(frozen=True, slots=True)
class ReportRequest:
    report_kind: str
    record_id: str


@dataclass(frozen=True, slots=True)
class RenderedReport:
    media_type: str
    body: str


ReportRenderer = Callable[[ReportRequest], RenderedReport]
PluginProvider = Callable[[], object]


@dataclass(frozen=True, slots=True)
class PluginManifest:
    """Client-owned values returned by a provider factory.

    Validation intentionally lives in the host rather than ``__post_init__`` so
    construction errors and contract-validation errors remain distinguishable.
    """

    name: str
    api_major: int
    capabilities: frozenset[str]
    claims: frozenset[str]


@dataclass(frozen=True, slots=True)
class PluginOffer:
    manifest: PluginManifest
    render: ReportRenderer


class DistributionLike(Protocol):
    @property
    def version(self) -> str: ...

    @property
    def metadata(self) -> Mapping[str, str]: ...


class EntryPointLike(Protocol):
    name: str
    value: str
    group: str

    @property
    def dist(self) -> DistributionLike | None: ...

    def load(self) -> object: ...


@dataclass(frozen=True, slots=True)
class PluginCandidate:
    entry_name: str
    object_ref: str
    distribution: str
    version: str
    source: CandidateSource
    loader: Callable[[], object]

    @property
    def provider_id(self) -> str:
        return f"{self.distribution}=={self.version}:{self.entry_name}"


@dataclass(frozen=True, slots=True)
class HostPolicy:
    api_major: int = 1
    required_capabilities: frozenset[str] = frozenset()
    enabled_names: frozenset[str] | None = None
    required_names: frozenset[str] = frozenset()
    allowed_distributions: frozenset[str] | None = None
    failure_policy: FailurePolicy = FailurePolicy.FAIL_FAST


DEFAULT_HOST_POLICY = HostPolicy()


@dataclass(frozen=True, slots=True)
class LifecycleEvent:
    provider: str
    distribution: str
    version: str
    stage: LifecycleStage
    outcome: str


ObservationSink = Callable[[LifecycleEvent], None]


@dataclass(frozen=True, slots=True)
class PluginFailure:
    candidate: PluginCandidate
    stage: LifecycleStage
    error_type: str
    reason: str


class DiscoveryError(RuntimeError):
    """The host could not enumerate metadata for the requested group."""


class PluginStartupError(RuntimeError):
    def __init__(self, failures: Iterable[PluginFailure]) -> None:
        ordered = tuple(failures)
        if not ordered:
            raise ValueError("PluginStartupError requires at least one failure")
        self.failures = ordered
        first = ordered[0]
        super().__init__(
            f"plugin startup failed at {first.stage.value} for "
            f"{first.candidate.provider_id}: {first.reason}"
        )


class PluginActivationError(RuntimeError):
    """Required validated providers could not be published."""


class UnknownPluginError(LookupError):
    """Invocation requested a provider absent from the published snapshot."""


@dataclass(frozen=True, slots=True)
class ActivatedPlugin:
    candidate: PluginCandidate
    offer: PluginOffer


@dataclass(frozen=True, slots=True)
class RegistrySnapshot:
    """Immutable bindings published after startup validation completes."""

    _by_name: Mapping[str, ActivatedPlugin]
    _claim_owner: Mapping[str, str]

    @classmethod
    def publish(cls, plugins: Iterable[ActivatedPlugin]) -> RegistrySnapshot:
        ordered = sorted(plugins, key=lambda plugin: candidate_order_key(plugin.candidate))
        by_name = {plugin.offer.manifest.name: plugin for plugin in ordered}
        claim_owner = {
            claim: plugin.offer.manifest.name
            for plugin in ordered
            for claim in sorted(plugin.offer.manifest.claims)
        }
        return cls(MappingProxyType(by_name), MappingProxyType(claim_owner))

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(self._by_name)

    @property
    def claim_owners(self) -> Mapping[str, str]:
        return self._claim_owner

    def resolve(self, name: str) -> ActivatedPlugin:
        try:
            return self._by_name[name]
        except KeyError:
            raise UnknownPluginError(f"plugin is not active: {name!r}") from None


@dataclass(frozen=True, slots=True)
class StartupResult:
    snapshot: RegistrySnapshot
    quarantined: tuple[PluginFailure, ...]


def _ignore_event(_event: LifecycleEvent) -> None:
    return None


def _safe_distribution(entry_point: EntryPointLike) -> tuple[str, str]:
    distribution = getattr(entry_point, "dist", None)
    if distribution is None:
        return "<unknown-distribution>", "<unknown-version>"
    name = distribution.metadata.get("Name", "<unknown-distribution>")
    return str(name), str(distribution.version)


def candidate_from_entry_point(entry_point: EntryPointLike) -> PluginCandidate:
    distribution, version = _safe_distribution(entry_point)
    return PluginCandidate(
        entry_name=entry_point.name,
        object_ref=entry_point.value,
        distribution=distribution,
        version=version,
        source=CandidateSource.ENTRY_POINT,
        loader=entry_point.load,
    )


def configured_import_candidate(
    *,
    name: str,
    module: str,
    attribute: str,
    distribution: str = "application-config",
    version: str = "local",
) -> PluginCandidate:
    """Create a candidate from an explicit module allow-list without importing yet."""

    def load_configured() -> object:
        loaded_module = importlib.import_module(module)
        return getattr(loaded_module, attribute)

    return PluginCandidate(
        entry_name=name,
        object_ref=f"{module}:{attribute}",
        distribution=distribution,
        version=version,
        source=CandidateSource.CONFIGURED_IMPORT,
        loader=load_configured,
    )


def static_candidate(
    *,
    name: str,
    provider: PluginProvider,
    distribution: str = "application",
    version: str = "local",
) -> PluginCandidate:
    """Register an already imported provider at an explicit composition root."""

    return PluginCandidate(
        entry_name=name,
        object_ref=f"{provider.__module__}:{provider.__qualname__}",
        distribution=distribution,
        version=version,
        source=CandidateSource.STATIC,
        loader=lambda: provider,
    )


def candidate_order_key(candidate: PluginCandidate) -> tuple[str, str, str, str, str]:
    return (
        candidate.entry_name.casefold(),
        normalize_distribution_name(candidate.distribution),
        candidate.version,
        candidate.object_ref,
        candidate.source.value,
    )


def normalize_distribution_name(name: str) -> str:
    """Apply the PyPA comparison normalization for distribution names."""

    return re.sub(r"[-_.]+", "-", name).casefold()


def discover_entry_point_candidates(
    group: str = ENTRY_POINT_GROUP,
    *,
    source: Callable[..., Iterable[EntryPointLike]] | None = None,
    observe: ObservationSink = _ignore_event,
) -> tuple[PluginCandidate, ...]:
    """Discover metadata only; no returned entry point is loaded here."""

    try:
        selected = (
            cast(Iterable[EntryPointLike], metadata.entry_points(group=group))
            if source is None
            else source(group=group)
        )
        candidates = tuple(candidate_from_entry_point(entry_point) for entry_point in selected)
    except Exception as error:
        raise DiscoveryError(f"entry-point discovery failed for group {group!r}") from error
    ordered = tuple(sorted(candidates, key=candidate_order_key))
    for candidate in ordered:
        observe(_event(candidate, LifecycleStage.DISCOVERY, "found"))
    return ordered


def _event(candidate: PluginCandidate, stage: LifecycleStage, outcome: str) -> LifecycleEvent:
    return LifecycleEvent(
        provider=candidate.entry_name,
        distribution=candidate.distribution,
        version=candidate.version,
        stage=stage,
        outcome=outcome,
    )


def _failure(
    candidate: PluginCandidate,
    stage: LifecycleStage,
    error: BaseException | str,
) -> PluginFailure:
    if isinstance(error, str):
        return PluginFailure(candidate, stage, "PluginPolicyError", error)
    return PluginFailure(candidate, stage, type(error).__name__, str(error))


def _record_failure(
    failure: PluginFailure,
    *,
    policy: HostPolicy,
    failures: list[PluginFailure],
    observe: ObservationSink,
) -> None:
    observe(_event(failure.candidate, failure.stage, f"error:{failure.error_type}"))
    if policy.failure_policy is FailurePolicy.FAIL_FAST:
        raise PluginStartupError((failure,))
    failures.append(failure)


def _registration_failures(
    candidates: tuple[PluginCandidate, ...], policy: HostPolicy
) -> tuple[PluginFailure, ...]:
    failures: list[PluginFailure] = []
    by_name: dict[str, list[PluginCandidate]] = defaultdict(list)
    for candidate in candidates:
        by_name[candidate.entry_name].append(candidate)
        if not _NAME_PATTERN.fullmatch(candidate.entry_name):
            failures.append(
                _failure(
                    candidate,
                    LifecycleStage.REGISTRATION,
                    f"invalid entry-point name {candidate.entry_name!r}",
                )
            )
        if not candidate.object_ref.strip():
            failures.append(
                _failure(candidate, LifecycleStage.REGISTRATION, "empty object reference")
            )
        if not candidate.distribution.strip() or not candidate.version.strip():
            failures.append(
                _failure(
                    candidate,
                    LifecycleStage.REGISTRATION,
                    "incomplete distribution provenance",
                )
            )

    for name, claimants in sorted(by_name.items()):
        if len(claimants) > 1:
            reason = f"duplicate entry-point name {name!r}; no claimant wins by ordering"
            failures.extend(
                _failure(candidate, LifecycleStage.REGISTRATION, reason) for candidate in claimants
            )

    allowed = policy.allowed_distributions
    if allowed is not None:
        normalized_allowed = {normalize_distribution_name(name) for name in allowed}
        for candidate in candidates:
            if normalize_distribution_name(candidate.distribution) not in normalized_allowed:
                failures.append(
                    _failure(
                        candidate,
                        LifecycleStage.REGISTRATION,
                        f"distribution {candidate.distribution!r} is not allow-listed",
                    )
                )
    return tuple(sorted(failures, key=lambda item: candidate_order_key(item.candidate)))


def _validate_offer(candidate: PluginCandidate, value: object, policy: HostPolicy) -> PluginOffer:
    if not isinstance(value, PluginOffer):
        raise TypeError("provider must return the client-owned PluginOffer dataclass")
    manifest = value.manifest
    if not _NAME_PATTERN.fullmatch(manifest.name):
        raise ValueError(f"invalid plugin name: {manifest.name!r}")
    if manifest.name != candidate.entry_name:
        raise ValueError(
            f"manifest name {manifest.name!r} does not match entry-point name "
            f"{candidate.entry_name!r}"
        )
    if manifest.api_major != policy.api_major:
        raise ValueError(
            f"plugin API major {manifest.api_major} is incompatible with host "
            f"major {policy.api_major}"
        )
    if not isinstance(manifest.capabilities, frozenset) or not all(
        isinstance(item, str) and _NAME_PATTERN.fullmatch(item) for item in manifest.capabilities
    ):
        raise TypeError("capabilities must be normalized non-empty strings in a frozenset")
    if (
        not isinstance(manifest.claims, frozenset)
        or not manifest.claims
        or not all(
            isinstance(item, str) and _NAME_PATTERN.fullmatch(item) for item in manifest.claims
        )
    ):
        raise TypeError("claims must be normalized non-empty strings in a non-empty frozenset")
    missing = policy.required_capabilities - manifest.capabilities
    if missing:
        raise ValueError(f"missing required capabilities: {', '.join(sorted(missing))}")
    if not callable(value.render):
        raise TypeError("PluginOffer.render must be callable")
    return value


def _semantic_duplicate_failures(
    validated: tuple[ActivatedPlugin, ...],
) -> tuple[PluginFailure, ...]:
    by_claim: dict[str, list[ActivatedPlugin]] = defaultdict(list)
    for plugin in validated:
        for claim in plugin.offer.manifest.claims:
            by_claim[claim].append(plugin)

    failures: list[PluginFailure] = []
    for claim, claimants in sorted(by_claim.items()):
        if len(claimants) > 1:
            names = ", ".join(sorted(plugin.offer.manifest.name for plugin in claimants))
            reason = f"semantic claim {claim!r} is duplicated by {names}; all claimants rejected"
            failures.extend(
                _failure(plugin.candidate, LifecycleStage.VALIDATION, reason)
                for plugin in claimants
            )
    unique = {
        (failure.candidate.provider_id, failure.stage, failure.reason): failure
        for failure in failures
    }
    return tuple(sorted(unique.values(), key=lambda item: candidate_order_key(item.candidate)))


def start_plugins(
    configured: Iterable[PluginCandidate],
    discovered: Iterable[PluginCandidate] = (),
    *,
    policy: HostPolicy = DEFAULT_HOST_POLICY,
    observe: ObservationSink = _ignore_event,
) -> StartupResult:
    """Build and atomically publish one process-local registry snapshot."""

    combined = tuple(sorted((*configured, *discovered), key=candidate_order_key))
    if policy.enabled_names is not None:
        enabled = policy.enabled_names
        candidates = tuple(candidate for candidate in combined if candidate.entry_name in enabled)
    else:
        candidates = combined

    failures: list[PluginFailure] = []
    invalid_candidate_ids: set[int] = set()
    registration_failures = _registration_failures(candidates, policy)
    if registration_failures and policy.failure_policy is FailurePolicy.FAIL_FAST:
        for failure in registration_failures:
            observe(_event(failure.candidate, failure.stage, f"error:{failure.error_type}"))
        raise PluginStartupError(registration_failures)
    for failure in registration_failures:
        failures.append(failure)
        invalid_candidate_ids.add(id(failure.candidate))
        observe(_event(failure.candidate, failure.stage, f"error:{failure.error_type}"))

    validated: list[ActivatedPlugin] = []
    for candidate in candidates:
        if id(candidate) in invalid_candidate_ids:
            continue
        observe(_event(candidate, LifecycleStage.REGISTRATION, "accepted"))

        try:
            loaded = candidate.loader()
        except Exception as error:
            _record_failure(
                _failure(candidate, LifecycleStage.LOAD, error),
                policy=policy,
                failures=failures,
                observe=observe,
            )
            continue
        observe(_event(candidate, LifecycleStage.LOAD, "ok"))

        try:
            provider = cast(PluginProvider, loaded)
            constructed = provider()
        except Exception as error:
            _record_failure(
                _failure(candidate, LifecycleStage.CONSTRUCTION, error),
                policy=policy,
                failures=failures,
                observe=observe,
            )
            continue
        observe(_event(candidate, LifecycleStage.CONSTRUCTION, "ok"))

        try:
            offer = _validate_offer(candidate, constructed, policy)
        except Exception as error:
            _record_failure(
                _failure(candidate, LifecycleStage.VALIDATION, error),
                policy=policy,
                failures=failures,
                observe=observe,
            )
            continue
        observe(_event(candidate, LifecycleStage.VALIDATION, "ok"))
        validated.append(ActivatedPlugin(candidate, offer))

    duplicate_failures = _semantic_duplicate_failures(tuple(validated))
    if duplicate_failures:
        if policy.failure_policy is FailurePolicy.FAIL_FAST:
            for failure in duplicate_failures:
                observe(_event(failure.candidate, failure.stage, f"error:{failure.error_type}"))
            raise PluginStartupError(duplicate_failures)
        duplicate_candidate_ids = {id(failure.candidate) for failure in duplicate_failures}
        validated = [
            plugin for plugin in validated if id(plugin.candidate) not in duplicate_candidate_ids
        ]
        failures.extend(duplicate_failures)
        for failure in duplicate_failures:
            observe(_event(failure.candidate, failure.stage, f"error:{failure.error_type}"))

    active_names = {plugin.offer.manifest.name for plugin in validated}
    missing_required = policy.required_names - active_names
    if missing_required:
        names = ", ".join(sorted(missing_required))
        raise PluginActivationError(f"required plugins are not activatable: {names}")

    snapshot = RegistrySnapshot.publish(validated)
    for plugin in validated:
        observe(_event(plugin.candidate, LifecycleStage.ACTIVATION, "published"))
    return StartupResult(snapshot=snapshot, quarantined=tuple(failures))


def invoke_plugin(
    snapshot: RegistrySnapshot,
    name: str,
    request: ReportRequest,
    *,
    observe: ObservationSink = _ignore_event,
) -> RenderedReport:
    plugin = snapshot.resolve(name)
    candidate = plugin.candidate
    try:
        result = plugin.offer.render(request)
        if not isinstance(result, RenderedReport):
            raise TypeError("plugin renderer must return RenderedReport")
    except Exception as error:
        observe(_event(candidate, LifecycleStage.INVOCATION, f"error:{type(error).__name__}"))
        raise
    observe(_event(candidate, LifecycleStage.INVOCATION, "ok"))
    return result
