# SDP-STR-010 — Adapter

## Physical Notebook Core

### Problem or change pressure

The stock screen asks for individual items. A warehouse SDK answers in cases, uses different names,
and can return unknown stock. Copying its rules into every screen makes a provider change a domain change.

### One-sentence mental model

> Put a translator at the boundary so the consumer receives the meaning it already expects.

### One essential visual

```text
consumer: read("BOLT") → Stock(units=12)
                    │ target contract
                    ▼
             WarehouseAdapter
               │ request: item_code="BOLT"
               ▼
           LegacyWarehouse
               │ response: cases=2, pack_size=6
               └────────► validate → multiply → Stock(12) → consumer
```

### How to read this visual

Follow the request downward and the translated response back to the consumer. Arrows are calls/data
flow; the consumer knows `StockReader`, while the adapter knows the warehouse vocabulary.

### Key insight

A renamed method is insufficient if its number still means cases instead of individual items.

### Simplification or limitation

This is a conceptual call map, not Python memory layout. It shows one successful synchronous read;
unknown values, errors, ownership, and concurrent inventory changes need explicit contracts too.

### Governing rules or invariants

1. The consumer owns the target meaning: units, absence, errors, and observable effects.
2. Validate the external representation before constructing a domain value; do not guess missing facts.
3. State whether the adapter borrows or owns its collaborator, and what repeated calls do.

### Minimal Python example

```python
def individual_units(cases: int, pack_size: int) -> int:
    return cases * pack_size


assert individual_units(2, 6) == 12  # Trusted values in this tiny conversion example.
```

### One common misconception

**Mistake:** If the methods have the same type signature, the adapter is correct.

**Correction:** A type checker can accept an integer measured in the wrong unit. Contract tests must
check meaning, exceptions, state, and effects that the annotations cannot express.

### Important trade-offs

- A boundary localizes vendor knowledge but adds a maintained translation contract.
- A small function is often sufficient; an object helps when a collaborator must be retained.
- Lossy conversion needs an explicit policy. No wrapper can recover information the provider lacks.

### Interview-revision cues

- Recognition: useful existing behavior has an incompatible interface or representation.
- Comparison: translating a contract differs from simplifying a subsystem or wrapping extra behavior.
- Rejection: when you safely own both ends, changing the original API may be simpler.

## Unit metadata

| Field | Value |
|---|---|
| Domain | GoF structural patterns |
| Curriculum | [SDP-STR-010](../../../CURRICULUM.md#sdp-str-010) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Translate one interface or data shape into another at a boundary without contaminating domain code. |
| Hard prerequisites | [SDP-FND-050](../../../CURRICULUM.md#sdp-fnd-050), [SDP-FND-070](../../../CURRICULUM.md#sdp-fnd-070) |
| Soft prerequisites | None |
| Priority | Core |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D2 |
| Scope | GoF, Structural, Python |
| Size | L |
| First understanding | 4–6 h |
| Hands-on practice | 5–9 h |
| Evidence profile | E+I+D+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Approved |

Frequency labels are curriculum judgments, not measured statistics. Learning remains **Not started**:
maintainer authoring and test execution are not Rahul's evidence. Study the worked
[examples](examples/run_adapter_demo.py), [controlled boundary experiment](experiments/EXP-01-shape-and-meaning/README.md),
and [separate unsolved route lab](practice/README.md). Actual checks belong in [VALIDATION.md](VALIDATION.md).

## 1. Simple explanation and prerequisite bridge

A stock screen asks, “Can I supply ten bolts?” The warehouse replies, “Two cases.” Both can be
correct, yet they cannot collaborate safely until somebody establishes that each case contains six
bolts. A translator knows the supplier's wording and the screen's expected wording. The screen
continues to compare individual units with individual units.

Composition means the adapter **has** a warehouse object. Delegation means its `read` method calls
that object's `fetch_cases`. Inheritance means a class participates in another class's lookup/type
relationship; it is not required for this collaboration. Runtime duck typing calls an available
method. A `Protocol` lets a static checker compare the required methods without mandatory base-class
inheritance. The prerequisite notes are approved, but their learning states are Not started; this
bridge does not assert prior mastery.

## 2. Real problem and a decision ladder

The stable concern is deciding whether a requested item quantity is available. The changing concern
is how a supplier expresses it. Constraints include a provider we cannot edit, several consumers,
meaningful unknown values, and an existing domain vocabulary that should survive migration.

| Choice | Smallest useful form | When to move beyond it |
|---|---|---|
| Ordinary direct call | Client calls an API that already means what it needs | A real incompatibility appears |
| Conversion function | A pure function changes a data representation | Conversion also needs calls, errors, or a retained dependency |
| Injected callable | Consumer receives one operation with the right signature | Named capabilities or related operations improve clarity |
| Composition-based object adapter | An object retains the adaptee and exposes the target operation | More objects alone are not a reason to add another layer |
| Class adapter | Inherit existing behavior and expose a different interface | Use only with a deliberate inheritance/override requirement |
| Metaclass/automatic forwarding | Generates many apparent adapters | Usually obscures contracts; first prove repetition is truly semantic repetition |

Do not add an adapter merely because a library exists. An isolated script can call that library
directly. When both ends are yours and all consumers can migrate together, rename or reshape the
owned API and remove the mismatch. For a rolling migration, a temporary adapter can be useful; give
it an owner and removal condition rather than declaring the transitional interface permanent.

## 3. GoF intent and modern interpretation

The GoF intent is to enable collaboration despite an incompatible existing interface. Their catalog
distinguishes inheritance-based class adaptation from composition-based object adaptation.
The original participant names remain useful; Python can implement the same design with a function
or structurally compatible object. See the authors' publisher-hosted
[intent excerpt](https://www.informit.com/articles/article.aspx?p=1398600) and
[structure, participants, and consequences](https://www.informit.com/articles/article.aspx?p=1398600&seqNum=2).
The examples and diagrams here are original and use no book implementation or artwork.

Data/schema conversion at a backend boundary is this unit's modern application of the idea. Adapter
is a design relationship, not a Python keyword, generated class requirement, or guarantee that any
two systems can be made equivalent.

## 4. Participants and formal contract

| Participant | Here | Owns | Must not own |
|---|---|---|---|
| Target | `StockReader` and `Stock` | Consumer's callable shape and documented meaning | Vendor schema names |
| Client | `availability` | Policy: enough, short, or unknown | Case conversion, SDK exceptions |
| Adaptee | `LegacyWarehouse` | Existing keyword-only operation and payload | Consumer policy |
| Adapter | `WarehouseAdapter` | Request, result, and known error translation | Reservations, retries, unrelated business decisions |
| Composition root | Demo's `main` | Construction, injection, and close | Per-item availability policy |

The first four roles correspond to the GoF collaboration; the composition root is an explicit
ownership addition in this example. The
[publisher excerpt](https://www.informit.com/articles/article.aspx?p=1398600&seqNum=2) describes clients
calling adapters, which delegate to adaptees. The following constraints are our synthetic contract.

| Dimension | Agreed boundary behavior |
|---|---|
| Input | 1–24 uppercase ASCII letters, digits, or hyphens; no silent trimming or case changes |
| Value | `Stock.units` is a nonnegative integer or `None`; booleans are excluded |
| Units | Individual items; valid cases multiplied by valid pack size |
| Absence | Missing vendor row or explicit null case count means unknown, not zero |
| Errors | Known vendor timeout → `StockUnavailable`; malformed answer → `InvalidStock` |
| Timing/effects | Exactly one provider query per valid read; no cache, retry, or reservation |
| Lifetime | Adapter borrows the warehouse; root closes it after consumers finish |
| Freshness | Each call queries again, but there is no multi-read snapshot or reservation guarantee |

A wrapper cannot promise atomic reservation using only an observational read. If the target requires
that stronger effect, change the target/provider capability or reject the integration. Calling the
operation twice and choosing the larger answer does not repair the mismatch.

## 5. Collaboration and execution flow

```text
main owns Warehouse ──lends──► Adapter ──injected as StockReader──► availability

availability       Adapter                  Warehouse
     │ read("BOLT")  │                          │
     ├──────────────►│ validate input           │
     │               ├─ fetch_cases(item_code) ►│
     │               │◄─ schema-v1 record ──────┤
     │               │ validate identity/schema/count/pack
     │◄─ Stock(12) ──┤                          │
     │ compare to 10 │                          │
main ──────────────────────────────────────────► close (after use)
```

### How to read this visual

The top line names ownership/injection; the lower lines are a conceptual timeline. Read downward.
Only the adapter translates the successful provider answer, and only the root closes the provider.

### Key insight

Runtime calls travel from policy toward a provider; source dependencies stop the policy from
importing the vendor. Injection chooses the concrete adapter without moving vendor details inward.

### Simplification or limitation

This shows synchronous success with one owner. Timeout exits before decoding; bad input exits
before I/O. Real transports require their own authentication, timeouts, byte limits, and shutdown
guarantees. The diagram does not certify concurrency or depict CPython internals.

## 6. Before-pattern code and concrete pain

```python
row = {"cases": 2, "pack_size": 6}
screen_has_enough = row["cases"] * row["pack_size"] >= 10
assert screen_has_enough
```

This is reasonable for one trusted calculation. Now export, alerts, and preview all repeat it.
One compares `cases` directly to item demand. Another converts null to zero with `or 0`. A third
knows a renamed vendor field. The concrete pain is disagreement about meaning and three change sites,
not the number of `if` statements. Extract one conversion boundary and test the agreed behavior there.

## 7. Minimal Pythonic implementation and callable alternative

A consumer with only one operation can receive a callable. The names in this tiny example describe
trusted inputs; the full decoder later validates untrusted payloads.

```python
from collections.abc import Callable


def label(read_units: Callable[[str], int], sku: str) -> str:
    return f"{sku}: {read_units(sku)} units"


def legacy_cases(item_code: str) -> int:
    return {"BOLT": 2}[item_code]


def read_units(sku: str) -> int:
    return legacy_cases(sku) * 6


assert label(read_units, "BOLT") == "BOLT: 12 units"
```

The callable already performs adaptation. A closure can retain a provider; an object gives the
retained dependency a named home. Neither form removes the need to specify unknown values, errors,
ownership, and freshness. Do not force the fuller nullable stock contract into this deliberately
smaller integer-only example without revising its type and behavior.

## 8. Typed implementation: shape plus meaning

Read [stock_contract.py](examples/stock_contract.py), then
[warehouse_adapter.py](examples/warehouse_adapter.py). The former has no vendor import. The latter
contains the only warehouse-to-domain conversion. The
[synthetic SDK](examples/legacy_warehouse.py) exposes `fetch_cases(*, item_code)` returning `object`,
so a vendor annotation cannot be mistaken for validated JSON.

```python
from legacy_warehouse import LegacyWarehouse
from stock_contract import Stock, StockReader, availability
from warehouse_adapter import WarehouseAdapter

vendor = LegacyWarehouse({"BOLT": {"schema": 1, "item": "BOLT", "pack_size": 6, "cases": 2}})
reader: StockReader = WarehouseAdapter(vendor)
assert reader.read("BOLT") == Stock(12)
assert availability(reader, "BOLT", 10) == "enough"
assert availability(reader, "UNKNOWN", 1) == "unknown"
```

`WarehouseAdapter` does not subclass `StockReader`; structural assignability checks its members.
The positional-only `sku` lets implementations choose a local parameter name. If the target allowed
keyword calls, compatible parameter naming/kinds would matter too. Narrowing input types, adding a
required argument, or returning the wrong type breaks substitutability at the call level.
These are typing-specification rules, not a runtime adapter generator:
[protocol assignability](https://typing.python.org/en/latest/spec/protocol.html#assignability-relationships-with-other-types),
[callable assignability](https://typing.python.org/en/latest/spec/callables.html#assignability-rules-for-callables).

Passing mypy does not establish the documented count unit. The probe's `CountsCases` matches the
signature yet answers two instead of twelve. A runtime-checkable protocol is even shallower: it does
not validate method signatures or attribute types. From Python 3.12 onward, its attribute lookup uses
`inspect.getattr_static` and its checked member set is frozen at class creation; 3.11 uses older
behavior. Ordinary methods in this example work on both baselines. No adapter should rely on such a
presence check as boundary validation. See
[`runtime_checkable`](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable).

No framework is involved and no CPython-specific implementation is needed. The runnable files use
Python 3.11-compatible syntax, including ordinary `Protocol`, unions, and dataclasses. Python 3.14
annotation changes do not drive this design: the adapter does not introspect annotations.

## 9. Schema, units, nullability, and validation

`decode_stock` accepts a decoded JSON-shaped value. An actual network integration must bound the
response and parse JSON before this function. It is not a sandbox for hostile Python objects.

| Vendor condition | Translation | Why |
|---|---|---|
| No record | `Stock(None)` | Synthetic vendor contract says unknown |
| Schema 1, matching item, valid pack, null cases | `Stock(None)` | Unknown survives the boundary |
| Zero cases | `Stock(0)` | Known empty is useful information |
| Two cases × six per case | `Stock(12)` | Target uses individual units |
| Missing required field or wrong item | `InvalidStock` | Defaulting would invent meaning or mix identities |
| Unknown schema or invalid pack/count | `InvalidStock` | Reject unsupported semantics |
| Extra metadata | Ignore | Target does not expose vendor debug fields |

This is an explicit policy: optional unknown *values* are allowed; missing mandatory *fields* are not.
Even a null count must carry a valid schema, item, and pack size. Accepting schema 2 by guessing that
its fields still mean the same thing would erase the version boundary. Extra fields are tolerated,
but changed meanings of recognized fields are not.

Counts are bounded here to 0–1,000,000 cases and 1–1,000 items per case as synthetic service limits.
They are not Python limits. Booleans are integer subtypes, so `isinstance(True, int)` would accept a
boolean; `type(value) is int` deliberately rejects booleans and integer subclasses at this decoded
data boundary. Python integers have unlimited precision; our limits express a service contract, not
machine overflow prevention. See [built-in numeric types](https://docs.python.org/3.14/library/stdtypes.html#numeric-types-int-float-complex).

For currencies, timestamps, or measurements, write the corresponding rules before conversion:
currency and scale, zone/offset, rounding, inclusive limits, and whether null means unknown or absent.
Do not reuse the stock multiplication as a generic recipe. If seconds become whole minutes, an
information-losing policy is unavoidable; if timestamps lack a time zone, an adapter cannot discover it.

## 10. Error translation, observability, and security

Only `WarehouseTimeout` becomes `StockUnavailable`. A provider timeout is not zero stock and does
not prove a route is missing. Malformed answers become `InvalidStock`. Unexpected `TypeError` and
use-after-close errors remain visible programming/lifecycle failures. Broadly catching `Exception`
and returning a successful domain value would turn defects into false business facts.

The adapter uses `raise StockUnavailable(...) from error` to preserve diagnostic causality.
Python's explicit chaining records the cause; `from None` suppresses its ordinary display but is not
data erasure. See the [raise statement](https://docs.python.org/3.14/reference/simple_stmts.html#the-raise-statement).
Our tests check a safe outer message, not a secret-free traceback. An API edge must serialize an
allowlisted public error, and logging must have its own redaction/access policy. Do not return
`repr(error)`, raw payloads, SDK client representations, or chained traceback text to callers.

As a production design choice, count boundary outcomes such as success, unknown, timeout, and invalid
schema; measure latency at the call boundary and attach safe correlation IDs. Avoid item IDs as
unbounded metric labels. Correlate a spike in invalid answers with provider/deployment revisions.
These are operational recommendations for this design, not measured security or performance results.
Translation does not authorize access: tenant identity and permissions must be established explicitly.

Failure walk-through: schema 2 starts sending strings. The decoder rejects it; the outer application
shows a provider error instead of “out of stock.” Inspect a sanitized fixture and release/version
agreement, then add a dedicated tested v2 translator or roll back the integration. Do not silently
enable coercion to make the alert disappear.

## 11. Ownership, state, and repeated calls

The demo's root uses `closing(warehouse)`. The adapter borrows it; successful reads, unknown reads,
and timeouts do not close it. `closing` calls `close()` when leaving its context, including when its
body raises; see [`contextlib.closing`](https://docs.python.org/3.14/library/contextlib.html#contextlib.closing).
The synthetic `close` cannot fail. A real SDK needs documented acquisition and cleanup failure behavior.

```python
from contextlib import closing

from legacy_warehouse import LegacyWarehouse
from warehouse_adapter import WarehouseAdapter

with closing(LegacyWarehouse({})) as vendor:
    reader = WarehouseAdapter(vendor)
    assert reader.read("BOLT").units is None
    assert not vendor.closed
assert vendor.closed
```

An adapter object has a provider reference even when it has no per-read cache. Two adapters borrowing
the same provider share that provider's state; two providers can serve independent configurations.
Each read is fresh in the limited sense of making a new query. Inventory can still change immediately
after the answer. `Stock` contains only an integer or None, so results do not alias the mutable vendor
record; mutating a later payload does not retroactively change an earlier result.

Caching changes freshness and error behavior. Retrying changes call count and latency, and a timeout
on a write may leave its outcome unknown. Decide deadlines, idempotency, and reconciliation before
adapting a side-effectful API. Our read-only example deliberately performs no retry or reservation.

## 12. Proportionate concurrency and async boundaries

A stateless translation function does not establish that the borrowed SDK client is safe to share
between threads. This synthetic client has mutable rows, call tracking, and a one-shot failure flag;
the tests are sequential and claim no concurrency safety. A real integration needs a provider
guarantee, per-request instances, or appropriate coordination. A lock cannot make two external reads
one atomic inventory snapshot.

An `async def read` has a different call contract from a synchronous `read`: callers await it.
Merely wrapping a blocking SDK call in `async def` still blocks when that call runs. `asyncio.to_thread`
can move suitable blocking I/O to a thread, as documented in
[running in threads](https://docs.python.org/3.14/library/asyncio-task.html#running-in-threads).
Before choosing it, settle SDK thread affinity, cancellation, deadlines, and who may close the client
while work is outstanding. This unit implements no async adapter and makes no cancellation guarantee.

## 13. Refactoring and a realistic backend migration

1. Characterize the current consumer's units, absence, errors, and effects with tests.
2. Identify the mismatch that the provider cannot reasonably change for you.
3. Write the smallest target contract; do not mirror every SDK method.
4. Extract conversion, then inject a callable or composed adapter where that seam is needed.
5. Test provider-shaped fixtures at the boundary and domain behavior without vendor imports.
6. Wire the owner at startup; migrate one consumer and observe boundary outcomes.
7. Add the next provider/revision only after its actual contract is known; remove obsolete glue.

A backend preview endpoint and export worker can consume the same `StockReader` contract while
startup chooses a vendor-specific adapter for each configuration. They can test “unknown versus
short” with a small fake. Provider contract/integration tests separately prove whether the SDK still
returns the documented schema and timeout type. These local synthetic tests cannot verify a live
provider, deployment permissions, transport, or real freshness.

## 14. Testing strategy and controlled experiment

| Check | Evidence | Limit |
|---|---|---|
| Decoder examples/property test | Exact integer conversion, bounds, nullability, identity, drift | Only declared decoded shapes |
| Adapter behavior | Request shape, one call, known error translation, fresh reads | Synthetic SDK only |
| Consumer tests | Policy works with an independently implemented target | Does not prove vendor translation |
| Lifetime tests | Owner closes once on success/body failure; borrower does not | Synthetic close cannot fail |
| Strict mypy and negative assignment | Structural method contract accepted/rejected | Cannot distinguish cases from items |
| Boundary probe | Runtime shape acceptance, call failure, semantic mismatch | Controlled observation, not a benchmark |
| Real provider contract test, future integration | Versioned fixtures and actual SDK/transport agreement | Not run in this unit |

The [experiment](experiments/EXP-01-shape-and-meaning/README.md) keeps the canonical evidence profile
**E+I+D+T** unchanged. It demonstrates why runtime presence, static signatures, and behavior are three
different checks. Add regression cases when an integration failure exposes a missing contract rule;
avoid asserting private attribute names or incidental object counts.

## 15. Object versus class adapter; overengineering

An object adapter holds an adaptee and delegates. A class adapter inherits adaptee behavior and
exposes the target interface; the GoF class form uses multiple inheritance. In Python a structural
target may remove the need for a separate target base class. Inheritance still ties construction,
overrides, and method lookup to the chosen vendor class. Composition lets this example borrow an
already configured client. See
[GoF consequences](https://www.informit.com/articles/article.aspx?p=1398600&seqNum=2).

| Misuse | Concrete problem | Better choice |
|---|---|---|
| Subclass every vendor and every target | Constructor/MRO and override assumptions multiply | Inject a configured vendor object |
| Metaclass creates methods from field names | Names reveal neither units nor error semantics | Explicit short translators and contracts |
| Forward everything through `__getattr__` | Vendor API becomes an accidental consumer API | Expose only the target capability |
| Convert every missing value to zero | Unknown becomes a false fact | Preserve absence or reject according to contract |
| Adapter contains discount/reservation policy | Translation becomes a domain decision center | Keep policy in the consumer/domain layer |
| Separate class for each two-line conversion | More indirection without lifecycle or naming value | A pure function or injected callable |

A two-way adapter is not automatically reversible. A many-to-one conversion cannot reconstruct the
original distinction. An adapter also need not expose every capability of either side: justify the
small consumer-facing subset instead of promising universal transparency.

## 16. Related patterns, bounded comparisons

| Related unit | Shared appearance | Key distinction here |
|---|---|---|
| [SDP-STR-020](../../../CURRICULUM.md#sdp-str-020) — Facade | A new entry point | Adapter translates a required contract; Facade simplifies subsystem use |
| [SDP-STR-030](../../../CURRICULUM.md#sdp-str-030) — Decorator | Wraps an object | Decorator adds behavior around a compatible contract |
| [SDP-STR-040](../../../CURRICULUM.md#sdp-str-040) — Proxy | Intermediary object | Proxy controls access; hidden caching can change observable semantics |
| [SDP-STR-060](../../../CURRICULUM.md#sdp-str-060) — Bridge | Composition | Bridge separates independently varying dimensions |
| [SDP-SOL-050](../../../CURRICULUM.md#sdp-sol-050) — DIP | Consumer-facing abstraction | DIP concerns source dependencies; Adapter handles incompatibility |

These are recognition cues, not implementations or new units. More detailed comparison belongs to
[SDP-INT-030](../../../CURRICULUM.md#sdp-int-030) and [SDP-INT-040](../../../CURRICULUM.md#sdp-int-040).
Composition alone does not identify intent.

## 17. Use, rejection, and production trade-offs

Use adaptation for an external/legacy API, independently released service, or staged migration when
a stable consumer contract has real value. Keep vendor-specific names, exceptions, pagination, and
data parsing at the boundary. Pick an object when retained configuration/dependencies clarify use;
pick a function for a small pure conversion.

Reject it when the interfaces already agree, the only caller can safely change, the adapter cannot
meet the required effect, or speculative compatibility creates more maintenance than the mismatch.
Translation costs another call layer and validation work, but this unit measures no speed or memory
advantage. Network cost may dominate in a real service; measure that actual workload before removing
validation. The synthetic bounds do not replace transport-level size limits.

## 18. Interview preparation

Ask these **one at a time** during a live review and wait for the answer. The gap column diagnoses
what to probe next; it is not a memorized answer script or evidence that Rahul has answered.

| Prompt | Weak-answer trap | Exact missing reasoning step |
|---|---|---|
| Explain Adapter in plain language | “A wrapper class” | Name the incompatible contracts and what stays stable |
| Two cases pass a typed `int` check; enough for ten items? | “The checker passed” | Establish units and pack-size semantics |
| Could this be a function? | “Patterns require classes” | Identify whether any state/lifetime needs an object |
| Why composition here? | “Inheritance is bad” | Explain borrowing an existing client and preserving its lifecycle |
| Null count arrives; return zero? | “Avoid optional types” | Distinguish lack of knowledge from known empty |
| SDK times out; retry three times? | “Retries increase reliability” | Establish effect, deadline, and idempotency before policy |
| v2 adds a field and changes a unit | “Ignore unknown fields” | Separate additive shape changes from semantic drift |
| The provider is synchronous, caller asynchronous | “Add async to the method” | Explain where blocking work actually executes |
| Can read implement reserve? | “Add a method called reserve” | Prove the required external effect is available |
| Should we keep this migration adapter forever? | “Abstractions are always good” | Name ownership and a removal condition |

Code-review exercise: someone replaces the decoder with `int(payload.get("cases") or 0)` and returns
that number. Identify the first violated invariant before proposing code. Follow up with a malformed
schema, a timeout, and a zero count one at a time. For implementation evidence use the separate route
lab; the worked example is not a learner attempt.

## 19. Closed-book revision and vocabulary

Reconstruct the four GoF roles, draw request/result/ownership arrows, explain two versus twelve, then
state how unknown differs from zero. Reject an unnecessary wrapper for an owned API. Transfer the
reasoning to timestamps without assuming the same conversion policy.

| Word | Pronunciation | Simple meaning | Hindi cue | Design use |
|---|---|---|---|---|
| Translate | trans-LAYT | Express the same meaning differently | रूप बदलना | Preserve meaning across representations |
| Contract | KON-trakt | An agreed promise | तय वादा | Inputs, outputs, errors, and effects |
| Compatible | kum-PAT-uh-bul | Able to work together | साथ काम करने योग्य | Calls and behavior satisfy consumer expectations |

Natural usage: “Translate the directions for the visitor.” “The contract states the delivery time.”
“Check whether the charger is compatible.” In an interview: “The signature is compatible, but the
count uses the wrong unit.” In review: “Keep the vendor translation outside the availability policy.”

## 20. Run and study

Run from the repository root. Use an existing locked development interpreter as `python`; do not
modify an unrelated environment. Inspect `python --version` and tool versions first. Route generated
state outside the repository (including for mypy subprocesses in the full regression):

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-str-010/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-str-010/mypy
export RUFF_CACHE_DIR=/tmp/sdp-str-010/ruff
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-str-010/hypothesis
export UV_CACHE_DIR=/tmp/sdp-str-010/uv
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-str-010/venv
export COVERAGE_FILE=/tmp/sdp-str-010/coverage
mkdir -p /tmp/sdp-str-010/pytest
python units/structural/SDP-STR-010-adapter/examples/run_adapter_demo.py
python units/structural/SDP-STR-010-adapter/examples/boundary_probe.py
python units/structural/SDP-STR-010-adapter/practice/route_lab.py
python -m pytest -p no:cacheprovider --basetemp=/tmp/sdp-str-010/pytest/focused units/structural/SDP-STR-010-adapter
python scripts/validate_repo.py
```

The demo's expected lines are `enough`, `unknown`, `short`, `queries=3`, `closes=1`. Snippets importing
example modules require `PYTHONPATH=units/structural/SDP-STR-010-adapter/examples`; each Python fence
is otherwise independently executable. The lab prints a working old label and explicitly reports
that the target is incomplete. Consult [VALIDATION.md](VALIDATION.md) for executed checks and limits.

## 21. Python Mastery references

There is no direct Adapter row in [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md). Through the
two hard prerequisite mappings, use the exact following references without inventing new prerequisites:

- [PY-OBJ-010 — Classes, instances, methods, and construction](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-010): identify instance state and bound calls.
- [PY-OBJ-020 — Properties, encapsulation, and composition](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-020): retain and delegate to another object.
- [PY-OBJ-030 — Inheritance, MRO, and super](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-030): distinguish inheritance lookup from borrowing a client.
- [PY-TYP-050 — Protocols, ABCs, and structural versus nominal typing](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-typ-050): separate runtime duck typing, static shape, and explicit nominal relationships.

## 22. Authoritative sources and handoff boundaries

Read on 2026-09-09. Sources support the linked claims, not every independent engineering judgment.

1. Gamma, Helm, Johnson, Vlissides: InformIT's [Adapter intent excerpt](https://www.informit.com/articles/article.aspx?p=1398600) and [applicability/structure/participants/consequences](https://www.informit.com/articles/article.aspx?p=1398600&seqNum=2). Publisher-hosted excerpt read; no book text, code, or diagrams copied.
2. Python typing specification: [Protocols](https://typing.python.org/en/latest/spec/protocol.html) and [Callables](https://typing.python.org/en/latest/spec/callables.html), assignability sections.
3. Python 3.14 [`typing.runtime_checkable`](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable), shallow checks and 3.12 changes.
4. Python 3.14 [built-in numeric types](https://docs.python.org/3.14/library/stdtypes.html#numeric-types-int-float-complex), integers and booleans.
5. Python 3.14 [raise statement](https://docs.python.org/3.14/reference/simple_stmts.html#the-raise-statement), explicit exception chaining.
6. Python 3.14 [`contextlib.closing`](https://docs.python.org/3.14/library/contextlib.html#contextlib.closing), owner cleanup.
7. Python 3.14 [asyncio running in threads](https://docs.python.org/3.14/library/asyncio-task.html#running-in-threads), blocking I/O adaptation boundary.

After approval, only this approved integrated note and relevant canonical/source-policy excerpts
are NotebookLM inputs. Do not upload progress trackers, validation logs, code trees, raw attempts,
solutions, or private data. Follow [NOTEBOOKLM.md](../../../NOTEBOOKLM.md). No learner review exists yet;
there is no invented recall, attempt, weakness, or completion claim.
