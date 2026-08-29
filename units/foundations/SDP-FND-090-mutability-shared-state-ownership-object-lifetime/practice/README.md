# Practice — SDP-FND-090 Mutability, shared state, ownership, and object lifetime

| Field | Value |
|---|---|
| Unit note | [SDP-FND-090](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-090) |
| Evidence target | E+I+D+(X)+T |
| Attempt required before solution | Yes |
| Focused test command | `uv run pytest -q units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice` |
| Status | Not attempted |

The starter, characterization suite, and four controlled experiments have been run to verify the
artifact. That proves only that the supplied files execute as documented. It does **not** count as
Rahul's prediction, ownership analysis, refactoring attempt, trade-off explanation, or learning
evidence.

## Learning question

How can a cart component make mutation authority, observation semantics, state scope, and lifetime
explicit without deep-copying everything, hiding state in a Singleton, or adding locks before the
actual sharing boundary is known?

## Lab cycle

```text
predict → run → observe → explain → map aliases → define ownership → refactor → vary
```

Do not begin by changing `{}` to `None` and declaring the problem solved. That repairs one Python
mechanism while leaving live return aliases, nested input aliases, snapshot depth, deletion, and
concurrency contracts unresolved.

## Starter files

```text
practice/
├── README.md
├── cart_ownership_lab.py
├── test_cart_ownership_lab.py
├── default_argument_experiment.py
├── copy_depth_experiment.py
├── weakref_lifetime_experiment.py
├── lost_update_experiment.py
└── test_runtime_experiments.py
```

- `cart_ownership_lab.py` is the unsolved ownership refactoring starter.
- `test_cart_ownership_lab.py` characterizes validation and five deliberate alias/lifetime
  defects.
- `default_argument_experiment.py` isolates definition-time default reuse.
- `copy_depth_experiment.py` compares assignment, shallow copy, and deep copy.
- `weakref_lifetime_experiment.py` separates strong ownership from weak observation.
- `lost_update_experiment.py` forces one stale-read interleaving and compares a lock-owned
  transition.
- `test_runtime_experiments.py` makes all experiment results reproducible.

All carts, identifiers, SKUs, attributes, and runtime state are synthetic. The code performs no
network requests, accesses no credentials, and contains no production data.

## Problem

`CartStore` appears to provide a small in-memory cart API:

1. construct a store;
2. add a validated `CartLine`;
3. ask for a cart's lines;
4. take a snapshot;
5. delete a cart.

The signatures hide the most important state contracts:

- default-constructed stores share one dictionary created when the function was defined;
- an explicitly supplied dictionary is retained rather than copied or documented as transferred;
- `lines()` returns the live internal list and creates a missing cart as a read side effect;
- `add_line()` retains the caller's mutable `attributes` dictionary;
- the returned `CartLine` is the exact mutable object stored internally;
- `snapshot()` copies only the outer list;
- `delete()` removes one registry path but cannot invalidate aliases already returned;
- no owner or atomic operation exists for competing quantity changes.

These are not all solved by immutability. The learner must decide which sharing is required and
which contracts should become values, commands, or explicit ownership transfers.

## Current object and authority graph

```text
function definition
      │ owns once
      ▼
default carts dict <──────── CartStore A._carts
      ▲                              ▲
      └──────────────── CartStore B._carts
      │
      └── cart_id → live list ────────────────> lines() caller
                         │                          may append/remove
                         ▼
                    mutable CartLine ◀────────▶ returned add_line value
                         │
                         └── attributes dict <── caller-supplied dict
                                  ▲
shallow snapshot ──new outer list─┘ (nested objects still shared)
```

### How to read this visual

Begin at the default dictionary and follow identity arrows. Two stores reach one registry. Follow
the cart entry to the live list, then to the mutable line and nested attributes. The snapshot owns
a new outer list only; it still reaches the same line and attributes.

### Key insight

The starter has several ownership edges at different graph depths. Fixing the default dictionary
does not stop a caller from mutating stored state through the returned list, line, or nested input.

### Simplification or limitation

The diagram shows reference identity, not memory addresses. It omits garbage-collector roots,
threads, external storage, cache expiry, framework scopes, and the future API the learner must
design.

## Current deterministic behavior

Before refactoring, predict and then verify:

- two default-constructed stores observe the same cart registry;
- two stores given separate explicit dictionaries remain isolated;
- appending to the result of `lines()` changes store state without calling `add_line()`;
- clearing a shallow snapshot does not clear the owner's outer list;
- changing a line or its attributes through that snapshot changes owner-visible state;
- changing the caller's input attributes after `add_line()` changes stored state;
- changing the returned `CartLine` changes stored state;
- deleting a cart removes the registry entry but an old list alias still contains its lines;
- blank IDs/SKUs and non-positive quantities are rejected before a cart is created.

Treat the first seven observations as **defect characterizations**, not desired contracts. The
validation behavior is stable meaning to preserve.

## Change pressure

The next version must support request handlers that edit the same logical cart through an
application service while read-only consumers receive point-in-time cart summaries.

Required meaning:

1. default construction does not accidentally share state between owners;
2. intentional sharing is created explicitly at the composition boundary;
3. only the selected state owner performs mutations;
4. caller mutation of supplied input cannot silently change stored cart state;
5. observations are documented as either live views or independent snapshots;
6. a snapshot remains stable after later updates and deletion;
7. validation failure leaves state unchanged;
8. one quantity-change operation preserves the positive-quantity invariant as a complete
   transition;
9. the design states where coordination would move if several processes share durable carts.

Do not add persistence, a web framework, distributed locks, events, or a full checkout domain. The
lab is about ownership mechanics and judgment.

## Stable contract worksheet — complete before code changes

### Logical identity and scope

- What identifies one logical cart?
- Is the starter owner call-, request-, application-, or storage-scoped?
- Who constructs that owner?
- How would two request handlers intentionally reach the same logical cart?
- What must remain isolated between tests, tenants, or application instances?

### Mutation ownership

- Which component may add a line?
- Which component may change quantity?
- Which component may delete a cart?
- May a caller transfer a mutable object into the owner, or must input be normalized/copied?
- Which invariant spans read → decide → write?

### Observation

- Is a cart query live or point-in-time?
- What exact type should it return?
- Can the outer collection change?
- Can a contained line change?
- Can nested attributes change?
- Does observation create an empty cart or merely report absence?

### Lifetime and deletion

- What event begins a cart's logical lifetime?
- What does deletion guarantee to future queries?
- What may an already returned snapshot continue to show?
- Which owner-held reference must be removed?
- Would an expired cart differ from an explicitly deleted one?

### Concurrency

- Which competitors exist in the in-memory version?
- What is the entire quantity-change transition?
- Would confinement, immutable replacement, a lock, or a queue be simplest?
- Where must atomicity live after moving carts to a shared database?

Do not fill the worksheet with “use a tuple,” “use `deepcopy`,” or “add a lock.” State the contract
first; select mechanisms afterward.

## Required refactoring evidence

- Rahul's original prediction and object graph before the first run.
- The completed ownership worksheet.
- The first refactoring attempt preserved at a path or commit.
- A before/after alias-and-authority visual with arrow meanings.
- Independent default owners and explicit intentional sharing.
- No uncontrolled mutation path through input, returned line, query, snapshot, or nested
  attributes.
- A written snapshot-depth contract and tests that try to mutate every layer.
- Read operations without accidental state creation unless that side effect is explicitly chosen.
- Failure atomicity for validation and quantity changes.
- One deterministic competing-update test or a precise explanation of why confinement removes the
  competitor.
- A production transfer explaining where cross-process atomicity belongs.
- One rejected `deepcopy`, Singleton, weak-reference, or lock-based design with a concrete reason.
- Focused tests, static checks, and lint passing for the learner's final code.

Passing the supplied characterization tests unchanged is insufficient. Several assertions encode
the defects and should be replaced only after the intended contract is written.

## Required edge cases

- Empty store and unknown cart query.
- Blank and whitespace-only cart ID.
- Blank and whitespace-only SKU.
- Zero and negative quantity.
- One line and several lines.
- Repeated SKU with a stated merge-or-separate policy.
- Caller mutates the original attributes dictionary after adding.
- Caller attempts to mutate the returned outer collection.
- Caller attempts to mutate a returned line.
- Caller attempts to mutate nested attributes.
- Later owner update after an earlier snapshot.
- Deletion after an earlier snapshot.
- Failed update after earlier valid state.
- Two independently created owners in both test orders.
- Two intentionally sharing services, if that design is chosen.
- Two updates forced to derive from the same earlier quantity.

Do not add discounts, inventory reservation, payment, shipping, or persistence until the ownership
contract passes these cases.

## Commands

Run from the repository root through the locked environment:

```bash
uv run python \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice/cart_ownership_lab.py

uv run pytest -q \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice
```

Run the experiments individually:

```bash
uv run python \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice/default_argument_experiment.py
uv run python \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice/copy_depth_experiment.py
uv run python \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice/weakref_lifetime_experiment.py
uv run python \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice/lost_update_experiment.py
```

After refactoring:

```bash
uv run ruff check \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice

uv run mypy \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice
```

Record actual commands and output. Never describe a command as passed until it has run.

## Prediction before the first run

Write answers before executing anything:

1. Are `CartStore()` instances independent? Draw the binding that proves the answer.
2. Does `lines()` return a view, copy, snapshot, or live alias?
3. Which changes when `snapshot.clear()` runs: the snapshot, store, both, or neither?
4. Which changes when `snapshot[0].quantity = 8` runs?
5. What happens if the caller edits the dictionary passed as `attributes`?
6. What remains reachable through an old alias after `delete()`?
7. Which tests describe stable validation and which describe defects?
8. How many increments survive the forced unsafe concurrency experiment?

Record:

- Expected script output:
- Current object graph:
- Mutation authority paths:
- Lifetime owners:
- Defect-characterization tests:
- Stable tests:
- Reasoning:

## Artifact-verification observation

Do not copy these outputs into the prediction. On 2026-08-29, the supplied artifact was run with
CPython 3.14.7 on Linux x86_64.

Starter output:

```text
default_registry_shared=True
returned_line_quantity=9
snapshot_gift_wrap=yes
```

Focused test output:

```text
.................                                                        [100%]
17 passed in 0.11s
```

Timing is informational and may differ. The three behavior lines and pass count are the relevant
observations. Passing tests characterize the starter; they do not approve its design.

## Rahul's attempt

- Prediction:
- First run and actual output:
- First explanation:
- Current object graph:
- Intended ownership graph:
- State scope chosen:
- Observation contract:
- Copy/share/transfer decisions:
- Concurrency strategy:
- Attempt path or commit:
- Rejected alternative:
- Focused test result:
- Static/lint result:
- Remaining uncertainty:

## Refactoring checkpoints

### Checkpoint 1 — Mark every alias

For each object below, list all current reference paths and mutation paths:

| Object | Reference paths | Who can mutate today? | Intended owner |
|---|---|---|---|
| Default carts dictionary |  |  |  |
| Per-cart list |  |  |  |
| `CartLine` |  |  |  |
| Attributes dictionary |  |  |  |
| Shallow snapshot list |  |  |  |

Do not write only variable names. Include argument defaults, returned values, stored attributes,
and caller inputs.

### Checkpoint 2 — Choose the state scope

Choose one scope for the in-memory lab and justify it:

- one owner per call;
- one owner per request;
- one owner shared by selected application services;
- one durable owner outside the process.

If sharing is needed, show the composition boundary that creates it deliberately. Do not hide
sharing in a default, class attribute, module global, or Singleton constructor.

### Checkpoint 3 — Define commands and observations

Write the smallest operations clients need without exposing representation:

- add line:
- change quantity:
- remove line or cart:
- query absence:
- observe current cart:
- snapshot semantics:
- conflict/failure semantics:

Decide whether plain functions plus immutable values are enough before retaining a service class.

### Checkpoint 4 — Decide graph depth

For every input and output boundary, fill one choice:

| Boundary | Share | Shallow copy | Domain snapshot | Transfer | Reason |
|---|:---:|:---:|:---:|:---:|---|
| Caller attributes → owner |  |  |  |  |  |
| Owner → add result |  |  |  |  |  |
| Owner → cart query |  |  |  |  |  |
| Owner → historical snapshot |  |  |  |  |  |

Use `deepcopy()` only if its recursive semantics match the domain better than an explicit snapshot.

### Checkpoint 5 — Replace defect characterizations carefully

Preserve tests that prove:

- input validation;
- failure leaves no new cart;
- documented query behavior;
- chosen line/quantity invariants.

Replace tests that currently expect:

- default stores to share accidentally;
- `lines()` to expose a live mutable list;
- nested mutation through a shallow snapshot;
- caller input and returned line to mutate stored state;
- deletion to act as though escaped live aliases are canonical state.

Do not delete a failing test until its old observation and new contract are both recorded.

### Checkpoint 6 — Protect one complete transition

Define one quantity-change command. Identify:

1. read current quantity;
2. validate expected/current state;
3. calculate new quantity;
4. reject or commit;
5. return a value/version.

Then choose:

- confinement with no competitor;
- immutable replacement at one owner;
- one explicit lock around the entire transition;
- a queue-owned mutation loop;
- a durable transaction/version check for a production transfer.

Do not place a lock only around the dictionary read and another around the write.

## Progressive hints

No hints are populated yet. Request one hint at a time after preserving the original attempt.

## Experiment environment

All four controlled experiments below were reproduced in this environment:

```text
Date: 2026-08-29
Operating system: Linux 7.0.0-30-generic
Architecture: x86_64
Python version: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation: cpython
Dependencies: Python standard library only
Relevant flags: default GIL-enabled repository interpreter; no optimization flags
```

The source/version record is part of artifact reproducibility. It is not a portability claim about
collection timing, address reuse, scheduler behavior, or another Python implementation.

## Experiment 1 — Definition-time mutable default

| Field | Value |
|---|---|
| Precise question | Do two omitted-argument calls receive two lists or one definition-bound list? |
| Classification | Python language/tutorial mechanism |
| Status | Run and interpreted |

### Why observation is necessary

The dangerous code looks like ordinary per-call construction in a signature. Identity checks make
the hidden reuse directly visible.

### Hypothesis

> The default expression creates one list when the nested function is defined. Both calls append
> to and return that same object, so the first alias observes the second append.

### Controls and variables

- Controlled: one freshly defined function per experiment call, two fixed strings, no external
  state.
- Changed: call number and appended value.
- Measured: object identity and tuple snapshots of content.

### Reproduction command

```bash
uv run python \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice/default_argument_experiment.py
```

### Predicted result

```text
same_result_object=True
default_is_result_object=True
value_after_second_call=('first', 'second')
```

### Observed result

```text
first_value_before_second_call=('first',)
same_result_object=True
default_is_result_object=True
value_after_second_call=('first', 'second')
```

### Interpretation

1. Directly shown: both results and the function's stored default identify the same list.
2. Reasonable inference: omitted-argument calls share mutations through that list.
3. Not shown: every mutable default is a bug, how long an imported module remains alive, or that
   replacing `{}` with `None` fixes other alias leaks.

### Visual interpretation

```text
definition ─creates once─> default list
                              ▲      ▲
call 1 ─omits argument────────┘      └────────call 2 ─omits argument
             append first      same object      append second
```

#### How to read this visual

Both call arrows end at the object created during definition. Each append changes that object.

#### Key insight

The accidental lifetime begins at function definition, not at each call.

#### Simplification or limitation

The experiment defines the function inside the observation function to keep repeated test runs
isolated. A module-level function can retain its default for a much longer module lifetime.

### Design conclusion

Use a sentinel/per-call construction for independent state, or name and inject an intentionally
shared owner. A signature default is a poor hidden cache boundary.

### Source

Python 3.14.7 Tutorial,
[“Default Argument Values”](https://docs.python.org/3.14/tutorial/controlflow.html#default-argument-values).

## Experiment 2 — Assignment, shallow copy, and deep copy

| Field | Value |
|---|---|
| Precise question | Which outer and nested identities are shared after assignment, `copy()`, and `deepcopy()`? |
| Classification | Python standard library |
| Status | Run and interpreted |

### Why observation is necessary

Printing only equality can hide distinct outer objects and shared nested objects. The experiment
checks identity at each graph layer and then mutates one nested list.

### Hypothesis

> Assignment reuses the outer list; a shallow copy creates a new outer list but reuses nested
> lists; a deep copy creates detached nested lists for this acyclic built-in graph.

### Controls and variables

- Controlled: one two-level list graph containing strings, one nested append.
- Changed: copy operation.
- Measured: outer identity, nested identity, and nested values after mutation.

### Reproduction command

```bash
uv run python \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice/copy_depth_experiment.py
```

### Predicted result

```text
assignment_is_original=True
shallow_is_original=False
shallow_first_step_is_original=True
deep_first_step_is_original=False
```

### Observed result

```text
assignment_is_original=True
shallow_is_original=False
shallow_first_step_is_original=True
deep_first_step_is_original=False
original_first_step=('pick', 'scan')
shallow_first_step=('pick', 'scan')
deep_first_step=('pick',)
```

### Interpretation

1. Directly shown: shallow copy detaches outer membership but not the first nested list; deep copy
   detaches that nested list in this graph.
2. Reasonable inference: a snapshot contract must identify the graph depth that later mutation
   cannot cross.
3. Not shown: `deepcopy()` is suitable for arbitrary domain objects, external resources, recursive
   graphs, shared identities, or performance-sensitive workloads.

### Visual interpretation

```text
assignment ───────────────┐
original ───────────────> outer A ─────> nested X ─────> "pick"
                          ▲                 ▲
shallow ───────────────> outer B ──────────┘

deep ──────────────────> outer C ─────> nested Y ─────> "pick"
```

#### How to read this visual

Assignment and `original` reach the same outer object. `shallow` reaches a new outer object but the
same nested object. `deep` reaches a separately copied nested object for this example.

#### Key insight

Copy depth is an object-graph fact, not a property implied by the word “copy.”

#### Simplification or limitation

The graph is acyclic and uses only built-in lists and immutable strings. User-defined copy hooks,
resources, recursive graphs, and intentionally shared objects can behave differently.

### Design conclusion

Prefer an explicit domain snapshot when callers need a stable meaning. Choose shallow copy when
shared elements are deliberate; do not automatically escalate to deep copy.

### Source

Python 3.14.7 Standard Library,
[`copy` — shallow and deep copy operations](https://docs.python.org/3.14/library/copy.html).

## Experiment 3 — Strong registry ownership versus weak observation

| Field | Value |
|---|---|
| Precise question | Does a strong registry keep an object alive after its local name is deleted, and does a weak reference do so alone? |
| Classification | Python standard library plus implementation-sensitive lifetime observation |
| Status | Run and interpreted |

### Why observation is necessary

Deleting one name is often mistaken for deleting the object. The experiment keeps a weak observer
while adding and then removing one explicit strong registry edge.

### Hypothesis

> Removing the local name will not end lifetime while the registry strongly references the
> session. After the registry releases its reference and collection is requested, the weak
> observer will report no live referent.

### Controls and variables

- Controlled: one plain user-defined object, one weak reference, explicit `gc.collect()` calls.
- Changed: presence of the strong registry entry.
- Measured: whether calling the weak reference returns a live object or `None`.

### Reproduction command

```bash
uv run python \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice/weakref_lifetime_experiment.py
```

### Predicted result

```text
alive_while_strongly_registered=True
dead_after_strong_owner_releases=True
```

### Observed result

```text
alive_while_strongly_registered=True
dead_after_strong_owner_releases=True
```

### Interpretation

1. Directly shown: the registry reference kept the referent observable after the local name was
   removed; the weak reference alone did not keep it alive after explicit release and collection.
2. Reasonable inference: caches, callbacks, and registries participate in object lifetime through
   their strong references.
3. Not shown: exact finalization timing without `gc.collect()`, behavior of every Python
   implementation/type, resource cleanup correctness, or a complete cache eviction policy.

### Visual interpretation

```text
phase 1: registry ─strong─> Session <─weak─ observer    alive
phase 2: registry.clear()   Session <─weak─ observer    eligible
phase 3: collection         None    <─weak─ observer    dead
```

#### How to read this visual

Only the strong arrow owns reachability. The weak arrow can observe while the target lives but
does not preserve it by itself.

#### Key insight

Deleting one name is not an ownership policy; every strong reference path matters.

#### Simplification or limitation

The object has no cycle, external resource, finalizer, or concurrent access. Explicit collection
makes this a controlled observation rather than a claim about normal collection timing.

### Design conclusion

Use weak references only when an auxiliary relationship should not own lifetime. Prefer explicit
logical expiry and deterministic resource cleanup for domain state and resources.

### Sources

1. Python 3.14.7 Standard Library,
   [`weakref` — weak references](https://docs.python.org/3.14/library/weakref.html).
2. Python 3.14.7 Language Reference,
   [“Objects, values and types”](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types).

## Experiment 4 — Forced lost update and lock-owned transition

| Field | Value |
|---|---|
| Precise question | Can two accepted read-modify-write operations lose one increment, and does one lock around each whole transition preserve both? |
| Classification | Python standard library threading experiment |
| Status | Run and interpreted |

### Why observation is necessary

A final assignment may be individually safe while the business operation “read, add, write” is not
atomic. A barrier forces both unsafe workers to derive from the same stale read without depending
on scheduler luck.

### Hypothesis

> Both unsafe workers read zero and each writes one, leaving one accepted update. The lock-owned
> version admits one complete transition at a time and leaves two.

### Controls and variables

- Controlled: two threads, one integer-valued dictionary, deterministic barrier, no sleeps.
- Changed: no synchronization versus one `Lock` around read and write.
- Measured: final quantity.

### Reproduction command

```bash
uv run python \
  units/foundations/SDP-FND-090-mutability-shared-state-ownership-object-lifetime/practice/lost_update_experiment.py
```

### Predicted result

```text
unsafe_expected_if_both_counted=2
unsafe_observed=1
locked_observed=2
```

### Observed result

```text
unsafe_expected_if_both_counted=2
unsafe_observed=1
locked_observed=2
```

### Interpretation

1. Directly shown: the forced stale-read ordering loses one update; the selected lock boundary
   preserves two in this process.
2. Reasonable inference: synchronization must cover the whole invariant transition rather than
   isolated container operations.
3. Not shown: race probability, lock performance, fairness, deadlock freedom in a larger design,
   async behavior, or cross-process/database safety.

### Visual interpretation

```text
unsafe                        locked

A read 0                      A lock → read 0 → write 1 → unlock
B read 0                      B lock → read 1 → write 2 → unlock
A write 1
B write 1
final 1                       final 2
```

#### How to read this visual

The unsafe side permits both reads before either write. The locked side serializes each whole
transition.

#### Key insight

The protected unit is the business transition, not the dictionary assignment.

#### Simplification or limitation

The experiment intentionally forces one interleaving and one lock. It does not recommend a lock
over confinement, a queue, immutable replacement, or a database transaction for every design.

### Design conclusion

First avoid sharing when possible. If in-process threads truly share the state, give one owner a
lock over the complete invariant. Move protection to a durable boundary when other processes
compete.

### Sources

1. Python 3.14.7 Standard Library,
   [`threading` lock objects](https://docs.python.org/3.14/library/threading.html#lock-objects).
2. Python 3.14.7 HOWTO,
   [“Python support for free threading — Thread safety”](https://docs.python.org/3.14/howto/free-threading-python.html#thread-safety).

## Observe and explain

After running the starter and experiments, explain without reading the canonical note:

1. Which names alias each object in the starter?
2. Which object is created at function definition time?
3. Why does a new outer list not detach its lines?
4. Why does deleting one dictionary entry not invalidate an old alias?
5. Which strong reference keeps the session alive?
6. What does the weak reference prove and not prove?
7. Which steps form the unsafe quantity transition?
8. Where should synchronization live with two processes?
9. Which defect can be fixed with ordinary local construction?
10. Which defect needs a new public contract rather than a syntax change?

## Vary

After the core refactoring passes, choose exactly one variation:

### Variation A — optimistic version

Add a cart version and require a quantity-change command to state the version it observed. Force a
stale update and return an explicit conflict without partial mutation.

### Variation B — intentional shared owner

Build two application services that intentionally receive one owner from a composition function.
Prove that services share the selected cart while two separate composition roots remain isolated.

### Variation C — expiring carts

Add an explicit clock dependency and expiry policy. Prove observation does not silently refresh
expiry, cleanup removes the owner's reference, and an earlier snapshot remains a stable value.

Do not combine all variations. The purpose is transfer of the ownership model, not feature volume.

## Review rubric

| Area | Strong evidence | Weak evidence |
|---|---|---|
| Object graph | Every outer/nested alias and owner edge is drawn | “Lists are references” |
| Scope | Lifetime matches one stated use case | Global/application scope chosen for convenience |
| Mutation | Commands preserve named invariants | Private fields plus leaked live getters |
| Observation | View/snapshot semantics and depth are tested | Tuple or frozen label without nested analysis |
| Copying | Copy/share/transfer choice justified per boundary | `deepcopy()` used as an ownership substitute |
| Deletion | Future queries and earlier snapshots have defined meaning | Assumes `del` invalidates all aliases |
| Concurrency | Complete transition and real competitor named | GIL or one dictionary call cited as safety |
| Production transfer | Atomicity moves to the shared durable boundary | Process lock proposed for all workers |
| Simplicity | Local values/confinement considered first | Singleton, repository, and locks added together |
| Explanation | Design, Python, standard-library, and CPython claims separated | One experiment generalized to all runtimes |

## Troubleshooting

- Run commands from the repository root so direct practice-module imports resolve as they do for
  existing units.
- If mutable-default tests influence later tests, give tests explicit `{}` registries except where
  the default defect itself is under observation.
- If a concurrency test hangs, inspect barrier participant count and make sure every started thread
  reaches the barrier or failure is propagated.
- If mypy rejects a deliberate mutation, do not silence the type checker broadly; distinguish the
  unsolved starter from the learner's final value types.
- If a frozen dataclass still exposes mutation, inspect every nested field rather than adding more
  `frozen=True` wrappers.
- If `deepcopy()` fails or produces surprising identity, reduce the graph and inspect custom copy,
  pickle, resource, and recursive-object behavior.
- If a weak-reference result differs, record implementation/version/type and collection controls;
  do not rewrite the observation as a language-wide timing guarantee.
- If a proposed lock does not protect another process, move the invariant to the database,
  coordinator, or protocol boundary.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Original attempt preserved at:
- Ownership worksheet:
- Before/after object graphs:
- Focused test result:
- Static/lint result:
- Variation result:
- Rejected alternative:
- Production transfer:
- Trade-offs:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
