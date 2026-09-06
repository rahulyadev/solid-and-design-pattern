# Validation — SDP-PYT-080

## Scope and evidence boundary

| Field | Observed value |
|---|---|
| Date | 2026-09-06 |
| Exact branch | `topic/SDP-PYT-080` |
| Initialization baseline (`INIT_START`) | `6859415b29eca216ca2a536338b8eaf670bfc466` |
| Initialization commit | `9e78aefeb815b2ad81918ae613f504b397c67bf5` |
| Evidence profile | `E+I+D+X+T` |
| Canonical runtime | CPython 3.14.7 |
| Compatibility runtime | CPython 3.11.16 |
| Artifact state during this record | Approved |
| Learning state during this record | Not started |

This record validates maintainer-authored curriculum material. It contains no learner prediction,
attempt, explanation, delayed recall, transfer, refactoring submission, or interview answer.
Therefore only artifact state advances from Absent through Draft to Approved. Rahul's learning state
remains Not started, and every learner-evidence field in `PROGRESS.md` remains `—`.

## Sources actually read

- Python 3.14 `functools` documentation for first-argument dispatch, decorator and functional
  registration, annotation inference, explicit collection registration, the `object` default, MRO,
  ABC virtual subclasses, `dispatch()`, read-only `registry`, `singledispatchmethod`, and version
  notes.
- Python 3.11 `functools` documentation for the compatibility-floor API and union registration.
- PEP 443 for the accepted definition and rationale, operation-versus-data ownership, ABC ordering
  and ambiguity, original concurrency and caching implementation notes, usage patterns, and the
  deliberately narrow scope of single dispatch.
- The Python 3.14 glossary for generic-function and single-dispatch terminology.
- The Python 3.14 language reference for executable function definitions and decorator evaluation
  timing.
- The Python 3.14 import-system reference for module execution and `sys.modules` caching relevant to
  registration-by-import.
- Python 3.14 `importlib.metadata` documentation for entry-point discovery, which the unit carefully
  distinguishes from `singledispatch` registration.

Subtle claims cite these sources nearby in the unit note and experiment guides. No copied external
code, diagram, book prose, private data, production payload, credential, provider response, or
proprietary plugin was used.

## Executed checks

| Check | Observed result |
|---|---|
| Focused unit tests, CPython 3.14.7 | 29 passed: 20 example/experiment/visual tests and 9 practice behavior tests. |
| Focused unit tests, CPython 3.11.16 | The same 29 tests passed. |
| Repository regression, CPython 3.14.7 | 738 tests passed across all 51 discovered test directories, using a separate pytest process per directory. |
| Ruff lint | Passed for the complete SDP-PYT-080 unit tree with cache disabled. |
| Ruff formatting | All 19 format-eligible unit files were formatted. |
| Strict mypy, Python 3.14 target | No issues in 14 source files. |
| Strict mypy, Python 3.11 target | No issues in the same 14 source files. |
| Controlled negative mypy case | Both targets rejected an `object` passed to the typed facade and reported its exact supported union. |
| README Python snippets | All 11 fenced Python snippets compiled on CPython 3.14.7 and CPython 3.11.16. |
| Worked demo | Selected `render_user_registered` for an unregistered subclass and emitted the expected correlated observation. |
| Resolution experiment | Observed inherited `bool`→`int`, exact `bool` override, `list[int]` registration `TypeError`, and unrelated virtual-ABC ambiguity `RuntimeError`. |
| Import-order experiment | Fresh interpreters observed beta after alpha→beta imports and alpha after beta→alpha imports. |
| Practice starter | Emitted the expected alert and byte-message digests; the target refactoring remains absent. |
| Embedded visual model | Tests compared every field in all six embedded scenarios with maintained runtime observations. |
| HTML script syntax | Both script blocks were found, and the executable JavaScript compiled with Node.js 24.19.0. |
| Browser interaction | All six scenario controls updated phase, owner, value, runtime type, candidate path, selected handler, outcome, rule, warning, and pressed state. |
| Browser rendering | Default desktop layout was readable; 390×844 reflowed the path vertically with `scrollWidth=375` at `innerWidth=390`, so no horizontal overflow was observed. |
| Repository validator | All structure, metadata, Markdown, links, evidence, version, lock-file, source-policy, and hygiene checks passed after this record was added. |

Browser checks used the self-contained page through a temporary loopback server exposing only the
unit's `visuals/` directory. The viewport override was reset, the agent-created tab was closed, and
the server was stopped. These observations are not exhaustive accessibility conformance or coverage
of every browser, zoom level, color mode, assistive technology, and printing configuration.

## Repository-wide baseline constraints observed

- A repository-wide Ruff exploratory run reported 72 existing findings outside this new unit: 67
  line-length findings, three ambiguous-Unicode-string findings, one collection-literal
  concatenation finding, and one timezone modernization finding. The focused SDP-PYT-080 tree has
  zero Ruff findings, and no unrelated path was changed.
- A single repository-wide mypy invocation stops on the existing duplicate
  `test_runtime_experiments` module basenames before it can check all paths. The new unit was checked
  independently and strictly under both supported Python targets.
- The repository regression uses one pytest process per discovered test directory to avoid those
  pre-existing top-level test-module collisions.

These constraints do not weaken the focused results. They are recorded to keep the scope of each
green check honest.

## Manual content and boundary review

- Began with the change pressure and a simple first-argument mental model before formal mechanics.
- Covered the base/default implementation; decorator, explicit decorator, and functional
  registration; annotation inference; union registration; parameterized-container limits;
  `dispatch()`; `registry`; inheritance/MRO; ABC virtual subclasses; and ambiguity.
- Distinguished documented library behavior, static typing policy, design-level ownership
  inference, original PEP implementation notes, and current CPython observations.
- Compared the smallest direct call and conditional with dictionaries, pattern matching, methods,
  passed Strategy callables, Visitor, predicate rules, static overloads, and plugin discovery.
- Separated registration from discovery and deferred entry-point loading, trust, versioning,
  isolation, and plugin lifecycle to SDP-PYT-090.
- Made global registry ownership, deterministic imports, duplicate policy, multi-process startup,
  live-mutation risk, readiness inspection, testing isolation, and safe telemetry explicit.
- Tested exact selection, inherited selection, union entries, ABC selection, functional
  registration, public introspection, read-only registry view, container-content validation,
  fail-closed behavior, success/error observations, ABC ambiguity, and import order.
- Kept the audit-rendering worked example separate from the incident-digest practice domain.
- Kept practice runnable but unsolved: no target implementation, solution, released hint, learner
  attempt, or false learning evidence was added.
- Gave both non-trivial visuals reading guidance, a key insight, and a conceptual limitation; visual
  data is tied to executable observations rather than invented runtime internals.
- Used only synthetic identifiers, services, actors, payloads, results, and failures. Examples use no
  network, database, filesystem effects, framework, real endpoint, or credential.
- Removed every Worktree-local cache and bytecode directory created during checks before final
  repository validation.

## Approval boundary

The artifact is Approved because repository validation, dual-runtime focused tests, complete
repository regression, focused lint and formatting, strict dual-target typing, controlled negative
typing checks, snippet compilation, demo and starter execution, both experiments, visual model and
script tests, interactive browser checks, source review, and manual pedagogical review passed.
Approval applies only to the artifact. It does not claim that Rahul has practiced, recalled,
demonstrated, or retained the material.
