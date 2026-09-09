# SDP-BEH-020 — State

## Physical Notebook Core

### Problem or change pressure

A review packet accepts pages while editing, rejects them when sealed, and becomes permanently
closed after release or cancellation. Adding reopening makes the same event mean different things
at different times. Repeating phase checks across editing, release, and cancellation spreads the
lifecycle rules and makes it easy to allow an impossible transition.

### One-sentence mental model

> Keep one current behavior object; let it decide a legal next state, then let its owner commit it.

### One essential visual

```text
start -> EDITING --SEAL [pages > 0]--> SEALED --RELEASE [gate returns]--> RELEASED
            ^                           |
            +----------REOPEN-----------+
EDITING ----CANCEL----> CANCELLED <----CANCEL---- SEALED
EDITING --ADD [total ≤ 20]--> EDITING
```

### How to read this visual

Follow a named event from its current phase to its next phase. Brackets are guards that must pass.
RELEASED and CANCELLED have no outgoing events. Both CANCEL arrows have the same destination.

### Key insight

A valid event name does not imply a legal event **now**. The current state and its data decide.

### Simplification or limitation

This is a conceptual lifecycle, not a network protocol or a memory diagram. Input checks, revision
numbers, exceptions, and gate side effects are omitted. The exhaustive table below supplies them.
No browser rendering is required or claimed.

### Governing rules or invariants

1. One Packet owns one current state. Clients send events; they cannot install arbitrary phases.
2. Only editing can add pages. Sealing/releasing requires 1–20 pages; other phases preserve pages.
3. A successful event increments revision once. Rejection or a pre-commit exception preserves the
   same snapshot. That promise covers local state, not arbitrary callback effects.

### Minimal Python example

```python
from state import Event, InvalidTransition, Packet, Phase

packet = Packet()
packet.handle(Event.ADD, 2)
sealed = packet.handle(Event.SEAL)
try:
    packet.handle(Event.ADD, 1)
except InvalidTransition:
    assert packet.snapshot is sealed
assert packet.handle(Event.RELEASE).phase is Phase.RELEASED
```

Run imported snippets with `examples/` on `PYTHONPATH`; reproduction commands are below.

### One common misconception

**Mistake:** An enum, any conditional, or a strategy setter automatically implements State.

**Correction:** An enum names values. State organizes behavior around an object's evolving
lifecycle. A tiny conditional may already express that lifecycle better than four classes.

### Important trade-offs

- Local rules become easier to find, but the overall graph becomes distributed across states.
- Returning a candidate makes the commit boundary visible; it cannot undo an external effect.

### Interview-revision cues

- Trace the same event before and after a transition.
- Name who decides the successor and who is allowed to install it.
- Prefer a small table when transitions are regular and contain little behavior.

## Unit metadata

| Field | Value |
|---|---|
| Domain | GoF behavioral patterns |
| Curriculum | [SDP-BEH-020](../../../CURRICULUM.md#sdp-beh-020) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Move state-dependent behaviour behind explicit state transitions, preserving invariants and avoiding giant conditional dispatch. |
| Hard prerequisites | [SDP-FND-090](../../../CURRICULUM.md#sdp-fnd-090), [SDP-PYT-060](../../../CURRICULUM.md#sdp-pyt-060), [SDP-BEH-010](../../../CURRICULUM.md#sdp-beh-010) |
| Soft prerequisites | None specified |
| Priority | Core |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D3 |
| Scope | GoF, Behavioral, Python |
| Size | L |
| First understanding | 4–6 h |
| Hands-on practice | 5–9 h |
| Evidence profile | E+I+D+X+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Approved |

The frequency labels are curriculum judgments, not measured prevalence. Artifact approval and
learning completion are separate. The prerequisites have authored notes; no learner mastery is
assumed here.

## 1. Simple explanation and prerequisite bridge

Imagine a folder on a review desk. While you assemble it, adding a page is normal. Once you seal it,
adding that same page is a mistake. Reopen it first. Once released, this particular folder cannot
be edited again. The **object remains the same folder**; what it permits changes.

The context is that long-lived folder. Its state object answers “what can happen now?” This unit
keeps each state value immutable and lets the context replace it. A saved snapshot still describes
the earlier moment; it does not become a live view of the latest state.

The smallest prerequisite bridge is:

- **SDP-FND-090:** know who owns a mutable reference. Two aliases to Packet see later transitions;
  an alias to an old immutable Snapshot remains an old observation.
- **SDP-PYT-060:** an enum gives named alternatives; a frozen dataclass groups values with normal
  field assignment disabled. Use immutable fields if you need an immutable snapshot.
- **SDP-BEH-010:** delegation routes work through a contract. Here the delegation target follows
  lifecycle events instead of a selected ordering policy.

No Python class mutation is needed. `type(packet)` remains Packet throughout its lifetime.

## 2. Begin with the direct design

For a two-phase rule, use the simplest honest implementation:

```python
from enum import Enum


class Phase(Enum):
    EDITING = "editing"
    SEALED = "sealed"


def add_page(phase: Phase, pages: int) -> int:
    # Typed enum and exact integer 0..19 are this small sketch's preconditions.
    if phase is not Phase.EDITING:
        raise ValueError("reopen before editing")
    return pages + 1


assert add_page(Phase.EDITING, 2) == 3
```

This sketch only explains one operation; the runnable Packet enforces its full input domain.
Now add reopening, release admission, cancellation, and terminal behavior. If `add`, `seal`,
`release`, and `cancel` each repeat a growing phase switch, a new phase can be accepted by one
operation and forgotten by another. The real pain is scattered lifecycle knowledge, not the
presence of the word `if`.

Before refactoring, write the event/phase matrix. It may reveal that one small enum function or a
transition table is still sufficient. This example deliberately remains small enough to compare;
State classes earn their cost when phase-local rules and data grow together across operations.

## 3. Verified intent and original context

Gamma, Helm, Johnson and Vlissides describe State as changing an object's observable behavior as
its internal state changes. Their catalog assigns the client interface and current state reference
to Context, a common behavior interface to State, and phase-specific behavior to ConcreteState.
Requests delegate to the current state. Either the context or concrete states can decide successors.
The catalog also discusses table-driven alternatives and the coupling between states that name
one another. These are design relationships, not a guarantee of Python transaction safety.
[GoF catalog, State: intent, participants, collaborations and implementation](https://people.csail.mit.edu/addy/pattern/pat5h.htm).

That State section was opened and read through an MIT-hosted HTML reproduction. The authors'
pre-book catalog summary also identifies State and distinguishes Strategy and Template Method.
[GoF authors' paper, catalog summary](https://doczz.net/doc/6456109/erich-gamma---richard-helm---ralph-johnson---john-vlissides).
This is not a claim of reading the entire book; no source diagram or example is reproduced here.

Our Python interpretation uses structural typing, frozen state values, a returned successor and a
separate commit boundary. Those are choices for the synthetic packet. They are not extra conditions
in the historical pattern definition. Formally, the useful seam is **state-dependent behavior**,
with explicit control over how a state transition changes the context's future responses.

## 4. Participants and collaboration

| Role | Implementation here | Owns | Must not own |
|---|---|---|---|
| Client | Caller of `Packet.handle` | Event request | Direct installation of a state |
| Context | `Packet` | Current state/snapshot, revision, validation, gate and commit | A giant switch on concrete state type |
| State contract | `PacketState` Protocol | Read-only phase/pages and `handle` shape | Runtime proof of semantic correctness |
| Concrete states | `Editing`, `Sealed`, `Released`, `Cancelled` | Local rules and successor proposal | Mutating the context or calling external services |
| Release gate | Synchronous `ReleaseGate` callable | Accept by return, veto by raising | Claiming the proposal is already committed |
| Observation | Frozen `Snapshot` | Phase, page count and revision at one moment | A live mutable view or durable event log |

```text
caller -> Packet.handle(RELEASE)
  validate request; mark this context busy
  current Sealed.handle(RELEASE, 0) -> Released(same pages)
  build candidate snapshot with revision + 1
  gate(candidate snapshot)         [Packet.snapshot still SEALED]
      raises -> leave current unchanged; clear busy; propagate exception
      returns -> replace _current with candidate; clear busy; return snapshot
next request -> delegates to Released -> rejects every event
```

### How to read this visual

Read down one synchronous call. The candidate is prepared before the gate. Only the return path
installs it. The next request uses the newly installed behavior.

### Key insight

**Decision ownership and commit ownership differ:** the state chooses a legal successor; Packet
alone installs it. A pure successor does not become current just because it was constructed.

### Simplification or limitation

This conceptual trace assumes one serialized owner and ordinary execution. It is not a lock, a
crash-recovery protocol, or an event loop. No callback runs between local commit and return.

## 5. Exact runnable contract

The complete original implementation is [state.py](examples/state.py); the human-readable trace is
[run_state_demo.py](examples/run_state_demo.py). The packet represents local review admission only.
“Released” does not mean a file was uploaded, a message delivered, or a transaction committed.

| Current phase | ADD(n) | SEAL | REOPEN | RELEASE | CANCEL |
|---|---|---|---|---|---|
| EDITING | EDITING, add n if total ≤ 20 | SEALED if pages > 0 | Reject | Reject | CANCELLED |
| SEALED | Reject | Reject | EDITING | RELEASED if gate returns | CANCELLED |
| RELEASED | Reject | Reject | Reject | Reject | Reject |
| CANCELLED | Reject | Reject | Reject | Reject | Reject |

### How to read this visual

Choose the current row and requested event column. Each accepted cell is an edge; every Reject
cell raises `InvalidTransition` after argument validation. A failed page guard raises `ValueError`.

### Key insight

Terminal means no outgoing events in this contract, including repeated RELEASE/CANCEL. Repeating
an event is not silently idempotent. ADD is a self-transition with changed data and revision.

### Simplification or limitation

The table specifies behavior, not implementation inheritance. It has no time, permissions,
network acknowledgement, delivery retry, automatic transition, or restoration path.

**Input domain.** Construct Packet normally and call `handle` with an Event member. ADD needs an
exact built-in integer in 1–20; the resulting total must also fit. Other events accept only exact
integer zero, including the default. Strings, bools, floats, and malformed arguments are rejected.
Nested calls on the same Packet are rejected before argument checks. In a non-nested call,
argument validation precedes phase dispatch: invalid RELEASE arguments fail even in EDITING.

**Initial and terminal values.** A new Packet starts EDITING with zero pages and revision zero.
Empty cancellation is allowed. Sealed and Released values require nonzero pages; Editing and
Cancelled permit zero. Every transition except ADD preserves pages. Reopening preserves existing
pages and permits further additions within the bound. No event removes pages.

**Observation.** Every accepted event returns the exact new Snapshot also available through the
property, and increases revision by one. Rejection and ordinary exceptions before assignment keep
the exact previous Snapshot object. The context keeps no history list; callers may retain snapshots.
The revision is a local count of accepted events, not a timestamp or globally unique identifier.

**Trusted collaborators.** Packet constructs only its own concrete states; it accepts no arbitrary
initial state or state plugin. The Protocol is a type-checking boundary for maintainers. Direct
state `handle` calls assume arguments already validated by Packet and do not offer its revision,
reentrancy, or release-gate guarantees. `Snapshot` construction itself is an ordinary typed value
constructor, not an untrusted-input validator. Gate implementations must honor the synchronous
`Callable[[Snapshot], None]` contract; return values are ignored. Runtime code does not prove a gate
is synchronous or harmless. No mutation of private fields, class attributes or frozen internals is
supported as a client API.

```python
from state import Event, Packet, Phase, Snapshot

packet = Packet()
first = packet.handle(Event.ADD, 3)
packet.handle(Event.SEAL)
packet.handle(Event.REOPEN)
assert first == Snapshot(Phase.EDITING, 3, 1)
assert packet.snapshot == Snapshot(Phase.EDITING, 3, 3)
assert first is not packet.snapshot
```

## 6. Why these Python forms exist

The smallest view of the delegation is executable on its own:

```python
from state import Editing, Event, PacketState, Phase

current: PacketState = Editing(2)
previous = current
candidate = current.handle(Event.SEAL, 0)
assert previous.phase is Phase.EDITING
current = candidate
assert current.phase is Phase.SEALED
assert previous.pages == current.pages == 2
```

This lower-level sketch uses valid arguments and omits Packet's gate, revision and busy guard.
Notice that returning a successor does not mutate the old value. The complete context bundles its
successor and new snapshot into `_Current` so they are installed together through one reference.
That is a local representation choice, not proof of thread or crash atomicity.

`Editing.handle` answers its local event questions and constructs the next immutable state. It
uses ordinary `if` statements; State removes a switch *over all phases* from the context, not all
conditions from the program. The sealed state groups reopening, release and cancellation rules.
The two terminal classes give those endpoints explicit rejection behavior. This tiny implementation
could combine their mechanics; retaining separate named types makes the four roles inspectable.

Frozen dataclasses generate ordinary value operations and reject normal field assignment; they do
not recursively freeze arbitrary referenced containers or validate field types. Our state payloads
and snapshots use only enums and integers. Equality is useful for tests; identity distinguishes
an unchanged snapshot after failure. No singleton, metaclass, registry or class factory is needed.
[Python 3.11 dataclasses](https://docs.python.org/3.11/library/dataclasses.html),
[Python 3.14 dataclasses: frozen instances](https://docs.python.org/3.14/library/dataclasses.html#frozen-instances).

The read-only Protocol properties allow concrete dataclass attributes to satisfy the contract
without inheritance. Method parameters are positional-only so implementation parameter names do
not form a keyword API. Type compatibility does not establish allowed transitions, page preservation,
or lack of effects. These need behavioral checks.
[Typing specification: protocols and assignability](https://typing.python.org/en/latest/spec/protocol.html).

The gate is a function seam because one operation is enough. If one lifecycle phase later needs a
coherent group of operations with phase-local data, a state object remains a reasonable boundary.
Do not ship an ABC hierarchy, a registry of factories, and callable adapters just to display patterns.

All code uses 3.11 syntax. Python 3.14 normally defers annotation evaluation; the code does not
inspect annotations for runtime admission. Dataclasses still processes its fields. Both runtimes
are checked. The 3.13+ change to generated dataclass equality can matter for unusual non-reflexive
fields such as NaN; our enum/integer fields avoid that case.
[3.14 annotation changes](https://docs.python.org/3.14/whatsnew/3.14.html#pep-649-pep-749-deferred-evaluation-of-annotations),
[dataclass equality change](https://docs.python.org/3.14/library/dataclasses.html#dataclasses.dataclass).

## 7. A smaller alternative and a refactoring path

For a regular graph with no phase-specific calculation, a table is excellent:

```python
from enum import Enum


class Mode(Enum):
    EDITING = "editing"
    SEALED = "sealed"


edges = {(Mode.EDITING, "seal"): Mode.SEALED, (Mode.SEALED, "reopen"): Mode.EDITING}


def advance(mode: Mode, event: str) -> Mode:
    try:
        return edges[mode, event]
    except KeyError as error:
        raise ValueError("forbidden transition") from error


assert advance(Mode.EDITING, "seal") is Mode.SEALED
```

This deliberately models only phase movement. It does not implement Packet's page guards or gate.
A dictionary of pure functions can also return successor data. When rows all do the same operation,
use data. When states carry coherent changing behavior, state objects can make that behavior local.
A table with guard/action callables is a valid middle option; Python does not require choosing
between an unmaintainable switch and a class for every label.

Refactor incrementally:

1. Characterize the matrix, error categories, data invariants and effect ordering before moving code.
2. Find one duplicated phase rule. If there is none, keep the direct design unless another force exists.
3. Separate “decide successor” from “install successor”; move one phase's behavior behind a contract.
4. Delegate from the original context while preserving its public event API and error semantics.
5. Move the remaining phase-local rules; retain validation and common commit policy in the context.
6. Test the new requirement across every state, including forbidden transitions and terminal states.
7. Review whether the new abstractions reduce change cost. Remove speculative factories and hooks.

Adding a state still requires updating incoming edges, the model, tests, and possibly persistence.
It is not guaranteed to require edits only to a new class. Adding an event may touch many states.

## 8. Failures, reentrancy and the controlled observation

A release gate can check a synthetic rule and reject. Packet prepares the successor first, calls the
gate once, and installs the candidate only if it returns. It neither retries nor substitutes a
fallback. The same exception object propagates. A `finally` block clears the busy flag on exit;
that cleanup is not state rollback. Python's try/finally semantics explain this cleanup boundary.
[Language reference: finally](https://docs.python.org/3.14/reference/compound_stmts.html#finally-clause).

There are no entry/exit hooks in this sample. If you introduce them, define whether they run
before or after installation and whether they may send another event. A failing exit hook before
commit can preserve local state while leaving an effect; a failing entry hook after commit cannot
honestly report that nothing changed. Prefer returning a value describing intended work when that
keeps the boundary clear. Do not silently execute another transition from a hook.

A gate may inspect the candidate while `packet.snapshot` still describes SEALED. A gate calling
`packet.handle(CANCEL)` reenters the same object. We reject this nesting. If the gate lets that
exception escape, the outer release also fails. If it deliberately catches the exception and
returns normally, the outer release succeeds. Reads and operations on a different Packet are
allowed. This is an explicit local policy, not a universal rule for the State pattern.

[EXP-01 — transition boundary](experiments/EXP-01-transition-boundary/README.md) compares four
controlled cases: return, raise before effect, record then raise, and nested event. Its executable is
[observe_boundary.py](examples/observe_boundary.py). The experiment records actual outputs and
shows why “the state stayed sealed” is insufficient evidence that “nothing happened.”

A callback that records an external effect and then raises leaves that effect in place even though
Packet preserves its old snapshot. A caller retry could repeat the effect. Prefer a pure admission
gate here. Actual release delivery belongs in a separately designed durable boundary with an
explicit idempotency/reconciliation policy; the unit implements none of that infrastructure.

## 9. State safety and production transfer

One owner must serialize access to each Packet, including reads. `_handling` detects synchronous
reentrancy; it is not a lock and must not be described as thread safety. Python provides locks for
synchronization, and free-threaded builds change execution possibilities. Neither a GIL nor a
single `_current` assignment makes read/decide/callback/commit a transaction.
[Python threading: locks and GIL considerations](https://docs.python.org/3.14/library/threading.html).
No threaded, asynchronous, free-threaded, crash-recovery or database experiment was run.

In a backend, the State seam can live within one loaded review aggregate. Persist a stable phase
code, payload and version, rather than a Python class name. Professional design inference: make
concurrent updates conditional on the expected persisted version, and make any durable outgoing
work participate in an appropriate transaction. An in-memory revision alone cannot reject a stale
request across processes. Restoration would need schema validation and a deliberate constructor;
this Packet has no load-from-storage API.

For a transfer exercise, consider two workers submitting RELEASE and CANCEL against revision 8.
State legality alone is insufficient: both may read SEALED. Name the storage operation that allows
only one winner, the loser response, and how delivery is reconciled after a crash. Do not answer
“add a State class” or “use the GIL.” This is a design prompt, not implemented production evidence.

At a real boundary, record an entity reference, old phase/version, event, proposed phase, accepted
version and error category. Distinguish attempted from committed transitions. Avoid logging document
contents. Snapshot equality supports diagnosis but is not an audit log. A gate error may need a
separate effect identifier to reconcile uncertain work; revision alone is not one.

The sample does bounded page-count work and stores no page contents or history. Each success
allocates successor/snapshot/frame values. Saved snapshots remain alive while callers retain them.
No throughput, memory-saving, lookup-versus-dispatch, or speed comparison is claimed. Measure the
actual workload before optimizing; lifecycle clarity is the reason for this example.

## 10. Testing and debugging

| Layer | Evidence | Limit |
|---|---|---|
| Transition matrix | Every one of 4 × 5 state/event combinations at valid input | Does not cover every page count |
| Guards and input | Empty seal, full capacity, overflows, bool/type checks, argument precedence | Trusted typed gate contract remains a precondition |
| Stateful traces | Bounded generated sequences compared with an independent enum model | Sampled traces are not exhaustive proof |
| Failure boundary | Gate invocation count, identical old snapshot, exception identity, recovery after failure | Does not undo effects |
| Reentrancy | Uncaught rejection, caught rejection, other-context independence | No concurrent-access guarantee |
| Static clients | Positive clients and ten exact negative diagnostics for 3.11/3.14 targets | Signatures do not prove invariants |
| Experiment output | Four deterministic traces checked as observable contracts | Synthetic in-memory effects only |
| Practice | Baseline reservation behavior | Passing baseline tests does not complete the lab |

See [behavior tests](examples/test_state.py), [typing controls](examples/test_typing_contracts.py),
and [validation record](VALIDATION.md). The negative typing programs are generated in temporary
directories and never executed. Tests deliberately cast malformed inputs to exercise the public
runtime boundary; production clients should not do that.

When debugging, first identify the first wrong assumption: was the event malformed, forbidden in
the current phase, rejected by a guard, rejected by the gate, or nested? Record the before snapshot
and whether the gate ran. Do not catch every exception and pretend an event succeeded.

From the repository root, select the locked development interpreter as `python` and use the cache
controls in VALIDATION.md before these commands:

```bash
python units/behavioral/SDP-BEH-020-state/examples/run_state_demo.py
python units/behavioral/SDP-BEH-020-state/examples/observe_boundary.py
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-beh-020/pytest/unit \
  units/behavioral/SDP-BEH-020-state
python -m mypy --strict --python-version 3.11 units/behavioral/SDP-BEH-020-state
python -m ruff check --target-version py311 units/behavioral/SDP-BEH-020-state
```

Create `/tmp/sdp-beh-020/pytest` first. README Python fences execute independently with the unit's
`examples/` directory on PYTHONPATH. No repository cache or environment should be created.

## 11. Alternatives, related patterns and misuse

| Design / related unit | Primary question | Selection or trigger | Ownership difference |
|---|---|---|---|
| State — SDP-BEH-020 | What behavior is legal in this lifecycle phase? | Event plus current state/data/guards | Context or state decides transitions; context owns installation here |
| [Strategy — SDP-BEH-010](../SDP-BEH-010-strategy/README.md) | Which replaceable policy should perform this operation? | Client/configuration selects policy | Policy selection need not represent lifecycle progression |
| [Template Method — SDP-BEH-060](../../../CURRICULUM.md#sdp-beh-060) | Which steps vary inside a fixed algorithm skeleton? | Subclass implementations supply hooks | Base-class workflow controls step order; no lifecycle transition is implied |
| Enum / transition table | Which named value follows this event? | Table lookup and guards | Behavior may remain in one small function |
| [Flyweight — SDP-STR-070](../../structural/SDP-STR-070-flyweight/README.md) | Which immutable data/behavior can be shared? | Sharing key and lifetime | Sharing is separate from each context's current phase |

Strategy can have configuration or mutable state; State can be selected by user actions. Those
facts do not settle the distinction. Explain the intent and transition contract. A user switching
an editor's mode can be a lifecycle behavior change. A caller choosing page ordering is a policy
choice. A method named `set_state` proves neither. The authors' catalog summary distinguishes
state-driven behavior, objectified algorithms and subclass-controlled steps.
[GoF authors' summary](https://doczz.net/doc/6456109/erich-gamma---richard-helm---ralph-johnson---john-vlissides).

Possible variants include state-owned transitions with a restricted context callback, a context-owned
transition table, or pure functions returning successor data. Shared stateless handlers can serve
many contexts when all entity data stays elsewhere. Our concrete states contain packet page counts;
do not turn one mutable state instance into a global current state. Hierarchical or concurrent
regions require a richer state-machine model; multiplying independent flags into dozens of classes
usually signals that the flat model needs reconsideration.

| Misuse | Why it fails | Better move |
|---|---|---|
| Class for every enum with no behavior | More indirection with no localized rule | Keep an enum/table |
| Public arbitrary phase setter | Lets callers bypass guards and terminal policy | Expose domain events |
| State calls network then mutates Context | Hidden partial failures and callback ordering | Separate decision, effect policy and commit |
| Factory/registry/Singleton for four fixed states | Extra lifecycle and configuration mechanisms | Construct the few value objects directly |
| Reset after every exception | Can destroy valid prior state and hide effects | Preserve pre-commit state and report the failure |
| Treat Released as successful remote delivery | Confuses local state with external evidence | Define an explicit delivery boundary |
| Add a fallback for forbidden events | Silently changes the transition contract | Reject or specify deliberate idempotency |

Use State when several operations change together by phase, transitions protect meaningful
invariants, and localizing phase rules improves maintenance. Decline it for a stable two-branch
function, a data-only graph, or a problem whose real difficulty is durable distributed coordination.

## 12. Interview preparation and closed-book retrieval

Ask **one question at a time**, wait for Rahul's answer, then identify the exact missing step. This
bank is preparation material, not a completed interview.

| Prompt | Weak-answer trap | Exact reasoning gap to check |
|---|---|---|
| Explain State using one packet event | Recites class names | Must connect current phase to changed observable behavior |
| Who owns transitions here? | Says “the State does everything” | Separate successor decision from context installation |
| Can an empty packet be sealed? | Enum allows SEALED, so yes | Phase membership is not the payload invariant |
| Why not a dictionary? | Dictionaries are unprofessional | Explain whether behavior/guards or only edges vary |
| Add an Archived phase after release | Promises only one new class | Identify incoming edges, terminal-policy change, tests and storage schema |
| Gate records then raises: retry? | State unchanged means safe retry | Account for surviving external effects and duplicate risk |
| Can a callback cancel during release? | Python runs one line at a time | Trace synchronous reentrancy and the chosen busy policy |
| State versus mutable Strategy? | Mutable means State | Name lifecycle intent, trigger and owner of replacement |
| Template Method instead? | Same drawing means same pattern | Identify the fixed skeleton and subclass hooks that would justify it |
| Two workers release at once? | One assignment is atomic | Find the absent serialization/version check across the complete operation |

For code review, critique a `set_phase(Phase.RELEASED)` endpoint and a handler that catches all
exceptions and marks the packet CANCELLED. For design transfer, explain whether a three-status
support ticket with no status-specific behavior needs State at all. For implementation, use the
independent [reservation lab](practice/README.md) and preserve the first attempt before refactoring.

Closed-book reconstruction: draw the four phases, fill all 20 matrix cells, state the page/revision
invariants, trace gate failure, and reject one unnecessary abstraction. After a delay, repeat with
a changed domain. Author tests do not count as Rahul recalling or demonstrating any of this.

## 13. Vocabulary and professional English

### Transition — tran-ZISH-un

| Item | Content |
|---|---|
| Simple meaning | Movement from one condition to another |
| Hindi cue | एक अवस्था से दूसरी अवस्था में जाना |
| Here | An accepted event changes the current state or its data |

Natural examples: “The transition took a week.” “Help the team through the transition.” “The light
marks a transition.” **Interview:** “The sealed state proposes the release transition.”
**Engineering:** “Log the committed transition separately from the attempted one.”

### Invariant — in-VAIR-ee-unt

| Item | Content |
|---|---|
| Simple meaning | A rule that must remain true |
| Hindi cue | हमेशा सही रहने वाला नियम |
| Here | A released packet has pages and cannot accept more events |

Natural examples: “The total is invariant.” “We need an invariant for this calculation.” “Check the
invariant after each step.” **Interview:** “Every accepted transition preserves the page bound.”
**Engineering:** “A phase code alone cannot establish the data invariant.”

## 14. Python references and evidence artifacts

[PY-LIB-060 — Dataclasses, enums, types, and generated data models](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-lib-060)
is the exact hard Python mapping for this unit. Minimum bridge: understand generated initialization,
value equality, frozen field assignment, and enum members. See the prerequisite bridge above for
ownership and delegation. The mapping is not evidence that Rahul completed the Python unit.

| Evidence | Learner deliverable | Present artifact |
|---|---|---|
| E — Explain | Reconstruct ownership, graph and invariants without notes | Notebook core and prompts |
| I — Implement/test | Complete the separate reservation change with edge tests | Unsolved starter and baseline tests |
| D — Debug/refactor | Preserve first attempt; identify first broken invariant and refactor | Lab/refactoring checkpoints |
| X — Controlled experiment | Predict, reproduce and explain effect/commit observations | Author-run EXP-01; no learner prediction supplied |
| T — Production transfer | Defend lifecycle representation, serialization and recovery boundaries | Two-worker scenario and review prompts |

Learning remains Not started. Do not upload attempts, solutions, tracker, validation output or
review records to NotebookLM. Only the approved teaching note and allowed curriculum/policy
material are eligible under [the NotebookLM policy](../../../NOTEBOOKLM.md). No upload is performed.

## 15. Sources and review boundary

Sources actually read are linked near the relevant claims: the GoF State section's MIT-hosted HTML
reproduction; the GoF authors' paper transcription/catalog summary; Python 3.11/3.14 dataclasses,
3.14 annotation changes, try/finally and threading documentation; and the typing specification's
Protocol rules. Earlier full-PDF opening attempts failed; the successful State-section reading is
not a claim to have read an entire book. All explanations, text diagrams, code and lab requirements
are original synthetic material. No copied source examples or diagrams, performance measurements,
learner evidence, browser rendering or remote-delivery experiment are claimed.
