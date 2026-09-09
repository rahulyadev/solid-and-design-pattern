# Validation — SDP-BEH-020 State

## Scope and baseline

Only this unit and the matching artifact cell in PROGRESS.md are in scope. Learning remains
Not started. No subagents or parallel curriculum authoring are used. The unit/practice/experiment
templates supply E+I+D+X+T artifacts. The reservation starter stays unsolved. Text diagrams and
observation tables are conceptual; no browser rendering is attempted or claimed.

INIT_START: `f3fd2bbe24a014306c965e68c3a9c290b51b5492`. The clean detached Worktree, Local main,
and origin/main matched this baseline. Neither exact State branch existed. The workflow's exact
no-tag main fetch succeeded, and exact topic probe reached origin and returned absent (exit 2).
The exact branch `topic/SDP-BEH-020` was created from synchronized main and the task pinned.

Elevated authentication passed as rahulyadev after restricted checks reported a token error together
with API network failure. GitHub independently confirmed Strategy PR #43 merged with topic head
`91535b4b0bf12e9bfa16a77efb2271f1d8a74b62`; its approved tree and the baseline squash tree both equal
`8a714efc1ce7901bd843dfa56995e20790160509`. Baseline repository validation passed.

Independent preservation snapshot `/tmp/sdp-beh-020/local-artifacts-before.json` records 24 ignored
Local paths and SHA-256 hashes of all 11 foundation ZIPs. Those approved local artifacts and the
unrelated environments are preserved. All generated check state belongs under `/tmp`.

## Reproduction

Select one installed interpreter as `python`: CPython 3.14.7 at
`/home/parry/projects/solid-and-design-pattern/.venv/bin/python`, or CPython 3.11.16 at
`/tmp/sdp-cre-040/venv311/bin/python`. Recheck availability and versions rather than assuming paths
persist. Use the locked development dependencies without modifying these environments.

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-beh-020/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-beh-020/mypy
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-beh-020/hypothesis
export RUFF_CACHE_DIR=/tmp/sdp-beh-020/ruff
export UV_CACHE_DIR=/tmp/sdp-beh-020/uv
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-beh-020/venv
export COVERAGE_FILE=/tmp/sdp-beh-020/coverage
mkdir -p /tmp/sdp-beh-020/pytest
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-beh-020/pytest/focused \
  units/behavioral/SDP-BEH-020-state
python -m mypy --strict --python-version 3.11 units/behavioral/SDP-BEH-020-state
python -m mypy --strict --python-version 3.14 units/behavioral/SDP-BEH-020-state
python -m ruff check --target-version py311 units/behavioral/SDP-BEH-020-state
python -m ruff format --check units/behavioral/SDP-BEH-020-state
python units/behavioral/SDP-BEH-020-state/examples/run_state_demo.py
python units/behavioral/SDP-BEH-020-state/examples/observe_boundary.py
python units/behavioral/SDP-BEH-020-state/practice/reservation_lab.py
python scripts/validate_repo.py
git diff --check
```

For snippets, extract every Python fence into `/tmp`, parse with 3.11 grammar, compile and execute
independently on both runtimes with `examples/` on PYTHONPATH. Also parse every unit Python source
with 3.11 grammar. Run existing pytest directories in separate processes to avoid module collisions.
Export MYPY_CACHE_DIR for the entire regression because existing tests invoke mypy internally.
Use distinct temporary paths for independent check processes, and create custom basetemp parents.

## Manual review boundaries

Public Packet inputs are runtime checked. Direct concrete-state calls assume context-validated
arguments. The frozen Snapshot constructor is a typed data constructor, not an input parser.
Concrete states are closed implementation collaborators; there is no plugin injection or arbitrary
initial-state API. Gates are trusted synchronous callables: typing checks their shape, while the
runtime invokes them and ignores their return value. Normal private/frozen/class boundaries are
preconditions, not protection against hostile Python code.

The gate sees a proposal before commit; the context remains sealed until return. Callback effects
are not rolled back. Same-context nesting is rejected, including invalid nested requests; a gate
can catch that error and permit the outer transition. The busy flag is not a lock. No remote effect,
transaction, concurrent access, benchmark, browser rendering, or learner evidence is inferred.

## Initialization checks — 2026-09-10

Both CPython 3.14.7 and 3.11.16 passed 87 focused tests. The static controls accepted positive
clients and produced exactly ten intended negative diagnostics for each 3.11/3.14 typing target.
Strict mypy passed all seven Python files for both targets on both runtimes. Ruff py311 lint and
format checks passed. Four independent README snippets parsed with 3.11 grammar, compiled and
executed on both runtimes; all seven Python sources also passed that grammar check.

The demo printed the accepted/rejected sequence documented by the matrix, finishing released with
three pages at revision 6, then rejecting CANCEL. The independent starter printed `free, owner=None`
and `target_complete=False`. EXP-01's four recorded lines matched on both runtimes. The repository
validator passed on both, including uv lock consistency and zero forbidden paths. Whitespace and
scope review passed: eleven unit files and only the matching Draft tracker cell.

During preparation, a long line and import order were fixed. Ruff's literal-setattr rewrite in an
intentional frozen-assignment test was changed to a variable attribute name so the negative runtime
probe remains explicit while strict typing passes. The validator initially mistook an ASCII
less-than comparison in a diagram for a template placeholder; the diagram now uses the mathematical
≤ sign. All affected checks passed after correction. No failure was bypassed.

Logs are under `/tmp/sdp-beh-020/init314`, `init311`, `init314-finish` and `init311-finish`.
Initialization is complete enough to study with an unsolved lab. Final approval awaits the separate
review/regression phase. The task's publication report will record the initialization commit and
current-operation-only push proof; initialization itself creates no PR and performs no merge.
