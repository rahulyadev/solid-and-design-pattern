# SDP-STR-030 — Decorator

## Physical Notebook Core

### Problem or change pressure

Two notice previews need the same source text with independently optional labels, brackets, and
observations. Subclasses for every combination duplicate policy; scattered flags make order hard to see.

### One-sentence mental model

> Put a compatible capability around another capability, add one responsibility, and delegate the rest.

### One essential visual

```text
client → Observed → Bracket → Label → MemoryText
           render(key) travels inward →
           ← "[note: ready]" is built outward
owner ───────────────────────────────→ closes MemoryText
```

### How to read this visual

Horizontal arrows mean calls through the same `render` capability. Work reaches the leaf, then its
result travels back through Label, Bracket, and Observed. The separate arrow identifies the owner.

### Key insight

The outside object is the client's entry point; result transformations happen from inside to outside.
Compatible signatures permit nesting. Compatible behavior makes the nesting useful.

### Simplification or limitation

This is a conceptual success trace, not memory layout. It omits exceptions and observer failure.
The root owns the source; the wrappers in this example borrow it and do not expose `close`.

### Governing rules or invariants

1. Describe the whole contract: inputs, result meaning, effects, failures, order, and lifetime.
2. Keep each wrapper's responsibility small and make the composition order explicit.
3. A wrapper is a distinct object. Matching a method name does not make it universally transparent.

### Minimal Python example

```python
from collections.abc import Callable


def bracket(render: Callable[[str], str]) -> Callable[[str], str]:
    def wrapped(key: str) -> str:
        return "[" + render(key) + "]"

    return wrapped


assert bracket(lambda key: "ready")("N-1") == "[ready]"
```

A callable is enough for one operation. Object wrappers become useful when named capabilities,
configuration, state, and inspection help the client and maintainer.

### One common misconception

**Mistake:** Every Python `@decorator` implements the GoF Decorator pattern.

**Correction:** `@` applies a transformation at definition time. It can register and return the same
object, replace it, or wrap it. GoF Decorator describes compatible objects collaborating through layers.

### Important trade-offs

- Reusable combinations reduce subclass duplication but introduce order and lifetime decisions.
- A small seam is easy to wrap; a huge interface creates a forwarding maintenance burden.
- Added behavior changes something observable. State precisely which promises remain compatible.

### Interview-revision cues

- Recognition: optional behaviors combine differently for different clients.
- Trace: construct inside out, enter outside in, transform return values inside out.
- Rejection: one fixed formatting rule may belong in an ordinary function.

## Unit metadata

| Field | Value |
|---|---|
| Domain | GoF structural patterns |
| Curriculum | [SDP-STR-030](../../../CURRICULUM.md#sdp-str-030) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Add behaviour by wrapping compatible objects, preserve the wrapped contract, and compare object decorators with Python function decorators. |
| Hard prerequisites | [SDP-FND-050](../../../CURRICULUM.md#sdp-fnd-050), [SDP-PYT-030](../../../CURRICULUM.md#sdp-pyt-030) |
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

Frequency labels are curriculum judgments, not measured statistics. Learning remains **Not started**.
Authoring and maintainer checks supply material, not learner evidence. Start with the
[worked demo](examples/run_decorator_demo.py), then the [unsolved lab](practice/README.md).
The [controlled experiment](experiments/EXP-01-order-and-effects/README.md) supports explanation and
debugging without adding X to the canonical evidence profile. See [actual validation](VALIDATION.md).

## 1. Simple explanation and prerequisite bridge

Imagine a preview panel asking, “Render notice N-1.” The source knows the stored words. A label layer
adds a prefix. A bracket layer encloses what it receives. An observation layer records the size of
what passes through it. The client still makes one `render` call, regardless of the chosen combination.

From SDP-FND-050, reconstruct three distinct ideas: composition stores a collaborator; delegation
calls it; inheritance creates a class relationship. These wrappers store and call another TextSource.
They do not inherit its storage implementation. Foundation notes exist, but their presence does not
prove Rahul has practiced them.

SDP-PYT-030 is currently absent in synchronized main. The minimum bridge is: a function can receive
another callable and return a wrapper; `@outer` above `@inner` applies them as `outer(inner(function))`;
`functools.wraps` helps metadata, not semantic equivalence. Sections 9–10 verify the needed mechanics.
This bridge does not initialize or author that other unit.

## 2. Real problem and forces

Stable need: obtain a configured plain-text presentation of an existing notice. Variable needs:
which source supplies it, which decorations surround it, and which stage should be observed.
A label is not always outside brackets. Different preview clients need different arrangements.
No request sends a notice or changes stored content.

| Design | Good fit | Pressure or cost |
|---|---|---|
| Direct expression | One caller, one fixed presentation | Repeated policy changes require edits in several callers |
| Helper function | Repeated fixed policy, dependencies already available | Nested ad hoc calls may hide named configuration |
| Function wrapper/closure | One operation, a little captured configuration | State and several related methods can become awkward |
| Composition-based object decorators | Independently reusable behaviors and per-client stacks | Extra objects, delegation, order, diagnostics, and lifetime policy |
| Inheritance combinations | A small, stable family of honest subtypes | Optional axes create many combinations; order becomes MRO-dependent |
| Universal wrapper registry | A demonstrated runtime plugin requirement | Otherwise hides a simple expression behind discovery, flags, and configuration |

Three binary options already have eight presence/absence combinations before considering order.
This arithmetic illustrates the pressure, not a demand to create eight subclasses. Often one function
with two explicit transformations remains easier. Earn an abstraction with a concrete change.

## 3. GoF intent and formal definition

Decorator adds responsibilities to selected objects through compatible wrappers, allowing combinations
to be assembled without a subclass for each combination. The GoF authors' publisher-hosted
[Related Patterns discussion](https://www.informit.com/articles/article.aspx?p=1398600&seqNum=2)
identifies unchanged interface and recursive composition as key distinctions from Adapter.
This is the original-author excerpt read here; access to the full Decorator chapter is not claimed.

Thomas Minka's [Decorator notes](https://alumni.media.mit.edu/~tpminka/patterns/Decorator.html)
also describe forwarding around added actions and warn that wrapper identity differs from subject
identity. Our implementation and notices are original Python teaching material. No historical GUI
example, source diagram, or memory-manipulation technique is reproduced or required.

At the design level, an object implements a component contract while holding another object with
that contract. It delegates the shared operation and adds responsibility around that operation.
Because the delegate can itself be a decorator, layering repeats. This structure does not require
an abstract Decorator superclass; a single Protocol and ordinary composition are sufficient here.

## 4. Participants and responsibilities

| Participant | Here | Owns | Must not own |
|---|---|---|---|
| Client | `preview` | The requested key and use of the presentation | Knowledge of concrete layer classes |
| Component contract | `TextSource` | The narrow `render` capability | Storage administration or arbitrary object APIs |
| Concrete component | `MemoryText` | A copied text snapshot and explicit closed state | Labels, brackets, observation policy |
| Concrete decorators | `Label`, `Bracket`, `Observed` | One named added behavior each | The borrowed source's lifetime |
| Composition root | Demo `main` | Wiring, layer order, source cleanup | Presentation implementation |

[TextSource](examples/text_contract.py) is imported by clients and implementations. The root imports
concrete classes. The base has no reference to its wrappers. `Observed` takes a callable rather than
inventing an observer hierarchy for one method.

## 5. Collaboration, order, and self-calls

```text
root constructs: MemoryText → Label(base) → Bracket(label) → Observed(bracket)

client: render("N-1")
  Observed: enter try
    Bracket: call inner
      Label: call inner
        MemoryText: "ready"
      Label: "note: ready"
    Bracket: "[note: ready]"
  Observed: emit Observation("ok", 13), return SAME received string

reverse just two layers:
  Label(Bracket(base), "note: ") → "note: [ready]"
```

### How to read this visual

The first row is construction order. Indentation is call depth. Lines after each inner call show the
return transformation. The second expression keeps the same leaf and changes only the nesting.

### Key insight

“Both options enabled” does not specify a behavior. The order is part of configuration and testing.
Observation placement decides whether the measured result contains the decorations.

### Simplification or limitation

This is a conceptual sequential trace of the included code. It omits observer failures and control
exceptions. It is not a browser rendering, network trace, or benchmark.

Delegating `inner.render(key)` binds `self` to the inner object. If that method calls `self.other()`,
the call stays on that inner object; it does not jump back to the outer wrapper. Python's
[instance-method model](https://docs.python.org/3.14/reference/datamodel.html#instance-methods)
explains this binding. A returned `self`, callback holding the base, or saved bound method can also
bypass later wrapping. Avoid promising whole-object interception when you wrap one explicit method.

## 6. Before-pattern code and concrete pain

Each Python fence is independently runnable with `examples` on `PYTHONPATH`.

```python
from text_components import MemoryText

base = MemoryText({"N-1": "ready"})
try:
    preview_text = "[" + "note: " + base.render("N-1") + "]"
    assert preview_text == "[note: ready]"
finally:
    base.close()
```

This is clear for one fixed output. The pressure arrives when multiple clients independently decide
label order, bracket order, and whether observations count source characters or displayed characters.
Duplicating those decisions is the problem; string concatenation itself is not a design smell.

A `LabelledMemoryText` subclass could add a prefix. Adding a bracketed file source then makes storage
choice and presentation interact in the class family. Cooperative mixins can work, but every mixin
must respect method signatures and `super` conventions, and MRO order becomes public behavior.
Composition makes per-object arrangement visible without coupling wrappers to storage subclasses.

## 7. Minimal Pythonic object implementation

```python
from text_components import Bracket, Label, MemoryText
from text_contract import TextSource

base = MemoryText({"N-1": "ready"})
source: TextSource = Bracket(Label(base, "note: "))
try:
    assert source.render("N-1") == "[note: ready]"
    assert base.render("N-1") == "ready"
finally:
    base.close()
```

The implementation is two tiny frozen dataclasses, each with `inner: TextSource` and an explicit
`render` method. Label prepends its configured text; Bracket encloses its inner result. They need no
base Decorator class and no unknown-attribute forwarding. `eq=False` keeps equality at object identity
for these wrappers, rather than accidentally equating differently owned layer objects by their fields.
These [dataclass options](https://docs.python.org/3.14/library/dataclasses.html#dataclasses.dataclass)
control generated assignment/equality behavior; they do not freeze borrowed dependencies.
`Observed` also has mutable diagnostic state.

“Dynamic” here means choosing objects and wiring at runtime. Existing references still point to their
old objects if a root assigns a new wrapper to a variable. Reconfiguration should build a new stack
and hand it to new clients deliberately. No class mutation or hidden rewiring is required.

## 8. Typed implementation and the full contract

Read [text_components.py](examples/text_components.py), then use this view of the public promise:

| Dimension | Contract in this example | What would break it |
|---|---|---|
| Inputs | Every string key, including empty, is delegated unchanged | New validation rejects keys the source accepts |
| Success | Configured plain-text presentation; empty stored text is valid | Returning bytes, a coroutine, or silently treating failure as empty text |
| Source effects | Exactly one delegation per wrapper call; no consumption, storage edits, or retries | Rendering twice to measure the result; cache hits skipping an observable read |
| Transformations | Label and Bracket preserve the original text within documented additions | Claiming the result is byte-for-byte stored content |
| Failures | Underlying ordinary exceptions keep their identity; wrappers do not translate them | Catching errors and returning a successful placeholder |
| Observation | One optional success/error observation per ordinary completion at that layer | Mandatory audit disguised as best-effort telemetry |
| Ownership | Root closes the source; render-only wrappers borrow it | An inner layer unexpectedly closes a shared source |
| Trust | Typed application values, synthetic keys/text, plain text only | Treating brackets as HTML escaping, encryption, or sanitization |

A client that demands the exact stored text cannot substitute Label for MemoryText even though mypy
accepts both as TextSource. Our shared contract explicitly allows configured presentation. The stronger
base-specific promise is available only to callers deliberately depending on that base behavior.
This is why “same interface” must include meaning, not just spelling.

Python's [typing specification](https://typing.python.org/en/latest/spec/protocol.html#assignability-relationships-with-other-types)
uses structural member compatibility for Protocol assignability. A class need not inherit TextSource.
The [typing checks](examples/test_typing_contract.py) accept the assembled stack and a typed function
wrapper, then reject a byte-returning source and an integer argument. Static typing does not verify
one delegation, exception identity, ownership, or semantic honesty. Behavioral tests do that.
We do not use `runtime_checkable` as a substitute for validation.

`Observed` wraps only the source call in its error-detection `try`. A source exception triggers an
error observation and bare `raise`; a successful return triggers a success observation. Its separate
`_record` boundary drops **ordinary observer exceptions**, increments `dropped`, and returns. That
broad catch is deliberate only for expendable diagnostics. `BaseException` control flow escapes.
An observer control exception can replace an otherwise successful return or an in-flight source
exception; this is explicitly outside the ordinary-exception preservation promise.

There is no rollback, retry, or transactional success in this layer. Observer failure cannot undo a
source read. If audit delivery is essential, use an explicit audited operation with a failure contract;
do not silently reuse this optional observer.

## 9. Function wrappers and Python `@` syntax

A helper can implement a fixed composition directly; the notebook example returns a closure for
reusable one-operation wrapping. Use an object when a named capability or retained state helps.
Functions are not a less serious design.

[function_wrappers.py](examples/function_wrappers.py) contains a generic `traced` decorator using
[`ParamSpec`](https://docs.python.org/3.11/library/typing.html#typing.ParamSpec), `TypeVar`, and `wraps`.
It preserves the parameter/return types for static callers while adding trace entries. The list sink is assumed to work, so it has a different failure policy from
Observed. It records exit on failure through `finally`; “exit” is not “success.”

```python
from function_wrappers import order_probe

assert order_probe() == (
    "evaluate:outer",
    "evaluate:inner",
    "apply:inner",
    "apply:outer",
    "enter:outer",
    "enter:inner",
    "body",
    "exit:inner",
    "exit:outer",
)
```

The [language reference](https://docs.python.org/3.14/reference/compound_stmts.html#function-definitions)
specifies definition-time expression evaluation and nested application. Read the three phases
separately: decorator factory expressions evaluate top down; resulting decorators apply bottom up;
when this returned wrapper is called, execution enters outside in. Importing a module can execute
the first two phases because definitions execute. They do not wait for the first function call.

For [class decorators](https://docs.python.org/3.14/reference/compound_stmts.html#class-definitions),
the class object is passed to the decorator and the returned value is bound to the class name.
A registration decorator can append that class to a registry and return it unchanged. Tests demonstrate
this without creating any wrapper instances. Syntax alone therefore does not establish pattern intent.

## 10. Metadata, introspection, and version boundaries

`functools.wraps` uses `update_wrapper`: it copies selected metadata, updates the wrapper dictionary,
and sets `__wrapped__`. The 3.14 defaults also copy `__type_params__` (added in 3.12); the
[3.11 documentation](https://docs.python.org/3.11/library/functools.html#functools.update_wrapper)
and [3.14 documentation](https://docs.python.org/3.14/library/functools.html#functools.update_wrapper)
show the version distinction. It does not restore identity, behavior, resource ownership, or the
wrapper's actual argument-binding implementation. It also does not manufacture a type-safe wrapper;
the ParamSpec annotations serve static callers.

[`inspect.signature`](https://docs.python.org/3.14/library/inspect.html#inspect.signature) follows
`__wrapped__` by default. With `follow_wrapped=False`, our wrapper's parameter names are `args` and
`kwargs`. `inspect.unwrap` reaches the original function. Introspection can show the advertised
signature even while the wrapper still performs different effects. `__wrapped__` access is a bypass,
not an authorization mechanism.

Python 3.14 adds `annotation_format` to `inspect.signature` and makes annotations lazy by default;
see the [annotation rules](https://docs.python.org/3.14/reference/compound_stmts.html#annotations).
This unit uses Python 3.11 syntax and does not depend on annotation evaluation timing, the new
parameter, or 3.12 generic type-parameter syntax. Do not evaluate untrusted annotations merely to
prove a wrapper's behavior. The verification compares parameters and local trusted functions.
No CPython layout claim follows from the observed outputs.

### A narrow special-method boundary

```python
class Forward:
    def __getattr__(self, name):
        return getattr([1, 2], name)


wrapper = Forward()
assert wrapper.__len__() == 2
try:
    len(wrapper)
except TypeError:
    pass
else:
    raise AssertionError("implicit len must not come from __getattr__")
```

For implicit protocols, Python generally looks for special methods on the type, bypassing normal
instance lookup; see [special-method lookup](https://docs.python.org/3.14/reference/datamodel.html#special-method-lookup).
A real sequence wrapper must deliberately implement the intended sequence operations. The same
review question applies to iteration and context management. Our TextSource needs only `render`, so
adding a generic transparent-object framework would solve a problem it does not have.

## 11. Refactoring path

1. Characterize existing output, failures, and number of underlying calls before moving policy.
2. Name the actual independent variation: label/bracket order across preview clients.
3. Extract the smallest render seam. Keep the original direct implementation available as a baseline.
4. Move one formatting responsibility into a callable or object wrapper; preserve current behavior.
5. Assemble the existing order at the root and rerun tests. Add a second order only when required.
6. Decide where observations belong, including their failure and data-retention policy.
7. Remove flags/subclasses made redundant by the extraction; keep useful direct functions.

Passing output tests while doubling source calls is a failed refactor. Preserving every internal
class name is unnecessary. Preserve behavior the client relies on, then make the new capability clear.

## 12. Realistic backend use case and lifecycle

A service produces internal notice previews for two consumers: one requests a label inside brackets,
another uses the plain source. Give each a configured TextSource at application construction. An
optional observation sink measures presentation length without receiving the key or text itself.
The sample performs no HTTP, file I/O, database access, or notice delivery.

MemoryText copies input mapping data to establish a stable snapshot. Its `close` models an explicit
owner-managed capability shutdown; it does not hold an operating-system handle. The root's
`try/finally` closes it even on failure. Two wrappers can share it, so neither closes it during render.
The root may retain the base for lifetime operations; ordinary clients receive only the narrow seam.

If a real wrapper owns a file, spell out close delegation, flush order, repeated close, use-after-close,
and partial initialization cleanup. If it borrows the file, root lifetime must outlast every user.
Do not infer ownership from the word Decorator. For comparison, the library's
[`IOBase.close`](https://docs.python.org/3.14/library/io.html#io.IOBase.close) is idempotent and
includes flushing; that library-specific contract is not automatically inherited by our wrapper.
Real `close` can fail. This synthetic source's close cannot, and the demo does not model competing
cleanup failures.

## 13. Failure, observation, and debugging

A common mistake is observing a result by calling `inner.render(key)` a second time. That can repeat
an effect or read a different value. Save one result, measure that result, and return it. Another is
logging in a `finally` block that raises and masks the original source failure.

The [failure tests](examples/test_decorator.py) inject a source error and an observer error together.
They assert the original source exception object reaches the client, exactly one source call occurs,
and an observer failure is counted. Successful rendering still succeeds under ordinary observer
failure. The `dropped` counter means the observer raised; it does not prove that no observation
was recorded. A sink can append an event and then fail, as a separate test demonstrates.
This does not make observation durable or independent of observer latency.

When debugging, first record the root's stack description, then identify where each observation was
made. In the experiment, observation inside formatting counts 5 characters; outside counts 13. Both
counts are correct for different scopes. `len(str)` counts Unicode code points, not UTF-8 bytes or
user-perceived graphemes; our test contrasts `é` with its two encoded bytes. See the
[Python text-sequence definition](https://docs.python.org/3.14/library/stdtypes.html#text-sequence-type-str).
A size log is not evidence that a notice was delivered. Avoid storing raw notice content in logs.
The toy counter is inspectable locally; no monitoring backend or secure audit is implemented.

## 14. Testing strategy

| Check | What it establishes | Limit |
|---|---|---|
| Baseline comparison | Original plain text is unchanged at the leaf | It does not prove every composition is valid |
| Order examples and generated text | Exact configured output, including empty/Unicode/newline text | Only the documented transforms are modeled |
| Common contract cases | Key handling, failures, one delegation, borrowed lifetime | A Protocol assignment alone cannot establish these |
| Failure injection | Source exceptions survive ordinary observer errors; no retry | No distributed partial-write or cancellation simulation |
| Observation placement | Counts match the layer's result, not an assumed global scope | The probe measures characters, not time |
| Typing controls | Valid stack/call accepted; wrong result and argument rejected | No runtime validation of arbitrary external objects |
| Function/class probes | Definition/application/call order, metadata, class registration | No framework integration or universal callable introspection |
| Starter characterization | Existing quote behavior and unsolved target | No learner completion claim |

[Focused tests](examples/test_decorator.py), [syntax tests](examples/test_function_wrappers.py), and
[typing controls](examples/test_typing_contract.py) use synthetic data and temporary files. Test
contract observables rather than hard-coding a universal number of wrappers. One-call assertions are
justified here because exactly one delegation is a documented boundary, not a universal Decorator law.

From the repository root, use an existing locked interpreter (`python` below) and route generated
state outside the repository before running tools:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-str-030/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-str-030/mypy
export RUFF_CACHE_DIR=/tmp/sdp-str-030/ruff
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-str-030/hypothesis
export UV_CACHE_DIR=/tmp/sdp-str-030/uv-cache
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-str-030/uv-env
export COVERAGE_FILE=/tmp/sdp-str-030/coverage
mkdir -p /tmp/sdp-str-030/pytest
python units/structural/SDP-STR-030-decorator/examples/run_decorator_demo.py
python units/structural/SDP-STR-030-decorator/examples/order_effects_probe.py
python units/structural/SDP-STR-030-decorator/examples/function_wrappers.py
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-str-030/pytest/focused units/structural/SDP-STR-030-decorator
python -m mypy --strict --python-version 3.11 units/structural/SDP-STR-030-decorator
python -m mypy --strict --python-version 3.14 units/structural/SDP-STR-030-decorator
python -m ruff check --target-version py311 units/structural/SDP-STR-030-decorator
python -m ruff format --check units/structural/SDP-STR-030-decorator
python scripts/validate_repo.py
```

Set `PYTHONPATH` to the absolute `examples` directory when running extracted README snippets.
For whole-repository regression, isolate existing test directories to avoid repeated module names;
export MYPY_CACHE_DIR for the **complete** run because older tests invoke mypy internally.
Actual interpreter paths and observed results are recorded separately in VALIDATION.md.

## 15. Concurrency, async, performance, and memory

These examples are synchronous and sequential. Frozen wrapper configuration does not freeze the
borrowed source, observer, or source lifetime. `MemoryText.calls`, `Observed.dropped`, and sink lists
are mutable shared state. No thread-safety claim or concurrency test is made. A real shared service
must decide whether to serialize the complete operation, use a thread-safe sink, or build per-request
state; adding a lock layer also changes reentrancy and lock-order obligations. Never hold a lock
across an arbitrary callback without examining what it can call.

An async TextSource would need an explicit awaitable contract. A synchronous wrapper can otherwise
observe coroutine construction instead of completed work. Cleanup belongs around the awaited
operation, and cancellation must remain visible. Python's
[asyncio cancellation guidance](https://docs.python.org/3.14/library/asyncio-task.html#task-cancellation)
recommends cleanup and propagation; CancelledError derives directly from BaseException. No async
variant is implemented here, and a sync observer's BaseException test is not an async cancellation test.

A chain with k wrappers has k additional dispatch steps and retains k wrapper objects plus their
references. In these text wrappers, every layer can construct another string. Cost depends on lengths
at each layer; if prefixes grow the result, summing intermediate lengths matters. Very deep chains
also consume call depth. These are deductions from this code, not benchmark measurements. Do not
claim “negligible overhead” without a relevant workload. A fixed pipeline in one function may allocate
less and be easier to profile. Root-held wrappers also keep sources/sinks reachable; explicit close
manages the resource contract instead of relying on object collection timing.

## 16. Contract-changing variants and misuse

| Proposed layer | Contract question | Better decision when the answer is unclear |
|---|---|---|
| Cache | Are freshness, key/tenant scope, shared returned objects, and skipped calls acceptable? | Make cached lookup explicit or define its consistency contract |
| Retry | Which errors, attempts, deadline, cancellation, and duplicate effects are permitted? | Keep recovery at a boundary with documented idempotency |
| Log/observe | Can failure or blocking prevent success? What data is retained? | Separate optional diagnostics from mandatory audit |
| Authorization | Can clients reach the inner object? Does it check current identity each time? | Enforce access at the protected capability and control references |
| Compression/encryption | Does the return still mean plain text in the same encoding? | Expose an honest encoded-payload contract |
| Resource wrapper | Who closes, flushes, and handles cleanup failure? | Choose an explicit owned or borrowed lifetime |

These are design review questions, not claims that the example implements those production features.
Even a library cache that is internally thread-safe can invoke the underlying function more than
once for overlapping misses, per [`functools.lru_cache`](https://docs.python.org/3.14/library/functools.html#functools.lru_cache).
A wrapper name supplies no stronger guarantee.

Other misuses include wrapping a giant object with `__getattr__` and promising total transparency;
peeling through `.inner.inner` in ordinary client code; wrapping the same source twice accidentally;
and inventing a metaclass-driven chain builder for two known options. Keep stack construction visible.
If mandatory order creates many invalid stacks, a fixed named composition or explicit feature API
may be safer than arbitrary mixing. Optional internal access is convenient, but it is not a trust boundary.

## 17. Related patterns and bounded comparisons

| Related unit | Connection | Boundary |
|---|---|---|
| [SDP-STR-010](../../../CURRICULUM.md#sdp-str-010) | Adapter also wraps a collaborator | Its main intent is interface translation |
| [SDP-STR-020](../../../CURRICULUM.md#sdp-str-020) | Facade also delegates | It offers a simpler subsystem task rather than recursive same-capability layers |
| [SDP-STR-040](../../../CURRICULUM.md#sdp-str-040) | Proxy can have similar structure | Its intent is access/representation policy; name the behavioral difference |
| [SDP-STR-050](../../../CURRICULUM.md#sdp-str-050) | Composite also uses recursive contracts | Its primary relationship is whole/parts rather than one wrapped capability |
| [SDP-PYT-030](../../../CURRICULUM.md#sdp-pyt-030) | Python decorator syntax | Definition transformation is distinct from pattern intent |

These links locate other owners. They do not initialize those units or substitute for their evidence.

## 18. When to use it and when to keep things simpler

Use wrappers when several clients need different combinations, a narrow contract is stable, and
order/effect/lifetime policy can be explained. Prefer explicit object wrappers when named configuration
and diagnostic state make maintenance easier. Prefer closures when one operation and little state fit.

Keep a direct expression or helper for a stable fixed sequence. Put mandatory business rules in an
explicit feature when arbitrary stacks would be invalid. If callers need many concrete methods or
identity-sensitive operations, redesign the seam before attempting universal forwarding.
The senior answer includes the smallest design that meets the actual change, not the most patterns.

## 19. Interview preparation

Use these prompts one at a time in a live session; wait for an attempt and diagnose the exact missing
reasoning step before providing a hint or replacement answer.

| Prompt | Exact gap to check |
|---|---|
| Define Decorator using this preview service. | Does the answer connect independent optional behavior to the shared capability? |
| Predict Label(Bracket(base)) versus Bracket(Label(base)). | Does it distinguish call entry order from result transformation order? |
| A source returns bytes but has `render`. Can it substitute? | Does it check result meaning and type beyond method spelling? |
| Mypy accepts a caching wrapper; the counter test fails. Which contract changed? | Does it connect skipped calls/freshness/effects to substitution? |
| A success observer raises; now the client sees failure. Review it. | Does it explicitly choose optional observation versus mandatory audit? |
| Two clients share a source. Who calls close? | Does it identify ownership rather than delegate every method automatically? |
| Does wraps make a function identical to the original? | Does it separate metadata, identity, execution, and advertised signature? |
| Can a base method calling self.render re-enter the outer wrapper? | Does it trace the actual receiver and references? |
| A file source replaces MemoryText. What must be revalidated? | Does it ask about I/O errors, lifecycle, effects, and blocking? |
| Remove the pattern if only one fixed format remains. | Can it justify a simpler expression or function without losing the contract? |

Weak-answer traps: “Decorator avoids all inheritance,” “all decorators are transparent,” “@ always
wraps,” “frozen means thread-safe,” and “logging cannot affect behavior.” A strong answer makes a
specific promise, tests it under change/failure, and names what remains unsupported.
Likely follow-up: add a deadline, mutable return value, mandatory audit, or a third client that requires
raw data. Explain which assumptions fail before writing another wrapper.

## 20. Closed-book revision and evidence route

1. Reconstruct the notebook diagram, roles, construction order, and return path.
2. State the smallest contract that permits the two formatting wrappers honestly.
3. Explain one compatible effect and one incompatible effect with the same signature.
4. Refactor the [quote lab](practice/README.md), preserving your original attempt.
5. Diagnose a changed order or failure and test the boundary you claim.
6. Transfer to another scenario, or reject Decorator with a simpler design and a reason.

E is your explanation; I is your implementation and tests; D is debugging or refactoring with
a corrected assumption; T is selecting or rejecting this design for a changed production scenario. Generated examples,
a green maintainer suite, and this document do not satisfy those learning evidence thresholds.
For NotebookLM, use only the approved note and permitted curriculum context after approval. Do not
upload drafts, the progress tracker, raw attempts, lab solutions, source trees, or tool logs; follow
[the repository policy](../../../docs/NOTEBOOKLM.md). No upload has been performed.

## 21. Vocabulary and professional English

### Delegate — DEL-uh-gayt

| Item | Content |
|---|---|
| Simple meaning | Ask another person or part to carry out work |
| Hindi cue | काम सौंपना |
| Design meaning | Forward the operation to the collaborator that owns it |

1. I delegate the scheduling to the coordinator.
2. The lead delegates one clearly bounded task.
3. Delegating work does not remove responsibility for the outcome.
4. **Interview:** Each wrapper delegates once through the same render capability.
5. **Engineering:** We can delegate storage access while keeping presentation here.

### Compatible — kum-PAT-uh-bul

| Item | Content |
|---|---|
| Simple meaning | Able to work together under the required conditions |
| Hindi cue | साथ काम कर सकने वाला |
| Design meaning | Satisfies the promises the client depends on |

1. These two connectors are compatible.
2. Our schedules are compatible this week.
3. A similar label does not prove two parts are compatible.
4. **Interview:** Compatible signatures are necessary here but do not prove compatible behavior.
5. **Engineering:** Check whether the cached result is compatible with our freshness promise.

## 22. Python Mastery references

The direct hard mapping is [PY-FIT-050 — Decorators](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-fit-050).
Reconstruct a closure, application order, and wraps metadata before practicing object stacks.
For the composition prerequisite, the relevant mappings are
[PY-OBJ-010 — Classes, instances, methods, and construction](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-010),
[PY-OBJ-020 — Properties, encapsulation, and composition](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-020), and
[PY-OBJ-030 — Inheritance, MRO, and super](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-030).
These are the exact repository mappings read in PYTHON_REFERENCES.md, not a claim that the external
notes were inspected or that their exercises were completed.

## 23. Authoritative sources and claim boundaries

Sources below were opened/read for this unit. Important claims are linked near their use.

1. GoF authors, [publisher excerpt: Related Patterns](https://www.informit.com/articles/article.aspx?p=1398600&seqNum=2): compatible interface and recursive composition. Only this excerpt, not the full Decorator chapter, was read.
2. Thomas Minka, [Decorator notes](https://alumni.media.mit.edu/~tpminka/patterns/Decorator.html): original discussion of wrapping, variable responsibilities, and identity. Used selectively; no implementation-specific hot swapping is adopted.
3. Python [function/class definitions and annotations](https://docs.python.org/3.14/reference/compound_stmts.html): language mechanisms and 3.14 annotation behavior.
4. Python [functools 3.14](https://docs.python.org/3.14/library/functools.html) and [3.11](https://docs.python.org/3.11/library/functools.html): wraps, metadata defaults, and cache limits.
5. Python [inspect](https://docs.python.org/3.14/library/inspect.html): signature, follow_wrapped, unwrap, and version overlay.
6. Python [data model](https://docs.python.org/3.14/reference/datamodel.html): bound methods and implicit special-method lookup.
7. Python typing [Protocols specification](https://typing.python.org/en/latest/spec/protocol.html): structural assignability.
8. Python [I/O lifecycle](https://docs.python.org/3.14/library/io.html#io.IOBase.close), [asyncio cancellation](https://docs.python.org/3.14/library/asyncio-task.html#task-cancellation), and [text sequences](https://docs.python.org/3.14/library/stdtypes.html#text-sequence-type-str): bounded library/language comparisons.
9. Python [dataclasses](https://docs.python.org/3.14/library/dataclasses.html#dataclasses.dataclass) and
   [ParamSpec](https://docs.python.org/3.11/library/typing.html#typing.ParamSpec): generated methods and
   typed callable forwarding.

The contract and domain are original design choices. Static diagnostics are tool results. Probe outputs
are CPython observations on the recorded versions that illustrate documented mechanics. No framework
behavior, security enforcement, live service, browser render, or measured performance is claimed.
