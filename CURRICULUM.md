# SOLID and Design Pattern Curriculum

[Learning paths](LEARNING_PATHS.md) · [Python Mastery references](PYTHON_REFERENCES.md) · [Progress](PROGRESS.md) · [Projects](PROJECTS.md)

This file is the canonical source for learning-unit IDs, titles, outcomes, prerequisites, classifications, order, and stable anchors. Paths are recommendations; any unit may be initialized earlier with the smallest correct prerequisite bridge.

## Hierarchy

```text
Domain
└── Learning unit
    ├── Subtopic
    └── Evidence artifact
```

Only a learning unit receives one stable ID, one dedicated Codex chat, one progress row, one estimate, and one just-in-time folder. Subtopics stay inside the integrated unit note unless they develop an independent outcome, prerequisite boundary, practice need, or review cycle. Experiments and labs are evidence artifacts, not automatic curriculum units.

## Stable IDs and granularity

- IDs use `SDP-<DOMAIN>-<THREE-DIGIT-SEQUENCE>` with gaps of ten.
- IDs are immutable, never silently reused, and always written in full.
- A unit normally has one observable primary outcome and meaningful independent practice or review.
- Split a unit only when it has independent outcomes, distinct prerequisites, separate evidence, or excessive size.
- Do not create one unit per term, method, variant, or interview fact.

## Classification system

Interview frequency and production frequency are **reasoned professional classifications**, not measured population statistics. A unit may be common in interviews but uncommon in Python production, or common in production without being named explicitly.

| Dimension | Values | Meaning |
|---|---|---|
| Priority | Core / Professional / Advanced / Reference | Learning importance, independent of frequency |
| Interview frequency | High / Medium / Low | Likelihood of direct or indirect interview use |
| Production frequency | High / Medium / Low | How often the idea materially appears in real designs |
| Python/backend relevance | High / Medium / Low | Value for Python and backend engineering |
| Depth | D1 / D2 / D3 / D4 | Practical use / formal mechanics / Python mechanism awareness / unusually deep or source-level work |
| Scope | Design, Python, GoF, Application, Architecture, Refactoring, Interview, Distributed, or related labels | What kind of knowledge the unit owns |
| Evidence | E / I / D / X / (X) / T | Explain / implement and test / debug or refactor / required experiment / recommended experiment / production-design transfer |

Human-friendly labels, when shown in learning material, are derived from these dimensions: **Must Know** means Priority Core; **Most Common** means High interview or production frequency; **Deep** means D3; **Very Deep** means D4. They never replace the canonical fields.

## Size and time estimates

| Size | First understanding | Hands-on practice |
|---|---:|---:|
| S | 1–2 h | 1–3 h |
| M | 2–4 h | 3–6 h |
| L | 4–6 h | 5–9 h |
| XL | 6–9 h | 8–14 h |

First understanding includes active explanation, diagrams, code tracing, and notebook reconstruction. Practice includes labs, tests, debugging, refactoring, and design defence. Spaced reviews and projects are additional.

## Priority layers

1. **Essential foundations:** design foundations, SOLID, and core Pythonic mechanisms.
2. **Interview-core and commonly useful patterns:** Factory Method, Builder, Adapter, Facade, Decorator, Proxy, Strategy, State, Observer, Command, Chain of Responsibility, Template Method, DI, Repository, Unit of Work, Service Layer, Pipeline, and refactoring fundamentals.
3. **Useful but less-common patterns:** Abstract Factory, Composite, Bridge, Mediator, Memento, Specification, Domain Events, MVC/MVT, Hexagonal Architecture, and related application patterns.
4. **Rare but credible production patterns:** Prototype, Flyweight, Visitor, Object Pool, Lazy Initialization, Identity Map, CQRS, Circuit Breaker, and selected specialist designs.
5. **Reference knowledge:** Interpreter, Borg, Blackboard, Active Object, Event Sourcing, Saga, and patterns whose operational depth belongs partly in another repository.

## Domain totals

| Domain | Units | First understanding | Practice |
|---|---:|---:|---:|
| Design foundations | 11 | 33–54 h | 43–81 h |
| SOLID principles | 8 | 36–54 h | 46–82 h |
| Pythonic design mechanisms | 10 | 44–66 h | 56–100 h |
| GoF creational patterns | 5 | 20–30 h | 25–45 h |
| GoF structural patterns | 7 | 26–40 h | 33–60 h |
| GoF behavioral patterns | 11 | 48–72 h | 61–109 h |
| Application patterns | 12 | 44–68 h | 56–102 h |
| Architectural patterns | 8 | 36–54 h | 46–82 h |
| Rare and specialist patterns | 8 | 26–42 h | 34–63 h |
| Refactoring and anti-patterns | 10 | 42–63 h | 53–95 h |
| Interview comparisons and synthesis | 10 | 42–63 h | 53–95 h |
| **Total** | **100** | **397–606 h** | **506–914 h** |

## Canonical learning units

### Design foundations

Core language for change pressure, responsibilities, boundaries, contracts, collaboration, state, testing seams, modules, and simplicity.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-fnd-010"></a> `SDP-FND-010` — **Design vocabulary: principle, pattern, idiom, framework, and architecture** | Distinguish the major levels of software-design knowledge and use pattern names without confusing them with syntax, frameworks, or architecture. | None | Core | High | High | High | D1 | Design | S | 1–2 h | 1–3 h | `E+D+T` |
| <a id="sdp-fnd-020"></a> `SDP-FND-020` — **Change pressure, responsibilities, and boundaries** | Identify the reason a design is changing, assign responsibilities deliberately with GRASP lenses—Information Expert, Creator, Controller, Low Coupling, High Cohesion, Indirection, Polymorphism, Protected Variations, and Pure Fabrication—and draw boundaries around stable decisions. | [SDP-FND-010](#sdp-fnd-010) | Core | High | High | High | D2 | Design | M | 2–4 h | 3–6 h | `E+D+T` |
| <a id="sdp-fnd-030"></a> `SDP-FND-030` — **Cohesion, coupling, and dependency direction** | Evaluate cohesion, coupling, dependency shape, and the cost of changing one part of a Python system. | [SDP-FND-020](#sdp-fnd-020) | Core | High | High | High | D2 | Design | M | 2–4 h | 3–6 h | `E+D+T` |
| <a id="sdp-fnd-040"></a> `SDP-FND-040` — **Abstraction, encapsulation, information hiding, and contracts** | Separate abstraction from encapsulation, hide volatile decisions, and express useful behavioural contracts. | [SDP-FND-020](#sdp-fnd-020) | Core | High | High | High | D2 | Design, Python | M | 2–4 h | 3–6 h | `E+I+D+T` |
| <a id="sdp-fnd-050"></a> `SDP-FND-050` — **Composition, delegation, and inheritance** | Choose among composition, delegation, and inheritance from actual change forces rather than slogans. | [SDP-FND-030](#sdp-fnd-030), [SDP-FND-040](#sdp-fnd-040) | Core | High | High | High | D2 | Design, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-fnd-060"></a> `SDP-FND-060` — **Polymorphism, dynamic dispatch, and subtyping** | Explain behavioural polymorphism and dynamic dispatch, then design substitutions that preserve useful contracts. | [SDP-FND-040](#sdp-fnd-040), [SDP-FND-050](#sdp-fnd-050) | Core | High | High | High | D2 | Design, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-fnd-070"></a> `SDP-FND-070` — **Duck typing, structural typing, nominal typing, Protocols, and ABCs** | Select duck typing, typing.Protocol, an abstract base class, or nominal inheritance for a concrete Python boundary. | [SDP-FND-060](#sdp-fnd-060) | Core | High | High | High | D3 | Python, Typing | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-fnd-080"></a> `SDP-FND-080` — **Dependency management, test seams, and test doubles** | Expose controllable seams, pass dependencies explicitly, and choose fakes, stubs, spies, or mocks without coupling tests to implementation details. | [SDP-FND-030](#sdp-fnd-030), [SDP-FND-070](#sdp-fnd-070) | Core | High | High | High | D2 | Design, Testing | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-fnd-090"></a> `SDP-FND-090` — **Mutability, shared state, ownership, and object lifetime** | Reason about state ownership, aliases, mutation, lifetime, and concurrency risks before choosing an object pattern. | [SDP-FND-020](#sdp-fnd-020), [SDP-FND-040](#sdp-fnd-040) | Core | Medium | High | High | D3 | Python, Runtime | L | 4–6 h | 5–9 h | `E+I+D+(X)+T` |
| <a id="sdp-fnd-100"></a> `SDP-FND-100` — **Modules, package boundaries, and circular dependencies** | Design Python module and package boundaries that keep dependencies visible and prevent circular-import design traps. | [SDP-FND-030](#sdp-fnd-030), [SDP-FND-080](#sdp-fnd-080) | Core | High | High | High | D3 | Python, Modules | L | 4–6 h | 5–9 h | `E+I+D+(X)+T` |
| <a id="sdp-fnd-110"></a> `SDP-FND-110` — **Simplicity heuristics and collaboration laws** | Apply KISS, DRY, YAGNI, separation of concerns, Tell Don’t Ask, Law of Demeter, and favour-composition guidance without turning them into rigid rules. | [SDP-FND-020](#sdp-fnd-020), [SDP-FND-030](#sdp-fnd-030), [SDP-FND-050](#sdp-fnd-050) | Core | High | High | High | D2 | Design | M | 2–4 h | 3–6 h | `E+D+T` |

### SOLID principles

Each SOLID principle independently, then their interactions, Pythonic application, critique, and legacy refactoring.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-sol-010"></a> `SDP-SOL-010` — **Single Responsibility Principle** | Find the actual axis of change behind a class, function, or module and refactor responsibilities without creating meaningless micro-objects. | [SDP-FND-020](#sdp-fnd-020), [SDP-FND-030](#sdp-fnd-030), [SDP-FND-110](#sdp-fnd-110) | Core | High | High | High | D2 | SOLID, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-sol-020"></a> `SDP-SOL-020` — **Open/Closed Principle** | Create stable extension points only where variation is real, and compare polymorphism, callables, registration, and data-driven alternatives. | [SDP-FND-030](#sdp-fnd-030), [SDP-FND-040](#sdp-fnd-040), [SDP-FND-050](#sdp-fnd-050) | Core | High | High | High | D2 | SOLID, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-sol-030"></a> `SDP-SOL-030` — **Liskov Substitution Principle and behavioural subtyping** | Evaluate subtype invariants, preconditions, postconditions, return behaviour, exceptions, mutation, and observable contracts instead of using the simplistic parent-child slogan. | [SDP-FND-040](#sdp-fnd-040), [SDP-FND-060](#sdp-fnd-060), [SDP-FND-070](#sdp-fnd-070), [SDP-FND-090](#sdp-fnd-090) | Core | High | High | High | D3 | SOLID, Contracts | XL | 6–9 h | 8–14 h | `E+I+D+X+T` |
| <a id="sdp-sol-040"></a> `SDP-SOL-040` — **Interface Segregation Principle** | Design small client-shaped capabilities in Python without multiplying nominal interfaces that add no value. | [SDP-FND-030](#sdp-fnd-030), [SDP-FND-070](#sdp-fnd-070) | Core | High | High | High | D2 | SOLID, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-sol-050"></a> `SDP-SOL-050` — **Dependency Inversion Principle** | Reverse source-code dependency direction around policy, and distinguish dependency inversion from injection, inversion of control, service location, and framework-managed dependencies. | [SDP-FND-030](#sdp-fnd-030), [SDP-FND-070](#sdp-fnd-070), [SDP-FND-080](#sdp-fnd-080), [SDP-FND-100](#sdp-fnd-100) | Core | High | High | High | D3 | SOLID, Architecture | XL | 6–9 h | 8–14 h | `E+I+D+T` |
| <a id="sdp-sol-060"></a> `SDP-SOL-060` — **SOLID interactions, tensions, and trade-offs** | Diagnose which principle is truly under pressure, explain tensions among principles, and choose the smallest coherent refactoring. | [SDP-SOL-010](#sdp-sol-010), [SDP-SOL-020](#sdp-sol-020), [SDP-SOL-030](#sdp-sol-030), [SDP-SOL-040](#sdp-sol-040), [SDP-SOL-050](#sdp-sol-050) | Core | High | High | High | D3 | SOLID, Design | L | 4–6 h | 5–9 h | `E+D+T` |
| <a id="sdp-sol-070"></a> `SDP-SOL-070` — **Pythonic SOLID with functions, modules, Protocols, and ABCs** | Apply SOLID to dynamically typed Python using functions, callables, modules, Protocols, ABCs, and explicit data rather than Java-style interface hierarchies. | [SDP-FND-070](#sdp-fnd-070), [SDP-FND-100](#sdp-fnd-100), [SDP-SOL-060](#sdp-sol-060) | Core | High | High | High | D3 | SOLID, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-sol-080"></a> `SDP-SOL-080` — **SOLID critiques, overapplication, and legacy refactoring** | Explain the limits of SOLID, recognize needless abstraction, and refactor legacy Python incrementally while preserving behaviour. | [SDP-SOL-060](#sdp-sol-060), [SDP-SOL-070](#sdp-sol-070), [SDP-FND-110](#sdp-fnd-110) | Professional | High | High | High | D3 | SOLID, Refactoring | L | 4–6 h | 5–9 h | `E+I+D+T` |

### Pythonic design mechanisms

Functions, callables, protocols, decorators, generators, modules, values, dispatch, plugins, and advanced class mechanisms.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-pyt-010"></a> `SDP-PYT-010` — **Functions, closures, and callable objects as design tools** | Use first-class callables to implement Strategy- or Command-like collaboration before introducing class hierarchies. | [SDP-FND-060](#sdp-fnd-060), [SDP-FND-070](#sdp-fnd-070) | Core | High | High | High | D3 | Python, Idiom | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-pyt-020"></a> `SDP-PYT-020` — **Dispatch tables, dictionaries of callables, and registries** | Replace brittle conditional dispatch with explicit callable maps or registries while controlling defaults, ordering, and extension boundaries. | [SDP-FND-030](#sdp-fnd-030), [SDP-PYT-010](#sdp-pyt-010) | Core | High | High | High | D2 | Python, Idiom | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-pyt-030"></a> `SDP-PYT-030` — **Python decorator syntax versus the Decorator pattern** | Distinguish the `@decorator` transformation mechanism from object-wrapping Decorator design, and choose functions, closures, or wrapper objects appropriately. | [SDP-PYT-010](#sdp-pyt-010), [SDP-FND-050](#sdp-fnd-050) | Core | High | High | High | D3 | Python, Idiom | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-pyt-040"></a> `SDP-PYT-040` — **Iterators, generators, and context managers as language-supported patterns** | Recognize where Python’s protocols make explicit Iterator or resource-management pattern classes unnecessary. | [SDP-FND-060](#sdp-fnd-060), [SDP-PYT-010](#sdp-pyt-010) | Core | High | High | High | D3 | Python, Protocols | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-pyt-050"></a> `SDP-PYT-050` — **Modules, import caching, and dependency lifetimes** | Compare module namespaces, import caching, application-scoped objects, and explicit lifetimes with a traditional Singleton. | [SDP-FND-090](#sdp-fnd-090), [SDP-FND-100](#sdp-fnd-100) | Core | High | High | High | D3 | Python, Modules | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-pyt-060"></a> `SDP-PYT-060` — **Dataclasses, immutable value objects, and enums** | Model values and states with dataclasses, frozen data, enums, and explicit invariants instead of unnecessary behavioural objects. | [SDP-FND-040](#sdp-fnd-040), [SDP-FND-090](#sdp-fnd-090) | Core | Medium | High | High | D2 | Python, Data model | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-pyt-070"></a> `SDP-PYT-070` — **Practical interface design with Protocols, ABCs, and duck typing** | Build and test Python-facing interfaces that balance runtime simplicity, static checking, discoverability, and substitutability. | [SDP-FND-070](#sdp-fnd-070), [SDP-SOL-070](#sdp-sol-070) | Core | High | High | High | D3 | Python, Typing | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-pyt-080"></a> `SDP-PYT-080` — **singledispatch and open function extension** | Use `functools.singledispatch` as a controlled extension mechanism and compare it with Visitor, Strategy, and manual dispatch. | [SDP-PYT-010](#sdp-pyt-010), [SDP-PYT-070](#sdp-pyt-070), [SDP-SOL-020](#sdp-sol-020) | Professional | Medium | Medium | Medium | D3 | Python, Standard library | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-pyt-090"></a> `SDP-PYT-090` — **Dynamic registration and plugin discovery mechanics** | Implement registration, entry-point-style discovery, import boundaries, duplicate detection, and safe plugin contracts. | [SDP-FND-100](#sdp-fnd-100), [SDP-PYT-020](#sdp-pyt-020), [SDP-PYT-070](#sdp-pyt-070) | Professional | Medium | High | High | D3 | Python, Plugins | XL | 6–9 h | 8–14 h | `E+I+D+X+T` |
| <a id="sdp-pyt-100"></a> `SDP-PYT-100` — **Descriptors, class hooks, and metaclasses only when justified** | Evaluate descriptors, `__init_subclass__`, class decorators, and metaclasses as advanced pattern mechanisms while preferring simpler Python designs. | [SDP-FND-040](#sdp-fnd-040), [SDP-FND-060](#sdp-fnd-060), [SDP-PYT-070](#sdp-pyt-070) | Advanced | Low | Medium | Medium | D4 | Python, Runtime | XL | 6–9 h | 8–14 h | `E+I+D+X+T` |

### GoF creational patterns

All five Gang of Four creational patterns, re-evaluated for modern Python.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-cre-010"></a> `SDP-CRE-010` — **Factory Method** | Move variable construction behind a stable creation decision, then compare class-based Factory Method with a simple Python factory function. | [SDP-SOL-020](#sdp-sol-020), [SDP-PYT-010](#sdp-pyt-010), [SDP-PYT-070](#sdp-pyt-070) | Core | High | High | High | D2 | GoF, Creational, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-cre-020"></a> `SDP-CRE-020` — **Abstract Factory** | Create coherent families of related objects without binding policy code to concrete implementations, and identify when ordinary dependency injection is simpler. | [SDP-CRE-010](#sdp-cre-010), [SDP-FND-050](#sdp-fnd-050) | Professional | Medium | Medium | Medium | D2 | GoF, Creational | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-cre-030"></a> `SDP-CRE-030` — **Builder** | Separate complex, validated, or staged construction from the final object while comparing fluent builders with keyword arguments, dataclasses, and factory functions. | [SDP-FND-040](#sdp-fnd-040), [SDP-FND-050](#sdp-fnd-050), [SDP-PYT-060](#sdp-pyt-060) | Core | High | Medium | High | D2 | GoF, Creational, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-cre-040"></a> `SDP-CRE-040` — **Prototype** | Create objects through copying when construction state is expensive or externally configured, and reason about shallow copies, deep copies, identity, and shared state. | [SDP-FND-090](#sdp-fnd-090), [SDP-PYT-060](#sdp-pyt-060) | Advanced | Low | Low | Medium | D3 | GoF, Creational, Python | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-cre-050"></a> `SDP-CRE-050` — **Singleton** | Explain controlled single-instance access, lifecycle and testing costs, and why modules, explicit dependency lifetimes, or composition roots are usually better in Python. | [SDP-FND-090](#sdp-fnd-090), [SDP-FND-100](#sdp-fnd-100), [SDP-PYT-050](#sdp-pyt-050) | Core | High | Medium | High | D3 | GoF, Creational, Python | L | 4–6 h | 5–9 h | `E+I+D+X+T` |

### GoF structural patterns

All seven Gang of Four structural patterns, emphasizing object shape and boundary collaboration.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-str-010"></a> `SDP-STR-010` — **Adapter** | Translate one interface or data shape into another at a boundary without contaminating domain code. | [SDP-FND-050](#sdp-fnd-050), [SDP-FND-070](#sdp-fnd-070) | Core | High | High | High | D2 | GoF, Structural, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-str-020"></a> `SDP-STR-020` — **Facade** | Offer a small task-oriented entry point over a complicated subsystem while preserving access to lower-level capabilities when justified. | [SDP-FND-020](#sdp-fnd-020), [SDP-FND-100](#sdp-fnd-100) | Core | High | High | High | D2 | GoF, Structural, Backend | M | 2–4 h | 3–6 h | `E+I+D+T` |
| <a id="sdp-str-030"></a> `SDP-STR-030` — **Decorator** | Add behaviour by wrapping compatible objects, preserve the wrapped contract, and compare object decorators with Python function decorators. | [SDP-FND-050](#sdp-fnd-050), [SDP-PYT-030](#sdp-pyt-030) | Core | High | High | High | D2 | GoF, Structural, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-str-040"></a> `SDP-STR-040` — **Proxy** | Control access to another object for laziness, authorization, caching, remoting, or observation while keeping semantic differences visible. | [SDP-FND-050](#sdp-fnd-050), [SDP-FND-070](#sdp-fnd-070) | Core | High | High | High | D2 | GoF, Structural, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-str-050"></a> `SDP-STR-050` — **Composite** | Treat individual objects and recursive groups through a common operation while controlling ownership, traversal, and invalid combinations. | [SDP-FND-050](#sdp-fnd-050), [SDP-FND-060](#sdp-fnd-060) | Professional | Medium | Medium | Medium | D2 | GoF, Structural | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-str-060"></a> `SDP-STR-060` — **Bridge** | Separate two independently varying dimensions before inheritance creates a Cartesian product of subclasses. | [SDP-FND-050](#sdp-fnd-050), [SDP-SOL-020](#sdp-sol-020) | Professional | Medium | Medium | Medium | D2 | GoF, Structural | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-str-070"></a> `SDP-STR-070` — **Flyweight** | Share stable intrinsic state across many logical objects while making identity, mutability, caching, and memory trade-offs explicit. | [SDP-FND-090](#sdp-fnd-090), [SDP-PYT-060](#sdp-pyt-060) | Advanced | Low | Low | Low | D3 | GoF, Structural, Runtime | L | 4–6 h | 5–9 h | `E+I+D+X+T` |

### GoF behavioral patterns

All eleven Gang of Four behavioral patterns, emphasizing control flow, state, events, and collaboration.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-beh-010"></a> `SDP-BEH-010` — **Strategy** | Make an algorithm or policy replaceable through a callable or object contract and compare the simplest Python forms with class-based implementations. | [SDP-PYT-010](#sdp-pyt-010), [SDP-SOL-020](#sdp-sol-020) | Core | High | High | High | D2 | GoF, Behavioral, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-beh-020"></a> `SDP-BEH-020` — **State** | Move state-dependent behaviour behind explicit state transitions, preserving invariants and avoiding giant conditional dispatch. | [SDP-FND-090](#sdp-fnd-090), [SDP-PYT-060](#sdp-pyt-060), [SDP-BEH-010](#sdp-beh-010) | Core | High | High | High | D3 | GoF, Behavioral, Python | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-beh-030"></a> `SDP-BEH-030` — **Observer** | Notify interested objects about changes while managing subscription lifecycle, failure isolation, ordering, reentrancy, and weak references. | [SDP-FND-090](#sdp-fnd-090), [SDP-PYT-010](#sdp-pyt-010) | Core | High | High | High | D3 | GoF, Behavioral, Python | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-beh-040"></a> `SDP-BEH-040` — **Command** | Represent an action and its data as a callable or object to support queues, retries, audit, undo, or deferred execution. | [SDP-PYT-010](#sdp-pyt-010), [SDP-FND-090](#sdp-fnd-090) | Core | High | High | High | D2 | GoF, Behavioral, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-beh-050"></a> `SDP-BEH-050` — **Chain of Responsibility** | Pass a request through ordered handlers while making continuation, stopping, error handling, and observability explicit. | [SDP-PYT-010](#sdp-pyt-010), [SDP-FND-050](#sdp-fnd-050) | Core | High | High | High | D2 | GoF, Behavioral, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-beh-060"></a> `SDP-BEH-060` — **Template Method** | Keep an invariant algorithm skeleton while allowing selected steps to vary, and compare inheritance with composition and callable injection. | [SDP-FND-050](#sdp-fnd-050), [SDP-FND-060](#sdp-fnd-060) | Professional | High | Medium | Medium | D2 | GoF, Behavioral | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-beh-070"></a> `SDP-BEH-070` — **Iterator** | Separate traversal state from a collection and connect the original pattern to Python’s iterable, iterator, and generator protocols. | [SDP-PYT-040](#sdp-pyt-040) | Core | High | High | High | D3 | GoF, Behavioral, Python | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-beh-080"></a> `SDP-BEH-080` — **Mediator** | Centralize complex peer-to-peer coordination without turning the mediator into a new God Object. | [SDP-FND-030](#sdp-fnd-030), [SDP-FND-050](#sdp-fnd-050) | Professional | Medium | Medium | Medium | D2 | GoF, Behavioral | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-beh-090"></a> `SDP-BEH-090` — **Memento** | Capture and restore state without exposing internals, while controlling copying, storage cost, versioning, and privacy. | [SDP-FND-090](#sdp-fnd-090), [SDP-PYT-060](#sdp-pyt-060) | Advanced | Medium | Low | Medium | D3 | GoF, Behavioral | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-beh-100"></a> `SDP-BEH-100` — **Visitor** | Add operations across a stable object structure, understand double dispatch, and compare Visitor with singledispatch, pattern matching, and methods. | [SDP-FND-060](#sdp-fnd-060), [SDP-PYT-070](#sdp-pyt-070) | Advanced | Medium | Low | Low | D3 | GoF, Behavioral, Python | XL | 6–9 h | 8–14 h | `E+I+D+X+T` |
| <a id="sdp-beh-110"></a> `SDP-BEH-110` — **Interpreter** | Represent and evaluate a small language or rule grammar while recognizing when parsing libraries, functions, or data-driven rules are simpler. | [SDP-FND-040](#sdp-fnd-040), [SDP-STR-050](#sdp-str-050) | Reference | Low | Low | Low | D3 | GoF, Behavioral | XL | 6–9 h | 8–14 h | `E+I+D+T` |

### Application patterns

Dependency management, persistence boundaries, use cases, domain events, pipelines, and presentation organization.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-app-010"></a> `SDP-APP-010` — **Dependency Injection and the composition root** | Construct object graphs at an explicit boundary, choose constructor/function injection, and manage lifetimes without requiring a framework. | [SDP-SOL-050](#sdp-sol-050), [SDP-PYT-070](#sdp-pyt-070) | Core | High | High | High | D2 | Application, Python, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-app-020"></a> `SDP-APP-020` — **Null Object and sentinel alternatives** | Represent absence with a behaviourally safe object or sentinel only when it removes branching without hiding errors. | [SDP-FND-070](#sdp-fnd-070), [SDP-PYT-060](#sdp-pyt-060) | Professional | Medium | Medium | Medium | D2 | Application, Python | M | 2–4 h | 3–6 h | `E+I+D+T` |
| <a id="sdp-app-030"></a> `SDP-APP-030` — **Specification** | Compose business rules as testable predicates or objects, and compare specifications with plain functions, query objects, and validation schemas. | [SDP-SOL-020](#sdp-sol-020), [SDP-PYT-010](#sdp-pyt-010), [SDP-PYT-060](#sdp-pyt-060) | Professional | Medium | High | High | D2 | Application, Domain | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-app-040"></a> `SDP-APP-040` — **Repository** | Provide a collection-like domain boundary over persistence while avoiding leaky query APIs and needless abstraction. | [SDP-FND-100](#sdp-fnd-100), [SDP-PYT-070](#sdp-pyt-070) | Core | High | High | High | D2 | Application, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-app-050"></a> `SDP-APP-050` — **Unit of Work** | Coordinate a consistency boundary and commit or rollback multiple changes while making transaction ownership explicit. | [SDP-APP-040](#sdp-app-040), [SDP-FND-090](#sdp-fnd-090) | Core | High | High | High | D3 | Application, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-app-060"></a> `SDP-APP-060` — **Service Layer** | Expose application use cases as stable operations that coordinate domain behaviour, repositories, transactions, and external ports. | [SDP-APP-010](#sdp-app-010), [SDP-APP-040](#sdp-app-040) | Core | High | High | High | D2 | Application, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-app-070"></a> `SDP-APP-070` — **Domain Events** | Record meaningful domain facts and handle consequences without coupling the domain model to infrastructure delivery. | [SDP-APP-060](#sdp-app-060), [SDP-BEH-030](#sdp-beh-030) | Professional | High | High | High | D3 | Application, Domain, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-app-080"></a> `SDP-APP-080` — **Pipeline** | Compose ordered transformations or handlers with explicit data shape, failure policy, short-circuiting, and observability. | [SDP-PYT-040](#sdp-pyt-040), [SDP-BEH-050](#sdp-beh-050) | Core | High | High | High | D2 | Application, Python, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-app-090"></a> `SDP-APP-090` — **Transaction Script** | Organize simple business use cases procedurally and recognize when growing complexity justifies richer domain or service patterns. | [SDP-FND-100](#sdp-fnd-100), [SDP-SOL-010](#sdp-sol-010) | Professional | Medium | High | High | D2 | Application, Backend | M | 2–4 h | 3–6 h | `E+I+D+T` |
| <a id="sdp-app-100"></a> `SDP-APP-100` — **Active Record versus Data Mapper** | Compare persistence-coupled entities with separate mapping, including testability, domain complexity, and framework trade-offs. | [SDP-APP-040](#sdp-app-040), [SDP-FND-100](#sdp-fnd-100) | Professional | Medium | High | High | D3 | Application, Persistence | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-app-110"></a> `SDP-APP-110` — **Identity Map and object identity** | Keep one in-memory representation per persistence identity within a scope and understand caching, stale state, and unit-of-work interaction. | [SDP-APP-100](#sdp-app-100), [SDP-FND-090](#sdp-fnd-090) | Advanced | Low | Medium | Medium | D3 | Application, Persistence | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-app-120"></a> `SDP-APP-120` — **MVC, MVT, and presentation boundaries** | Separate presentation input, rendering, application coordination, and domain decisions while mapping textbook MVC to Python framework variants. | [SDP-FND-020](#sdp-fnd-020), [SDP-FND-100](#sdp-fnd-100) | Professional | High | High | High | D2 | Application, Architecture, Backend | L | 4–6 h | 5–9 h | `E+D+T` |

### Architectural patterns

Application-scale dependency rules and boundaries without becoming a distributed-systems curriculum.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-arc-010"></a> `SDP-ARC-010` — **Layered Architecture** | Separate presentation, application, domain, and infrastructure responsibilities while controlling dependency direction and layer leakage. | [SDP-APP-060](#sdp-app-060), [SDP-FND-100](#sdp-fnd-100) | Core | High | High | High | D2 | Architecture, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-arc-020"></a> `SDP-ARC-020` — **Ports and Adapters / Hexagonal Architecture** | Protect application policy behind inward-facing ports and outward adapters, with explicit composition at the edge. | [SDP-SOL-050](#sdp-sol-050), [SDP-APP-010](#sdp-app-010), [SDP-APP-060](#sdp-app-060) | Core | High | High | High | D3 | Architecture, Backend | XL | 6–9 h | 8–14 h | `E+I+D+T` |
| <a id="sdp-arc-030"></a> `SDP-ARC-030` — **Clean Architecture** | Apply concentric dependency rules while critically comparing Clean Architecture with simpler layering and hexagonal structure. | [SDP-ARC-020](#sdp-arc-020), [SDP-SOL-060](#sdp-sol-060) | Professional | High | Medium | High | D3 | Architecture, Backend | L | 4–6 h | 5–9 h | `E+D+T` |
| <a id="sdp-arc-040"></a> `SDP-ARC-040` — **Functional Core, Imperative Shell** | Keep decisions in pure functions and side effects at explicit boundaries to simplify tests and reduce stateful pattern machinery. | [SDP-PYT-010](#sdp-pyt-010), [SDP-FND-090](#sdp-fnd-090) | Core | Medium | High | High | D2 | Architecture, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-arc-050"></a> `SDP-ARC-050` — **Event-driven application boundaries** | Use events at application boundaries while distinguishing in-process observers, domain events, publish/subscribe, and external messaging. | [SDP-APP-070](#sdp-app-070), [SDP-BEH-030](#sdp-beh-030) | Professional | High | High | High | D3 | Architecture, Events, Backend | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-arc-060"></a> `SDP-ARC-060` — **CQRS at application scale** | Separate command and query models only when read/write forces differ enough to justify duplicated models and consistency cost. | [SDP-ARC-050](#sdp-arc-050), [SDP-APP-060](#sdp-app-060) | Advanced | Medium | Medium | Medium | D3 | Architecture, Backend | L | 4–6 h | 5–9 h | `E+D+T` |
| <a id="sdp-arc-070"></a> `SDP-ARC-070` — **Event Sourcing** | Persist state changes as an event history, reconstruct state, and explain versioning, replay, consistency, and operational cost. | [SDP-ARC-050](#sdp-arc-050), [SDP-APP-070](#sdp-app-070) | Advanced | Medium | Low | Medium | D3 | Architecture, Events, Reference | XL | 6–9 h | 8–14 h | `E+I+D+X+T` |
| <a id="sdp-arc-080"></a> `SDP-ARC-080` — **Architectural boundaries and evolutionary design** | Separate object collaboration from application architecture, enforce dependency rules, and evolve boundaries without pattern-driven overengineering. | [SDP-FND-020](#sdp-fnd-020), [SDP-FND-030](#sdp-fnd-030), [SDP-ARC-010](#sdp-arc-010), [SDP-ARC-020](#sdp-arc-020) | Professional | High | High | High | D3 | Architecture, Refactoring | L | 4–6 h | 5–9 h | `E+D+T` |

### Rare and specialist patterns

Credible but less-common techniques, with explicit limits and reference labels.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-rar-010"></a> `SDP-RAR-010` — **Object Pool** | Reuse scarce or expensive objects only when measurement and resource semantics justify pooling over ordinary allocation. | [SDP-FND-090](#sdp-fnd-090), [SDP-CRE-010](#sdp-cre-010) | Reference | Low | Low | Low | D3 | Creational, Reference | M | 2–4 h | 3–6 h | `E+I+D+(X)+T` |
| <a id="sdp-rar-020"></a> `SDP-RAR-020` — **Monostate / Borg** | Share instance state through class-level machinery, compare it with Singleton and module state, and understand why it is rarely appropriate. | [SDP-FND-090](#sdp-fnd-090), [SDP-CRE-050](#sdp-cre-050) | Reference | Low | Low | Low | D3 | Python, Reference | M | 2–4 h | 3–6 h | `E+I+D+X+T` |
| <a id="sdp-rar-030"></a> `SDP-RAR-030` — **Lazy Initialization** | Defer construction until first use while controlling failure timing, concurrency, caching, and observability. | [SDP-FND-090](#sdp-fnd-090), [SDP-PYT-050](#sdp-pyt-050) | Professional | Medium | Medium | High | D3 | Creational, Python | M | 2–4 h | 3–6 h | `E+I+D+X+T` |
| <a id="sdp-rar-040"></a> `SDP-RAR-040` — **Blackboard** | Coordinate independent knowledge sources through shared evolving state for specialist problem-solving systems. | [SDP-BEH-030](#sdp-beh-030), [SDP-BEH-080](#sdp-beh-080) | Reference | Low | Low | Low | D3 | Behavioral, Reference | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-rar-050"></a> `SDP-RAR-050` — **Service Locator** | Understand lookup-based dependency access, limited legacy uses, hidden-dependency costs, and why explicit injection is usually preferable. | [SDP-SOL-050](#sdp-sol-050), [SDP-APP-010](#sdp-app-010) | Professional | High | Medium | High | D2 | Application, Anti-pattern risk | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-rar-060"></a> `SDP-RAR-060` — **Active Object** | Decouple method invocation from execution using queued commands and a scheduler, while separating this object pattern from architecture-level boundaries. | [SDP-BEH-040](#sdp-beh-040), [SDP-BEH-030](#sdp-beh-030), [SDP-FND-090](#sdp-fnd-090) | Reference | Low | Low | Medium | D3 | Concurrency, Reference | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-rar-070"></a> `SDP-RAR-070` — **Saga as a distributed workflow pattern** | Coordinate multi-step distributed work through compensating actions while keeping the repository at conceptual and local-simulation scope. | [SDP-ARC-050](#sdp-arc-050), [SDP-APP-070](#sdp-app-070) | Advanced | Medium | Medium | Medium | D3 | Distributed, Reference | L | 4–6 h | 5–9 h | `E+D+T` |
| <a id="sdp-rar-080"></a> `SDP-RAR-080` — **Circuit Breaker as a resilience pattern** | Stop repeated calls to an unhealthy dependency, model state transitions, and explain why resilience belongs at a boundary rather than throughout business code. | [SDP-STR-040](#sdp-str-040), [SDP-BEH-020](#sdp-beh-020) | Professional | Medium | High | High | D3 | Distributed, Backend | L | 4–6 h | 5–9 h | `E+I+D+X+T` |

### Refactoring and anti-patterns

Smell diagnosis, safe refactoring, simplification, testing seams, and removal of pattern overengineering.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-ref-010"></a> `SDP-REF-010` — **Design smells and change-force diagnosis** | Observe symptoms, identify the underlying change force, and choose whether to simplify, refactor, or introduce a pattern. | [SDP-FND-020](#sdp-fnd-020), [SDP-FND-030](#sdp-fnd-030), [SDP-FND-110](#sdp-fnd-110) | Core | High | High | High | D2 | Refactoring | L | 4–6 h | 5–9 h | `E+D+T` |
| <a id="sdp-ref-020"></a> `SDP-REF-020` — **God Object, Spaghetti Code, and Shotgun Surgery** | Diagnose oversized responsibility clusters, tangled control flow, and changes scattered across many files, then create safe boundaries incrementally. | [SDP-REF-010](#sdp-ref-010), [SDP-SOL-010](#sdp-sol-010) | Core | High | High | High | D2 | Refactoring, Anti-patterns | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-ref-030"></a> `SDP-REF-030` — **Feature Envy, Primitive Obsession, and weak domain models** | Move behaviour toward the information it uses, introduce value concepts when justified, and avoid both anemic and overengineered domain models. | [SDP-REF-010](#sdp-ref-010), [SDP-SOL-010](#sdp-sol-010), [SDP-FND-040](#sdp-fnd-040) | Professional | High | High | High | D2 | Refactoring, Domain | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-ref-040"></a> `SDP-REF-040` — **Excessive inheritance and fragile hierarchies** | Recognize inheritance used for reuse rather than substitutability and refactor toward composition, delegation, or explicit capabilities. | [SDP-REF-010](#sdp-ref-010), [SDP-FND-050](#sdp-fnd-050), [SDP-SOL-030](#sdp-sol-030) | Core | High | High | High | D2 | Refactoring, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-ref-050"></a> `SDP-REF-050` — **Boolean flags, giant conditional dispatch, and hidden state** | Refactor APIs whose flags or conditionals encode multiple behaviours, while avoiding unnecessary Strategy or State objects for simple cases. | [SDP-REF-010](#sdp-ref-010), [SDP-BEH-010](#sdp-beh-010), [SDP-BEH-020](#sdp-beh-020) | Core | High | High | High | D2 | Refactoring, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-ref-060"></a> `SDP-REF-060` — **Singleton and Service Locator misuse** | Remove hidden global dependencies, make lifetimes explicit, and restore test isolation without blindly replacing one container with another. | [SDP-REF-010](#sdp-ref-010), [SDP-CRE-050](#sdp-cre-050), [SDP-RAR-050](#sdp-rar-050) | Core | High | High | High | D2 | Refactoring, Anti-patterns | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-ref-070"></a> `SDP-REF-070` — **Circular dependencies and temporal coupling** | Break cycles and order-dependent protocols through boundary changes, state modelling, callbacks, or orchestration. | [SDP-REF-010](#sdp-ref-010), [SDP-FND-100](#sdp-fnd-100) | Core | High | High | High | D3 | Refactoring, Modules | L | 4–6 h | 5–9 h | `E+I+D+X+T` |
| <a id="sdp-ref-080"></a> `SDP-REF-080` — **Mock-heavy tests and meaningless interfaces** | Repair fragile tests, overspecified interactions, and one-implementation abstractions by improving seams and testing observable behaviour. | [SDP-REF-010](#sdp-ref-010), [SDP-FND-080](#sdp-fnd-080) | Core | High | High | High | D2 | Refactoring, Testing | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-ref-090"></a> `SDP-REF-090` — **Unnecessary factories, abstraction layers, and pattern soup** | Remove speculative indirection and choose the simplest design that handles current forces while preserving an honest extension path. | [SDP-REF-010](#sdp-ref-010), [SDP-SOL-080](#sdp-sol-080) | Core | High | High | High | D2 | Refactoring, Anti-patterns | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-ref-100"></a> `SDP-REF-100` — **Safe incremental refactoring with characterization tests** | Preserve existing behaviour, introduce seams, make one reversible change at a time, and verify design improvement through tests and new requirements. | [SDP-REF-010](#sdp-ref-010), [SDP-FND-080](#sdp-fnd-080) | Core | High | High | High | D2 | Refactoring, Testing | XL | 6–9 h | 8–14 h | `E+I+D+T` |

### Interview comparisons and synthesis

Scenario recognition, exact pattern comparisons, senior code review, combinations, and mock-interview transfer.

| ID | Learning outcome and included scope | Prerequisite IDs | Priority | Interview | Production | Python/backend | Depth | Scope | Size | First understanding | Hands-on practice | Evidence |
|---|---|---|---|---|---|---|---|---|:---:|---:|---:|---|
| <a id="sdp-int-010"></a> `SDP-INT-010` — **Scenario recognition and choosing the simplest design** | Translate an interview scenario into change forces, reject irrelevant patterns, and choose the smallest design that can evolve. | [SDP-FND-020](#sdp-fnd-020), [SDP-FND-030](#sdp-fnd-030), [SDP-FND-110](#sdp-fnd-110), [SDP-SOL-060](#sdp-sol-060) | Core | High | High | High | D2 | Interview, Design | L | 4–6 h | 5–9 h | `E+D+T` |
| <a id="sdp-int-020"></a> `SDP-INT-020` — **Strategy versus State versus Template Method versus Command** | Choose among four commonly confused behavioural designs from ownership, trigger, lifecycle, and change-pressure clues. | [SDP-BEH-010](#sdp-beh-010), [SDP-BEH-020](#sdp-beh-020), [SDP-BEH-040](#sdp-beh-040), [SDP-BEH-060](#sdp-beh-060) | Core | High | High | High | D3 | Interview, Comparison | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-int-030"></a> `SDP-INT-030` — **Adapter versus Facade versus Proxy versus Decorator** | Distinguish interface translation, subsystem simplification, access control, and behaviour wrapping from a scenario and object-flow diagram. | [SDP-STR-010](#sdp-str-010), [SDP-STR-020](#sdp-str-020), [SDP-STR-030](#sdp-str-030), [SDP-STR-040](#sdp-str-040) | Core | High | High | High | D3 | Interview, Comparison | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-int-040"></a> `SDP-INT-040` — **Bridge versus Adapter; Composite versus Decorator** | Separate planned independent variation from after-the-fact compatibility, and recursive part-whole structure from wrapper composition. | [SDP-STR-010](#sdp-str-010), [SDP-STR-030](#sdp-str-030), [SDP-STR-050](#sdp-str-050), [SDP-STR-060](#sdp-str-060) | Professional | Medium | Medium | Medium | D3 | Interview, Comparison | L | 4–6 h | 5–9 h | `E+D+T` |
| <a id="sdp-int-050"></a> `SDP-INT-050` — **Factory Method versus Abstract Factory versus Builder versus Prototype** | Select the right creation approach from product families, construction stages, copying, and Python simplification opportunities. | [SDP-CRE-010](#sdp-cre-010), [SDP-CRE-020](#sdp-cre-020), [SDP-CRE-030](#sdp-cre-030), [SDP-CRE-040](#sdp-cre-040) | Core | High | Medium | High | D3 | Interview, Comparison | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-int-060"></a> `SDP-INT-060` — **Observer versus publish/subscribe versus Mediator versus Domain Events** | Compare coupling, addressing, delivery boundary, ownership, failure handling, and consistency across event-related designs. | [SDP-BEH-030](#sdp-beh-030), [SDP-BEH-080](#sdp-beh-080), [SDP-APP-070](#sdp-app-070), [SDP-ARC-050](#sdp-arc-050) | Core | High | High | High | D3 | Interview, Comparison | L | 4–6 h | 5–9 h | `E+D+T` |
| <a id="sdp-int-070"></a> `SDP-INT-070` — **Dependency Inversion versus Injection versus IoC versus Service Locator** | Explain source dependency direction, object construction, control flow ownership, lookup, and framework management without conflating the terms. | [SDP-SOL-050](#sdp-sol-050), [SDP-APP-010](#sdp-app-010), [SDP-RAR-050](#sdp-rar-050) | Core | High | High | High | D3 | Interview, Comparison | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-int-080"></a> `SDP-INT-080` — **Protocol versus ABC versus duck typing; inheritance versus composition versus delegation** | Choose Python collaboration mechanisms from runtime, typing, substitution, reuse, discoverability, and ownership requirements. | [SDP-FND-050](#sdp-fnd-050), [SDP-FND-070](#sdp-fnd-070), [SDP-PYT-070](#sdp-pyt-070) | Core | High | High | High | D3 | Interview, Comparison, Python | L | 4–6 h | 5–9 h | `E+I+D+T` |
| <a id="sdp-int-090"></a> `SDP-INT-090` — **Repository versus DAO and Unit of Work; object versus architectural boundaries** | Distinguish collection-like domain repositories, data-access objects, transaction coordination, Singleton lifetimes, and object patterns from architecture-level boundaries. | [SDP-CRE-050](#sdp-cre-050), [SDP-APP-040](#sdp-app-040), [SDP-APP-050](#sdp-app-050), [SDP-APP-100](#sdp-app-100), [SDP-ARC-080](#sdp-arc-080) | Core | High | High | High | D3 | Interview, Comparison, Backend | L | 4–6 h | 5–9 h | `E+D+T` |
| <a id="sdp-int-100"></a> `SDP-INT-100` — **Senior pattern combinations, code review, and mock interview synthesis** | Defend a small pattern combination, review overengineered code, handle changing requirements, and complete one-question-at-a-time senior interview rounds. | [SDP-INT-010](#sdp-int-010), [SDP-INT-020](#sdp-int-020), [SDP-INT-030](#sdp-int-030), [SDP-INT-040](#sdp-int-040), [SDP-INT-050](#sdp-int-050), [SDP-INT-060](#sdp-int-060), [SDP-INT-070](#sdp-int-070), [SDP-INT-080](#sdp-int-080), [SDP-INT-090](#sdp-int-090), [SDP-REF-100](#sdp-ref-100) | Core | High | High | High | D3 | Interview, Synthesis | XL | 6–9 h | 8–14 h | `E+I+D+T` |

## Gang of Four coverage audit

All 23 Gang of Four patterns have their own canonical unit because each has a distinct collaboration model and useful independent comparison or implementation evidence.

| Category | Patterns |
|---|---|
| Creational | [Factory Method](#sdp-cre-010), [Abstract Factory](#sdp-cre-020), [Builder](#sdp-cre-030), [Prototype](#sdp-cre-040), [Singleton](#sdp-cre-050) |
| Structural | [Adapter](#sdp-str-010), [Facade](#sdp-str-020), [Decorator](#sdp-str-030), [Proxy](#sdp-str-040), [Composite](#sdp-str-050), [Bridge](#sdp-str-060), [Flyweight](#sdp-str-070) |
| Behavioral | [Strategy](#sdp-beh-010), [State](#sdp-beh-020), [Observer](#sdp-beh-030), [Command](#sdp-beh-040), [Chain of Responsibility](#sdp-beh-050), [Template Method](#sdp-beh-060), [Iterator](#sdp-beh-070), [Mediator](#sdp-beh-080), [Memento](#sdp-beh-090), [Visitor](#sdp-beh-100), [Interpreter](#sdp-beh-110) |

## Non-GoF classification audit

These classifications describe why an addition belongs. They are professional judgments, not usage statistics.

| Area | Representative units | Why it belongs | Classification |
|---|---|---|---|
| Pythonic mechanisms | `SDP-PYT-010` through `SDP-PYT-100` | Python often supplies a simpler language or library mechanism than the textbook object structure. | Commonly useful to advanced Python-specific |
| Application patterns | `SDP-APP-010` through `SDP-APP-120` | These organize use cases, persistence, rules, events, and presentation boundaries in backend applications. | Commonly used or occasionally useful |
| Architectural patterns | `SDP-ARC-010` through `SDP-ARC-080` | These define application-scale dependency rules rather than object collaborations. | Common backend to advanced architectural |
| Rare/reference patterns | `SDP-RAR-010` through `SDP-RAR-080` | Each is credible, but context-sensitive, framework-managed, distributed, or specialist. | Occasional, rare, or reference |
| Refactoring and anti-patterns | `SDP-REF-010` through `SDP-REF-100` | Pattern knowledge is incomplete without recognizing when to simplify, remove indirection, or preserve behaviour first. | Common production and interview value |

## Mandatory comparison audit

| Comparison | Canonical owner |
|---|---|
| Strategy vs State vs Template Method; Command vs Strategy | [`SDP-INT-020`](#sdp-int-020) |
| Adapter vs Facade vs Proxy vs Decorator | [`SDP-INT-030`](#sdp-int-030) |
| Bridge vs Adapter; Composite vs Decorator | [`SDP-INT-040`](#sdp-int-040) |
| Factory Method vs Abstract Factory vs Builder vs Prototype | [`SDP-INT-050`](#sdp-int-050) |
| Observer vs publish/subscribe; Observer vs Domain Events; Mediator | [`SDP-INT-060`](#sdp-int-060) |
| Dependency Inversion vs Dependency Injection vs IoC vs Service Locator | [`SDP-INT-070`](#sdp-int-070) |
| Protocol vs ABC vs duck typing; inheritance vs composition vs delegation | [`SDP-INT-080`](#sdp-int-080) |
| Repository vs DAO; Repository plus Unit of Work; Singleton vs module state and dependency lifetime; object vs architectural boundaries | [`SDP-INT-090`](#sdp-int-090) |

## Curriculum maintenance rules

- Keep canonical order stable unless an explicitly approved curriculum migration changes it.
- Never infer mastery from generated files.
- Add a subtopic before adding a new unit.
- Add a new unit only when the independent-outcome and evidence rules are satisfied.
- Application and distributed-system patterns stay bounded to Python application design; deeper distributed systems belong in a separate repository.
- See [LEARNING_PATHS.md](LEARNING_PATHS.md) for recommended sequences and [PYTHON_REFERENCES.md](PYTHON_REFERENCES.md) for exact cross-repository Python prerequisites.
