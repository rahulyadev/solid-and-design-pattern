# SDP-PYT-010 — Functions, closures, and callable objects as design tools

## Physical Notebook Core

### Problem or change pressure

A batch operation stays the same, but one decision inside it must vary by caller.
Later, some callers need configuration or state. A new base class is not automatically needed.

### One-sentence mental model

> Pass the behaviour the caller needs; give its state an explicit owner and lifetime.

### One essential visual

```text
setup chooses encode -> encode_batch(texts, encode) -> encode(text) -> bytes
                        same workflow                variable behaviour
```

### How to read this visual

Read left to right. The first arrow passes a callable; the later arrows show calls and results.

### Key insight

The workflow depends on a calling contract, not on a particular function or class name.

### Simplification or limitation

This is conceptual collaboration, not memory layout. It omits exceptions and state ownership.

### Governing rules or invariants

1. Pass `encode` to defer its call; `encode(text)` runs it now and passes its result.
2. Agree on arguments, result, errors, effects, and state lifetime before substituting callables.
3. Capturing a reference does not copy an object; sharing a callable can share its state.

### Minimal Python example

```python
from collections.abc import Callable


def transform(text: str, encode: Callable[[str], bytes]) -> bytes:
    return encode(text)


def utf8(text: str) -> bytes:
    return text.encode("utf-8")


assert transform("ok", utf8) == b"ok"
```

### One common misconception

**Mistake:** A closure freezes everything that it mentions.

**Correction:** An enclosing binding is read when needed. A retained mutable object can
also change. An intentional immutable value snapshot is a separate design choice.

### Important trade-offs

- A function keeps a small boundary clear; hidden captured state can make it harder to inspect.
- A callable object makes state explicit; a hierarchy can add unnecessary navigation.

### Interview-revision cues

- Where does the changing decision live?
- Who owns the state, and which calls share it?
- What would justify a class, a named method, or a durable command record?

## Unit metadata

| Field | Value |
|---|---|
| Domain | Pythonic design mechanisms |
| Curriculum | [SDP-PYT-010](../../../CURRICULUM.md#sdp-pyt-010) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Use first-class callables to implement Strategy- or Command-like collaboration before introducing class hierarchies. |
| Hard prerequisites | [SDP-FND-060](../../../CURRICULUM.md#sdp-fnd-060), [SDP-FND-070](../../../CURRICULUM.md#sdp-fnd-070) |
| Soft prerequisites | None specified by the curriculum |
| Priority | Core |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D3 |
| Scope | Python, Idiom |
| Size | L |
| First understanding | 4–6 h |
| Hands-on practice | 5–9 h |
| Evidence profile | E+I+D+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Draft |

The frequency labels are curriculum judgments, not measured statistics. The two supporting
experiments do not change the canonical evidence profile. Material validation is recorded in
[VALIDATION.md](VALIDATION.md); it does not establish learner progress.

## 1. Simple explanation and prerequisite bridge

Imagine a machine that processes every item in a tray. Different callers want different
treatment of each item. Give the machine the treatment operation instead of making the
machine know every caller. If that treatment needs a label, configure it once. If it needs
a visible count, give the count a clear owner.

The minimum bridge from **SDP-FND-060** is that different implementations can answer the
same call. From **SDP-FND-070**, compatible shape is useful, but behaviour must also match.
No prerequisite learning evidence is assumed: both tracker rows currently say Not started.

A function is an object: you can assign it, pass it, or return it. A higher-order function
accepts or returns a callable. `callback = utf8` retains the operation; `payload = utf8("ok")`
obtains a result. Creating a nested function does not execute its body.
[Python language reference: function definitions](https://docs.python.org/3.14/reference/compound_stmts.html#function-definitions).

Study in this order: this note → [worked demo](examples/run_callable_demo.py) →
[visuals](visuals/README.md) → [binding experiment](experiments/EXP-01-binding-and-aliases/README.md)
→ [effects experiment](experiments/EXP-02-deferred-effects/README.md) →
[unsolved practice](practice/README.md). Predict before opening recorded observations.

## 2. Real problem and forces

Our synthetic backend encodes a finite stream of text items into byte payloads.

| Concern | Promise or change |
|---|---|
| Stable workflow | Preserve order and duplicates; encode each consumed item once. |
| First implementation | Plain UTF-8 encoding. |
| New callers | Add different prefixes without duplicating the batch traversal. |
| State requirement | Count successful encodings for one owner. |
| Deferred work | Prepare a write now, execute it later in the same process. |
| Failure boundary | Stop on the first failure; do not silently retry or claim rollback. |

All inputs follow their annotations. Encoding may fail, for example for an unpaired
surrogate. These examples are synchronous and in memory. They are not a broker, streaming
transport, dependency-injection framework, or runtime validator for untrusted plugin code.

## 4. Formal mechanics, after the intuition

| Mechanism | What it provides | What it does not establish |
|---|---|---|
| Function | A named callable operation. | Purity, statelessness, or absence of global dependencies. |
| Closure | A function using bindings from an enclosing function scope. | A copied environment or recursively frozen configuration. |
| Bound method | A method coupled to its receiver. | A fresh receiver for every call. |
| Callable instance | An instance whose class defines `__call__`. | Thread safety, immutability, or suitability for this signature. |
| `functools.partial` | A callable with some arguments supplied in advance. | Deep copying or an unchangeable keyword configuration. |

The function and method relationships above are Python data-model mechanics, not a
pattern framework. User-defined functions expose closure cells through `__closure__`;
a bound method exposes its receiver through `__self__`.
[Python data model: callable types](https://docs.python.org/3.14/reference/datamodel.html#callable-types).

`callable(x)` is only a coarse capability check. It cannot prove that `x(text)` accepts
the required arguments, returns bytes, or honors an error/effect contract.
[Built-in `callable`](https://docs.python.org/3.14/library/functions.html#callable).

**Design-level interpretation:** choosing a replaceable encoder is Strategy-like;
packaging a particular write for later execution is Command-like. The role in the
collaboration determines that description. A lambda by itself is neither pattern.
The full pattern trade-offs belong to **SDP-BEH-010** and **SDP-BEH-040**.

## 5. Participants and responsibilities

| Participant | Responsibility | What it must not assume |
|---|---|---|
| Setup code | Choose/configure an encoder or sink and its lifetime. | That every caller can share mutable state. |
| `encode_batch` | Traverse input and invoke the chosen encoder. | Concrete subclass names or prefix rules. |
| Encoder | Convert one text item under its documented policy. | That the workflow will retry it after failure. |
| `CountingEncoder` | Delegate encoding and count successful returns. | That failed calls made no external changes. |
| Prepared action | Retain one payload and the sink reference needed later. | Undo, deduplication, or an open resource forever. |
| `run_actions` | Invoke actions in order and stop on error. | Transactions or reliable cross-process delivery. |

## 6. Collaboration and execution flow

```text
SETUP                 EXECUTION                       OBSERVABLE RESULT
make_prefix_encoder   encode_batch
("api/")              ├─ encode("alpha") ──────────> b"api/alpha"
   └─ returned encode └─ encode("beta")  ──────────> b"api/beta"

make_write_action     run_actions
(payload, sink)        └─ action() -> sink(payload, channel=...) -> effect
   └─ returned action    no automatic undo if a later action fails
```

### How to read this visual

The left column constructs a callable. The middle column invokes it later. Arrows on the
right identify results or effects. Construction of our action performs no write.

### Key insight

Separate the choice of behaviour, the data it retains, and the moment of execution.

### Simplification or limitation

This is a sequential call sketch. It omits source iteration errors and does not describe
threads, frames, object addresses, or a persistent queue.

## 7. Before-pattern code and concrete pain

[The executable starting point](examples/callable_tools.py) is `direct_batch`: a tuple
comprehension calling `text.encode("utf-8")`. For one fixed policy, it is sufficient.

When API payloads need `api/` and audit payloads need `audit/`, copying that traversal
creates multiple places to fix ordering, error propagation, and source handling. Adding
caller-name branches inside the traversal mixes selection with execution.

A traditional object design could pass an `EncoderStrategy` with an `encode` method.
That separates the policy correctly. A base class adds little here because the client
needs exactly one operation and no inherited algorithm. Python can pass that operation
directly. Retain a class when its state, lifecycle, or several related operations earn it.

## 8. Minimal Pythonic implementation

```python
from collections.abc import Callable, Iterable


def encode_batch(texts: Iterable[str], encode: Callable[[str], bytes]) -> tuple[bytes, ...]:
    return tuple(encode(text) for text in texts)


def make_prefix_encoder(prefix: str) -> Callable[[str], bytes]:
    def encode(text: str) -> bytes:
        return (prefix + text).encode("utf-8")

    return encode


api_encode = make_prefix_encoder("api/")
assert encode_batch(("ready", "ready"), api_encode) == (b"api/ready", b"api/ready")
```

There are two useful boundaries: one item versus a batch, and configuration versus use.
The factory is justified when a configured encoder must be handed to another component.
If you make only one direct call, `(prefix + text).encode("utf-8")` remains simpler.

The runnable version factors the one-item operation into `prefixed_utf8` so the same
operation can also be configured with `partial`. No registry or inheritance is required.

## 9. Typed implementation and an explicit effect boundary

`Encoder = Callable[[str], bytes]` describes a single positional argument and result.
For the sink, `channel` is keyword-only, so [the implementation](examples/callable_tools.py)
uses a callback `Protocol`:

```python
from typing import Protocol


class ByteSink(Protocol):
    def __call__(self, payload: bytes, /, *, channel: str) -> None: ...
```

The positional-only slash permits an implementation to name the payload parameter
differently. The `channel` name and its keyword support are part of the contract.
`Callable[..., None]` would give up those input checks. An implementation does not need
to inherit from this Protocol. These are static typing rules, not runtime enforcement.
[Typing specification: callables and callback protocols](https://typing.python.org/en/latest/spec/callables.html#callback-protocols).

`make_write_action` captures a `bytes` payload, a string channel, and the sink. The returned
zero-argument action calls the sink later. `MemoryWriter.write` shows a bound method used
as that sink. `CountingEncoder` shows a callable instance with an inspectable success count.

The count changes **after** the wrapped encoder returns successfully. It counts neither
attempts nor acknowledged durable writes. The counter starts at zero per instance; aliases
to one instance share it. This is an explicit example contract verified by the tests.

An `async def` call produces a coroutine object; it cannot replace our synchronous
bytes-returning encoder. An asynchronous boundary would need its own return type and
awaiting policy. [Python data model: coroutine functions](https://docs.python.org/3.14/reference/datamodel.html#coroutine-functions).

## 10. Choose the smallest useful form

| Need | Start with | Reconsider when |
|---|---|---|
| One fixed operation | Direct function call. | Another real caller varies the operation. |
| Swappable stateless operation | Function parameter. | Configuration needs to travel with the operation. |
| One configured operation | Closure or `partial`. | State needs naming, inspection, or a larger lifecycle. |
| Existing service with the right method | Pass its bound method. | The service's lifetime does not cover deferred calls. |
| Inspectable evolving state | Callable object or a named method on an object. | Several responsibilities have accumulated. |
| Several distinct operations | An object with descriptive methods. | Do not hide `reserve`, `commit`, and `cancel` behind one vague call. |

These are professional design judgments, not a rule that one form is always superior.
A one-line lambda can be a readable local expression; use `def` for a reusable operation
whose name, error path, or explanation matters.

## 11. Refactoring path

1. Characterize ordering, duplicates, errors, source consumption, and effects.
2. Identify the one decision that actually varies.
3. Accept a callable for that decision; keep selection in setup code.
4. Preserve the original function as a caller or compatibility entry point if needed.
5. Test a second implementation and its boundary cases.
6. Add configuration or state only when required; name its lifetime.
7. Remove speculative factories, base classes, and string dispatch from the stable workflow.

The [review-queue exercise](practice/README.md) asks you to do this in a different domain.
It deliberately does not provide a replacement implementation.

## 12. Realistic backend use case

A batch adapter accepts an encoder supplied by application setup. The adapter preserves
input semantics while the encoder chooses a wire representation. A dry run can use an
in-memory sink; the production shell owns connection setup, error reporting, and cleanup.

For deferred work in the **same process**, a callable may be enough. For work that must
survive a restart, prefer an explicit operation record with validated data and a versioned
handler contract. This is a design recommendation, not a guarantee supplied by a function.

Standard `pickle` stores ordinary functions by importable name, not their captured code
and environment. A local closure is not a general-purpose durable job format. A callable
instance is not automatically serializable either: its class and retained state matter.
[Python `pickle`: supported objects](https://docs.python.org/3.14/library/pickle.html#what-can-be-pickled-and-unpickled).

## 13. Failure scenarios and debugging

| Failure | Detection | Smallest useful response |
|---|---|---|
| Passing `encode(text)` as the dependency | Setup performs work; later call receives the wrong object. | Separate the operation from its result. |
| All loop callbacks use the last setting | Call after construction and compare outputs. | Decide whether each callback needs a distinct binding or a value snapshot. |
| A caller mutates retained configuration | Old and new calls unexpectedly differ. | Document live configuration or create an intentional snapshot. |
| One shared callable owns request-local state | Two callers affect the same count or allowance. | Move construction to the correct lifetime boundary. |
| A sink records data and then raises | Error occurs but an effect is already visible. | Preserve error context; do not assume retry is safe. |
| A deferred action outlives its connection | The retained object still exists but the resource is closed. | Execute within the resource scope or reacquire through an explicit owner. |

The [binding experiment](experiments/EXP-01-binding-and-aliases/README.md) distinguishes
mutation from rebinding. The [effects experiment](experiments/EXP-02-deferred-effects/README.md)
shows retained effects and repeated writes. Neither effect rollback nor deduplication is
implemented in this unit's runner.

## 14. Testing strategy

| Check | What it establishes | What it must not freeze |
|---|---|---|
| Fixed input/output cases | Exact public encoding and selection behaviour. | Internal class counts. |
| Recording callable | Invocation order, multiplicity, and skipped later work after failure. | Which helper name was called. |
| Error before/after an effect | Partial effects and exception propagation. | An assumption that failure means no effect. |
| Repeated and interleaved owners | Whether configuration and counters are shared. | Private storage representation in ordinary contract tests. |
| Static checking | Signature compatibility, including keyword-only parameters. | Runtime behaviour or business invariants. |
| Runtime probe | The particular binding/alias observation under the recorded runtime. | A universal benchmark or CPython memory map. |

The probes inspect cells only to answer a mechanism question. Production contract tests
should normally assert behaviour. Relevant commands and actual results are in
[practice](practice/README.md) and [VALIDATION.md](VALIDATION.md).

## 15. Observability and state lifetime

Give an operation a stable application label when logging it. Log the policy label,
configuration version, outcome, and safe request identifier at the owning boundary;
do not dump captured payloads or credentials. Not every callable has a useful `__name__`:
`partial` does not create one automatically.
[Standard library: partial objects](https://docs.python.org/3.14/library/functools.html#partial-objects).

Before sharing a callable, answer: who constructed it, who can mutate what it retains,
when its resource stops being valid, and whether two invocations may overlap.
Keeping an object reachable does not keep a closed file or expired connection usable.

## 16. Concurrency and state safety

The examples are deliberately sequential. A closure with `nonlocal` and an instance with
a mutable counter both need an explicit sharing policy. Neither syntax establishes safe
concurrent access. Per-request construction or immutable configuration is often easier to
reason about; a truly shared owner needs suitable synchronization and a documented contract.
No thread, task, process, race, or throughput experiment was run here.

Use `nonlocal` to rebind an existing enclosing function variable. Merely mutating an
object, such as `items.append(x)`, does not rebind the name `items`. Assignment without
the required declaration can make the name local and cause `UnboundLocalError`.
[Python execution model: name resolution](https://docs.python.org/3.14/reference/executionmodel.html#resolution-of-names).

## 17. Performance and memory limits

There is no measured speed ranking here. Pick the clearest correct boundary, then measure
a representative workload if invocation overhead matters. Our batch implementation holds
the resulting tuple in memory; a very large stream may need a separate streaming contract.

A captured large object can remain reachable as long as the callable retains it. That is
a lifetime concern, not proof of a leak. These examples do not measure byte sizes, object
destruction timing, interpreter optimizations, or garbage-collector behaviour.

## 18. Binding is not copying

| Construction | What later calls use | Effect of mutating the original list |
|---|---|---|
| Closure reads enclosing `values` | The object currently bound to that name. | Visible while that binding refers to the list. |
| Default argument set to `values` | The original retained object when the argument is omitted. | Visible; a default is not a deep copy. |
| `partial(tuple_of, values)` | The retained positional argument object. | Visible. |
| Intentional `tuple(values)` snapshot | A new tuple containing those element references. | Appending to the original list is not visible. |

Defaults are evaluated when the definition executes, not on every call. They are also
parameters: a caller can explicitly supply a replacement. Our snapshot contains only
integers; a tuple containing mutable elements would still share those elements.
[Python function definitions: defaults](https://docs.python.org/3.14/reference/compound_stmts.html#function-definitions).

`partial` binds arguments; later keyword arguments can override stored keywords. Its
configuration is not an authorization boundary. Python 3.14 adds `functools.Placeholder`
for positional holes; these examples use ordinary `partial` and work on Python 3.11.
[Standard library: partial](https://docs.python.org/3.14/library/functools.html#functools.partial).

The loop probe uses settings `2`, `5`, and `8`, then invokes every reader **after** the
loop. The shared-binding readers all see the last setting. This applies to `def` as
well as lambda; the separate factory and default-argument controls test different binding
choices. [Python FAQ: functions defined in loops](https://docs.python.org/3.14/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result).

## 19. Related units and scope boundaries

| Related unit | Relationship | What belongs there |
|---|---|---|
| [SDP-PYT-020](../../../CURRICULUM.md#sdp-pyt-020) | Next mechanism after passing one callable. | Selecting callables by key; defaults, ordering, and registry boundaries. |
| [SDP-BEH-010](../../../CURRICULUM.md#sdp-beh-010) | Strategy collaboration. | Policy selection and fuller Strategy trade-offs. |
| [SDP-BEH-040](../../../CURRICULUM.md#sdp-beh-040) | Command collaboration. | Queues, retry, audit, and undo design. |
| [SDP-PYT-030](../../../CURRICULUM.md#sdp-pyt-030) | Callables can wrap other callables. | Decorator syntax versus the Decorator pattern. |
| [SDP-PYT-070](../../../CURRICULUM.md#sdp-pyt-070) | Callback contracts. | Wider Protocol, ABC, and interface design judgment. |
| [SDP-FND-090](../../../CURRICULUM.md#sdp-fnd-090) | State ownership. | Deeper mutability and lifetime reasoning. |
| [SDP-ARC-040](../../../CURRICULUM.md#sdp-arc-040) | Keep effects explicit. | Functional Core, Imperative Shell architecture. |

## 20. When to use it

- A stable workflow has one changing decision or effect boundary.
- A caller needs to provide behaviour without imposing an inheritance hierarchy.
- Configuration should travel with a small operation.
- A local action should execute later under an explicit owner.

## 21. When not to use it

- One direct call already handles the actual need.
- The collaboration requires several distinct operations or explicit lifecycle methods.
- Captured mutable state would hide a critical ownership or authorization decision.
- The request needs durable delivery, rollback, or idempotency; a callable alone does not supply them.

## 22. Common misuse and overengineering

| Misuse | Why it hurts | Better move |
|---|---|---|
| One subclass per tiny formula | More navigation than behaviour. | Start with a named function. |
| Calling every function “Strategy” | Confuses mechanism with collaboration. | Identify the varying decision and its client first. |
| Capturing a whole request in a long-lived closure | Hides retained data and its lifetime. | Retain only needed values or explicit dependencies. |
| A universal `Callable[..., object]` registry | Defers signature mistakes and selection policy. | Use a narrow contract; registries are a separate need. |
| Adding reset/close/configure functions around a complex closure | The closure has become an implicit object API. | Consider an object with meaningful methods. |
| Catching every exception and trying another callable | Can duplicate effects and conceal failures. | Define failure and retry policy at the owning boundary. |

## 23. Interview preparation

Begin with one question: **“A batch workflow needs a configurable per-item rule. What
would make you choose a function, a closure, or a callable object?”** Wait for the answer.

A strong answer identifies the changing behaviour, calling contract, configuration,
state owner, failure semantics, and a simpler alternative. It does not rank syntax by
sophistication. Then probe only the missing step: introduce shared mutable state, a
keyword-only argument, or a restart requirement. Do not reveal all follow-ups at once.

Weak-answer traps include “closures copy variables,” “all callables are pure,” “a class
is automatically thread-safe,” and “a command automatically supports retry and undo.”
Use a small counterexample and ask for a corrected explanation before replacement code.

## 24. Closed-book revision cues

1. Reconstruct the setup → invocation → result/effect distinction.
2. Explain `f` versus `f()` without using a memorized definition.
3. Predict the difference between mutation and rebinding for each retained reference.
4. Identify which calls share a counter and why.
5. Refactor the independent lab while preserving the original observations.
6. Reject one unnecessary abstraction and explain a deferred-action failure.

For **SDP-PYT-020**, carry forward the distinction between selecting a callable and
invoking it. Material publication makes the repository ready for that next initialization;
it does not claim that these revision checks or this unit's learner practice are complete.

## 25. Vocabulary and professional English

### Capture

| Item | Content |
|---|---|
| Pronunciation | KAP-cher |
| Simple English meaning | Keep or record something for later use. |
| Hindi cue | बाद के लिए रखना |
| Design meaning | Retain a binding or object reference needed by a callable; not necessarily copy it. |

Natural examples:

1. The camera captures a picture.
2. Please capture the decision in the notes.
3. This diagram captures the main relationship.
4. **Interview:** The closure captures a binding; it does not freeze the whole environment.
5. **Engineering discussion:** Capture only the values this delayed operation needs.

### Defer

| Item | Content |
|---|---|
| Pronunciation | dih-FUR |
| Simple English meaning | Arrange for something to happen later. |
| Hindi cue | बाद के लिए टालना |
| Design meaning | Separate preparation of an operation from its execution. |

Natural examples:

1. We deferred the meeting until Friday.
2. The team deferred an optional purchase.
3. I will defer that decision until the evidence arrives.
4. **Interview:** This callable defers execution but does not provide durable storage.
5. **Engineering discussion:** If we defer the write, who keeps the connection usable?

## 26. Python Mastery references

These exact links come from [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md).
They are navigation references; their external lesson contents were not reviewed here.

- Hard bridge: [PY-FIT-030 — Higher-order functions, callable objects, and side effects](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-fit-030).
  Pass and return a callable; identify the effect when it runs.
- Hard bridge: [PY-FIT-040 — Closures, free variables, and late binding](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-fit-040).
  Predict which enclosing binding an inner function reads.
- Optional: [PY-TYP-060 — Callable typing, overloads, ParamSpec, and Self](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-typ-060).
  Basic `Callable` is sufficient to begin; ParamSpec and overloads are not prerequisites here.

## 27. Authoritative sources

Read on **2026-08-31**; original prose and synthetic examples are used throughout.

1. [Python 3.14 data model: callable types](https://docs.python.org/3.14/reference/datamodel.html#callable-types) — functions, closure attributes, bound methods, instances, and coroutines.
2. [Python 3.14 execution model: name resolution](https://docs.python.org/3.14/reference/executionmodel.html#resolution-of-names) — bindings, free names, and `nonlocal`.
3. [Python 3.14 function definitions](https://docs.python.org/3.14/reference/compound_stmts.html#function-definitions) — construction and default evaluation.
4. [Python 3.14 functools: partial](https://docs.python.org/3.14/library/functools.html#functools.partial) — retained arguments, keyword overrides, and the 3.14 Placeholder addition.
5. [Typing specification: callables](https://typing.python.org/en/latest/spec/callables.html) — positional signatures, keyword-only callback protocols, and assignability.
6. [Python 3.14 programming FAQ: loop-defined functions](https://docs.python.org/3.14/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result) — late lookup and default-argument controls.
7. [Python 3.14 built-ins: callable](https://docs.python.org/3.14/library/functions.html#callable) and [pickle: supported objects](https://docs.python.org/3.14/library/pickle.html#what-can-be-pickled-and-unpickled) — limits of capability checks and persistence assumptions.

## 29. Durable clarification log

| Date | Clarification | Why it belongs in canonical notes | Source or evidence |
|---|---|---|---|
| 2026-08-31 | Capture, mutation, rebinding, and copying are different decisions. | Prevents unstable configuration and accidental state sharing. | [Binding probe](examples/binding_probe.py) and the nearby language references. |
| 2026-08-31 | Preparing an action supplies neither rollback nor safe replay. | Prevents accidental duplicate effects after failure. | [Effects probe](examples/effects_probe.py) and worked contract tests. |
