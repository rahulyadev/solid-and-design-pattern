# Progress and Evidence

[Curriculum](CURRICULUM.md) · [Learning paths](LEARNING_PATHS.md) · [Projects](PROJECTS.md)

Artifact state and learning state are separate. Generated files never prove learning.

## Artifact states

| State | Meaning |
|---|---|
| Absent | No unit folder exists. |
| Draft | Material exists but is incomplete, unapproved, or still being learned. |
| Approved | Canonical material is coherent, source-checked, and runnable where applicable. |

## Learning states

```text
⬜ Not started
→ 🟠 Learning
→ 🟡 Practiced
→ 🔵 Recalled
→ 🟣 Demonstrated
→ 🟢 Retained
```

`★ Mastery` remains a separate exceptional badge.

## Evidence transitions

### Not started → Learning

- Rahul engaged with the mental model or change pressure.
- At least one prediction, question, reconstruction, or misconception was recorded.
- Initialization alone is insufficient.

### Learning → Practiced

- Required labs or exercises were attempted before solutions.
- Relevant tests pass when deterministic verification applies.
- Rahul explains the observed collaboration, trade-off, and important edge cases.
- The original attempt is preserved and linked.

### Practiced → Recalled

- A closed-book review occurs after at least one day.
- Rahul reconstructs the problem, essential visual, participants, and governing rules.
- Approximately 80% of core retrieval checks are correct and no critical misconception remains.

### Recalled → Demonstrated

- Rahul selects or rejects the design for a new scenario.
- He explains at least one rejected alternative.
- Required implementation, debugging, refactoring, comparison, or production-transfer evidence is complete without a direct solution.

### Demonstrated → Retained

- Successful retrieval normally occurs at least seven days later.
- A second successful retrieval normally occurs at least twenty-one days after that.
- Equivalent documented project or production transfer may contribute, but the unit is still evaluated independently.

### ★ Mastery

- Retained state.
- Transfer across at least two contexts.
- Successful teach-back.
- Diagnosis of a subtle misuse or failure.
- Accurate explanation of when not to use the principle or pattern.

Failed review may lower a state. This is evidence correction, not punishment.

## Unit tracker

| Unit ID | Title | Priority | Artifact state | Learning state | Last evidence | Next review | Weakest point | Evidence link |
|---|---|---|---|---|---|---|---|---|
| `SDP-FND-010` | [Design vocabulary: principle, pattern, idiom, framework, and architecture](CURRICULUM.md#sdp-fnd-010) | Core | Approved | Not started | — | — | — | — |
| `SDP-FND-020` | [Change pressure, responsibilities, and boundaries](CURRICULUM.md#sdp-fnd-020) | Core | Approved | Not started | — | — | — | — |
| `SDP-FND-030` | [Cohesion, coupling, and dependency direction](CURRICULUM.md#sdp-fnd-030) | Core | Approved | Not started | — | — | — | — |
| `SDP-FND-040` | [Abstraction, encapsulation, information hiding, and contracts](CURRICULUM.md#sdp-fnd-040) | Core | Approved | Not started | — | — | — | — |
| `SDP-FND-050` | [Composition, delegation, and inheritance](CURRICULUM.md#sdp-fnd-050) | Core | Approved | Not started | — | — | — | — |
| `SDP-FND-060` | [Polymorphism, dynamic dispatch, and subtyping](CURRICULUM.md#sdp-fnd-060) | Core | Approved | Not started | — | — | — | — |
| `SDP-FND-070` | [Duck typing, structural typing, nominal typing, Protocols, and ABCs](CURRICULUM.md#sdp-fnd-070) | Core | Approved | Not started | — | — | — | — |
| `SDP-FND-080` | [Dependency management, test seams, and test doubles](CURRICULUM.md#sdp-fnd-080) | Core | Approved | Not started | — | — | — | — |
| `SDP-FND-090` | [Mutability, shared state, ownership, and object lifetime](CURRICULUM.md#sdp-fnd-090) | Core | Approved | Not started | — | — | — | — |
| `SDP-FND-100` | [Modules, package boundaries, and circular dependencies](CURRICULUM.md#sdp-fnd-100) | Core | Approved | Not started | — | — | — | — |
| `SDP-FND-110` | [Simplicity heuristics and collaboration laws](CURRICULUM.md#sdp-fnd-110) | Core | Approved | Not started | — | — | — | — |
| `SDP-SOL-010` | [Single Responsibility Principle](CURRICULUM.md#sdp-sol-010) | Core | Approved | Not started | — | — | — | — |
| `SDP-SOL-020` | [Open/Closed Principle](CURRICULUM.md#sdp-sol-020) | Core | Approved | Not started | — | — | — | — |
| `SDP-SOL-030` | [Liskov Substitution Principle and behavioural subtyping](CURRICULUM.md#sdp-sol-030) | Core | Approved | Not started | — | — | — | — |
| `SDP-SOL-040` | [Interface Segregation Principle](CURRICULUM.md#sdp-sol-040) | Core | Approved | Not started | — | — | — | — |
| `SDP-SOL-050` | [Dependency Inversion Principle](CURRICULUM.md#sdp-sol-050) | Core | Approved | Not started | — | — | — | — |
| `SDP-SOL-060` | [SOLID interactions, tensions, and trade-offs](CURRICULUM.md#sdp-sol-060) | Core | Approved | Not started | — | — | — | — |
| `SDP-SOL-070` | [Pythonic SOLID with functions, modules, Protocols, and ABCs](CURRICULUM.md#sdp-sol-070) | Core | Approved | Not started | — | — | — | — |
| `SDP-SOL-080` | [SOLID critiques, overapplication, and legacy refactoring](CURRICULUM.md#sdp-sol-080) | Professional | Approved | Not started | — | — | — | — |
| `SDP-PYT-010` | [Functions, closures, and callable objects as design tools](CURRICULUM.md#sdp-pyt-010) | Core | Approved | Not started | — | — | — | — |
| `SDP-PYT-020` | [Dispatch tables, dictionaries of callables, and registries](CURRICULUM.md#sdp-pyt-020) | Core | Approved | Not started | — | — | — | — |
| `SDP-PYT-030` | [Python decorator syntax versus the Decorator pattern](CURRICULUM.md#sdp-pyt-030) | Core | Absent | Not started | — | — | — | — |
| `SDP-PYT-040` | [Iterators, generators, and context managers as language-supported patterns](CURRICULUM.md#sdp-pyt-040) | Core | Absent | Not started | — | — | — | — |
| `SDP-PYT-050` | [Modules, import caching, and dependency lifetimes](CURRICULUM.md#sdp-pyt-050) | Core | Absent | Not started | — | — | — | — |
| `SDP-PYT-060` | [Dataclasses, immutable value objects, and enums](CURRICULUM.md#sdp-pyt-060) | Core | Absent | Not started | — | — | — | — |
| `SDP-PYT-070` | [Practical interface design with Protocols, ABCs, and duck typing](CURRICULUM.md#sdp-pyt-070) | Core | Absent | Not started | — | — | — | — |
| `SDP-PYT-080` | [singledispatch and open function extension](CURRICULUM.md#sdp-pyt-080) | Professional | Absent | Not started | — | — | — | — |
| `SDP-PYT-090` | [Dynamic registration and plugin discovery mechanics](CURRICULUM.md#sdp-pyt-090) | Professional | Absent | Not started | — | — | — | — |
| `SDP-PYT-100` | [Descriptors, class hooks, and metaclasses only when justified](CURRICULUM.md#sdp-pyt-100) | Advanced | Absent | Not started | — | — | — | — |
| `SDP-CRE-010` | [Factory Method](CURRICULUM.md#sdp-cre-010) | Core | Absent | Not started | — | — | — | — |
| `SDP-CRE-020` | [Abstract Factory](CURRICULUM.md#sdp-cre-020) | Professional | Absent | Not started | — | — | — | — |
| `SDP-CRE-030` | [Builder](CURRICULUM.md#sdp-cre-030) | Core | Absent | Not started | — | — | — | — |
| `SDP-CRE-040` | [Prototype](CURRICULUM.md#sdp-cre-040) | Advanced | Absent | Not started | — | — | — | — |
| `SDP-CRE-050` | [Singleton](CURRICULUM.md#sdp-cre-050) | Core | Absent | Not started | — | — | — | — |
| `SDP-STR-010` | [Adapter](CURRICULUM.md#sdp-str-010) | Core | Absent | Not started | — | — | — | — |
| `SDP-STR-020` | [Facade](CURRICULUM.md#sdp-str-020) | Core | Absent | Not started | — | — | — | — |
| `SDP-STR-030` | [Decorator](CURRICULUM.md#sdp-str-030) | Core | Absent | Not started | — | — | — | — |
| `SDP-STR-040` | [Proxy](CURRICULUM.md#sdp-str-040) | Core | Absent | Not started | — | — | — | — |
| `SDP-STR-050` | [Composite](CURRICULUM.md#sdp-str-050) | Professional | Absent | Not started | — | — | — | — |
| `SDP-STR-060` | [Bridge](CURRICULUM.md#sdp-str-060) | Professional | Absent | Not started | — | — | — | — |
| `SDP-STR-070` | [Flyweight](CURRICULUM.md#sdp-str-070) | Advanced | Absent | Not started | — | — | — | — |
| `SDP-BEH-010` | [Strategy](CURRICULUM.md#sdp-beh-010) | Core | Absent | Not started | — | — | — | — |
| `SDP-BEH-020` | [State](CURRICULUM.md#sdp-beh-020) | Core | Absent | Not started | — | — | — | — |
| `SDP-BEH-030` | [Observer](CURRICULUM.md#sdp-beh-030) | Core | Absent | Not started | — | — | — | — |
| `SDP-BEH-040` | [Command](CURRICULUM.md#sdp-beh-040) | Core | Absent | Not started | — | — | — | — |
| `SDP-BEH-050` | [Chain of Responsibility](CURRICULUM.md#sdp-beh-050) | Core | Absent | Not started | — | — | — | — |
| `SDP-BEH-060` | [Template Method](CURRICULUM.md#sdp-beh-060) | Professional | Absent | Not started | — | — | — | — |
| `SDP-BEH-070` | [Iterator](CURRICULUM.md#sdp-beh-070) | Core | Absent | Not started | — | — | — | — |
| `SDP-BEH-080` | [Mediator](CURRICULUM.md#sdp-beh-080) | Professional | Absent | Not started | — | — | — | — |
| `SDP-BEH-090` | [Memento](CURRICULUM.md#sdp-beh-090) | Advanced | Absent | Not started | — | — | — | — |
| `SDP-BEH-100` | [Visitor](CURRICULUM.md#sdp-beh-100) | Advanced | Absent | Not started | — | — | — | — |
| `SDP-BEH-110` | [Interpreter](CURRICULUM.md#sdp-beh-110) | Reference | Absent | Not started | — | — | — | — |
| `SDP-APP-010` | [Dependency Injection and the composition root](CURRICULUM.md#sdp-app-010) | Core | Absent | Not started | — | — | — | — |
| `SDP-APP-020` | [Null Object and sentinel alternatives](CURRICULUM.md#sdp-app-020) | Professional | Absent | Not started | — | — | — | — |
| `SDP-APP-030` | [Specification](CURRICULUM.md#sdp-app-030) | Professional | Absent | Not started | — | — | — | — |
| `SDP-APP-040` | [Repository](CURRICULUM.md#sdp-app-040) | Core | Absent | Not started | — | — | — | — |
| `SDP-APP-050` | [Unit of Work](CURRICULUM.md#sdp-app-050) | Core | Absent | Not started | — | — | — | — |
| `SDP-APP-060` | [Service Layer](CURRICULUM.md#sdp-app-060) | Core | Absent | Not started | — | — | — | — |
| `SDP-APP-070` | [Domain Events](CURRICULUM.md#sdp-app-070) | Professional | Absent | Not started | — | — | — | — |
| `SDP-APP-080` | [Pipeline](CURRICULUM.md#sdp-app-080) | Core | Absent | Not started | — | — | — | — |
| `SDP-APP-090` | [Transaction Script](CURRICULUM.md#sdp-app-090) | Professional | Absent | Not started | — | — | — | — |
| `SDP-APP-100` | [Active Record versus Data Mapper](CURRICULUM.md#sdp-app-100) | Professional | Absent | Not started | — | — | — | — |
| `SDP-APP-110` | [Identity Map and object identity](CURRICULUM.md#sdp-app-110) | Advanced | Absent | Not started | — | — | — | — |
| `SDP-APP-120` | [MVC, MVT, and presentation boundaries](CURRICULUM.md#sdp-app-120) | Professional | Absent | Not started | — | — | — | — |
| `SDP-ARC-010` | [Layered Architecture](CURRICULUM.md#sdp-arc-010) | Core | Absent | Not started | — | — | — | — |
| `SDP-ARC-020` | [Ports and Adapters / Hexagonal Architecture](CURRICULUM.md#sdp-arc-020) | Core | Absent | Not started | — | — | — | — |
| `SDP-ARC-030` | [Clean Architecture](CURRICULUM.md#sdp-arc-030) | Professional | Absent | Not started | — | — | — | — |
| `SDP-ARC-040` | [Functional Core, Imperative Shell](CURRICULUM.md#sdp-arc-040) | Core | Absent | Not started | — | — | — | — |
| `SDP-ARC-050` | [Event-driven application boundaries](CURRICULUM.md#sdp-arc-050) | Professional | Absent | Not started | — | — | — | — |
| `SDP-ARC-060` | [CQRS at application scale](CURRICULUM.md#sdp-arc-060) | Advanced | Absent | Not started | — | — | — | — |
| `SDP-ARC-070` | [Event Sourcing](CURRICULUM.md#sdp-arc-070) | Advanced | Absent | Not started | — | — | — | — |
| `SDP-ARC-080` | [Architectural boundaries and evolutionary design](CURRICULUM.md#sdp-arc-080) | Professional | Absent | Not started | — | — | — | — |
| `SDP-RAR-010` | [Object Pool](CURRICULUM.md#sdp-rar-010) | Reference | Absent | Not started | — | — | — | — |
| `SDP-RAR-020` | [Monostate / Borg](CURRICULUM.md#sdp-rar-020) | Reference | Absent | Not started | — | — | — | — |
| `SDP-RAR-030` | [Lazy Initialization](CURRICULUM.md#sdp-rar-030) | Professional | Absent | Not started | — | — | — | — |
| `SDP-RAR-040` | [Blackboard](CURRICULUM.md#sdp-rar-040) | Reference | Absent | Not started | — | — | — | — |
| `SDP-RAR-050` | [Service Locator](CURRICULUM.md#sdp-rar-050) | Professional | Absent | Not started | — | — | — | — |
| `SDP-RAR-060` | [Active Object](CURRICULUM.md#sdp-rar-060) | Reference | Absent | Not started | — | — | — | — |
| `SDP-RAR-070` | [Saga as a distributed workflow pattern](CURRICULUM.md#sdp-rar-070) | Advanced | Absent | Not started | — | — | — | — |
| `SDP-RAR-080` | [Circuit Breaker as a resilience pattern](CURRICULUM.md#sdp-rar-080) | Professional | Absent | Not started | — | — | — | — |
| `SDP-REF-010` | [Design smells and change-force diagnosis](CURRICULUM.md#sdp-ref-010) | Core | Absent | Not started | — | — | — | — |
| `SDP-REF-020` | [God Object, Spaghetti Code, and Shotgun Surgery](CURRICULUM.md#sdp-ref-020) | Core | Absent | Not started | — | — | — | — |
| `SDP-REF-030` | [Feature Envy, Primitive Obsession, and weak domain models](CURRICULUM.md#sdp-ref-030) | Professional | Absent | Not started | — | — | — | — |
| `SDP-REF-040` | [Excessive inheritance and fragile hierarchies](CURRICULUM.md#sdp-ref-040) | Core | Absent | Not started | — | — | — | — |
| `SDP-REF-050` | [Boolean flags, giant conditional dispatch, and hidden state](CURRICULUM.md#sdp-ref-050) | Core | Absent | Not started | — | — | — | — |
| `SDP-REF-060` | [Singleton and Service Locator misuse](CURRICULUM.md#sdp-ref-060) | Core | Absent | Not started | — | — | — | — |
| `SDP-REF-070` | [Circular dependencies and temporal coupling](CURRICULUM.md#sdp-ref-070) | Core | Absent | Not started | — | — | — | — |
| `SDP-REF-080` | [Mock-heavy tests and meaningless interfaces](CURRICULUM.md#sdp-ref-080) | Core | Absent | Not started | — | — | — | — |
| `SDP-REF-090` | [Unnecessary factories, abstraction layers, and pattern soup](CURRICULUM.md#sdp-ref-090) | Core | Absent | Not started | — | — | — | — |
| `SDP-REF-100` | [Safe incremental refactoring with characterization tests](CURRICULUM.md#sdp-ref-100) | Core | Absent | Not started | — | — | — | — |
| `SDP-INT-010` | [Scenario recognition and choosing the simplest design](CURRICULUM.md#sdp-int-010) | Core | Absent | Not started | — | — | — | — |
| `SDP-INT-020` | [Strategy versus State versus Template Method versus Command](CURRICULUM.md#sdp-int-020) | Core | Absent | Not started | — | — | — | — |
| `SDP-INT-030` | [Adapter versus Facade versus Proxy versus Decorator](CURRICULUM.md#sdp-int-030) | Core | Absent | Not started | — | — | — | — |
| `SDP-INT-040` | [Bridge versus Adapter; Composite versus Decorator](CURRICULUM.md#sdp-int-040) | Professional | Absent | Not started | — | — | — | — |
| `SDP-INT-050` | [Factory Method versus Abstract Factory versus Builder versus Prototype](CURRICULUM.md#sdp-int-050) | Core | Absent | Not started | — | — | — | — |
| `SDP-INT-060` | [Observer versus publish/subscribe versus Mediator versus Domain Events](CURRICULUM.md#sdp-int-060) | Core | Absent | Not started | — | — | — | — |
| `SDP-INT-070` | [Dependency Inversion versus Injection versus IoC versus Service Locator](CURRICULUM.md#sdp-int-070) | Core | Absent | Not started | — | — | — | — |
| `SDP-INT-080` | [Protocol versus ABC versus duck typing; inheritance versus composition versus delegation](CURRICULUM.md#sdp-int-080) | Core | Absent | Not started | — | — | — | — |
| `SDP-INT-090` | [Repository versus DAO and Unit of Work; object versus architectural boundaries](CURRICULUM.md#sdp-int-090) | Core | Absent | Not started | — | — | — | — |
| `SDP-INT-100` | [Senior pattern combinations, code review, and mock interview synthesis](CURRICULUM.md#sdp-int-100) | Core | Absent | Not started | — | — | — | — |

## Project tracker

Project state is separate from curriculum-unit learning state. Starting or completing a project never advances a unit automatically.

| Project ID | Project name | Project state | Branch | Last evidence date | Evidence link | Remaining weakness or unfinished requirement |
|---|---|---|---|---|---|---|
| `SDP-PRJ-010` | [SOLID Legacy Refactoring Clinic](PROJECTS.md#sdp-prj-010) | Planned | `project/SDP-PRJ-010` | — | — | Not initialized |
| `SDP-PRJ-020` | [Extensible Pricing and Promotion Engine](PROJECTS.md#sdp-prj-020) | Planned | `project/SDP-PRJ-020` | — | — | Not initialized |
| `SDP-PRJ-030` | [Multi-provider Notification Gateway](PROJECTS.md#sdp-prj-030) | Planned | `project/SDP-PRJ-030` | — | — | Not initialized |
| `SDP-PRJ-040` | [Typed Rule and Plugin Engine](PROJECTS.md#sdp-prj-040) | Planned | `project/SDP-PRJ-040` | — | — | Not initialized |
| `SDP-PRJ-050` | [Auditable Workflow and Command Engine](PROJECTS.md#sdp-prj-050) | Planned | `project/SDP-PRJ-050` | — | — | Not initialized |
| `SDP-PRJ-060` | [Python Backend Architecture Lab](PROJECTS.md#sdp-prj-060) | Planned | `project/SDP-PRJ-060` | — | — | Not initialized |

## Tracker rules

- Use complete canonical IDs.
- Set artifact state to Draft during initialization without changing learning state.
- Record exact weaknesses, such as “Cannot distinguish access control from interface adaptation,” not “needs revision.”
- Evidence links must point to existing files or headings.
- A project may link evidence to a unit, but the unit must still pass its own transition criteria.
- Dates use `YYYY-MM-DD`.
