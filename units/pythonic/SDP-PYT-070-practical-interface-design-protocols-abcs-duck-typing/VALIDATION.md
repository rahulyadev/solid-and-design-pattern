# Validation — SDP-PYT-070

## Scope and evidence boundary

| Field | Observed value |
|---|---|
| Date | 2026-09-06 |
| Exact branch | `topic/SDP-PYT-070` |
| Initialization baseline (`INIT_START`) | `1283e3094ce2db40adf6d60c4ee5beed2ceeb7d6` |
| Initialization commit | `d97c3a9d297fd5f529dcbdf390d4fdc24da730ab` |
| Evidence profile | `E+I+D+T` |
| Canonical runtime | CPython 3.14.7 |
| Compatibility runtime | CPython 3.11.16 |
| Artifact state during this record | Approved |
| Learning state during this record | Not started |

This record validates maintainer-authored curriculum material. It does not record a learner
prediction, attempt, explanation, delayed recall, transfer, or interview answer. Therefore only the
artifact state advances from Absent through Draft to Approved; Rahul's learning state remains Not
started and every learner-evidence field in `PROGRESS.md` remains `—`.

## Sources actually read

- Python 3.14 `typing` documentation for the non-enforcement of annotations, Protocol structural
  checking, callable Protocols, runtime-checkable limits, performance caution, and Python 3.12+
  runtime behavior.
- Python 3.11 `typing` documentation for the compatibility form and earlier runtime-checkable
  behavior.
- Python 3.14 `abc` documentation for abstract-member instantiation rules, concrete ABC methods,
  virtual registration, missing MRO inheritance, and `__subclasshook__` behavior.
- PEP 544 for structural-subtyping terminology, implicit and explicit implementation, module
  implementations, and the intentionally limited runtime-checkable model.
- The current Python typing specification for protocol member declarations, read/write versus
  read-only attributes, explicit implementation, modules, and runtime narrowing restrictions.

The unit cites those sources beside subtle claims. No copied external code, diagram, private data,
real provider response, credential, or proprietary interface was used.

## Executed checks

| Check | Observed result |
|---|---|
| Focused unit tests, CPython 3.14.7 | 24 passed. |
| Focused unit tests, CPython 3.11.16 | 24 passed. |
| Repository regression, CPython 3.14.7 | 709 tests passed across all 49 discovered test directories, using a separate pytest process per directory. |
| Ruff lint | Passed for the complete SDP-PYT-070 unit tree with cache disabled. |
| Ruff formatting | All 14 format-eligible unit files already formatted. |
| Strict mypy, Python 3.14 target | No issues in 10 source files. |
| Strict mypy, Python 3.11 target | No issues in the same 10 source files. |
| Controlled negative mypy case | Rejected the candidate for missing `channel_name` and an incompatible `deliver` signature and result. |
| README Python snippets | All 10 fenced Python snippets compiled on CPython 3.14.7 and CPython 3.11.16. |
| Worked demo | Both structural implementations returned the expected event and idempotency key. |
| Runtime Protocol probe | Presence recognition was `True`; the real wrong-signature call raised `TypeError`. |
| Practice starter | Emitted the expected synthetic export record; the target refactoring remains absent. |
| Embedded visual model | Unit tests compared every JSON field in all four scenarios with the maintained Python observations. |
| HTML script syntax | The visual's executable JavaScript passed `node --check` with Node.js 24.19.0. |
| Browser interaction | All four scenario controls updated the pressure, runtime, static, mechanism, evidence, cost text, and pressed state. |
| Browser rendering | The default desktop layout was readable; 390×844 reflowed controls and cards to one column with no horizontal overflow. |
| Repository validator | All structure, metadata, Markdown, links, evidence, version, lock-file, source-policy, and hygiene checks passed after this record was added. |

The browser checks used the self-contained page through a temporary server exposing only the unit's
`visuals/` directory on loopback. The viewport override was reset, the agent-created tab was closed,
and the server was stopped. These observations are not exhaustive accessibility conformance or
coverage of every browser, zoom level, printing mode, and color mode.

## Repository-wide baseline constraints observed

- A repository-wide Ruff exploratory run reported 72 existing findings under
  `scripts/validate_repo.py`; the focused unit tree has zero findings, and no unrelated file was
  changed.
- A single repository-wide mypy invocation stops on existing duplicate test module basenames before
  checking all paths. The unit was therefore checked independently and strictly under both supported
  Python targets.
- The repository regression uses one pytest process per discovered test directory to avoid the same
  pre-existing top-level test-module collisions.

These constraints predate SDP-PYT-070 and do not weaken the focused unit results. They are recorded
so the scope of each green check is explicit.

## Manual content and boundary review

- Began with the client promise and runtime call before formal typing terminology.
- Distinguished runtime duck typing, structural static conformance, normal annotation behavior,
  nominal ABC inheritance, virtual registration, and behavioral substitutability.
- Covered explicit and implicit Protocol implementation, read-only properties, callable alternatives,
  ABC abstract members, concrete shared methods, registration, subclass hooks, adapters, modules,
  generic-variance boundaries, and Python 3.11 compatibility.
- Compared the simplest concrete/function design, pressure-driven Protocol, owned ABC family,
  adapter boundary, and overengineered hierarchy.
- Tested compatible independent implementations, idempotency collision, invalid input, wrong receipt,
  ABC batch behavior, incomplete direct subclasses, virtual recognition, and wrong-signature runtime
  Protocol behavior.
- Separated signature evidence from inputs, results, errors, effects, history, concurrency, retry,
  cancellation, durability, and security promises.
- Kept the audit-delivery worked example separate from the report-export practice domain.
- Kept practice runnable but unsolved; no target implementation, solution, released hint, learner
  attempt, or false learning evidence was added.
- Used synthetic identifiers, payloads, providers, results, and failures; no network, database,
  filesystem, framework, real endpoint, or credential is used by the examples.
- Removed the Worktree-local environment and all generated caches created during checking before the
  final repository validation.

## Approval boundary

The artifact is Approved because repository validation, dual-runtime focused tests, complete
repository regression, focused lint and formatting, strict dual-target typing, a controlled negative
typing case, snippet compilation, demo and starter execution, visual model/script/browser checks,
source review, and manual pedagogical review passed. Approval applies only to the artifact. It does
not claim that Rahul has practiced, recalled, demonstrated, or retained the material.
