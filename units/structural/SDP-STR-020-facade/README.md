# SDP-STR-020 — Facade

## Physical Notebook Core

### Problem or change pressure

A command-line tool and a web endpoint both know how to load a report, render it, and store the
packet. When the subsystem changes its sequence or errors, both clients need the same repair.

### One-sentence mental model

> Give a common task a small front door; keep the machinery behind it independently usable.

### One essential visual

```text
ordinary client → build(report_id) → load → render → store → receipt
                    facade          └──── subsystem ────┘
maintenance client ───────────────────────────→ archive.read(key)
```

### How to read this visual

Read left to right. Arrows mean calls in the common task. The lower arrow is a deliberately supported
expert capability, not a call back from the subsystem into the facade.

### Key insight

The client names a task instead of assembling a subsystem recipe. The facade still has to understand
that recipe; complexity has an owner rather than disappearing.

### Simplification or limitation

This is a conceptual call map, not memory layout. It shows success only. One call can still perform
several effects, fail halfway, or leave the caller unsure whether a write succeeded.

### Governing rules or invariants

1. Keep a small task contract with explicit results, failures, and effect boundaries.
2. Subsystem components need not know the facade; borrowed dependencies remain caller-owned.
3. Simplification does not supply atomicity, retries, authorization, or thread safety.

### Minimal Python example

```python
from collections.abc import Callable


def packet(load: Callable[[], str], render: Callable[[str], bytes]) -> bytes:
    return render(load())


assert packet(lambda: "open=3", str.encode) == b"open=3"
```

### One common misconception

**Mistake:** A facade must hide every subsystem feature behind one large class.

**Correction:** It offers a useful common path. A supported lower-level API can serve expert tasks;
copying every subsystem method into the facade recreates the complexity.

### Important trade-offs

- Fewer client dependencies, but one more public contract to maintain.
- Convenient defaults, but less room for unusual workflows; preserve an intentional escape path.
- A function may suffice. An object earns its place when retaining collaborators helps clients.

### Interview-revision cues

- Recognition: several clients repeat the same subsystem knowledge.
- Comparison: simplification differs from translating an incompatible interface.
- Rejection: one clear direct call usually needs no extra facade.

## Unit metadata

| Field | Value |
|---|---|
| Domain | GoF structural patterns |
| Curriculum | [SDP-STR-020](../../../CURRICULUM.md#sdp-str-020) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Offer a small task-oriented entry point over a complicated subsystem while preserving access to lower-level capabilities when justified. |
| Hard prerequisites | [SDP-FND-020](../../../CURRICULUM.md#sdp-fnd-020), [SDP-FND-100](../../../CURRICULUM.md#sdp-fnd-100) |
| Soft prerequisites | None |
| Priority | Core |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D2 |
| Scope | GoF, Structural, Backend |
| Size | M |
| First understanding | 2–4 h |
| Hands-on practice | 3–6 h |
| Evidence profile | E+I+D+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Approved |

Frequency labels are curriculum judgments, not measured statistics. Learning remains **Not started**;
authored notes and maintainer checks are not learner evidence. Use the worked
[demo](examples/run_facade_demo.py), [failure experiment](experiments/EXP-01-partial-failure/README.md),
[unsolved lab](practice/README.md), and actual [validation record](VALIDATION.md).
The experiment supports explanation/debugging without changing the canonical E+I+D+T profile.

## 1. Simple explanation and prerequisite bridge

Imagine asking a workshop desk for a finished information packet. You do not want instructions for
finding the source, setting up the printer, and filing the output each time. The desk coordinates a
known task. A technician may still use the printer directly for calibration.

In this unit, the desk is `ReportFacade`, the task is `build`, and the machinery is a snapshot reader,
a renderer, and an archive. It is a small interface **to a subsystem**, not necessarily a network API.
The pattern describes collaboration; Python has no `facade` keyword.

Both prerequisite notes are approved but their learning states are Not started. The minimum bridge
from SDP-FND-020 is: group decisions by their reason to change. Report formatting belongs to the
renderer; the common preparation sequence belongs to the facade. From SDP-FND-100: draw imports
before moving files. Stable task values and ports must not import concrete storage or web clients.
Dependency injection here means passing ordinary objects explicitly, without a framework.

## 2. Real problem and the decision ladder

The stable need is “prepare one report packet and return its receipt.” Subsystem details vary:
snapshot acquisition, output encoding, storage keys, and recognized errors. A second client should
not have to rediscover the order and error meanings. The chosen contract permits one archive write
attempt and makes no promise of retry safety.

| Design | Useful when | Cost or next change pressure |
|---|---|---|
| Direct subsystem calls | One caller with a clear, stable sequence; expert operation | Repeated sequence knowledge spreads across clients |
| Small function/module entry point | A common recipe with simple dependencies | Hidden module globals can make configuration and tests awkward |
| Injected orchestration function | Callers or a root already have the collaborators | Repeated wiring can clutter otherwise simple client signatures |
| Composition-based facade | Related clients reuse a configured dependency bundle | Additional lifecycle and public API to explain |
| Universal facade with flags for every subsystem option | Rarely justified | Becomes another complicated subsystem or a God Object |

The first three are valid designs, and the latter two function forms can already express Facade
intent. A class is not the moment at which a design becomes legitimate. Name a real change that gets
cheaper; if there is none, leave the direct code alone.

## 3. GoF intent and formal mechanics

The GoF intent is to offer a higher-level entry point that makes a collection of subsystem interfaces
easier to use. This wording is paraphrased from the GoF intent as presented in Shalloway and Trott's
[publisher-hosted introduction](https://www.informit.com/articles/article.aspx?p=347700&seqNum=2).
That is the source read here; this note does not claim access to the original GoF chapter.

Their [field notes](https://www.informit.com/articles/article.aspx?p=347700&seqNum=4) also discuss
reducing how many subsystem objects a client handles. Our report example is an original Python
interpretation: it moves common sequencing into a function and optionally retains dependencies in
an object. None of their examples, diagrams, or implementations is reproduced.

Formally, clients ask the facade for a coarse task; the facade delegates the necessary operations
to subsystem collaborators; those collaborators keep their own responsibilities. In this design,
they have no reference to the facade. Returning a receipt instead of the archive itself stops ordinary
clients from having to learn its management interface. Fewer exposed concepts matters more than
merely counting method calls.

## 4. Participants, imports, and optional lower-level access

| Participant | Here | Owns | Must not accumulate |
|---|---|---|---|
| Client | CLI/web consumer of `PacketBuilder` | Request intent and presenting the result | Storage sequencing and vendor failures |
| Facade | `ReportFacade` / `build_packet` | Common ordering and task-level failure context | Report policy, transport credentials, unrelated workflows |
| Subsystem | Reader, renderer, archive | Their respective capabilities and contracts | Knowledge of facade callers |
| Composition root | Demo `main` | Construction, configuration, lifetime | Per-request formatting decisions |
| Expert client | Maintenance code using `keys`/`read` | A supported low-level task | Reimplementing the ordinary build path everywhere |

The first three are the central design roles. The root and maintenance client make this example's
ownership and escape path explicit.

```text
source imports (arrow = imports/knows)
run_facade_demo → report_facade → report_contracts
       └────────→ report_subsystem → report_contracts

runtime references
root owns archive; facade borrows reader + renderer + archive
request_packet receives facade as PacketBuilder
```

### How to read this visual

Read each arrow as a source dependency, then read the runtime references separately. The two modules
share stable contract definitions. The root is allowed to know concrete components to assemble them.

### Key insight

A call reaching concrete storage does not require the client or facade module to import that concrete
implementation. Source dependencies and runtime collaboration answer different questions.

### Simplification or limitation

This is a conceptual module graph for the worked files, omitting standard-library imports and test
modules. Ports localize knowledge; they do not automatically make every replacement behave correctly.

Expert access is a supported interface with a documented audience, compatibility policy, and owner.
Here, the root can give maintenance code the archive directly. The facade does not expose an arbitrary
`raw` object getter or forward unknown attributes. Application import conventions alone are not an
access-control boundary: if low-level calls could bypass required authorization, enforce that rule
at the actual protected capability and control which clients receive it. This is a design requirement
for a real integration; the synthetic archive has no user/tenant security model.

## 5. Before-pattern code and concrete pain

Run each Python fence independently with the example directory on `PYTHONPATH` (commands below).
This direct version is perfectly reasonable for one script:

```python
from report_contracts import Snapshot
from report_subsystem import MemoryArchive, MemoryReports, TextRenderer

steps: list[str] = []
reader = MemoryReports({"WEEK-1": Snapshot(("open=3",))}, steps)
renderer = TextRenderer(steps)
archive = MemoryArchive(steps)
try:
    snapshot = reader.load("WEEK-1")
    payload = renderer.render(snapshot)
    receipt = archive.store("WEEK-1", payload)
    assert receipt.byte_count == 14
finally:
    archive.close()
```

Now a scheduled job also builds the packet. Both callers implement the same order and catch subsystem
errors. A renderer failure must stop storage; a storage failure must be reported as an uncertain
write. Copying that rule into every route and job is the concrete pressure. A facade centralizes the
common rule. It does not make storage failures impossible.

## 6. Smallest Pythonic facade and injected function

The notebook function is enough for a two-step trusted recipe. A module can expose such a task as
its public API without creating a class or opening connections on import. The worked
[`build_packet`](examples/report_facade.py) is the same approach with explicit ports, input checking,
and bounded error translation. The function is the single owner of the sequence; the object delegates
to it so we do not maintain two orchestration implementations.

```python
from report_contracts import Snapshot
from report_facade import build_packet
from report_subsystem import MemoryArchive, MemoryReports, TextRenderer

steps: list[str] = []
archive = MemoryArchive(steps)
try:
    result = build_packet(
        "WEEK-1",
        reader=MemoryReports({"WEEK-1": Snapshot(())}, steps),
        renderer=TextRenderer(steps),
        archive=archive,
    )
    assert result.byte_count == 8
    assert steps == ["load", "render", "store"]
finally:
    archive.close()
```

Use the function directly when the dependencies are already at hand. If many callers should receive
one ready-to-use task object, `ReportFacade(reader, renderer, archive).build(report_id)` retains the
same collaborators. No base class, registry, metaclass, singleton, or dependency container is needed.

## 7. Typed implementation and exact contract

Read [contracts](examples/report_contracts.py), [facade](examples/report_facade.py), and
[synthetic subsystem](examples/report_subsystem.py) in that order. Narrow Protocols describe the
capabilities this task needs, not every feature the implementations offer. Concrete classes need
not inherit them to satisfy static structural assignability; see the
[typing specification](https://typing.python.org/en/latest/spec/protocol.html#assignability-relationships-with-other-types).
The client port `PacketBuilder` lets a client be tested without arranging an entire subsystem.

| Dimension | This example's agreed behavior |
|---|---|
| Input | Typed `str`; 1–24 uppercase ASCII letters, digits, or hyphens; no trimming or normalization |
| Source | One snapshot lookup per valid call; missing report is a load failure, empty rows are valid |
| Order | Load must succeed before render; render must succeed before store |
| Result | Receipt with storage key and encoded byte count, after storage acknowledges success |
| Effects | At most one archive write attempt per call; no retry, deletion, reservation, or notification |
| Load/render failure | `PacketUnavailable` with precise stage and `NOT_ATTEMPTED` write outcome |
| Store failure | `PacketUnavailable` with `STORE` and `UNKNOWN`; never infer rollback from an exception |
| Unexpected exception | Propagates for diagnosis; not relabeled as a known availability failure |
| Lifetime | Dependencies are borrowed; root closes the archive, including on failure |
| Repetition | Every call executes again; same report ID does not imply same packet key |
| Trust | Ports are trusted typed components; untrusted payload parsing belongs at their boundary |

Annotations do not express “does not store twice” or enforce these semantics. The negative checker
fixture rejects a store returning `str` instead of `Receipt`; behavioral tests must still catch a
signature-compatible implementation that lies about its effects. Runtime-checkable Protocols only
check attribute presence, not signatures. Python 3.12 changed that lookup and froze the member set
used by those checks; see [typing documentation](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable).
This implementation uses no runtime Protocol check as a validator.

`Snapshot` and `Receipt` use frozen dataclasses with immutable field values. Frozen dataclasses
block ordinary field assignment, not mutation of arbitrary referenced objects; see
[dataclass frozen instances](https://docs.python.org/3.14/library/dataclasses.html#frozen-instances).
The facade is an ordinary object retaining references; it is not a copied subsystem or a protected
security container.

## 8. Call flow, lifecycle, and configuration

For a successful request, `request_packet` calls `build`, which validates the identifier, loads one
snapshot, renders bytes, and asks the archive to store them once. Only an acknowledged receipt is
returned. The facade does not retain a “current report” field between requests.

The root creates the archive and closes it in `finally`. It lends that same archive to the facade
and, where justified, maintenance code. A facade call never closes a borrowed dependency, because
another caller may still use it. Our fake's close is infallible. A real close failure needs a policy
for preserving the primary exception and reporting cleanup failure; this example does not simulate it.

Inject configuration when assembling components: reader location, renderer options, storage timeout,
and credentials belong with the components that interpret them. Do not let every request read a
mutable global settings dictionary. Do not make the facade construct a client during module import.
Choosing an application lifetime or request lifetime is a root decision, based on collaborator safety
and cost, not a consequence of using Facade.

## 9. Partial failure, errors, and recovery

A store may allocate an object and then fail before acknowledging it. From the caller's perspective,
“the method raised” and “no object exists” are different facts. The exception below deliberately says
`UNKNOWN` even though our instrumented fake can see that a write happened:

```python
from report_contracts import PacketUnavailable, Snapshot, WriteOutcome
from report_facade import ReportFacade
from report_subsystem import MemoryArchive, MemoryReports, TextRenderer

steps: list[str] = []
archive = MemoryArchive(steps, lose_ack=True)
try:
    facade = ReportFacade(
        MemoryReports({"WEEK-1": Snapshot(())}, steps), TextRenderer(steps), archive
    )
    try:
        facade.build("WEEK-1")
    except PacketUnavailable as error:
        assert error.write_outcome is WriteOutcome.UNKNOWN
        assert len(archive.keys()) == 1
    else:
        raise AssertionError("the injected failure must be visible")
finally:
    archive.close()
```

A blind retry creates a second object in this fake. Production recovery would need a provider-supported
operation identity and lookup/deduplication contract, or an explicit reconciliation decision. This
facade contract has no safe retry method. Do not invent a key after losing the acknowledgement or
silently delete objects you cannot reliably identify.

The three `try` blocks catch only their port's documented failures. Stage is an observable boundary,
not a guess from exception message text. `raise ... from exc` preserves the original exception as
`__cause__`; unhandled chained exceptions can display both messages, per the
[language reference](https://docs.python.org/3.14/reference/simple_stmts.html#the-raise-statement).
A short public error message therefore does **not** prove a traceback is safe to expose.

If a later requirement adds notification after storing, first define whether notification failure
means packet creation failed, or means a successful packet needs a pending notification. That is a
contract decision, not a reason to wrap everything in `except Exception: return False`.

## 10. Production boundaries and senior trade-offs

| Concern | Deliberate decision | What the facade structure does not provide |
|---|---|---|
| Business policy | Caller/domain decides which reports may be requested; renderer owns representation | A reason to collect billing, permissions, retention, and pricing rules in one class |
| Authorization | Protect actual operations and tenant boundaries even for expert clients | Security from underscore attributes or convenient routing alone |
| Observability | Record task outcome, stage, permitted operation ID, duration, and write certainty | Permission to log packet contents, credentials, or raw causes |
| Atomicity | This contract permits partial effects; a real transaction must cover the actual resources | Rollback across independent systems merely because there is one method |
| Retries | No automatic retry; first establish idempotency, lookup, limits, and retryable failures | Exactly-once behavior or safe repetition |
| Concurrency | Share only if all collaborators and per-call state support it | Thread safety from having no mutable facade request fields |
| Async | Use async-compatible ports and explicit deadlines/cancellation semantics if needed | Converting synchronous storage into nonblocking I/O by renaming the facade method |
| Performance | Count and measure actual I/O and materialized data for a real workload | Fewer network trips because the client sees fewer methods |

These are design judgments and integration requirements, not claims of a particular framework's
behavior. The synthetic implementation has no framework, live database, transaction manager,
network retries, cancellation, or concurrency control. Its in-memory archive is sequential and
non-durable. Multiple concurrent requests and live transport failures require new integration evidence.

The current packet is fully materialized in memory. Large reports may need a streaming contract,
resource lifetime, and different error timing. Introducing that contract changes more than the return
type. No time or memory benchmark is asserted here.

For an async variant, identify which steps depend on previous outputs before attempting parallelism:
render requires the snapshot, and store requires rendered bytes. Define what cancellation means after
a write starts. A wrapper cannot establish whether an external operation finished simply by ceasing
to wait for it. This is the same uncertainty boundary as a lost acknowledgement, applied to a future
async integration, not an experiment performed by this unit.

## 11. Testing and the controlled experiment

| Evidence | What it establishes | Limit |
|---|---|---|
| Behavioral example tests | Order required by data flow, results, failures, no retries, ownership, repeated calls | The synthetic ports, not a real vendor |
| Strict mypy and negative control | Concrete components fit the declared ports; wrong return shape is rejected | No proof of side effects, units, or truthful acknowledgements |
| Client seam | `PacketBuilder` can be supplied without storage knowledge | Client tests should not assert the facade's private attributes |
| Failure probe | Identical public store failures can correspond to zero or one stored object | Deliberate fault injection, no network or durability claim |
| Integration tests to add for a real archive | Acknowledgement meaning, persistence, identity, auth, timeouts, cleanup | Not supplied by an in-memory fake |

The [experiment](experiments/EXP-01-partial-failure/README.md) records a question, hypothesis, exact
commands, observed output, and limitations. It is an observation table plus conceptual diagrams;
no browser rendering is needed or claimed. The earlier blocked browser attempt in another unit is
not evidence for this one and is not worked around.

Tests should preserve the required data dependency and side effects. They should not freeze incidental
helper names or demand a particular number of classes. When changing the subsystem, run its contract
suite against the new implementation as well as facade tests; mocks alone can agree with a mistaken
assumption.

## 12. Refactoring path and when to stop

1. Capture current results, errors, and effects in characterization tests.
2. Find the shared recipe and the clients that actually repeat it.
3. Extract one task function while preserving observable behavior.
4. Pass collaborators explicitly; put shared values in a stable module if imports would cycle.
5. Introduce the documented failure contract as an intentional change, and migrate callers' handling.
6. Keep an object facade only if retaining the configured collaborators improves call sites.
7. Preserve needed lower-level capabilities for a named audience and remove speculative forwarding.

Behavior preservation and changing error semantics are separate review steps. Renaming a subsystem
error into a task error is an API change even when the happy-path bytes stay identical.

Use Facade for repeated subsystem coordination, a deliberate convenience layer for common tasks,
or a stable client boundary over a changing implementation. Prefer direct calls for expert one-off
operations, small scripts, or a subsystem that already exposes the correct task. Prefer a function
when there is only one cohesive operation and no useful retained configuration.

## 13. Misuse, variants, and bounded comparisons

| Misuse | Concrete symptom | Better move |
|---|---|---|
| God Object | `PlatformFacade` handles reports, payroll, login, refunds, and feature flags | Separate cohesive tasks and return policy decisions to their owners |
| One-to-one forwarding | Fifty facade methods mirror fifty subsystem methods | Expose the few common tasks or use the subsystem directly |
| Flag maze | `build(raw=True, skip_store=True, notify=False, force=True)` | Name distinct tasks; keep expert operations at a supported lower level |
| Hidden construction | Each call opens global-configured clients without a clear owner | Assemble and close at an explicit root |
| Blanket failure hiding | Every error becomes `None`, followed by a caller retry | Preserve recognized failure stage and effect certainty |
| Mandatory gateway by habit | Debug/maintenance features become inaccessible | Offer a deliberate expert capability when security and contract permit |

Function/module facades and composed objects are implementation choices. Several focused facades can
serve different audiences over the same subsystem, provided they do not duplicate policy or create
cycles. That is a cohesion choice, not a mandate to create an additional facade per client.

| Related unit | Boundary of comparison |
|---|---|
| [SDP-STR-010 — Adapter](../../../CURRICULUM.md#sdp-str-010) | Adapter repairs an incompatible interface; Facade simplifies using a subsystem. A facade may call an adapter internally. |
| [SDP-STR-030 — Decorator](../../../CURRICULUM.md#sdp-str-030) | Compatible behavior wrapping differs from presenting a coarse task interface. |
| [SDP-STR-040 — Proxy](../../../CURRICULUM.md#sdp-str-040) | Controlling access to a represented object differs from simplifying subsystem coordination. |
| [SDP-BEH-080 — Mediator](../../../CURRICULUM.md#sdp-beh-080) | Peer coordination differs from this one-way client-to-subsystem front door. |
| [SDP-APP-060 — Service Layer](../../../CURRICULUM.md#sdp-app-060) | An application operation boundary may use a facade, but its policy/transaction responsibilities need separate justification. |
| [SDP-APP-050 — Unit of Work](../../../CURRICULUM.md#sdp-app-050) | Coordinating a persistence transaction is a distinct obligation from making calls convenient. |

These are recognition boundaries, not implementations or teaching material for the related units.
A shape that looks like “A calls B” does not identify the intent by itself.

## 14. Interview preparation

Use these as a question bank. In a live interview, ask **one question**, wait for the attempt, identify
the first missing reasoning step, then offer a follow-up. Do not memorize the checkpoint wording.

| Prompt | Weak-answer trap | Exact reasoning gap to diagnose |
|---|---|---|
| Explain Facade to a junior engineer | “A wrapper class” | Does not connect a common task to subsystem coordination pressure |
| Two clients repeat load/render/store; refactor it | Immediately creates a base class hierarchy | Has not tested whether one injected function solves the problem |
| Draw clients, facade, and subsystem | Every component refers to the facade | Confuses common entry point with peer coordination |
| The store timed out; can we retry? | “Yes, catch the exception” | Has not distinguished missing acknowledgement from missing effect |
| Maintenance needs raw stored bytes | Add every archive method to the facade | Has not identified a supported expert audience and contract |
| A stateless facade uses a mutable shared client; is it safe? | “Yes, no state in facade” | Ignores collaborator state, lifetime, and concurrent operations |
| Where should report eligibility rules live? | Put all rules in the facade for convenience | Has not separated subsystem preparation from business policy ownership |
| Review a facade that catches every exception and returns False | Calls it good encapsulation | Loses failure cause, effect certainty, and unexpected bug visibility |
| A single stable function already builds the packet | Adds another facade because it is GoF | Has not named a change made cheaper by the abstraction |

Likely follow-ups: change the output representation; add a second client; introduce a failing archive;
require cancellation; require a tenant boundary; require safe retries. Start with the contract affected
by the change, not a list of more patterns. A strong answer names the force, simplest alternative,
participants, ownership, effect boundary, and an explicit reason to reject unnecessary machinery.

## 15. Closed-book revision and evidence

Reconstruct the two arrows in the notebook diagram. Explain which modules know concrete storage.
Compare direct calls, a function, and an object for one caller versus three callers. Predict the number
of stored objects after a lost acknowledgement and a blind retry. State which required guarantee the
facade cannot provide alone. Then work the [separate lab](practice/README.md) without reading a solution.

E: explain the force and trade-offs. I: implement the lab's task boundary. D: diagnose a partial-failure
or duplication problem. T: transfer the reasoning to a new subsystem and reject an unnecessary facade.
Record genuine attempts/reviews under repository policy; generated tests alone advance no state.

## 16. Vocabulary and professional English

### Facade — “fuh-SAHD”

| Item | Content |
|---|---|
| Simple meaning | The front or outward-facing part |
| Hindi cue | सामने का भाग |
| Design meaning | A convenient task interface over more detailed capabilities |

Examples: “The facade faces the street.” “They repaired the facade.” “A plain facade can hide complex
machinery.” **Interview:** “The facade gives ordinary clients a small task interface.”
**Engineering discussion:** “Keep archive diagnostics available outside the report facade.”

### Orchestrate — “OR-kuh-strayt”

| Item | Content |
|---|---|
| Simple meaning | Arrange several participants to complete a task |
| Hindi cue | तालमेल से काम करवाना |
| Design meaning | Coordinate calls without absorbing every participant's responsibility |

Examples: “She orchestrated the event.” “We orchestrated the move.” “The team orchestrated the rehearsal.”
**Interview:** “The facade orchestrates existing capabilities.” **Engineering discussion:**
“Orchestrating the write does not make the operation atomic.”

## 17. Python Mastery references and version boundaries

There is no direct Facade row in [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md). These exact
links are supporting bridges through existing mapped units, not added hard prerequisites:

| Existing mapping | Exact Python reference | Minimum bridge |
|---|---|---|
| SDP-FND-100 | [PY-MOD-010 — Modules, packages, and executable modules](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-mod-010) | A module can expose a public task function. |
| SDP-FND-100 | [PY-MOD-020 — Import resolution, sys.path, and module caching](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-mod-020) | Importing a module can execute top-level code; keep resource creation explicit. |
| SDP-FND-100 | [PY-MOD-030 — Circular imports and package boundaries](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-mod-030) | Put shared contracts where they do not import concrete callers. |
| SDP-FND-100 | [PY-MOD-070 — Package layouts, resources, entry points, and plugin boundaries](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-mod-070) | Public entry points and construction roots have different jobs. |
| SDP-FND-070 / SDP-PYT-070 | [PY-TYP-050 — Protocols, ABCs, and structural versus nominal typing](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-typ-050) | A checker compares capabilities; runtime calls still need truthful behavior. |

The code uses Python 3.11-compatible annotations, dataclasses, Protocols, enums, and exception chaining.
Python 3.14 defers annotation evaluation by default, as documented in
[What's New](https://docs.python.org/3.14/whatsnew/3.14.html#pep-649-pep-749-deferred-evaluation-of-annotations).
These modules define referenced types before use and perform no annotation-driven dependency lookup;
that version change does not add facade behavior. Strict typing and behavioral runs on both runtimes
are recorded separately. No CPython memory or dispatch internals are needed to explain this design.

## 18. Run and review

From the repository root, use an existing locked development interpreter as `python`. Direct example
runs need no third-party runtime dependency. Tests need the locked pytest/mypy tools. Keep generated
state outside the repository:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-str-020/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-str-020/mypy
export RUFF_CACHE_DIR=/tmp/sdp-str-020/ruff
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-str-020/hypothesis
export UV_CACHE_DIR=/tmp/sdp-str-020/uv
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-str-020/environment
export COVERAGE_FILE=/tmp/sdp-str-020/coverage
mkdir -p /tmp/sdp-str-020/pytest
export PYTHONPATH="$PWD/units/structural/SDP-STR-020-facade/examples"
python units/structural/SDP-STR-020-facade/examples/run_facade_demo.py
python units/structural/SDP-STR-020-facade/examples/failure_probe.py
python units/structural/SDP-STR-020-facade/practice/import_lab.py
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-str-020/pytest/focused units/structural/SDP-STR-020-facade
python -m mypy --strict --python-version 3.11 units/structural/SDP-STR-020-facade
python -m ruff check units/structural/SDP-STR-020-facade
python -m ruff format --check units/structural/SDP-STR-020-facade
python scripts/validate_repo.py
```

Expected successful demo: packet `WEEK-1/1`, 14 bytes, steps `load,render,store`, one maintenance key,
and one close. The starter intentionally prints `target_complete=False`. See [VALIDATION.md](VALIDATION.md)
for exact executed environments, checks, and limitations; these commands alone are not evidence.

## 19. Sources, rights, and handoff

Sources actually read on 2026-09-09:

1. Shalloway and Trott, *Design Patterns Explained*, publisher-hosted
   [Facade introduction](https://www.informit.com/articles/article.aspx?p=347700&seqNum=2) and
   [field notes](https://www.informit.com/articles/article.aspx?p=347700&seqNum=4): intent and simplification.
2. [Typing specification: Protocols](https://typing.python.org/en/latest/spec/protocol.html): structural assignability.
3. Python [3.11 typing](https://docs.python.org/3.11/library/typing.html#typing.Protocol) and
   [3.14 runtime-checkable protocols](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable).
4. Python 3.14 [raise statement](https://docs.python.org/3.14/reference/simple_stmts.html#the-raise-statement)
   and [frozen dataclasses](https://docs.python.org/3.14/library/dataclasses.html#frozen-instances).
5. Python 3.14 [annotation changes](https://docs.python.org/3.14/whatsnew/3.14.html#pep-649-pep-749-deferred-evaluation-of-annotations).

Explanations, code, diagrams, data, and exercises are original and synthetic. No license decision is
made here. NotebookLM may receive this note after approval, following
[the policy](../../../docs/NOTEBOOKLM.md); do not upload the tracker, attempts, tests, or validation logs.
No learner attempt or solution is represented by this authored material.
