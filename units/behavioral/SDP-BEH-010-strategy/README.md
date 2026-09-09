# SDP-BEH-010 — Strategy

## Physical Notebook Core

### Problem or change pressure

A small print service prepares a batch. One customer wants arrival order; another wants short jobs
first. Batch validation and total pages stay the same. Copying the planner for each policy makes
every validation fix a repeated edit.

### One-sentence mental model

> Give the stable workflow a replaceable way to make one decision.

### One essential visual

```text
caller chooses policy ──> plan(jobs, policy)
                           validate batch
                           policy(jobs) ──> chosen ordering algorithm
                           check all IDs <── ordered IDs
                           build Plan
```

### How to read this visual

Read downward. The caller chooses the policy; `plan` executes it once after validating input.
The return arrow carries a proposed ordering, which the context checks before returning a plan.

### Key insight

Selecting an algorithm and running it are separate responsibilities. The context depends on what
the policy promises, not on which concrete policy the caller selected.

### Simplification or limitation

This is a conceptual call flow, not an object-memory diagram. It omits failure arrows and actual
printing. No browser rendering is required or claimed.

### Governing rules or invariants

1. Every policy accepts the same valid input domain and preserves the agreed output meaning.
2. Request data belongs to the call; configuration belongs to the configured policy's owner.
3. The caller owns selection. The context owns the stable workflow and its failure boundary.

### Minimal Python example

```python
from strategy import Job, arrival_order, fewest_pages, plan

jobs = (Job(7, 8), Job(2, 3))
assert plan(jobs, arrival_order).job_ids == (7, 2)
assert plan(jobs, fewest_pages).job_ids == (2, 7)
assert plan(jobs, arrival_order).total_pages == 11
```

Pass `fewest_pages`, the function. Calling `fewest_pages(jobs)` produces data and is a different
operation. Run imported snippets with `examples/` on `PYTHONPATH`; commands appear below.

### One common misconception

**Mistake:** Every callable, conditional, or class named Strategy implements this pattern.

**Correction:** Identify a real family of replaceable decisions and a stable consuming workflow.
A fixed helper can be useful extraction without being Strategy.

### Important trade-offs

- A small seam isolates policy changes, but creates a contract and a selection point to maintain.
- A function is often enough. A class earns its place through coherent state or operations.

### Interview-revision cues

- Name the changing decision and the responsibility that remains stable.
- Explain who selects the policy and when; replacement during a request is not required.
- Reject Strategy when a number, lookup table, or one direct function handles the actual variation.

## Unit metadata

| Field | Value |
|---|---|
| Domain | GoF behavioral patterns |
| Curriculum | [SDP-BEH-010](../../../CURRICULUM.md#sdp-beh-010) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Make an algorithm or policy replaceable through a callable or object contract and compare the simplest Python forms with class-based implementations. |
| Hard prerequisites | [SDP-PYT-010](../../../CURRICULUM.md#sdp-pyt-010), [SDP-SOL-020](../../../CURRICULUM.md#sdp-sol-020) |
| Soft prerequisites | None declared in the canonical entry |
| Priority | Core |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D2 |
| Scope | GoF, Behavioral, Python |
| Size | L |
| First understanding | 4–6 h |
| Hands-on practice | 5–9 h |
| Evidence profile | E+I+D+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Draft |

These frequency labels are curriculum judgments, not measured prevalence. Generated notes and tests
do not prove learning; the tracker remains Not started. See [practice](practice/README.md) for the
separate unsolved task and [validation](VALIDATION.md) for actual author checks.

## 1. Simple explanation and prerequisite bridge

A planner asks, “In what order should these jobs run?” It does not need to own every possible
answer. It can accept an ordering function and do its other work consistently. The selected
function is the Strategy; the planner is the context.

From [SDP-PYT-010](../../../CURRICULUM.md#sdp-pyt-010), carry three ideas: a function can be stored
and passed; a closure can retain configuration; a callable object can keep that configuration in
fields. From [SDP-SOL-020](../../../CURRICULUM.md#sdp-sol-020), carry one judgment: introduce an
extension point where a requirement really varies. This does not mean every module stays unchanged
forever. Adding a named policy still changes application selection and adds tests.

The smallest bridge is to trace `plan(jobs, fewest_pages)`: `policy` receives a function reference;
`policy(jobs)` later calls that function. No inheritance, registration, metaclass or framework is
involved. Explain this aloud before studying the object comparison.

## 2. The direct design and the pressure that breaks its comfort

For one fixed rule, directly call a function or write a sort. With two tiny, stable rules, a
conditional is also reasonable. This illustrative before-version assumes a valid batch and omits
the complete runnable implementation's boundary checks:

```python
from strategy import Job, Jobs, Plan


def before_plan(jobs: Jobs, mode: str) -> Plan:
    if mode == "arrival":
        ordered = jobs
    elif mode == "fewest":
        ordered = tuple(sorted(jobs, key=lambda job: job.pages))
    else:
        raise ValueError("unknown mode")
    return Plan(tuple(job.job_id for job in ordered), sum(job.pages for job in jobs))


assert before_plan((Job(7, 8), Job(2, 3)), "fewest") == Plan((2, 7), 11)
```

Now add a customer-specific “small jobs first” rule. It groups jobs at or below a configured page
cutoff before all others, preserving arrival order inside each group. It is not just another
numeric cutoff for ascending order. A preview endpoint and a batch worker must use the same rule.
If each workflow embeds the growing selection and algorithm bodies, one can silently diverge.

The useful change is to move interchangeable ordering behavior behind `OrderPolicy`, then pass it
into the common planner. The improvement is one reusable decision boundary and independent policy
tests. A lone three-branch function does not automatically justify this refactoring; duplicated
policy knowledge and independently changing rules do.

## 3. Verified original intent and modern interpretation

Gamma, Helm, Johnson and Vlissides describe Strategy as moving variable algorithms into separate
objects so clients can use different behavior without absorbing each implementation. Their
pre-book paper describes a context holding a selected strategy, forwarding work to it, and a
client installing the choice. It also describes strategies calling back into context state.
Read here through the paper's available transcription, specifically its Strategy section, not a
claim of reading a complete book. [GoF authors, Strategy: intent, participants and collaborations](https://www.researchgate.net/publication/221496095_Design_Patterns_Abstraction_and_Reuse_of_Object-Oriented_Design).

The catalog's indexed case-study excerpt likewise identifies strategy and context as the key
participants and emphasizes a common interface broad enough for the intended algorithms. Full PDF
opening failed; only the indexed excerpt was readable. [Catalog excerpt](https://vik.wiki/images/4/45/Sznikak_jegyzet_E.Gamma_R.Helm_R.Johnson_J.Vlissides_DesignPatterns.pdf).

Our Python interpretation passes a small immutable batch, avoiding a callback into the entire
context. A function can fill the algorithm role; a context can itself be a function. These are
design choices for this example, not claims that the original object catalog required Python
callables, purity, or our exact validation rules.

Formally, Strategy encapsulates a family of interchangeable algorithms behind a common contract
and lets a context delegate the varying operation. “Interchangeable” means suitable under the
contract, not identical outputs. Arrival order and page order intentionally differ.

## 4. Participants, responsibilities and execution

| Participant | Implementation here | Must not own |
|---|---|---|
| Client/composition boundary | Caller of `select_policy`, or caller passing a function directly | Duplicate implementations of the chosen ordering rule |
| Context | `plan(jobs, policy)` | A branch on concrete strategy type or name |
| Strategy contract | `OrderPolicy = Callable[[Jobs], Order]`, plus semantic rules below | A promise that typing alone verifies behavior |
| Concrete policies | `arrival_order`, `fewest_pages`, configured closure or object | Printing, changing jobs, or retaining the last request |
| Input | A tuple of frozen `Job` values | Mutable process-wide request state |
| Result | `Plan(job_ids, total_pages)` | Permission to claim jobs actually ran |

```text
configuration/request boundary: select_policy("small", cutoff=5) -> callable
request: jobs -> plan
  1. check <=64 jobs and unique IDs
  2. invoke the selected callable once, including for an empty batch
  3. require a tuple containing every input ID exactly once
  4. derive total pages from input; return Plan
policy raises ---------------------> same exception escapes; no Plan
policy returns invalid IDs --------> PolicyContractError; no Plan
```

### How to read this visual

Selection precedes the request path and may happen once during configuration or for each request.
The numbered lines belong to the context. Failure exits skip result creation.

### Key insight

The context owns validation and result construction. The policy owns ordering only. The selection
conditional is localized at the boundary, not magically eliminated from the program.

### Simplification or limitation

This is a conceptual synchronous trace. No queue, worker, lock, retry or transaction is modeled.
Exactly one invocation is a property of this implementation, not a universal Strategy rule.

## 5. Runnable implementation and semantic contract

Read [strategy.py](examples/strategy.py) and [the demo](examples/run_strategy_demo.py).
The domain is original synthetic print planning, not a production scheduler. Input arrival order
is tuple order, not ID order. A lower job ID does not mean earlier arrival.

| Boundary | Contract | Limit |
|---|---|---|
| `Job` construction | Exact integer ID 0–999999; exact integer pages 1–100; bool rejected | No document loading, content or identity database |
| `plan` input | Typed tuple of normally constructed Jobs; 0–64 jobs; unique IDs in this batch | Not a decoder for arbitrary untyped objects |
| Policy input | Read the whole same batch; accept every valid batch, including empty | No narrower undocumented “only nonempty” precondition |
| Policy result | Tuple of integer IDs, each input ID exactly once | May reorder; may not filter, invent, duplicate or mutate jobs |
| Policy behavior | Deterministic for the same batch/configuration; no I/O or cross-request mutation | Documented and tested; the signature cannot enforce purity |
| Failure | Invalid input/configuration raises ValueError; invalid output raises PolicyContractError; policy exceptions propagate | No automatic retry or fallback |
| Result construction | Total pages always comes from validated input; no Plan on failure | Manually constructing Plan does not run these checks |

`plan` checks result shape as well as membership. Length plus equal sets proves a permutation here
because input IDs are already unique. Length alone misses a duplicate; set equality alone misses
extra repetitions. Exact-integer checks stop `True` from impersonating ID `1`. This is a deliberate
runtime check for ordinary extension mistakes, not isolation of hostile Python code.

This shared contract does not prove a named policy implements its advertised ordering. A function
that returns arrival order always satisfies the permutation check but is a wrong implementation
of “fewest pages.” Test common invariants and each policy's meaning separately.

### The observation to reconstruct

Input is IDs/pages `7/8, 2/3, 9/3, 5/1`; cutoff is 5.

| Choice | Ordered IDs | Total pages | Reason |
|---|---|---|---|
| arrival | 7, 2, 9, 5 | 15 | Retain input order |
| fewest | 5, 2, 9, 7 | 15 | Ascending pages; the two 3-page jobs retain arrival order |
| small | 2, 9, 5, 7 | 15 | Stable small/large partition; no sort inside a group |

### How to read this visual

Compare the middle columns for the same batch. Only order changes; no row drops work or changes
the total. The demo prints these rows and tests verify them.

### Key insight

Different correct results can satisfy one useful semantic contract.

### Simplification or limitation

This table is a bounded correctness observation. It measures neither waiting time nor fairness.
It cannot establish that any rule is a better real-world scheduling policy.

Python's stable sort preserves equal-key input order; `sorted` produces a new list. Those library
guarantees support `fewest_pages`, which then extracts IDs into a tuple.
[Python sorting: basics and stability](https://docs.python.org/3.14/howto/sorting.html#sort-stability-and-complex-sorts).

## 6. Functions, closures, callable objects and method contracts

For one operation without retained configuration, a named function is the smallest useful form.
`Callable[[Jobs], Order]` precisely states its one positional input and output types. Do not weaken
it to `Callable[..., Order]` just to accept incompatible implementations.

```python
from strategy import Job, SmallJobsFirst, plan, small_jobs_first

jobs = (Job(7, 8), Job(2, 3), Job(5, 1))
closed = small_jobs_first(3)
configured = SmallJobsFirst(3)
assert plan(jobs, closed) == plan(jobs, configured)
assert configured.cutoff == 3
```

The closure factory validates once and captures one integer in its own invocation. The callable
dataclass exposes that configuration for inspection. Both delegate to the same small algorithm so
this comparison isolates storage and invocation form. The class is useful when named configuration
and a readable representation matter; it is not necessary to make the algorithm replaceable.

A closure captures access to variables, not a deep copy of arbitrary objects. Functions created
inside a loop can all read the final loop binding; the issue also applies to ordinary nested `def`.
Calling our factory once per cutoff creates independent local bindings. Capturing a mutable list
would still share that list unless the design explicitly copied or converted it.
[Python FAQ: late binding](https://docs.python.org/3.14/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result).

For comparison, [object_strategy.py](examples/object_strategy.py) has `Ordering.order`, an
`ObjectPlanner` that holds an Ordering, and `SmallFirstOrdering` with explicit configured behavior.
It demonstrates the familiar object structure while reusing the exact validation context:

```python
from object_strategy import ObjectPlanner, Ordering, SmallFirstOrdering
from strategy import Job, SmallJobsFirst, plan

ordering: Ordering = SmallFirstOrdering(SmallJobsFirst(3))
context = ObjectPlanner(ordering)
jobs = (Job(7, 8), Job(2, 3))
assert context.plan(jobs).job_ids == (2, 7)
assert context.plan(jobs) == plan(jobs, ordering.order)
```

The extra wrapper is pedagogical, not a recommendation to ship both APIs. Choose one. A method
contract becomes useful when an existing object API or coherent related operations justify it.
Do not add unrelated `save`, `send`, and `close` methods merely to make the interface look serious.

`Ordering` is structural: implementations need not inherit it. Its positional-only `/` lets an
implementation call its parameter `batch` instead of `jobs`. If the contract allowed keyword calls,
keyword names and kinds would matter. A callable replacement must accept every allowed argument
combination and return an assignable result; wider inputs can be safe, narrower ones cannot.
[Typing specification: Callable, callback protocols and assignability](https://typing.python.org/en/latest/spec/callables.html).

The bound method `ordering.order` carries its receiver; the context supplies only the batch.
Calling a `SmallJobsFirst` instance dispatches through its class's `__call__` operation. These are
Python language mechanics, not special Strategy internals or a CPython memory trick.
[Python data model: instance methods and callable objects](https://docs.python.org/3.14/reference/datamodel.html#instance-methods).

## 7. Selection, lifetime and error ownership

| Selection point | Use | Ownership decision |
|---|---|---|
| Configuration time | One worker uses one rule for many batches | Construct a policy once and pass it explicitly |
| Request boundary | A request chooses among approved policy names | Resolve the name once, then call plan with that local choice |
| Mid-operation replacement | Usually unnecessary for this bounded operation | Would need explicit consistency rules; not implemented |

`select_policy` is a small conditional. It rejects unknown names; it never silently converts a typo
into arrival order. Its cutoff belongs only to `small`; an irrelevant cutoff is ignored by the
other choices. External configuration validation may choose to reject irrelevant fields earlier.
A dispatch dictionary could organize more names, but registration and plugin lifecycle are separate
concerns in [SDP-PYT-020](../../../CURRICULUM.md#sdp-pyt-020).

Do not keep a global `current_policy` that one request changes before another request runs. A local
policy parameter provides clear request ownership. The object context is frozen and can be replaced
as a whole when configuration changes; it has no setter that alters an in-progress request.

The provided policies retain no jobs and have no mutable cross-request counters. A shared custom
policy with `last_batch`, a cursor, or a mutable cache would need an explicit ownership and
synchronization design. Freezing the context does not freeze arbitrary objects referenced by it.
Frozen dataclasses reject ordinary field assignment, but do not recursively freeze a mutable
object graph or defend against low-level tampering. [Dataclasses: frozen instances](https://docs.python.org/3.14/library/dataclasses.html#frozen-instances).

The context propagates a policy exception unchanged. It cannot undo a custom policy's side effects,
and checking output after invocation does not make that code safe to execute. A production boundary
can record failure and reject the operation. Fallback requires a separate explicit product promise:
arrival order is not automatically acceptable when a caller requested another rule.

## 8. Substitution and version boundaries

Typing catches a wrong signature, result type, missing method or async function used as a sync
strategy. It does not prove correct ordering, termination, exception behavior, purity, or fairness.
`bool` being accepted by an integer annotation is another reason our domain has explicit checks.
The positive static client intentionally includes a broad-input function; static compatibility does
not certify its output semantics for nonempty batches.

`Protocol` is chiefly a static structural contract. Even `@runtime_checkable` checks attribute
presence rather than full signatures or semantic behavior. Python 3.12 changed its runtime lookup
to static attribute inspection and froze protocol member sets for those checks. This unit uses no
runtime protocol admission, so it does not depend on that difference between 3.11 and 3.14.
[Python 3.11 Protocol](https://docs.python.org/3.11/library/typing.html#typing.Protocol),
[Python 3.14 runtime-checkable protocols](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable).

All source uses 3.11-compatible syntax, including assignment-based aliases. Python 3.14 defers
annotation evaluation by default; this example neither inspects annotations nor uses them for
runtime validation. Its observed functional contracts are checked on both installed runtimes.
[Python 3.14 annotation changes](https://docs.python.org/3.14/whatsnew/3.14.html).

An async policy needs an async context that awaits it and defines cancellation and failure
ownership. Wrapping an async function under the sync annotation does not make its returned coroutine
an Order. No async execution or free-threaded execution is claimed here.

## 9. Refactoring and testing

1. Characterize current output, empty input, ties and invalid input before moving code.
2. Name the varying responsibility: ordering a complete valid batch.
3. Extract one typed operation; keep batch checks and page totals in the context.
4. Inject a direct function and prove old results are preserved for the same rule.
5. Move selection to the boundary; add the new policy with its own semantic cases.
6. Compare a closure and configured object, retaining only the form the application needs.
7. Review errors and state ownership; remove speculative registries and factories.

| Test layer | What it checks | What it cannot prove |
|---|---|---|
| Shared behavior | Empty/singleton batches, complete permutations, totals, repeat calls, unchanged input | Correct named policy ordering |
| Policy-specific cases | Stable ties and stable partition, distinct configurations | A universal real-world optimization |
| Context collaboration | One selected invocation; invalid input invokes none; exceptions keep identity | Safety of arbitrary injected code |
| Invalid output controls | Missing, repeated, extra, unknown, bool and wrong-shape IDs rejected | All possible malicious objects |
| Static clients | Valid functions/objects accepted; ten intended contract violations rejected | Runtime truth of every annotation |
| Bounded property checks | Up to 64 generated jobs, permutation and tie properties, closure/object parity | Exhaustive proof or production load testing |

Tests live in [test_strategy.py](examples/test_strategy.py) and
[test_typing_contracts.py](examples/test_typing_contracts.py). Test doubles can record calls for
collaboration assertions; those probes are not offered as pure production policies. Negative static
programs are generated under pytest's temporary directory and are never executed.

Run from the repository root with the locked development interpreter selected:

```bash
export PYTHONDONTWRITEBYTECODE=1
export MYPY_CACHE_DIR=/tmp/sdp-beh-010/mypy
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-beh-010/hypothesis
export RUFF_CACHE_DIR=/tmp/sdp-beh-010/ruff
mkdir -p /tmp/sdp-beh-010/pytest
python units/behavioral/SDP-BEH-010-strategy/examples/run_strategy_demo.py
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-beh-010/pytest/unit \
  units/behavioral/SDP-BEH-010-strategy
python -m mypy --strict --python-version 3.11 units/behavioral/SDP-BEH-010-strategy
python -m ruff check --target-version py311 units/behavioral/SDP-BEH-010-strategy
python -m ruff format --check units/behavioral/SDP-BEH-010-strategy
```

For README snippets, add `units/behavioral/SDP-BEH-010-strategy/examples` to `PYTHONPATH`.
See [VALIDATION.md](VALIDATION.md) for all cache controls, both runtime checks, and actual results.

## 10. Production transfer, failure and cost

A backend could use this seam to prepare a preview and a worker plan from one policy implementation.
Bind a stable policy identifier and configuration revision at the request boundary. Record batch
size, selected policy/revision, success/failure category and the plan reference. Avoid depending on
`__name__`: closures can share names and callable objects need not expose it. These are production
design suggestions; the example writes no logs or durable records.

A concrete failure: a new “small first” implementation filters out large jobs instead of moving
them later. A return annotation still passes static checking. The context detects missing IDs and
returns no plan. Capture that contract failure, repair the policy, and retry only under an explicit
operation policy. Do not mark printing complete just because planning succeeded.

Another failure: a rule accepts only nonempty batches and indexes the first job. Shared contract
tests expose the strengthened precondition. Fix the strategy or change and version the public
contract deliberately; do not scatter special empty-case handling among clients.

Page count is a synthetic estimate, not job duration. Short-job preference in a stream may starve
large jobs; this example operates on a fixed finite batch and establishes no fairness guarantee.
If real policies need deadlines, priorities, cancellation or resource capabilities, first decide
whether those inputs belong in one shared domain model. Do not pass the whole service object to
every strategy simply to avoid deciding which data is required.

The provided policies allocate bounded ID tuples and sometimes temporary sorted data. The example
does not measure speed or memory and needs no benchmark for E+I+D+T. Strategy provides a change
boundary, not an automatic speed improvement. For a hot path, measure representative work before
adding caches or trading a clearer function for clever dispatch machinery.

## 11. Alternatives, nearby patterns and misuse

| Choice | Change pressure it fits | Distinction from this unit |
|---|---|---|
| Direct function/helper | One rule, or local extraction of a fixed step | No need to promise interchangeable policies |
| Parameter/data option | Same rule with another cutoff, flag or lookup value | Varying data alone does not require a new algorithm object |
| Callable/key function | A small replaceable decision inside a stable operation | Often sufficient Python Strategy form; no class required |
| [State, SDP-BEH-020](../../../CURRICULUM.md#sdp-beh-020) | Behavior follows lifecycle state and explicit transitions | Here a caller selects a policy; no lifecycle transition is modeled |
| [Template Method, SDP-BEH-060](../../../CURRICULUM.md#sdp-beh-060) | A base workflow fixes steps and subclasses override hooks | Strategy delegates to a supplied collaborator through composition |
| [Command, SDP-BEH-040](../../../CURRICULUM.md#sdp-beh-040) | Store an action and its data for later execution or other action management | This policy answers an ordering question now; it is not a queued print action |
| [Bridge, SDP-STR-060](../../../CURRICULUM.md#sdp-str-060) | Two independently varying design dimensions need separate structures | The focus here is one replaceable algorithm consumed by a stable context |

These distinctions concern intent and ownership, not whether two class diagrams happen to resemble
each other. A mutable strategy is not automatically State; an object with `execute` is not
automatically Command. `sorted(..., key=...)` illustrates replaceable comparison-key behavior, but
an incidental one-off lambda does not need a grand pattern story.

Use Strategy when consumers share a real policy family, rules change independently of the workflow,
or configuration/request choices must be explicit and testable. Keep the direct function or
conditional when choices are few, local, stable, and comprehensible. Prefer a data table when rules
really are data. A cutoff of 3 versus 5 is two configurations of one small-first algorithm.

| Misuse | Concrete problem | Smaller correction |
|---|---|---|
| Class plus factory plus registry per one-line rule | More names and lifecycle questions than behavior | Pass a named function |
| Context branches on `isinstance(policy, ...)` | New strategies require context edits again | Move the decision behind the common operation |
| Catch every exception and fall back | Wrong or failed policies appear successful | Preserve errors; define any fallback explicitly |
| Interface accepts arbitrary `**kwargs` | Each policy requires different hidden inputs | Define coherent domain inputs or split contracts |
| Share a mutable last-request field | One request can change another's result | Pass request data; scope real mutable state deliberately |
| Claim all algorithms are universally interchangeable | Some require unavailable input or different output meaning | Revisit the abstraction boundary |

An overengineered print design might introduce `AbstractOrderingFactory`, three context subclasses,
a global plugin registry, and an abstract base class for each cutoff. None solves an additional
requirement here. The method-based comparison is deliberately optional; it should not be stacked
on the function API merely to increase the number of pattern participants.

## 12. Interview preparation and retrieval

Use this sequence as a bank. During a live interview, ask only one question and wait for the answer.
Identify the first missing reasoning step before moving on or offering a hint.

| Prompt | Weak-answer trap | Exact reasoning step to check |
|---|---|---|
| Explain Strategy using these jobs. | “It removes if statements.” | Identify fixed workflow, varying decision, and selection owner |
| Implement the smallest seam. | Start with an ABC and factory | Show why a typed callable suffices for one operation |
| Why can two correct results differ? | “Substitution means same output.” | Separate shared meaning from intentionally different policy results |
| A policy returns all IDs plus a duplicate. | Only compare sets | Account for multiplicity and unique input IDs |
| Why does a type-correct policy fail on empty input? | Trust annotations alone | Identify a strengthened precondition |
| When should a policy be an object? | “Patterns use classes.” | Name actual configuration, coherent operations, or lifecycle ownership |
| The selected policy times out; silently use arrival order? | Treat fallback as an implementation detail | Establish the caller's required semantics and failure promise |
| A job becomes paused and later resumes. | Call any behavior object Strategy | Identify lifecycle transitions and State's different ownership |
| Add fairness for a continuously growing queue. | Claim fewest-pages is already fair | Explain the finite-batch limitation and new state/time inputs |
| Review the method wrapper. | Keep it because it resembles the catalog | Justify it from application needs or remove it |

Follow-ups: trace the selected callable from configuration to result; contrast a closure with a
shared mutable service; show which files change for a new named policy; reject an interface that
requires different private fields for every implementation. A strong senior answer includes a
simpler alternative and the concrete requirement that would change the choice.

Closed-book reconstruction: draw the call flow; state the permutation contract; distinguish stable
ties from stable partition; explain one exception path; reconstruct the callable signature; give
one scenario where data is enough; diagnose one lab attempt without replacing the learner's code.

## 13. Vocabulary and professional English

### Policy — POL-uh-see

| Item | Content |
|---|---|
| Simple meaning | A rule for deciding what to do |
| Hindi cue | निर्णय का नियम |
| Here | The rule that chooses job order |

Natural examples: “Our policy allows returns.” “The school changed its policy.” “Check the policy
before deciding.” **Interview:** “The context delegates its ordering policy.” **Engineering:**
“We must record which policy revision produced this plan.”

### Substitute — SUB-sti-toot

| Item | Content |
|---|---|
| Simple meaning | Put one thing in place of another |
| Hindi cue | जगह पर दूसरा रखना |
| Here | Supply another implementation that respects the same contract |

Natural examples: “Substitute rice for bread.” “She found a substitute teacher.” “This tool can
substitute for the old one.” **Interview:** “A compatible signature is necessary but insufficient
for safe substitution.” **Engineering:** “We can substitute the policy if it preserves every job.”

## 14. Python Mastery references and evidence

- [PY-FIT-030 — Higher-order functions, callable objects, and side effects](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-fit-030): pass a function; distinguish returning a value from producing an effect.
- [PY-FIT-040 — Closures, free variables, and late binding](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-fit-040): explain a captured binding and independent factory calls.

These are the exact hard mappings in [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md), not a
claim that Rahul has completed them. The bridge above is enough to begin; deeper callable typing
can follow the prerequisite unit's references when needed.

| Evidence | Required learner artifact | Current state |
|---|---|---|
| E — Explain | Reconstruct participants, invariants and selection ownership | No learner evidence |
| I — Implement/test | Complete the independent packing lab with edge cases | Starter only |
| D — Debug/refactor | Preserve an attempt; find the first broken contract or misplaced decision | Not attempted |
| T — Production transfer | Defend a policy seam, state scope and failure behavior in a changed scenario | Prompts only |

No X experiment requirement is added. No hints or solutions have been released. NotebookLM may use
this note only after approval; exclude the tracker, raw attempts, test output and lab solutions.
Follow [the NotebookLM policy](../../../docs/NOTEBOOKLM.md).

## 15. Authoritative sources and review boundary

Sources actually read are linked beside their claims: the GoF authors' Strategy paper section
through its available transcription; the catalog's indexed case-study excerpt (full PDF opening
failed); Python sorting, data model, dataclasses, programming FAQ and 3.11/3.14 typing documentation;
the callable typing specification; and Python 3.14's annotation-change documentation. No complete
book reading, copied diagram, production benchmark or CPython-internals experiment is claimed.

The code, diagrams and exercises are original synthetic teaching material. The intentional open
boundary is production scheduling: fairness, persistence, cancellation and actual print execution
need different requirements. They are not hidden features of this planner.
