# SDP-SOL-030 — Liskov Substitution Principle and behavioural subtyping

## Physical Notebook Core

### Problem or change pressure

A client works with one catalog. A replacement has the same method, yet rejects a previously
valid code, hides absence, or consumes an entry. The client breaks without changing its own code.

### One-sentence mental model

> Replace the provider without taking away a promise the client was entitled to rely on.

### One essential visual

```text
client's valid call → promised contract → replacement
                         ↓
                 result + error + state
                         ↓
                 next valid call still works
```

### How to read this visual

Follow the call, then inspect its outcome and the state available to the next call.

### Key insight

A correct-looking first return value is not enough.

### Simplification or limitation

Conceptual contract reasoning, not Python memory layout. Timing and concurrent calls are omitted.

### Governing rules or invariants

1. Do not reject an input/state the shared contract accepts.
2. Preserve promised results, failures, and externally observable effects.
3. Preserve legal states and promised histories, including changes through other references.

### Minimal Python example

```python
from collections.abc import Callable


def read_twice(read: Callable[[str], str], code: str) -> tuple[str, str]:
    return read(code), read(code)


entries = {"x": "parcel"}
assert read_twice(entries.__getitem__, "x") == ("parcel", "parcel")
# Replacing __getitem__ with pop would break the second read.
```

### One common misconception

**Mistake:** “It inherits the class, or mypy accepts it, so substitution is safe.”

**Correction:** Shape and signature checks leave business meaning and effects to be established.

### Important trade-offs

- A stronger shared promise helps clients but admits fewer providers.
- Composition removes an inheritance relationship; it does not automatically repair behaviour.

### Interview-revision cues

- Name the caller's promise, a valid input, and the first observable violation.
- Compare an invariant at one moment with a restriction across moments.
- Reject the substitution when the real provider cannot honour the promised operation.

## Unit metadata

| Field | Value |
|---|---|
| Domain | SOLID principles |
| Curriculum | [SDP-SOL-030](../../../CURRICULUM.md#sdp-sol-030) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Evaluate subtype invariants, preconditions, postconditions, return behaviour, exceptions, mutation, and observable contracts instead of using the simplistic parent-child slogan. |
| Hard prerequisites | [SDP-FND-040](../../../CURRICULUM.md#sdp-fnd-040), [SDP-FND-060](../../../CURRICULUM.md#sdp-fnd-060), [SDP-FND-070](../../../CURRICULUM.md#sdp-fnd-070), [SDP-FND-090](../../../CURRICULUM.md#sdp-fnd-090) |
| Soft prerequisites | No additional curriculum units; Python generics and variance references below |
| Priority | Core |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D3 |
| Scope | SOLID, Contracts |
| Size | XL |
| First pass | 6–9 h |
| Practice and mastery | 8–14 h |
| Evidence profile | E+I+D+X+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11; the same supplied code is used |
| Artifact state | Approved |

Frequency labels are curriculum judgments, not measured statistics. Files are not learning
evidence. Read the [practice](practice/README.md) and [experiment guides](#runtime-experiments)
before running their commands; preserve your own predictions first.

## 1. Simple explanation and minimum prerequisite bridge

Imagine a lookup desk that promises to answer the same code consistently. Replacing the clerk
is fine; replacing the desk with a machine that destroys a record after answering is not fine
under that promise. “It can answer once” misses what the next customer needs.

The prerequisite artifacts exist, but no learner understanding is inferred from that:

- **Contract:** write what valid callers may ask and what they may observe afterward.
- **Dispatch:** calling `obj.lookup(code)` chooses behaviour from the actual object.
- **Interface:** inheritance and structural matching describe different relationships; neither
  establishes the complete behavioural contract.
- **Ownership:** two names can refer to one object. A change through one can affect the other.

Know instance attributes, overriding, composition, and `super()` from the exact Python units
listed below. `super()` delegates according to method resolution; calling it is not a contract
proof. [Python built-ins: super](https://docs.python.org/3.14/library/functions.html#super).
This unit does not require CPython internals or a deep generic-type implementation.

## 2. Real problem and forces

The solved example has a stable catalog of code-to-label entries. A shipping-label client may
read a code twice, distinguish absence from an empty label, and keep the original source mapping
for unrelated work. We want a second storage representation without changing those expectations.

The tension is not “never change anything.” It is deciding what belongs in this boundary's
promise. A consuming queue, an eventually refreshed catalog, and a snapshot catalog can all be
useful APIs. They are not interchangeable under an explicitly stable-read contract.

## 3. History and formal definition

Liskov and Wing's 1994 paper formalizes behavioural subtyping in terms of preserving properties
established from the supertype specification. It distinguishes state invariants from history
properties, particularly when mutable objects are shared. This unit uses that reasoning as an
engineering checklist, not a reproduction of the paper's proof system.
[Original paper, introduction and sections 4–5](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf).

For a proposed subtype `S` of `T`, compare operations at corresponding abstract states:

- `Pre_T ⇒ Pre_S`: the replacement cannot require more of a valid caller.
- On those calls, `Post_S ⇒ Post_T`: the replacement cannot promise less afterward.
- Legal subtype states must satisfy the supertype invariant under the representation mapping.
- Added operations and alias-visible changes must preserve specified history constraints too.
- Exceptional outcomes must remain within the promised failure behaviour.

Different internal representations are allowed. This is a compact account of the paper's
constraint-based formulation, not its alternative explanation-method formulation.
[Original paper, section 5.2](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf).

## 4. Participants and the concrete catalog contract

| Participant | Responsibility | Must not assume or own |
|---|---|---|
| `lookup_twice` client | Use stable repeated reads | A particular dictionary implementation |
| `label_or_unlisted` client | Convert documented absence to a display label | Catch every exception and pretend it means absence |
| `Catalog` protocol and prose | State the required call shape and meaning | Runtime verification of those promises |
| `DictCatalog`, `TupleCatalog` | Preserve the same observable catalogue | Caller-specific class checks |
| Composition code | Select and construct an implementation | Quietly weaken the client's contract |

The mapping passed at construction supplies the initial abstract contents. Compare replacements
built from the same contents, not unrelated catalogs with different data.

| Dimension | Promise in this example | Small counterexample |
|---|---|---|
| Inputs | Any `str` code; exact, case-sensitive matching | Refuse the present code `"x"` because it is short |
| Result | Exact stored string, including an empty string | Trim a meaningful label or return a placeholder |
| Absence | Raise `UnknownCode` | Return `""` for a missing code |
| Error boundary | Clients can handle `UnknownCode` | Leak a storage `KeyError` instead |
| State/effects | Lookup does not change observable entries | Remove a key while returning its value |
| History | Contents remain the construction-time snapshot | A later alias edit changes a previously read value |

### How to read this visual

Read each row as one independently testable promise, then run the counterexample with a valid
caller. These are specifications for our synthetic API, not universal rules for every catalog.

### Key insight

Returning the correct Python type covers only a small part of this table.

### Simplification or limitation

Typed, cooperative callers; string keys and values; sequential calls; no I/O or process failure.
This is not an untrusted-input parser or a promise to survive resource exhaustion.

## 5. Collaboration and execution flow

1. Composition builds a catalog from `{"x": "parcel"}`.
2. The client makes a valid `lookup("x")` call.
3. The actual object executes its own implementation.
4. The client observes a result or documented exception.
5. The client, or another reference, reads again and still relies on the same contract.

Use the [interactive contract explorer](visuals/README.md) to step through the same catalog
calls with compatible and incompatible replacements. The explorer illustrates recorded
teaching scenarios; the Python tests are the executable checks.

## 6. Before-principle code and concrete pain

```python
entries = {"x": "parcel"}
first = entries["x"]
second = entries["x"]
assert (first, second) == ("parcel", "parcel")
```

This direct dictionary is enough when there is one owner and no replacement boundary. Adding
classes merely to say “SOLID” adds no value. The concrete pressure is a second representation
while preserving exact values, absence handling, and repeated reads.

The complete [teaching module](examples/catalog_contracts.py) contains two conforming providers
and four deliberately broken candidates. They all expose `lookup(code: str) -> str`:

- `RestrictedCatalog` rejects a valid short code.
- `BlankOnMissingCatalog` hides absence as a plausible string result.
- `ConsumingCatalog` returns the right value but removes the entry.
- `LeakyErrorCatalog` exposes an exception the client was not asked to handle.

These are solved teaching counterexamples. They are not the separate reservation-lab solution.

## 7. Minimal Pythonic and typed implementation

Use a small structural boundary when multiple providers are real. No concrete provider needs
to inherit from the protocol. The prose supplies the meaning absent from annotations.

```python
from collections.abc import Mapping
from typing import Protocol


class UnknownCode(LookupError):
    pass


class Catalog(Protocol):
    def lookup(self, code: str) -> str: ...


class SnapshotCatalog:
    def __init__(self, entries: Mapping[str, str]) -> None:
        self._entries = dict(entries)

    def lookup(self, code: str) -> str:
        try:
            return self._entries[code]
        except KeyError as error:
            raise UnknownCode(code) from error


def read_pair(catalog: Catalog, code: str) -> tuple[str, str]:
    return catalog.lookup(code), catalog.lookup(code)


source = {"x": "parcel"}
catalog = SnapshotCatalog(source)
source["x"] = "changed elsewhere"
assert read_pair(catalog, "x") == ("parcel", "parcel")
```

The copy is sufficient here because all keys and values are immutable strings; it would not
detach nested mutable values. Python's data model distinguishes object identity from value
and mutable from immutable objects. [Python data model, objects, values and types](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types).

The narrowly scoped `except KeyError` translates the lookup failure. A future adapter should
not wrap unrelated provider setup, decoding, and lookup in one large catch that mislabels bugs
as missing codes. An adapter is appropriate only when it can actually preserve this contract.

## 8. What typing can and cannot establish

Static structural typing compares the required members and their types. An implementation
need not explicitly inherit a protocol. A read-only protocol property restricts access through
that interface; it does not freeze the underlying object.
[Typing specification, protocols](https://typing.python.org/en/latest/spec/protocol.html).

`@runtime_checkable` supplies a presence check, not a check of signatures or semantics. In the
[shape experiment](experiments/EXP-01-shape-is-not-contract/README.md), one accepted object has
the wrong call arity; another accepts the call but returns the wrong integer. Ordinary methods
are used because dynamic-attribute lookup details changed in Python 3.12.
[Python typing documentation](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable).

### Input and output variance: a small bridge

A replacement callable must accept every argument combination the caller's expected signature
allows. Parameter types can therefore widen; return types can narrow. Parameter names, keyword
support, and defaults matter too, not just the number of arguments.
[Typing specification, callable assignability](https://typing.python.org/en/latest/spec/callables.html#assignability-rules-for-callables).

```python
from collections.abc import Callable


def describe(value: object) -> str:
    return str(value)


render: Callable[[str], str] = describe
assert render("ready") == "ready"
```

The replacement accepts all strings and more. Reversing that assignment would promise support
for arbitrary objects to a function that only accepts strings. A compatible return type still
does not prove that `render` returns the correct business value.

For containers, allowing a `list[InsuredParcel]` where a caller can mutate a `list[Parcel]`
would let the caller append a plain parcel. `list` is invariant; an appropriate read-only
`Sequence` interface can be covariant. Read-only access is not a snapshot or an ownership
guarantee. [Typing specification, variance](https://typing.python.org/en/latest/spec/generics.html#variance).

## 9. Simpler alternatives and when to reject substitution

| Design | Appropriate force | Cost or boundary |
|---|---|---|
| Direct dictionary lookup | One known representation; no replacement need | Dictionary errors and ownership remain part of that API |
| A passed lookup callable | One operation is the whole capability | Document semantics outside `Callable` too |
| Small `Catalog` protocol | Multiple real providers with one shared promise | Maintain prose and shared contract tests |
| An adapter using composition | Representation or error translation is genuinely possible | Cannot invent unavailable guarantees |
| Separate consuming API | Reading is intentionally destructive | Clients must opt into different behaviour |
| Universal base class with unsupported methods | No coherent shared operation | Speculative structure and runtime surprises |

### How to read this visual

Match the observed change pressure to a row; compare the obligation added by that choice.

### Key insight

A smaller honest boundary is preferable to a broad promise a provider cannot keep.

### Simplification or limitation

Conceptual design alternatives, not a ranking. Real provider guarantees determine feasibility.

Do not silently replace an established exact lookup with “best effort.” A weaker API can be a
valid **new** contract, but migrating callers is real work. A cache with allowed staleness is
not automatically a substitute for a current-value store. Conversely, clients cannot demand
ordering, identity, or timing that their abstraction never promised.

## 10. Invariants, history, and aliasing

Our counter experiment's invariant is `value >= 0`. Its separate history promise is that later
reads never decrease. `0 → 3 → 0` satisfies the invariant at every observed moment but breaks
the history promise. A subclass adds `reset()` without overriding `advance()` or `value`.
A second reference calls `reset()`; the original reader sees the change.

The [alias experiment](experiments/EXP-02-history-through-aliases/README.md) demonstrates this
with sequential calls, no threads, and no CPython memory claims. The result follows from shared
object identity and mutation. [Python data model](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types).

The property name `value` alone does not promise monotonicity. Our prose does. Under a different
contract that allowed resets, this particular reset would not violate that history promise.
Always state the contract before judging the class.

For another original thought experiment, a mutable display has `set_width(w)` promised to
leave height unchanged. A “square display” that updates both dimensions breaks that operation's
postcondition. Immutable dimensions exposed only for reading do not create this setter conflict.
The API's operations decide the answer, not the everyday meaning of “is a.”

## 11. Errors, effects, and production boundaries

Returning `None` instead of raising `UnknownCode` changes control flow as well as the result
domain. A new exception subtype can be compatible when the documented handler catches it and
its meaning and state guarantees remain valid; exceptions are not forbidden merely because
they are more specific. Python exception handlers match subclasses of the listed class.
[Python tutorial, handling exceptions](https://docs.python.org/3.14/tutorial/errors.html#handling-exceptions).

For a backend reservation boundary, distinguish “rejected without effects” from “the response
failed after allocation.” Retrying under the wrong assumption may allocate again. This is a
design risk to investigate, not an asserted behaviour of a particular service. Contracts should
identify allowed partial effects, retry rules, and the observable result of uncertain outcomes.
The separate [lab](practice/README.md) lets you investigate the small sequential version.

Private memoization may preserve the catalog's contract if callers cannot distinguish it within
the agreed observations. Logging, billing, timing, and provider calls may be relevant effects
in a real boundary. Decide explicitly which are contractual instead of claiming byte-for-byte
equivalence of every possible implementation detail.

Constructor signatures need not match merely because instances are substitutable. If clients
also substitute factories or classes, that construction interface needs its own contract.
Similarly, a synchronous result and an awaitable result are different calling obligations.

## 12. Refactoring path and debugging

1. Write the existing client's valid calls and observations, including its next call after failure.
2. Preserve the baseline with tests. Name any known bug separately from intended behaviour.
3. Find the smallest valid call sequence that breaks the proposed replacement.
4. Classify the lost promise; do not begin by moving methods into more classes.
5. Make the replacement honour the contract, adapt a genuinely translatable boundary, or reject
   the substitution and introduce an explicitly different operation.
6. Run the same contract suite for every admitted implementation, then test the changed requirement.
7. Remove class-name branches added merely to compensate for non-substitutability.

During diagnosis record the provider, operation, input category, result/error category, and
before/after public state. Avoid private customer data. A stack trace alone may miss an earlier
side effect; repeat-call and failure-then-recovery sequences expose it.

## 13. Testing strategy

| Check | Evidence it provides | What it does not prove |
|---|---|---|
| Static typing | Compatible signatures for analyzed code | Correct labels, effect safety, or history |
| Shared contract suite | Same observations for all admitted factories in tested cases | Every possible execution |
| Boundary cases | Empty values, missing codes, short codes, exact matching | A single happy path is representative |
| Generated cases | Broader dictionary/string combinations and monotone increments | A formal proof or production integration |
| Sequence tests | Repeated calls, failed calls, alias-visible changes | Concurrent or distributed atomicity |
| Adapter integration tests | Real provider error and state semantics | A fake's behaviour alone validates the provider |

### How to read this visual

For each check, separate the evidence it supplies from the conclusion it cannot justify.

### Key insight

Use complementary checks; no single green signal establishes the entire contract.

### Simplification or limitation

This is an evidence map, not a coverage measurement or a claim that integration tests ran here.

The [catalog tests](examples/test_catalog_contracts.py) apply the shared contract to two
conforming factories. Separate witness tests deliberately demonstrate why the four bad
candidates are not admitted. A green witness test means the violation was reproduced.
The practice tests establish only `SeatPool`'s baseline; they do not certify its partner.

### Runtime experiments

- [EXP-01 — Shape is not a contract](experiments/EXP-01-shape-is-not-contract/README.md): compare
  runtime presence, static signatures, and actual returned values.
- [EXP-02 — History through aliases](experiments/EXP-02-history-through-aliases/README.md): observe
  an added method breaking a promise through another reference.

These are maintainer-reproduced demonstrations. Learner predictions and explanations remain
unrecorded until you supply them.

## 14. Concurrency and performance limits

All supplied examples are sequential. A check followed by an update does not establish atomicity
for a real shared service. If the public contract includes concurrent reservations, choose and
test a synchronization or storage guarantee appropriate to that actual service. No concurrency,
transaction, load, or benchmark result is claimed here.

`TupleCatalog` demonstrates a different representation, not a performance recommendation.
Latency or memory limits matter to substitution when they are part of the agreed operational
contract; this unit has not measured them. Avoid treating an accidental microbenchmark result
as a universal requirement of LSP.

## 15. Related units, use, and misuse

| Unit | Connection | Distinction |
|---|---|---|
| [SDP-SOL-020](../../../CURRICULUM.md#sdp-sol-020) | Stable extension points | LSP asks whether the extension preserves the promise |
| [SDP-SOL-040](../../../CURRICULUM.md#sdp-sol-040) | Client-shaped capabilities | ISP asks what each client should depend on; LSP asks whether providers behave compatibly |
| [SDP-REF-040](../../../CURRICULUM.md#sdp-ref-040) | Fragile inheritance | Composition changes structure; behaviour still needs checking |
| [SDP-FND-090](../../../CURRICULUM.md#sdp-fnd-090) | Shared state and ownership | Aliases can reveal changes a single-call test misses |

Use this reasoning for provider replacements, test doubles, strategies, storage adapters, and
public subclass APIs. You do not need an inheritance hierarchy to have substitutability pressure.
Do not create a universal hierarchy when the actual capabilities differ.

Common traps are claiming `super()` proves correctness, silencing unexpected errors with defaults,
adding `isinstance` branches in every client, or weakening the original contract just to make a
new implementation “fit.” A broad `except Exception` that restores nothing is not rollback.
Rejecting a false substitution can be the correct design result.

## 16. Interview preparation and closed-book revision

Start with this one question and wait for the learner's answer:

> A replacement returns the same label on the first lookup but removes the entry. What exact
> promise could the original client use to demonstrate that the replacement is invalid?

After that answer, choose only one follow-up at a time: a narrower input domain, an unexpected
exception, an alias-visible reset, a mutable generic container, or a provider that cannot make
the requested operation atomic. Do not reveal a full answer before the attempt.

A strong answer identifies the client, contract, valid counterexample, first observable failure,
smallest repair or rejection, and a test that distinguishes the designs. “Child objects can
replace parents” without those details is incomplete. Missing reasoning should be diagnosed
specifically: for example, checking the return type but never checking the next call's state.

For delayed closed-book review, reconstruct the notebook visual, explain input/output direction,
contrast an invariant with a history promise, and transfer the idea to a new backend boundary.
Dates and progress change only after actual evidence satisfies [the tracker](../../../PROGRESS.md).

## 17. Vocabulary and professional English

| Word | Pronunciation | Simple meaning | Design use |
|---|---|---|---|
| Substitute | SUB-sti-toot | Use one thing in place of another | “This provider can substitute for the original under the same contract.” |
| Invariant | in-VAIR-ee-unt | A condition that stays true in legal states | “Available capacity must remain nonnegative.” |
| Postcondition | post-kun-DISH-un | A promise after an operation | “Failure has a postcondition too: the reservation state is unchanged.” |

In an interview, prefer “The caller supplied a valid request, but the replacement changed state
before rejecting it” to “This subclass is bad.” The first sentence names evidence.

## 18. Python Mastery references

Exact mappings from [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md):

- Hard: [PY-OBJ-010 — Classes, instances, methods, and construction](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-010).
- Hard: [PY-OBJ-020 — Properties, encapsulation, and composition](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-020).
- Hard: [PY-OBJ-030 — Inheritance, MRO, and super](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-030).
- Soft: [PY-TYP-030 — Generics and type variables](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-typ-030).
- Soft: [PY-TYP-040 — Variance and safe generic API design](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-typ-040).

The minimum object-model bridge is in section 1; the variance bridge is in section 8. These
cross-repository links identify prerequisite units, not sources read for this artifact.

## 19. Authoritative sources

Opened for this unit on 2026-08-30; explanations, scenarios, diagrams, and code are original.

1. Liskov and Wing, [A Behavioral Notion of Subtyping](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf), introduction and sections 4–5; formal definition and historical context.
2. Python 3.14, [typing: Protocol and runtime_checkable](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable); runtime-check scope and version caveat.
3. Python typing specification, [protocols](https://typing.python.org/en/latest/spec/protocol.html); structural members and read-only properties.
4. Python typing specification, [callable assignability](https://typing.python.org/en/latest/spec/callables.html#assignability-rules-for-callables); input/output direction and parameter kinds.
5. Python typing specification, [variance](https://typing.python.org/en/latest/spec/generics.html#variance); mutable containers and read-only interfaces.
6. Python 3.14, [data model](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types); identity and mutation.
7. Python 3.14, [handling exceptions](https://docs.python.org/3.14/tutorial/errors.html#handling-exceptions); exception-class matching.
8. Python 3.14, [super](https://docs.python.org/3.14/library/functions.html#super); method-resolution delegation.

The material's checks are recorded in [VALIDATION.md](VALIDATION.md), a maintainer record.
Publication does not mark the practice attempted or establish understanding. `SDP-SOL-040`
is the next requested unit and is not initialized here.
