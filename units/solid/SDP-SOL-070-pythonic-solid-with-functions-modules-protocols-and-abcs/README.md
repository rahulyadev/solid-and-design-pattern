# SDP-SOL-070 — Pythonic SOLID with functions, modules, Protocols, and ABCs

## Physical Notebook Core

### Problem or change pressure

A caller needs interchangeable behaviour. Copying an interface hierarchy into Python can
hide the actual need: sometimes it is one operation; sometimes a small capability or an
owned family with shared implementation.

### One-sentence mental model

> Describe the caller's promise, then choose the smallest Python shape that can keep it.

### One essential visual

```text
caller --needs--> contract --can be supplied by--> function / object / module
                              optional reuse --> an owned ABC family
```

### How to read this visual

Read left to right. Arrows mean design relationships, not imports or inheritance.
A function fits a callable contract; a module fits a compatible named-member contract.

### Key insight

SOLID does not require class hierarchies. The collaboration and its promises matter.

### Simplification or limitation

This is conceptual. The shapes are not interchangeable under every interface, and an ABC
does not certify behaviour. No Python memory layout or execution timing is depicted.

### Governing rules or invariants

1. Keep policy independent of the selected implementation's details.
2. Match the needed operations, call signature, results, errors, and state promises.
3. Add structure only for a real change pressure; type checks do not replace contract tests.

### Minimal Python example

```python
from collections.abc import Callable


def name_line(name: str, render: Callable[[str], str]) -> str:
    return render(name)


assert name_line("Asha", str.upper) == "ASHA"
```

### One common misconception

**Mistake:** “An ABC or a Protocol makes an implementation satisfy SOLID.”

**Correction:** It expresses part of a boundary. You still have to justify that boundary
and check behaviour, errors, state ownership, and dependency direction.

### Important trade-offs

- A function is easy to pass; named members can make a richer capability clearer.
- A Protocol supports independent implementations; an ABC couples an owned family for reuse.

### Interview-revision cues

- One operation: why is a callable insufficient?
- Named capability: what exactly does this client use?
- Shared base: what real implementation or extension rule earns the inheritance?

## Unit metadata

| Field | Value |
|---|---|
| Domain | SOLID principles |
| Curriculum | [SDP-SOL-070](../../../CURRICULUM.md#sdp-sol-070) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Apply SOLID to dynamically typed Python using functions, callables, modules, Protocols, ABCs, and explicit data rather than Java-style interface hierarchies. |
| Hard prerequisites | [SDP-FND-070](../../../CURRICULUM.md#sdp-fnd-070), [SDP-FND-100](../../../CURRICULUM.md#sdp-fnd-100), [SDP-SOL-060](../../../CURRICULUM.md#sdp-sol-060) |
| Soft prerequisites | None specified by the curriculum |
| Priority | Core |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D3 |
| Scope | SOLID, Python |
| Size | L |
| First understanding | 4–6 h |
| Hands-on practice | 5–9 h |
| Evidence profile | E+I+D+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Approved |

The frequency labels are curriculum judgments, not survey results. Runtime experiments
support this unit; they do not add a required X outcome to its canonical evidence profile.

## 1. Simple explanation

Imagine handing a colleague a job. If the job is “format this name,” a function is enough.
If the colleague must also tell you the document's content type, name those two needs.
If your own team maintains several variants of one shared algorithm, a base class may help.
The shape follows the job.

The prerequisite notes exist, but the tracker does not establish that Rahul has studied
them. This bridge is enough to begin:

- **SDP-FND-070:** duck typing uses the supported operation at runtime; structural typing
  compares an interface; nominal typing recognizes a declared type relationship.
- **SDP-FND-100:** modules are namespaces and code boundaries. Separate the module choosing
  a provider from the module expressing the caller's needs.
- **SDP-SOL-060:** first identify the client, the change pressure, and the behavioural promise.
  One coherent boundary can address several SOLID concerns.

## 2. Real problem and forces

Our worked example prepares event badges. A tiny script originally prints an event and an
attendee name. That direct function is appropriate for one format.

Now a kiosk needs JSON, a text printer needs the existing spelling, and a caller needs a
content type that agrees with the document. Some layouts have configuration. Separately,
an internal team wants staff and visitor layouts to share one framing algorithm.

These are distinct pressures. Do not make the JSON layout inherit the internal framing
base just because both produce badges. Do not require printer access, plugin discovery,
or a factory registry in code whose job ends at returning a document.

## 4. Formal definition and Python application

Pythonic SOLID applies the principles to functions, modules, data, and objects. It does not
introduce a different set of principles. The following is an application to this example;
see [SDP-SOL-060](../SDP-SOL-060-solid-interactions-tensions-and-trade-offs/README.md#4-formal-definitions-and-diagnostic-questions)
for their formal concerns and original sources.

| Principle | Question here | Small Python expression |
|---|---|---|
| SRP | Do layout edits disturb request validation? | Separate policy from representation. |
| OCP | Can another known format fit the existing caller? | Supply an implementation at composition time. |
| LSP | Does the replacement still represent the attendee and event and expose failures? | Test the semantic contract, not only the signature. |
| ISP | Does this caller need printing, editing, or registration? | Expose only `render` and `content_type` here. |
| DIP | Must badge policy import the JSON or printer implementation? | Express its own needs; choose details elsewhere. |

### Mechanism comparison

| Mechanism | Good reason to use it | What it does not provide |
|---|---|---|
| Direct function/module call | One stable local implementation is sufficient. | Automatic isolation from a concrete imported detail. |
| Passed function | One operation varies. | A business contract merely by being callable. |
| Closure | One operation needs a small captured configuration. | Automatically immutable captured objects. |
| Callable instance | Configuration or lifecycle needs a visible owner. | Thread safety or good boundaries merely by being a class. |
| Protocol | A client needs a named, statically checkable shape without requiring inheritance. | Runtime validation or inherited implementation for implicit implementers. |
| Module implementing a Protocol | Stateless functions and attributes already form the capability. | Separate per-request state. |
| ABC | An owned extension family benefits from shared implementation and abstract hooks. | Signature or behavioural correctness from runtime membership alone. |
| Dataclass | Values need explicit names and useful generated methods. | Business validation or deep immutability by default. |

**Typing mechanics:** an implicit Protocol implementation need not inherit or import the
Protocol. A compatible module is valid too; its function signatures are compared without
the Protocol method's `self`. [Typing specification: Protocols and module implementations](https://typing.python.org/en/latest/spec/protocol.html#modules-as-implementations-of-protocols).

**Language mechanics:** defining `__call__` on a class makes its instances callable. This
is ordinary dispatch, not a new dependency-injection framework.
[Python data model: callable objects](https://docs.python.org/3.14/reference/datamodel.html#object.__call__).

## 5. Participants and responsibilities

| Participant | Responsibility | What it must not own |
|---|---|---|
| `run_badge_demo.py` | Construct data and select a layout. | Duplicate the policy's validation. |
| `BadgeRequest` | Carry the attendee and event as explicit values. | Discover or construct providers. |
| `prepare_badge` | Validate the request and return a finished document. | JSON encoding, role layout rules, or printing. |
| `BadgeLayout` | State the capability used by this caller. | Every feature offered by a vendor. |
| Layout module/object | Represent the values and report the matching content type. | Decide whether a request is accepted. |
| `BadgeDocument` | Carry representation and metadata together. | Claim physical printing or delivery occurred. |

Dataclasses generate methods; they do not inspect annotation types for general validation.
`frozen=True` prevents ordinary field reassignment, not mutation of nested mutable values.
These records contain strings; `prepare_badge` explicitly checks the business preconditions.
[Dataclasses: decorator and frozen instances](https://docs.python.org/3.14/library/dataclasses.html).

## 6. Collaboration and execution flow

```text
Source imports in examples/ (standard library omitted):
run_badge_demo.py --> badge_policy.py
                 --> plain_badges.py
                 --> badge_layouts.py
                 --> owned_layouts.py
                 --> callable_choices.py (separate name-only demonstration)

Runtime for the selected layout:
prepare_badge --> layout.content_type
              --> layout.render(attendee, event=event)
              <-- text
caller        <-- BadgeDocument(content_type, body)
```

### How to read this visual

The top arrows are literal imports. The lower arrows are member access, a call, and returns.
`BadgeLayout` is declared inside `badge_policy.py`; the providers need not import it.

### Key insight

Policy calls a concrete implementation at runtime while remaining independent of its
source module. Structural typing does not require an extra provider-to-Protocol import.

### Simplification or limitation

The runtime portion condenses several statements. It omits failure branches, printing,
and networking; the example performs no external delivery. It is not a memory diagram.

Trace one request: reject blank values, read the content type, reject blank metadata,
render once, reject blank output, and return the document. Other layout exceptions propagate.
The caller can then choose an output destination. A successful return means prepared text,
not “printed,” “sent,” or “durably stored.”

Explore the [interactive mechanism comparison](visuals/mechanism-chooser.html) with its
[reading guide](visuals/README.md).

## 7. Before-pattern code and concrete pain

For already accepted text input, the original formatter can be this small:

```python
def text_badge(attendee: str, event: str) -> str:
    return f"{event}\n{attendee}"


assert text_badge("Asha", "Open Lab") == "Open Lab\nAsha"
```

Keep it while there is one stable format. The problem arrives when selection, JSON details,
metadata, and request rules grow together. A factory interface for this original function
would solve no demonstrated problem.

## 8. Minimal Pythonic implementation

The earlier name-only requirement uses [callable_choices.py](examples/callable_choices.py).
`render_names` accepts `Callable[[str], str]`; the same call works with a plain function,
the result of `make_prefix`, or a `NamePrefix` instance. All preserve order and duplicates.
The closure captures one prefix; the callable instance makes that configuration visible.
Neither needs an ABC.

This is Strategy-like collaboration expressed with Python callables. That description is
design interpretation, not a claim that every higher-order function needs a pattern name.

`Callable[[str], str]` describes a simple call signature. When a callable contract needs
named keyword-only parameters, a Protocol with `__call__` can express them. Type annotations
are not enforced by Python's call machinery.
[Typing: callable annotations](https://docs.python.org/3.14/library/typing.html#annotating-callable-objects).

```python
from typing import Protocol


class RenderCall(Protocol):
    def __call__(self, attendee: str, /, *, event: str) -> str: ...
```

This optional shape is not another required layer. Use it if the client wants the callable
itself; use the named layout capability below when it also needs metadata.

## 9. Typed production-oriented implementation

Read [badge_policy.py](examples/badge_policy.py), then the independent
[module layout](examples/plain_badges.py) and [configured JSON layout](examples/badge_layouts.py).
`BadgeLayout` has exactly the two members this caller uses. The property advertises a read
capability; it does not make every provider's metadata immutable.

```python
import plain_badges
from badge_layouts import JsonBadgeLayout
from badge_policy import BadgeRequest, prepare_badge

request = BadgeRequest("Asha", "Open Lab")
text_document = prepare_badge(request, plain_badges)
json_document = prepare_badge(request, JsonBadgeLayout(indent=2))
assert text_document.content_type != json_document.content_type
```

Run this excerpt with `examples/` on the import path, or run the complete
[composition example](examples/run_badge_demo.py) using the practice commands.
No nominal inheritance connects these providers to `BadgeLayout`.

For the separate owned-family requirement, [owned_layouts.py](examples/owned_layouts.py)
uses an ABC: `render` shares the framing skeleton and calls the abstract `name_line` hook.
The staff and visitor subclasses supply that hook. The policy still accepts `BadgeLayout`;
external providers do not inherit the skeleton. This is a small Template Method variant,
not the default form of every layout.

**Standard-library mechanics:** an incomplete regular ABC subclass cannot be instantiated.
Virtual registration changes membership without supplying inherited methods or applying the
same abstract-method gate. Neither mechanism proves postconditions.
[ABC documentation: registration and abstract methods](https://docs.python.org/3.14/library/abc.html).

## 10. Simpler Python alternative

If one format is sufficient, call its function directly. If metadata is constant for the
whole application, pass one renderer and that constant at the composition point. If only a
prefix differs, configuration data plus one function may replace several classes.

The named Protocol is useful here because every selected layout brings both representation
and metadata. An ABC is useful only for the additional shared-skeleton requirement. You may
reject either choice when your actual constraints are smaller.

## 11. Refactoring path

1. Characterize exact existing output, accepted inputs, and failures.
2. Identify what now varies; do not generalize every function.
3. Pass one operation before inventing a provider hierarchy.
4. Introduce a named capability only when the client benefits from its shape.
5. Move concrete selection to the composition point and inspect imports.
6. Test the new implementation against its semantic and format-specific promises.
7. Remove unused factories, marker bases, and speculative lifecycle methods.

The [reading-room exercise](practice/README.md) applies this process to a different contract.
Its new integration remains unsolved.

## 12. Realistic backend use case

A request handler can construct a badge request, select a configured layout during application
setup, and return the prepared document with its content type. Do not put web-framework types
inside the layout contract unless the policy needs them. Keep authentication, payload parsing,
delivery, retries, and transport error translation at their actual boundaries.

This is an architectural extension scenario; no framework server or real kiosk is included.

## 13. Failure scenario and experiments

A plugin exposes the correct method name but accepts different arguments. Another accepts
the arguments yet drops the attendee's name. Both can pass a runtime Protocol membership
test; only the first necessarily raises during the call. A silent semantic failure needs
an explicit behavioural check.

`@runtime_checkable` checks member presence, not signatures or business rules. Ordinary
Protocols do not opt in to these membership checks. The lookup mechanism changed in Python
3.12; our probe uses ordinary methods and avoids dynamic attribute tricks.
[Typing: runtime-checkable Protocols](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable).

- [EXP-01: Protocol boundary](experiments/EXP-01-protocol-boundary/README.md) compares membership,
  call success, and one explicit postcondition.
- [EXP-02: ABC boundary](experiments/EXP-02-abc-boundary/README.md) separates abstract construction,
  virtual membership, inherited implementation, and stored results.

Contain a malformed implementation at its integration boundary. Do not return a fake successful
document, and do not retry a renderer with side effects without understanding those effects.

## 14. Testing strategy

| Check | What it proves here | What it does not prove |
|---|---|---|
| Characterization | Existing text, order, duplicates, and missing-item behaviour remain stable. | That every old behaviour is desirable. |
| Behaviour/contract | Supplied implementations preserve values, formats, and visible failures in tested cases. | Universal substitutability for every future provider. |
| Type checker | Concrete module/object/callable signatures fit their declared uses. | Content truth, operational availability, or effects. |
| Runtime experiment | Specific membership and dispatch observations on recorded interpreters. | Complete validation of arbitrary plugins. |
| Design review | Each boundary has a client and a reason to exist. | That class count or passing tests measures design quality. |

The practice baseline tests intentionally do not implement or test the future integration.
Do not weaken a meaningful assertion simply to make a new design pass.

## 15. Observability and debugging

When diagnosing a failed request, separate input rejection, layout selection, rendering,
and delivery. In a real service, record a safe request identifier, selected layout name,
stage, and exception category. Do not log attendee data by default. A wrong content type is
a representation contract failure even when the body is nonblank.

## 16. State ownership and lifetime

Ordinary imports normally reuse the named module object from `sys.modules`. Consequently,
mutable module state can be shared by callers using that module; it is not per-request
configuration. [Import system: module cache](https://docs.python.org/3.14/reference/import.html#the-module-cache).

Our module layout is stateless. A configured instance is clearer when two callers need
different simultaneous configuration. A closure can also own configuration, but capturing
a mutable object does not copy it. If a provider later owns a connection or mutable cache,
define who creates, shares, synchronizes, and closes it. Neither Protocol nor ABC answers
those lifecycle questions. No concurrency or performance benchmark is claimed here.

## 18. Variants

- Use a bound method when an existing instance owns the operation; no wrapper is needed.
- Return explicit result data when collaborators need outcomes, not a command hierarchy.
- Give different clients different Protocol views of one coherent implementation if needed.
- Keep asynchronous completion as an explicit contract change; returning a coroutine is not
  substitutable for an already completed string in these synchronous callers.

## 19. Related patterns and combinations

| Related unit | Relationship | Key difference |
|---|---|---|
| [SDP-SOL-060](../../../CURRICULUM.md#sdp-sol-060) | Diagnostic prerequisite | Decides which principle is under pressure. |
| [SDP-PYT-010](../../../CURRICULUM.md#sdp-pyt-010) | Mechanism depth | Explores functions, closures, and callable objects further. |
| [SDP-PYT-070](../../../CURRICULUM.md#sdp-pyt-070) | Interface depth | Develops practical Protocol/ABC interface mechanics. |
| [SDP-BEH-010](../../../CURRICULUM.md#sdp-beh-010) | Strategy collaboration | Focuses on interchangeable algorithms. |
| [SDP-BEH-060](../../../CURRICULUM.md#sdp-beh-060) | Template Method collaboration | Focuses on a shared algorithm with varying hooks. |
| [SDP-SOL-080](../../../CURRICULUM.md#sdp-sol-080) | Next unit | Critiques overapplication and preserves legacy behaviour while refactoring. |

## 20. When to use it

Use these choices when a real variation, independent implementation, test seam, ownership
need, or shared extension skeleton makes the current direct design costly to change.
Name the force before choosing the mechanism.

## 21. When not to use it

Keep a direct function, small conditional, or configuration value when that fully expresses
the current requirement. You need not add a Protocol to every internal function. You need
not forbid useful classes to be Pythonic.

## 22. Common misuse and overengineering

| Misuse | Cost or failure | Better move |
|---|---|---|
| Interface + abstract factory + concrete factory for one prefix | Several names hide a string configuration. | Use data and a function. |
| Runtime Protocol check as plugin validation | Wrong signatures or wrong results still pass. | Static checks where possible and explicit boundary/contract checks. |
| Register an unrelated class to repair an ABC mismatch | Membership changes while missing behaviour stays missing. | Implement or adapt the actual required behaviour. |
| Put a vendor's whole API in a Protocol | The client remains coupled to details it does not need. | Express this client's vocabulary and operations. |
| Mutable global layout settings | Callers interfere through shared configuration. | Pass configuration or an owned instance. |
| Force all providers to inherit a shared skeleton | Independent providers acquire unnecessary coupling. | Keep the external capability structural. |

## 23. Interview preparation

Ask one question at a time and wait for Rahul's answer. Begin with:
**“A client needs one configurable operation. What would make you choose a function,
a closure, a callable instance, or an ABC?”**

Then adapt follow-ups: a keyword-only contract, two needed members, a module provider,
a shared algorithm, and finally a replacement that accepts the call but violates the result.
Do not turn this sequence into a memorized answer script.

Weak-answer traps include “Python does not need contracts,” “Protocol means runtime
validation,” “ABC guarantees LSP,” and “fewer classes always means better design.” A strong
answer identifies the missing force or promise and offers the smallest test or alternative.

## 24. Closed-book revision cues

Reconstruct the essential visual; distinguish source imports from runtime calls; explain
why a module fits the named Protocol; identify what each type mechanism cannot check;
refactor one needless hierarchy; and describe a requirement that genuinely earns an ABC.

Evidence still needs Rahul's own explanation, implementation/refactoring, tests, and transfer.
Generated notes and maintainer runs do not advance learning state.

## 25. Vocabulary and professional English

### Capability

| Item | Content |
|---|---|
| Pronunciation | kay-puh-BIL-uh-tee |
| Simple meaning | Something a person or system can do. |
| Hindi cue | क्षमता |
| Design meaning | An operation or small related set of operations a client needs. |

Examples: “The team gained a new capability.” “The device has limited capabilities.”
“We tested its recovery capability.” **Interview:** “This client needs one reading capability.”
**Engineering:** “Do not add editing methods to the read-only capability.”

### Conformance

| Item | Content |
|---|---|
| Pronunciation | kun-FOR-muns |
| Simple meaning | Meeting a stated rule or expectation. |
| Hindi cue | नियम के अनुरूप होना |
| Design meaning | Matching a declared interface; specify separately which behaviour is tested. |

Examples: “The review checks conformance.” “Conformance requires evidence.” “We found a
gap in conformance.” **Interview:** “Structural conformance does not establish the business
postcondition.” **Engineering:** “Add contract tests alongside the conformance check.”

## 26. Python Mastery references

These exact navigation references come from [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md),
through this unit's prerequisites and related mechanism units. They are not a new mapping
row, a claim that the external lessons were read, or a prerequisite progress update.

| Reference | Minimum bridge |
|---|---|
| [PY-TYP-050 — Protocols, ABCs, and structural versus nominal typing](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-typ-050) | Separate runtime operations, static shapes, and declared inheritance. |
| [PY-MOD-010 — Modules, packages, and executable modules](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-mod-010) | A module groups names and can be passed as an object. |
| [PY-MOD-020 — Import resolution, sys.path, and module caching](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-mod-020) | Reusing a module can reuse its mutable state. |
| [PY-MOD-030 — Circular imports and package boundaries](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-mod-030) | Keep composition outside stable policy. |
| [PY-FIT-030 — Higher-order functions, callable objects, and side effects](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-fit-030) | Functions and callable instances can be passed as dependencies. |
| [PY-FIT-040 — Closures, free variables, and late binding](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-fit-040) | A returned function can retain access to outer configuration. |
| [PY-TYP-060 — Callable typing, overloads, ParamSpec, and Self](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-typ-060) | Start with simple Callable; callback Protocols can describe named parameters. |

## 27. Authoritative sources

Sources opened for this unit on 2026-08-30; examples and explanations are original.

1. [Python 3.14 typing documentation](https://docs.python.org/3.14/library/typing.html): callable annotations, Protocol, and runtime-checkable Protocol.
2. [Typing specification: Protocols](https://typing.python.org/en/latest/spec/protocol.html): structural assignability and modules as implementations.
3. [Python 3.14 abc documentation](https://docs.python.org/3.14/library/abc.html): abstract methods and virtual registration.
4. [Python 3.14 data model](https://docs.python.org/3.14/reference/datamodel.html#object.__call__): calling instances.
5. [Python 3.14 import reference](https://docs.python.org/3.14/reference/import.html#the-module-cache): module cache and loading.
6. [Python 3.14 dataclasses documentation](https://docs.python.org/3.14/library/dataclasses.html): generated methods and frozen instances.

All supplied code uses Python 3.11-compatible syntax and APIs. See each experiment for actual
runtime observations. Design recommendations are contextual engineering judgments, not
language guarantees. There are no CPython layout, performance, or universal SOLID-score claims.
