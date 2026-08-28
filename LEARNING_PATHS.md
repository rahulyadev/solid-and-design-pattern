# Learning Paths

[Curriculum](CURRICULUM.md) · [Progress](PROGRESS.md) · [Projects](PROJECTS.md) · [Python references](PYTHON_REFERENCES.md)

Paths are recommendations, not gates. A learner may initialize any unit in any order. Codex should warn about important prerequisites, supply the smallest correct bridge, and continue unless the result would be materially misleading.

## Study-depth contracts

The same canonical unit can be studied at two deliberately different depths.

### Rapid interview pass

Use this depth only for urgent interview paths. For each unit, cover the `Physical Notebook Core`, essential visual, minimal Python example, scenario-recognition cues, one important comparison, common interview traps, and focused interview questions. A rapid pass does **not** require the full lab, every exercise, complete history, all implementation variants, internals, or evidence needed to advance the unit to Practiced.

### Full mastery pass

Complete the entire unit: deep explanation, history where relevant, implementation variants, exercises, experiments, tests, refactoring, comparison work, and the unit's evidence profile. The estimate combines the canonical first-understanding and hands-on-practice ranges; spaced retrieval and milestone-project transfer remain additional.

| Unit size | Rapid interview pass | Full mastery pass |
|---|---:|---:|
| S | 10–15 min | 2–5 h |
| M | 15–25 min | 5–10 h |
| L | 20–30 min | 9–15 h |
| XL | 30–45 min | 14–23 h |

The first four paths calculate their rapid unit totals from this table, then add separate time for required practice, recall, comparisons, mock interviews, and project or refactoring checkpoints.

## Choose a path

- [Emergency interview revision](#emergency-interview-revision)
- [7-day interview crash path](#seven-day-interview-crash)
- [14-day interview preparation](#fourteen-day-interview-preparation)
- [30-day strong-foundation path](#thirty-day-strong-foundation)
- [Complete SOLID and design-pattern mastery](#complete-solid-pattern-mastery)
- [Python backend and application architecture](#python-backend-application-architecture)
- [Refactoring and Pythonic design](#refactoring-pythonic-design)
- [Senior interview comparison and design practice](#senior-comparison-design-practice)

<a id="emergency-interview-revision"></a>
## Emergency interview revision

**Who it is for:** An experienced Python engineer with an interview within one or two days who needs recognition, explanation, and comparison—not full mastery evidence.

**Recommended depth:** Rapid interview pass.

**Time assumption:** One or two intensive days. Plan **9 h 45 min–14 h** for the required rapid path; this is not full mastery.

**Rapid-pass unit total:** 7 h 15 min–11 h.

**Required path activities:** 2 h 30 min–3 h.

**Rapid-path total:** 9 h 45 min–14 h.

**Full-mastery unit total:** 189–321 h before spaced retention and milestone projects.

### Required timed activity breakdown

| Activity | Required time |
|---|---:|
| Recall | 45 min |
| Comparison | 30–45 min |
| Mock interview | 45 min |
| Refactoring/project checkpoint | 30–45 min |

**SOLID coverage:** Complete five-principle coverage: SRP, OCP, LSP, ISP, and DIP.

**Prerequisite policy:** Assumed prior knowledge: working Python functions, classes, imports, and testing. Use a prerequisite bridge for omitted internal units. Every prerequisite that is included appears earlier.

**Intentionally deferred:** Detailed GoF coverage, rare patterns, architectural depth, full projects, and spaced-retention evidence.

**Canonical units in this path:** 22

### Recommended sequence

1. [SDP-FND-010 — Design vocabulary: principle, pattern, idiom, framework, and architecture](CURRICULUM.md#sdp-fnd-010)
2. [SDP-FND-020 — Change pressure, responsibilities, and boundaries](CURRICULUM.md#sdp-fnd-020)
3. [SDP-FND-030 — Cohesion, coupling, and dependency direction](CURRICULUM.md#sdp-fnd-030)
4. [SDP-FND-050 — Composition, delegation, and inheritance](CURRICULUM.md#sdp-fnd-050)
5. [SDP-FND-070 — Duck typing, structural typing, nominal typing, Protocols, and ABCs](CURRICULUM.md#sdp-fnd-070)
6. [SDP-FND-110 — Simplicity heuristics and collaboration laws](CURRICULUM.md#sdp-fnd-110)
7. [SDP-SOL-010 — Single Responsibility Principle](CURRICULUM.md#sdp-sol-010)
8. [SDP-SOL-020 — Open/Closed Principle](CURRICULUM.md#sdp-sol-020)
9. [SDP-SOL-030 — Liskov Substitution Principle and behavioural subtyping](CURRICULUM.md#sdp-sol-030)
10. [SDP-SOL-040 — Interface Segregation Principle](CURRICULUM.md#sdp-sol-040)
11. [SDP-SOL-050 — Dependency Inversion Principle](CURRICULUM.md#sdp-sol-050)
12. [SDP-PYT-010 — Functions, closures, and callable objects as design tools](CURRICULUM.md#sdp-pyt-010)
13. [SDP-PYT-070 — Practical interface design with Protocols, ABCs, and duck typing](CURRICULUM.md#sdp-pyt-070)
14. [SDP-CRE-010 — Factory Method](CURRICULUM.md#sdp-cre-010)
15. [SDP-STR-010 — Adapter](CURRICULUM.md#sdp-str-010)
16. [SDP-STR-030 — Decorator](CURRICULUM.md#sdp-str-030)
17. [SDP-BEH-010 — Strategy](CURRICULUM.md#sdp-beh-010)
18. [SDP-BEH-020 — State](CURRICULUM.md#sdp-beh-020)
19. [SDP-BEH-030 — Observer](CURRICULUM.md#sdp-beh-030)
20. [SDP-APP-010 — Dependency Injection and the composition root](CURRICULUM.md#sdp-app-010)
21. [SDP-REF-010 — Design smells and change-force diagnosis](CURRICULUM.md#sdp-ref-010)
22. [SDP-INT-010 — Scenario recognition and choosing the simplest design](CURRICULUM.md#sdp-int-010)

### Practice, recall, and interview schedule

| Session | Unit steps | Required activity |
|---|---|---|
| Block 1 | Steps 1–6 | Rapid-pass design vocabulary, change forces, boundaries, composition, interfaces, and simplicity. |
| Block 2 | Steps 7–11 | Rapid-pass all five SOLID principles, with extra time on LSP, ISP, and DIP. |
| Block 3 | Steps 12–20 | Rapid-pass Pythonic callables, Factory Method, Adapter, Decorator, Strategy, State, Observer, and DI. |
| Block 4 | Steps 21–22 | Smell recognition and scenario selection. |
| Recall | 45 min | Closed-book definitions, three diagrams, and one refactoring explanation. |
| Comparison | 30–45 min | Compare Strategy/State and Adapter/Decorator from scenarios. |
| Mock interview | 45 min | One question at a time: SOLID violation, pattern selection, trade-off, and simpler Python alternative. |

### Project or refactoring milestones

- [SDP-PRJ-010 — SOLID Legacy Refactoring Clinic](PROJECTS.md#sdp-prj-010) — Use a 30–45 minute characterization-test and responsibility-splitting checkpoint; do not attempt the full project.

### Completion meaning

Finishing a path does not automatically mark every unit Retained or Mastered. Each unit advances only through the evidence rules in [PROGRESS.md](PROGRESS.md).

<a id="seven-day-interview-crash"></a>
## 7-day interview crash path

**Who it is for:** Rahul when interviews are close and he needs a serious first pass over SOLID and the most recognizable Python patterns.

**Recommended depth:** Rapid interview pass plus selected focused labs.

**Time assumption:** Seven days at approximately 3.5–5 focused hours per day. The required rapid path totals **25 h 15 min–35 h 5 min**.

**Rapid-pass unit total:** 13 h 15 min–20 h 5 min.

**Required path activities:** 12–15 h.

**Rapid-path total:** 25 h 15 min–35 h 5 min.

**Full-mastery unit total:** 348–589 h before spaced retention and milestone projects.

The 12–15 activity hours cover seven focused labs or refactorings, daily closed-book recall, two comparison sessions, one mock interview, and a reduced project checkpoint.

**SOLID coverage:** Complete five-principle coverage: SRP, OCP, LSP, ISP, and DIP.

**Prerequisite policy:** Assumed prior knowledge: professional Python basics. Use prerequisite bridges for omitted specialist units. Every included prerequisite appears earlier.

**Intentionally deferred:** Visitor, Interpreter, Flyweight, most rare patterns, deep architecture, event sourcing, CQRS, and full long-term reviews.

**Canonical units in this path:** 40

### Recommended sequence

1. [SDP-FND-010 — Design vocabulary: principle, pattern, idiom, framework, and architecture](CURRICULUM.md#sdp-fnd-010)
2. [SDP-FND-020 — Change pressure, responsibilities, and boundaries](CURRICULUM.md#sdp-fnd-020)
3. [SDP-FND-030 — Cohesion, coupling, and dependency direction](CURRICULUM.md#sdp-fnd-030)
4. [SDP-FND-040 — Abstraction, encapsulation, information hiding, and contracts](CURRICULUM.md#sdp-fnd-040)
5. [SDP-FND-050 — Composition, delegation, and inheritance](CURRICULUM.md#sdp-fnd-050)
6. [SDP-FND-060 — Polymorphism, dynamic dispatch, and subtyping](CURRICULUM.md#sdp-fnd-060)
7. [SDP-FND-070 — Duck typing, structural typing, nominal typing, Protocols, and ABCs](CURRICULUM.md#sdp-fnd-070)
8. [SDP-FND-080 — Dependency management, test seams, and test doubles](CURRICULUM.md#sdp-fnd-080)
9. [SDP-FND-100 — Modules, package boundaries, and circular dependencies](CURRICULUM.md#sdp-fnd-100)
10. [SDP-FND-110 — Simplicity heuristics and collaboration laws](CURRICULUM.md#sdp-fnd-110)
11. [SDP-SOL-010 — Single Responsibility Principle](CURRICULUM.md#sdp-sol-010)
12. [SDP-SOL-020 — Open/Closed Principle](CURRICULUM.md#sdp-sol-020)
13. [SDP-SOL-030 — Liskov Substitution Principle and behavioural subtyping](CURRICULUM.md#sdp-sol-030)
14. [SDP-SOL-040 — Interface Segregation Principle](CURRICULUM.md#sdp-sol-040)
15. [SDP-SOL-050 — Dependency Inversion Principle](CURRICULUM.md#sdp-sol-050)
16. [SDP-SOL-060 — SOLID interactions, tensions, and trade-offs](CURRICULUM.md#sdp-sol-060)
17. [SDP-SOL-070 — Pythonic SOLID with functions, modules, Protocols, and ABCs](CURRICULUM.md#sdp-sol-070)
18. [SDP-SOL-080 — SOLID critiques, overapplication, and legacy refactoring](CURRICULUM.md#sdp-sol-080)
19. [SDP-PYT-010 — Functions, closures, and callable objects as design tools](CURRICULUM.md#sdp-pyt-010)
20. [SDP-PYT-030 — Python decorator syntax versus the Decorator pattern](CURRICULUM.md#sdp-pyt-030)
21. [SDP-PYT-070 — Practical interface design with Protocols, ABCs, and duck typing](CURRICULUM.md#sdp-pyt-070)
22. [SDP-CRE-010 — Factory Method](CURRICULUM.md#sdp-cre-010)
23. [SDP-CRE-030 — Builder](CURRICULUM.md#sdp-cre-030)
24. [SDP-CRE-050 — Singleton](CURRICULUM.md#sdp-cre-050)
25. [SDP-STR-010 — Adapter](CURRICULUM.md#sdp-str-010)
26. [SDP-STR-020 — Facade](CURRICULUM.md#sdp-str-020)
27. [SDP-STR-030 — Decorator](CURRICULUM.md#sdp-str-030)
28. [SDP-STR-040 — Proxy](CURRICULUM.md#sdp-str-040)
29. [SDP-BEH-010 — Strategy](CURRICULUM.md#sdp-beh-010)
30. [SDP-BEH-020 — State](CURRICULUM.md#sdp-beh-020)
31. [SDP-BEH-030 — Observer](CURRICULUM.md#sdp-beh-030)
32. [SDP-BEH-040 — Command](CURRICULUM.md#sdp-beh-040)
33. [SDP-BEH-050 — Chain of Responsibility](CURRICULUM.md#sdp-beh-050)
34. [SDP-BEH-060 — Template Method](CURRICULUM.md#sdp-beh-060)
35. [SDP-APP-010 — Dependency Injection and the composition root](CURRICULUM.md#sdp-app-010)
36. [SDP-REF-010 — Design smells and change-force diagnosis](CURRICULUM.md#sdp-ref-010)
37. [SDP-REF-050 — Boolean flags, giant conditional dispatch, and hidden state](CURRICULUM.md#sdp-ref-050)
38. [SDP-REF-090 — Unnecessary factories, abstraction layers, and pattern soup](CURRICULUM.md#sdp-ref-090)
39. [SDP-REF-100 — Safe incremental refactoring with characterization tests](CURRICULUM.md#sdp-ref-100)
40. [SDP-INT-010 — Scenario recognition and choosing the simplest design](CURRICULUM.md#sdp-int-010)

### Practice, recall, and interview schedule

| Session | Unit steps | Required activity |
|---|---|---|
| Day 1 | Steps 1–6 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 2 | Steps 7–12 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 3 | Steps 13–18 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 4 | Steps 19–24 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 5 | Steps 25–30 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 6 | Steps 31–35 | Rapid-pass the units, complete a focused task, then compare Strategy, State, Template Method, and Command. |
| Day 7 | Steps 36–40 | Rapid-pass the units, complete the reduced project checkpoint, perform closed-book recall, and run a one-question-at-a-time mock interview. |

### Project or refactoring milestones

- [SDP-PRJ-010 — SOLID Legacy Refactoring Clinic](PROJECTS.md#sdp-prj-010) — Complete the characterization-test stage and one defended SOLID refactoring.
- [SDP-PRJ-020 — Extensible Pricing and Promotion Engine](PROJECTS.md#sdp-prj-020) — Use one staged pricing requirement as the final pattern-selection exercise.

### Completion meaning

Finishing a path does not automatically mark every unit Retained or Mastered. Each unit advances only through the evidence rules in [PROGRESS.md](PROGRESS.md).

<a id="fourteen-day-interview-preparation"></a>
## 14-day interview preparation

**Who it is for:** A senior Python candidate who wants broader GoF coverage, explicit comparison practice, and production-oriented application patterns.

**Recommended depth:** Rapid interview pass plus broader comparison, practice, and application work.

**Time assumption:** Fourteen days at approximately 2.75–4 focused hours per day. The required rapid path totals **39 h 15 min–56 h 5 min**.

**Rapid-pass unit total:** 21 h 15 min–32 h 5 min.

**Required path activities:** 18–24 h.

**Rapid-path total:** 39 h 15 min–56 h 5 min.

**Full-mastery unit total:** 564–949 h before spaced retention and milestone projects.

The 18–24 activity hours cover focused implementation and refactoring exercises, daily recall, comparison drills, one mock interview, and reduced project milestones.

**SOLID coverage:** Complete five-principle coverage: SRP, OCP, LSP, ISP, and DIP.

**Prerequisite policy:** Assumed prior knowledge: ordinary Python and basic testing. Use a prerequisite bridge for omitted advanced or rare units. Every included prerequisite appears earlier.

**Intentionally deferred:** Most reference patterns, full event sourcing, metaclasses, deep rare-pattern labs, and durable spaced-retention evidence.

**Canonical units in this path:** 64

### Recommended sequence

1. [SDP-FND-010 — Design vocabulary: principle, pattern, idiom, framework, and architecture](CURRICULUM.md#sdp-fnd-010)
2. [SDP-FND-020 — Change pressure, responsibilities, and boundaries](CURRICULUM.md#sdp-fnd-020)
3. [SDP-FND-030 — Cohesion, coupling, and dependency direction](CURRICULUM.md#sdp-fnd-030)
4. [SDP-FND-040 — Abstraction, encapsulation, information hiding, and contracts](CURRICULUM.md#sdp-fnd-040)
5. [SDP-FND-050 — Composition, delegation, and inheritance](CURRICULUM.md#sdp-fnd-050)
6. [SDP-FND-060 — Polymorphism, dynamic dispatch, and subtyping](CURRICULUM.md#sdp-fnd-060)
7. [SDP-FND-070 — Duck typing, structural typing, nominal typing, Protocols, and ABCs](CURRICULUM.md#sdp-fnd-070)
8. [SDP-FND-080 — Dependency management, test seams, and test doubles](CURRICULUM.md#sdp-fnd-080)
9. [SDP-FND-090 — Mutability, shared state, ownership, and object lifetime](CURRICULUM.md#sdp-fnd-090)
10. [SDP-FND-100 — Modules, package boundaries, and circular dependencies](CURRICULUM.md#sdp-fnd-100)
11. [SDP-FND-110 — Simplicity heuristics and collaboration laws](CURRICULUM.md#sdp-fnd-110)
12. [SDP-SOL-010 — Single Responsibility Principle](CURRICULUM.md#sdp-sol-010)
13. [SDP-SOL-020 — Open/Closed Principle](CURRICULUM.md#sdp-sol-020)
14. [SDP-SOL-030 — Liskov Substitution Principle and behavioural subtyping](CURRICULUM.md#sdp-sol-030)
15. [SDP-SOL-040 — Interface Segregation Principle](CURRICULUM.md#sdp-sol-040)
16. [SDP-SOL-050 — Dependency Inversion Principle](CURRICULUM.md#sdp-sol-050)
17. [SDP-SOL-060 — SOLID interactions, tensions, and trade-offs](CURRICULUM.md#sdp-sol-060)
18. [SDP-SOL-070 — Pythonic SOLID with functions, modules, Protocols, and ABCs](CURRICULUM.md#sdp-sol-070)
19. [SDP-SOL-080 — SOLID critiques, overapplication, and legacy refactoring](CURRICULUM.md#sdp-sol-080)
20. [SDP-PYT-010 — Functions, closures, and callable objects as design tools](CURRICULUM.md#sdp-pyt-010)
21. [SDP-PYT-020 — Dispatch tables, dictionaries of callables, and registries](CURRICULUM.md#sdp-pyt-020)
22. [SDP-PYT-030 — Python decorator syntax versus the Decorator pattern](CURRICULUM.md#sdp-pyt-030)
23. [SDP-PYT-040 — Iterators, generators, and context managers as language-supported patterns](CURRICULUM.md#sdp-pyt-040)
24. [SDP-PYT-050 — Modules, import caching, and dependency lifetimes](CURRICULUM.md#sdp-pyt-050)
25. [SDP-PYT-060 — Dataclasses, immutable value objects, and enums](CURRICULUM.md#sdp-pyt-060)
26. [SDP-PYT-070 — Practical interface design with Protocols, ABCs, and duck typing](CURRICULUM.md#sdp-pyt-070)
27. [SDP-CRE-010 — Factory Method](CURRICULUM.md#sdp-cre-010)
28. [SDP-CRE-020 — Abstract Factory](CURRICULUM.md#sdp-cre-020)
29. [SDP-CRE-030 — Builder](CURRICULUM.md#sdp-cre-030)
30. [SDP-CRE-040 — Prototype](CURRICULUM.md#sdp-cre-040)
31. [SDP-CRE-050 — Singleton](CURRICULUM.md#sdp-cre-050)
32. [SDP-STR-010 — Adapter](CURRICULUM.md#sdp-str-010)
33. [SDP-STR-020 — Facade](CURRICULUM.md#sdp-str-020)
34. [SDP-STR-030 — Decorator](CURRICULUM.md#sdp-str-030)
35. [SDP-STR-040 — Proxy](CURRICULUM.md#sdp-str-040)
36. [SDP-STR-050 — Composite](CURRICULUM.md#sdp-str-050)
37. [SDP-STR-060 — Bridge](CURRICULUM.md#sdp-str-060)
38. [SDP-BEH-010 — Strategy](CURRICULUM.md#sdp-beh-010)
39. [SDP-BEH-020 — State](CURRICULUM.md#sdp-beh-020)
40. [SDP-BEH-030 — Observer](CURRICULUM.md#sdp-beh-030)
41. [SDP-BEH-040 — Command](CURRICULUM.md#sdp-beh-040)
42. [SDP-BEH-050 — Chain of Responsibility](CURRICULUM.md#sdp-beh-050)
43. [SDP-BEH-060 — Template Method](CURRICULUM.md#sdp-beh-060)
44. [SDP-BEH-070 — Iterator](CURRICULUM.md#sdp-beh-070)
45. [SDP-BEH-080 — Mediator](CURRICULUM.md#sdp-beh-080)
46. [SDP-BEH-090 — Memento](CURRICULUM.md#sdp-beh-090)
47. [SDP-APP-010 — Dependency Injection and the composition root](CURRICULUM.md#sdp-app-010)
48. [SDP-APP-030 — Specification](CURRICULUM.md#sdp-app-030)
49. [SDP-APP-040 — Repository](CURRICULUM.md#sdp-app-040)
50. [SDP-APP-050 — Unit of Work](CURRICULUM.md#sdp-app-050)
51. [SDP-APP-060 — Service Layer](CURRICULUM.md#sdp-app-060)
52. [SDP-APP-070 — Domain Events](CURRICULUM.md#sdp-app-070)
53. [SDP-REF-010 — Design smells and change-force diagnosis](CURRICULUM.md#sdp-ref-010)
54. [SDP-REF-050 — Boolean flags, giant conditional dispatch, and hidden state](CURRICULUM.md#sdp-ref-050)
55. [SDP-REF-090 — Unnecessary factories, abstraction layers, and pattern soup](CURRICULUM.md#sdp-ref-090)
56. [SDP-REF-100 — Safe incremental refactoring with characterization tests](CURRICULUM.md#sdp-ref-100)
57. [SDP-INT-010 — Scenario recognition and choosing the simplest design](CURRICULUM.md#sdp-int-010)
58. [SDP-INT-020 — Strategy versus State versus Template Method versus Command](CURRICULUM.md#sdp-int-020)
59. [SDP-INT-030 — Adapter versus Facade versus Proxy versus Decorator](CURRICULUM.md#sdp-int-030)
60. [SDP-INT-040 — Bridge versus Adapter; Composite versus Decorator](CURRICULUM.md#sdp-int-040)
61. [SDP-INT-050 — Factory Method versus Abstract Factory versus Builder versus Prototype](CURRICULUM.md#sdp-int-050)
62. [SDP-INT-060 — Observer versus publish/subscribe versus Mediator versus Domain Events](CURRICULUM.md#sdp-int-060)
63. [SDP-INT-070 — Dependency Inversion versus Injection versus IoC versus Service Locator](CURRICULUM.md#sdp-int-070)
64. [SDP-INT-080 — Protocol versus ABC versus duck typing; inheritance versus composition versus delegation](CURRICULUM.md#sdp-int-080)

### Practice, recall, and interview schedule

| Session | Unit steps | Required activity |
|---|---|---|
| Day 1 | Steps 1–5 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 2 | Steps 6–10 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 3 | Steps 11–15 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 4 | Steps 16–20 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 5 | Steps 21–25 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 6 | Steps 26–30 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 7 | Steps 31–35 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 8 | Steps 36–40 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 9 | Steps 41–44 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 10 | Steps 45–48 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 11 | Steps 49–52 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 12 | Steps 53–56 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 13 | Steps 57–60 | Rapid-pass the comparison units and complete two scenario-selection drills with rejected alternatives. |
| Day 14 | Steps 61–64 | Finish comparison practice, perform closed-book recall, and run a one-question-at-a-time senior mock interview. |

### Project or refactoring milestones

- [SDP-PRJ-010 — SOLID Legacy Refactoring Clinic](PROJECTS.md#sdp-prj-010) — Complete the full refactoring clinic or a reduced two-stage version.
- [SDP-PRJ-020 — Extensible Pricing and Promotion Engine](PROJECTS.md#sdp-prj-020) — Implement the Strategy, Factory, and Specification stages.
- [SDP-PRJ-050 — Auditable Workflow and Command Engine](PROJECTS.md#sdp-prj-050) — Use the State-versus-Command design checkpoint for interview practice.

### Completion meaning

Finishing a path does not automatically mark every unit Retained or Mastered. Each unit advances only through the evidence rules in [PROGRESS.md](PROGRESS.md).

<a id="thirty-day-strong-foundation"></a>
## 30-day strong-foundation path

**Who it is for:** A learner who wants interview readiness plus a durable foundation in Pythonic implementation, application patterns, and safe refactoring.

**Recommended depth:** Rapid interview pass over every linked unit plus selected full-depth practice and projects.

**Time assumption:** Thirty days at 3–4 focused hours per day. The required rapid path totals **90–120 h**.

**Rapid-pass unit total:** 28 h 40 min–43 h 20 min.

**Required path activities:** 61 h 20 min–76 h 40 min.

**Rapid-path total:** 90–120 h.

**Full-mastery unit total:** 760–1,280 h before spaced retention and milestone projects.

The 61 h 20 min–76 h 40 min activity allocation covers selected full labs, refactoring checkpoints, repeated recall, comparison sessions, mock interviews, and staged project work. It does not mean all 86 units reach full mastery.

**SOLID coverage:** Complete five-principle coverage: SRP, OCP, LSP, ISP, and DIP.

**Prerequisite policy:** Assumed prior knowledge: basic professional Python. Omitted specialist units require a prerequisite bridge. Every included prerequisite appears earlier.

**Intentionally deferred:** The deepest reference patterns, full event-sourcing operations, and source-level Python mechanism investigations.

**Canonical units in this path:** 86

### Recommended sequence

1. [SDP-FND-010 — Design vocabulary: principle, pattern, idiom, framework, and architecture](CURRICULUM.md#sdp-fnd-010)
2. [SDP-FND-020 — Change pressure, responsibilities, and boundaries](CURRICULUM.md#sdp-fnd-020)
3. [SDP-FND-030 — Cohesion, coupling, and dependency direction](CURRICULUM.md#sdp-fnd-030)
4. [SDP-FND-040 — Abstraction, encapsulation, information hiding, and contracts](CURRICULUM.md#sdp-fnd-040)
5. [SDP-FND-050 — Composition, delegation, and inheritance](CURRICULUM.md#sdp-fnd-050)
6. [SDP-FND-060 — Polymorphism, dynamic dispatch, and subtyping](CURRICULUM.md#sdp-fnd-060)
7. [SDP-FND-070 — Duck typing, structural typing, nominal typing, Protocols, and ABCs](CURRICULUM.md#sdp-fnd-070)
8. [SDP-FND-080 — Dependency management, test seams, and test doubles](CURRICULUM.md#sdp-fnd-080)
9. [SDP-FND-090 — Mutability, shared state, ownership, and object lifetime](CURRICULUM.md#sdp-fnd-090)
10. [SDP-FND-100 — Modules, package boundaries, and circular dependencies](CURRICULUM.md#sdp-fnd-100)
11. [SDP-FND-110 — Simplicity heuristics and collaboration laws](CURRICULUM.md#sdp-fnd-110)
12. [SDP-SOL-010 — Single Responsibility Principle](CURRICULUM.md#sdp-sol-010)
13. [SDP-SOL-020 — Open/Closed Principle](CURRICULUM.md#sdp-sol-020)
14. [SDP-SOL-030 — Liskov Substitution Principle and behavioural subtyping](CURRICULUM.md#sdp-sol-030)
15. [SDP-SOL-040 — Interface Segregation Principle](CURRICULUM.md#sdp-sol-040)
16. [SDP-SOL-050 — Dependency Inversion Principle](CURRICULUM.md#sdp-sol-050)
17. [SDP-SOL-060 — SOLID interactions, tensions, and trade-offs](CURRICULUM.md#sdp-sol-060)
18. [SDP-SOL-070 — Pythonic SOLID with functions, modules, Protocols, and ABCs](CURRICULUM.md#sdp-sol-070)
19. [SDP-SOL-080 — SOLID critiques, overapplication, and legacy refactoring](CURRICULUM.md#sdp-sol-080)
20. [SDP-PYT-010 — Functions, closures, and callable objects as design tools](CURRICULUM.md#sdp-pyt-010)
21. [SDP-PYT-020 — Dispatch tables, dictionaries of callables, and registries](CURRICULUM.md#sdp-pyt-020)
22. [SDP-PYT-030 — Python decorator syntax versus the Decorator pattern](CURRICULUM.md#sdp-pyt-030)
23. [SDP-PYT-040 — Iterators, generators, and context managers as language-supported patterns](CURRICULUM.md#sdp-pyt-040)
24. [SDP-PYT-050 — Modules, import caching, and dependency lifetimes](CURRICULUM.md#sdp-pyt-050)
25. [SDP-PYT-060 — Dataclasses, immutable value objects, and enums](CURRICULUM.md#sdp-pyt-060)
26. [SDP-PYT-070 — Practical interface design with Protocols, ABCs, and duck typing](CURRICULUM.md#sdp-pyt-070)
27. [SDP-PYT-080 — singledispatch and open function extension](CURRICULUM.md#sdp-pyt-080)
28. [SDP-PYT-090 — Dynamic registration and plugin discovery mechanics](CURRICULUM.md#sdp-pyt-090)
29. [SDP-CRE-010 — Factory Method](CURRICULUM.md#sdp-cre-010)
30. [SDP-CRE-020 — Abstract Factory](CURRICULUM.md#sdp-cre-020)
31. [SDP-CRE-030 — Builder](CURRICULUM.md#sdp-cre-030)
32. [SDP-CRE-040 — Prototype](CURRICULUM.md#sdp-cre-040)
33. [SDP-CRE-050 — Singleton](CURRICULUM.md#sdp-cre-050)
34. [SDP-STR-010 — Adapter](CURRICULUM.md#sdp-str-010)
35. [SDP-STR-020 — Facade](CURRICULUM.md#sdp-str-020)
36. [SDP-STR-030 — Decorator](CURRICULUM.md#sdp-str-030)
37. [SDP-STR-040 — Proxy](CURRICULUM.md#sdp-str-040)
38. [SDP-STR-050 — Composite](CURRICULUM.md#sdp-str-050)
39. [SDP-STR-060 — Bridge](CURRICULUM.md#sdp-str-060)
40. [SDP-BEH-010 — Strategy](CURRICULUM.md#sdp-beh-010)
41. [SDP-BEH-020 — State](CURRICULUM.md#sdp-beh-020)
42. [SDP-BEH-030 — Observer](CURRICULUM.md#sdp-beh-030)
43. [SDP-BEH-040 — Command](CURRICULUM.md#sdp-beh-040)
44. [SDP-BEH-050 — Chain of Responsibility](CURRICULUM.md#sdp-beh-050)
45. [SDP-BEH-060 — Template Method](CURRICULUM.md#sdp-beh-060)
46. [SDP-BEH-070 — Iterator](CURRICULUM.md#sdp-beh-070)
47. [SDP-BEH-080 — Mediator](CURRICULUM.md#sdp-beh-080)
48. [SDP-BEH-090 — Memento](CURRICULUM.md#sdp-beh-090)
49. [SDP-APP-010 — Dependency Injection and the composition root](CURRICULUM.md#sdp-app-010)
50. [SDP-APP-020 — Null Object and sentinel alternatives](CURRICULUM.md#sdp-app-020)
51. [SDP-APP-030 — Specification](CURRICULUM.md#sdp-app-030)
52. [SDP-APP-040 — Repository](CURRICULUM.md#sdp-app-040)
53. [SDP-APP-050 — Unit of Work](CURRICULUM.md#sdp-app-050)
54. [SDP-APP-060 — Service Layer](CURRICULUM.md#sdp-app-060)
55. [SDP-APP-070 — Domain Events](CURRICULUM.md#sdp-app-070)
56. [SDP-APP-080 — Pipeline](CURRICULUM.md#sdp-app-080)
57. [SDP-APP-090 — Transaction Script](CURRICULUM.md#sdp-app-090)
58. [SDP-APP-100 — Active Record versus Data Mapper](CURRICULUM.md#sdp-app-100)
59. [SDP-APP-120 — MVC, MVT, and presentation boundaries](CURRICULUM.md#sdp-app-120)
60. [SDP-ARC-010 — Layered Architecture](CURRICULUM.md#sdp-arc-010)
61. [SDP-ARC-020 — Ports and Adapters / Hexagonal Architecture](CURRICULUM.md#sdp-arc-020)
62. [SDP-ARC-040 — Functional Core, Imperative Shell](CURRICULUM.md#sdp-arc-040)
63. [SDP-ARC-050 — Event-driven application boundaries](CURRICULUM.md#sdp-arc-050)
64. [SDP-ARC-080 — Architectural boundaries and evolutionary design](CURRICULUM.md#sdp-arc-080)
65. [SDP-RAR-030 — Lazy Initialization](CURRICULUM.md#sdp-rar-030)
66. [SDP-RAR-050 — Service Locator](CURRICULUM.md#sdp-rar-050)
67. [SDP-RAR-080 — Circuit Breaker as a resilience pattern](CURRICULUM.md#sdp-rar-080)
68. [SDP-REF-010 — Design smells and change-force diagnosis](CURRICULUM.md#sdp-ref-010)
69. [SDP-REF-020 — God Object, Spaghetti Code, and Shotgun Surgery](CURRICULUM.md#sdp-ref-020)
70. [SDP-REF-030 — Feature Envy, Primitive Obsession, and weak domain models](CURRICULUM.md#sdp-ref-030)
71. [SDP-REF-040 — Excessive inheritance and fragile hierarchies](CURRICULUM.md#sdp-ref-040)
72. [SDP-REF-050 — Boolean flags, giant conditional dispatch, and hidden state](CURRICULUM.md#sdp-ref-050)
73. [SDP-REF-060 — Singleton and Service Locator misuse](CURRICULUM.md#sdp-ref-060)
74. [SDP-REF-070 — Circular dependencies and temporal coupling](CURRICULUM.md#sdp-ref-070)
75. [SDP-REF-080 — Mock-heavy tests and meaningless interfaces](CURRICULUM.md#sdp-ref-080)
76. [SDP-REF-090 — Unnecessary factories, abstraction layers, and pattern soup](CURRICULUM.md#sdp-ref-090)
77. [SDP-REF-100 — Safe incremental refactoring with characterization tests](CURRICULUM.md#sdp-ref-100)
78. [SDP-INT-010 — Scenario recognition and choosing the simplest design](CURRICULUM.md#sdp-int-010)
79. [SDP-INT-020 — Strategy versus State versus Template Method versus Command](CURRICULUM.md#sdp-int-020)
80. [SDP-INT-030 — Adapter versus Facade versus Proxy versus Decorator](CURRICULUM.md#sdp-int-030)
81. [SDP-INT-040 — Bridge versus Adapter; Composite versus Decorator](CURRICULUM.md#sdp-int-040)
82. [SDP-INT-050 — Factory Method versus Abstract Factory versus Builder versus Prototype](CURRICULUM.md#sdp-int-050)
83. [SDP-INT-060 — Observer versus publish/subscribe versus Mediator versus Domain Events](CURRICULUM.md#sdp-int-060)
84. [SDP-INT-070 — Dependency Inversion versus Injection versus IoC versus Service Locator](CURRICULUM.md#sdp-int-070)
85. [SDP-INT-080 — Protocol versus ABC versus duck typing; inheritance versus composition versus delegation](CURRICULUM.md#sdp-int-080)
86. [SDP-INT-090 — Repository versus DAO and Unit of Work; object versus architectural boundaries](CURRICULUM.md#sdp-int-090)

### Practice, recall, and interview schedule

| Session | Unit steps | Required activity |
|---|---|---|
| Day 1 | Steps 1–3 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 2 | Steps 4–6 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 3 | Steps 7–9 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 4 | Steps 10–12 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 5 | Steps 13–15 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 6 | Steps 16–18 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 7 | Steps 19–21 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 8 | Steps 22–24 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 9 | Steps 25–27 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 10 | Steps 28–30 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 11 | Steps 31–33 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 12 | Steps 34–36 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 13 | Steps 37–39 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 14 | Steps 40–42 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 15 | Steps 43–45 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 16 | Steps 46–48 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 17 | Steps 49–51 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 18 | Steps 52–54 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 19 | Steps 55–57 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 20 | Steps 58–60 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 21 | Steps 61–63 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 22 | Steps 64–66 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 23 | Steps 67–69 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 24 | Steps 70–72 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 25 | Steps 73–75 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 26 | Steps 76–78 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 27 | Steps 79–80 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 28 | Steps 81–82 | Study the linked units, complete one prediction/refactoring task, then perform 15–20 minutes of closed-book recall. |
| Day 29 | Steps 83–84 | Complete comparison and design-defence drills, then review the selected project decisions. |
| Day 30 | Steps 85–86 | Complete final synthesis, closed-book recall, and a one-question-at-a-time senior mock interview. |

### Project or refactoring milestones

- [SDP-PRJ-010 — SOLID Legacy Refactoring Clinic](PROJECTS.md#sdp-prj-010) — Complete and defend the refactoring sequence.
- [SDP-PRJ-020 — Extensible Pricing and Promotion Engine](PROJECTS.md#sdp-prj-020) — Complete the extensible pricing engine.
- [SDP-PRJ-030 — Multi-provider Notification Gateway](PROJECTS.md#sdp-prj-030) — Implement one provider adapter plus fallback and observability.
- [SDP-PRJ-050 — Auditable Workflow and Command Engine](PROJECTS.md#sdp-prj-050) — Complete the workflow transition and audit stages.

### Completion meaning

Finishing a path does not automatically mark every unit Retained or Mastered. Each unit advances only through the evidence rules in [PROGRESS.md](PROGRESS.md).

<a id="complete-solid-pattern-mastery"></a>
## Complete SOLID and design-pattern mastery

**Who it is for:** A long-term learner who wants every canonical unit, all 23 GoF patterns, Pythonic alternatives, architecture, rare patterns, and evidence-backed retention.

**Time assumption:** Approximately 903–1,520 hours for first understanding plus practice, before long-term spaced review and project transfer.

**Prerequisite policy:** No internal prerequisite is intentionally omitted. The canonical curriculum order is prerequisite-safe.

**Intentionally deferred:** Nothing in the canonical catalog; external distributed-systems depth remains in a separate learning system.

**Canonical units in this path:** 100

### Recommended sequence

1. [SDP-FND-010 — Design vocabulary: principle, pattern, idiom, framework, and architecture](CURRICULUM.md#sdp-fnd-010)
2. [SDP-FND-020 — Change pressure, responsibilities, and boundaries](CURRICULUM.md#sdp-fnd-020)
3. [SDP-FND-030 — Cohesion, coupling, and dependency direction](CURRICULUM.md#sdp-fnd-030)
4. [SDP-FND-040 — Abstraction, encapsulation, information hiding, and contracts](CURRICULUM.md#sdp-fnd-040)
5. [SDP-FND-050 — Composition, delegation, and inheritance](CURRICULUM.md#sdp-fnd-050)
6. [SDP-FND-060 — Polymorphism, dynamic dispatch, and subtyping](CURRICULUM.md#sdp-fnd-060)
7. [SDP-FND-070 — Duck typing, structural typing, nominal typing, Protocols, and ABCs](CURRICULUM.md#sdp-fnd-070)
8. [SDP-FND-080 — Dependency management, test seams, and test doubles](CURRICULUM.md#sdp-fnd-080)
9. [SDP-FND-090 — Mutability, shared state, ownership, and object lifetime](CURRICULUM.md#sdp-fnd-090)
10. [SDP-FND-100 — Modules, package boundaries, and circular dependencies](CURRICULUM.md#sdp-fnd-100)
11. [SDP-FND-110 — Simplicity heuristics and collaboration laws](CURRICULUM.md#sdp-fnd-110)
12. [SDP-SOL-010 — Single Responsibility Principle](CURRICULUM.md#sdp-sol-010)
13. [SDP-SOL-020 — Open/Closed Principle](CURRICULUM.md#sdp-sol-020)
14. [SDP-SOL-030 — Liskov Substitution Principle and behavioural subtyping](CURRICULUM.md#sdp-sol-030)
15. [SDP-SOL-040 — Interface Segregation Principle](CURRICULUM.md#sdp-sol-040)
16. [SDP-SOL-050 — Dependency Inversion Principle](CURRICULUM.md#sdp-sol-050)
17. [SDP-SOL-060 — SOLID interactions, tensions, and trade-offs](CURRICULUM.md#sdp-sol-060)
18. [SDP-SOL-070 — Pythonic SOLID with functions, modules, Protocols, and ABCs](CURRICULUM.md#sdp-sol-070)
19. [SDP-SOL-080 — SOLID critiques, overapplication, and legacy refactoring](CURRICULUM.md#sdp-sol-080)
20. [SDP-PYT-010 — Functions, closures, and callable objects as design tools](CURRICULUM.md#sdp-pyt-010)
21. [SDP-PYT-020 — Dispatch tables, dictionaries of callables, and registries](CURRICULUM.md#sdp-pyt-020)
22. [SDP-PYT-030 — Python decorator syntax versus the Decorator pattern](CURRICULUM.md#sdp-pyt-030)
23. [SDP-PYT-040 — Iterators, generators, and context managers as language-supported patterns](CURRICULUM.md#sdp-pyt-040)
24. [SDP-PYT-050 — Modules, import caching, and dependency lifetimes](CURRICULUM.md#sdp-pyt-050)
25. [SDP-PYT-060 — Dataclasses, immutable value objects, and enums](CURRICULUM.md#sdp-pyt-060)
26. [SDP-PYT-070 — Practical interface design with Protocols, ABCs, and duck typing](CURRICULUM.md#sdp-pyt-070)
27. [SDP-PYT-080 — singledispatch and open function extension](CURRICULUM.md#sdp-pyt-080)
28. [SDP-PYT-090 — Dynamic registration and plugin discovery mechanics](CURRICULUM.md#sdp-pyt-090)
29. [SDP-PYT-100 — Descriptors, class hooks, and metaclasses only when justified](CURRICULUM.md#sdp-pyt-100)
30. [SDP-CRE-010 — Factory Method](CURRICULUM.md#sdp-cre-010)
31. [SDP-CRE-020 — Abstract Factory](CURRICULUM.md#sdp-cre-020)
32. [SDP-CRE-030 — Builder](CURRICULUM.md#sdp-cre-030)
33. [SDP-CRE-040 — Prototype](CURRICULUM.md#sdp-cre-040)
34. [SDP-CRE-050 — Singleton](CURRICULUM.md#sdp-cre-050)
35. [SDP-STR-010 — Adapter](CURRICULUM.md#sdp-str-010)
36. [SDP-STR-020 — Facade](CURRICULUM.md#sdp-str-020)
37. [SDP-STR-030 — Decorator](CURRICULUM.md#sdp-str-030)
38. [SDP-STR-040 — Proxy](CURRICULUM.md#sdp-str-040)
39. [SDP-STR-050 — Composite](CURRICULUM.md#sdp-str-050)
40. [SDP-STR-060 — Bridge](CURRICULUM.md#sdp-str-060)
41. [SDP-STR-070 — Flyweight](CURRICULUM.md#sdp-str-070)
42. [SDP-BEH-010 — Strategy](CURRICULUM.md#sdp-beh-010)
43. [SDP-BEH-020 — State](CURRICULUM.md#sdp-beh-020)
44. [SDP-BEH-030 — Observer](CURRICULUM.md#sdp-beh-030)
45. [SDP-BEH-040 — Command](CURRICULUM.md#sdp-beh-040)
46. [SDP-BEH-050 — Chain of Responsibility](CURRICULUM.md#sdp-beh-050)
47. [SDP-BEH-060 — Template Method](CURRICULUM.md#sdp-beh-060)
48. [SDP-BEH-070 — Iterator](CURRICULUM.md#sdp-beh-070)
49. [SDP-BEH-080 — Mediator](CURRICULUM.md#sdp-beh-080)
50. [SDP-BEH-090 — Memento](CURRICULUM.md#sdp-beh-090)
51. [SDP-BEH-100 — Visitor](CURRICULUM.md#sdp-beh-100)
52. [SDP-BEH-110 — Interpreter](CURRICULUM.md#sdp-beh-110)
53. [SDP-APP-010 — Dependency Injection and the composition root](CURRICULUM.md#sdp-app-010)
54. [SDP-APP-020 — Null Object and sentinel alternatives](CURRICULUM.md#sdp-app-020)
55. [SDP-APP-030 — Specification](CURRICULUM.md#sdp-app-030)
56. [SDP-APP-040 — Repository](CURRICULUM.md#sdp-app-040)
57. [SDP-APP-050 — Unit of Work](CURRICULUM.md#sdp-app-050)
58. [SDP-APP-060 — Service Layer](CURRICULUM.md#sdp-app-060)
59. [SDP-APP-070 — Domain Events](CURRICULUM.md#sdp-app-070)
60. [SDP-APP-080 — Pipeline](CURRICULUM.md#sdp-app-080)
61. [SDP-APP-090 — Transaction Script](CURRICULUM.md#sdp-app-090)
62. [SDP-APP-100 — Active Record versus Data Mapper](CURRICULUM.md#sdp-app-100)
63. [SDP-APP-110 — Identity Map and object identity](CURRICULUM.md#sdp-app-110)
64. [SDP-APP-120 — MVC, MVT, and presentation boundaries](CURRICULUM.md#sdp-app-120)
65. [SDP-ARC-010 — Layered Architecture](CURRICULUM.md#sdp-arc-010)
66. [SDP-ARC-020 — Ports and Adapters / Hexagonal Architecture](CURRICULUM.md#sdp-arc-020)
67. [SDP-ARC-030 — Clean Architecture](CURRICULUM.md#sdp-arc-030)
68. [SDP-ARC-040 — Functional Core, Imperative Shell](CURRICULUM.md#sdp-arc-040)
69. [SDP-ARC-050 — Event-driven application boundaries](CURRICULUM.md#sdp-arc-050)
70. [SDP-ARC-060 — CQRS at application scale](CURRICULUM.md#sdp-arc-060)
71. [SDP-ARC-070 — Event Sourcing](CURRICULUM.md#sdp-arc-070)
72. [SDP-ARC-080 — Architectural boundaries and evolutionary design](CURRICULUM.md#sdp-arc-080)
73. [SDP-RAR-010 — Object Pool](CURRICULUM.md#sdp-rar-010)
74. [SDP-RAR-020 — Monostate / Borg](CURRICULUM.md#sdp-rar-020)
75. [SDP-RAR-030 — Lazy Initialization](CURRICULUM.md#sdp-rar-030)
76. [SDP-RAR-040 — Blackboard](CURRICULUM.md#sdp-rar-040)
77. [SDP-RAR-050 — Service Locator](CURRICULUM.md#sdp-rar-050)
78. [SDP-RAR-060 — Active Object](CURRICULUM.md#sdp-rar-060)
79. [SDP-RAR-070 — Saga as a distributed workflow pattern](CURRICULUM.md#sdp-rar-070)
80. [SDP-RAR-080 — Circuit Breaker as a resilience pattern](CURRICULUM.md#sdp-rar-080)
81. [SDP-REF-010 — Design smells and change-force diagnosis](CURRICULUM.md#sdp-ref-010)
82. [SDP-REF-020 — God Object, Spaghetti Code, and Shotgun Surgery](CURRICULUM.md#sdp-ref-020)
83. [SDP-REF-030 — Feature Envy, Primitive Obsession, and weak domain models](CURRICULUM.md#sdp-ref-030)
84. [SDP-REF-040 — Excessive inheritance and fragile hierarchies](CURRICULUM.md#sdp-ref-040)
85. [SDP-REF-050 — Boolean flags, giant conditional dispatch, and hidden state](CURRICULUM.md#sdp-ref-050)
86. [SDP-REF-060 — Singleton and Service Locator misuse](CURRICULUM.md#sdp-ref-060)
87. [SDP-REF-070 — Circular dependencies and temporal coupling](CURRICULUM.md#sdp-ref-070)
88. [SDP-REF-080 — Mock-heavy tests and meaningless interfaces](CURRICULUM.md#sdp-ref-080)
89. [SDP-REF-090 — Unnecessary factories, abstraction layers, and pattern soup](CURRICULUM.md#sdp-ref-090)
90. [SDP-REF-100 — Safe incremental refactoring with characterization tests](CURRICULUM.md#sdp-ref-100)
91. [SDP-INT-010 — Scenario recognition and choosing the simplest design](CURRICULUM.md#sdp-int-010)
92. [SDP-INT-020 — Strategy versus State versus Template Method versus Command](CURRICULUM.md#sdp-int-020)
93. [SDP-INT-030 — Adapter versus Facade versus Proxy versus Decorator](CURRICULUM.md#sdp-int-030)
94. [SDP-INT-040 — Bridge versus Adapter; Composite versus Decorator](CURRICULUM.md#sdp-int-040)
95. [SDP-INT-050 — Factory Method versus Abstract Factory versus Builder versus Prototype](CURRICULUM.md#sdp-int-050)
96. [SDP-INT-060 — Observer versus publish/subscribe versus Mediator versus Domain Events](CURRICULUM.md#sdp-int-060)
97. [SDP-INT-070 — Dependency Inversion versus Injection versus IoC versus Service Locator](CURRICULUM.md#sdp-int-070)
98. [SDP-INT-080 — Protocol versus ABC versus duck typing; inheritance versus composition versus delegation](CURRICULUM.md#sdp-int-080)
99. [SDP-INT-090 — Repository versus DAO and Unit of Work; object versus architectural boundaries](CURRICULUM.md#sdp-int-090)
100. [SDP-INT-100 — Senior pattern combinations, code review, and mock interview synthesis](CURRICULUM.md#sdp-int-100)

### Practice, recall, and interview schedule

| Session | Unit steps | Required activity |
|---|---|---|
| Every study block | Next 1–3 steps | Physical Notebook Core, one code/refactoring task, and one rejected alternative |
| Every third block | Previous steps | Closed-book recall and one comparison from a new scenario |
| Every domain boundary | Completed domain steps | Code review or refactoring drill |
| Final checkpoint | Entire path | One-question-at-a-time senior mock interview and weakness log |

### Project or refactoring milestones

- [SDP-PRJ-010 — SOLID Legacy Refactoring Clinic](PROJECTS.md#sdp-prj-010) — Complete at the indicated point in the path and link project evidence without automatically changing unit states.
- [SDP-PRJ-020 — Extensible Pricing and Promotion Engine](PROJECTS.md#sdp-prj-020) — Complete at the indicated point in the path and link project evidence without automatically changing unit states.
- [SDP-PRJ-030 — Multi-provider Notification Gateway](PROJECTS.md#sdp-prj-030) — Complete at the indicated point in the path and link project evidence without automatically changing unit states.
- [SDP-PRJ-040 — Typed Rule and Plugin Engine](PROJECTS.md#sdp-prj-040) — Complete at the indicated point in the path and link project evidence without automatically changing unit states.
- [SDP-PRJ-050 — Auditable Workflow and Command Engine](PROJECTS.md#sdp-prj-050) — Complete at the indicated point in the path and link project evidence without automatically changing unit states.
- [SDP-PRJ-060 — Python Backend Architecture Lab](PROJECTS.md#sdp-prj-060) — Complete at the indicated point in the path and link project evidence without automatically changing unit states.

### Completion meaning

Finishing a path does not automatically mark every unit Retained or Mastered. Each unit advances only through the evidence rules in [PROGRESS.md](PROGRESS.md).

<a id="python-backend-application-architecture"></a>
## Python backend and application architecture

**Who it is for:** A backend engineer who wants patterns that improve APIs, persistence boundaries, integrations, application use cases, transactions, and testability.

**Time assumption:** Approximately 180–300 hours including two substantial projects.

**Prerequisite policy:** Assumed prior knowledge: working Python and HTTP/database basics. Omitted GoF or rare prerequisites use a bridge. Every included prerequisite appears earlier.

**Intentionally deferred:** UI-heavy patterns, most reference patterns, Visitor, Interpreter, Blackboard, and source-level Python internals.

**Canonical units in this path:** 71

### Recommended sequence

1. [SDP-FND-010 — Design vocabulary: principle, pattern, idiom, framework, and architecture](CURRICULUM.md#sdp-fnd-010)
2. [SDP-FND-020 — Change pressure, responsibilities, and boundaries](CURRICULUM.md#sdp-fnd-020)
3. [SDP-FND-030 — Cohesion, coupling, and dependency direction](CURRICULUM.md#sdp-fnd-030)
4. [SDP-FND-040 — Abstraction, encapsulation, information hiding, and contracts](CURRICULUM.md#sdp-fnd-040)
5. [SDP-FND-050 — Composition, delegation, and inheritance](CURRICULUM.md#sdp-fnd-050)
6. [SDP-FND-060 — Polymorphism, dynamic dispatch, and subtyping](CURRICULUM.md#sdp-fnd-060)
7. [SDP-FND-070 — Duck typing, structural typing, nominal typing, Protocols, and ABCs](CURRICULUM.md#sdp-fnd-070)
8. [SDP-FND-080 — Dependency management, test seams, and test doubles](CURRICULUM.md#sdp-fnd-080)
9. [SDP-FND-090 — Mutability, shared state, ownership, and object lifetime](CURRICULUM.md#sdp-fnd-090)
10. [SDP-FND-100 — Modules, package boundaries, and circular dependencies](CURRICULUM.md#sdp-fnd-100)
11. [SDP-FND-110 — Simplicity heuristics and collaboration laws](CURRICULUM.md#sdp-fnd-110)
12. [SDP-SOL-010 — Single Responsibility Principle](CURRICULUM.md#sdp-sol-010)
13. [SDP-SOL-020 — Open/Closed Principle](CURRICULUM.md#sdp-sol-020)
14. [SDP-SOL-030 — Liskov Substitution Principle and behavioural subtyping](CURRICULUM.md#sdp-sol-030)
15. [SDP-SOL-040 — Interface Segregation Principle](CURRICULUM.md#sdp-sol-040)
16. [SDP-SOL-050 — Dependency Inversion Principle](CURRICULUM.md#sdp-sol-050)
17. [SDP-SOL-060 — SOLID interactions, tensions, and trade-offs](CURRICULUM.md#sdp-sol-060)
18. [SDP-SOL-070 — Pythonic SOLID with functions, modules, Protocols, and ABCs](CURRICULUM.md#sdp-sol-070)
19. [SDP-SOL-080 — SOLID critiques, overapplication, and legacy refactoring](CURRICULUM.md#sdp-sol-080)
20. [SDP-PYT-010 — Functions, closures, and callable objects as design tools](CURRICULUM.md#sdp-pyt-010)
21. [SDP-PYT-020 — Dispatch tables, dictionaries of callables, and registries](CURRICULUM.md#sdp-pyt-020)
22. [SDP-PYT-030 — Python decorator syntax versus the Decorator pattern](CURRICULUM.md#sdp-pyt-030)
23. [SDP-PYT-040 — Iterators, generators, and context managers as language-supported patterns](CURRICULUM.md#sdp-pyt-040)
24. [SDP-PYT-050 — Modules, import caching, and dependency lifetimes](CURRICULUM.md#sdp-pyt-050)
25. [SDP-PYT-060 — Dataclasses, immutable value objects, and enums](CURRICULUM.md#sdp-pyt-060)
26. [SDP-PYT-070 — Practical interface design with Protocols, ABCs, and duck typing](CURRICULUM.md#sdp-pyt-070)
27. [SDP-PYT-090 — Dynamic registration and plugin discovery mechanics](CURRICULUM.md#sdp-pyt-090)
28. [SDP-CRE-010 — Factory Method](CURRICULUM.md#sdp-cre-010)
29. [SDP-CRE-030 — Builder](CURRICULUM.md#sdp-cre-030)
30. [SDP-CRE-050 — Singleton](CURRICULUM.md#sdp-cre-050)
31. [SDP-STR-010 — Adapter](CURRICULUM.md#sdp-str-010)
32. [SDP-STR-020 — Facade](CURRICULUM.md#sdp-str-020)
33. [SDP-STR-030 — Decorator](CURRICULUM.md#sdp-str-030)
34. [SDP-STR-040 — Proxy](CURRICULUM.md#sdp-str-040)
35. [SDP-BEH-010 — Strategy](CURRICULUM.md#sdp-beh-010)
36. [SDP-BEH-020 — State](CURRICULUM.md#sdp-beh-020)
37. [SDP-BEH-030 — Observer](CURRICULUM.md#sdp-beh-030)
38. [SDP-BEH-040 — Command](CURRICULUM.md#sdp-beh-040)
39. [SDP-BEH-050 — Chain of Responsibility](CURRICULUM.md#sdp-beh-050)
40. [SDP-BEH-060 — Template Method](CURRICULUM.md#sdp-beh-060)
41. [SDP-APP-010 — Dependency Injection and the composition root](CURRICULUM.md#sdp-app-010)
42. [SDP-APP-020 — Null Object and sentinel alternatives](CURRICULUM.md#sdp-app-020)
43. [SDP-APP-030 — Specification](CURRICULUM.md#sdp-app-030)
44. [SDP-APP-040 — Repository](CURRICULUM.md#sdp-app-040)
45. [SDP-APP-050 — Unit of Work](CURRICULUM.md#sdp-app-050)
46. [SDP-APP-060 — Service Layer](CURRICULUM.md#sdp-app-060)
47. [SDP-APP-070 — Domain Events](CURRICULUM.md#sdp-app-070)
48. [SDP-APP-080 — Pipeline](CURRICULUM.md#sdp-app-080)
49. [SDP-APP-090 — Transaction Script](CURRICULUM.md#sdp-app-090)
50. [SDP-APP-100 — Active Record versus Data Mapper](CURRICULUM.md#sdp-app-100)
51. [SDP-APP-110 — Identity Map and object identity](CURRICULUM.md#sdp-app-110)
52. [SDP-APP-120 — MVC, MVT, and presentation boundaries](CURRICULUM.md#sdp-app-120)
53. [SDP-ARC-010 — Layered Architecture](CURRICULUM.md#sdp-arc-010)
54. [SDP-ARC-020 — Ports and Adapters / Hexagonal Architecture](CURRICULUM.md#sdp-arc-020)
55. [SDP-ARC-030 — Clean Architecture](CURRICULUM.md#sdp-arc-030)
56. [SDP-ARC-040 — Functional Core, Imperative Shell](CURRICULUM.md#sdp-arc-040)
57. [SDP-ARC-050 — Event-driven application boundaries](CURRICULUM.md#sdp-arc-050)
58. [SDP-ARC-060 — CQRS at application scale](CURRICULUM.md#sdp-arc-060)
59. [SDP-ARC-080 — Architectural boundaries and evolutionary design](CURRICULUM.md#sdp-arc-080)
60. [SDP-RAR-030 — Lazy Initialization](CURRICULUM.md#sdp-rar-030)
61. [SDP-RAR-050 — Service Locator](CURRICULUM.md#sdp-rar-050)
62. [SDP-RAR-080 — Circuit Breaker as a resilience pattern](CURRICULUM.md#sdp-rar-080)
63. [SDP-REF-010 — Design smells and change-force diagnosis](CURRICULUM.md#sdp-ref-010)
64. [SDP-REF-060 — Singleton and Service Locator misuse](CURRICULUM.md#sdp-ref-060)
65. [SDP-REF-070 — Circular dependencies and temporal coupling](CURRICULUM.md#sdp-ref-070)
66. [SDP-REF-080 — Mock-heavy tests and meaningless interfaces](CURRICULUM.md#sdp-ref-080)
67. [SDP-REF-100 — Safe incremental refactoring with characterization tests](CURRICULUM.md#sdp-ref-100)
68. [SDP-INT-060 — Observer versus publish/subscribe versus Mediator versus Domain Events](CURRICULUM.md#sdp-int-060)
69. [SDP-INT-070 — Dependency Inversion versus Injection versus IoC versus Service Locator](CURRICULUM.md#sdp-int-070)
70. [SDP-INT-080 — Protocol versus ABC versus duck typing; inheritance versus composition versus delegation](CURRICULUM.md#sdp-int-080)
71. [SDP-INT-090 — Repository versus DAO and Unit of Work; object versus architectural boundaries](CURRICULUM.md#sdp-int-090)

### Practice, recall, and interview schedule

| Session | Unit steps | Required activity |
|---|---|---|
| Every study block | Next 1–3 steps | Physical Notebook Core, one code/refactoring task, and one rejected alternative |
| Every third block | Previous steps | Closed-book recall and one comparison from a new scenario |
| Every domain boundary | Completed domain steps | Code review or refactoring drill |
| Final checkpoint | Entire path | One-question-at-a-time senior mock interview and weakness log |

### Project or refactoring milestones

- [SDP-PRJ-030 — Multi-provider Notification Gateway](PROJECTS.md#sdp-prj-030) — Complete the provider gateway and defend the integration boundary.
- [SDP-PRJ-040 — Typed Rule and Plugin Engine](PROJECTS.md#sdp-prj-040) — Complete plugin contracts and discovery.
- [SDP-PRJ-060 — Python Backend Architecture Lab](PROJECTS.md#sdp-prj-060) — Complete the backend architecture lab and senior walkthrough.

### Completion meaning

Finishing a path does not automatically mark every unit Retained or Mastered. Each unit advances only through the evidence rules in [PROGRESS.md](PROGRESS.md).

<a id="refactoring-pythonic-design"></a>
## Refactoring and Pythonic design

**Who it is for:** A Python engineer who recognizes overengineered or tangled code and wants to improve it safely without memorizing pattern catalogs.

**Time assumption:** Approximately 120–210 hours including the legacy clinic.

**Prerequisite policy:** Assumed prior knowledge: Python classes, functions, and pytest. Use a prerequisite bridge for omitted specialized patterns. Every included prerequisite appears earlier.

**Intentionally deferred:** Complete GoF coverage, distributed patterns, event sourcing, and architecture catalogs not needed for the selected refactorings.

**Canonical units in this path:** 44

### Recommended sequence

1. [SDP-FND-010 — Design vocabulary: principle, pattern, idiom, framework, and architecture](CURRICULUM.md#sdp-fnd-010)
2. [SDP-FND-020 — Change pressure, responsibilities, and boundaries](CURRICULUM.md#sdp-fnd-020)
3. [SDP-FND-030 — Cohesion, coupling, and dependency direction](CURRICULUM.md#sdp-fnd-030)
4. [SDP-FND-040 — Abstraction, encapsulation, information hiding, and contracts](CURRICULUM.md#sdp-fnd-040)
5. [SDP-FND-050 — Composition, delegation, and inheritance](CURRICULUM.md#sdp-fnd-050)
6. [SDP-FND-060 — Polymorphism, dynamic dispatch, and subtyping](CURRICULUM.md#sdp-fnd-060)
7. [SDP-FND-070 — Duck typing, structural typing, nominal typing, Protocols, and ABCs](CURRICULUM.md#sdp-fnd-070)
8. [SDP-FND-080 — Dependency management, test seams, and test doubles](CURRICULUM.md#sdp-fnd-080)
9. [SDP-FND-090 — Mutability, shared state, ownership, and object lifetime](CURRICULUM.md#sdp-fnd-090)
10. [SDP-FND-100 — Modules, package boundaries, and circular dependencies](CURRICULUM.md#sdp-fnd-100)
11. [SDP-FND-110 — Simplicity heuristics and collaboration laws](CURRICULUM.md#sdp-fnd-110)
12. [SDP-SOL-010 — Single Responsibility Principle](CURRICULUM.md#sdp-sol-010)
13. [SDP-SOL-020 — Open/Closed Principle](CURRICULUM.md#sdp-sol-020)
14. [SDP-SOL-030 — Liskov Substitution Principle and behavioural subtyping](CURRICULUM.md#sdp-sol-030)
15. [SDP-SOL-040 — Interface Segregation Principle](CURRICULUM.md#sdp-sol-040)
16. [SDP-SOL-050 — Dependency Inversion Principle](CURRICULUM.md#sdp-sol-050)
17. [SDP-SOL-060 — SOLID interactions, tensions, and trade-offs](CURRICULUM.md#sdp-sol-060)
18. [SDP-SOL-070 — Pythonic SOLID with functions, modules, Protocols, and ABCs](CURRICULUM.md#sdp-sol-070)
19. [SDP-SOL-080 — SOLID critiques, overapplication, and legacy refactoring](CURRICULUM.md#sdp-sol-080)
20. [SDP-PYT-010 — Functions, closures, and callable objects as design tools](CURRICULUM.md#sdp-pyt-010)
21. [SDP-PYT-020 — Dispatch tables, dictionaries of callables, and registries](CURRICULUM.md#sdp-pyt-020)
22. [SDP-PYT-030 — Python decorator syntax versus the Decorator pattern](CURRICULUM.md#sdp-pyt-030)
23. [SDP-PYT-050 — Modules, import caching, and dependency lifetimes](CURRICULUM.md#sdp-pyt-050)
24. [SDP-PYT-070 — Practical interface design with Protocols, ABCs, and duck typing](CURRICULUM.md#sdp-pyt-070)
25. [SDP-CRE-050 — Singleton](CURRICULUM.md#sdp-cre-050)
26. [SDP-BEH-010 — Strategy](CURRICULUM.md#sdp-beh-010)
27. [SDP-BEH-020 — State](CURRICULUM.md#sdp-beh-020)
28. [SDP-BEH-040 — Command](CURRICULUM.md#sdp-beh-040)
29. [SDP-APP-010 — Dependency Injection and the composition root](CURRICULUM.md#sdp-app-010)
30. [SDP-RAR-050 — Service Locator](CURRICULUM.md#sdp-rar-050)
31. [SDP-REF-010 — Design smells and change-force diagnosis](CURRICULUM.md#sdp-ref-010)
32. [SDP-REF-020 — God Object, Spaghetti Code, and Shotgun Surgery](CURRICULUM.md#sdp-ref-020)
33. [SDP-REF-030 — Feature Envy, Primitive Obsession, and weak domain models](CURRICULUM.md#sdp-ref-030)
34. [SDP-REF-040 — Excessive inheritance and fragile hierarchies](CURRICULUM.md#sdp-ref-040)
35. [SDP-REF-050 — Boolean flags, giant conditional dispatch, and hidden state](CURRICULUM.md#sdp-ref-050)
36. [SDP-REF-060 — Singleton and Service Locator misuse](CURRICULUM.md#sdp-ref-060)
37. [SDP-REF-070 — Circular dependencies and temporal coupling](CURRICULUM.md#sdp-ref-070)
38. [SDP-REF-080 — Mock-heavy tests and meaningless interfaces](CURRICULUM.md#sdp-ref-080)
39. [SDP-REF-090 — Unnecessary factories, abstraction layers, and pattern soup](CURRICULUM.md#sdp-ref-090)
40. [SDP-REF-100 — Safe incremental refactoring with characterization tests](CURRICULUM.md#sdp-ref-100)
41. [SDP-INT-010 — Scenario recognition and choosing the simplest design](CURRICULUM.md#sdp-int-010)
42. [SDP-INT-020 — Strategy versus State versus Template Method versus Command](CURRICULUM.md#sdp-int-020)
43. [SDP-INT-070 — Dependency Inversion versus Injection versus IoC versus Service Locator](CURRICULUM.md#sdp-int-070)
44. [SDP-INT-080 — Protocol versus ABC versus duck typing; inheritance versus composition versus delegation](CURRICULUM.md#sdp-int-080)

### Practice, recall, and interview schedule

| Session | Unit steps | Required activity |
|---|---|---|
| Every study block | Next 1–3 steps | Physical Notebook Core, one code/refactoring task, and one rejected alternative |
| Every third block | Previous steps | Closed-book recall and one comparison from a new scenario |
| Every domain boundary | Completed domain steps | Code review or refactoring drill |
| Final checkpoint | Entire path | One-question-at-a-time senior mock interview and weakness log |

### Project or refactoring milestones

- [SDP-PRJ-010 — SOLID Legacy Refactoring Clinic](PROJECTS.md#sdp-prj-010) — Use as the central project; complete every characterization, refactoring, and design-defence checkpoint.
- [SDP-PRJ-020 — Extensible Pricing and Promotion Engine](PROJECTS.md#sdp-prj-020) — Use one change-pressure stage to verify that the new design remains extensible.

### Completion meaning

Finishing a path does not automatically mark every unit Retained or Mastered. Each unit advances only through the evidence rules in [PROGRESS.md](PROGRESS.md).

<a id="senior-comparison-design-practice"></a>
## Senior interview comparison and design practice

**Who it is for:** A candidate who already knows definitions and needs scenario selection, comparison precision, code review, changing requirements, and senior critique.

**Time assumption:** Approximately 140–230 hours including repeated interview rounds and one integration project.

**Prerequisite policy:** Assumed prior knowledge: working Python plus basic SOLID and common pattern definitions. Omitted units require a bridge. Every included prerequisite appears earlier.

**Intentionally deferred:** Exhaustive rare-pattern implementation and unrelated framework or distributed-system detail.

**Canonical units in this path:** 60

### Recommended sequence

1. [SDP-FND-010 — Design vocabulary: principle, pattern, idiom, framework, and architecture](CURRICULUM.md#sdp-fnd-010)
2. [SDP-FND-020 — Change pressure, responsibilities, and boundaries](CURRICULUM.md#sdp-fnd-020)
3. [SDP-FND-030 — Cohesion, coupling, and dependency direction](CURRICULUM.md#sdp-fnd-030)
4. [SDP-FND-040 — Abstraction, encapsulation, information hiding, and contracts](CURRICULUM.md#sdp-fnd-040)
5. [SDP-FND-050 — Composition, delegation, and inheritance](CURRICULUM.md#sdp-fnd-050)
6. [SDP-FND-060 — Polymorphism, dynamic dispatch, and subtyping](CURRICULUM.md#sdp-fnd-060)
7. [SDP-FND-070 — Duck typing, structural typing, nominal typing, Protocols, and ABCs](CURRICULUM.md#sdp-fnd-070)
8. [SDP-FND-080 — Dependency management, test seams, and test doubles](CURRICULUM.md#sdp-fnd-080)
9. [SDP-FND-090 — Mutability, shared state, ownership, and object lifetime](CURRICULUM.md#sdp-fnd-090)
10. [SDP-FND-100 — Modules, package boundaries, and circular dependencies](CURRICULUM.md#sdp-fnd-100)
11. [SDP-FND-110 — Simplicity heuristics and collaboration laws](CURRICULUM.md#sdp-fnd-110)
12. [SDP-SOL-010 — Single Responsibility Principle](CURRICULUM.md#sdp-sol-010)
13. [SDP-SOL-020 — Open/Closed Principle](CURRICULUM.md#sdp-sol-020)
14. [SDP-SOL-030 — Liskov Substitution Principle and behavioural subtyping](CURRICULUM.md#sdp-sol-030)
15. [SDP-SOL-040 — Interface Segregation Principle](CURRICULUM.md#sdp-sol-040)
16. [SDP-SOL-050 — Dependency Inversion Principle](CURRICULUM.md#sdp-sol-050)
17. [SDP-SOL-060 — SOLID interactions, tensions, and trade-offs](CURRICULUM.md#sdp-sol-060)
18. [SDP-SOL-070 — Pythonic SOLID with functions, modules, Protocols, and ABCs](CURRICULUM.md#sdp-sol-070)
19. [SDP-SOL-080 — SOLID critiques, overapplication, and legacy refactoring](CURRICULUM.md#sdp-sol-080)
20. [SDP-PYT-010 — Functions, closures, and callable objects as design tools](CURRICULUM.md#sdp-pyt-010)
21. [SDP-PYT-030 — Python decorator syntax versus the Decorator pattern](CURRICULUM.md#sdp-pyt-030)
22. [SDP-PYT-070 — Practical interface design with Protocols, ABCs, and duck typing](CURRICULUM.md#sdp-pyt-070)
23. [SDP-CRE-010 — Factory Method](CURRICULUM.md#sdp-cre-010)
24. [SDP-CRE-020 — Abstract Factory](CURRICULUM.md#sdp-cre-020)
25. [SDP-CRE-030 — Builder](CURRICULUM.md#sdp-cre-030)
26. [SDP-CRE-040 — Prototype](CURRICULUM.md#sdp-cre-040)
27. [SDP-CRE-050 — Singleton](CURRICULUM.md#sdp-cre-050)
28. [SDP-STR-010 — Adapter](CURRICULUM.md#sdp-str-010)
29. [SDP-STR-020 — Facade](CURRICULUM.md#sdp-str-020)
30. [SDP-STR-030 — Decorator](CURRICULUM.md#sdp-str-030)
31. [SDP-STR-040 — Proxy](CURRICULUM.md#sdp-str-040)
32. [SDP-STR-050 — Composite](CURRICULUM.md#sdp-str-050)
33. [SDP-STR-060 — Bridge](CURRICULUM.md#sdp-str-060)
34. [SDP-BEH-010 — Strategy](CURRICULUM.md#sdp-beh-010)
35. [SDP-BEH-020 — State](CURRICULUM.md#sdp-beh-020)
36. [SDP-BEH-030 — Observer](CURRICULUM.md#sdp-beh-030)
37. [SDP-BEH-040 — Command](CURRICULUM.md#sdp-beh-040)
38. [SDP-BEH-050 — Chain of Responsibility](CURRICULUM.md#sdp-beh-050)
39. [SDP-BEH-060 — Template Method](CURRICULUM.md#sdp-beh-060)
40. [SDP-BEH-080 — Mediator](CURRICULUM.md#sdp-beh-080)
41. [SDP-APP-010 — Dependency Injection and the composition root](CURRICULUM.md#sdp-app-010)
42. [SDP-APP-040 — Repository](CURRICULUM.md#sdp-app-040)
43. [SDP-APP-050 — Unit of Work](CURRICULUM.md#sdp-app-050)
44. [SDP-APP-070 — Domain Events](CURRICULUM.md#sdp-app-070)
45. [SDP-APP-100 — Active Record versus Data Mapper](CURRICULUM.md#sdp-app-100)
46. [SDP-ARC-050 — Event-driven application boundaries](CURRICULUM.md#sdp-arc-050)
47. [SDP-ARC-080 — Architectural boundaries and evolutionary design](CURRICULUM.md#sdp-arc-080)
48. [SDP-RAR-050 — Service Locator](CURRICULUM.md#sdp-rar-050)
49. [SDP-REF-010 — Design smells and change-force diagnosis](CURRICULUM.md#sdp-ref-010)
50. [SDP-REF-100 — Safe incremental refactoring with characterization tests](CURRICULUM.md#sdp-ref-100)
51. [SDP-INT-010 — Scenario recognition and choosing the simplest design](CURRICULUM.md#sdp-int-010)
52. [SDP-INT-020 — Strategy versus State versus Template Method versus Command](CURRICULUM.md#sdp-int-020)
53. [SDP-INT-030 — Adapter versus Facade versus Proxy versus Decorator](CURRICULUM.md#sdp-int-030)
54. [SDP-INT-040 — Bridge versus Adapter; Composite versus Decorator](CURRICULUM.md#sdp-int-040)
55. [SDP-INT-050 — Factory Method versus Abstract Factory versus Builder versus Prototype](CURRICULUM.md#sdp-int-050)
56. [SDP-INT-060 — Observer versus publish/subscribe versus Mediator versus Domain Events](CURRICULUM.md#sdp-int-060)
57. [SDP-INT-070 — Dependency Inversion versus Injection versus IoC versus Service Locator](CURRICULUM.md#sdp-int-070)
58. [SDP-INT-080 — Protocol versus ABC versus duck typing; inheritance versus composition versus delegation](CURRICULUM.md#sdp-int-080)
59. [SDP-INT-090 — Repository versus DAO and Unit of Work; object versus architectural boundaries](CURRICULUM.md#sdp-int-090)
60. [SDP-INT-100 — Senior pattern combinations, code review, and mock interview synthesis](CURRICULUM.md#sdp-int-100)

### Practice, recall, and interview schedule

| Session | Unit steps | Required activity |
|---|---|---|
| Every study block | Next 1–3 steps | Physical Notebook Core, one code/refactoring task, and one rejected alternative |
| Every third block | Previous steps | Closed-book recall and one comparison from a new scenario |
| Every domain boundary | Completed domain steps | Code review or refactoring drill |
| Final checkpoint | Entire path | One-question-at-a-time senior mock interview and weakness log |

### Project or refactoring milestones

- [SDP-PRJ-020 — Extensible Pricing and Promotion Engine](PROJECTS.md#sdp-prj-020) — Defend pattern selection under staged pricing changes.
- [SDP-PRJ-050 — Auditable Workflow and Command Engine](PROJECTS.md#sdp-prj-050) — Use the workflow engine for State, Command, Memento, and Observer comparisons.
- [SDP-PRJ-060 — Python Backend Architecture Lab](PROJECTS.md#sdp-prj-060) — Run the final architecture and repository/UoW interview walkthrough.

### Completion meaning

Finishing a path does not automatically mark every unit Retained or Mastered. Each unit advances only through the evidence rules in [PROGRESS.md](PROGRESS.md).
