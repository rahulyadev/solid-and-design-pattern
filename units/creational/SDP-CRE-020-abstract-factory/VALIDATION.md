# Validation — SDP-CRE-020

## Scope and evidence boundary

| Field | Observed value |
|---|---|
| Date | 2026-09-07 |
| Exact branch | `topic/SDP-CRE-020` |
| Initialization baseline (`INIT_START`) | `bef6d713a96d3391181da247ee36e788a09664f9` |
| Initialization commit | `0732705a877ed2ec69b8e7a4ec19b9924d222884` |
| Evidence profile | `E+I+D+T` |
| Canonical runtime | CPython 3.14.7 |
| Compatibility runtime | CPython 3.11.16 |
| Artifact state during this record | Approved |
| Learning state during this record | Not started |

This record validates maintainer-authored curriculum material. It contains no learner prediction,
attempt, explanation, delayed recall, transfer, refactoring submission, or interview answer.
Authoring therefore advances only artifact state from Absent through Draft to Approved. Rahul's
learning state and every learner-evidence field in `PROGRESS.md` remain unchanged.

## Sources actually read

- The Addison-Wesley/O'Reilly catalog preview for the four authors, October 1994 publication, and
  the neighboring creational-pattern intents.
- The authorized InformIT Abstract Factory excerpt for original intent, applicability, family
  coherence, and classic participant names.
- The Python typing specification and reference for structural Protocol and callback-Protocol
  mechanics.
- Python 3.14.7 and 3.11.16 `contextlib` documentation for deterministic `ExitStack` cleanup,
  reverse callback order, partial acquisition, and the Python 3.11 `enter_context` error change.
- Python 3.14.7 `importlib.metadata` documentation for entry-point selection and the 3.12/3.13 API
  changes relevant to a Python 3.11-compatible discovery boundary.

Subtle history and Python-version claims cite these sources near the relevant mechanics. Design
selection, compatibility validation, configuration, observability, security, concurrency, and
performance recommendations are presented as professional judgment rather than Python guarantees.
No external pattern diagram, book prose, book example, proprietary code, production data,
credential, private message, or customer schema is reproduced.

## Checks executed

| Check | Observed result |
|---|---|
| Focused unit tests, CPython 3.14.7 | 36 passed across worked examples, Hypothesis family contracts, partial-acquisition experiment, visual contracts, and unsolved-practice behavior. |
| Focused unit tests, CPython 3.11.16 | The same 36 tests passed. |
| Repository regression, CPython 3.14.7 | 918 tests passed with no skips across all 61 discovered test directories, using a separate pytest process per directory. |
| Ruff lint | Passed for the complete SDP-CRE-020 unit tree with cache under `/tmp`. |
| Ruff formatting | All 16 format-eligible unit files were formatted or already compliant. |
| Strict mypy, Python 3.14 target | No issues in all 6 non-test Python source files. |
| Strict mypy, Python 3.11 target | No issues in the same 6 source files. |
| Controlled negative mypy case | Both targets rejected an incomplete family missing `open_channel` and `create_acknowledgement_decoder`. |
| README Python snippets | All 11 fenced Python snippets compiled on CPython 3.14.7 and CPython 3.11.16. |
| Worked demo | Both families produced accepted family-specific receipts and the expected phase sequence. |
| Practice starter | Produced one internal receipt and reported `target_complete=False`. |
| Lifetime experiment | Observed reverse cleanup on success and cleanup of the first resource when the second acquisition failed. |
| Embedded visual model | Tests matched every field and order for all eight embedded scenarios to maintained Python data. |
| HTML script syntax | The executable JavaScript block compiled with Node.js 24.19.0. |
| Static visual structure | Accessible tab/panel roles, keyboard handlers, balanced braces, reduced-motion handling, and the responsive breakpoint were present. |
| Interactive browser rendering | Not performed: the in-app browser blocked the local `file:` URL under its URL security policy. No workaround, indirect navigation, alternate browser, or policy bypass was attempted. |
| Repository validator after approval edits | Passed every structural, metadata, Markdown, link, evidence, version, lock-file, and hygiene check with zero forbidden-path violations. |
| Git diff check | `git diff --check` passed; final scope is the matching progress row plus the SDP-CRE-020 unit tree. |

All pytest, Hypothesis, Ruff, mypy, uv, and bytecode caches were directed to `/tmp`; pytest's
in-repository cache provider was disabled. No generated cache or test output was created in the
Worktree.

## Manual authoring review

- Began with direct construction, a ready coherent bundle, a family function, and ordinary
  dependency injection before class/object Abstract Factory.
- Named the concrete pressure: encoder, Channel, and acknowledgement decoder must share one wire
  protocol family.
- Distinguished structural Product-role typing from semantic cross-product compatibility and
  defended the invariant before external writes.
- Distinguished Abstract Factory from one-product Factory Method and from a bag of unrelated
  constructors.
- Kept family selection and concrete imports at the composition root while keeping policy code
  dependent on small Protocols.
- Separated malformed, unknown, disallowed, alias mismatch, construction/acquisition, coherence,
  encode, send, decode, and cleanup failures.
- Made the factory path's fresh owned Channel and the ready bundle's borrowed Channel different,
  documented lifetime contracts.
- Covered partial multi-resource acquisition, reverse cleanup, cleanup during send failure,
  observer failure policy, uncertain external effects, async cancellation, and provider load
  boundaries without promising rollback.
- Kept observations allow-listed and free of message bodies, acknowledgement bytes, credentials,
  complete configuration, and arbitrary object representations.
- Addressed frozen-but-not-transitively-immutable factories, captured state, registry snapshots,
  worker-process boundaries, and the lack of a pattern-level concurrency guarantee.
- Bounded dynamic registration to independently shipped providers and treated entry-point loading
  as a trust/deployment boundary rather than a sandbox.
- Included adding-family versus adding-Product-role costs, overengineering rejections, one-question
  interview prompts with exact missing reasoning steps, and reconstruction-oriented notebook notes.
- Used only synthetic event and notification data with no network, database, framework, production
  service, private data, or employer artifact.
- Preserved the separate lab as runnable but unsolved with predict → run → observe → explain →
  refactor → vary and empty learner-evidence fields.

## Initialization closure

Initialization changed exactly the new SDP-CRE-020 tree and its matching `PROGRESS.md` row to
Draft. The local-only commit list against synchronized `main` and the current-operation list from
`INIT_START` were identical: only initialization commit
`0732705a877ed2ec69b8e7a4ec19b9924d222884`. That commit was pushed normally and established the
remote branch; initialization did not create a pull request, merge, or change `main`.

## Approval boundary

The artifact is Approved because the complete teaching material, worked code, unsolved lab,
experiment, visual contract, dual-runtime tests, property-based family checks, strict typing,
negative typing control, lint/formatting, snippet compilation, regression suite, authoritative
source review, final repository validation, scoped Git checks, and manual
pedagogical/production review passed.

Approval applies only to the teaching artifact. It does not claim Rahul has predicted,
implemented, debugged, explained, recalled, transferred, demonstrated, or retained SDP-CRE-020.
