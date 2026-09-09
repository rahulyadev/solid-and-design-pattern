# SDP-STR-040 — Proxy

## Physical Notebook Core

### Problem or change pressure

A document preview should open its catalog only if someone may read it. Repeated previews can reuse
recent content, but a revoked reader must be denied even when the content is already cached.

### One-sentence mental model

> Give the client a representative that decides whether, when, and how to reach the real capability.

### One essential visual

```text
preview → CatalogProxy.read(key) → authorize fixed principal + full key
                 │ denied → raise; no target access
                 │ allowed + fresh matching slot → return cached snapshot
                 └ allowed + miss → construct once if needed → real Catalog.read(key)
owner → proxy.close() → close constructed target, if any
```

### How to read this visual

Read the access paths top to bottom. Arrows are calls or decisions; the three paths are alternatives.
The owner has an administration capability that the preview does not need.

### Key insight

A cache hit skips storage, so authorization must happen before the hit can return data.

### Simplification or limitation

This is a conceptual sequential flow, not memory layout, network traffic, or a rendered browser
figure. It omits errors, telemetry and reentry checks. Permission checking and data retrieval are
separate steps; this picture does not promise atomic revocation.

### Governing rules or invariants

1. Describe compatibility in meaning, failures, freshness, effects and lifetime, beyond signatures.
2. Decide which access paths can bypass the representative; a Python wrapper is no security sandbox.
3. State who owns the target, what is cached, and what happens after failed construction or close.

### Minimal Python example

```python
from collections.abc import Callable


def guarded(read: Callable[[str], str], check: Callable[[str], None]) -> Callable[[str], str]:
    def access(key: str) -> str:
        check(key)  # Return normally to allow; raise to deny.
        return read(key)

    return access


def allow_public(key: str) -> None:
    if key != "public":
        raise PermissionError("denied")


assert guarded(lambda key: "ready", allow_public)("public") == "ready"
```

### One common misconception

**Mistake:** A proxy is indistinguishable from its target because both have `read`.

**Correction:** The call shape can match while identity, access, latency, errors or freshness differ.
Name those differences so the client can make a correct decision.

### Important trade-offs

- Deferred construction saves unused work but moves failure to first access.
- Caching saves reads but makes freshness and shared results part of the contract.
- Central access policy helps consistent callers; bypasses still need a real enforcement boundary.

### Interview-revision cues

- Recognition: the capability stays recognizable; access to it needs mediation.
- Trace: permission → cache decision → optional construction → real read.
- Rejection: one caller with an already available dependency may need only a helper.

## Unit metadata

| Field | Value |
|---|---|
| Domain | GoF structural patterns |
| Curriculum | [SDP-STR-040](../../../CURRICULUM.md#sdp-str-040) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Control access to another object for laziness, authorization, caching, remoting, or observation while keeping semantic differences visible. |
| Hard prerequisites | [SDP-FND-050](../../../CURRICULUM.md#sdp-fnd-050), [SDP-FND-070](../../../CURRICULUM.md#sdp-fnd-070) |
| Soft prerequisites | None |
| Priority | Core |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D2 |
| Scope | GoF, Structural, Backend |
| Size | L |
| First understanding | 4–6 h |
| Hands-on practice | 5–9 h |
| Evidence profile | E+I+D+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Draft |

Frequency labels are curriculum judgments, not measured statistics. Learning remains **Not started**.
Generated notes and maintainer checks do not supply Rahul's evidence. Study the
[demo](examples/run_proxy_demo.py), then attempt the independent [lab](practice/README.md).
The [controlled experiment](experiments/EXP-01-access-and-freshness/README.md) supports E/D without
adding X to the canonical profile. [Validation](VALIDATION.md) records actual checks.

## 1. Simple explanation and prerequisite bridge

The preview asks for a document. The representative first checks whether its configured reader may
see that document. It may then return a recent snapshot or ask the real catalog. The preview knows
the reading operation; the representative knows the access rules.

From SDP-FND-050: composition stores a collaborator, delegation calls it, inheritance relates
classes. From SDP-FND-070: a Protocol describes a capability for static checking; compatible types
do not prove compatible business behavior. Both prerequisite notes are Approved, but their learning
states remain Not started. Reconstruct these two ideas before studying the larger example.

## 2. Real problem and forces

Our synthetic orchard team previews operational guides. A trusted application root establishes a
reader identity. Authorization may change while the preview exists. Opening a catalog can fail and
should be deferred until permitted use. Repeated previews tolerate a short local reuse window.
A tenant and document name together identify a request. Nothing here writes to an external system.

| Design | When it is enough | New pressure or cost |
|---|---|---|
| Direct `catalog.read(key)` | Trusted caller needs current source result | No central place to apply access and reuse policy |
| Explicit dependency passing | Caller must be independent of storage construction | Injection alone does not enforce access policy |
| Small helper/function | One operation and one fixed policy | Passing several pieces of persistent state may become awkward |
| Callable closure | One operation with a little captured configuration | Inspection and administration can become less discoverable |
| Composition-based proxy | Several clients share a narrow mediated capability | More state, delegation and failure decisions |
| Explicit feature API | Caller needs control of freshness, preparation or deadlines | It deliberately exposes a different interface |
| Universal object impersonation | Only if broad transparency is an established requirement | Special methods, identity, typing and lifecycle multiply obligations |

The stable concern is reading a document. The changing concern is permission and cost of reaching
that capability. Do not add a proxy because a direct method call looks insufficiently sophisticated.

## 3. GoF intent and formal mechanics

The GoF authors' publisher-hosted [Related Patterns discussion](https://www.informit.com/articles/article.aspx?p=1398600&seqNum=2)
describes Proxy as a representative for another object with the same interface. This is the
original-author excerpt read here; access to the full Proxy chapter is not claimed. We express
that intent as controlled access through a compatible subject operation. The document domain,
code, diagrams and policy below are original teaching material, not copied book examples.

Design mechanics: the client calls a subject capability; the proxy provides that capability and
holds, creates or locates a real subject. It can defer or suppress delegation according to policy.
GoF role names do not require a superclass named `Subject`, a `ProxyBase`, or a reflection framework.
A narrow Protocol, ordinary classes and injected callables are sufficient here.

## 4. Participants and responsibilities

| Participant | Here | Owns | Must not own |
|---|---|---|---|
| Client | `headline` | Requested key and presentation | Factory, cache administration, authorization implementation |
| Subject | `Catalog` | `read(Key) -> Document` shape | A claim that every implementation has identical freshness |
| Proxy | `CatalogProxy` | Fixed principal, policy order, one slot, lazy target, close state | Authentication or process isolation |
| Real subject | `MemoryCatalog` | Current copied mapping, reads and closed state | Reader permission or cache policy |
| Composition root | Demo `main` | Trusted identity, factory, policy, closing proxy | Hidden global configuration |
| Collaborators | Authorizer, clock, observer | One explicit operation each | Reentering the proxy or smuggling new capabilities |

`OwnedCatalog` adds close for the owner/factory boundary. Clients accept `Catalog`, so they need
only read. These Protocols exist because the consumer and owner need different capabilities.
Type annotations discourage accidental misuse; they cannot keep hostile code from accessing
administration methods. Dependencies point to [catalog_contract.py](examples/catalog_contract.py);
the root wires concrete implementations.

## 5. Collaboration and execution flow

```text
new proxy: no target, no cache
read:
  reject closed or reentrant use
  authorize(principal, key)       failure → no clock/factory/read
  record local monotonic time
  matching fresh slot?            yes → return same stored Document
  discard previous slot
  no target?                     factory success → retain target
                                 factory failure → remain unconstructed
  target.read(key)                failure → retain target, leave slot empty
  result.key == key?              no → ContractError, leave slot empty
  store successful snapshot with this request's start time
  return snapshot
finally: observe one outcome; restore idle state
close:
  mark terminal, drop slot and direct target reference, then close former target
```

### How to read this visual

Follow one read from top to bottom; right-hand branches stop normal progress. The final observation
runs after a read has entered the busy state, including failures. Closed/reentrant rejection occurs
before that state and emits no event.

### Key insight

Failed construction and failed reading are different states. The first leaves nothing to reuse;
the second leaves a constructed catalog that a later explicit call can try again.

### Simplification or limitation

Conceptual trace of synchronous code. There is no retry loop, network, lock, durable audit, or
transaction joining permission and data. The busy flag detects sequential callback recursion;
it does not synchronize threads.

## 6. Before-pattern code and concrete pain

Every Python fence in this note is independently runnable with `examples` on `PYTHONPATH`.

```python
from catalog_contract import Document, Key, headline
from catalog_proxy import MemoryCatalog

key = Key("orchard", "guide")
base = MemoryCatalog({key: Document(key, 1, ("ready",))})
try:
    assert headline(base, key) == "ready"
finally:
    base.close()
```

This already uses explicit dependency passing. A fake can replace the catalog; no Proxy is needed
for that benefit. Now add “denied previews must perform no catalog work” and “permission can be
revoked between two previews.” Constructing before checking permission wastes work and moves
construction failure ahead of denial. Checking only once at construction leaves future accesses
using an old decision. Returning a cached value before checking permission has the same defect.

For one route, a helper that checks and calls may be clearer than an object. Multiple consumers
needing a persistent access policy and controlled lifetime justify the representative below.

## 7. Minimal Pythonic implementation and simpler alternative

The notebook closure is a protection proxy for a single callable. No `@` syntax is required.
A fixed-policy helper is even smaller when the caller already owns the dependency:

```python
from collections.abc import Callable
from catalog_contract import Catalog, Document, Key
from catalog_proxy import MemoryCatalog


def checked_read(catalog: Catalog, key: Key, check: Callable[[Key], None]) -> Document:
    check(key)
    return catalog.read(key)


key = Key("orchard", "guide")
base = MemoryCatalog({key: Document(key, 1, ())})
try:
    assert checked_read(base, key, lambda requested: None).key == key
finally:
    base.close()
```

This helper borrows `catalog`; its caller closes it. It does not defer construction or store a cache.
If caller needs “fresh now” versus “cached if available,” expose methods or a documented freshness
parameter instead of pretending these meanings are equivalent. An explicit `prepare()` can make
startup cost visible. These are valid API choices, even when they no longer preserve the original
subject shape. Avoid an automatic proxy registry for three ordinary constructor arguments.

## 8. Typed implementation and precise contract

Read [catalog_proxy.py](examples/catalog_proxy.py) alongside [the contract](examples/catalog_contract.py).
The class combines three access decisions deliberately in one fixed order. It is a bounded worked
example, not a toolkit covering every proxy variant.

```python
from catalog_contract import Catalog, Document, Key, headline
from catalog_proxy import CatalogProxy, MemoryCatalog

key = Key("orchard", "guide")


def authorize(principal: str, requested: Key) -> None:
    if (principal, requested) != ("reader", key):
        raise PermissionError("denied")


owner = CatalogProxy(
    "reader",
    lambda: MemoryCatalog({key: Document(key, 1, ("ready",))}),
    authorize,
    ttl=10,
    clock=lambda: 0.0,
)
client: Catalog = owner
try:
    assert headline(client, key) == "ready"
    assert client.read(key) is client.read(key)
finally:
    owner.close()
```

The fixed clock makes this snippet deterministic; real code defaults to `time.monotonic`.
Only the root should choose the principal. The authorizer returns `None` to allow or raises to
prevent access. A predicate returning `False` is a different API: the proxy ignores return values.
Static negative tests reject a Boolean predicate, but untyped callers still require review.

| Contract dimension | Worked proxy promise | Visible difference from direct storage |
|---|---|---|
| Input and output | Trusted `Key`; returned `Document.key` must match | Wrong-key result is rejected with `ContractError` |
| Authorization | Every open read checks fixed principal plus full key before cache/factory | Can deny a read that direct storage permits |
| Snapshot meaning | Current source snapshot on miss; same stored object on hit | May return an older revision |
| Cache scope | One proxy, one fixed principal, at most one `(tenant, document)` slot | No cross-proxy sharing or global invalidation |
| Cache time | Reuse only while elapsed time since pre-load start is less than positive finite TTL | TTL bounds reuse eligibility, not source freshness or request duration |
| Exceptions | Policy, construction and read errors propagate; no negative cache | Failure may occur at first use instead of wiring |
| Effects | Denial does no target work; hit does no target read; observer runs afterward | Method call count differs from backend read count |
| Lifecycle | Factory transfers exclusive target ownership; close is terminal | Client must not outlive its owner |
| Concurrency | Single caller, sequential, no reentry | Not safe to share across threads or tasks without redesign |

Shared behavioral tests cover authorized stable snapshots, missing keys and closed use. They do
not assert “freshest revision on every call,” because caching would violate that contract. If a
consumer already requires current storage on every call, substituting this proxy is incorrect even
though a type checker accepts it. Explicitly negotiate weaker freshness or choose another API.

## 9. Laziness, failure and lifetime

Wiring performs no factory call, authorization, clock read, catalog read or telemetry. Closing an
unused proxy does not construct a target merely to close it. The factory is tried once per relevant
read until it successfully returns; there is no automatic within-call retry. A successful target is
retained even if its read raises. Invalidation clears only the value slot, not the target.

The factory must return a fresh, exclusively owned target. Returning a shared connection pool handle
without agreed ownership violates that precondition. If construction partly acquires resources and
then fails, the factory must clean them up: no target was transferred to the proxy. If a real target
becomes unusable after failure, retaining it may be wrong; choose a documented reopen policy or
create a new owner. Do not silently make every exception mean “reconnect.”

`close()` marks the proxy terminal before delegating close. A close failure propagates and repeated
close does not retry it; resource release is then uncertain and requires owner handling. This is a
policy, not a guarantee every resource API needs. The synthetic target models closure, not OS handle
cleanup. Captured references inside injected callables can keep other objects alive after close.

Use explicit `try/finally` ownership as the demo does. Immediate finalization is not a portable
resource policy; Python's [object lifetime guidance](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types)
recommends explicit closure. If close itself can fail while another exception is active, a plain
`finally` can make cleanup failure the active exception; a real owner must choose preservation,
chaining or aggregation deliberately. The demo target's close does not fail.

## 10. Authorization and bypass boundaries

[OWASP's authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#validate-the-permissions-on-every-request)
requires consistent permission checks on each request and recommends default denial. Our ordering
applies that principle to local cache hits. Policy failures propagate without consulting the cache.
A successful old check is never reused as permission for a new read.

This is cooperative application structure. It does not authenticate the reader or protect against
arbitrary Python code in the same process. A caller holding the real object, a saved bound method,
credentials, or a direct storage endpoint can bypass it. Private attribute spelling is not an
isolation boundary. Production enforcement must cover every path at the trusted service/data
boundary. The integration question is “can a request reach data without the authorized entry point?”

A checked permission can change during a slow read. Already returned data cannot be recalled from
a caller. Strong revocation or transactional permission/data consistency needs another mechanism;
this proxy offers neither. Permission denial retains its old value slot, but that value cannot be
returned through this proxy until a later authorization succeeds. This retention policy is unsuitable
if revocation also requires immediate in-memory erasure. Even clearing the slot cannot erase copies
already held by consumers. These are design limits, not tested security certification.

## 11. Cache identity, freshness and returned state

Cache identity includes tenant and document. A principal is fixed per proxy instance, so there is
no mutable current-user switch or shared principal cache. The example assumes all permitted readers
of a key receive the same document representation. If data is redacted by principal, locale, schema,
revision request, or permission version, those inputs affect identity and must be modeled explicitly.
Do not share a cache across users merely because a short document ID matches.

A hit does not extend the timer. At exact TTL equality the entry expires. A miss clears the former
slot before construction or read; an error leaves it empty. Missing documents and denied decisions
are not cached as successful values. Alternating keys repeatedly misses: the one-slot bound trades
hit rate for very simple memory policy. Invalidation is explicit owner administration and affects
only this proxy; writers and other processes are not notified automatically.

TTL starts before construction/read so a slow load does not gain a new full window afterward.
The first response can still arrive after that window, and the backend can itself return an old
snapshot. “TTL ten seconds” therefore does not mean “data is at most ten seconds old.” The source's
own consistency and request deadlines are separate contracts. [Monotonic time](https://docs.python.org/3.14/library/time.html#time.monotonic)
measures elapsed time without wall-clock corrections; its origin is unspecified. Injected clocks
must be finite, nondecreasing and in the same seconds scale. Tests use a controllable clock, not sleeps.

The slot returns the same `Document` object. Ordinary mutation is discouraged with a frozen
dataclass containing a frozen key, integers, strings and a tuple of strings. `frozen=True` alone
would not make nested lists immutable; it emulates immutability through generated assignment
methods. See [frozen instances](https://docs.python.org/3.14/library/dataclasses.html#frozen-instances).
This is a trusted typed value model, not adversarial runtime validation. If results are mutable,
choose copying, immutable conversion or explicitly shared ownership; test consumer mutation effects.

## 12. Python mechanics, typing and transparency

The [typing specification](https://typing.python.org/en/latest/spec/protocol.html#assignability-relationships-with-other-types)
accepts a concrete class structurally when its members have compatible types. Neither implementation
inherits `Catalog`. `OwnedCatalog` requires close at the factory boundary, while read-only consumers
stay small. The negative tests reject a bytes result, a non-ownable factory target and a Boolean
policy. They cannot prove current permission, correct tenant semantics or the freshness promise.

Ordinary delegation binds methods to the actual receiver. A real subject's `self.other()` continues
on that subject; it does not automatically revisit the proxy. A returned target or saved bound
method can escape mediation. Also, implicit special methods generally use type-level lookup:
forwarding attributes with `__getattr__` does not supply `len(proxy)`. Identity remains distinct.
These are [language-level object mechanics](https://docs.python.org/3.14/reference/datamodel.html#special-method-lookup),
not a CPython memory explanation. Add explicit forwarding only for capabilities clients require.

```python
class AttributeForwarder:
    def __init__(self, target: object) -> None:
        self.target = target

    def __getattr__(self, name: str) -> object:
        return getattr(self.target, name)


forwarded = AttributeForwarder([1, 2])
assert getattr(forwarded, "__len__")() == 2
try:
    len(forwarded)
except TypeError:
    pass
else:
    raise AssertionError("ordinary attribute forwarding did not define a length operation")
```

The snippet is an intentional misuse demonstration, not part of the statically accepted library.
An `Any`-returning universal forwarder can conceal missing contracts from the checker; a `cast`
changes a static view and does not install runtime behavior. Equality, hashing, iteration, context
management, serialization and returned-self semantics would each need deliberate decisions.
This example exposes only read and owner administration instead of claiming whole-object transparency.

Version boundary: `@runtime_checkable` checks attribute presence, not signatures or semantics.
Starting with Python 3.12 it uses `inspect.getattr_static` instead of `hasattr`, and the protocol's
runtime member set is frozen. A dynamically forwarded member can therefore be recognized in 3.11
and fail recognition in 3.14. [Official typing documentation](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable)
records this change. Our version-aware test demonstrates it on both interpreters. The working
catalog uses static Protocol checking and explicit methods; it does not use runtime Protocol gates.
All source syntax remains Python 3.11 compatible. No framework or CPython-specific dispatch is needed.

## 13. Backend transfer and remoting limits

A service might supply a tenant-scoped catalog proxy to a preview handler and keep storage
credentials inside a trusted composition root. That analogy does not make this in-memory example a
production security component. Test actual routing, identity establishment, credential exposure and
storage access separately when integrating a real service.

A remote proxy represents a distant capability. In professional design judgment, making the call
look like a local method must not hide serialization, deadlines, authentication, latency, partial
failure or uncertain completion. An explicit remote client API is often more honest. If a write
request times out, the remote side might already have applied it; a wrapper cannot manufacture
exactly-once execution. Define idempotency and retry semantics at the operation boundary. No network
transport, retry policy or distributed guarantee is implemented or experimentally verified here.

## 14. Failure scenarios and observability

| Symptom | First reasoning check | Detection and containment |
|---|---|---|
| Revoked reader still sees content | Does cache lookup bypass policy? | Test warm-cache revocation; move enforcement ahead of every return path |
| Wrong tenant content | Is the full identity represented? | Test same document name in two tenants; reject wrong-key responses |
| Never sees an update | Is there expiry/invalidation, and which source is authoritative? | Fake-clock boundary tests; inspect policy, not just hit ratio |
| First preview fails after successful startup | Construction was deferred | Distinguish factory failures from read failures; decide startup readiness needs |
| Too many backend reads | Alternating keys, expiry or failed loads? | Separate hit/miss/error outcomes from request counts |
| Proxy remains unusable after error | Target state or terminal close policy? | Inspect lifecycle; don't reopen implicitly without a contract |

The worked observer receives only outcome: hit, miss, denied or error. It deliberately excludes
principal, key and document content. One attempted event follows each entered read. Ordinary observer
exceptions increment `observer_failures` and are suppressed, preserving the pending read result or
exception. An observer may record an event and then fail; the counter does not prove the event was
lost. A `BaseException` can interrupt delivery of an already cached result or replace a pending error.
The busy flag is restored in a nested `finally` even then. This is best-effort telemetry, not durable
security audit. If audit is mandatory before disclosure, observer failure must become an explicit
access-policy outcome and needs a different design.

## 15. Concurrency, async and cancellation

The example promises sequential access with non-reentrant collaborators. A Boolean busy flag is no
lock: concurrent check/set, construction, invalidation, read and close can race. Even Python's
[standard memoization](https://docs.python.org/3.14/library/functools.html#functools.lru_cache) can invoke
a wrapped function more than once during overlapping misses despite coherent cache bookkeeping.
Do not infer single construction from “thread-safe cache.”

Before sharing this design, specify whether callers wait for one load, whether failures are shared,
who can close while reads run, and how invalidation interacts with an in-flight result. A lock around
arbitrary policy/factory/observer calls can cause blocking or reentry trouble. This unit does not
add untested locks or claim that the GIL solves compound operations.

An async version needs an async contract and `await`, not a synchronous proxy around a coroutine
object. Decide who owns shared in-flight work and whether cancellation of one waiter cancels it for
others. Use cleanup paths and generally propagate cancellation: [asyncio task guidance](https://docs.python.org/3.14/library/asyncio-task.html#task-cancellation)
notes `CancelledError` derives directly from `BaseException`. The included implementation and tests
are synchronous; they do not establish async cancellation, scheduling or remote deadline behavior.

## 16. Performance and memory

No benchmark was run. The controlled probe measures call counts, not speed. A hit still performs
permission checking, clock reading, branching and observation. Deferred construction helps only
when some owners never read or when startup cost may move to use time. A cheap in-memory read might
be faster and simpler directly.

The proxy retains one document entry plus its constructed target and injected collaborators.
“One entry” does not bound payload bytes or the target's own storage. Cached snapshots and captured
factory references can extend lifetimes. Expiry is checked on access rather than by a timer; an
expired document remains referenced until a miss, invalidation or close. A larger cache would need
an explicit capacity, eviction, invalidation and observability policy. Add it only with workload evidence.

## 17. Refactoring path

1. Test the direct read's important meaning, failures and ownership before wrapping it.
2. State the new force: permission on every read, optional construction, or measured repeated cost.
3. Extract the client-sized capability and pass it explicitly.
4. Move one access decision to a helper or representative and test bypass paths.
5. For caching, negotiate freshness, full identity, return sharing and invalidation before changing calls.
6. Keep the root responsible for identity and lifetime; exercise construction/read/close failures.
7. Re-run behavioral and typing checks; remove forwarding or variants that no client needs.

## 18. Variants and related-unit boundaries

| Variant | Access decision | Semantic difference to disclose |
|---|---|---|
| Virtual/lazy proxy | Construct only on need | First-use latency and failure; ownership after partial construction |
| Protection proxy | Check permission before delegation | Denial and bypass boundaries; revocation timing |
| Caching proxy | Reuse a prior result | Identity, freshness, invalidation and shared state |
| Remote proxy | Reach a distant capability | Transport costs, serialization and uncertain completion |
| Observation proxy | Record accesses to the subject | Audit/telemetry failure, content exposure and whether hits count |

The worked class covers a deliberate subset of the first three and a small telemetry hook. These
are access concerns, not a recommendation to combine every variant into one universal class.

| Related unit | Relationship | Distinguishing question |
|---|---|---|
| [SDP-STR-010](../../../CURRICULUM.md#sdp-str-010) — Adapter | Similar forwarding structure | Are we translating an incompatible interface? |
| [SDP-STR-020](../../../CURRICULUM.md#sdp-str-020) — Facade | Convenient boundary | Are we simplifying a subsystem into a different task interface? |
| [SDP-STR-030](../../../CURRICULUM.md#sdp-str-030) — Decorator | Compatible wrapping can look identical | Are we adding responsibilities or mediating access to a subject? |
| [SDP-SOL-030](../../../CURRICULUM.md#sdp-sol-030) | Contract reasoning | Can this consumer tolerate denial, older data and different failures? |
| [SDP-INT-030](../../../CURRICULUM.md#sdp-int-030) | Later scenario comparison | Which change pressure best explains the design? |

These are bounded comparisons, not authored content for other units. Intent and contract matter
more than the wrapper's class name; an observation wrapper can serve more than one design intent.

## 19. When to use, reject and critique

Use a proxy when multiple clients need a stable capability with a justified access policy and the
observable differences are acceptable. Use a helper for one small rule and explicit dependency
passing when replaceable construction is the only need. Prefer an explicit freshness or remote API
when callers must make decisions that a local-looking operation would conceal.

| Misuse | Why it fails | Better decision |
|---|---|---|
| Cache outside authorization | A hit returns without a current check | Make policy order explicit and test revocation |
| Boolean authorizer wired into raise-to-deny API | False is ignored as a normal return | Use the correct callable contract; reject mismatches statically |
| Return shared mutable response | One consumer can poison later results | Immutable values, copies or declared shared mutation |
| Proxy owns a borrowed target | Close breaks another consumer | Transfer ownership explicitly or keep closure in the root |
| Universal `__getattr__` proxy | Ordinary forwarding misses operations and hides types | Expose narrow explicit capabilities |
| Retry every failure | Work may have happened; unusable state may persist | Classify failures and operation semantics first |
| Treat every method as remote-safe | Call syntax hides costly or uncertain effects | Expose deadlines, errors and completion semantics |

## 20. Testing and controlled evidence

| Check | What it proves here | What it does not prove |
|---|---|---|
| Shared read contract | Authorized stable values, missing keys and closed behavior | Equal freshness for every implementation |
| Policy tests | Denial before construction/read; warm hits recheck permission | Full service security or authentication |
| Fake-clock tests | Exact expiry, invalidation, non-sliding window and slow-load behavior | Real latency, wall-clock synchronization or source freshness |
| Failure and ownership tests | Later-call retry, retained target, terminal close, observer boundaries | Real connection recovery or handle cleanup |
| Static positive/negative controls | Intended member/result/callback shapes accepted or rejected | Runtime permissions or semantic correctness |
| Version probe | Dynamic forwarding runtime Protocol distinction on tested interpreters | General compatibility of all proxy libraries |
| Independent lab baseline | Original flawed behavior runs; exercise remains unsolved | Learner implementation or understanding |

See [actual results](VALIDATION.md). Do not merge all repository test directories into one pytest
invocation: existing teaching modules reuse names. Run isolated directories for regression.

## 21. Unsolved practice and evidence plan

The [export-preview lab](practice/README.md) uses versioned binary exports with locale and permission
changes. It asks the learner to choose an API and defend reuse identity; the worked catalog is not
its solution. Preserve the original attempt before hints. Give only one progressive hint at a time.

- **E:** Reconstruct the permission/cache/lazy flow and identify one promised semantic difference.
- **I:** Implement and test the chosen export API, including boundary cases Rahul identifies.
- **D:** Diagnose the supplied work-before-denial behavior and a separate stale/shared-result mistake.
- **T:** Defend or reject reuse for a changed backend requirement with an alternative and failure policy.

These are tasks to complete, not evidence already earned. No learner state, date or weakness changes
until Rahul supplies the required reasoning and artifacts.

## 22. Interview preparation

Use this bank one question at a time; wait for the answer before giving feedback or a follow-up.
The gap column guides the reviewer, not a memorized answer script.

| Prompt | Weak-answer trap | Exact missing reasoning step to inspect |
|---|---|---|
| Explain Proxy to a teammate using a real pressure | “A wrapper class” | Connect the representative to a specific access decision |
| Where does the real subject sit on a cache hit? | “Every call forwards” | Trace the branch that suppresses delegation |
| Can a revoked reader get a warm cached value? | “It was authorized when cached” | Separate current permission from content freshness |
| Both implementations satisfy Catalog; can I substitute them? | “Mypy passed” | Compare this consumer's freshness, error and lifetime requirements |
| First construction fails; what happens next? | “It retries” | Distinguish same-call retry, later-call retry and retained partial state |
| Do frozen results make any cache safe? | “Frozen means fully immutable” | Inspect nested members and caller ownership |
| Is this a Decorator, Adapter or Proxy? | Class-name guessing | Identify the change force and preserved/changed interface |
| What can bypass your policy? | “Private fields are secure” | Trace all real-object and credential access paths |
| Add concurrency to the design | “Use a lock” | Define shared in-flight work, invalidation and close ordering first |
| Remote read times out after a write | “Retry automatically” | Separate transport failure from known operation completion |
| Only one handler needs this rule | Unnecessary framework | Compare a helper and explicit dependency passing concretely |
| Review a False-returning authorizer | “False denies” | Read the actual callback contract and control flow |

For a small design exercise, ask for a verbal API for a preview requiring fresh data on demand.
For code review, show a cache return before permission checking and ask for the first violated
invariant. For transfer, change the rule to principal-specific redaction and ask which identities
and enforcement boundaries must change. Stop after one question in an interactive session.

## 23. Closed-book revision cues

1. Draw the three possible access paths and the owner arrow.
2. Explain why injection alone does not provide access control.
3. State construction-failure, read-failure and close-failure policies separately.
4. Reconstruct the complete cache identity and exact expiry condition.
5. Give a behaviorally invalid substitution with a perfectly valid signature.
6. Reject a universal forwarder and offer the smallest suitable Python alternative.

## 24. Vocabulary and professional English

### Surrogate

| Item | Content |
|---|---|
| Pronunciation | SUR-uh-gut |
| Simple English meaning | A representative acting in place of something else |
| Hindi cue | प्रतिनिधि |
| Meaning here | Client-facing object representing a real capability |

Natural examples: “Use a surrogate during the rehearsal.” “The sensor is a surrogate for direct
measurement.” “This score is only a surrogate for quality.” **Interview:** “The proxy is a surrogate
that controls access.” **Engineering:** “Which calls can bypass the surrogate?”

### Invalidation

| Item | Content |
|---|---|
| Pronunciation | in-val-ih-DAY-shun |
| Simple English meaning | Making something no longer eligible for use |
| Hindi cue | अमान्य करना |
| Meaning here | Removing a cached value's eligibility for reuse |

Natural examples: “The correction caused invalidation of the result.” “The rule defines certificate
invalidation.” “Invalidation does not undo past use.” **Interview:** “Expiry and explicit invalidation
are distinct policies.” **Engineering:** “Which owners receive an invalidation after this update?”

### Transparency

| Item | Content |
|---|---|
| Pronunciation | trans-PAIR-un-see |
| Simple English meaning | How little a substitution changes what a user observes |
| Hindi cue | बदलाव कितना दिखाई देता है |
| Meaning here | Compatibility of an agreed set of observations, not identical objects |

Natural examples: “Explain the limits of transparency.” “Operational transparency needs useful
information.” “The report improves transparency.” **Interview:** “Signature transparency does not
imply freshness equivalence.” **Engineering:** “Let us list what this transparent API actually hides.”

## 25. Python Mastery references

There is no direct SDP-STR-040 row in PYTHON_REFERENCES.md. These exact mappings come through its hard
prerequisites; no cross-repository study or completion is claimed:

- [PY-OBJ-010 — Classes, instances, methods, and construction](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-010): instance state, bound methods and construction.
- [PY-OBJ-020 — Properties, encapsulation, and composition](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-020): storing and delegating to a collaborator.
- [PY-OBJ-030 — Inheritance, MRO, and super](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-030): distinguish inheritance from this composition design; no MRO deep dive needed.
- [PY-TYP-050 — Protocols, ABCs, and structural versus nominal typing](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-typ-050): separate duck typing, structural checking and nominal categories.

## 26. Authoritative sources and claim boundaries

Sources opened and read for this unit:

1. [GoF authors, publisher excerpt, Related Patterns](https://www.informit.com/articles/article.aspx?p=1398600&seqNum=2): representative and unchanged interface; not claimed access to the complete Proxy chapter.
2. [Python 3.14 Data Model](https://docs.python.org/3.14/reference/datamodel.html): objects, instance methods, lifetime and special-method lookup; language guarantees distinguished from CPython notes.
3. [Typing specification, Protocol assignability](https://typing.python.org/en/latest/spec/protocol.html#assignability-relationships-with-other-types): structural static compatibility.
4. [Python 3.14 typing, runtime_checkable](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable): limited presence checks and the Python 3.12 lookup change.
5. [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): default denial and permission checks on every request.
6. [Python time.monotonic](https://docs.python.org/3.14/library/time.html#time.monotonic): elapsed-time clock semantics.
7. [Python dataclasses, frozen instances](https://docs.python.org/3.14/library/dataclasses.html#frozen-instances): emulated immutability.
8. [Python functools.lru_cache](https://docs.python.org/3.14/library/functools.html#functools.lru_cache): coherent cache bookkeeping does not promise only one concurrent computation.
9. [Python asyncio task cancellation](https://docs.python.org/3.14/library/asyncio-task.html#task-cancellation): cleanup and cancellation propagation; not an async implementation claim.

Cache scope, ordering, error retention, terminal close and telemetry policy are explicit design
choices in this example. Cross-process security, remoting and concurrency guidance is professional
transfer judgment, not a measured property of this code. No benchmark, framework behavior or
CPython internal algorithm is asserted. No source conflict is left unresolved within this scope.

## 27. NotebookLM and maintenance boundary

After artifact approval, this README may be used as the unit's note under
[NotebookLM policy](../../../docs/NOTEBOOKLM.md). Do not upload the tracker, raw attempts, starter
solutions, generated logs or private inputs. No upload is performed here. Source links and original
explanations do not grant a license to copied material; no license has been added.
