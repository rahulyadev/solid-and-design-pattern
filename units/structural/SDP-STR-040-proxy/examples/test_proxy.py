from collections.abc import Callable, Sized
from dataclasses import FrozenInstanceError, dataclass, fields
from typing import Protocol, cast, runtime_checkable

import pytest
from access_probe import Clock, probe
from catalog_contract import Catalog, Closed, ContractError, Document, Key, OwnedCatalog, headline
from catalog_proxy import CatalogProxy, MemoryCatalog, Observation

KEY = Key("orchard", "guide")
DOC = Document(KEY, 1, ("ready",))


@dataclass
class Rig:
    base: MemoryCatalog
    clock: Clock
    permissions: set[tuple[str, Key]]
    events: list[Observation]
    calls: list[str]
    proxy: CatalogProxy


def rig() -> Rig:
    base = MemoryCatalog({KEY: DOC})
    clock = Clock()
    permissions = {("reader", KEY)}
    events: list[Observation] = []
    calls: list[str] = []

    def authorize(principal: str, key: Key) -> None:
        calls.append("authorize")
        if (principal, key) not in permissions:
            raise PermissionError("denied")

    def factory() -> MemoryCatalog:
        calls.append("factory")
        return base

    proxy = CatalogProxy("reader", factory, authorize, ttl=10, clock=clock, observe=events.append)
    return Rig(base, clock, permissions, events, calls, proxy)


def allow(principal: str, key: Key) -> None:
    pass


@pytest.mark.parametrize("proxied", [False, True])
@pytest.mark.parametrize("lines", [(), ("ready",), ("first", "second")])
def test_shared_authorized_stable_snapshot_contract(proxied: bool, lines: tuple[str, ...]) -> None:
    base = MemoryCatalog({KEY: Document(KEY, 1, lines)})
    owner: OwnedCatalog = CatalogProxy("reader", lambda: base, allow, ttl=10) if proxied else base
    client: Catalog = owner
    try:
        assert client.read(KEY) == Document(KEY, 1, lines)
        assert headline(client, KEY) == (lines[0] if lines else "(empty)")
        with pytest.raises(KeyError):
            client.read(Key("orchard", "missing"))
    finally:
        owner.close()
    with pytest.raises(Closed):
        client.read(KEY)


def test_wiring_and_invalidation_do_not_construct() -> None:
    r = rig()
    r.proxy.invalidate()
    assert r.calls == []
    assert r.events == []
    assert r.base.reads == 0


def test_authorize_before_factory_and_again_on_hit() -> None:
    r = rig()
    assert r.proxy.read(KEY) is r.proxy.read(KEY)
    assert r.calls == ["authorize", "factory", "authorize"]
    assert r.base.reads == 1
    assert [event.outcome for event in r.events] == ["miss", "hit"]


@pytest.mark.parametrize("warm", [False, True])
def test_revocation_blocks_even_cached_access(warm: bool) -> None:
    r = rig()
    if warm:
        r.proxy.read(KEY)
    before = r.base.reads
    r.permissions.clear()
    with pytest.raises(PermissionError):
        r.proxy.read(KEY)
    assert r.base.reads == before
    assert r.calls.count("factory") == int(warm)
    assert r.events[-1].outcome == "denied"


@pytest.mark.parametrize("now,revision,reads", [(9.999, 1, 1), (10.0, 2, 2), (11.0, 2, 2)])
def test_exact_expiry_boundary(now: float, revision: int, reads: int) -> None:
    r = rig()
    r.proxy.read(KEY)
    r.base.put(Document(KEY, 2, ("new",)))
    r.clock.now = now
    assert r.proxy.read(KEY).revision == revision
    assert r.base.reads == reads


def test_invalidation_reloads_without_rebuilding() -> None:
    r = rig()
    r.proxy.read(KEY)
    r.base.put(Document(KEY, 2, ("new",)))
    r.proxy.invalidate()
    assert r.proxy.read(KEY).revision == 2
    assert r.calls.count("factory") == 1
    assert r.base.reads == 2


def test_full_key_and_one_slot_bound() -> None:
    r = rig()
    other = Key("meadow", KEY.document)
    r.permissions.add(("reader", other))
    r.base.put(Document(other, 8, ("other tenant",)))
    assert r.proxy.read(KEY) == DOC
    assert r.proxy.read(other).revision == 8
    assert r.proxy.read(KEY) == DOC
    assert r.base.reads == 3


def test_factory_failure_retries_only_on_later_call() -> None:
    attempts = 0
    base = MemoryCatalog({KEY: DOC})
    failure = OSError("construction failed")

    def factory() -> MemoryCatalog:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise failure
        return base

    proxy = CatalogProxy("reader", factory, allow, ttl=10)
    with pytest.raises(OSError) as raised:
        proxy.read(KEY)
    assert raised.value is failure
    assert attempts == 1
    assert proxy.read(KEY) == DOC
    assert attempts == 2


def test_read_failure_keeps_target_but_not_negative_cache() -> None:
    r = rig()
    missing = Key("orchard", "later")
    r.permissions.add(("reader", missing))
    for _ in range(2):
        with pytest.raises(KeyError):
            r.proxy.read(missing)
    r.base.put(Document(missing, 1, ()))
    assert r.proxy.read(missing).key == missing
    assert r.base.reads == 3
    assert r.calls.count("factory") == 1
    assert [event.outcome for event in r.events] == ["error", "error", "miss"]


def test_policy_error_fails_closed_without_construction() -> None:
    events: list[Observation] = []

    def policy(principal: str, key: Key) -> None:
        raise OSError("policy unavailable")

    def forbidden_factory() -> OwnedCatalog:
        pytest.fail("must not construct")

    proxy = CatalogProxy("reader", forbidden_factory, policy, ttl=10, observe=events.append)
    with pytest.raises(OSError, match="policy unavailable"):
        proxy.read(KEY)
    assert events == [Observation("error")]


def test_wrong_identity_is_rejected_and_not_cached() -> None:
    base = MemoryCatalog({KEY: Document(Key("meadow", "guide"), 1, ())})
    proxy = CatalogProxy("reader", lambda: base, allow, ttl=10)
    for _ in range(2):
        with pytest.raises(ContractError):
            proxy.read(KEY)
    assert base.reads == 2


def test_slow_load_does_not_extend_cache_window() -> None:
    clock = Clock()

    class SlowCatalog(MemoryCatalog):
        def read(self, key: Key, /) -> Document:
            clock.now += 20
            return super().read(key)

    base = SlowCatalog({KEY: DOC})
    proxy = CatalogProxy("reader", lambda: base, allow, ttl=10, clock=clock)
    proxy.read(KEY)
    proxy.read(KEY)
    assert base.reads == 2


@pytest.mark.parametrize("ttl", [0.0, -1.0, float("nan"), float("inf"), -float("inf")])
def test_invalid_ttl(ttl: float) -> None:
    with pytest.raises(ValueError):
        CatalogProxy("reader", lambda: MemoryCatalog({}), allow, ttl=ttl)


@pytest.mark.parametrize("warm", [False, True])
def test_close_is_terminal_and_does_not_build(warm: bool) -> None:
    r = rig()
    if warm:
        r.proxy.read(KEY)
    r.proxy.close()
    r.proxy.close()
    assert r.base.closes == int(warm)
    calls = r.calls.copy()
    events = r.events.copy()
    with pytest.raises(Closed):
        r.proxy.read(KEY)
    with pytest.raises(Closed):
        r.proxy.invalidate()
    assert r.calls == calls
    assert r.events == events


def test_close_failure_is_terminal_and_not_retried() -> None:
    class BrokenClose(MemoryCatalog):
        def close(self) -> None:
            self.closes += 1
            raise OSError("cleanup failed")

    base = BrokenClose({KEY: DOC})
    proxy = CatalogProxy("reader", lambda: base, allow, ttl=10)
    proxy.read(KEY)
    with pytest.raises(OSError, match="cleanup failed"):
        proxy.close()
    proxy.close()
    with pytest.raises(Closed):
        proxy.read(KEY)
    assert base.closes == 1


@pytest.mark.parametrize("success", [False, True])
def test_observer_exception_preserves_result_or_error(success: bool) -> None:
    seen: list[Observation] = []

    def observer(event: Observation) -> None:
        seen.append(event)
        raise ValueError("telemetry offline after recording")

    base = MemoryCatalog({KEY: DOC} if success else {})
    proxy = CatalogProxy("reader", lambda: base, allow, ttl=10, observe=observer)
    if success:
        assert proxy.read(KEY) == DOC
    else:
        with pytest.raises(KeyError):
            proxy.read(KEY)
    assert proxy.observer_failures == 1
    assert seen == [Observation("miss" if success else "error")]


@pytest.mark.parametrize("action", ["read", "invalidate", "close"])
def test_sequential_callback_reentry_is_rejected(action: str) -> None:
    attempted: list[str] = []
    proxy: CatalogProxy

    def observer(event: Observation) -> None:
        operations: dict[str, Callable[[], object]] = {
            "read": lambda: proxy.read(KEY),
            "invalidate": proxy.invalidate,
            "close": proxy.close,
        }
        with pytest.raises(RuntimeError, match="reentry"):
            operations[action]()
        attempted.append(action)

    base = MemoryCatalog({KEY: DOC})
    proxy = CatalogProxy("reader", lambda: base, allow, ttl=10, observe=observer)
    assert proxy.read(KEY) == DOC
    assert proxy.read(KEY) == DOC
    assert attempted == [action, action]
    proxy.close()


def test_observer_baseexception_can_interrupt_completed_read() -> None:
    calls = 0

    def observer(event: Observation) -> None:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise KeyboardInterrupt

    base = MemoryCatalog({KEY: DOC})
    proxy = CatalogProxy("reader", lambda: base, allow, ttl=10, observe=observer)
    with pytest.raises(KeyboardInterrupt):
        proxy.read(KEY)
    assert proxy.read(KEY) == DOC
    assert base.reads == 1
    assert proxy.observer_failures == 0


def test_snapshot_ordinary_mutation_is_rejected() -> None:
    field_name = "revision"
    with pytest.raises(FrozenInstanceError):
        setattr(DOC, field_name, 7)
    assert isinstance(DOC.lines, tuple)
    assert [field.name for field in fields(Observation)] == ["outcome"]


def test_saved_direct_capability_bypasses_policy() -> None:
    r = rig()
    direct = r.base.read
    r.permissions.clear()
    with pytest.raises(PermissionError):
        r.proxy.read(KEY)
    assert direct(KEY) == DOC
    assert id(r.proxy) != id(r.base)


class LengthForwarder:
    def __init__(self, inner: Sized) -> None:
        self.inner = inner

    def __getattr__(self, name: str) -> object:
        return getattr(self.inner, name)


@runtime_checkable
class HasLength(Protocol):
    def __len__(self) -> int: ...


def test_dynamic_forwarding_is_not_special_method_transparency() -> None:
    wrapper = LengthForwarder([1, 2])
    assert cast(Callable[[], int], wrapper.__len__)() == 2
    with pytest.raises(TypeError):
        len(cast(Sized, wrapper))  # Deliberately false cast; it adds no runtime method.


def test_runtime_protocol_dynamic_forwarding_version_boundary() -> None:
    import sys

    assert isinstance(LengthForwarder([1]), HasLength) is (sys.version_info < (3, 12))


def test_controlled_observation_table() -> None:
    assert probe() == [
        ("wired", "-", 0, 0, "-"),
        ("first", "1", 1, 1, "miss"),
        ("cached", "1", 1, 1, "hit"),
        ("revoked", "PermissionError", 1, 1, "denied"),
        ("expiry", "2", 1, 2, "miss"),
        ("invalidated", "3", 1, 3, "miss"),
        ("closed", "1", 1, 3, "-"),
    ]


def test_hits_do_not_slide_the_expiry_window() -> None:
    r = rig()
    r.proxy.read(KEY)
    r.clock.now = 9
    assert r.proxy.read(KEY).revision == 1
    r.base.put(Document(KEY, 2, ()))
    r.clock.now = 10
    assert r.proxy.read(KEY).revision == 2
    assert r.base.reads == 2


def test_denial_occurs_before_clock_access() -> None:
    def deny(principal: str, key: Key) -> None:
        raise PermissionError("denied")

    def forbidden_clock() -> float:
        pytest.fail("denial must not reach the clock")

    proxy = CatalogProxy("reader", lambda: MemoryCatalog({}), deny, ttl=10, clock=forbidden_clock)
    with pytest.raises(PermissionError):
        proxy.read(KEY)


def test_failed_other_key_load_discards_former_slot() -> None:
    r = rig()
    r.proxy.read(KEY)
    other = Key("orchard", "missing")
    r.permissions.add(("reader", other))
    with pytest.raises(KeyError):
        r.proxy.read(other)
    r.base.put(Document(KEY, 2, ()))
    assert r.proxy.read(KEY).revision == 2
    assert r.base.reads == 3


def test_principal_decisions_are_per_proxy() -> None:
    checks: list[str] = []

    def authorize(principal: str, key: Key) -> None:
        checks.append(principal)
        if principal != "reader":
            raise PermissionError("denied")

    reader = CatalogProxy("reader", lambda: MemoryCatalog({KEY: DOC}), authorize, ttl=10)
    visitor = CatalogProxy("visitor", lambda: MemoryCatalog({KEY: DOC}), authorize, ttl=10)
    try:
        assert reader.read(KEY) == DOC
        with pytest.raises(PermissionError):
            visitor.read(KEY)
        assert reader.read(KEY) == DOC
        assert checks == ["reader", "visitor", "reader"]
    finally:
        reader.close()
        visitor.close()


def test_real_subject_self_call_stays_on_real_receiver() -> None:
    class SelfCallingCatalog(MemoryCatalog):
        def read(self, key: Key, /) -> Document:
            return self.internal_read(key)

        def internal_read(self, key: Key) -> Document:
            return super().read(key)

    base = SelfCallingCatalog({KEY: DOC})
    checks: list[str] = []
    proxy = CatalogProxy("reader", lambda: base, lambda p, k: checks.append(p), ttl=10)
    assert proxy.read(KEY) == DOC
    assert checks == ["reader"]
    assert base.reads == 1
    proxy.close()


def test_root_finally_closes_constructed_target_after_read_error() -> None:
    base = MemoryCatalog({})
    proxy = CatalogProxy("reader", lambda: base, allow, ttl=10)
    with pytest.raises(KeyError):
        try:
            proxy.read(KEY)
        finally:
            proxy.close()
    assert base.closes == 1
    with pytest.raises(Closed):
        proxy.read(KEY)
