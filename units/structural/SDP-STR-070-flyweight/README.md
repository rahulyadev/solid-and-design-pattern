# SDP-STR-070 — Flyweight

## Physical Notebook Core

### Problem or change pressure

An inspection grid has thousands of placed tiles but only a few repeated grayscale designs.
Each placement needs its own ID and coordinates. Rebuilding the same pixels for every placement
may waste space; putting a placement's coordinates into shared data would corrupt other placements.

### One-sentence mental model

> Keep one stable value for many uses, and supply each use's changing context separately.

### One essential visual

```text
placement 10: (100, 200) ──┐
                         ├── Tile(key=(7, 4), immutable pixels)
placement 11: (-10, 20) ──┘                  ↑
                                  TilePool[key] owns a reference
sample(dx, dy): placement supplies context; Tile reads its pixels
```

### How to read this visual

The two arrows converge on one tile. Placement identity and world position stay on the left.
The pool also holds the tile; deleting a placement does not necessarily end the tile's lifetime.

### Key insight

Sharing removes repeated intrinsic data, not the need to represent distinct logical occurrences.

### Simplification or limitation

This is a conceptual reference graph, not CPython memory layout or a browser-rendered image.
It omits dictionaries, allocation overhead and temporary values. It proves no memory saving.

### Governing rules or invariants

1. Shared state must be independent of an occurrence's context and safe for every borrower.
2. A key must include every input that changes the shared value's meaning within its scope.
3. Values remain usable after eviction; callers must not confuse value equality with pool identity.

### Minimal Python example

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Style:
    shade: int


common = Style(80)
placements = [(10, 3, common), (11, 9, common)]
assert placements[0][2] is placements[1][2]
assert placements[0][0] != placements[1][0]
```

Explicit sharing may be enough. The list triples represent ID, position and shared style; there
is no factory because this small composition already owns the one shared value.

### One common misconception

**Mistake:** Equal values must be the same object, and the same object proves lower memory use.

**Correction:** Sharing is a representation choice. Count reachable allocations and retention for
an equivalent workload before making a memory claim.

### Important trade-offs

- Fewer repeated values can cost extra keys, references, lookups and retained unused data.
- Immutable shared values simplify callers; mutable shared values multiply a mistaken edit's reach.

### Interview-revision cues

- Separate one intrinsic field from one extrinsic field and explain why.
- State the key and the exact lifetime of the identity promise.
- Reject a pool when a direct shared constant or ordinary value is clearer.

## Unit metadata

| Field | Value |
|---|---|
| Domain | Structural patterns |
| Curriculum | [SDP-STR-070](../../../CURRICULUM.md#sdp-str-070) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Share stable intrinsic state across many logical objects while making identity, mutability, caching, and memory trade-offs explicit. |
| Hard prerequisites | [SDP-FND-090](../../../CURRICULUM.md#sdp-fnd-090), [SDP-PYT-060](../../../CURRICULUM.md#sdp-pyt-060) |
| Soft prerequisites | None declared in the canonical entry |
| Priority | Advanced |
| Interview frequency | Low |
| Production frequency | Low |
| Python/backend relevance | Low |
| Depth | D3 |
| Scope | GoF, Structural, Runtime |
| Size | L |
| First understanding | 4–6 h |
| Hands-on practice | 5–9 h |
| Evidence profile | E+I+D+X+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Draft |

Frequency labels are curriculum judgments, not measured usage statistics. Generated notes and
maintainer checks do not prove learning. The tracker remains Not started.

## 1. Simple explanation and prerequisite bridge

Imagine printing the same tile design at several positions on a map. Its pixels do not need to
know where the map puts it. Store the pixels once; keep each position separately. A placement
asks the tile for a shade at a local offset and adds its own world coordinates to the result.
The shared tile never remembers the last placement that used it.

[SDP-FND-090](../../../CURRICULUM.md#sdp-fnd-090) supplies aliases and ownership: two names can
reach one object; editing that object is visible through both names. A container can keep its
contents alive. [SDP-PYT-060](../../../CURRICULUM.md#sdp-pyt-060) supplies value modeling: equality
can describe content; a frozen field binding does not recursively freeze objects inside it.
Both prerequisite artifacts are Approved, but their learning rows are Not started. This bridge
lets you begin without pretending that the prerequisites have been demonstrated.

The distinction between `is` and value equality is a language-level distinction. Built-in immutable
values may already be reused by an implementation; do not infer a portable interning policy from
one literal experiment. See [Objects, values and types](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types).

## 2. Ordinary data first, then a concrete pressure

For a small grid, constructing each value independently is straightforward:

```python
from flyweight import PlacedTile, Tile, TileKey

rows = [PlacedTile(i, i * 4, 0, Tile(TileKey(7, 4))) for i in range(3)]
assert [row.sample(1, 2).shade for row in rows] == [86, 86, 86]
assert len({id(row.tile) for row in rows}) == 3
```

Run note snippets with the examples directory on `PYTHONPATH`. Keeping all rows alive makes the
identity count meaningful; counting IDs of discarded temporaries could count reused IDs instead.

Now load thousands of placements from a feed that repeatedly describes the same designs. We want
the same samples, IDs and positions while avoiding repeated pixel construction. Do not start by
assuming the feed is repetitive: record total placements N, distinct valid keys K, payload sizes,
and lifetime first. With K close to N, a dictionary can retain one extra entry for every tile and
provide almost no reuse. With just two fixed designs, construct two tile values explicitly.

| Design | Change pressure it handles | Cost or failure to check |
|---|---|---|
| Independent values | Small grid, independent construction | Duplicate payload allocations |
| Explicit shared values | Known small set selected by composition | Caller must reuse the supplied values |
| Scoped Flyweight pool | Repeated specifications arrive dynamically | Key completeness, capacity, ownership |
| Pythonic immutable values | Stable content safe across borrowers | Frozen bindings alone are insufficient |
| Needless global cache | No demonstrated pressure | Hidden lifetime and cross-job coupling |

## 3. Verified intent and formal mechanics

Gamma, Helm, Johnson and Vlissides discuss Flyweight in their ECOOP 1993 paper's object-structural
section: large object populations motivate sharing, and context-dependent information is supplied
when needed. That is the verified historical basis here; this note's frozen values and bounded
pool are an original Python interpretation. See [the authors' paper, §3.2](https://doczz.net/doc/6456109/erich-gamma---richard-helm---ralph-johnson---john-vlissides).

Flyweight supports many fine-grained logical objects by sharing context-independent state. Intrinsic
state belongs to that shared representation; extrinsic state describes a particular use. The split
is relative to the operation and sharing scope, not an intrinsic property of a field name. A color
might be intrinsic to a tile design and extrinsic to a selection highlight.

The GoF catalog roles include a Flyweight operation receiving extrinsic context, a shareable concrete
value, a managing factory and clients holding context. It also permits unshared implementations;
an operation interface alone does not guarantee sharing. The catalog's [indexed participants and
collaboration excerpt](https://vik.wiki/images/4/45/Sznikak_jegyzet_E.Gamma_R.Helm_R.Johnson_J.Vlissides_DesignPatterns.pdf)
was readable in search; the full PDF could not be opened. No claim of reading the complete book
or reproducing its diagrams is made.

### Participants mapped to this example

| Role | Python participant and responsibility | Must not own |
|---|---|---|
| Intrinsic specification | `TileKey(seed, side)` identifies a design | Placement ID or world position |
| Concrete flyweight | `Tile` owns derived `bytes`; `pixel(dx, dy)` reads it | Last caller, cursor or mutable scratch buffer |
| Factory | `TilePool.get(key)` reuses or constructs a tile | A global list of placements |
| Client/context | `PlacedTile` holds tile, ID and position; passes offsets | Authority to edit shared pixel data |
| Result | `Pixel` carries one observation | The pool or a resource lease |

There is one concrete operation family, so no interface hierarchy or Protocol is needed. Direct
construction remains valid for ordinary value clients; clients requiring canonical sharing use the
pool. This deliberate public constructor allows us to compare representations fairly.

### Collaboration and execution flow

```text
get(TileKey(7, 4)) -> miss -> construct bytes completely -> publish Tile -> return
get(TileKey(7, 4)) -> hit  -------------------------------------------> same Tile
PlacedTile.sample(1, 2) -> Tile.pixel(1, 2) -> shade 86
                      -> Pixel(placement_id, x + 1, y + 2, 86)
clear() -> remove pool references -> old placements still sample successfully
```

### How to read this visual

Each line is a separate operation in one thread. A miss publishes only a completed value. A sample
combines the tile's intrinsic shade with the placement's extrinsic identity and coordinates.

### Key insight

The flyweight does not need to be updated before a new client uses it. Context crosses the method
boundary as arguments rather than becoming shared object state.

### Simplification or limitation

This is a conceptual sequential trace. It omits allocator failures and dictionary mechanics and
makes no concurrent construction guarantee. Browser rendering was not attempted or claimed.

## 4. Runnable typed implementation and contract

Read [flyweight.py](examples/flyweight.py) beside [the demo](examples/run_flyweight_demo.py).
The module is small enough to reconstruct: specification, immutable tile, placement, result and pool.
Pixel generation is a synthetic deterministic formula, not an image decoder or a real inspection
algorithm. `seed` is 0–65535; `side` is 1–64. A tile owns `side * side` bytes in row-major order.

```python
from flyweight import Pixel, PlacedTile, TileKey, TilePool

pool = TilePool(capacity=2)
a = PlacedTile(10, 100, 200, pool.get(TileKey(7, 4)))
b = PlacedTile(11, -10, 20, pool.get(TileKey(7, 4)))
assert a.tile is b.tile
assert a.sample(1, 2) == Pixel(10, 101, 202, 86)
assert b.sample(1, 2) == Pixel(11, -9, 22, 86)
```

| Boundary | Guarantee for typed callers | Explicit limit |
|---|---|---|
| `TileKey` | Seed and side ranges checked; bool rejected | Not an untrusted-input decoder |
| `Tile` | Payload fully derived from key; caller cannot pass pixels to constructor | Normal construction and ordinary frozen APIs assumed |
| `pixel(dx, dy)` | Both offsets inside tile; returns integer shade 0–255 | Does not clip, wrap, or accept world coordinates |
| `PlacedTile` | ID 0–1,000,000; world origins within ±1,000,000 | Caller owns uniqueness of IDs across its collection |
| `sample` | Preserves ID; translates offsets to world coordinates | Result coordinates may extend beyond the origin bounds |
| `get` | Equal keys return identical tile until clear in this one pool | No identity promise across pools or clear calls |
| Capacity | Hits work at capacity; new keys raise `PoolFull` without insertion | Entry bound, not a process memory quota |
| `clear` | Releases pool references; is repeatable | Does not revoke borrowers or promise immediate deallocation |

All APIs use Python 3.11-compatible syntax. Types such as `TileKey` and integer arguments are a
static caller precondition; range checks do not constitute runtime type admission. For example,
a hostile duck object or a float passed through untyped code is outside this contract. Parse
external input into validated domain values at an application boundary. `Pixel` is an output value;
its public constructor does not validate arbitrary manually supplied results.

`Tile` excludes derived `pixels` from equality because its normal constructor deterministically
computes them from the full key. This saves redundant comparisons; it is sound only while the key
completely defines the payload. Low-level field replacement would violate that invariant.
Different keys can sometimes produce equal pixel arrays; we intentionally canonicalize design
specifications rather than every possible pixel-content equivalence class.

## 5. Identity, equality and substitution

A logical placement's ID answers “which occurrence?” Python object identity answers “which in-memory
object?” Value equality answers “does this representation mean the same value under this class's
contract?” They are different questions. Two placements may use the same tile yet differ in ID and
coordinates. Two equal Tile values from different pools may have different object identities.

```python
from flyweight import PlacedTile, Tile, TileKey, TilePool

key = TileKey(7, 4)
pool = TilePool(1)
old = pool.get(key)
pool.clear()
new = pool.get(key)
assert old == new and old is not new
assert PlacedTile(1, 0, 0, old).sample(1, 2) == PlacedTile(1, 0, 0, Tile(key)).sample(1, 2)
```

Substitution has two levels. A rendering client can substitute any correctly constructed equal Tile
and preserve observed samples. A client promised one canonical object per retained key depends on
the pool contract; replacing that pool with a constructor that always returns a fresh Tile would
violate that stronger promise even though rendering tests pass. Keep `is` assertions in pool tests,
not business decisions. Do not use an object ID as a persisted key or wire identity.

## 6. Key correctness, scope and mutation hazards

The key is a semantic decision. Omitting `side` would reuse a 4-by-4 tile when an 8-by-8 tile was
requested. Adding placement ID would prevent reuse. Adding a value that changes on every request
would silently turn a cache into an append-only retention structure.

No key normalization occurs here. Equal typed seed/side pairs mean the same design. In a real asset
service, tenant, asset revision, color profile and decoding options may change meaning. Either put
them in the key or make them immutable properties of an isolated owner. A global key such as
`asset_name` is insufficient if the same name resolves differently for two tenants. A digest of
payload bytes needs a collision policy and still requires constructing or loading the payload first.

`frozen=True` rejects ordinary field rebinding; it does not freeze a referenced list. Our intrinsic
graph uses integers, a frozen key and bytes, with no borrowed mutable buffer. `slots=True` controls
instance storage; `weakref_slot=True` supports the experiment's lifetime witnesses and is available
in 3.11. `final` is a static restriction, not runtime tamper protection.
See [3.11 dataclasses](https://docs.python.org/3.11/library/dataclasses.html),
[3.14 frozen instances](https://docs.python.org/3.14/library/dataclasses.html#frozen-instances), and
[typing.final](https://docs.python.org/3.14/library/typing.html#typing.final).

If a new requirement adds a selection highlight, put it on the placement or pass it to a rendering
operation. Do not put mutable `selected`, `last_x`, `owner_id` or a scratch list on the shared tile.
To change an intrinsic design, create a new key/value and explicitly replace the intended placements.
Silently mutating the old tile makes every borrower observe the change.

## 7. Errors, ownership, retention and eviction

Validation precedes insertion. A rejected capacity miss leaves existing entries usable. Normal
construction publishes a completed Tile only after its byte generation succeeds; construction
exceptions propagate and no tile is inserted. There is no I/O, retry, cached exception or partial
placeholder in this design. Allocation failure is not translated into a fake success.

The pool has strong references to keys and values. Each placement also owns a reference to its tile.
Dropping placements can leave tiles retained solely by the pool. Clearing the pool cannot free a
tile still referenced by a placement. Language semantics do not promise immediate finalization;
resource cleanup must be explicit when external resources exist.
[Python object lifetime](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types).

| Policy | Useful when | Contract consequence |
|---|---|---|
| Explicit catalog | Designs are known before the job | Predictable scope; no dynamic lookup factory needed |
| Strong bounded pool with reject | Owner can budget a maximum distinct working set | New key may fail; hits remain usable |
| LRU eviction | Recency predicts reuse and misses can reconstruct | Old borrowers may coexist with equal new instances |
| Weak-value pool | Keep canonical values only while another owner needs them | Dead entries disappear; lookup can reconstruct |
| No sharing | Little repetition or sharing violates semantics | Simpler lifetime and no retention index |

A weak reference does not keep its target alive. `WeakValueDictionary` removes entries when values
are collected; obtain one strong reference from a lookup and use that reference. Weak caching
requires weak-reference-capable values and does not make the whole workflow thread safe.
[weakref documentation](https://docs.python.org/3.14/library/weakref.html).

Entry count is only a bound on pool retention: values can have different sizes, placements can grow,
and old borrowers can keep values after clear. Here each payload is at most 4096 bytes, but object,
key and dictionary overhead is additional. Production resource budgets need byte and lifetime
accounting too. A database connection or mutable decoder with a cursor is not this kind of value:
sharing it requires separate lease, synchronization and explicit close rules.

## 8. Concurrency and Python-version boundaries

`TilePool` is single-thread-owned. Its lookup/check/build/insert sequence is one logical action but
several Python operations. Two concurrent misses could construct duplicates, violate the capacity
policy or return different objects for an equal key. A GIL does not establish this API's contract.
Confine the pool to one worker or put an explicit lock around the complete operation, including
clear. If construction moves outside the lock, design publication and duplicate-disposal rules.

`functools.cache` and `lru_cache` keep their internal data coherent across threads, yet may invoke
the function more than once for overlapping misses. They therefore do not supply an unconditional
“construct exactly once” guarantee. They also retain arguments/results until eviction or clearing.
[functools cache contract](https://docs.python.org/3.14/library/functools.html#functools.lru_cache).
A decorator can implement a pool when those semantics and that lifetime are acceptable.

The 3.14 free-threaded build's internal container locks are implementation behavior, not a substitute
for application synchronization. This unit's measured builds are identified in the experiment;
no free-threaded testing is claimed.
[Python free-threading guide, thread safety](https://docs.python.org/3.14/howto/free-threading-python.html#thread-safety).

Dataclass equality implementation changed in 3.13: direct field comparisons replaced tuple-based
comparison, which can matter for values such as NaN. Our key uses ordinary bounded integers and
our supported observations match on 3.11 and 3.14; we make no float or NaN key contract.
[3.14 dataclasses, eq](https://docs.python.org/3.14/library/dataclasses.html#dataclasses.dataclass).
No 3.14-only syntax or reliance on runtime annotation evaluation is needed here.

## 9. Performance and the controlled runtime experiment

Read [EXP-01: sharing and retention](experiments/EXP-01-sharing-retention/README.md). It compares
fresh construction, an explicit shared catalog, and the dynamic pool at N=4000 with K=8 and K=4000.
The semantic workload, placement count and payload size stay constant inside each case. It measures
retained traced allocations after construction and after dropping placements and clearing owners.
Every trial runs in a fresh process; all outputs and limitations are recorded there.

A conceptual cost estimate is: fresh values cost roughly N times intrinsic payload plus placement
cost; shared values cost roughly K times intrinsic payload plus placement references and the sharing
index. This omits allocator and Python object overhead and is not a measured formula. The break-even
point depends on actual representation, repeated keys and retention duration.

`sys.getsizeof` reports the direct size of an object, not its referenced graph. Summing it per
placement can double-count shared children; inspecting only the placement can miss its payload.
[sys.getsizeof](https://docs.python.org/3.14/library/sys.html#sys.getsizeof).
`tracemalloc` reports traced Python allocation blocks, not process RSS or every native allocation.
Its current-size observation is suitable for this controlled byte payload, with the scope and
measurement overhead documented. [tracemalloc](https://docs.python.org/3.14/library/tracemalloc.html).

This is an allocation/retention experiment, not a timing benchmark. It does not prove lower latency,
production capacity, cross-process sharing or operating-system memory reclamation. Before adopting
Flyweight in a service, measure a representative distribution, longer-lived owners and peak behavior.
For compact numeric data, arrays or a table of indices may beat a graph of Python objects entirely.

## 10. Refactoring, backend transfer and operational judgment

1. Preserve samples and occurrence IDs with characterization tests.
2. Measure which intrinsic data actually repeats and who keeps it alive.
3. Extract an immutable value while keeping context on the caller.
4. Try explicit reuse in the composition root before adding a lookup pool.
5. Define a full semantic key, scope and error policy; then introduce the pool if justified.
6. Compare fresh/shared observations and test hits, misses, distinct variants and clear.
7. Measure equivalent workloads and remove the pool if retention outweighs reuse.

A backend generating a synthetic asset manifest could share decoded, versioned tile metadata across
many placement records in one export job. The owner would create one pool per job, reject excess
working-set cardinality according to the export contract, and discard the owner after the export.
That is a professional design inference, not a claim about a deployed system or framework.

If a process-wide cache causes memory growth, inspect distinct-key count, payload bytes, owner ages,
hit/miss rates and surviving borrower references. A high hit rate alone does not prove bounded memory.
If two customers see the wrong asset version, inspect key completeness and scope before adding a
bigger cache. Contain by isolating the faulty owner, repair the key or revision policy, and reproduce
the two-customer case. Clearing alone does not repair already-issued incorrect values.

Use Flyweight when stable repeated data is material, many contexts can safely share it, and evidence
justifies the ownership machinery. Reject it for a small data set, nearly unique keys, identity-bound
entities, mutable per-client sessions or expensive external resources without a sharing contract.

## 11. Tests, debugging and evidence boundaries

| Test | What it proves | What it does not prove |
|---|---|---|
| Pixel values, offsets, translation | Deterministic samples and domain bounds | Real image-format correctness |
| Equal keys, changed seed/side | Canonical reuse and complete current key | Completeness for future fields |
| Capacity failure and clear | Pool errors preserve valid old values | Thread safety or byte-budget enforcement |
| Frozen mutation checks | Ordinary API rejects intrinsic edits | Hostile reflection resistance |
| Weak-reference witnesses | Observed owners retain/release values after explicit collection | Universal finalization time |
| Generated bounded comparisons | Fresh/shared sample equivalence on tested inputs | A proof over every Python object |
| Positive/negative static clients | Accepted API and nine intended type failures | Semantic correctness of unchecked code |
| Probe workload tests | Same placements, results and intended live-object counts | Portable byte totals or speed |

The [typing checks](examples/test_typing_contracts.py) reject frozen edits, injected payloads,
wrong key/placement/offset types, wrong result expectations, writing size, and subclassing a final
value. They verify exact diagnostic locations and categories for both target versions; invalid
clients are never executed. The tests exercise runtime behavior separately from typing.

For E, explain intrinsic/extrinsic state without notes. For I, implement and test the separate lab.
For D, diagnose its design pressure and refactor while preserving the original attempt. For X,
predict and reproduce the controlled experiment, then challenge its limits. For T, decide whether
a new backend workload deserves sharing. Maintainer execution supplies teaching artifacts only;
Rahul's evidence must be recorded separately before any learning state advances.

## 12. Related patterns, alternatives and misuse

| Related unit | Relationship | Distinction |
|---|---|---|
| [SDP-CRE-050 — Singleton](../../../CURRICULUM.md#sdp-cre-050) | Both can reuse objects | Singleton constrains instance availability; Flyweight shares values per key and scope |
| [SDP-CRE-040 — Prototype](../../../CURRICULUM.md#sdp-cre-040) | Alternative representation choice | Copying derives objects; Flyweight intentionally aliases safe state |
| [SDP-STR-040 — Proxy](../../../CURRICULUM.md#sdp-str-040) | A proxy may cache a target/result | Proxy controls access; Flyweight separates repeated intrinsic state |
| [SDP-STR-050 — Composite](../../../CURRICULUM.md#sdp-str-050) | Leaves may share values | Recursive structure does not by itself justify canonicalization |
| [SDP-PYT-060 — Dataclasses, immutable value objects, and enums](../../../CURRICULUM.md#sdp-pyt-060) | Practical value representation | Equality/frozen fields do not automatically create a sharing factory |

A resource pool lends exclusive or limited-use resources that may return for reuse; a Flyweight can
be used by many clients as shared intrinsic state. An identity map preserves one entity instance per
persistent identity so edits stay consistent; our tiles are specifications whose equal values remain
substitutable even without one canonical object. Memoization saves repeated computation; it becomes
part of a Flyweight design only when its result is suitable shared state with extrinsic context outside.

Common misuses: use global mutable dictionaries as “immutable metadata”; key by `hash(key)` alone
and ignore collisions; include user IDs merely to avoid analyzing ownership; call `setdefault(key,
Tile(key))` and assume hits skip Tile construction; claim a memory win from `a is b`; or close a shared
resource when one borrower finishes. Each needs a contract correction, not another factory layer.

## 13. Interview preparation

Ask one prompt at a time and wait for the attempt. During review identify the first missing reasoning
step; do not reveal every prompt's answer as a script.

| Prompt | Weak-answer trap | Exact reasoning checkpoint |
|---|---|---|
| Explain sharing for 100,000 placements and 20 designs. | “Use a dictionary.” | Separate occurrence context from repeated payload and identify owners |
| Why can equal tiles be different objects? | “Dataclasses intern values.” | Separate generated equality from factory canonicalization |
| A design gains a color profile. What changes? | Add the field but keep the old key | Connect every meaning-changing input to key or fixed scope |
| Pool size is low but memory grows after clear. Why? | Blame garbage collection first | Find surviving placement references and total live populations |
| Does `lru_cache` construct each tile once across threads? | “It is thread safe.” | Distinguish cache coherence from duplicate overlapping computation |
| Every tile is unique and small. Should we share? | Always apply the named pattern | Compare index overhead and simpler representations |
| Can a client close a shared decoder? | Treat a resource as plain immutable data | State lifetime/lease ownership and reject unsafe substitution |

Follow up with one changed requirement: live asset revisions, a byte budget, parallel requests,
selection highlight, or restart persistence. A senior answer names a scope and failure policy,
considers explicit sharing first, and states what must be measured before promising savings.

## 14. Closed-book reconstruction and vocabulary

Rebuild the reference graph, name the key, trace one hit and one rejected miss, explain an old
placement after clear, then predict both workload distributions. Diagnose a mutable list inside a
frozen tile. Transfer the reasoning to a shared lookup table and reject it for one session object.

| Word | Pronunciation | Simple meaning | Hindi cue | Engineering usage |
|---|---|---|---|---|
| Intrinsic | in-TRIN-zik | Belonging to the thing itself | अंतर्निहित | Pixel data is intrinsic within this tile-design scope |
| Extrinsic | ek-STRIN-zik | Coming from its context | बाहरी संदर्भ | Placement position is extrinsic to the tile |
| Retention | ri-TEN-shun | Keeping something longer | बनाए रखना | The pool retains tiles after the placements disappear |

Natural uses: “The material has intrinsic strength.” “The score reflects extrinsic conditions.”
“The retention period ends tomorrow.” In an interview: “I would separate intrinsic content from
extrinsic position.” In a review: “Who owns retention after this export job completes?”

## 15. Python Mastery references and sources

The relevant mapped prerequisite is
[PY-LIB-060 — Dataclasses, enums, types, and generated data models](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-lib-060),
through SDP-PYT-060 in [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md). Minimum bridge:
generated fields/equality describe values; frozen is an ordinary API constraint; reuse is explicit.
There is no direct SDP-STR-070 mapping, so no new cross-repository prerequisite is invented.

Sources actually read on 2026-09-09 are linked near claims: the GoF authors' paper §3.2 (available
transcription), the catalog's indexed participants/collaboration excerpt (full PDF unavailable),
Python 3.11 and 3.14 dataclasses, Python's data model, typing.final, weakref, functools cache,
free-threading guide, sys.getsizeof, and tracemalloc. These support mechanics; the grid, lab and
measurement workload are original synthetic material. No copied book diagrams, license change,
private data or NotebookLM upload is included. Approved notes may be reviewed under the
[NotebookLM policy](../../../docs/NOTEBOOKLM.md); raw attempts, solutions and logs are excluded.

## 16. Practice and recorded validation

Start the [unsolved legend lab](practice/README.md) with a prediction, then inspect the
[controlled experiment](experiments/EXP-01-sharing-retention/README.md). Run commands and see actual
maintainer results in [VALIDATION.md](VALIDATION.md). No learner attempt or solution is present.
