# Validation — SDP-PYT-050

## Record scope

This record verifies the maintainer-created learning artifact for **SDP-PYT-050 — Modules, import
caching, and dependency lifetimes**. It does not claim that Rahul attempted the lab, recalled the
material, demonstrated transfer, or reached any learning state.

| Field | Value |
|---|---|
| Branch | `topic/SDP-PYT-050` |
| Initialization start | `a95528693e74c3ee76011553e733bfa0c114d7b4` |
| Artifact state during this record | Approved |
| Learning state | Not started |
| Validation date | 2026-09-06 |
| Canonical target | CPython 3.14.7 |
| Compatibility target | Python 3.11.16 |

## Canonical alignment

- Exact curriculum outcome: compare module namespaces, import caching, application-scoped objects,
  and explicit lifetimes with a traditional Singleton.
- Canonical prerequisites: `SDP-FND-090` and `SDP-FND-100`.
- Classification: Core; High interview, production, and Python/backend relevance; D3; size L.
- Evidence profile: `E+I+D+X+T`.
- Progress edit: only the `SDP-PYT-050` artifact state advanced from Absent through Draft to
  Approved; learning state remained Not started.

## Artifact inventory

| Evidence | Artifact |
|---|---|
| Explain (`E`) | Integrated simple-first note covering import/name mechanics, scope taxonomy, ownership, alternatives, failures, backend mapping, and interview judgment. |
| Implement/test (`I`) | Explicit application pool and request session owners, typed policy boundary, runnable demo, and behavior tests. |
| Debug/refactor (`D`) | Independent module-global fulfillment starter, characterization tests, phased unsolved lifetime refactoring, and failure cases. |
| Experiment (`X`) | Cache/reload/alias probe and two-process cache-scope probe with hypotheses, exact environments, actual normalized output, interpretations, and limitations. |
| Transfer (`T`) | FastAPI mapping plus new-scenario prompts for mounted apps, workers, background work, models, plugins, and distributed uniqueness. |
| Visual | Responsive selectable lifetime map whose complete embedded JSON is compared with maintained Python data. |

## Sources actually read

The maintainer read the current Python 3.14 import-system sections for packages, search, module
cache, loading, and submodule binding; the `sys.modules`, `importlib.reload`, `functools.cache`,
`contextvars`, and multiprocessing start-method documentation; and the current FastAPI lifespan and
yield-dependency guides. The unit cites subtle semantics near their claims and uses original
synthetic prose, code, exercises, experiments, and diagrams.

## Executed checks

| Check | Observed result |
|---|---|
| Unit tests, CPython 3.14.7 | 15 passed. |
| Unit tests, CPython 3.11.16 | 15 passed. |
| Repository regression, CPython 3.14.7 | 659 tests passed across all 45 discovered test directories, using a separate pytest process per directory. |
| Ruff lint | Passed for the unit tree. |
| Ruff formatting | Passed for all files in the unit tree considered by Ruff. |
| Strict mypy, Python 3.14 target | No issues in 12 source files. |
| Strict mypy, Python 3.11 target | No issues in the same 12 source files. |
| README Python snippets | All 15 fenced snippets compiled on CPython 3.14.7 and CPython 3.11.16. |
| Worked demo | Both runtimes returned remaining allowances 3 and 10, used two request sessions, closed the pool, and produced the expected nested trace. |
| Cache/reload probe | Both runtimes matched the recorded JSON for repeated import, reload, retained alias, cache deletion, and fresh import. |
| Process-scope probe | Both runtimes started two distinct children; each executed once and reused its own second import. |
| Practice starter | Both runtimes returned the expected synthetic allocation; learner refactoring remains absent. |
| Embedded visual model | Unit test compared all five HTML JSON states with the maintained Python observations. |
| HTML script syntax | The visual's executable JavaScript passed `node --check` with Node.js 24.19.0. |
| Browser rendering | Not claimed: the available in-app browser blocked the local `file:` URL by security policy. |
| Repository validator | All repository structure, metadata, link, evidence, version, lock-file, and source-policy checks passed after generated tool caches were moved outside the Worktree. |

The browser limitation does not change the semantic visual checks. The HTML source was manually
reviewed for native controls, keyboard access, 760 px and 390 px reflow rules, text wrapping, and
absence of fixed-width content; no claim is made about actual browser rendering, exhaustive
accessibility, untested engines, or color modes.

## Manual content and boundary review

- Began with concrete change pressure and a cache-versus-owner mental model before formal mechanics.
- Distinguished module namespace, import search/loading, local name binding, cache association,
  application scope, request scope, task context, transient scope, and distributed coordination.
- Compared stateless modules, module globals, ordinary factories, context managers, explicit app
  containers, cached factories, context variables, traditional Singleton, and external ownership.
- Separated Python language/import guarantees, standard-library contracts, framework behavior,
  version-dependent behavior, deployment assumptions, and professional design inference.
- Covered partially initialized imports, stale aliases, reload, cache deletion, concurrent lazy
  initialization, worker multiplicity, partial startup, cleanup competition, resource escape,
  observability, and state safety.
- Kept the worked domain separate from the practice domain.
- Kept practice runnable but unsolved; no target implementation, hint, comparison solution,
  learner attempt, or false learning evidence was added.
- Used no external code, copied diagram, private data, credential, real endpoint, framework
  dependency, license, generated environment, cache, or conversation transcript.

## Approval boundary

The artifact is Approved because repository validation, dual-runtime unit checks, repository
regression, lint, formatting, strict typing, experiment reproduction, snippet compilation, visual
model/script verification, and final manual content review passed. This approves maintainer-created
material only; it does not advance learning state or assert learner evidence. Push, pull-request,
merge, and synchronization results are reported only after those operations actually complete.
