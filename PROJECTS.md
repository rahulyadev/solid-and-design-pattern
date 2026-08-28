# Milestone Projects

[Learning paths](LEARNING_PATHS.md) · [Progress](PROGRESS.md) · [Workflow](docs/WORKFLOW.md)

Projects integrate multiple units and create interview-ready evidence. They are not curriculum units and never advance unit states automatically. Project folders are created only when initialized.

## Project overview

| Project ID | Project | Main integration |
|---|---|---|
| `SDP-PRJ-010` | [SOLID Legacy Refactoring Clinic](#sdp-prj-010) | Refactoring, SOLID |
| `SDP-PRJ-020` | [Extensible Pricing and Promotion Engine](#sdp-prj-020) | Application, Python |
| `SDP-PRJ-030` | [Multi-provider Notification Gateway](#sdp-prj-030) | Backend integration |
| `SDP-PRJ-040` | [Typed Rule and Plugin Engine](#sdp-prj-040) | Python extensibility |
| `SDP-PRJ-050` | [Auditable Workflow and Command Engine](#sdp-prj-050) | Workflow, Behavioral |
| `SDP-PRJ-060` | [Python Backend Architecture Lab](#sdp-prj-060) | Backend architecture |

## Project workflow

Initialize in a dedicated Worktree chat with:

```text
Initialize project <PROJECT-ID>.
```

This creates or safely resumes exactly `project/<PROJECT-ID>`, generates the just-in-time project starter, changes only the matching project tracker row to Active, validates, and commits. Before any automatic push, Codex enumerates local-only commits and pushes only commits created during the current initialization operation. It stops if older local-only project work would also be published, and it does not push again when the validated initialized version is already remote. It does not open a pull request or merge.

<a id="sdp-prj-010"></a>
## SDP-PRJ-010 — SOLID Legacy Refactoring Clinic

Stabilize a deliberately tangled Python codebase with characterization tests, then refactor responsibilities and dependencies without pattern soup.

### Prerequisites

**Required:** [`SDP-FND-020`](CURRICULUM.md#sdp-fnd-020), [`SDP-FND-030`](CURRICULUM.md#sdp-fnd-030), [`SDP-FND-050`](CURRICULUM.md#sdp-fnd-050), [`SDP-FND-080`](CURRICULUM.md#sdp-fnd-080), [`SDP-SOL-010`](CURRICULUM.md#sdp-sol-010), [`SDP-SOL-020`](CURRICULUM.md#sdp-sol-020), [`SDP-SOL-030`](CURRICULUM.md#sdp-sol-030), [`SDP-SOL-050`](CURRICULUM.md#sdp-sol-050), [`SDP-REF-010`](CURRICULUM.md#sdp-ref-010), [`SDP-REF-100`](CURRICULUM.md#sdp-ref-100)

**Recommended:** [`SDP-SOL-060`](CURRICULUM.md#sdp-sol-060), [`SDP-SOL-080`](CURRICULUM.md#sdp-sol-080), [`SDP-REF-020`](CURRICULUM.md#sdp-ref-020), [`SDP-REF-040`](CURRICULUM.md#sdp-ref-040), [`SDP-REF-080`](CURRICULUM.md#sdp-ref-080), [`SDP-REF-090`](CURRICULUM.md#sdp-ref-090)

### Patterns and principles integrated

SRP, OCP, LSP, DIP, characterization testing, incremental refactoring.

### Deliberately poor starting design

A single service object parses input, calculates results, sends notifications, writes files, and reaches global dependencies. Existing behaviour is poorly documented.

### Staged change pressure

1. Add characterization tests around current behaviour.
2. Separate volatile I/O from policy without changing outputs.
3. Introduce explicit dependencies and remove hidden global state.
4. Add a new requirement that exposes a weak responsibility boundary.
5. Compare the chosen refactoring with a smaller alternative and remove unnecessary abstraction.

### Required visuals

- Before/after dependency diagram.
- Object or call collaboration diagram.
- At least one sequence diagram for the main use case.
- Every non-trivial visual must include how to read it, the key insight, and its simplification or limitation.

### Tests and evidence

- Unit tests for pure policies and value objects.
- Contract tests for replaceable implementations.
- Integration tests across the principal boundary.
- At least one deliberate regression test for every seeded defect.
- A written design decision comparing the chosen pattern with a simpler alternative.

### Seeded defects

- A mock patches the wrong namespace.
- A subclass strengthens a precondition and breaks substitution.
- A new interface has one meaningless implementation.

### Refactoring checkpoints

At each stage, preserve the previous tests, identify the new force, name the smallest safe change, document a rejected alternative, and explain whether a named pattern is actually needed.

### Definition of done

- [ ] Characterization and focused unit tests pass.
- [ ] At least three responsibilities are moved for explicit reasons.
- [ ] One proposed pattern is rejected and documented.
- [ ] The final design has no hidden global dependency.
- [ ] Rahul can explain each change as a response to a concrete force.
- [ ] Repository validation and all project tests pass.
- [ ] A final one-question-at-a-time senior interview walkthrough is recorded.
- [ ] Project evidence is linked without automatic unit-state changes.

### Senior interview walkthrough

1. What changed first, and why was the original design inadequate?
2. Which pattern was selected, and what simpler alternative was rejected?
3. Which dependency direction or object collaboration matters most?
4. What failure or test exposed the hardest flaw?
5. What would you remove if the requirements became simpler?
6. Which parts are Python language mechanics and which are design-level choices?

<a id="sdp-prj-020"></a>
## SDP-PRJ-020 — Extensible Pricing and Promotion Engine

Evolve a simple checkout calculator through staged requirements for pricing policies, promotions, eligibility rules, and audit explanations.

### Prerequisites

**Required:** [`SDP-SOL-010`](CURRICULUM.md#sdp-sol-010), [`SDP-SOL-020`](CURRICULUM.md#sdp-sol-020), [`SDP-SOL-030`](CURRICULUM.md#sdp-sol-030), [`SDP-PYT-010`](CURRICULUM.md#sdp-pyt-010), [`SDP-CRE-010`](CURRICULUM.md#sdp-cre-010), [`SDP-BEH-010`](CURRICULUM.md#sdp-beh-010), [`SDP-APP-030`](CURRICULUM.md#sdp-app-030), [`SDP-REF-050`](CURRICULUM.md#sdp-ref-050)

**Recommended:** [`SDP-BEH-050`](CURRICULUM.md#sdp-beh-050), [`SDP-PYT-020`](CURRICULUM.md#sdp-pyt-020), [`SDP-PYT-060`](CURRICULUM.md#sdp-pyt-060), [`SDP-INT-020`](CURRICULUM.md#sdp-int-020)

### Patterns and principles integrated

Strategy, Factory Method, Specification, Chain of Responsibility, value objects.

### Deliberately poor starting design

A checkout function contains growing `if/elif` trees for customer type, product type, coupon type, and campaign date.

### Staged change pressure

1. Add one replaceable pricing policy.
2. Add composable eligibility specifications.
3. Add a factory boundary for configured policies.
4. Add an ordered promotion chain with explicit stopping rules.
5. Generate an audit explanation without coupling it to the calculation core.

### Required visuals

- Before/after dependency diagram.
- Object or call collaboration diagram.
- At least one sequence diagram for the main use case.
- Every non-trivial visual must include how to read it, the key insight, and its simplification or limitation.

### Tests and evidence

- Unit tests for pure policies and value objects.
- Contract tests for replaceable implementations.
- Integration tests across the principal boundary.
- At least one deliberate regression test for every seeded defect.
- A written design decision comparing the chosen pattern with a simpler alternative.

### Seeded defects

- Promotion order changes silently.
- A mutable default policy list leaks between tests.
- A Strategy object is created where a plain function is clearer.

### Refactoring checkpoints

At each stage, preserve the previous tests, identify the new force, name the smallest safe change, document a rejected alternative, and explain whether a named pattern is actually needed.

### Definition of done

- [ ] Staged requirements are implemented through stable extension points.
- [ ] All pricing and eligibility edge cases have tests.
- [ ] The design compares functions, objects, and dispatch tables.
- [ ] The audit path is observable and deterministic.
- [ ] Rahul defends Strategy, Specification, Factory, and Chain choices.
- [ ] Repository validation and all project tests pass.
- [ ] A final one-question-at-a-time senior interview walkthrough is recorded.
- [ ] Project evidence is linked without automatic unit-state changes.

### Senior interview walkthrough

1. What changed first, and why was the original design inadequate?
2. Which pattern was selected, and what simpler alternative was rejected?
3. Which dependency direction or object collaboration matters most?
4. What failure or test exposed the hardest flaw?
5. What would you remove if the requirements became simpler?
6. Which parts are Python language mechanics and which are design-level choices?

<a id="sdp-prj-030"></a>
## SDP-PRJ-030 — Multi-provider Notification Gateway

Design a provider-neutral notification boundary with adapters, retries, observability, fallback, and controlled event callbacks.

### Prerequisites

**Required:** [`SDP-SOL-050`](CURRICULUM.md#sdp-sol-050), [`SDP-APP-010`](CURRICULUM.md#sdp-app-010), [`SDP-STR-010`](CURRICULUM.md#sdp-str-010), [`SDP-STR-020`](CURRICULUM.md#sdp-str-020), [`SDP-STR-040`](CURRICULUM.md#sdp-str-040), [`SDP-BEH-030`](CURRICULUM.md#sdp-beh-030), [`SDP-BEH-050`](CURRICULUM.md#sdp-beh-050), [`SDP-APP-060`](CURRICULUM.md#sdp-app-060)

**Recommended:** [`SDP-RAR-080`](CURRICULUM.md#sdp-rar-080), [`SDP-ARC-050`](CURRICULUM.md#sdp-arc-050), [`SDP-PYT-070`](CURRICULUM.md#sdp-pyt-070), [`SDP-INT-030`](CURRICULUM.md#sdp-int-030), [`SDP-INT-060`](CURRICULUM.md#sdp-int-060)

### Patterns and principles integrated

Adapter, Facade, Proxy, Observer, Chain of Responsibility, Dependency Injection.

### Deliberately poor starting design

Application code calls vendor SDKs directly, repeats retry logic, and mixes provider errors with business decisions.

### Staged change pressure

1. Create a provider-neutral port and one adapter.
2. Add a second provider without modifying application policy.
3. Add a Facade for the application use case.
4. Add retry/fallback through explicit handlers or proxy behaviour.
5. Add event callbacks and structured diagnostics.

### Required visuals

- Before/after dependency diagram.
- Object or call collaboration diagram.
- At least one sequence diagram for the main use case.
- Every non-trivial visual must include how to read it, the key insight, and its simplification or limitation.

### Tests and evidence

- Unit tests for pure policies and value objects.
- Contract tests for replaceable implementations.
- Integration tests across the principal boundary.
- At least one deliberate regression test for every seeded defect.
- A written design decision comparing the chosen pattern with a simpler alternative.

### Seeded defects

- A retry catches every exception.
- A callback retains an object longer than intended.
- A proxy changes business semantics without documenting it.

### Refactoring checkpoints

At each stage, preserve the previous tests, identify the new force, name the smallest safe change, document a rejected alternative, and explain whether a named pattern is actually needed.

### Definition of done

- [ ] At least two providers pass a shared contract suite.
- [ ] Fallback and failure rules are explicit.
- [ ] No vendor type leaks into application policy.
- [ ] Observability shows provider choice, attempts, and final outcome.
- [ ] Rahul compares Adapter, Facade, Proxy, Chain, and Observer.
- [ ] Repository validation and all project tests pass.
- [ ] A final one-question-at-a-time senior interview walkthrough is recorded.
- [ ] Project evidence is linked without automatic unit-state changes.

### Senior interview walkthrough

1. What changed first, and why was the original design inadequate?
2. Which pattern was selected, and what simpler alternative was rejected?
3. Which dependency direction or object collaboration matters most?
4. What failure or test exposed the hardest flaw?
5. What would you remove if the requirements became simpler?
6. Which parts are Python language mechanics and which are design-level choices?

<a id="sdp-prj-040"></a>
## SDP-PRJ-040 — Typed Rule and Plugin Engine

Build a framework-free typed plugin system with rule discovery, deterministic ordering, duplicate detection, and safe extension contracts.

### Prerequisites

**Required:** [`SDP-PYT-020`](CURRICULUM.md#sdp-pyt-020), [`SDP-PYT-070`](CURRICULUM.md#sdp-pyt-070), [`SDP-PYT-090`](CURRICULUM.md#sdp-pyt-090), [`SDP-CRE-010`](CURRICULUM.md#sdp-cre-010), [`SDP-BEH-010`](CURRICULUM.md#sdp-beh-010), [`SDP-APP-030`](CURRICULUM.md#sdp-app-030), [`SDP-SOL-020`](CURRICULUM.md#sdp-sol-020)

**Recommended:** [`SDP-PYT-080`](CURRICULUM.md#sdp-pyt-080), [`SDP-PYT-100`](CURRICULUM.md#sdp-pyt-100), [`SDP-BEH-110`](CURRICULUM.md#sdp-beh-110), [`SDP-INT-080`](CURRICULUM.md#sdp-int-080)

### Patterns and principles integrated

Registry, Plugin, Factory Method, Strategy, Specification, Protocol.

### Deliberately poor starting design

Rules are imported manually into a global dictionary, duplicate names overwrite silently, and plugin tests depend on import order.

### Staged change pressure

1. Define a typed rule Protocol.
2. Build deterministic registration with duplicate detection.
3. Add plugin discovery behind an explicit boundary.
4. Add specifications and priorities.
5. Compare class hooks, decorators, entry points, and a plain configuration list.

### Required visuals

- Before/after dependency diagram.
- Object or call collaboration diagram.
- At least one sequence diagram for the main use case.
- Every non-trivial visual must include how to read it, the key insight, and its simplification or limitation.

### Tests and evidence

- Unit tests for pure policies and value objects.
- Contract tests for replaceable implementations.
- Integration tests across the principal boundary.
- At least one deliberate regression test for every seeded defect.
- A written design decision comparing the chosen pattern with a simpler alternative.

### Seeded defects

- Import-time side effects register twice.
- A plugin violates the return contract.
- The registry is shared across tests.

### Refactoring checkpoints

At each stage, preserve the previous tests, identify the new force, name the smallest safe change, document a rejected alternative, and explain whether a named pattern is actually needed.

### Definition of done

- [ ] Discovery and execution are deterministic.
- [ ] Duplicate and invalid plugins fail clearly.
- [ ] Tests isolate registry state.
- [ ] The simplest rejected design is documented.
- [ ] Rahul defends Protocol, Registry, Factory Method, Strategy, and Specification.
- [ ] Repository validation and all project tests pass.
- [ ] A final one-question-at-a-time senior interview walkthrough is recorded.
- [ ] Project evidence is linked without automatic unit-state changes.

### Senior interview walkthrough

1. What changed first, and why was the original design inadequate?
2. Which pattern was selected, and what simpler alternative was rejected?
3. Which dependency direction or object collaboration matters most?
4. What failure or test exposed the hardest flaw?
5. What would you remove if the requirements became simpler?
6. Which parts are Python language mechanics and which are design-level choices?

<a id="sdp-prj-050"></a>
## SDP-PRJ-050 — Auditable Workflow and Command Engine

Implement a stateful workflow with commands, audit records, undoable operations, notifications, and explicit transition invariants.

### Prerequisites

**Required:** [`SDP-FND-090`](CURRICULUM.md#sdp-fnd-090), [`SDP-BEH-020`](CURRICULUM.md#sdp-beh-020), [`SDP-BEH-030`](CURRICULUM.md#sdp-beh-030), [`SDP-BEH-040`](CURRICULUM.md#sdp-beh-040), [`SDP-BEH-090`](CURRICULUM.md#sdp-beh-090), [`SDP-PYT-060`](CURRICULUM.md#sdp-pyt-060), [`SDP-REF-050`](CURRICULUM.md#sdp-ref-050)

**Recommended:** [`SDP-BEH-050`](CURRICULUM.md#sdp-beh-050), [`SDP-APP-070`](CURRICULUM.md#sdp-app-070), [`SDP-INT-020`](CURRICULUM.md#sdp-int-020), [`SDP-RAR-060`](CURRICULUM.md#sdp-rar-060)

### Patterns and principles integrated

State, Command, Memento, Observer, value objects.

### Deliberately poor starting design

Workflow code uses status strings, nested conditionals, ad-hoc audit messages, and direct mutation that cannot be undone.

### Staged change pressure

1. Model explicit states and allowed transitions.
2. Represent user actions as commands.
3. Record audit events.
4. Add reversible operations with a bounded memento.
5. Notify listeners without allowing observers to corrupt transitions.

### Required visuals

- Before/after dependency diagram.
- Object or call collaboration diagram.
- At least one sequence diagram for the main use case.
- Every non-trivial visual must include how to read it, the key insight, and its simplification or limitation.

### Tests and evidence

- Unit tests for pure policies and value objects.
- Contract tests for replaceable implementations.
- Integration tests across the principal boundary.
- At least one deliberate regression test for every seeded defect.
- A written design decision comparing the chosen pattern with a simpler alternative.

### Seeded defects

- A transition partially mutates before failing.
- Undo restores data but not the state invariant.
- An observer re-enters the workflow unexpectedly.

### Refactoring checkpoints

At each stage, preserve the previous tests, identify the new force, name the smallest safe change, document a rejected alternative, and explain whether a named pattern is actually needed.

### Definition of done

- [ ] Invalid transitions leave the workflow unchanged.
- [ ] Commands and audit records are deterministic.
- [ ] Undo behaviour and storage limits are tested.
- [ ] Observer failures have an explicit policy.
- [ ] Rahul compares State, Strategy, Command, Memento, and Observer.
- [ ] Repository validation and all project tests pass.
- [ ] A final one-question-at-a-time senior interview walkthrough is recorded.
- [ ] Project evidence is linked without automatic unit-state changes.

### Senior interview walkthrough

1. What changed first, and why was the original design inadequate?
2. Which pattern was selected, and what simpler alternative was rejected?
3. Which dependency direction or object collaboration matters most?
4. What failure or test exposed the hardest flaw?
5. What would you remove if the requirements became simpler?
6. Which parts are Python language mechanics and which are design-level choices?

<a id="sdp-prj-060"></a>
## SDP-PRJ-060 — Python Backend Architecture Lab

Build an in-memory backend application with explicit use cases, persistence ports, transaction boundaries, domain events, and replaceable adapters.

### Prerequisites

**Required:** [`SDP-APP-010`](CURRICULUM.md#sdp-app-010), [`SDP-APP-040`](CURRICULUM.md#sdp-app-040), [`SDP-APP-050`](CURRICULUM.md#sdp-app-050), [`SDP-APP-060`](CURRICULUM.md#sdp-app-060), [`SDP-APP-070`](CURRICULUM.md#sdp-app-070), [`SDP-ARC-010`](CURRICULUM.md#sdp-arc-010), [`SDP-ARC-020`](CURRICULUM.md#sdp-arc-020), [`SDP-ARC-040`](CURRICULUM.md#sdp-arc-040), [`SDP-SOL-050`](CURRICULUM.md#sdp-sol-050)

**Recommended:** [`SDP-ARC-030`](CURRICULUM.md#sdp-arc-030), [`SDP-ARC-050`](CURRICULUM.md#sdp-arc-050), [`SDP-APP-100`](CURRICULUM.md#sdp-app-100), [`SDP-APP-120`](CURRICULUM.md#sdp-app-120), [`SDP-INT-090`](CURRICULUM.md#sdp-int-090)

### Patterns and principles integrated

Dependency Injection, Repository, Unit of Work, Service Layer, Domain Events, Hexagonal Architecture.

### Deliberately poor starting design

A small backend mixes request parsing, business rules, ORM-like persistence, transaction control, and event publication in one layer.

### Staged change pressure

1. Define application use cases in a Service Layer.
2. Introduce Repository ports and in-memory adapters.
3. Add a Unit of Work boundary.
4. Compose dependencies at one root.
5. Record Domain Events and handle them at an application boundary.
6. Add an optional thin HTTP adapter without making the project a framework course.

### Required visuals

- Before/after dependency diagram.
- Object or call collaboration diagram.
- At least one sequence diagram for the main use case.
- Every non-trivial visual must include how to read it, the key insight, and its simplification or limitation.

### Tests and evidence

- Unit tests for pure policies and value objects.
- Contract tests for replaceable implementations.
- Integration tests across the principal boundary.
- At least one deliberate regression test for every seeded defect.
- A written design decision comparing the chosen pattern with a simpler alternative.

### Seeded defects

- A repository commits implicitly.
- A domain object imports infrastructure.
- An event is published before a failed transaction completes.

### Refactoring checkpoints

At each stage, preserve the previous tests, identify the new force, name the smallest safe change, document a rejected alternative, and explain whether a named pattern is actually needed.

### Definition of done

- [ ] Application policy runs without a web framework or real database.
- [ ] Transaction ownership is explicit and tested.
- [ ] Adapters can be replaced without changing use cases.
- [ ] Domain events respect commit outcome.
- [ ] Rahul defends Layered, Hexagonal, Functional Core, Repository, UoW, Service Layer, and DI choices.
- [ ] Repository validation and all project tests pass.
- [ ] A final one-question-at-a-time senior interview walkthrough is recorded.
- [ ] Project evidence is linked without automatic unit-state changes.

### Senior interview walkthrough

1. What changed first, and why was the original design inadequate?
2. Which pattern was selected, and what simpler alternative was rejected?
3. Which dependency direction or object collaboration matters most?
4. What failure or test exposed the hardest flaw?
5. What would you remove if the requirements became simpler?
6. Which parts are Python language mechanics and which are design-level choices?
