# Validation — SDP-STR-070

## Scope and safe baseline

Only Flyweight and its matching tracker artifact cell change. Canonical contract: Advanced,
Low/Low/Low, L/D3, GoF/Structural/Runtime, E+I+D+X+T, 4–6 h first understanding and 5–9 h practice.
Learning stays Not started. No learner attempts, dates or weaknesses are generated.

`topic/SDP-STR-070` starts at `56f3853bf734ef35f62a25a85a6d015b14d64b7a`, recorded as INIT_START
only after branch creation and completely empty tracked/staged/untracked porcelain status. HEAD,
clean Local main and exact-ref refreshed origin/main matched. Neither exact topic ref existed;
the remote probe reached origin and exited 2. No other Worktree owned the branch. This task is pinned.

The restricted authentication check reported an invalid token alongside a network error. Elevated
`gh auth status` and `gh api user --jq .login` succeeded as `rahulyadev` before authoring. The exact
no-tag main fetch and exact topic probe reached origin. No plaintext credential was exposed.
Shared Git metadata required elevated filesystem permission for branch creation.

Predecessor Bridge PR #41 was published at the baseline. Its approved topic tree and squash tree
were reported identical in the handoff. The baseline validator independently passed here, including
uv lock consistency and zero forbidden paths. Local's current 24 ignored paths and 11 foundation ZIP
SHA-256 hashes are snapshotted at `/tmp/sdp-str-070/local-artifacts-before.json`. They are preserved
outside the dedicated validation Worktree; no ignored ZIP is staged or published.

Read: AGENTS.md, workflow, matching canonical/progress rows, both hard prerequisite tracker rows,
relevant Python mappings, unit/practice/experiment templates, structural-unit standards, and
source/version, rights and NotebookLM policies. No later unit is authored; no subagent is used.

## Review boundaries

The worked tile example is original synthetic byte generation, not real image processing. Typed
integer/key inputs and normal construction are caller preconditions. Runtime ranges reject bool
but do not admit arbitrary untyped objects. Frozen/final boundaries are explained honestly. Logical
placement IDs are caller-managed; the module does not maintain a global uniqueness registry.
The pool is single-thread-owned, strongly retaining, and entry-bounded with rejection on a new
key at capacity. Clearing ends its canonicalization scope without revoking old placements.

The lab is unsolved, with separate language/revision/row-edit requirements. Baseline tests do not
certify the target. No hints, answers, learner evidence or comparison solution is added. Sources
are cited near subtle claims. The primary GoF paper was read through its available transcription;
only indexed participants/collaboration text was readable for the catalog PDF, whose full open failed.
No complete-book reading claim is made. Visuals are conceptual text diagrams and tables with reading
guides and limits. No browser rendering is claimed or attempted; prior local-URL blocks are not bypassed.

## Reproduction environment

Existing interpreters: `/home/parry/projects/solid-and-design-pattern/.venv/bin/python`
(CPython 3.14.7) and `/tmp/sdp-cre-040/venv311/bin/python` (CPython 3.11.16).
Linux 7.0.0-31-generic x86_64, glibc 2.43; both Python builds use Clang 22.1.3.
Locked tools inspected: pytest 8.4.2, mypy 1.20.2, Ruff 0.16.1, Hypothesis 6.165.2.
No unrelated environment is modified. All generated state is redirected to `/tmp`.

From repository root, select the desired Python executable and use:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-str-070/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-str-070/mypy
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-str-070/hypothesis
export RUFF_CACHE_DIR=/tmp/sdp-str-070/ruff
export UV_CACHE_DIR=/tmp/sdp-str-070/uv
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-str-070/venv
export COVERAGE_FILE=/tmp/sdp-str-070/coverage
mkdir -p /tmp/sdp-str-070/pytest
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-str-070/pytest/focused \
  units/structural/SDP-STR-070-flyweight
python -m mypy --strict --python-version 3.11 units/structural/SDP-STR-070-flyweight
python -m mypy --strict --python-version 3.14 units/structural/SDP-STR-070-flyweight
python -m ruff check --target-version py311 units/structural/SDP-STR-070-flyweight
python -m ruff format --check units/structural/SDP-STR-070-flyweight
python units/structural/SDP-STR-070-flyweight/examples/run_flyweight_demo.py
python units/structural/SDP-STR-070-flyweight/examples/memory_probe.py
python units/structural/SDP-STR-070-flyweight/practice/legend_lab.py
python scripts/validate_repo.py
git diff --check
```

Use distinct cache/basetemp paths for simultaneous processes. The complete regression must export
MYPY_CACHE_DIR because existing tests invoke mypy internally. Run each existing pytest directory
independently to avoid module-name collisions. Parse Python files and independently extracted README
Python fences with the 3.11 grammar; compile and execute fences on both runtimes with examples on
PYTHONPATH. Generated snippets and command logs belong under `/tmp`.

## Controlled experiment

[EXP-01](experiments/EXP-01-sharing-retention/README.md) records question, hypothesis, controls,
exact environment, commands, all observed outputs and limits. Three representations, two key
distributions, three fresh-process trials and two runtimes give 36 actual measured child runs.
The probe measures retained traced allocations, not timing, shallow sizes or process RSS.
The repeated-key case favors sharing; the all-unique case costs more with the pool on both runtimes.
Strong owners retain values after placements are dropped. Clear releases those owner references.
No production memory improvement or universal finalization deadline is claimed.

## Initialization results — 2026-09-09

63 focused tests passed on each runtime, including positive and exactly nine negative static
contract controls for both 3.11 and 3.14 targets. Strict mypy passed all eight source files for
both target versions on both runtimes. Ruff py311 lint and format checks passed (12 eligible files).
Four independent README Python snippets parsed with the 3.11 grammar, compiled and executed on
both runtimes; all eight source files also parsed with the 3.11 grammar. Demo and unsolved starter
ran on both runtimes. The starter retained `target_complete=False`.

Both runtime validator runs passed, including uv lock consistency and zero forbidden paths.
Whitespace checks passed. Initial lint exposed long lines and converted constant-name `setattr`
negative tests into direct assignments; the latter needed narrowly scoped `type: ignore[misc]`
comments because those three tests intentionally exercise runtime frozen failures. Independent
negative typing clients still verify rejection without suppression. No failed check was bypassed.

The complete Draft material is ready for the initialization commit and exact current-operation-only
push proof. Initialization does not create a PR or merge. Approval awaits final review and repository
regression; no learner state is advanced.

## Initialization publication and final review

Initialization commit: `9e1b264cd2cd14a4fbf46c5d7bce2d07a86edb63`. Refreshed main remained at
INIT_START and the exact remote topic ref was absent. Exact local-only and current-operation commit
lists contained only that initialization commit. Normal exact-ref push set upstream; local-only and
remote-only counts were 0/0. No PR or merge was performed during initialization.

GitHub independently confirmed Bridge PR #41 merged, its approved topic head and squash SHA as
reported in the handoff; local Git confirmed both trees equal `dce6ab22051b0aaf165a74b5c466e468dd801109`.

Final review adds five checks: failed construction leaves no entry and can retry; a hit and rejected
miss do not construct discarded candidates; the pool alone retains a value; an incomplete key
returns the wrong dimension; and equal payloads can belong to different specifications. Probe
contract tests now compare complete byte payloads as well as samples and placement values.
The lab remains unsolved. Runtime implementation and measured workload are unchanged apart from
formatting; the two runtime experiment outputs remain applicable.

## Final observed results — 2026-09-09

| Check | Actual result |
|---|---|
| Focused CPython 3.14.7 | 68 passed |
| Focused CPython 3.11.16 | 68 passed |
| Strict mypy | All eight source files passed 3.11 and 3.14 targets under both runtimes |
| Static contract controls | Positive clients passed; exactly nine intended negative diagnostics per target/runtime |
| Ruff | py311 lint and format passed; 12 eligible unit files |
| Python snippets | Four independent snippets parsed with 3.11 grammar, compiled and executed under both runtimes |
| Source compatibility | All eight Python files parsed with 3.11 grammar |
| Demo and unsolved starter | Ran successfully under both runtimes; starter reports incomplete |
| Controlled experiment | 36 fresh-process trials; both distributions and all outputs recorded with limits |
| Full repository regression | 1,466 passed across all 84 isolated pytest directories on CPython 3.14.7; each exited zero |
| Validator | Passed under both runtimes, including uv lock consistency and zero forbidden paths |
| Scope and whitespace | Only 12 Flyweight files and its tracker artifact cell; no whitespace errors |
| Local preservation | All 24 recorded ignored paths present and all 11 ZIP hashes unchanged before publication |

The final review approves the artifact while preserving learning Not started. No learner evidence,
retrieval date, weakness or completed attempt is invented. No source implementation changes followed
the checks; final note citations, approval and result recording are followed by validator, format/lint
and whitespace checks before commit. Runtime negatives are deliberate tests, not suppressed API flaws.

GitHub reports no main rules, no branch protection (explicit HTTP 404: Branch not protected), and
zero CI workflows. Exact PR base/head, commits, files, reviews, checks and status contexts will be
reviewed before an ordinary squash merge with a verified head. No bypass is authorized or used.
The task report carries exact final commit, PR, squash tree parity, clean Local main synchronization
and preserved artifacts. This commit will not be rewritten to contain its own hash.
