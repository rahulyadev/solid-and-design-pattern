# SDP-STR-060 — Bridge

## Physical Notebook Core

### Problem or change pressure

A stock report starts as CSV. Then the team needs a shortage report and a JSON consumer. Encoding
rules should not be copied into each report, and business selection should not be copied per format.

### One-sentence mental model

> Let one family decide what work means and a second family supply how that work is represented.

### One essential visual

```text
                         holds an Encoder reference
InventoryReport ──┐
                  ├── Report.render(items) ── encode(Table) ──┬── CsvEncoder
ShortageReport ───┘         │                                └── JsonEncoder
                     project(items)
                     report-specific rows

                         CSV              JSON
Inventory            all stock          all stock
Shortage             deficits only      deficits only
```

### How to read this visual

Read left to right for delegation. Choose one report and one encoder; the matrix shows all four
supported pairs. `project` is dispatched on the report; `encode` is dispatched on its collaborator.

### Key insight

There are two reasons to change. New report meaning should reuse encoders; a new encoding should
reuse report meaning. The shared Table contract makes that possible.

### Simplification or limitation

Conceptual dependencies and supported combinations, not memory layout or a rendered browser view.
A future chart or streaming consumer may exceed the Table contract. Four valid pairs do not prove
that every imaginable pair is valid.

### Governing rules or invariants

1. Identify two real variation dimensions and a semantic contract between them.
2. The report selects rows; the encoder preserves ordered cells and produces a complete artifact.
3. Configuration selects a pair; substitution must preserve meaning, errors and ownership.

### Minimal Python example

```python
from collections.abc import Callable


def report(
    values: tuple[int, ...], select: Callable[[int], bool], encode: Callable[[tuple[int, ...]], str]
) -> str:
    return encode(tuple(value for value in values if select(value)))


assert report((0, 3, 8), lambda n: n < 5, repr) == "(0, 3)"
assert report((0, 3, 8), lambda n: True, repr) == "(0, 3, 8)"
```

This is the separation in callable form. It has no configuration parser, labels, bounds or media
type. Functions may be the final design when both responsibilities stay this small.

### One common misconception

**Mistake:** A class holding an interface reference is automatically Bridge.

**Correction:** That structure occurs in many designs. Bridge is justified by two independently
changing families whose behavior can be combined through a stable contract.

### Important trade-offs

- Composition removes duplicated combination logic; the compatibility and test matrix still exists.
- A small seam helps extension. An invented universal interface creates coupled exceptions instead.

### Interview-revision cues

- Name the two dimensions and one concrete change on each side.
- Trace a request through both participants and state what must remain unchanged.
- Reject the pattern when a function or data option handles the actual requirement.

## Unit metadata

| Field | Value |
|---|---|
| Domain | Structural patterns |
| Curriculum | [SDP-STR-060](../../../CURRICULUM.md#sdp-str-060) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Separate two independently varying dimensions before inheritance creates a Cartesian product of subclasses. |
| Hard prerequisites | [SDP-FND-050](../../../CURRICULUM.md#sdp-fnd-050), [SDP-SOL-020](../../../CURRICULUM.md#sdp-sol-020) |
| Soft prerequisites | None declared in the canonical entry |
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

Frequency classifications are curriculum judgments, not measured prevalence. Generated material
and maintainer tests do not prove learning; the tracker remains Not started.

## 1. Simple explanation and the minimum prerequisite bridge

Imagine two questions: “Which stock facts should this report show?” and “How does this consumer
want those facts encoded?” Inventory and shortage reporting answer the first. CSV and JSON answer
the second. A shortage report need not know how commas are quoted. A JSON encoder need not know
what a shortage means.

[SDP-FND-050](../../../CURRICULUM.md#sdp-fnd-050) supplies the mechanics: an object can hold another
object and call its methods; holding it does not mean being a subtype of it. Inheritance is useful
only where a behavioral substitution makes sense.
[SDP-SOL-020](../../../CURRICULUM.md#sdp-sol-020) supplies the judgment: protect demonstrated variation
behind a stable seam. It does not mean every file is closed to every future edit. Both prerequisite
artifacts are Approved but learning is Not started, so recall these ideas before deeper practice.

## 2. The simplest design and the actual change pressure

With one report and one format, write a direct function:

```python
import csv
import io


def stock_csv(items: tuple[tuple[str, int], ...]) -> str:
    with io.StringIO(newline="") as stream:
        writer = csv.writer(stream, lineterminator="\r\n")
        writer.writerow(("sku", "on_hand"))
        writer.writerows(items)
        return stream.getvalue()


assert stock_csv((("clip", 3),)) == "sku,on_hand\r\nclip,3\r\n"
```

This is a sound answer to the current problem. A boolean option for including a column can also
be enough. Do not create a class family for one formatting flag.

The changed requirements are stronger: a report for every item with on-hand and reorder values,
and a shortage report containing only below-threshold items with their deficits. Each report is
required by both a CSV consumer and a JSON consumer. Business selection and wire syntax now have
independent requesters and separate acceptance criteria.

An inheritance design that places both choices in concrete leaves can grow like this:

```text
Report
├── InventoryCsvReport       copies inventory projection + CSV machinery
├── InventoryJsonReport      copies inventory projection + JSON machinery
├── ShortageCsvReport        copies shortage projection + CSV machinery
└── ShortageJsonReport       copies shortage projection + JSON machinery
```

### How to read this visual

Each leaf hardwires one pair. Compare the first two for duplicated business rules, then first and
third for duplicated encoding. The drawing describes the tempting design, not code in this repo.

### Key insight

With R report meanings and F encodings, this naive design needs R×F leaves. Composition can express
R report implementations plus F encoders, with shared contracts and configuration overhead.

### Simplification or limitation

This is a source-structure count, not measured complexity, runtime speed, or a rule that every
inheritance design duplicates code. Shared helpers can already remove duplication. Pairwise
compatibility still needs review, and the four supported combinations here are all tested.

If inheritance leaves merely call two extracted helpers, the helpers already contain the useful
separation. Delete unnecessary leaves instead of building a framework around them.

## 3. GoF intent and precise terminology

Bridge separates a client-facing abstraction from the implementing collaborator it uses, allowing
both sides to change independently. “Implementation” here means that collaborator, not just the
concrete subclass of the client-facing abstraction. Shalloway and Trott explain this distinction
while discussing the GoF intent in their [publisher-hosted introduction](https://www.informit.com/articles/article.aspx?p=1398603).
This note uses their explanation; it does not claim direct access to the complete GoF chapter.

The GoF participant names are **Abstraction**, **Refined Abstraction**, **Implementor**, and
**Concrete Implementor**. Our design uses a small shared report workflow, report-specific
projections, and a structural encoding contract. The authored example and diagrams are original.
The implementor interface only needs to support the variations being built; designing for every
conceivable variation is unnecessary, as the authors emphasize in their
[retrospective](https://www.informit.com/articles/article.aspx?p=1398603&seqNum=5).

## 4. Participants, responsibilities and collaboration

| Participant | This example | Owns | Must not own |
|---|---|---|---|
| Client / composition root | Demo or `make_report` caller | Select a supported report/format pair | Duplicate projection or encoding |
| Abstraction | `Report` | Validate a request, project it, delegate encoding once | CSV/JSON choices |
| Refined Abstraction | `InventoryReport`, `ShortageReport` | Column and row meaning | Quoting, syntax or delivery |
| Implementor | `Encoder` Protocol | Contract for complete text artifact production | Stock business rules |
| Concrete Implementor | `CsvEncoder`, `JsonEncoder` | Correct encoding of all Table cells | Filtering or aggregate decisions |
| Boundary values | `StockItem`, `Table`, `Artifact` | Bounded data and explicit result | Registries, transport or lifecycle management |

```text
make_report("shortage", "json") → ShortageReport(JsonEncoder())
client calls render((clip: 3/5, tray: 8/8))
  1. Report.render validates count and unique SKUs
  2. ShortageReport.project selects clip and calculates 5 - 3 = 2
  3. Table carries columns (sku, deficit), rows ((clip, 2),) as text
  4. JsonEncoder.encode receives that Table exactly once
  5. Artifact(application/json, complete body) returns to the client
```

### How to read this visual

Read in numeric order. Slashes in stock values mean on-hand/reorder quantities, not division.
The final body is a JSON object with `columns` and `rows`; the example demo prints it.

### Key insight

`render` dispatches to the report's projection and then to a separately selected encoder. Those
are ordinary method calls. There is no automatic pattern detection or dependency injection engine.

### Simplification or limitation

Sequential successful flow only. Validation or projection failure prevents encoding. An encoder
exception propagates unchanged; there is no fallback, retry, delivery, network or background job.

## 5. The bounded typed implementation

Read [bridge.py](examples/bridge.py), then run [the demo](examples/run_bridge_demo.py).
The report ABC shares a real workflow. The encoder Protocol needs only one operation; encoder
classes do not inherit it. `@final` communicates that typed subclasses should retain `render`'s
workflow. The public request API is `render`; `project` is the subclass extension hook and direct
calls to it do not perform `render`'s duplicate/count checks.

```python
from bridge import CsvEncoder, InventoryReport, JsonEncoder, ShortageReport, StockItem

items = (StockItem("clip", 3, 5), StockItem("tray", 8, 8))
assert InventoryReport(CsvEncoder()).render(items).body == (
    "sku,on_hand,reorder_at\r\nclip,3,5\r\ntray,8,8\r\n"
)
assert ShortageReport(JsonEncoder()).render(items).body == (
    '{"columns":["sku","deficit"],"rows":[["clip","2"]]}'
)
```

### Semantic contract beyond the signature

| Boundary | Promise / decision | Enforcement or limitation |
|---|---|---|
| Stock quantities | Plain integers in 0..1,000,000; bool rejected | Value validation at construction |
| SKU | Nonblank, at most 40 characters; retain original text | Construction check; whitespace is not normalized |
| Request | Typed tuple of StockItem; at most 100; unique exact SKUs | `render` checks size and duplicates; no untrusted deserializer |
| Inventory projection | All input items, same order; explicit quantity strings | Behavioral tests |
| Shortage projection | Only on-hand strictly below reorder; positive deficit | Equality is not a shortage; tested |
| Table | 1..4 distinct nonblank columns; rectangular text rows; at most 100 rows; 80 characters per cell | Value validation; tuple/string types are the typed caller's responsibility |
| Encoder | Preserve every cell and its order, duplicates and empty cells; keep schema for empty input | Common contract tests; Protocol cannot prove semantics |
| Output | Fresh complete Artifact, explicit media type, body is text | Built-in implementations; no file or byte encoding promised |
| Failure | No partial Artifact returned, no retry or fallback; original exception propagates | Tested; collaborator side effects cannot be rolled back |
| State / ownership | Report borrows encoder; built-ins keep no request state | No close, implicit replacement or per-report global registry |

Both built-in encoders accept every valid Table, so all four current pairs are valid. `make_report`
uses a closed string/enum vocabulary: unknown names fail with ValueError. Direct constructors are
open to other typed encoders; adding a config option intentionally edits the composition root.
A registry is unnecessary for four choices.

The code validates values needed for this example, not arbitrary Python object forgery. Type hints
are not an input security boundary. Frozen dataclasses reject ordinary field reassignment but do
not recursively freeze arbitrary referenced collaborators; see the
[dataclass frozen-instance contract](https://docs.python.org/3.14/library/dataclasses.html#frozen-instances).
Tuples containing frozen values support this example's request discipline. Passing a list from
unchecked code or bypassing setters is outside it.

### Why types and behavior need separate checks

[The typing specification](https://typing.python.org/en/latest/spec/protocol.html#assignability-relationships-with-other-types)
uses structural assignability: compatible members suffice without explicit inheritance. Tests admit
an external encoder and reject missing `encode`, wrong return type and an extra required argument.
They also reject encoder field replacement, a nonexistent `close`, a mutable-list request, and
overriding the final render workflow.

Yet an encoder that returns a valid empty JSON document for a nonempty Table type-checks. It breaks
cell preservation. The semantic-liar test demonstrates that the client trusts this promise and does
not secretly decode every result. Admission of external code therefore needs contract testing and
review; a Protocol annotation is not certification.

Python 3.12 changed runtime-checkable Protocol attribute lookup to `inspect.getattr_static` and
freezes the inspected member set. Runtime checks still do not validate method signatures. We do
not use runtime Protocol checks, so those differences do not govern this design. `@final` also
has no runtime override enforcement. These are [typing-library contracts](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable),
not Bridge mechanics.

Python 3.14 adds deferred annotation evaluation; `bridge.py` retains the Python 3.11-compatible
`from __future__ import annotations` behavior. Our application code performs no annotation introspection,
so it needs no version-specific dispatch path. See the official
[Python 3.14 annotation change](https://docs.python.org/3.14/whatsnew/3.14.html).
The source uses syntax supported by Python 3.11. Actual runtime and typing results are recorded in
[VALIDATION.md](VALIDATION.md); no CPython memory or GIL assumptions are required.

## 6. A simpler Python form, and an unnecessary abstraction

An encoder object has one method and no state. Passing its bound method as a callable removes the
need for an encoder interface in very small programs:

```python
from collections.abc import Callable
from bridge import Artifact, CsvEncoder, Table


def render_table(table: Table, encode: Callable[[Table], Artifact]) -> Artifact:
    return encode(table)


artifact = render_table(Table(("sku",), (("clip",),)), CsvEncoder().encode)
assert artifact.body == "sku\r\nclip\r\n"
```

Two plain functions, `project(items)` and `encode(table)`, may also replace the report hierarchy.
Keep classes when a coherent report API, meaningful variants and shared request checks make them
clearer. Keep configuration as data when variants differ only by a constant; independence does not
require two inheritance trees. The ABC in the worked example is one justified implementation,
not part of the definition of Bridge in Python.

An overengineered design would introduce `UniversalReportFactory`, a plugin manager, five abstract
bases and capability flags for formats no consumer needs. An incorrect seam would take
`encode_inventory`, `encode_shortage` and `encode_future_chart`: every report addition would then
force every encoder to change. Or `encode(table, shortage=True)` would smuggle business selection
back across the boundary. Put selection in the projection and test that it stays there.

## 7. Independence, invalid pairs and contract evolution

Ask for evidence: can a new report be expressed entirely as another valid Table? Can a new encoder
preserve that Table without inspecting report type? The test suite adds a zero-stock report using
both existing encoders and a third encoder using both existing reports. These are bounded extension
witnesses; they do not prove arbitrary future extension.

Independence is false when business meaning depends on the output: a chart consumer needs numeric
series and units, while this Table deliberately stores text. A signed audit export might require
canonical bytes and exact column order beyond what a general display export promises. Neither is
currently a valid plug-in under the existing contract just because it can implement `encode`.

Choose one concrete response: reject the unsupported combination during configuration, introduce
a separate capability contract and constrained pairing, or revise the shared value model and
migrate consumers. Do not silently omit columns, guess numeric types or return “unsupported” as a
successful Artifact. A matrix full of special cases is evidence that the chosen dimensions or
boundary need reconsideration. Independence always holds relative to a stated contract.

## 8. Refactoring path and backend transfer

1. Characterize the existing direct report, including ordering and escaping.
2. Write the actual two report and two encoding requirements. Challenge speculative variations.
3. Extract the stable Table representation and move business selection into projections.
4. Extract encoders with a single contract; compare functions before committing to classes.
5. Compose pairs explicitly and remove duplicated combination subclasses.
6. Run contract tests on every current pair and add one change on each dimension.
7. Revisit validation, failure and lifecycle ownership before connecting external resources.

In a backend, an inventory export endpoint could map validated request options to `make_report`,
load an immutable stock snapshot in the application layer, call `render`, then construct a response
from the media type and body. Database consistency, authentication and delivery belong outside this
bounded example. Bridge does not choose transaction isolation or certify a consistent snapshot.

This CSV is a text interchange format tested with Python's csv reader. It is not a spreadsheet
export safety contract; adding spreadsheet interpretation requirements would need separate policy.
No actual customer system, web framework or deployment is involved.

## 9. Errors, observability, state and resource lifetime

A subtle production failure is a JSON encoder that helpfully drops rows it considers “uninteresting.”
Reports disagree across formats although the types pass. Detect it by decoding formats to the same
Table-shaped observation in contract tests. Contain it by rejecting that implementor during review;
do not add type-based workarounds to every report.

Record the selected report kind and output format at the application boundary, plus row counts and
exception type where appropriate. Avoid logging raw stock data. A failed projection never reaches
the encoder; a failed encoder is called once and its exception is preserved. The
[controlled probe](examples/matrix_probe.py) makes the real delegation count observable.

Built-in encoders create only local temporary values. CsvEncoder owns and closes its StringIO
within the call; it returns the completed text. Report does not close its borrowed encoder. If an
implementor later wraps a resource, the creator must own its lifetime explicitly and keep it usable
for the whole report operation. That is a new contract to design, not a behavior already tested.

A frozen Report can still hold a mutable encoder, as the recording test double shows. Sharing that
collaborator across requests needs a separate concurrency policy. The unit does not prove thread
safety, cancellation behavior, async safety or safe live replacement. Prefer a new configured
report object when selection changes; `@final` and frozen fields are not concurrency primitives.

## 10. Performance and standard-library details

For the supplied reports, projection scans N input items and builds at most N output rows. For
fixed columns, built-in encoding work follows the amount of text produced; whole tables and whole output
bodies remain in memory. Boundaries of 100 items and 80 characters per cell keep this a small
in-memory teaching example. These are design/algorithm observations, not measured speedups.

Bridge removes no required report calculation and does not turn R×F combinations into R+F tests.
Streaming, very large exports, I/O, backpressure and caching are outside scope. Measure the actual
bottleneck before adding a streaming implementor; streaming would change failure and lifetime
semantics from those of an all-at-once Artifact.

CSV uses `csv.writer` and an explicit CRLF record terminator instead of hand-joining cells. The
[Python 3.11 csv documentation](https://docs.python.org/3.11/library/csv.html#csv.writer)
explains the writer and file-like boundary. Tests round-trip commas, quotes, CR/LF, empty cells and
Unicode through the reader. This is format preservation, not arbitrary spreadsheet behavior.
JSON uses `json.dumps(..., ensure_ascii=True)`; non-ASCII text is escaped in the serialized body
and recovered by decoding. Its contract is text, not encoded bytes, as described in the
[Python 3.11 JSON documentation](https://docs.python.org/3.11/library/json.html#json.dumps).

## 11. Testing and controlled observation

| Check | What it establishes | Limit |
|---|---|---|
| Four report/format combinations | Current projections survive both serializations | No proof about future formats |
| Shared encoder contract cases | Order, duplicates, special text, empty schema, repeatability | Targeted values plus 40 generated cases per encoder; trusted collaborators |
| Boundaries and failures | Invalid values fail; no encoding after projection failure; no retry | No transactional side-effect rollback |
| Extension witnesses | One added report and encoder need no opposite-side edits | Shared Table contract stays unchanged |
| Static positive/negative clients | Supported call surface and intended diagnostics | Semantics remain outside type checking |
| Starter characterization | Existing walking-guide behavior remains runnable | New lab requirements remain unsolved |

The probe fixes two stock records and changes report policy and encoder. Hypothesis: each pair
encodes exactly once; row count changes only with report selection. It counts actual `encode`
invocations through a recording collaborator. It does not count hypothetical constructors or
measure timing. Commands, environment, actual output and limitations are in [VALIDATION.md](VALIDATION.md).

The matrix in the notebook is conceptual text. Its row-count/delegation observations are executable
assertions. No browser rendering is claimed; no blocked local URL is worked around.

## 12. Nearby designs: distinguish by the pressure

| Design / reference | Main pressure | Boundary relative to Bridge |
|---|---|---|
| [Adapter — SDP-STR-010](../../../CURRICULUM.md#sdp-str-010) | An existing interface does not fit a desired one | Translation at a boundary; may implement one side of a Bridge |
| [Strategy — SDP-BEH-010](../../../CURRICULUM.md#sdp-beh-010) | Replace an algorithm or policy for a context | Bridge argues for two evolving dimensions; the same code shape can support either account |
| Dependency injection | Supply a collaborator from outside | Construction/wiring mechanism; it does not establish two variation families |
| Ordinary composition | An object uses another object | Broad mechanism; Bridge is a specific design intent using it |
| [Abstract Factory — SDP-CRE-020](../../../CURRICULUM.md#sdp-cre-020) | Select a coherent family of products | Can create compatible collaborators; this unit needs only explicit configuration |

Adapter is often used to reconcile existing interfaces and Bridge to organize variation, but timing
alone is not decisive. A refactor can introduce Bridge into an old system. Name the responsibility
and intended changes, not simply “before versus after.” These comparisons locate boundaries; the
referenced units retain their own curriculum scope.

## 13. When to use it, when to reject it

Use it when both dimensions already vary, the combinations are useful, and a common semantic
boundary lets each side evolve without inspecting the other. This example meets that narrow test.

Reject it for a single stable report, one fixed format, variation that is only data, or two
supposed dimensions whose special cases dominate their shared behavior. Start with direct
functions or small configuration. A third independent dimension is not permission to grow another
hierarchy automatically: establish its actual coupling and ownership first.

## 14. Interview preparation and exact reasoning gaps

Use this as an interviewer queue. Ask one question, wait for the attempt, then select the smallest
follow-up; do not reveal the whole answer sequence during an interview.

| Prompt | Weak answer | Exact missing reasoning step / follow-up |
|---|---|---|
| Explain Bridge simply. | “Use composition.” | Name two changing concerns and the shared semantic boundary. |
| Why is the stock example a candidate? | “Four classes are bad.” | Show which business change and which format change should be independent. |
| Trace shortage JSON. | “Report calls interface.” | Identify where selection, deficit calculation and encoding each happen. |
| Implement the smallest form. | Start with four abstract classes. | Compare two functions and justify every retained class. |
| What does Protocol guarantee? | “Any encoder works.” | Separate compatible signatures from preservation of all ordered cells. |
| A chart encoder rejects half the reports. | Add checks in each report. | Decide whether the common data model supports charts at all. |
| How is this unlike Adapter or Strategy? | Repeat class-diagram differences. | Explain compatibility pressure versus two-dimensional change versus algorithm replacement. |
| Can reports share one encoder safely? | “Report is frozen.” | Identify mutable collaborator state, owner and concurrency contract. |
| A serialization failure occurs halfway through. | Retry automatically. | State side effects, retry ownership and what complete-result semantics promise. |
| Does R+F implementation mean R+F tests? | “Yes, fewer classes.” | The valid-pair contract matrix still needs coverage. |

Code-review exercise: an encoder branches on `isinstance(report, ShortageReport)` and removes rows.
Explain which responsibility crossed the boundary and design a test that detects the wrong output.
Refactoring exercise: characterize two duplicated pair subclasses before choosing an extraction.
Transfer exercise: a batch export needs atomic publication to external storage; identify what this
Bridge covers and which owner must provide publication and recovery semantics. These prompts are
not learner evidence or a solved version of the separate lab.

## 15. Closed-book reconstruction and evidence

Rebuild the four-pair matrix, draw the two dispatches, write the one-method contract, name a
statically valid semantic failure, and reject one case where independence is imagined.
Then attempt [the separate unsolved lab](practice/README.md).

E means explain the pressure and alternatives. I means implement and test valid behavior. D means
debug or refactor with a preserved attempt and reasoning. T means transfer to a production design,
including constraints and rejection criteria. A controlled probe does not add X to the canonical
E+I+D+T profile. Learning states require Rahul's evidence under [PROGRESS.md](../../../PROGRESS.md).

## 16. Vocabulary and professional English

| Word | Say it | Meaning here | Hindi cue |
|---|---|---|---|
| Orthogonal | or-THOG-uh-nuhl | Choices can change separately within the contract | स्वतंत्र बदलाव |
| Decouple | dee-KUP-uhl | Reduce one concern's need to know another | निर्भरता कम करना |
| Cartesian product | kar-TEE-zhun product | All pairs drawn from two choice sets | सभी जोड़ियाँ |

Natural use: “These two decisions are orthogonal within our current format contract.” “We can
decouple selection from serialization.” “The configuration matrix is their Cartesian product.”
In an interview, add a concrete example after each term rather than relying on the vocabulary.
In review, say “This format-specific branch couples the two dimensions again.”

## 17. Python Mastery references

`PYTHON_REFERENCES.md` has no direct SDP-STR-060 mapping. Its prerequisite mappings supply
[PY-OBJ-010 — Classes, instances, methods, and construction](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-010),
[PY-OBJ-020 — Properties, encapsulation, and composition](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-020),
and [PY-OBJ-030 — Inheritance, MRO, and super](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-030)
through SDP-FND-050. The minimum bridge is constructing an object, retaining a collaborator,
calling its bound method and distinguishing delegation from overriding.

For the mechanisms used in this example, the existing map links
[PY-TYP-050 — Protocols, ABCs, and structural versus nominal typing](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-typ-050)
through SDP-PYT-070 and
[PY-LIB-060 — Dataclasses, enums, types, and generated data models](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-lib-060)
through SDP-PYT-060. These are supporting bridges, not newly declared canonical prerequisites.
No Python Mastery lesson content has been copied or claimed reviewed.

## 18. Sources and material boundaries

Sources actually read: Shalloway/Trott's publisher-hosted introduction and retrospective; the Python
typing specification's Protocol member/assignability sections; Python 3.14 typing, dataclasses and
What's New annotation sections; Python 3.11 csv and json documentation. Exact links appear beside
the supported claims above. Design judgments and the synthetic example are this unit's own work.

The worked code, contract checks and maintainer results are study material. The separate lab remains
unsolved. Approved notes may be used under the [NotebookLM policy](../../../docs/NOTEBOOKLM.md);
exclude the tracker, raw attempts, source trees and validation output. No upload or license change
is performed by authoring this unit.
