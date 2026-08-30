# SDP-SOL-080 — SOLID critiques, overapplication, and legacy refactoring

## Physical Notebook Core

### Problem or change pressure

A small change requires navigating many wrappers, yet nobody can confidently say what
the old code does on failure. Adding another interface will not resolve that uncertainty.

### One-sentence mental model

> Protect what callers can observe, then make the next real change easier in small steps.

### One essential visual

```text
known change -> observe old boundary -> one structural edit -> compare -> keep or undo
                      result + errors + effects + state + input consumption
```

### How to read this visual

Follow the top row left to right. Arrows mean engineering steps; the lower row names what
the comparison may need to include.

### Key insight

Identical return values do not establish identical behaviour.

### Simplification or limitation

This is a conceptual workflow, not runtime internals. Tests sample a chosen boundary;
they cannot prove every possible production behaviour is unchanged.

### Governing rules or invariants

1. Name the actual change and the callers whose promises must survive.
2. Preserve surprising behaviour during refactoring; approve a correction separately.
3. An abstraction must earn its cost. Stop when the known change is easy and safe enough.

### Minimal Python example

```python
def format_name(name: str) -> str:
    if name == "":
        raise ValueError("empty name")
    return f"[{name.upper()}]"


assert format_name(" Mira ") == "[ MIRA ]"  # Do not silently add stripping.
```

### One common misconception

**Mistake:** “All tests passed, so the new design is correct and more SOLID.”

**Correction:** The checked behaviours passed. You still need the right observation
boundary, justified responsibilities, and evidence that the next change became easier.

### Important trade-offs

- A stable boundary can contain change; speculative boundaries add work to every change.
- Keeping an old quirk aids compatibility; keeping it forever needs a separate decision.

### Interview-revision cues

- What change is painful, for which caller?
- What observable behaviour could this cleanup accidentally change?
- Which abstraction would you remove, and what evidence would make you retain it?

## Unit metadata

| Field | Value |
|---|---|
| Domain | SOLID principles |
| Curriculum | [SDP-SOL-080](../../../CURRICULUM.md#sdp-sol-080) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Explain the limits of SOLID, recognize needless abstraction, and refactor legacy Python incrementally while preserving behaviour. |
| Hard prerequisites | [SDP-SOL-060](../../../CURRICULUM.md#sdp-sol-060), [SDP-SOL-070](../../../CURRICULUM.md#sdp-sol-070), [SDP-FND-110](../../../CURRICULUM.md#sdp-fnd-110) |
| Soft prerequisites | None specified by the curriculum |
| Priority | Professional |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D3 |
| Scope | SOLID, Refactoring |
| Size | L |
| First understanding | 4–6 h |
| Hands-on practice | 5–9 h |
| Evidence profile | E+I+D+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Approved |

The frequency labels are curriculum judgments, not measured statistics. The supporting
experiment does not change the canonical evidence profile to require X.

## 1. Simple explanation

Think of repairing a busy workshop while it remains open. First find out which doors people
use and what must keep working. Move one obstruction, check the route, and continue. A new
corridor is useful only if it improves an actual journey.

SOLID helps you ask about responsibilities, variation, promises, capabilities, and dependency
direction. It does not select the correct business boundary for you. A program can have many
interfaces and still hide state, mishandle failure, or be difficult to change.

The prerequisite notes exist; their tracker rows do not establish learner mastery. The
smallest bridge is:

- **SDP-SOL-060:** identify the caller, change pressure, and behavioural promise before
  choosing a principle. Principles can pull in different directions.
- **SDP-SOL-070:** a function or small module can be a useful boundary. Protocols describe
  shapes; an inheritance tree is not a certificate of correct behaviour.
- **SDP-FND-110:** simplicity concerns the whole task. Similar-looking code may express
  different knowledge, while a short function may conceal expensive coupling.

## 2. Real problem and forces

Our synthetic exporter reads names and emits bracketed uppercase lines. The old function
already accepts an output callable, which is enough to substitute an in-memory recorder
for a device. Do not add a new interface to solve a seam that already exists.

The next real requirement is a finite preview with the same representation rules and no
output writes. Copying those rules risks drift. Extracting one pure formatting operation
helps both callers. A plugin loader, registry, base class, and factory are not required.

The difficult constraint is compatibility: names arrive through an iterable, which may
perform work or fail between items. Output can also fail after a prior line was saved.
Moving all validation ahead of all writes changes these interactions.

## 4. Formal definition and limits

Refactoring changes internal structure while keeping observable behaviour stable. A new
feature or corrected result is a behaviour change even when bundled with better structure.
Keep those steps distinguishable in tests and review.
[Fowler: definition of refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html).

Here, **characterization tests** record what the existing program does at a selected
boundary. A recorded quirk is evidence of current behaviour, not a declaration that it is
desirable. A **seam** is a place where a collaborator can be substituted or behaviour can
be isolated for a test or change. This example already has an output seam.

For this unit, compare an observation containing:

```text
result or exception + ordered effects + caller-visible state + consumed input
```

Two implementations may agree on the result and disagree on that observation. The chosen
boundary matters: line content may be public while a private helper's call count is not.
The probe explicitly makes source reads and writes observable; it does not require every
application to freeze all internal scheduling.

### Critique each principle without turning it into a slogan

| Principle | Useful concern | Overapplication or limit | Better judgment |
|---|---|---|---|
| SRP | Separate changes driven by different responsibilities. | “One method per class” fragments a coherent operation; responsibility depends on context. | Identify who requests each change and which rules must change together. |
| OCP | Protect a caller from a known kind of variation. | No design is closed against every future change; universal extension hooks become a framework. | Support a concrete variation and keep other edits ordinary. |
| LSP | A replacement must keep the client's behavioural promises. | A type hierarchy or type-checker success does not establish all promises. | Test results, failures, mutation, and ordering where clients depend on them. |
| ISP | A client should depend only on capabilities it needs. | Atomizing every operation loses meaningful concepts and increases wiring. | Group operations that form a coherent client capability. |
| DIP | Policy should not be controlled by unstable implementation details. | An interface for every helper adds navigation without isolating volatility. | Protect an actual policy boundary; direct calls remain reasonable elsewhere. |

These are applications and professional judgments, not alternative formal definitions.
The [prerequisite's definitions and original sources](../SDP-SOL-060-solid-interactions-tensions-and-trade-offs/README.md#4-formal-definitions-and-diagnostic-questions)
remain useful. SOLID alone does not establish business correctness, a transaction boundary,
security, good data modelling, latency, or a deployment strategy.

Sandi Metz describes how preserving an unsuitable shared abstraction can accumulate
caller-specific parameters and conditions. Separating the callers can reveal which rules
actually belong together. This is a reason to inspect the shared knowledge, not a ban on
reuse. [Metz: The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction).

## 5. Participants and responsibilities

| Participant | Responsibility | What it must not assume |
|---|---|---|
| Caller | Supply names and choose the output operation. | A failed call means no effect occurred. |
| Source iterable | Yield the next name or expose its failure. | Every consumer reads the entire source. |
| Export function | Preserve the public sequence and successful count. | Validation or buffering is automatically a transaction. |
| `format_name` | Keep the existing per-name rule. | It may silently trim, reject, or deduplicate more values. |
| Output callable | Attempt to store one formatted line. | Its exception proves the line was not stored. |
| Characterization harness | Capture the relevant observable boundary. | Passing examples prove exhaustive equivalence. |

## 6. Collaboration and execution flow

```text
legacy / extracted: read Mira -> emit [MIRA] -> read empty -> ValueError
already saved:      [MIRA]

eager rewrite:      read Mira -> read empty -> ValueError
already saved:      nothing
```

### How to read this visual

Read each row as event order. “Emit” combines an attempted call and its successful save
in this particular case. The second input is an empty string.

### Key insight

The same `ValueError` can leave different external state.

### Simplification or limitation

This condenses a literal trace from our in-memory probe. It is not a distributed transaction
or CPython memory diagram. Another sink may fail before or after an effect.

Try the [interactive behaviour comparison](visuals/behaviour-comparison.html), then read its
[reading guide](visuals/README.md). Select both successful and failing scenarios; compare
the final outcome with the sequence of events.

## 7. Before-pattern code and concrete pain

The complete baseline is preserved in [name_export.py](examples/name_export.py):

```python
def export_legacy(names, emit):
    count = 0
    for name in names:
        if name == "":
            raise ValueError("empty name")
        emit(f"[{name.upper()}]")
        count += 1
    return count
```

This is appropriate for the original requirement. The preview requirement introduces a
second caller of the representation rule. It does not introduce independently supplied
format plugins or a family of shared algorithms.

## 8. Minimal Pythonic implementation

Extract `format_name` as shown in the notebook core. Then change just the loop body:

```python
def export_refactored(names, emit):
    count = 0
    for name in names:
        emit(format_name(name))
        count += 1
    return count
```

Run the same characterization tests against both functions. Only after establishing that
boundary should the new `preview_names` operation reuse the formatting rule. The preview
materializes a finite result and has its own tests; it is a separate feature.

The helper earns its place because there are two real consumers of one rule. It is not a
mandatory split merely because the original function did two kinds of work.

## 9. Typed boundary and production concerns

The runnable source uses the following public signature on both export implementations:

```python
from collections.abc import Callable, Iterable


def export_refactored(names: Iterable[str], emit: Callable[[str], None]) -> int:
    count = 0
    for name in names:
        emit(format_name(name))
        count += 1
    return count
```

Its promises remain precise: reject only an empty string, preserve order and duplicates,
preserve surrounding whitespace, emit once per accepted item, propagate errors, do not
retry, and stop consuming after failure. The count is returned only on complete success.
A successful callback return does not by itself promise durable storage.

The caller owns the source and sink lifecycle. The exporter neither opens nor closes them.
If production needs cancellation, buffering, durability, or a connection owner, specify
that contract before introducing the corresponding structure. The current type signature
cannot express all of those promises.

## 10. Simpler alternatives and the cost of abstraction

| Design | What supports it here | Cost or reason to reject it |
|---|---|---|
| Keep the original function | One format, one caller, no current pain. | Preview would duplicate the same rule. |
| Extract one ordinary helper | Two actual consumers of one representation rule. | An extra name to navigate, justified by shared meaning. |
| Pass a formatting callable | Independent formats really vary at this boundary. | An unnecessary configuration decision for the current fixed format. |
| Use a small Protocol | A caller needs a coherent named capability. | Does not add value to the one fixed formatting operation here. |
| Use an ABC with shared hooks | An owned family genuinely shares an algorithm. | No such family exists in this example. |
| Add a rule, factory, and service | The runnable overbuilt version shows the mechanics. | More construction and navigation, with no current variation to contain. |

The [overbuilt implementation](examples/name_export.py) passes the same behavioural tests.
That is intentional: needless abstraction need not be functionally broken. Conversely,
one production implementation can justify a boundary for testing, ownership, or an unstable
external dependency. Count reasons and costs, not classes or implementations.

Deferring speculative features is compatible with investing in tests and refactoring.
Fowler explicitly distinguishes those enabling practices from unused future capabilities.
[Fowler: Yagni](https://martinfowler.com/bliki/Yagni.html).

## 11. Refactoring path

1. Name the immediate change and identify existing callers and entry points.
2. Capture representative success, edge, and failure cases at those boundaries.
3. Mark uncertain behaviours for a product or contract decision; do not silently normalize them.
4. If tests are blocked by I/O, use an existing seam or introduce one narrow dependency seam.
5. Make one structural edit. Keep the public API, data interpretation, and error policy stable.
6. Rerun checks and inspect the diff. A new failure may expose a missing contract, not a bad test.
7. Add the approved requirement with separate assertions and a distinguishable change.
8. Remove now-unused wrappers only after checking their callers and extension contracts.
9. Stop when the known change is supported and the boundary is understandable.

The worked example is stored as named variants for comparison, not as a claim that each
was historically deployed. In a real repository, small commits make each step reviewable.

## 12. Realistic backend use case and migration

Consider a long-lived export endpoint used by a scheduled consumer. Its exact delimiter,
empty-value spelling, field order, and failure response may be part of that consumer's
contract even when nobody wrote them down. A new interactive consumer has different needs.

Keep the old entry point while isolating its interpretation and side-effect boundary.
Use synthetic or appropriately sanitized fixtures and a recorder to compare the candidate.
Where a gradual rollout is justified, select the path at one controlled entry point, define
who owns that temporary switch, and set a removal condition.

Compare mismatch counts, error categories, input sizes, and partial-effect reports for the
relevant cases. Do not blindly run old and new writers against a live destination: a shadow
comparison should suppress candidate side effects or use an isolated destination. Prepare
rollback for both code and data compatibility. Reverting code does not undo saved records.
These are engineering considerations, not a deployment performed by this lab.

## 13. Failure scenario

A reviewer moves formatting into a tuple before writing because it looks more separated.
For valid names, saved lines and return count match. For a late empty name, the old program
has already saved a prefix and the eager program has saved nothing. For a writer failure,
the eager program has consumed names the old program never requested.

The [experiment](experiments/EXP-01-observable-trace/README.md) also includes a sink that
saves a line and then raises. The exporter cannot infer the saved state from the exception
alone. An automatic retry could repeat an effect; any retry policy needs a separate contract.

## 14. Testing strategy

| Test type | What it contributes | Limitation |
|---|---|---|
| Fixed characterization case | An independently written expected result, error, or effect. | Covers selected cases only; old behaviour may be undesirable. |
| Differential comparison | Old and new observations match for the same input. | Both implementations may share a defect. |
| Property-based comparison | Broader generated successful inputs, including Unicode and duplicates. | Does not replace explicit failure and boundary oracles. |
| Contract failure test | Prefix effects, no retry, remaining iterator tail, and exception identity. | A synthetic recorder is not a real device integration. |
| Production integration check | Actual encoding, client parsing, and resource behaviour. | Requires the real supported environment; not run here. |

Prefer stable results and boundary events over assertions about private helper names,
factory counts, or exact internal class structure. Do not normalize a captured snapshot
so aggressively that meaningful ordering, whitespace, or failures disappear.

For legacy Python imports, patch the name where the code under test looks it up. Patching
the module that originally defined an object may not affect an already imported alias.
[Python: where to patch](https://docs.python.org/3.14/library/unittest.mock.html#where-to-patch).
This unit's worked example needs no patching because it already accepts a callable.

## 15. Observability and debugging

Record the first differing event, not just “old failed/new failed.” Ask whether a source
was advanced, a sink was called, and an effect was committed. Distinguish an attempt from
an acknowledgement. Real diagnostics should avoid logging private raw payloads just because
the synthetic probe can safely print its names.

In Python, a `for` loop requests an item and executes its body before requesting the next
item. Moving work into a fully consumed tuple changes that schedule in our program.
[Python language reference: the for statement](https://docs.python.org/3.14/reference/compound_stmts.html#the-for-statement).
This is language-level execution reasoning, not a CPython optimization claim.

## 16. State safety and resource boundaries

Neither an extracted helper nor a list of prevalidated inputs creates an atomic write.
The probe is synchronous and single-threaded. Real shared state, concurrent consumers,
cancellation, and transaction isolation require their own policies and tests.

Do not change who closes an injected resource during cleanup. Moving from streaming to
buffering also retains all formatted values before writing and is unsuitable for an
unbounded source. No timing or memory benchmark was performed; fewer classes does not
establish a runtime speed improvement.

## 19. Related units and scope boundary

| Related unit | Relationship | Key difference |
|---|---|---|
| [SDP-SOL-060](../../../CURRICULUM.md#sdp-sol-060) | Prerequisite | Diagnoses tensions among principles. |
| [SDP-SOL-070](../../../CURRICULUM.md#sdp-sol-070) | Prerequisite | Chooses Python mechanisms for a justified boundary. |
| [SDP-FND-110](../../../CURRICULUM.md#sdp-fnd-110) | Prerequisite | Provides simplicity and collaboration heuristics. |
| [SDP-REF-080](../../../CURRICULUM.md#sdp-ref-080) | Later depth | Focuses on fragile mocks and meaningless interfaces. |
| [SDP-REF-090](../../../CURRICULUM.md#sdp-ref-090) | Later depth | Focuses on removing factories and pattern soup. |
| [SDP-REF-100](../../../CURRICULUM.md#sdp-ref-100) | Later depth | Expands characterization and incremental refactoring practice. |
| [SDP-PYT-010](../../../CURRICULUM.md#sdp-pyt-010) | Next planned unit | Studies functions, closures, and callable objects in depth. |

This unit supplies judgment and one bounded migration exercise. It does not initialize any
later unit or duplicate the full refactoring curriculum.

## 20. When to use this approach

Use it when a concrete change is blocked by uncertain legacy behaviour, scattered edits,
or abstractions that now serve incompatible callers. Start close to the requested change.
A small seam can be worthwhile even before adding a second implementation.

## 21. When not to expand the refactoring

Leave stable code alone when the proposed cleanup has no clear benefit for a current
change. Avoid a broad rewrite during incident containment or when the relevant behaviour
cannot yet be observed. A necessary emergency bug fix may change behaviour first, but
make that intent explicit and add the smallest useful regression check.

## 22. Common misuse and overengineering

| Misuse | Why it fails | Better move |
|---|---|---|
| “Every concrete class needs an interface.” | Adds shape without demonstrating a useful boundary. | Name the client and volatility being isolated. |
| “Every shared line belongs in one abstraction.” | Textual similarity may hide independently changing knowledge. | Inspect each caller's meaning and allow limited duplication. |
| “A single implementation makes an interface pointless.” | Ignores testability, ownership, and unstable external details. | Evaluate the boundary's actual job. |
| “Fix all quirks while extracting.” | Makes compatibility regressions hard to distinguish from intended changes. | Separate structural and behavioural steps. |
| “Green tests justify a rewrite.” | Missing observations remain missing. | Add boundary cases and keep edits small. |
| “Validate everything first for safety.” | Changes streaming and may still allow partial writes. | Specify the intended contract before changing timing. |
| “Delete every old API after moving its code.” | Unknown callers or extensions may still use it. | Inventory callers; use a deliberate compatibility period if needed. |

## 23. Practice and interview preparation

Start the [workshop report lab](practice/README.md). It is intentionally different from
the streaming example: two report clients share configurable machinery but have different
reasons to change. Baseline tests pass before the design exercise is attempted.

During an interactive interview, ask one question at a time. Begin with:

**“A rewrite returns exactly the same output for every successful fixture. What else would
you inspect before calling it a safe refactoring?”**

After the answer, probe one missing part: failure effects, input consumption, state,
caller compatibility, or adequacy of the fixtures. Do not recite all follow-ups at once.

Weak answers count classes, name five principles without a concrete force, assume tests
prove requirements, or equate an exception with rollback. A strong answer identifies the
observer, one risky case, a small step, a rejected alternative, and a stopping condition.

For senior transfer, ask how the answer changes for a public library with third-party
subclasses, an external writer with uncertain acknowledgements, or a read-only batch job.
Removing an internal wrapper and removing a public extension API are different decisions.

## 24. Closed-book revision cues

Reconstruct the essential workflow and the late-error trace. Explain why the eager rewrite
is incompatible here, when buffering could instead be an intentional design, and why a
single implementation may still deserve a boundary. Then defend one abstraction to remove
and one to retain in a new scenario. These are future retrieval prompts, not completed evidence.

## 25. Vocabulary and professional English

### Incremental

| Item | Content |
|---|---|
| Pronunciation | in-kruh-MEN-tuhl |
| Simple English meaning | Done in small steps. |
| Hindi cue | छोटे-छोटे चरणों में |
| Design meaning | Each step is narrow enough to inspect and verify. |

Natural examples: “We made incremental progress.” “The rollout is incremental.” “An
incremental plan reduces the size of each decision.” **Interview:** “I would use incremental
refactoring around the public boundary.” **Engineering discussion:** “Can we separate this
incremental extraction from the output change?”

### Speculative

| Item | Content |
|---|---|
| Pronunciation | SPEK-yuh-luh-tiv |
| Simple English meaning | Based on an uncertain future possibility. |
| Hindi cue | अनुमान पर आधारित |
| Design meaning | Added for a variation that is not yet an actual requirement. |

Natural examples: “That estimate is speculative.” “The proposal depends on speculative
demand.” “We should label speculative assumptions.” **Interview:** “The plugin hierarchy
is speculative for this fixed-format caller.” **Engineering discussion:** “What current
requirement pays for this speculative extension point?”

## 26. Python Mastery references

`PYTHON_REFERENCES.md` has no direct mapping for SDP-SOL-080. Do not invent one. The following
approved mappings support prerequisite mechanisms when needed; they are navigation links,
not external lessons reviewed as part of this initialization:

- Via **SDP-FND-080**, [PY-TST-020 — Pytest fundamentals and fixtures](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-tst-020)
  and [PY-TST-040 — Test doubles, mocking, and patching boundaries](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-tst-040):
  assert public outcomes, use a small recorder, and patch the looked-up name only when needed.
- Via **SDP-FND-100**, [PY-MOD-010 — Modules, packages, and executable modules](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-mod-010):
  distinguish an import dependency from a runtime call.

All executable examples use Python 3.11-compatible syntax. The next planned unit,
**SDP-PYT-010**, has its own exact callable and closure prerequisites; it remains uninitialized.

## 27. Authoritative sources

Read for this unit on 2026-08-30; explanations, examples, and visuals are original.

1. [Martin Fowler: Definition Of Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) — structure versus observable behaviour.
2. [Sandi Metz: The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction) — independently changing callers and unsuitable shared abstractions.
3. [Martin Fowler: Yagni](https://martinfowler.com/bliki/Yagni.html) — speculative capability versus keeping code changeable.
4. [Python 3.14 language reference: for statement](https://docs.python.org/3.14/reference/compound_stmts.html#the-for-statement) — iteration and execution of the loop body.
5. [Python 3.14 language reference: Boolean operations](https://docs.python.org/3.14/reference/expressions.html#boolean-operations) — zero, `None`, and the value returned by `or` in the practice baseline.
6. [Python 3.14 unittest.mock: where to patch](https://docs.python.org/3.14/library/unittest.mock.html#where-to-patch) — name lookup at a legacy test seam.

See the [maintainer validation record](VALIDATION.md) for actual checks and limits. Material
approval is separate from learner evidence. The practice remains unsolved; no learner review,
recall, retention, or completion is inferred from publishing these files.
