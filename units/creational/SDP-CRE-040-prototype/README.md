# SDP-CRE-040 — Prototype

## Physical Notebook Core

### Problem or change pressure

You already have an approved, configured starting object. Rebuilding it repeats configuration work;
sharing it lets one request damage another. Its nested graph may contain intentional shared nodes.

### One-sentence mental model

> Start from a known exemplar, then create a new object using an explicit policy for what to copy,
> share, reset, reconstruct, or reject.

### One essential visual

```text
exemplar A ──► mutable graph G ──► shared child C (two paths)
     │
     └─ clone ──► request B ──► new graph G' ──► new child C' (same two paths)
           │
           ├─ immutable compiled rules: shared deliberately by A and B
           ├─ request identity: supplied fresh; cache: reset
           └─ live handles: acquired separately, never in the copied graph
```

### How to read this visual

Arrows mean references or the labeled clone operation. Apostrophes identify new mutable objects.
Two paths to C become two paths to one C', rather than two unrelated children.

### Key insight

Independence **between** requests and sharing **inside** one request are different requirements.

### Simplification or limitation

This is a conceptual ownership diagram, not CPython memory layout. It omits cycles, failure cleanup,
concurrent writers, authorization, and schema migration. Copying alone resolves none of those.

### Governing rules or invariants

1. Specify freshness and sharing per field and per edge; equality does not prove isolation.
2. Preserve intentional graph topology within one clone operation unless the domain says otherwise.
3. Validate before publishing, require new business identity where needed, and keep resources outside.

### Minimal Python example

```python
from dataclasses import dataclass, field


@dataclass
class Palette:
    colors: list[str] = field(default_factory=list)

    def clone(self) -> "Palette":
        return Palette(self.colors.copy())


approved = Palette(["ink", "sand"])
working = approved.clone()
working.colors.append("moss")
assert approved.colors == ["ink", "sand"]
```

A shallow list copy suffices here because its elements are immutable strings and there are no graph
edges, request counters, caches, or external handles. This is deliberately smaller than the worked
backend example.

### One common misconception

**Mistake:** `deepcopy` makes everything different and therefore safe.

**Correction:** Copy protocols can share objects, copying cannot confer authorization, and an
independent stale value is still stale. State the domain contract first.

### Important trade-offs

- Reusing configuration reduces reconstruction coupling but makes ownership policy another API.
- Full graph traversal can cost more than rebuilding a small value; immutable sharing may be simpler.
- A configured exemplar needs versioning and an owner; a global mutable template is fragile.

### Interview-revision cues

- Recognition: a configured starting instance is the useful input to creation.
- Comparison: Builder accumulates steps; Prototype starts from an existing instance.
- Rejection: three inexpensive immutable fields need keyword construction or replacement.

## Unit metadata

| Field | Value |
|---|---|
| Domain | GoF creational patterns |
| Curriculum | [SDP-CRE-040](../../../CURRICULUM.md#sdp-cre-040) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Create objects through copying when construction state is expensive or externally configured, and reason about shallow copies, deep copies, identity, and shared state. |
| Hard prerequisites | [SDP-FND-090](../../../CURRICULUM.md#sdp-fnd-090), [SDP-PYT-060](../../../CURRICULUM.md#sdp-pyt-060) |
| Soft Python bridge | [PY-OBJ-040](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-040), [PY-FND-020](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-fnd-020), [PY-IOP-060](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-iop-060) |
| Priority | Advanced |
| Interview frequency | Low |
| Production frequency | Low |
| Python/backend relevance | Medium |
| Depth | D3 |
| Scope | GoF, Creational, Python |
| Size | L |
| First understanding | 4–6 h |
| Hands-on practice | 5–9 h |
| Evidence profile | E+I+D+X+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Draft |

Frequency labels are curriculum judgments, not measured usage statistics. This is maintainer-authored
material; neither these files nor passing checks establish Rahul's learning evidence.

Study this note, run the [worked example](examples/run_prototype_demo.py), compare the
[interactive graph explorer](visuals/README.md), observe the
[controlled experiment](experiments/EXP-01-copy-graph/README.md), then attempt the
[separate unsolved dispatch lab](practice/README.md). Actual checks belong in [VALIDATION.md](VALIDATION.md).

## 1. Simple explanation and prerequisite bridge

Imagine an approved query plan with filters already arranged. A new request needs the same shape
but its own edits. Repeating the original configuration code is error prone. Handing out the same
object lets one request's edits affect everyone. Prototype makes the existing configured object the
starting point for creation and gives copying a documented meaning.

The useful input is the exemplar's **state**, not simply its class. The configuration might have
come from a visual editor, an expensive parser, or a trusted runtime extension. Copying could save
that work, but only measurement can establish a performance benefit.

The prerequisites have approved notes but are not recorded as learned. The smallest bridge is:

- Two names can refer to one object. Rebinding one name does not mutate that object.
- A list owns references to elements; copying the list need not copy the elements.
- An owner decides who may mutate state and when it becomes invalid or must be closed.
- A dataclass generates ordinary methods; it does not automatically define a deep-copy policy.
- A frozen outer value can still contain mutable children. Prefer immutable leaves when sharing.

Try tracing two names pointing to the same list before studying a cycle. If that is difficult, use
[SDP-FND-090](../../../CURRICULUM.md#sdp-fnd-090) first; use
[SDP-PYT-060](../../../CURRICULUM.md#sdp-pyt-060) for value invariants and generated construction.

## 2. Start with the simplest design

### Ordinary construction

```python
class Page:
    def __init__(self, title: str, limit: int) -> None:
        if limit < 1:
            raise ValueError("positive limit required")
        self.title = title
        self.limit = limit


page = Page("Summary", 20)
```

This is enough if there are two cheap, known inputs. A clone API would add an ownership promise
without removing any real reconstruction work.

### Keyword-only dataclass

```python
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class PageOptions:
    title: str
    columns: tuple[str, ...]
    limit: int = 20

    def __post_init__(self) -> None:
        if not self.columns or self.limit < 1:
            raise ValueError("invalid page options")


options = PageOptions(title="Summary", columns=("date", "total"))
```

Named fields expose intent, and immutable strings/tuples avoid shared-mutation problems for this
trusted typed example. Freezing is shallow; it does not recursively transform arbitrary inputs.
[Python 3.11 dataclasses](https://docs.python.org/3.11/library/dataclasses.html#frozen-instances).

### Focused factory function

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Limit:
    rows: int


def interactive_limit() -> Limit:
    return Limit(rows=50)
```

Use a function when a named rule supplies ordinary constructor arguments. Centralize defaults there
instead of storing a mutable example object simply to avoid writing its constructor twice.

### Immutable value replacement

```python
from dataclasses import dataclass, replace


@dataclass(frozen=True, kw_only=True)
class ExportOptions:
    columns: tuple[str, ...]
    limit: int = 20


base = ExportOptions(columns=("date", "total"))
large = replace(base, limit=200)
assert large.columns is base.columns
assert base.limit == 20
```

Unchanged references can be shared safely when their reachable values are immutable. This is often
the whole solution. Calling it GoF Prototype would add little explanatory value unless exemplar
selection and a creation contract are the actual design pressures.

### Explicit reconfiguration

If the external rules change, rebuild from current inputs. Copying a revision-3 object does not
magically apply revision-4 policy. A function such as `load_and_validate(current_revision)` at the
composition boundary can be clearer than cloning and repairing a stale graph field by field.

### The pressure that justifies Prototype

Now the approved plan contains a configurable graph, reused filter nodes, and a back edge for
navigation. The client must create request-local working instances without knowing how the editor
assembled them. A clone operation can hide that reconstruction and preserve its defined structure.
A prototype registry is still unnecessary when the client receives one chosen exemplar directly.

## 3. History and formal meaning

The GoF catalog belongs to Gamma, Helm, Johnson, and Vlissides' *Design Patterns: Elements of
Reusable Object-Oriented Software*, published by Addison-Wesley in October 1994.
[Publisher catalog](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/).
Its creational chapter treats creation as a responsibility that can be separated from use.
[Creational chapter preview](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/ch03.html).

In operational language, **Prototype chooses an existing configured instance as an exemplar and
creates further objects through that exemplar's copying contract**. This unit's graph, domain,
Python APIs, and policies are original teaching choices. No book example or diagram is reproduced.

`copy.copy(my_list)` is a library operation. It may support Prototype, defensive copying, a local
algorithm, or no named pattern at all. The GoF design is visible when client creation depends on an
exemplar and its copy contract rather than rebuilding concrete starting state itself. Prototype is
also distinct from the word “prototype” meaning a disposable proof of concept or JavaScript's
prototype-based inheritance.

## 4. Participants and responsibilities

| Participant | Owns | Must not own |
|---|---|---|
| Prototype contract | Meaning of creating from an exemplar; freshness, state and error promises | A claim that every reachable object is copyable |
| Concrete Prototype | Its field policy, validation, graph copy and allowed specialization | Application authorization or arbitrary live-resource duplication |
| Client | Requests a clone through the contract and uses the returned object | Knowledge of every concrete constructor or internal graph edge |
| Optional registry | Selects a trusted, versioned exemplar when many named exemplars exist | A global dumping ground for mutable per-request state |
| Composition root | Constructs/loads exemplars and injects dependencies | Hidden import-time network access |

[The code](examples/prototype.py) uses `DraftPrototype` as a structural typing seam for the client.
`QueryDraft` is the concrete exemplar and result. `GraphNode` owns graph mechanics. `CompiledRules`
is an immutable value shared by explicit policy. There is no inheritance hierarchy or registry class:
those would not solve an additional problem in this example.

## 5. Collaboration and execution flow

```text
composition root: trusted configuration → validated exemplar
                                            │ inject
                                            ▼
client → clone(fresh request ID, expected revision)
           1. reject invalid identity/version/type
           2. validate current source graph
           3. copy mutable graph with one memo
           4. construct valid candidate; share rules; reset cache
           5. return candidate
client → separate resource scope → use → close resources
```

### How to read this visual

Follow creation from the configured exemplar through the numbered boundary, then follow the
separate resource lifetime. Failure before step 5 leaves no returned candidate.

### Key insight

A graph copy and external resource reconstruction have different failure and lifetime semantics.

### Simplification or limitation

This is design-level control flow. It assumes an exclusively owned, trusted source during cloning.
It does not provide a database transaction, synchronized snapshot, or external rollback.

## 6. Identity, equality, aliases, and ownership

**Language contract:** `is` compares object identity; `==` invokes value-comparison behavior. A new
object may compare equal to its source. An immutable container can refer to mutable objects.
[Data model: objects, values and types](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types).

```python
a = ["base"]
b = a
c = a.copy()
assert b is a
assert c == a and c is not a
b = ["replacement"]
assert a == ["base"]
c.append("local")
assert a == ["base"]
```

For a graph, test the actual ownership edges: `result.root is not source.root` proves only a new
root. It says nothing about grandchildren. Follow the edge that a consumer can mutate.

An alias is a second path to the same object. It may be intentional: two stages can share one
request-local filter, so editing that filter should affect both stages in that request. Breaking all
aliases would change behavior just as surely as sharing a filter across independent requests.

Do not use generated recursive equality as a graph-isolation test. The worked `GraphNode` uses
`eq=False` so cycles do not invite recursive field comparison. A domain needing graph equivalence
must define whether labels, edges, sharing, and order all participate. It needs a cycle-aware
comparison, not a blind `source == clone` assertion.

A Python object ID is not a database key, request ID, tenant ID, idempotency key, or authorization
identity. The example accepts a fresh request ID, but the caller must ensure uniqueness across
requests. Checking inequality with the exemplar alone is insufficient for global uniqueness.

## 7. Shallow versus deep: trace a mutation

**Standard-library contract:** shallow copying creates an outer compound object with referenced
children; deep copying recursively uses copy behavior. One traversal's memo tracks already copied
objects, supporting cycles and repeated references. Custom hooks can control what is shared.
[Python 3.11 copy](https://docs.python.org/3.11/library/copy.html).

```python
from copy import copy, deepcopy

child = {"tags": ["base"]}
source = [child, child]
shallow = copy(source)
deep = deepcopy(source)
assert shallow is not source and shallow[0] is child
assert deep[0] is not child and deep[0] is deep[1]
deep[0]["tags"].append("local")
assert deep[1]["tags"] == ["base", "local"]
assert child["tags"] == ["base"]
```

Here the deep copy is independent from the source but internally shared. Neither “deep means every
reference differs” nor “shared means unsafe” is precise enough.

| Operation in the controlled graph | Fresh root | Child shared with source | Two child edges still alias | Back edge reaches returned new root |
|---|---|---|---|---|
| Assignment | No | Yes | Yes | No new root |
| Shallow copy | Yes | Yes | Yes | No |
| Deep copy in one call | Yes | No | Yes | Yes |
| Dataclass replacement of root label | Yes | Yes | Yes | No |
| Independent deep copy per child | Yes | No | No | No |

These are properties of our specific graph and classes, not universal promises for every custom
copy hook. The [experiment](experiments/EXP-01-copy-graph/README.md) and
[visual](visuals/README.md) use the same measured observations.

## 8. Cycles and memoization without invented internals

```python
from copy import deepcopy

source: list[object] = []
source.append(source)
result = deepcopy(source)
assert result is not source
assert result[0] is result
```

The new container must be remembered before following its back edge. In our custom node hook,
allocate a private shell, associate this source identity with it, and forward the same memo into all
child copies. Do not create a new memo inside the child loop.

For CPython 3.14.7 specifically, `deepcopy` consults the memo before dispatch, and the built-in list
copier records its new list before visiting elements. The implementation also stores private
bookkeeping there. This explains why the hook adds its own source-to-shell entry but must not assume
all memo values are graph nodes or inspect undocumented entries.
[Version-pinned copy.py](https://raw.githubusercontent.com/python/cpython/v3.14.7/Lib/copy.py).

Separate top-level `deepcopy(a)` and `deepcopy(b)` calls do not coordinate shared children. Copy
`[a, b]` together when the two roots belong to one graph. Reusing a memo across independent request
clones is also wrong: it can return old results and preserve cross-request sharing. Treat the memo
as scoped to one successful traversal. Discard it after a failed traversal; it may contain incomplete
shells. It is not a persistent application cache.

## 9. Copy protocols and custom hooks

The library recognizes `__copy__()` and `__deepcopy__(memo)`; recursive hooks must forward the memo.
It can also consult pickling interfaces and `copyreg` registrations. This is extensible execution,
not raw byte duplication. [Python 3.11 copy](https://docs.python.org/3.11/library/copy.html).

The worked node's shallow hook returns a new node that deliberately shares the tags and edges
containers. Its deep hook is the small graph-specific mechanism below:

```python
from copy import deepcopy


class Link:
    def __init__(self, label: str) -> None:
        self.label = label
        self.edges: list[Link] = []

    def __deepcopy__(self, memo: dict[int, object]) -> "Link":
        if type(self) is not Link:
            raise TypeError("subclass needs its own contract")
        result = object.__new__(Link)
        memo[id(self)] = result
        result.label = self.label
        result.edges = deepcopy(self.edges, memo)
        return result


root = Link("root")
root.edges.append(root)
assert deepcopy(root).edges[0].label == "root"
```

This hook intentionally bypasses `__init__`; it initializes every promised field itself. The
smaller `Link` is a teaching sketch. The maintained `GraphNode` additionally copies tags, has a
shallow hook, and is tested for cycles and repeated edges. Do not generalize `object.__new__` to
extension types or classes with allocation invariants.

The domain-level `QueryDraft` rejects both generic copy operations. Its caller must use
`clone(request_id=..., expected_revision=...)`, because neither standard hook accepts those required
business arguments. A named method is clearer than secretly generating IDs or retaining a stale
request cache inside `__deepcopy__`.

Do not add serialization hooks solely to implement cloning. If a class already defines
`__reduce_ex__`, `__getstate__`, or `__setstate__`, audit their interaction with copying and keep
persistence policy separate from request-clone policy. Trusted custom hooks can run code and cause
side effects; they are not a sandbox for objects received from unknown plugins.

## 10. Typed production-oriented example

The maintained files are [prototype.py](examples/prototype.py),
[client composition](examples/run_prototype_demo.py),
[typing contracts](examples/typing_contracts.py), and
[resource boundary](examples/resource_boundary.py). They run on Python 3.11 and 3.14.

| State or capability | QueryDraft policy | Reason |
|---|---|---|
| Request ID | Require nonempty value different from exemplar | New request identity is a caller decision |
| Compiled rules | Share frozen validated tuple-of-strings value | No mutable reachable rules are needed |
| Mutable node graph | Deep copy using graph hooks and one memo | Isolate requests while preserving internal topology |
| Cache | Fresh empty dictionary | Cached results describe the old request |
| Configuration revision | Compare to caller's required revision | Reject known stale exemplar |
| Node/draft subclasses | Reject unreviewed runtime types at copy boundary | New fields could silently lack policy |
| Live sockets/files/locks/DB sessions | Absent from the model | Reconstruct through an explicit resource scope |

Execution uses `new_request(prototype, ...)`; it does not select a constructor. A Protocol documents
what that client consumes without runtime registration. A structural type checker checks signatures,
not source isolation, version freshness, authorization, or alias topology. The tests supply those
behavioral checks. `@final` is static intent; exact-type guards at the copy seam enforce the selected
runtime policy. Other applications can support subclasses, but must define and test their policy.

The graph validator is iterative and counts distinct identities, so a legal cycle does not loop
forever. The example caps distinct nodes at 100 as a teaching bound. It does **not** bound edge count,
tag bytes, hook cost, or recursion depth of an arbitrary input. Trusted typed in-process objects and
exclusive ownership are explicit preconditions. An external-input boundary needs parsing, byte and
edge budgets, allowed types, authorization, and possibly a nonrecursive domain copier.

`CompiledRules` checks the tuple/string representation at construction; its frozen contract is an
ordinary application invariant, not protection against a hostile caller using reflection. The code
never copies secret-bearing runtime contexts into request drafts.

## 11. Dataclass construction is a separate axis

`dataclasses.replace` calls the constructor; a generated constructor invokes `__post_init__`.
Required `InitVar` inputs must be provided. `init=False` fields are not copied and cannot be supplied
as changes; computed fields may be rebuilt. Unknown fields fail. A custom constructor must arrange
its own post-init behavior. [Python 3.14 replacement and post-init](https://docs.python.org/3.14/library/dataclasses.html#dataclasses.replace).

```python
from dataclasses import dataclass, field, replace


@dataclass
class Batch:
    size: int
    tags: list[str] = field(default_factory=list)
    doubled: int = field(init=False)

    def __post_init__(self) -> None:
        if self.size < 1:
            raise ValueError("invalid size")
        self.doubled = self.size * 2


original = Batch(2)
updated = replace(original, size=3)
assert updated.doubled == 6
assert updated.tags is original.tags
```

The experiment compares replacement to ordinary copy dispatch for a similar dataclass. On both
observed runtimes, default shallow/deep copying preserved a deliberately altered computed field
without running post-init; replacement recomputed it. That is evidence about these classes and
runtimes. A custom hook or reducer can choose construction instead.

A dataclass `default_factory` creates a value when the constructor needs a default. It does not
promise a new child when replacement passes an existing field value, and it does not specify the
behavior of `deepcopy`. Keep expensive network reads out of `__post_init__`: replacement might repeat
them, while other copy paths might skip them. Separate pure invariant validation from external
readiness checks.

`asdict` is an export-oriented recursive conversion, not the clone contract. It changes the
representation and recursively converts containers/dataclasses while deep-copying other values.
Do not infer graph identity preservation from its output.
[Dataclass conversion](https://docs.python.org/3.14/library/dataclasses.html#dataclasses.asdict).

## 12. Python 3.11 and 3.14 boundary

| Facility | Python 3.11 | Python 3.14 | Choice in this unit |
|---|---|---|---|
| `copy.copy`, `copy.deepcopy`, hooks and memo | Available | Available | Explicit graph policy on both |
| `dataclasses.replace` | Available | Available | Use for dataclass field replacement |
| `copy.replace`, `__replace__` | Unavailable | Available, introduced in 3.13 | Optional overlay only |
| Keyword-only dataclasses, slots, `StrEnum` | Available | Available | Code remains 3.11-compatible |
| Dataclass `field(doc=...)`, `make_dataclass(decorator=...)` | Unavailable | Added in 3.14 | Not required here |

`copy.replace` accepts named tuples, dataclasses, and types exposing `__replace__`; it returns a new
same-type object with requested field changes. It is not generic recursive isolation. Functions and
classes can be returned unchanged by generic copying, while file/socket-like resources are outside
its supported copying contract. Container-specific copies can lose a subclass even when generic
`copy.copy` normally preserves it. [Python 3.14 copy](https://docs.python.org/3.14/library/copy.html).
The dataclass additions above are documented in
[Python 3.14 dataclasses](https://docs.python.org/3.14/library/dataclasses.html).

```python
import copy
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Window:
    limit: int


base = Window(20)
newer_replace = getattr(copy, "replace", None)
updated = replace(base, limit=30) if newer_replace is None else newer_replace(base, limit=30)
assert updated.limit == 30 and base.limit == 20
```

Prefer a direct `dataclasses.replace` call for a fixed dataclass. This runtime branch exists only to
show the version boundary. A non-dataclass `__replace__` API needs its own explicit 3.11 alternative,
such as `with_limit`; a dataclass fallback is not a universal polyfill. The note avoids newer generic
syntax so interview-platform compilation remains meaningful.

A verified documentation/source discrepancy matters for error handling: the 3.14 library prose
still describes `ValueError` for replacement of an `init=False` field, while the version-pinned
3.14.7 implementation raises `TypeError`. Our tests observe `TypeError` for both that case and a
missing required `InitVar` on 3.14.7, versus `ValueError` on 3.11.16. The invariant is rejection;
version-sensitive adapters should normalize these boundary errors intentionally. We do not infer the
first patch that changed the exception type. [CPython 3.14.7 dataclasses.py](https://raw.githubusercontent.com/python/cpython/v3.14.7/Lib/dataclasses.py).

A current-documentation sentence about “method” objects is broader than the version-pinned CPython
code: bound methods have a dedicated deep-copy path that copies their receiver. This is a reason
to inspect the concrete supported type, not promise that every callable is safely shared. The unit
relies only on the verified plain-function case and stores no callbacks in its graph.
[CPython method copier](https://raw.githubusercontent.com/python/cpython/v3.14.7/Lib/copy.py).

## 13. Subclasses and defensive contracts

A base-class `clone` returning `Base(...)` may erase a subclass and its fields. Replacing that with
`type(self)(...)` can fail when the subtype requires extra constructor arguments or different
invariants. A shell allocation can preserve the type yet leave new slots uninitialized. All three
can look correct in a base-only test.

Choose deliberately: forbid inheritance at the clone seam; require every subtype to implement a
contract suite; or use composition so variable policy lives in an explicit value. This example
chooses the first and third. A separate application that promises subtype-preserving clones could
use `Self`, but only if every permitted subtype actually fulfills that promise. A return annotation
cannot manufacture correct copying.

Whenever a field is added, review identity, mutable ownership, defaulting, validation, repr/logging,
serialization, and cleanup implications. New cache, lock, callback, or tenant context fields are
especially likely to invalidate an old “copy all attributes” implementation. Tests should fail when
an intended invariant stops holding, rather than snapshotting an internal `__dict__` layout.

## 14. Failure atomicity and partial clone cleanup

For trusted pure graph copying, the desired contract is: return one valid clone or raise without
mutating the source or publishing a partial result. The example validates, creates a private graph,
and constructs the candidate before returning it. A caller assigning `result = clone(...)` receives
no result when the call raises. It does not undo arbitrary side effects from custom hooks.

A hook that records its unfinished shell in a global registry has already broken that boundary.
A hook that opens a socket now also owns cleanup if a later child fails. Garbage collection is not
a substitute for explicit close, and a failed copy with a caller-supplied memo can leave an incomplete
shell reachable. Discard that memo; do not continue from it as if it were a valid graph.

The safer split is pure clone first, then resource materialization. The maintained
[resource scope](examples/resource_boundary.py) uses `ExitStack`: successful acquisitions register
cleanup, and failures in a later acquisition close earlier resources in reverse order. The failing
acquisition must clean up anything it allocated before its own context entry completed.
[ExitStack and partial entry cleanup](https://docs.python.org/3.14/library/contextlib.html#contextlib.ExitStack).

The tests inject first-acquisition, second-acquisition, and body failures. No real network resources
are opened. External actions already sent, billed, or committed cannot be rolled back by closing a
handle. A retry after an uncertain external result needs an idempotency/reconciliation policy at
that external boundary.

## 15. Resource and ownership decisions

| Candidate state | Default production judgment | Failure if copied mechanically |
|---|---|---|
| Immutable rule/value object | Share if truly immutable and valid for this scope | Hidden mutable leaf leaks edits |
| Mutable request graph | Copy according to topology/ownership contract | Cross-request mutations or broken internal aliases |
| Derived cache | Reset, or prove version/scope-safe sharing explicitly | Stale or cross-tenant results |
| File handle | Pass immutable path/descriptor data to a new acquisition scope | Shared cursor or double-close assumptions |
| Socket/client session | Reacquire or inject a managed dependency | Duplicated Python wrapper does not create a new remote session |
| Lock | Keep with the state it protects; redesign the boundary | New lock with shared state gives false exclusion |
| DB handle/transaction/ORM session | Keep outside the prototype | Transaction identity and lifecycle become ambiguous |
| Callback/closure | Audit captured state or inject separately | Shared function can retain mutable request or secret context |
| Credential | Resolve an authorized reference at use time | Secret lifetime and scope widen unnecessarily |

These are design recommendations, not a universal rule that every vendor handle raises the same
exception. The standard copy documentation lists important unsupported resource types, and the
experiment checks an actual file object on both tested runtimes.

## 16. Security, secrets, and observability

Treat a prototype loaded from an editor or plugin as a trust boundary. Validate serialized data
before constructing trusted graph objects. Never “sanitize” an arbitrary Python object by deep
copying it; its methods may execute, and the copy may retain forbidden capabilities or secrets.
A change of request ID also does not authorize a change of tenant.

Secret duplication can enlarge where sensitive data lives and how long it remains reachable. Even
when immutable string bytes are shared rather than physically copied, another logical owner can
retain or expose the secret. Prefer capability-scoped references, avoid snapshots of authentication
contexts, and define retention. Do not claim that deleting a Python reference securely erases bytes.
These are threat-model judgments for this design, not measurements of Python's allocator.

`observe` returns only node count, revision, and cache-entry count. It excludes labels, tags,
request IDs, and values; the top-level draft disables generated repr. That is a safe example payload,
not complete telemetry policy. Error messages use fixed codes. Review trace attributes and exception
logging too: suppressing repr on one class does not redact arbitrary nested objects.

In a service, record allowed clone outcome, policy version, bounded node/edge counts, elapsed time,
and rejection code. Use approved correlation metadata outside the graph. Separate clone latency
from external reconstruction latency. A telemetry failure should not retry the entire clone or
external work blindly; decide whether it is best-effort or explicitly required before publication.

## 17. Concurrency and snapshot consistency

Copying a graph requires many reads. If another owner mutates its edges and labels mid-traversal,
the result may combine states that never existed together. There is no synchronized snapshot
promise in this example. Keep the source request-local, freeze it after publication, or make every
writer cooperate with a lock held over validation and traversal.

Locking only the root assignment does not protect a shared mutable child. Copying a lock along with
the graph does not repair the source's synchronization. If copy hooks call arbitrary code, holding
a lock across them can cause reentrancy or deadlock; prefer immutable snapshots or narrowly trusted
copy functions. A revision check is useful only when the revision and state belong to one coherent
snapshot. Check-then-copy without coordination is a race.

CPython 3.14's free-threading guide recommends explicit synchronization rather than relying on
built-in internal locks. Those locks and the GIL are not a transaction over your graph.
[Thread safety guidance](https://docs.python.org/3.14/howto/free-threading-python.html#thread-safety).
The recorded runs use the available interpreters; they do not establish free-threaded safety or
stress-test concurrent writers.

## 18. Async and external reconstruction

`__deepcopy__` is synchronous. Do not smuggle an async connection setup into it or try to synchronously
run a second event loop. Copy a pure plan, then use an explicit async factory/context manager to
resolve external dependencies. At that seam, validate current credentials, configuration revision,
and resource readiness again as required by the domain.

Use `AsyncExitStack` for awaitable context entry and cleanup. Cancellation during acquisition is a
failure path: already-entered resources need cleanup; an acquisition interrupted before successful
entry must clean up its own partial allocation. Keep handles scoped to the async context and preserve
cancellation semantics. [AsyncExitStack](https://docs.python.org/3.14/library/contextlib.html#contextlib.AsyncExitStack).

The synchronous fake-resource tests illustrate ownership transfer only. They do not prove an async
provider's cancellation behavior, remote rollback, or cleanup under repeated cancellation. Verify
those through that provider's contract and integration tests before adapting the code.

## 19. Serialization, configuration drift, and persistence

Copying answers how a running process creates another object. Serialization answers how state is
represented across a storage or transport boundary. They may share implementation hooks but need
separate identity, compatibility, trust, and lifetime rules.

JSON does not preserve arbitrary object identity or cycles without an explicit graph schema. Pickle
can preserve sharing, but class importability and application schema changes still matter; loading
untrusted pickle data can execute code.
[Python pickle: comparison and security](https://docs.python.org/3.14/library/pickle.html).
Do not round-trip through pickle just to avoid deciding what a clone should contain.

A prototype registry should identify configuration and policy revisions, origin/trust level, and
scope. A revision mismatch should trigger deliberate reload or a supported migration, not a deep
copy of stale state. The example only checks an expected integer revision supplied by its caller;
it neither discovers current configuration nor proves that the caller's revision is up to date.

After a deployment, old exemplars may lack new fields or carry rules compiled for older code.
Reconstruct from validated source configuration where practical. If migration is required, define
it as a named operation, validate the output, and retain an audit of source/target versions. Cloning
is not migration, schema evolution, or database row duplication.

## 20. Import and composition boundaries

Keep the graph/value module free of import-time registration, credentials, sockets, and network
reads. A composition root loads trusted data once, chooses an exemplar, and injects it into the
client. The demo makes this direction visible in a small separate file.

If named runtime selection becomes necessary, a dictionary of trusted versioned exemplars may be
enough. Decide whether registration snapshots the exemplar, transfers exclusive ownership, or
accepts immutable values; otherwise the registering caller can mutate future results. Check
unknown names, duplicate registration, lifecycle, and update atomicity. Avoid a registry of every
class in the program or filesystem auto-discovery merely to use the pattern name.

A factory callable can wrap a clone operation if the client only needs “give me a fresh draft.”
That is often simpler than exposing a universal `Cloneable` interface. Retain the explicit version,
identity, and ownership contract regardless of surface syntax.

## 21. Performance and memory

The example does not simulate expensive parsing with a sleep or claim a speedup. Its force is
configured graph structure; performance is a hypothesis to measure. Constructing a small dataclass
can beat traversing a large graph, while sharing a compiled immutable value can avoid unnecessary
reconstruction without invoking generic deep copy at all.

For a bounded graph and constant-cost hooks, a reasonable cost model follows visited nodes, edges,
and copied payload. Memo lookup avoids revisiting shared nodes, but payload size, custom hook work,
allocation, and recursion depth still matter. Treat this as an analytical model, not a Python
language complexity guarantee. The 100-node limit is not a total memory budget.

If a benchmark is needed, compare ordinary reconstruction, immutable replacement, domain clone,
and generic deep copy on representative graph shapes. Include trees, high fan-out, repeated nodes,
cycles, large leaf buffers, and rejected inputs. Record Python build, hardware, warm-up, trials,
median/spread, peak allocations, and retained results. Measure external setup separately. Reusing
one memo or accidentally benchmarking a shared immutable object can make a misleading “fast clone.”

`id` values and object counts are not retained byte measurements. The current experiment is a
semantic probe with deterministic booleans and labels, not a timing or memory benchmark.

## 22. Realistic backend use and refactoring path

A trusted query editor produces a configured analysis graph. Each request receives a new working
graph with the same approved rules and its own cache/identity. This is a plausible Prototype use if
reconstructing that graph is coupled to editor details the request client should not know.

Start by preserving outputs with tests. Mark every field as copy/share/reset/reconstruct/reject.
Find the first actual shared-state bug and add a mutation test for its edge. Introduce one named
clone seam and move reconstruction knowledge behind it. Test a second request and repeated-node
identity. Add invalid input, stale version, and partial failure cases. Remove the seam if the graph
can instead become a small immutable value created by a clear factory.

For a database-backed service, prefer a pure specification over cloning ORM entities with sessions,
primary keys, and loaded relationships. For a simulation, a clone may be appropriate, but random
generator state and reproducibility need a deliberate policy. For a compiled parser, immutable
compiled rules may be shared while mutable parser state is freshly constructed. These are selection
examples, not additional implementations or new curriculum units.

## 23. Alternatives and related patterns

| Related design | Useful creation input | Relation to Prototype | Prefer it when |
|---|---|---|---|
| Ordinary constructor / keyword dataclass | Known field values | No exemplar needed | Construction is simple and cheap |
| Focused factory function | Named policy plus arguments | May internally clone, but need not | Defaults or setup are easy to centralize |
| Immutable replacement, [SDP-PYT-060](../../../CURRICULUM.md#sdp-pyt-060) | Existing value plus changed fields | Shares unchanged immutable state naturally | No mutable graph isolation is needed |
| Factory Method, [SDP-CRE-010](../../../CURRICULUM.md#sdp-cre-010) | Creator's overridable creation operation | Chooses creation through a method hook | Creator workflow is stable and product creation varies |
| Abstract Factory, [SDP-CRE-020](../../../CURRICULUM.md#sdp-cre-020) | Consistent product family | A family factory could own exemplars | Several collaborating product types must match |
| Builder, [SDP-CRE-030](../../../CURRICULUM.md#sdp-cre-030) | Construction steps and staged inputs | Builder can create the first exemplar | Incomplete construction needs controlled finalization |
| Prototype | Configured exemplar | Reuses starting instance state through a copy contract | Reconstruction is coupled or measured expensive |

A fluent API does not imply Builder, and a `clone` name does not prove Prototype solves a useful
force. These comparisons support this unit's selection judgment; later units are not authored here.

## 24. Failure scenarios and recovery judgment

| Symptom | First question | Containment / next action |
|---|---|---|
| Editing request A changes B | Which mutable edge still aliases? | Stop handing out that exemplar; add ownership test and repair policy |
| Second copied stage ignores first-stage edit | Were its shared children copied in separate traversals? | Restore intended internal alias contract |
| Recursion failure | Is the hook memoizing before following cycles? Is depth excessive? | Correct the hook or reject/rework the graph shape |
| New clone has old results | Was a cache copied across request/version scope? | Reset or key/share only under a proven invariant |
| New subtype loses state | Does base clone assume its constructor or slots? | Reject subtype until contract is implemented and tested |
| Clone passes tests but uses old policy | Who supplies the current revision? | Reload/revalidate at a coherent configuration boundary |
| Resource leak after child failure | Where did acquisition become owned? | Register cleanup at acquisition; keep handles outside graph |
| Copy returns source itself | Does its hook intentionally share? | Check contract; reject if independent mutation was promised |
| Request ID is fresh but data crosses tenants | Is authorization independent from copying? | Contain exposure; enforce tenant-scoped inputs and capabilities |

Recovery must address the violated invariant. Catching every exception and returning the source
silently is especially dangerous: callers believe they own an independent draft.

## 25. Testing strategy

| Test | Evidence | Avoid overspecifying |
|---|---|---|
| Mutation/isolation in both directions | Expected mutable edges do not cross requests | Numeric object addresses |
| Alias and cycle identity assertions | Internal topology survives | Allocation order or memo's private contents |
| Fresh ID, reset cache, shared immutable rules | Field-level domain policy holds | Equality alone |
| Rejection and failure injection | No candidate escapes and prior resources close | Vendor exception text for synthetic code |
| Dataclass reconstruction probe | Replacement and copying differ on tested classes | Universal claims that constructors always/never run |
| Protocol positive/negative checks | Client signature substitution | Runtime behavioral safety from annotations |
| Property tests of tag values | Mutation isolation over varied valid payload | Timing thresholds |
| Visual data parity | Every displayed observation matches the Python probe | A claim of browser rendering from string checks |

Tests live next to examples, the experiment, and the separate lab. The lab tests prove only baseline
behavior and that it remains unsolved. Do not interpret those green tests as solving the refactor.
The validation record distinguishes executed checks from design review and untested integration
boundaries.

## 26. When to use, when to reject, and overengineering

Use a clone seam when an approved or expensive-to-reconstruct starting instance is valuable, mutable
ownership can be specified, and the client benefits from not knowing reconstruction details. It can
also help when the concrete configured instance is chosen at runtime, though that does not require
a class hierarchy.

Reject it for tiny immutable values, objects dominated by live handles, untrusted arbitrary object
graphs, or configuration that must be fetched fresh every time. Prefer direct creation, replacement,
or a factory. A benchmark is needed if speed is the only argument.

| Misuse | Why it fails | Better move |
|---|---|---|
| Universal base class with reflective attribute copying | New fields silently inherit inappropriate policy | Explicit value/graph boundary |
| `deepcopy(self)` on a service container | Copies capabilities, caches, and lifecycle state indiscriminately | Clone pure specification; inject runtime dependencies |
| One global mutable prototype registry | Hidden sharing and update races | Explicit composition and versioned ownership |
| Reconstruct every immutable leaf | Unneeded work and obscured sharing intent | Reuse proven immutable values |
| Break every alias to achieve “independence” | Changes behavior within the clone | Define internal topology separately |
| Catch copy failure and return original | Violates ownership without warning | Raise a bounded error and retain source |
| Copy as a substitute for tenant authorization | Identity changes do not grant rights | Authorize at the boundary |

## 27. Interview preparation

Use one prompt at a time during an interview. These review notes identify gaps; they are not scripts
to memorize and do not reveal the dispatch lab's implementation.

1. **Define Prototype using a concrete force.** Weak answer: “It uses clone.” Missing step:
   explain why an existing configured instance is the input to creation. Follow-up: why not a factory?
2. **Two equal drafts pass an equality test; are they isolated?** Weak answer: “Yes.” Missing step:
   trace the mutable edge a consumer can reach and test identity plus mutation.
3. **Two filters intentionally alias inside a plan. What should a clone do?** Weak answer: “Duplicate
   each filter.” Missing step: separate cross-request isolation from within-request sharing.
4. **Review `[deepcopy(child) for child in edges]`.** Weak answer: “It is deep, so fine.” Missing step:
   identify separate memo scopes and their effect on repeated references and back edges.
5. **A copied dataclass has a stale derived field.** Weak answer: “Dataclasses validate automatically.”
   Missing step: distinguish replacement/constructor execution from copy hooks or reduction.
6. **A new subclass adds a lock and credential context.** Weak answer: “Use `type(self)`.” Missing
   step: assign copy and lifetime policy to the new fields and verify subtype invariants.
7. **A revision check passes while an editor changes the graph.** Weak answer: “The GIL handles it.”
   Missing step: define a coherent snapshot boundary covering all reads and writers.
8. **The second resource acquisition fails.** Weak answer: “Garbage collection closes it.” Missing
   step: show ownership and explicit cleanup of the first acquisition and the failing entry itself.
9. **Deep copy is proposed for a three-field immutable request.** Weak answer: “Prototype is flexible.”
   Missing step: compare direct keyword construction and value replacement with actual change pressure.
10. **A clone crosses tenants and retains an API credential.** Weak answer: “Generate a fresh ID.”
    Missing step: distinguish Python/business identity from authorization and capability scope.

A concise strong answer names the exemplar, field-level contract, simplest rejected alternative,
mutation evidence, and the major lifecycle or concurrency boundary. An honest “a factory is enough
here” can be the best senior answer.

## 28. Closed-book revision cues

Reconstruct the ownership visual. Explain `is` versus `==`. Draw one graph with two paths to a child
and a back edge, then predict assignment, shallow copy, deep copy, replacement, and separate child
copies. State where the memo starts and ends. Name one field for each policy: share, copy, reset,
reconstruct, reject. Explain why a fresh ID and passing Protocol check do not imply authorization or
isolation. Reject Prototype for a small immutable options object.

## 29. Practice and evidence

[The dispatch lab](practice/README.md) follows predict → run → observe → explain → refactor → vary.
Preserve the original starter and Rahul's first attempt. Reveal one progressive hint only when
requested. The worked query graph is a distinct example; no target dispatch implementation is
included.

| Evidence profile item | Available artifact | Evidence still needed from Rahul |
|---|---|---|
| E — explanation | Notebook core and decision comparisons | Closed-book force and policy explanation |
| I — implementation | Runnable examples; unsolved lab starter | Original implementation attempt and tests |
| D — debugging | Aliasing counterexample and failure scenarios | Diagnose a mutation/reconstruction failure |
| X — experiment | Copy-graph probe with actual output | Prediction, observation, explanation, limitation |
| T — transfer | Changed requirements and interview prompts | Select or reject copying in a new scenario |

No dates, weaknesses, practice, recall, or transfer evidence are invented. Learning stays **Not
started** until the tracker thresholds are actually met. NotebookLM may receive only approved notes
and relevant policy; do not upload this task's raw attempts, tracker, or generated check output.

## 30. Vocabulary and professional English

### Exemplar — ig-ZEM-plar

A representative instance; Hindi cue: नमूना. In this design it is the configured object used as a
starting point. “Keep an exemplar for review.” “This exemplar has current settings.” “The exemplar
belongs to the editor.” **Interview:** “Creation depends on an exemplar's state.” **Engineering:**
“Publish a new revision of the exemplar after validation.”

### Alias — AY-lee-us

Another name or path to the same thing; Hindi cue: दूसरा संदर्भ. “The shortcut is an alias.” “Both
labels refer to one item.” “Remove the obsolete alias.” **Interview:** “These edges alias one mutable
node.” **Engineering:** “The clone must retain this alias within its own graph.”

### Reconstruct — ree-kun-STRUKT

Build again from known information; Hindi cue: फिर से बनाना. “Reconstruct the sequence.” “The record
lets us reconstruct the decision.” “We reconstructed the model.” **Interview:** “A factory can
reconstruct a small immutable value.” **Engineering:** “Reconstruct external resources in their own
lifetime scope.”

### Topology — tuh-POL-uh-jee

How parts connect; Hindi cue: जुड़ाव का ढाँचा. “Draw the network topology.” “The topology changed.”
“Two maps can show the same topology.” **Interview:** “Deep copying should preserve this graph's
intentional topology.” **Engineering:** “Test repeated edges and cycles, not just field equality.”

## 31. Exact Python Mastery references

[PY-FND-020 — Objects, names, references, and mutability](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-fnd-020)
bridges names and object identity.
[PY-OBJ-040 — Python data model and special methods](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-040)
bridges protocol participation.
[PY-IOP-060 — Pickle, shelve, copying, and object graphs](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-iop-060)
bridges aliasing and serialization risks. For the hard dataclass prerequisite, the mapping for
[SDP-PYT-060](../../../CURRICULUM.md#sdp-pyt-060) points to
[PY-LIB-060 — Dataclasses, enums, types, and generated data models](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-lib-060).
These are exact repository mappings, not claims that Rahul has studied them.

## 32. Authoritative sources actually read

- [GoF publisher catalog](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/)
  and [creational chapter preview](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/ch03.html): authors, date, and creation context; only accessible previews were read.
- [Python 3.14 copy](https://docs.python.org/3.14/library/copy.html) and
  [Python 3.11 copy](https://docs.python.org/3.11/library/copy.html): shallow/deep contracts, hooks,
  sharing, memo, resources, and replacement version boundary.
- [Python 3.14 dataclasses](https://docs.python.org/3.14/library/dataclasses.html) and
  [Python 3.11 dataclasses](https://docs.python.org/3.11/library/dataclasses.html): replacement,
  init/post-init, frozen values, InitVar, conversion, and version-specific additions.
- [Data model](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types):
  identity, values, and mutable contents of immutable containers.
- [CPython 3.14.7 copy.py](https://raw.githubusercontent.com/python/cpython/v3.14.7/Lib/copy.py):
  bounded implementation inspection of memo ordering and bound-method behavior.
- [CPython 3.14.7 dataclasses.py](https://raw.githubusercontent.com/python/cpython/v3.14.7/Lib/dataclasses.py):
  verification of replacement exception types where current prose and implementation differ.
- [contextlib](https://docs.python.org/3.14/library/contextlib.html#contextlib.ExitStack): explicit
  resource cleanup and async counterpart.
- [Free-threading guidance](https://docs.python.org/3.14/howto/free-threading-python.html#thread-safety):
  explicit synchronization and the limits of built-in internal locks.
- [pickle](https://docs.python.org/3.14/library/pickle.html): serialization, sharing, and trust boundaries.

Design selection, defensive limits, performance models, observability, and operational recommendations
are professional reasoning applied to original examples. Runtime-specific observations are labeled
and recorded in the experiment and validation files; they are not invented language guarantees.
