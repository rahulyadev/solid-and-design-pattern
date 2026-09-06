# Validation — SDP-CRE-010

## Scope and evidence boundary

| Field | Observed value |
|---|---|
| Date | 2026-09-06 |
| Exact branch | `topic/SDP-CRE-010` |
| Initialization baseline (`INIT_START`) | `b6cc15a36f73c58d3ad78e2cdac0532c652a39b2` |
| Initialization commit | `b0fa3674d3f45e93186fabdf372a5b2636654dba` |
| Evidence profile | `E+I+D+T` |
| Canonical runtime | CPython 3.14.7 |
| Compatibility runtime | CPython 3.11.16 |
| Artifact state during this record | Approved |
| Learning state during this record | Not started |

This record validates maintainer-authored curriculum material. It contains no learner prediction,
attempt, explanation, delayed recall, transfer, refactoring submission, or interview answer.
Therefore authoring advances only artifact state from Absent through Draft to Approved. Rahul's
learning state and every learner-evidence field in `PROGRESS.md` remain unchanged.

## Sources actually read

- The Addison-Wesley/InformIT publisher record for the four authors and October 1994 publication of
  *Design Patterns: Elements of Reusable Object-Oriented Software*.
- The authorized O'Reilly catalog preview for the original Factory Method entry and the neighboring
  creational-pattern distinctions.
- Python 3.14.7 and 3.11.16 data-model documentation for class callability, callable instances,
  methods, dictionaries, object lifetime, and explicit resource cleanup.
- Python 3.14.7 built-in-function documentation for `classmethod` binding and version history.
- Python 3.14.7 `functools` documentation for partial application and the 3.14 `Placeholder`
  addition that the 3.11-compatible examples deliberately avoid.
- The Python typing specification for structural protocols, callback protocols, and callable
  assignability.
- Python 3.14.7 import-system documentation for execution, caching, and import-failure boundaries
  relevant to dynamic-registration comparisons.

Subtle claims cite these sources near their mechanics. Design selection, security, observability,
concurrency, and performance advice is presented as professional judgment rather than a Python
language guarantee. No external pattern diagram, book prose, book example, proprietary code,
production data, credential, private message, or customer schema is reproduced.

## Checks executed

| Check | Observed result |
|---|---|
| Focused unit tests, CPython 3.14.7 | 44 passed across worked examples, lifetime experiment, visual contracts, and unsolved-practice behavior. |
| Focused unit tests, CPython 3.11.16 | The same 44 tests passed. |
| Repository regression, CPython 3.14.7 | 882 tests passed with no skips across all 58 discovered test directories, using a separate pytest process per directory. |
| Ruff lint | Passed for the complete SDP-CRE-010 unit tree with cache disabled after import-order fixes. |
| Ruff formatting | All 18 format-eligible unit files were formatted or already compliant. |
| Strict mypy, Python 3.14 target | No issues in all 7 non-test Python source files. |
| Strict mypy, Python 3.11 target | No issues in the same 7 source files. |
| Controlled negative mypy case | Both targets rejected a callable with an extra required keyword-only argument as incompatible with `ConfiguredTransportFactory`. |
| README Python snippets | All 19 fenced Python snippets compiled on CPython 3.14.7 and CPython 3.11.16. |
| Worked demo | Both runtimes produced identical class, callable, configured Product, and event output. |
| Practice starter | Both runtimes exported one text report and reported `target_complete=False`. |
| Lifetime experiment | Both runtimes observed `construct > use > close` and failure cleanup before the caught error. |
| Embedded visual model | Tests matched every field in all eight embedded scenarios to maintained Python data. |
| HTML script syntax | The executable JavaScript block compiled with Node.js 24.19.0. |
| Static visual structure | Required accessible targets, keyboard handlers, balanced CSS braces, and responsive media rules were present. |
| Interactive browser rendering | Not performed: the in-app browser blocked the local `file:` URL under its URL security policy. No workaround, indirect navigation, alternate browser, or policy bypass was attempted. |
| Repository validator | Passed all structural, metadata, Markdown, link, evidence, version, lock-file, and hygiene checks with zero forbidden-path violations. |
| Git diff check | `git diff --check` passed; scope was one matching progress row plus the new SDP-CRE-010 unit tree. |

The first validator invocation correctly found the then-missing validation record, a Ruff cache
created by the formatting command, and a sandbox-only uv cache-lock failure. Those are remediation
inputs, not passing results. The final initialization validator result and Git diff checks are
recorded below only after they run.

## Manual initialization review

- Began with direct construction, a small conditional, a simple factory function, an explicit
  callable dictionary, and dependency injection before class-based Factory Method.
- Distinguished Product, Concrete Product, Creator, Concrete Creator, the factory method, client,
  and composition root.
- Kept Product construction separate from publication, domain validation, observations, and error
  translation.
- Compared subclass override with factory functions, class objects, `partial`, callback Protocols,
  alternate constructors, callable registries, explicit composition roots, and ready-Product
  injection.
- Bounded comparisons with Abstract Factory, Builder, Prototype, Strategy, dynamic registration,
  dependency injection, and service locator without creating later unit artifacts.
- Covered malformed, unknown, disallowed, construction, execution, and cleanup failure phases.
- Made new-versus-borrowed lifetime ownership and deterministic cleanup explicit.
- Kept observations allow-listed and free of alert bodies, credentials, and full configuration.
- Addressed independent per-call state, mutable captured state, registry mutation, async shape,
  imports, and multi-process boundaries without claiming a universal GIL guarantee.
- Used only synthetic alert and incident-report data with no network, database, production system,
  framework, or private dependency.
- Preserved the separate lab as runnable but unsolved with predict → run → observe → explain →
  refactor → vary and empty learner-evidence fields.

## Initialization closure

The validator passed with a writable cache under `/tmp`; its uv lock check also passed. No virtual
environment, bytecode, pytest/Ruff/mypy cache, coverage file, temporary typing input, validation
JSON, or generated runtime output is inside the Worktree. Initialization scope is exactly the new
SDP-CRE-010 tree and the matching `PROGRESS.md` row. Commit and current-operation-only push evidence
is recorded in Git and in the task handoff after the workflow proof runs.

The browser-policy limitation narrows visual evidence honestly: maintained-data parity, JavaScript
syntax, DOM targets, keyboard handlers, CSS balance, and responsive-source checks passed, but this
record does not claim a rendered desktop/mobile or accessibility observation.

## Approval boundary

The artifact is Approved because repository validation, dual-runtime focused tests, the complete
repository regression, focused lint/formatting, strict dual-target typing, a controlled negative
typing check, dual-runtime snippet compilation, worked demo and practice execution, the reproduced
lifetime experiment, visual-data parity, JavaScript syntax, static visual checks, authoritative
source review, and manual pedagogical/production review passed.

Approval applies only to the teaching artifact. It does not claim Rahul has predicted,
implemented, debugged, explained, recalled, transferred, demonstrated, or retained SDP-CRE-010.
