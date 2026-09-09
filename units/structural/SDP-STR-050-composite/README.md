# SDP-STR-050 — Composite

## Physical Notebook Core

### Problem or change pressure

A workshop planner estimates one task. Tomorrow it must estimate a kit containing tasks, then a
workshop containing kits. Each caller should ask the same question at any level.

### One-sentence mental model

> Give a part and a group the same useful operation; the group combines its children's answers.

### One essential visual

```text
describe(any Estimable) ──estimate()──> workshop Group
                                      ├─ setup Task: 5 min
                                      ├─ kit Group ──┬─ cut Task: 12 min
                                      │             └─ label Task: 3 min
                                      └─ same kit reference again: 15 min
                                      total: 35 min, 5 task occurrences
```

### How to read this visual

Start at the client, then follow children in order. A task answers directly; a group asks its
children and adds their results. The last edge refers to the existing kit, not a copied kit.

### Key insight

Uniform calling does not decide whether a shared part counts once or once per occurrence. Here it
counts per occurrence: the same reusable kit recipe appears twice in the workshop estimate.

### Simplification or limitation

This is a conceptual object/call picture. The drawn expansion hides sharing in the object DAG.
Minutes mean summed effort, not elapsed schedule time; no task is executed. It is not a browser
render, memory-layout diagram, or performance measurement.

### Governing rules or invariants

1. Keep the common operation meaningful for both leaf and group, including empty groups and errors.
2. Decide aliasing, cycles, order, mutation and ownership before claiming uniformity is safe.
3. Give child management only to things that can contain children; a narrow client need not edit.

### Minimal Python example

```python
from collections.abc import Callable


def group(*children: Callable[[], int]) -> Callable[[], int]:
    def minutes() -> int:
        return sum(child() for child in children)

    return minutes


kit = group(lambda: 12, lambda: 3)
workshop = group(lambda: 5, kit, kit)
assert kit() == 15
assert workshop() == 35
assert group()() == 0
```

This is the collaboration in callable form. It has no names, structure validation or traversal API;
its callables must keep the same pure minutes contract. The bounded value implementation follows.

### One common misconception

**Mistake:** Every object with children is a Composite, and all components must have `add`.

**Correction:** The useful property is a common operation for parts and groups. A recursive data
structure alone need not provide it, and leaf objects need no pretend child-management capability.

### Important trade-offs

- A small operation simplifies clients; a universal node interface creates meaningless methods.
- Shared immutable values simplify reuse; shared mutable entities need much stronger ownership rules.
- Recursive methods are readable; depth and expanded work still need explicit bounds.

### Interview-revision cues

- Recognition: a client must apply one operation to a part or a recursively assembled whole.
- Trace: leaf returns; group delegates and aggregates; client receives the common result.
- Rejection: a flat list or one recursive function can be the complete design.

## Unit metadata

| Field | Value |
|---|---|
| Domain | GoF structural patterns |
| Curriculum | [SDP-STR-050](../../../CURRICULUM.md#sdp-str-050) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Treat individual objects and recursive groups through a common operation while controlling ownership, traversal, and invalid combinations. |
| Hard prerequisites | [SDP-FND-050](../../../CURRICULUM.md#sdp-fnd-050), [SDP-FND-060](../../../CURRICULUM.md#sdp-fnd-060) |
| Soft prerequisites | None at curriculum-unit level |
| Priority | Professional |
| Interview frequency | Medium |
| Production frequency | Medium |
| Python/backend relevance | Medium |
| Depth | D2 |
| Scope | GoF, Structural |
| Size | L |
| First understanding | 4–6 h |
| Hands-on practice | 5–9 h |
| Evidence profile | E+I+D+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Approved |

Frequency labels are curriculum judgments, not measured statistics. Learning remains **Not started**.
Maintainer-generated notes and passing tests do not establish Rahul's learning evidence. Use the
[demo](examples/run_composite_demo.py), [independent unsolved lab](practice/README.md), and
[controlled observation](experiments/EXP-01-occurrences/README.md). The observation supports E/D;
it does not add X to the canonical evidence profile. [Validation](VALIDATION.md) records actual runs.

## 1. Simple explanation and prerequisite bridge

A task knows its own estimated effort. A group knows its children and combines their estimates.
The planner asks `estimate()` without unpacking the group itself. At every recursive level, a
child can answer directly or delegate further.

From SDP-FND-050: composition stores references; delegation calls the referenced collaborator;
inheritance is a class relationship. From SDP-FND-060: dynamic dispatch picks the receiver's method;
a substitute is useful only when it preserves the meaning of that method. Both prerequisite notes
are Approved, but their learning states remain Not started. The smallest bridge is to trace
`group.estimate()` → `child.estimate()` and explain why neither class needs to inherit the other.

A `Protocol` is a static description of the operation a caller requires. It does not run the
operation or validate its business meaning. Only that much typing is needed for the first pass.

## 2. Real problem and forces

The synthetic workshop team estimates preparation recipes. A recipe is reused in several places;
it is not a uniquely assigned real job. Effort adds even when a worker might later do tasks in
parallel. Names are labels, not identifiers. Inputs are trusted in-process values after construction.

| Design | Enough when | Pressure or cost |
|---|---|---|
| Values and `sum` | All work is flat and needs only arithmetic | New grouping may remain a presentation concern |
| Explicit recursive data and one function | Shape set is small; operation is centralized | Adding operations is easy; every operation must know the data variants |
| Helper dispatch on task/group | One caller needs a boundary over a closed model | Repeated dispatch in many clients duplicates structural knowledge |
| Composition-based Composite | Many clients ask the same operation at any depth | Each component must honor aggregation and failure semantics |
| Narrow Protocol plus validated values | Clients need flexibility; persisted structure needs limits | Open client capability and closed construction have different extension rules |
| Universal node hierarchy | Often motivated by speculative reuse | Leaves acquire editing, I/O and lifecycle methods they cannot honor |

Do not introduce Composite merely because JSON contains nested lists. Introduce it when the
part/group substitution improves a real client and the operation remains coherent at every level.

## 3. History and formal intent

The GoF Composite idea models recursive part–whole structures so a client can use a common operation
on a leaf or a group. A composite holds components and implements its operation through them.
The Python version here preserves that collaboration without requiring a shared implementation base.

Rebecca Wirfs-Brock's author-hosted [“Refreshing Patterns,” p. 46](https://www.wirfs-brock.com/PDFs/Refreshing%20Patterns.pdf)
examines the original Composite form and separates performing an operation from managing children.
She records Ralph Johnson's retrospective disagreement with putting child mutation on every
component. This supports choosing capabilities deliberately, rather than treating the original class
diagram as compulsory. This note does not claim access to the complete GoF Composite chapter or
reproduce either source diagram.

## 4. Participants and collaboration

| Participant | Here | Responsibility | Boundary |
|---|---|---|---|
| Client | `describe(component)` | Ask for an estimate and format it | Does not traverse or edit children |
| Component contract | `Estimable` | `estimate() -> Estimate` with common meaning | Does not promise `add`, parent lookup or resource cleanup |
| Leaf | `Task` | Answer with its minutes and one task occurrence | Has no children |
| Composite | `Group` | Hold ordered children; aggregate their answers | Does not schedule or execute tasks |
| Composition root | Demo/application code | Build validated values, retain a root version | Owns business interpretation and publication of new versions |
| Traversal helper | `walk_tasks` | Expose occurrence paths for diagnostics | Deliberately knows the closed Task/Group structure |

The common operation is polymorphic. Construction and traversal may know concrete variants; hiding
all type distinctions from every part of the program is not the goal.

```text
1. describe(workshop) asks workshop.estimate()
2. workshop visits setup                      → Estimate(5, 1)
3. workshop visits kit; kit visits cut, label  → Estimate(15, 2)
4. workshop visits that kit again              → Estimate(15, 2)
5. workshop returns                           → Estimate(35, 5)
6. describe formats                           → "35 min / 5 tasks"
```

**How to read:** numbers are a sequential call trace; each arrow is a returned value.
**Key insight:** the client does not branch on task versus group; each group owns its aggregation.
**Limitation:** the trace expands aliases and omits construction; it depicts pure value queries, not
an execution engine or transactional workflow.

## 5. Before-pattern code and concrete pain

```python
setup_minutes = 5
kit_minutes = [12, 3]
assert setup_minutes + sum(kit_minutes) == 20
assert setup_minutes + 2 * sum(kit_minutes) == 35
```

This is a good solution for one stable calculation. Now a recipe may contain other recipes, callers
may preview a single task or an entire workshop, and an explanation must preserve grouping. Teaching
every caller where to put nested loops scatters the structural rules. Flattening once is still a
reasonable alternative if no consumer needs those group boundaries afterward.

A helper dispatch function can centralize the recursion. A small, closed recursive value model is
an honest solution, not a failed attempt at a pattern:

```python
from typing import TypeAlias

Minutes: TypeAlias = int | tuple["Minutes", ...]


def effort(node: Minutes) -> int:
    if isinstance(node, int):
        return node
    return sum(effort(child) for child in node)


recipe: Minutes = (5, (12, 3), (12, 3))
assert effort(recipe) == 35
```

This snippet assumes valid nonnegative values and bounded acyclic input. It is not a validator.
For two variants and one operation, keep it. Composite becomes useful when domain components own
meaningful behavior and multiple clients should depend only on that behavior. A callable, as in the
notebook core, may provide the same seam without classes when names and structure are unnecessary.

## 6. Minimal Pythonic design and typed implementation

The runnable [work_plan.py](examples/work_plan.py) contains seven small concepts: a result value,
a one-operation Protocol, a formatting client, two value components, an occurrence value and a
traversal function. `Task.estimate` returns `Estimate(minutes, 1)`. `Group.estimate` calls the same
method on each child and adds both fields, starting at zero. Neither concrete component inherits
the Protocol or shares a base class. The constructors carry the structure policy, not the client.

```python
from dataclasses import replace

from work_plan import Estimable, Estimate, Group, Task, describe, walk_tasks

kit = Group("kit", (Task("cut", 12), Task("label", 3)))
root = Group("workshop", (Task("setup", 5), kit, kit))
client_view: Estimable = root
assert describe(client_view) == "35 min / 5 tasks"
assert root.estimate() == Estimate(35, 5)
assert [visit.path for visit in walk_tasks(root)] == [(0,), (1, 0), (1, 1), (2, 0), (2, 1)]
new_root = replace(root, children=(*root.children, Task("cleanup", 4)))
assert new_root.estimate() == Estimate(39, 6)
assert root.estimate() == Estimate(35, 5)
```

Run this fence with `examples/` on `PYTHONPATH`; every Python fence is independently executable.
The complete example stays in source files so explanatory snippets do not become a second copy of
the implementation. The [demo](examples/run_composite_demo.py) prints the same occurrence paths.

### Common behavior beyond the method signature

| Dimension | Accepted contract |
|---|---|
| Meaning | Nonnegative whole minutes of effort and count of leaf occurrences |
| Inputs | No request arguments; valid completed values, no external state needed |
| Leaf | One task even if its effort is zero |
| Empty group | `Estimate(0, 0)`; empty is not a task and not a validation success signal |
| Ordering | Left-to-right depth-first delegation, once per occurrence |
| Repetition | Same values produce the same answer; no mutation or I/O |
| Failures | Constructors raise `TypeError` for wrong admitted kinds, `ValueError` for invalid values/limits |
| Query failure | No catch-and-continue or partial estimate; an exception propagates |
| Ownership | Strong references to completed immutable values; aliases are permitted, no unique parent |

The supplied components do not introduce normal domain failures at query time. Interpreter/resource
failures remain possible. A foreign `Estimable` accepted by `describe` must keep the documented
semantics; neither the Protocol nor the formatter checks nonnegativity, effects, or honesty of its
`Estimate`. A class returning an hour count as minutes can pass static typing and still be wrong.

Integer addition here permits regrouping and reordering without changing totals. That is a property
of this aggregation, not a universal Composite rule. Rendering ordered text, stopping on a failed
check, choosing maximum duration, and collecting errors have different identities, order and
short-circuit behavior. A parallel schedule is not computed by summing effort.

## 7. Structure policy: ownership, aliases, mutation and cycles

Our structure is an **immutable value DAG with occurrence-based evaluation**. It includes ordinary
trees, but sharing means not every instance graph is a tree. A node may have several incoming edges,
including two edges from the same parent. Each edge means “include this recipe again.”

| Case | Our behavior | Why |
|---|---|---|
| Same task reference twice | Two tasks, twice the minutes | Inclusion is an occurrence, not unique-entity membership |
| Equal but distinct task values | Also two tasks | Equality does not mean one real-world identity |
| Shared group in two branches | Expand both occurrences | No global deduplication set |
| Empty group | Allowed; consumes one structural occurrence | Traversal work exists even with no task leaves |
| Mutable list or generator of children | Rejected; supply a completed tuple | No live collection, implicit consumption or infinite iterable |
| Foreign implementation/subclass in children | Rejected by exact-type admission | Local invariants require the supplied completed value types |
| Rename/reorder/replace | Construct a new value/root | Existing references keep their previous meaning |
| Self-edge or ancestor-edge via ordinary field assignment | Frozen assignment raises | Published nodes cannot be rewired through the supported API |

### Why construction is acyclic without a visited set

Construct a task first: it has no edges. Construct a group only from already completed valid values.
None of those existing values can acquire an edge back to the new group through the public API.
Inductively, bottom-up construction preserves acyclicity. A tuple cannot later be appended to, and
frozen nodes cannot normally have their fields rebound. This proof needs the closed admission rule;
accepting arbitrary mutable Protocol implementations as children would invalidate it.

This is trusted Python value discipline. [Frozen dataclasses](https://docs.python.org/3.14/library/dataclasses.html#frozen-instances)
emulate immutability; they are not a security boundary. `object.__setattr__`, forged objects,
monkey-patching, unchecked deserialization and hostile subclasses are outside the supported API.
The module uses `object.__setattr__` only while initializing derived metadata. It does not validate
an arbitrary already-existing object graph. It would be misleading to claim it detects all cycles.

For a mutable exclusive tree, adding a child needs checks for self/ancestor cycles, an existing
parent, duplicate edges and allowed parent/child kinds; moving it needs an atomic detach/attach
policy. For a general imported graph, validate cycles with a current DFS-path set; use a separate
completed/visited set only when the chosen semantics require it. A shared completed node is not a
cycle. These are alternatives to design, not implementations supplied by this unit.

### Identity and versions

Python's `is` tests identity, while a dataclass normally compares its field values. Identity and
container references are [language concepts](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types);
the numeric value of `id()` is not a portable business key. The probe keeps objects alive and counts
identities only within that run. Do not store those numbers in an API or database.

`replace(root, children=...)` runs construction again and yields a new validated root. It reuses
unchanged children; it does not clone a whole DAG. Changing one branch does not rewrite aliases in
other branches. An occurrence path such as `(1, 0)` means child 1, then child 0 **in this root
version**. Reordering siblings changes paths. Persist domain IDs and root revisions when stable
cross-version references are needed; names and tuple positions do not provide them.

## 8. Traversal and child-only capabilities

`estimate()` uses internal recursive delegation. `walk_tasks()` is an external iterator over leaves
with occurrence paths. The iterator uses an explicit stack, pushes children in reverse order, and
therefore pops them in the original left-to-right order. It preserves group boundaries in the path
and yields the actual task reference. A single-task root has path `()`; empty groups yield nothing.
Separate traversals use separate stacks. Consumers may stop early; no resources are acquired.

Keep group inspection/editing at a group-specific boundary. Keep task-specific editing, such as
changing its duration, at the task boundary. A client that only estimates needs neither. There is
no `len(group)` here: direct child count, leaf-occurrence count and total node count would be
ambiguous choices, so use explicit names.

A universal hierarchy can make nonsense type-check:

```python
class EverythingNode:
    def add(self, child: "EverythingNode") -> None:
        raise NotImplementedError("this leaf cannot contain children")


leaf = EverythingNode()
try:
    leaf.add(EverythingNode())
except NotImplementedError:
    pass
else:
    raise AssertionError("the advertised edit capability was meaningless for a leaf")
```

This is an executable misuse demonstration. Broadening every leaf to satisfy an editing API moves a
preventable design error into runtime. Do not solve that by quietly ignoring `add` either.

## 9. Python mechanics and version boundaries

- **Static typing:** [Protocol assignability](https://typing.python.org/en/latest/spec/protocol.html#assignability-relationships-with-other-types)
  checks compatible members without requiring inheritance. It cannot prove aggregation meaning,
  purity, acyclicity or ownership. `Estimable` is deliberately not runtime-checkable.
- **Construction versus clients:** `Work = Task | Group` restricts the stored vocabulary while
  `describe` accepts any `Estimable`. An external estimator can be a whole client dependency without
  being safe to embed as a child. Supporting more stored kinds requires reviewing validation,
  traversal and the invariant proof together. This is a deliberate extension cost.
- **Library behavior:** [dataclasses in 3.11](https://docs.python.org/3.11/library/dataclasses.html)
  already support our `frozen`, `slots`, `field(init=False)` and `replace` usage. Tuples freeze the
  child collection; freezing an object that contained a list would not freeze that list. Cached
  height/occurrence fields are derived at construction, excluded from equality and repr.
- **No runtime type magic:** [`final`](https://docs.python.org/3.14/library/typing.html#typing.final)
  tells a checker to reject subclassing; it does not prevent it at runtime. The exact-type child
  check supplies our runtime admission restriction. `cast` in negative runtime tests bypasses
  checking; it does not convert an object.
- **Duration validation:** [`bool` is a subtype of `int`](https://docs.python.org/3.14/library/stdtypes.html#boolean-type-bool).
  `type(minutes) is int` intentionally rejects booleans and other integer subclasses here. An
  annotation of `int` alone would not encode that domain restriction.
- **Python 3.14 overlay:** [annotations are deferred by default](https://docs.python.org/3.14/whatsnew/3.14.html#pep-649-pep-749-deferred-evaluation-of-annotations).
  The source retains `from __future__ import annotations` for 3.11 forward references; its string
  behavior is unchanged in 3.14. `Work: TypeAlias = Task | Group` appears after both classes, because
  its assigned expression is evaluated normally. The 3.12 `type` statement is not used. No annotation
  introspection, frame internals or runtime-checkable Protocol version behavior is required.

The same source is tested on CPython 3.11 and 3.14. No free-threaded, alternate-interpreter or
CPython memory-layout result is implied by those runs.

## 10. Bounds, performance and memory

A task or empty group has height 0; a nonempty parent adds one edge to its deepest child. Each root
admits at most 32 edges of height and 10,000 expanded node occurrences, including groups. These are
teaching policy constants, not Python limits or measured production thresholds. Checking only unique
objects would miss a compact shared DAG whose evaluation expands exponentially.

If a group has `k` direct children, its admission checks use O(k) child metadata, with an early length
rejection for a huge tuple. Metadata was computed by the same constructors. Each `estimate()` takes
O(N) visits for expanded occurrences N and O(H) call-stack depth H; integer arithmetic cost also grows
with integer size. We do not cache the estimate or benchmark these costs. Iterative traversal avoids
recursive calls but copies paths: its work includes O(N × H) path copying in the worst case, and its
pending stack can grow with width. Bounding recursion alone does not bound CPU or memory.

A chain at the allowed height is tested on both runtimes; it is not guaranteed to fit if called from
an already exhausted interpreter stack. [`sys.setrecursionlimit`](https://docs.python.org/3.14/library/sys.html#sys.setrecursionlimit)
has platform-dependent limits and setting it too high can crash a process. For deeply nested input,
use an iterative evaluator and input-size budgets instead of treating a larger limit as the fix.

Construction also costs memory for the caller's already-created tuple, which admission cannot undo.
No limits on label length, integer magnitude, total retained root versions or concurrent requests
are supplied. A public import endpoint needs byte limits and iterative parsing before these objects
exist. A cached summary could be computed at construction for this pure closed model, but that would
shift the demonstration away from recursive collaboration. If added later, test invariants and
version invalidation rather than claiming Composite itself makes queries fast.

## 11. Failure, observability, concurrency and lifetime

**Failure scenario:** an estimate is incorrectly reused as an execution plan. A shared kit is charged
or scheduled twice, even though the business meant a single real job. A global `visited` set makes
that incident disappear in one sample but silently changes legitimate repeated-recipe estimates.
Resolve the domain meaning first: unique jobs need stable IDs and explicit allocation semantics;
repeatable recipes need occurrence semantics. Test both the alias and equal-but-distinct cases.

A second failure is accepting mutable external children after validating once. A child can later
point back to its parent, making previous bounds false. Contain that with a value snapshot boundary,
or redesign for controlled mutations and synchronized validation. Do not add just a `seen` set to
one query and assume all future operations are safe.

The example raises on invalid construction and keeps previous roots usable. It does not swallow
child exceptions or return a subtotal. Pure queries have no business side effects to roll back.
If a later design adds network requests or writes, “raise on the first error” does not undo previous
writes; retries, deadlines, cancellation and compensation need separate contracts.

For debugging, log a root revision, operation, occurrence path and domain error category at the
application boundary. The demo prints synthetic labels and paths only. Distinguish counts of unique
objects, node occurrences, leaf occurrences and external actions; none of these counts is elapsed
time. A request-level correlation ID is more useful than printing a process-local `id()` value.

Read-only values remove ordinary shared writes, but publishing a new current root, editing a mutable
tree, or combining multiple reads with updates still needs a consistency policy. Python's
[free-threading guidance](https://docs.python.org/3.14/howto/free-threading-python.html#thread-safety)
advises explicit synchronization rather than relying on built-in container locks. This module has
no locking or parallel evaluation, and its tests make no concurrency proof. Do not share one live
iterator among threads or add parallel traversal without defining result order and error behavior.

Groups hold strong references to value children. Dropping one root need not make a shared subtree
unreachable. There are no sockets, files or sessions to close. For resource-bearing leaves, define
an external owner and deterministic cleanup; closing every occurrence could close a shared resource
several times. Python does not guarantee immediate finalization; use explicit resource management
as described in the [data model](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types).

## 12. Testing strategy and controlled observation

| Test | Evidence | Limit |
|---|---|---|
| Leaf, zero-minute leaf, empty group | Common result semantics and identity value | Not a scheduler or validation engine |
| Nested group and external client | Common operation works at different levels | Structural typing does not prove meaning |
| Alias, diamond, equal distinct values | Occurrences differ from unique identities | No arbitrary graph importer |
| Rebuild and frozen assignment | Supported edits preserve previous roots | Not tamper resistance |
| Height and occurrence boundaries | Exact boundary accepted, next level rejected | No measured service capacity |
| Ordered path assertions | External traversal preserves left-to-right leaf order | Paths are local to a root version |
| Hypothesis flat-value oracle | Nested aggregation agrees with independent sums | Generated cases are bounded; no universal proof |
| Negative typing controls | Wrong/missing operation, invalid stored kind, frozen edit, leaf editing rejected | No purity, duration-unit or ownership proof |
| Separate starter characterization | Current lab runs and its empty behavior is visible | Passing starter tests is not solving the target |

The [probe](examples/occurrence_probe.py) reports five cases plus a repeated-doubling bound. Same
reference twice gives two visits; distinct equal values also give two visits. A doubling DAG reaches
8,191 expanded nodes at level 12 and its next group is rejected. The test asserts every observation.
Read the [experiment record](experiments/EXP-01-occurrences/README.md) for actual output and limits.

## 13. Refactoring path and backend use

1. Characterize the current flat calculation, including zero and empty cases.
2. Decide what a repeated reference means before introducing nesting.
3. Centralize one recursive function; keep it if it solves the whole problem.
4. When clients need uniform behavior, move direct answers to leaves and aggregation to groups.
5. Introduce only the client operation; keep construction/editing capabilities separate.
6. Test aliasing, ordering, invalid combinations and the previous-root invariant.
7. Add bounded traversal for a real diagnostic consumer; remove unused generic node features.

A backend might store reusable preparation recipes, materialize one bounded immutable estimate
snapshot, and use the same formatter for a line item, kit or workshop. Authorization and request
size validation occur at the API boundary; database reads occur before value construction. This is
a proposed integration, not an executed database/FastAPI/Django example. ORM relationships alone
do not make a Composite, and recursively loading lazy database children could create many queries.

## 14. Variants, related units and selection

| Variant | Benefit | Obligation |
|---|---|---|
| Immutable occurrence model, supplied here | Safe recipe reuse and stable snapshots | Repeated references count repeatedly; rebuild to edit |
| Mutable exclusive tree | Natural editing and one parent per node | Centralize cycle checks, moves, permissions and atomicity |
| Shared entity DAG | Reuse one real entity in several views | Define unique-node versus path operations and lifetime ownership |
| Recursive data plus functions | Minimal machinery; easy new operations | Dispatch function owns the variant vocabulary |
| Capability-rich plugin Composite | New components implement the operation | Cannot inherit our acyclicity proof or immutable-child assumptions for free |

| Related unit | Relationship | Difference to remember |
|---|---|---|
| [SDP-FND-050](../../../CURRICULUM.md#sdp-fnd-050) | Composition and delegation supply mechanics | Composite specifically supports recursive part/group substitution |
| [SDP-STR-030](../../../CURRICULUM.md#sdp-str-030) | Both can recursively compose compatible operations | Decorator wraps a target to add behavior; Composite aggregates parts |
| [SDP-STR-040](../../../CURRICULUM.md#sdp-str-040) | May mediate access to an entire root | Proxy controls access; it does not define part–whole counting |
| [SDP-BEH-070](../../../CURRICULUM.md#sdp-beh-070) | Traversal can be a separate capability | Visiting elements does not itself give part/group operation uniformity |
| [SDP-BEH-100](../../../CURRICULUM.md#sdp-beh-100) | Alternative place for operations over a stable structure | Operation extensibility is a separate design pressure |
| [SDP-INT-040](../../../CURRICULUM.md#sdp-int-040) | Owns deeper comparison practice | This unit only identifies its boundary |

These are bounded comparisons, not initialization or teaching material for the later units.

Use Composite when recursive parts and groups really share an operation and clients benefit from
ignoring the distinction. Prefer simple values/loops for flat data; a recursive helper for a small
closed model; a graph algorithm when reachability, unique entities or cycles are the central problem.
Reject an aggregate that cannot give a truthful answer through the leaf contract.

| Misuse | Consequence | Better move |
|---|---|---|
| Every node supports `add`, `save`, `close`, `authorize` | Leaves advertise unsupported operations | Put each capability at its actual consumer/owner boundary |
| A visited set added to stop “double counting” | Changes repeated-recipe semantics silently | Specify occurrence versus entity identity first |
| Parent pointers added to shared immutable values | Ambiguous parent; harder lifetime and edit rules | Use root-local paths or choose an exclusive mutable tree |
| Recursive totals used as a scheduler | Effort confused with elapsed time | Model precedence, resources and concurrency separately |
| Arbitrary plugins admitted with `isinstance(Protocol)` | Signature/presence check treated as validation | Review behavioral and structure contracts explicitly |
| A node subclass for every business grouping label | More class names with identical behavior | Use a group name/value; specialize only differing behavior |

## 15. Interview preparation

Ask one question at a time. Wait for an attempt, then identify the first missing reasoning step from
this review guide. Do not deliver this table as a memorized answer script.

| Stage | Prompt | Exact reasoning gap to probe |
|---|---|---|
| Definition | Explain Composite using one task and a workshop | Names “tree” but never states the common operation |
| Forces | Would you replace a flat sum with classes? | Cannot name the change that pays for the abstraction |
| Collaboration | Trace the same kit appearing twice | Counts unique objects instead of following occurrences |
| Implementation | Sketch a group operation and its empty case | Omits the aggregation identity or counts an empty group as work |
| Contract review | Both methods return integers; are they compatible? | Fails to check units, effects, errors and repeatability |
| Capabilities | Where should `add_child` live? | Confuses operation uniformity with universal mutability |
| Failure | An imported child points to an ancestor | Cannot distinguish an active-path cycle from a shared completed node |
| Refactoring | Keep old root previews stable after an edit | Assumes shallow collection copying freezes mutable descendants |
| Comparison | A wrapper adds timing around one estimate | Chooses from shape alone instead of intent and aggregation |
| Changed requirement | These references now identify real jobs | Keeps recipe occurrence semantics without reconsidering identity |
| Production critique | Put network calls in each leaf | Assumes recursive errors imply rollback or bounded latency |
| Senior judgment | Support depth 50,000 and mutable shared nodes | Adds a recursion-limit tweak instead of changing algorithms and ownership |

Weak-answer traps: “everything is a tree,” “Protocol enforces the contract,” “frozen means any object
is immutable,” and “the GIL makes editing safe.” Follow up with the smallest counterexample, not a
long lecture. The [lab](practice/README.md) provides an independent implementation/debugging task.

## 16. Closed-book revision and evidence

Reconstruct the part/group diagram, the alias calculation, the empty identity and one rejection case.
Explain why the formatter is open to a foreign estimator while group children are closed. Trace a
leaf path in a rebuilt root. Reject Composite for one flat-data scenario and defend it for one
recursive scenario. Explain one failure caused by changing from recipes to real entities.

Evidence profile: E = explain the collaboration and contract; I = implement and test a separate lab
attempt; D = debug/refactor the starter using a small counterexample; T = select or reject the design
under changed identity/ownership requirements. A maintainer test run supplies none of Rahul's attempt,
delayed recall or transfer evidence. Record learner evidence only through PROGRESS.md rules.

## 17. Vocabulary and professional English

### Aggregate — AG-ri-gayt

Combine several answers into one. Hindi cue: जोड़कर एक नतीजा बनाना. Here the group aggregates effort.

1. We aggregate the survey results each week.
2. The report aggregates several estimates.
3. An aggregate can hide an exceptional case.
4. **Interview:** “The group aggregates the same result type that a leaf returns.”
5. **Engineering discussion:** “We should define whether this aggregate counts occurrences or IDs.”

### Alias — AY-lee-us

Another reference or name for the same thing. Hindi cue: उसी वस्तु का दूसरा संदर्भ.
Here two edges may point to one task object.

1. This command has a shorter alias.
2. Two names can be aliases for the same account.
3. An alias does not create a copy.
4. **Interview:** “Shared references form a DAG, but this operation counts each occurrence.”
5. **Engineering discussion:** “Rebuilding one branch should not mutate another branch's alias.”

### Invariant — in-VAIR-ee-unt

A rule that must remain true across supported operations. Hindi cue: हमेशा बनी रहने वाली शर्त.
Here a completed group stays acyclic and within its structural bounds.

1. The invariant applies before and after the update.
2. We wrote down the invariant before refactoring.
3. An optimization must preserve the invariant.
4. **Interview:** “The acyclicity proof relies on bottom-up construction and immutable children.”
5. **Engineering discussion:** “Allowing a mutable plugin would invalidate that proof.”

## 18. Python Mastery references

The exact direct mapping is [PY-OBJ-040 — Python data model and special methods](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-040),
**Soft**: understand that a capability is a meaningful operation; adding a container-looking class
does not automatically supply useful `len`, iteration or editing semantics.

The foundation prerequisites map to
[PY-OBJ-010 — Classes, instances, methods, and construction](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-010),
[PY-OBJ-020 — Properties, encapsulation, and composition](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-020),
and [PY-OBJ-030 — Inheritance, MRO, and super](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-030).
Minimum bridge: a stored child is a reference, a method runs on its receiver, and composition does
not require inheritance. These links come from PYTHON_REFERENCES.md; no cross-repository completion
or reading of those unit contents is claimed.

## 19. Authoritative sources and boundaries

Sources opened and read for this unit, with subtle claims linked near their use:

1. [Rebecca J. Wirfs-Brock, “Refreshing Patterns,” IEEE Software, May/June 2006, pp. 45–47](https://www.wirfs-brock.com/PDFs/Refreshing%20Patterns.pdf): author-hosted account of Composite roles and the child-management trade-off; not the full GoF chapter.
2. [Python 3.11 dataclasses](https://docs.python.org/3.11/library/dataclasses.html) and [Python 3.14 frozen instances](https://docs.python.org/3.14/library/dataclasses.html#frozen-instances): value machinery, equality, replacement and limits of freezing.
3. [Python typing specification, Protocol assignability](https://typing.python.org/en/latest/spec/protocol.html#assignability-relationships-with-other-types): structural static contract.
4. [Python 3.14 typing](https://docs.python.org/3.14/library/typing.html#typing.final): annotations, final and alias syntax/version boundaries.
5. [Python 3.14 data model, objects, values and types](https://docs.python.org/3.14/reference/datamodel.html#objects-values-and-types): identity, container references and explicit resource lifetime.
6. [Python 3.14 built-in Boolean type](https://docs.python.org/3.14/library/stdtypes.html#boolean-type-bool): Boolean/integer relationship.
7. [Python 3.14 sys.setrecursionlimit](https://docs.python.org/3.14/library/sys.html#sys.setrecursionlimit): depth limits and risks.
8. [What's new in Python 3.14, deferred annotations](https://docs.python.org/3.14/whatsnew/3.14.html#pep-649-pep-749-deferred-evaluation-of-annotations): default evaluation changed; future-import behavior retained.
9. [Python support for free threading, thread safety](https://docs.python.org/3.14/howto/free-threading-python.html#thread-safety): synchronize application mutation explicitly.

Structure admission, bounds, counting and error policy are this example's design choices. Complexity
statements are analysis of this code, not benchmarks. Runtime checks are in VALIDATION.md. No
framework behavior or CPython internals are invented. All examples and diagrams are original and
synthetic. No learner solution or private data is included. Only this README, once Approved, is a
candidate for NotebookLM under [the repository policy](../../../NOTEBOOKLM.md); no upload is performed.
