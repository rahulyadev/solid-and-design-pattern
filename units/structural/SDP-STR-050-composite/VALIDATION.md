# Validation — SDP-STR-050

## Scope and safe baseline

Only Composite is authored. Its artifact cell is the only tracker change; learning remains Not
started and learner dates, weaknesses and evidence remain untouched. Canonical scope: Professional,
Medium/Medium/Medium, L/D2, GoF/Structural, E+I+D+T, 4–6 h understanding and 5–9 h practice.

Branch: `topic/SDP-STR-050`. INIT_START: `bcb5a14fcc1ceb437a1dcfdaa4e7d022a4a69062`, recorded after
creation and empty tracked/staged/untracked porcelain status. HEAD, Local main and refreshed
origin/main matched the published Proxy PR #39 merge. The exact local and remote Composite refs
were absent (origin probe exit 2); no other Worktree owned the branch. The task was pinned.

Restricted authentication reported invalid credentials together with a network error. Elevated
`gh auth status` and `gh api user --jq .login` succeeded as `rahulyadev`; the exact no-tag main fetch
and exact topic probe reached origin. Shared Git metadata required elevated branch permission.
No broad refspec, history rewrite, plaintext credential output or unrelated environment change was used.

Read: AGENTS.md, docs/WORKFLOW.md, the current canonical entry, matching progress and prerequisite
rows, Python-reference mappings, relevant foundation bridges, unit/practice/experiment templates,
existing structural standards, source/version, copyright/license and NotebookLM policies. The clean
synchronized baseline passed the repository validator, including uv lock consistency. No later unit
is initialized here. Local's 24 ignored paths and 11 foundation ZIP fingerprints were recorded under
`/tmp/sdp-str-050`; those approved exceptions remain outside all staging and publication scope.

## Reproducible checks

Inspected existing runtimes: `/home/parry/projects/solid-and-design-pattern/.venv/bin/python`
(CPython 3.14.7) and `/tmp/sdp-cre-040/venv311/bin/python` (CPython 3.11.16), on Linux x86_64.
Both have pytest 8.4.2, mypy 1.20.2 and Hypothesis 6.165.2. No unrelated environment is modified.
`uv` is available for the validator's lock check.

From the repository root, using each selected Python:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-str-050/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-str-050/mypy
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-str-050/hypothesis
export RUFF_CACHE_DIR=/tmp/sdp-str-050/ruff
export UV_CACHE_DIR=/tmp/sdp-str-050/uv
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-str-050/venv
export COVERAGE_FILE=/tmp/sdp-str-050/coverage
mkdir -p /tmp/sdp-str-050/pytest
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-str-050/pytest/focused \
  units/structural/SDP-STR-050-composite
python -m mypy --strict --python-version 3.11 units/structural/SDP-STR-050-composite
python -m mypy --strict --python-version 3.14 units/structural/SDP-STR-050-composite
python -m ruff check --target-version py311 units/structural/SDP-STR-050-composite
python -m ruff format --check units/structural/SDP-STR-050-composite
python scripts/validate_repo.py
git diff --check
```

All generated state, including snippets, logs and regression subprocess caches, is under `/tmp`.
The complete regression exports MYPY_CACHE_DIR because existing tests invoke mypy internally.
Concurrent runtime checks use distinct cache and basetemp suffixes. Repository regression isolates
each pytest directory to avoid existing module-name collisions.

The typing test checks positive leaf/group/external Estimable assignments and exactly five negative
errors: wrong result, missing operation, inadmissible stored component, frozen children assignment,
and leaf child-management call. It runs both target versions in each runtime. The seven Python
files are also strict checked as a group. All five README Python fences are extracted independently
to `/tmp`, parsed with the 3.11 grammar, compiled and executed on both runtimes with `examples/` on
PYTHONPATH. The broad-node misuse fence catches its deliberately unsupported call.

## Maintainer review boundaries

The example is a bounded immutable value DAG evaluated per occurrence, not an exclusive mutable
tree, arbitrary graph validator, scheduler or execution engine. The acyclicity proof assumes completed
bottom-up construction and the supported frozen API; arbitrary object forging and unchecked imports
are outside it. The open Estimable client and closed Task/Group construction are explicitly different
boundaries. Height/occurrence metadata is admitted at construction; operations remain recursive for
teaching. Aliases are not deduplicated and path identities are local to a root version.

Initial review covered the exact canonical contract, simple-first progression, aggregation identity,
zero versus empty, error policy, capabilities, sharing versus cycles, root rebuilding, traversal,
complexity and input-size limitations. Sources are linked near subtle claims; the design source is
Wirfs-Brock's author-hosted discussion, not claimed access to the complete GoF chapter. All examples,
prose and diagrams are original and synthetic. No license, private data, learner evidence or solved
lab was added. No NotebookLM upload occurred.

Diagrams/table are conceptual text. Every experiment observation and path contract is checked by
executable assertions. No browser rendering was attempted or claimed; the earlier local-URL security
block was not worked around through another browser, server or indirect execution.

## Initialization observations — 2026-09-09

The first focused run passed 50 tests on CPython 3.14.7. Initial Ruff findings were import formatting
and a deliberate runtime `setattr` freeze probe; imports were fixed and the intentional probe was
locally documented. Lint and strict 3.11 typing then passed. Five independent README snippets,
the demo, the five-case probe and doubling bound, and the unsolved starter ran on both runtimes.
Both printed identical deterministic output. The starter reported `empty passes: True`,
`mixed passes: False`, and `target_complete=False`; it remains unsolved.

The complete initialization matrix, validator result and publication proof are recorded below after
execution. Final approval requires an additional scoped review and repository regression.

Initialization matrix completed: 50 focused tests passed on each runtime; strict mypy passed all
seven Python files for both 3.11 and 3.14 targets on both runtimes. The positive controls passed and
all five intended negative diagnostics were asserted in every target/runtime combination. Ruff
lint with py311 target and formatting passed (11 format-eligible unit files). All five independent
README snippets and all three runnable entry points succeeded on both runtimes. Validator passed,
including uv lock consistency and zero forbidden paths. Whitespace and scoped-file review passed.

Proxy PR #39 was independently confirmed merged with head
`ae65bf07678673f6084dd2d9ba87c3c4f633d412` and merge
`bcb5a14fcc1ceb437a1dcfdaa4e7d022a4a69062`; both trees equal
`5cb795e26f0dd9cf8922d66cd0f2e62ef70888f6`. Its local/remote topic counts are 0/0 and its Worktree
is clean. Initialization publication uses the exact current-operation-only proof before pushing.

## Initialization publication and final review

Initialization commit: `e34b75eab99e5f0ff058b1fb65a7bc0703674f5c`. Just before push, the exact
remote topic ref was still absent and refreshed origin/main still matched Local main/INIT_START.
The local-only and current-operation lists contained that identical single commit. The normal
exact-ref push set upstream and local-only/remote-only counts were 0/0. No PR or merge occurred
during initialization; final publication is separately authorized by the standing instruction.

Final review adds seven cases covering actual delegation order with aliases, failure propagation
without later visits, frozen derived bounds, snapshotting a caller list into a tuple, root-local
paths after reordering, and a statically valid but semantically dishonest estimator. Method tracing
and failure injection temporarily instrument Task in tests; they do not broaden supported mutation
or plugin admission. Runtime code needs no change after initialization. No lab solution is exposed.

## Final observed results — 2026-09-09

| Check | Actual result |
|---|---|
| CPython 3.14.7 focused suite | 57 passed |
| CPython 3.11.16 focused suite | 57 passed |
| Strict mypy | Seven Python files passed both 3.11/3.14 targets on both runtimes |
| Positive and negative controls | Positive client assignments accepted; exactly five intended errors on both targets/runtimes |
| Ruff lint/format | Passed with py311 lint target; all 11 format-eligible unit files compliant |
| README Python fences | Five independently parsed with 3.11 grammar, compiled and executed on both runtimes, including final artifact rerun |
| Runnable artifacts | Demo, five-case probe plus doubling bound, unsolved starter succeeded identically on both runtimes |
| Full repository regression | 1,335 passed across 80 isolated pytest directories on CPython 3.14.7; all directory runs exited zero |
| Repository validator | Passed, including uv lock consistency and zero forbidden paths |
| Scope/whitespace review | Exactly 12 paths versus main: 11 Composite artifacts and only the matching tracker artifact cell |
| Local unrelated artifacts | All 24 recorded ignored paths present; all 11 ZIP SHA-256 fingerprints unchanged before publication |

The artifact is Approved after source, pedagogical, contract, lab, typing, failure, visualization and
regression review. Learning remains Not started. No attempt, delayed recall, review date or weakness
has been fabricated. The last changes only record results and approval; the tested runtime code is
unchanged from initialization. Validator, lint/format and whitespace checks are repeated after this
record before the final commit.

GitHub currently reports no main branch protection/rules and zero CI workflows. PR-specific exact
base/head, commit and file lists, checks, status contexts and review requirements are inspected
again before squash merge. The final commit, PR, merge/tree-parity and Local synchronization facts
are reported in the task so this approved commit need not be rewritten to contain its own hash.
No failed check is bypassed.
