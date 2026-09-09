# Validation — SDP-STR-060

## Scope and initialization baseline

Only Bridge and its matching tracker artifact cell are changed. Canonical contract: Professional,
Medium/Medium/Medium, L/D2, GoF/Structural, E+I+D+T; 4–6 h understanding, 5–9 h practice. Learning
remains Not started. No learner evidence, dates or weaknesses are supplied by generated content.

`topic/SDP-STR-060` starts at `0dcbf6b00a775e8a85ac2bec5408b7bd784eff7a`, recorded as INIT_START
only after branch creation and fully empty tracked/staged/untracked porcelain status. HEAD, Local
main and refreshed origin/main matched. Exact local and remote Bridge refs were absent (remote
probe exit 2), and no other Worktree owned the branch. This task is pinned.

Elevated `gh auth status` and `gh api user --jq .login` succeeded as `rahulyadev` after the restricted
network reported an invalid token together with a connection error. The required exact no-tag main
fetch and exact topic probe reached origin. No plaintext token was printed. Shared Git metadata
needed elevated filesystem access for branch creation.

Predecessor PR #40 is merged: topic `7d5c38314133ddf3356aa7cc20586969d893640a`, squash
`0dcbf6b00a775e8a85ac2bec5408b7bd784eff7a`, equal trees
`1a40d4378f625f2ef51a245998308b4ebcf2bce0`. The clean synchronized baseline passed the validator,
including uv lock consistency and zero forbidden paths. Local's 24 ignored paths and 11 foundation
ZIP SHA-256 hashes are snapshotted at `/tmp/sdp-str-060/local-artifacts-before.json` for preservation.

Read: AGENTS.md, workflow, canonical entry, matching and hard prerequisite tracker rows, Python
reference mappings, unit/practice/experiment templates, structural-unit standards, source/version,
copyright/license and NotebookLM policies. No later unit is authored and no subagent is used.

## Maintainer review boundaries

The worked example separates report selection from text encoding. The four supported pairs share
an ordered bounded Table contract. Tuple/string types are a typed caller precondition; runtime
validation checks domain values, not hostile object construction or arbitrary deserialization.
The ordinary frozen API does not freeze borrowed collaborators. Direct `project` calls bypass
`render` request checks. Static `final` does not enforce runtime override restrictions.

The starter trail-guide lab remains unsolved. Baseline tests do not certify its missing combinations.
No hints, comparison solution or fabricated attempt are added. Sources are actually read and cited
near subtle claims. No copyright example, private data, license change or NotebookLM upload occurs.
Diagrams are conceptual text with reading guides and limits; browser rendering is not claimed or
attempted. Earlier local-URL blocks are not worked around.

## Reproduction environment and commands

Existing runtimes inspected: `/home/parry/projects/solid-and-design-pattern/.venv/bin/python`
(CPython 3.14.7) and `/tmp/sdp-cre-040/venv311/bin/python` (CPython 3.11.16). Neither environment is
modified. Generated caches, snippets, logs, bytecode and test state are routed to `/tmp`.

From the repository root with either selected Python:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-str-060/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-str-060/mypy
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-str-060/hypothesis
export RUFF_CACHE_DIR=/tmp/sdp-str-060/ruff
export UV_CACHE_DIR=/tmp/sdp-str-060/uv
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-str-060/venv
export COVERAGE_FILE=/tmp/sdp-str-060/coverage
mkdir -p /tmp/sdp-str-060/pytest
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-str-060/pytest/focused \
  units/structural/SDP-STR-060-bridge
python -m mypy --strict --python-version 3.11 units/structural/SDP-STR-060-bridge
python -m mypy --strict --python-version 3.14 units/structural/SDP-STR-060-bridge
python -m ruff check --target-version py311 units/structural/SDP-STR-060-bridge
python -m ruff format --check units/structural/SDP-STR-060-bridge
python units/structural/SDP-STR-060-bridge/examples/run_bridge_demo.py
python units/structural/SDP-STR-060-bridge/examples/matrix_probe.py
python units/structural/SDP-STR-060-bridge/practice/trail_lab.py
python scripts/validate_repo.py
git diff --check
```

Use distinct cache and basetemp suffixes for concurrent processes. Repository regression must run
each pytest directory independently to avoid existing module-name collisions, with MYPY_CACHE_DIR
exported for tests that launch mypy themselves. All Python README fences are extracted independently
to `/tmp`, parsed with the Python 3.11 grammar, compiled and executed on both runtimes with the
unit examples directory on PYTHONPATH. Shell fences are command guides, not Python snippets.

Static contract tests compile positive and negative clients for both target versions under each
runtime. The final seven expected diagnostics are wrong result type, missing encode, extra required argument,
frozen encoder replacement, nonexistent close, list instead of tuple input and final-method override. Bad clients are
never executed. Behavioral tests separately expose a statically valid but semantically wrong encoder.

## Controlled matrix probe

Question: does changing encoding preserve the report's selected rows, and how often is the encoder
actually called? Classification: design-level collaboration observed through Python method calls.
Hypothesis: each report/encoder pair calls encode once; selection changes row count from two to one.

Controlled: two stock records, report contracts and Table representation. Changed: report policy
and encoding. Measured: Table row count received by a recording collaborator and actual call count.
The recording encoder delegates to real CSV/JSON encoders; round-trip semantic checks are separate
behavioral tests. Reproduction command appears above. This is not a construction or speed benchmark.
No resource-lifetime, network, concurrency or future-format conclusion follows from four observations.

## Initialization observations — 2026-09-09

53 focused tests passed on each runtime. Strict mypy passed all seven Python files for both 3.11
and 3.14 targets on each runtime; positive clients passed and exactly six negative diagnostics were
asserted. Ruff py311 lint and formatting passed (10 format-eligible files). All four independent
README Python snippets parsed under the 3.11 grammar, compiled and executed on both runtimes.
The demo, matrix probe and unsolved starter ran on both runtimes with the same deterministic output.
The validator passed including uv lock consistency and zero forbidden paths; whitespace checks passed.

Environment: Linux x86_64, CPython 3.14.7 and 3.11.16, both built with Clang 22.1.3; pytest 8.4.2,
mypy 1.20.2, Ruff 0.16.1, Hypothesis 6.165.2. No unrelated environment was modified.

Observed probe output on both runtimes:

```text
InventoryReport/CsvEncoder: rows=2, calls=1
InventoryReport/JsonEncoder: rows=2, calls=1
ShortageReport/CsvEncoder: rows=1, calls=1
ShortageReport/JsonEncoder: rows=1, calls=1
```

Read each line as the selected pair followed by rows handed to the encoder and real call count.
The insight is that encoding choice preserved projection row count with one delegation. The limit
is this controlled two-record input and these four implementations, not arbitrary plugin behavior.
Contract tests supply the stronger cell-level comparison. No browser rendering or timing occurred.
The starter printed `Pond -> Tower -> Grove` and `target_complete=False`; it remains unsolved.

Initial lint findings were long lines and a Unicode multiplication sign in a docstring; these were
corrected. Review selected explicit CRLF CSV record endings to preserve carriage returns as data.
No failed check was bypassed. Initial content is complete study material and remains Draft pending
final review and repository regression. Initialization publication will use the exact current-operation
commit enumeration; it will not create a PR or merge.


## Initialization publication and final review

Initialization commit: `9187fc134c120879c5b08dc9623c34d9f3ad3ab9`. Refreshed main remained at
INIT_START and the exact remote Bridge ref was still absent. Both exact local-only and
current-operation lists contained that single commit. Normal exact-ref push set upstream and
local-only/remote-only counts were 0/0. No PR or merge occurred during initialization.

Final review adds isolated CR, LF and CRLF cell preservation, bounded generated-text round trips
(40 examples per encoder, deterministic Hypothesis settings), mixed shortage boundary/order, and
normal frozen Table mutation checks. A seventh negative typing diagnostic checks overriding final
render. The simple direct-function snippet now uses the same explicit CRLF convention. The 3.14
annotation note explicitly distinguishes the retained future import from the new default semantics.
No worked runtime behavior or learner starter solution is changed by this review.


## Final observed results — 2026-09-09

| Check | Actual result |
|---|---|
| Focused CPython 3.14.7 suite | 63 passed |
| Focused CPython 3.11.16 suite | 63 passed |
| Strict mypy | All seven Python files passed both 3.11 and 3.14 targets on both runtimes |
| Static contract controls | Positive clients accepted; exactly seven intended negative diagnostics per target/runtime |
| Ruff | py311 lint and formatting passed; 10 format-eligible unit files |
| Python fences | Four independent README snippets parsed with 3.11 grammar, compiled and executed on both runtimes |
| Source compatibility | All seven Python source files also parsed with 3.11 grammar |
| Runnable artifacts | Demo, matrix probe and unsolved starter succeeded on both runtimes |
| Generated-text contract tests | 40 deterministic Hypothesis examples per encoder in each focused runtime suite |
| Repository regression | 1,398 passed across 82 isolated pytest directories on CPython 3.14.7; every directory exited zero |
| Repository validator | Passed, including uv lock consistency and zero forbidden paths |
| Scope and whitespace | Exactly 11 paths versus main: 10 Bridge artifacts and only its tracker artifact cell |
| Unrelated Local artifacts | All 24 recorded ignored paths present; all 11 ZIP SHA-256 fingerprints unchanged |

Artifact Approved follows source, pedagogy, contract, typing, failure, lab and regression review.
Learning stays Not started; no learner attempt, retrieval, date or weakness is fabricated. All
runtime code is unchanged from the validated initialization. Final review changed tests and notes.
Final approval/result edits are followed by validator, lint/format and whitespace checks before commit.

GitHub currently reports no main rules, no branch protection (explicit HTTP 404: Branch not protected)
and zero CI workflows. Exact PR base/head, commits, files, reviews, checks and status contexts must
also be inspected before squash merge. The exact final commit, PR, merge tree parity and safe Local
main synchronization are reported in the task; this commit is not rewritten to contain its own hash.
No failed check, protection or unrelated change is bypassed.
