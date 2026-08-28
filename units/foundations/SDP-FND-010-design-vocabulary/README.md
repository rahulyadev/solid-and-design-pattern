# SDP-FND-010 — Design vocabulary: principle, pattern, idiom, framework, and architecture

## Physical Notebook Core

Keep this section short enough to reconstruct by hand. It is not a duplicate of the full note.

### Problem or change pressure

A team sees the same code and calls it five different things. One person proposes an architectural
rewrite for a local coding choice; another treats a framework convention as a universal design rule.
The labels hide the real decision, so the team solves the wrong-sized problem.

### One-sentence mental model

> A principle guides judgment, a pattern names recurring design knowledge, an idiom expresses an
> idea naturally in a language, a framework runs an extensible skeleton, and architecture captures
> the system's fundamental structures and relationships.

### One essential visual

```text
Question being answered                         Best starting label
────────────────────────────────────────────────────────────────────
What should guide the decision?                 PRINCIPLE
What recurring design shape fits these forces?  PATTERN
How is this naturally expressed in Python?      IDIOM
What reusable runtime skeleton calls our code?  FRAMEWORK
What is fundamental across the whole system?    ARCHITECTURE

One feature may legitimately involve all five; this is not a size ladder.
```

### How to read this visual

Start with the question being answered, not the code's appearance. Read each row left to right.
If several rows apply, make several precise statements instead of forcing the feature into one box.

### Key insight

The labels classify different kinds of claims. They overlap, but they are not synonyms.

### Simplification or limitation

This is a conceptual classification aid, not a formal hierarchy or runtime model. Scope and control
are continua: an idiom can implement a pattern, a framework can embody patterns, and architecture
can constrain both.

### Governing rules or invariants

1. Identify the problem, forces, scope, and owner of control before naming a pattern.
2. Name the smallest accurate concept; syntax or a class name alone proves very little.
3. Treat design names as compressed reasoning, never as substitutes for that reasoning.

### Minimal Python example

```python
from collections.abc import Callable

Sender = Callable[[str], str]


def send_email(message: str) -> str:
    return f"email:{message}"


def send_sms(message: str) -> str:
    return f"sms:{message}"


senders: dict[str, Sender] = {"email": send_email, "sms": send_sms}


def notify(channel: str, message: str) -> str:
    return senders[channel](message)
```

The dictionary of callables is a Python idiom. It may participate in Strategy when it solves the
forces of interchangeable behaviour, but this snippet alone does not establish that pattern. It
says almost nothing about the application's framework or architecture.

### One common misconception

**Mistake:** “The code uses classes and dependency injection, so it has a design-pattern
architecture.”

**Correction:** Classes and injection are mechanisms. A pattern needs a recurring problem and
solution shape; architecture concerns fundamental system structures and relationships.

### Important trade-offs

- Shared names speed communication only when the team also states context, forces, and limits.
- Precise vocabulary takes a little longer than buzzwords, but prevents much larger design mistakes.

### Interview-revision cues

- Start with the decision's scope and the problem it solves, not a memorized definition.
- Contrast pattern with implementation and framework with architecture.
- Say explicitly when a plain Python idiom is sufficient and no named pattern is justified.

## Unit metadata

| Field | Value |
|---|---|
| Domain | Design foundations |
| Curriculum | [SDP-FND-010](../../../CURRICULUM.md#sdp-fnd-010) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) — no direct prerequisite mapping |
| Learning outcome | Distinguish the major levels of software-design knowledge and use names at the right level. |
| Hard prerequisites | None |
| Soft prerequisites | None |
| Priority | Core |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D1 |
| Scope | Design |
| Size | S |
| Evidence profile | E+D+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Draft |

The frequency fields above are curriculum judgments, not measurements from a population survey.

## 1. Simple explanation

These five words answer different questions:

- A **principle** helps you judge choices. It says what quality to prefer or what risk to watch.
- A **pattern** gives a named, reusable way to organize collaboration for a recurring problem.
- An **idiom** is a conventional way to express something in a particular language.
- A **framework** is reusable running software that supplies a skeleton and extension points.
- **Architecture** is what is fundamental about how the system is structured and how its important
  parts relate.

Imagine building a notification service:

- “Keep policy separate from volatile provider details” is guiding advice: a principle-level claim.
- “Wrap incompatible provider clients behind one interface” describes an Adapter-shaped solution:
  a pattern-level claim.
- “Store functions in a dictionary and call the selected function” is a natural Python expression:
  an idiom-level claim.
- “The web toolkit resolves a route and calls our handler” describes framework control.
- “The API writes to a durable queue and independent workers contact providers” describes a
  consequential system structure: an architecture-level claim.

All five descriptions can be true at once. They are different views of the same feature.

## 2. Why confused vocabulary causes real pain

Vocabulary errors are not merely academic. They change what a team builds.

| Confusion | Typical wrong move | Concrete cost |
|---|---|---|
| Idiom called a pattern | Adds interfaces and class families around a callable or mapping | More code without a new design seam |
| Framework called architecture | Lets one tool determine every boundary | Business rules become coupled to tool lifecycle and APIs |
| Pattern called a principle | Applies a solution name as a universal rule | Context and contraindications disappear |
| Architecture called a pattern | Treats a system-wide trade-off as a local recipe | Operational and organizational consequences are missed |
| Library called a framework | Assumes the wrong owner of control | Startup, callbacks, testing, and error flow surprise the team |

The stable concern is communication: a reviewer must understand what kind of claim is being made.
The changing concerns are language, tools, deployment topology, and the particular forces of a
problem. Good vocabulary keeps those levels separate while allowing them to connect.

## 3. Source-checked context

Software-pattern writing grew as a way to record recurring solutions whose useful shape survives
changes in language and technology. Martin Fowler emphasizes that a pattern names a recurring,
useful solution and must explain the problem, forces, alternatives, and when the solution does not
fit—not merely its class diagram ([Writing Software Patterns](https://martinfowler.com/articles/writingPatterns.html)).

Python's documentation uses “Pythonic” for code that follows common Python idioms instead of
carrying over another language's habits. Its example contrasts direct iteration with index-based
iteration ([Python glossary: Pythonic](https://docs.python.org/3/glossary.html#term-Pythonic)). This
supports a practical boundary: an idiom is tied more closely to a language and its community than a
language-independent design pattern is.

Inversion of control is a useful framework diagnostic: application code supplies extension
behaviour, while framework code coordinates the larger execution flow and calls those extensions.
Frameworks and libraries can be hybrids, so this is a strong characteristic rather than a mechanical
pass/fail law ([Martin Fowler, Inversion of Control](https://martinfowler.com/bliki/InversionOfControl.html)).

For architecture, the Software Engineering Institute describes the structure or structures of a
system in terms of software elements, their externally visible properties, and their relationships.
That puts architecture above private implementation details while still allowing multiple useful
structures ([SEI, Reflections on 20 Years of Software Architecture](https://www.sei.cmu.edu/blog/reflections-on-20-years-of-software-architecture-a-presentation-by-linda-northrop/)).

PEP 20 is explicitly informational guidance about Python's design philosophy, not executable
machinery or an application architecture. It is a useful example of principle-level guidance
([PEP 20 — The Zen of Python](https://peps.python.org/pep-0020/)).

## 4. Working definitions and boundaries

### Principle

A principle is general guidance used to evaluate or steer design decisions. It usually expresses a
desired quality or warns about a recurring risk. A principle does not prescribe one implementation.

Examples include preferring explicit dependencies, keeping responsibilities cohesive, and making
important failures visible. Principles can conflict in a concrete situation; judgment resolves the
tension.

**Test:** Could two different implementations both honour this advice? If yes, “principle” may be
the right level.

### Pattern

A design pattern is named, reusable design knowledge for a recurring context and problem. Its core
is a collaboration or structural solution shaped by forces and consequences, not a copied code
template.

A pattern description should answer:

1. In what context does the problem recur?
2. What forces make the obvious solution insufficient?
3. Which participants take which responsibilities?
4. How do they collaborate?
5. What improves, what becomes harder, and what alternatives exist?

**Test:** Can you explain the recurring problem and why the collaboration fits without mentioning a
specific framework or syntax? If not, the pattern claim is weak.

### Idiom

An idiom is a conventional, recognizably natural expression in a particular language or ecosystem.
It exploits the language's ordinary strengths.

Python examples include direct iteration, context managers for bounded cleanup, generators for lazy
production, decorators for function transformation, and dictionaries of callables for small
dispatch problems. An idiom may implement a pattern more economically than a textbook class
diagram, but the idiom and the pattern remain different claims.

**Test:** Would the advice likely change when moving from Python to a language without the same
construct? If yes, “idiom” is probably useful.

### Framework

A framework is reusable executable software that supplies part of an application's structure,
lifecycle, and extension contract. Application code plugs into it through callbacks, subclasses,
registration, configuration, decorators, or other hooks.

Inversion of control often distinguishes a framework from an ordinary library:

```text
Library:    application code ──calls──> library
Framework:  framework loop   ──calls──> application hook
```

Real packages may do both. A web framework can call route handlers while those handlers call the
framework's response helpers. Ask who owns each execution phase rather than attaching one permanent
label to every function in the package.

**Test:** Does reusable runtime code coordinate lifecycle or call application-supplied behaviour?
If yes, “framework” may be the right level.

### Architecture

Architecture captures the fundamental structures needed to reason about a system: important
elements, their externally visible properties, their relationships, and the constraints or
principles guiding their evolution. A codebase can have module, runtime, deployment, and data views;
no single box diagram contains every architectural fact.

The word “fundamental” matters. Renaming a private helper is normally not architecture. Choosing
whether requests synchronously update one database or publish durable work to independently scaled
workers can be architectural because it changes failure modes, consistency, deployment, ownership,
and operational qualities.

**Test:** Would changing this decision alter important system boundaries, qualities, or several
teams' assumptions? If yes, it may be architectural.

## 5. Three axes that separate the terms

The terms are easier to classify along three axes than on one ladder.

| Term | Primary kind | Typical scope | Is it executable? | Main diagnostic |
|---|---|---|---|---|
| Principle | Guidance | Broad; applied locally or globally | No | What quality guides the choice? |
| Pattern | Reusable design knowledge | Recurring collaboration or structure | No; implementations are | What forces and solution shape recur? |
| Idiom | Language-specific expression | Usually small and local | Its implementation is | What is the natural language expression? |
| Framework | Reusable software and extension contract | Application or subsystem runtime | Yes | Who owns the lifecycle and calls whom? |
| Architecture | Fundamental system structure and constraints | System or major subsystem | The system is; the architecture is an abstraction | What is structurally consequential? |

“High level” is therefore an unreliable shortcut. Principles can guide one line or a whole system.
A small framework can control a narrow test lifecycle. A pattern can appear inside an architectural
boundary without becoming the architecture.

## 6. One feature described at all five levels

Consider a service that accepts a notification request.

```text
Client
  |
  v
[HTTP framework] --calls--> create_notification(request)
                                |
                                v
                           [durable queue]
                                |
                                v
                              Worker
                                |
                     provider adapter selected
                                |
                                v
                       Email or SMS provider
```

### How to read this visual

Read top to bottom as a conceptual request flow. The framework owns the inbound callback. The
handler emits durable work. A worker later selects a provider-facing collaborator.

### Key insight

The framework is one executable participant. The queue/worker/provider boundaries form part of an
architectural view. Adapter or Strategy may describe local collaborations. A callable mapping may
be the Python idiom used to implement selection. A principle explains why volatile provider details
are kept away from stable notification policy.

### Simplification or limitation

This is not literal runtime timing or deployment documentation. It omits retries, transaction
boundaries, provider errors, security, observability, and the exact pattern forces. The diagram does
not prove that any named pattern is justified.

## 7. The same syntax can carry different design meaning

Consider the dictionary-of-callables example from the notebook core.

### Simplest reading: an idiom

The code replaces a small conditional with ordinary Python data and first-class functions. If the
set is tiny and stable, that may be the entire explanation needed.

### Pattern reading: only after forces appear

Suppose selection varies per customer, algorithms must be tested independently, and new behaviours
arrive without modifying the selection client. The same callable boundary may now implement the
core collaboration of Strategy. The pattern name compresses those forces and consequences; the
dictionary syntax does not prove them.

### Framework reading: only when a host owns control

If reusable host code discovers registered callables and invokes them at defined lifecycle points,
the registration may be a framework extension mechanism. The callables themselves are not “the
framework.”

### Architecture reading: only when the decision is fundamental

If independently deployed plugins are loaded into isolated worker processes, the plugin boundary
may be architectural. If one module imports a dictionary from another module, it usually is not.

## 8. A reliable classification method

When someone names a design concept, ask these questions in order:

1. **Claim:** What exact sentence are we trying to say?
2. **Problem:** What concrete change or failure makes the sentence useful?
3. **Scope:** One expression, one collaboration, one runtime skeleton, or the wider system?
4. **Control:** Who calls whom and who owns lifecycle?
5. **Portability:** Would the idea survive a change of language or framework?
6. **Consequences:** What becomes easier, and what becomes harder?

Then choose the narrowest accurate noun. Multiple nouns are acceptable when each labels a distinct
claim:

> “We use a dictionary-of-callables idiom to implement Strategy inside a web framework; the
> framework is not our architecture, although its request lifecycle constrains one architectural
> boundary.”

That sentence is more useful than “we use the Strategy architecture.”

## 9. Simplest non-pattern design and overengineered misuse

For two stable notification channels, the direct Python code may be enough:

```python
def notify(channel: str, message: str) -> str:
    if channel == "email":
        return send_email(message)
    if channel == "sms":
        return send_sms(message)
    raise ValueError(f"unsupported channel: {channel}")
```

Calling this “bad because it has an `if`” mistakes syntax for change pressure. A conditional becomes
painful only under particular rates and kinds of change.

An overengineered response might create an abstract factory, a provider hierarchy, a registry, a
dependency-injection container, and a plugin framework before a third channel or independent
extension need exists. Pattern vocabulary has then hidden speculation rather than clarified design.

Use this progression:

1. Keep the direct design while its costs are small.
2. Observe a real change force.
3. Introduce the smallest seam that contains that force.
4. Name a pattern only if the name adds accurate, reusable reasoning.
5. Revisit architecture only if fundamental boundaries or system qualities are affected.

## 10. Production and code-review judgment

### Review prompts

| Claim heard in review | Ask next | Strong evidence |
|---|---|---|
| “This follows a principle.” | Which quality and trade-off? | Two plausible choices compared |
| “This is Strategy.” | What varies, who selects, and why is substitution useful? | Recurring force plus collaboration |
| “This is Pythonic.” | Which Python capability makes it simpler? | Clearer ordinary construct and behaviour |
| “The framework handles it.” | Which lifecycle phase and callback contract? | Traceable call direction and error boundary |
| “This is our architecture.” | Which structure, stakeholders, and system qualities? | Consequential elements and relationships |

### Failure scenario: vocabulary inflation

A team describes every helper as a service, every class as a pattern, and every module boundary as
architecture. Reviewers can no longer distinguish a local refactor from a deployment decision.

Detection:

- design names appear without a stated problem or trade-off;
- diagrams show classes but omit call direction and system boundaries;
- a framework migration is described as a total architectural rewrite without evidence;
- proposed abstractions outnumber demonstrated variants.

Containment:

1. Rewrite each claim as “because X changes or fails, we choose Y, accepting Z.”
2. Draw the smallest relevant boundary and call direction.
3. Remove any label that adds no decision information.
4. Verify important behaviour with tests rather than class-name assertions.

## 11. Testing and observability boundaries

Vocabulary is evaluated through reasoning, but the implementation it describes is tested through
behaviour.

| Level | Useful evidence | Avoid overspecifying |
|---|---|---|
| Idiom | Same outputs, errors, and side effects after a Pythonic rewrite | Exact internal syntax |
| Pattern implementation | Participant contracts and changed-requirement behaviour | Textbook class names |
| Framework integration | Callback registration, lifecycle, error translation, and real boundary wiring | Framework internals not promised by its API |
| Architecture | Cross-boundary contracts, failure handling, quality scenarios, and deployment checks | One private implementation detail |

Observability also follows the boundary. A framework may provide request hooks and exception
handling, while the application must add business context. An architectural flow may require a
correlation identifier across API, queue, worker, and provider. Neither logging nor tracing makes a
design “architectural”; they make consequential runtime relationships visible.

## 12. Related curriculum units

| Related unit | Relationship | Key difference |
|---|---|---|
| [SDP-FND-020](../../../CURRICULUM.md#sdp-fnd-020) | Next foundation | Identifies change pressure, responsibilities, and boundaries in detail. |
| [SDP-FND-110](../../../CURRICULUM.md#sdp-fnd-110) | Principle judgment | Applies common heuristics without turning them into rigid laws. |
| [SDP-PYT-010](../../../CURRICULUM.md#sdp-pyt-010) | Pythonic mechanism | Uses functions, closures, and callable objects as design tools. |
| [SDP-PYT-030](../../../CURRICULUM.md#sdp-pyt-030) | Naming trap | Separates Python decorator syntax from the object Decorator pattern. |
| [SDP-ARC-080](../../../CURRICULUM.md#sdp-arc-080) | Architectural depth | Evaluates boundaries and evolutionary design at system scale. |
| [SDP-REF-090](../../../CURRICULUM.md#sdp-ref-090) | Misuse | Diagnoses unnecessary factories, abstraction layers, and pattern soup. |
| [SDP-INT-010](../../../CURRICULUM.md#sdp-int-010) | Transfer | Chooses the simplest design for a new scenario. |

## 13. When the vocabulary is useful

- During code review, to match a proposed change to the real decision scale.
- In interviews, to explain forces and trade-offs instead of reciting names.
- During framework adoption, to separate tool lifecycle from application boundaries.
- During architecture discussion, to keep fundamental relationships separate from local syntax.
- During refactoring, to choose an idiom or small seam before reaching for a full pattern.

## 14. When not to lead with a named pattern

- The direct function or conditional remains clearer and change is speculative.
- The team cannot state the recurring problem or forces.
- The proposed label describes only syntax, a package name, or a class suffix.
- A domain term communicates the responsibility more precisely than a generic pattern name.
- The decision is local and reversible, while “architecture” would exaggerate its impact.

## 15. Common misuse and better language

| Misuse | Why it fails | Better statement |
|---|---|---|
| “Django is our architecture.” | A framework is one dependency within a wider system structure. | “Django owns HTTP dispatch inside our modular-monolith architecture.” |
| “A dictionary is Strategy.” | The syntax does not reveal the forces or collaboration. | “A callable dictionary is our Python implementation; Strategy fits because behaviours vary independently.” |
| “SOLID is a framework.” | SOLID supplies design principles, not executable lifecycle code. | “We use a SOLID principle to evaluate this boundary.” |
| “The decorator pattern uses `@`.” | Python decorator syntax and object Decorator solve related but distinct problems. | “`@` applies a callable transformation; the object pattern wraps a compatible collaborator.” |
| “Microservices is a pattern that fixes coupling.” | A distributed architecture adds operational coupling and trade-offs. | “We chose service boundaries for stated ownership and scaling forces, accepting distributed failure.” |

## 16. Interview preparation

### A concise strong answer

> A principle guides decisions; it does not prescribe one structure. A pattern names reusable design
> knowledge for a recurring problem, forces, collaboration, and consequences. An idiom is the
> language-native expression, such as a callable dictionary in Python. A framework is executable
> reusable software that usually owns part of the lifecycle and calls application hooks.
> Architecture concerns the system's fundamental elements and relationships. They overlap: an idiom
> can implement a pattern inside a framework constrained by an architecture.

### Common formulations

1. What is the difference between a design principle and a design pattern?
2. Is dependency injection a pattern, a principle, a framework feature, or an idiom?
3. Why is a framework not the same as architecture?
4. Is a dictionary of callables the Strategy pattern?
5. Give an example where the simplest Python design needs no named pattern.

### Weak-answer traps

- Giving five dictionary definitions without one shared example.
- Treating the terms as a strict low-to-high hierarchy.
- Identifying a pattern from class names or UML shape alone.
- Claiming inversion of control is unique to dependency-injection containers.
- Saying architecture means only deployment boxes or only “important decisions.”
- Praising patterns without naming the cost of abstraction.

### Likely follow-ups

1. What change pressure would justify upgrading the callable dictionary to a stronger boundary?
2. Can a library also behave like a framework in one execution phase?
3. Which parts of your current system are architectural, and why?
4. How would tests differ at idiom, pattern, framework, and architecture levels?
5. Which design label would you remove from a pattern-heavy code review?

### Senior reasoning checkpoint

A strong answer identifies the kind of claim, its scale, who owns control, the forces and
consequences, a simpler alternative, and the limits of the chosen label.

## 17. Closed-book revision and transfer

1. Reconstruct the five-row notebook visual without looking.
2. Explain the notification feature at all five levels.
3. Take one pattern claim and state its context, forces, collaboration, and cost.
4. Take one Python snippet and explain why syntax alone cannot prove a pattern.
5. Identify a framework callback in a familiar tool and trace who calls whom.
6. Name one fundamental system relationship and defend why it is architectural.
7. Reject a named pattern for a small scenario and propose the simpler design.

Complete the unsolved [classification and refactoring lab](practice/README.md) to produce the `D`
and `T` evidence required by this unit. Generated notes and passing starter checks do not advance the
learning state.

## Sources read

- Python Software Foundation, [Python glossary — “Pythonic”](https://docs.python.org/3/glossary.html#term-Pythonic), accessed 2026-08-29.
- Tim Peters, [PEP 20 — The Zen of Python](https://peps.python.org/pep-0020/), accessed 2026-08-29.
- Martin Fowler, [Writing Software Patterns](https://martinfowler.com/articles/writingPatterns.html), accessed 2026-08-29.
- Martin Fowler, [Inversion of Control](https://martinfowler.com/bliki/InversionOfControl.html), accessed 2026-08-29.
- Carnegie Mellon University Software Engineering Institute,
  [Reflections on 20 Years of Software Architecture](https://www.sei.cmu.edu/blog/reflections-on-20-years-of-software-architecture-a-presentation-by-linda-northrop/), accessed 2026-08-29.
