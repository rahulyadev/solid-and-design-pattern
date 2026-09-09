# Validation — SDP-STR-040

## Scope and safe baseline

Only SDP-STR-040 is authored. Its artifact cell is the only tracker change; learning remains Not
started and all learner dates, weaknesses and evidence are unchanged. The canonical contract is
Core, High/High/High, L/D2, GoF/Structural/Backend, E+I+D+T, with 4–6 h understanding and 5–9 h practice.
The exact branch is `topic/SDP-STR-040`.

`INIT_START`: `badef67fe26a94ca18eb606106b5ae932c1738f3`, recorded after branch creation and completely
empty tracked/staged/untracked porcelain status. Worktree HEAD, Local main and refreshed origin/main
all matched it. The local and remote exact topic refs were absent (remote probe exit 2); no other
Worktree owned the branch. This task was pinned before authoring. Decorator PR #38 was verified
merged at this baseline with approved head `61c60d4ed0fb151e2b500f4c4b76679fab076271`.

Restricted authentication reported an invalid token with a network error. Elevated `gh auth status`
and `gh api user --jq .login` succeeded as `rahulyadev`. The exact allowed no-tag main fetch and
exact topic probe reached origin. No broader refspec or plaintext token output was used. Shared Git
metadata required elevated filesystem permission for branch creation. No unrelated work is included.

Read: AGENTS.md, docs/WORKFLOW.md, the latest canonical entry and evidence definitions, matching
tracker and prerequisite rows, exact Python mappings, templates/unit.md, relevant foundation bridges,
existing structural standards, source/version, copyright/license and NotebookLM policies. No later
unit was initialized. The lab preserves the flawed starting behavior and leaves its target unsolved.

## Reproducible check method

The inspected existing runtimes are `/home/parry/projects/solid-and-design-pattern/.venv/bin/python`
(CPython 3.14.7) and `/tmp/sdp-cre-040/venv311/bin/python` (CPython 3.11.16). Both have mypy 1.20.2,
pytest 8.4.2 and Hypothesis 6.165.2. No unrelated environment was modified. The main environment has
no pip module; pip is not needed for these locked tools. `uv` is available for the validator's lock check.

All generated state goes under `/tmp/sdp-str-040`: Hypothesis, mypy, Ruff, pytest, uv, coverage,
bytecode, snippets and logs. Pytest's repository cache is disabled, basetemp parents are created,
and the complete regression inherits MYPY_CACHE_DIR because existing tests invoke mypy internally.
Local's 24 ignored paths and all eleven foundation ZIP SHA-256 fingerprints were recorded before
work; those approved exceptions are preserved and are never staged or treated as blockers.

Commands use these environment settings from the repository root and an existing locked Python:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-str-040/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-str-040/mypy
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-str-040/hypothesis
export RUFF_CACHE_DIR=/tmp/sdp-str-040/ruff
export UV_CACHE_DIR=/tmp/sdp-str-040/uv
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-str-040/venv
export COVERAGE_FILE=/tmp/sdp-str-040/coverage
mkdir -p /tmp/sdp-str-040/pytest
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-str-040/pytest/focused \
  units/structural/SDP-STR-040-proxy
python -m mypy --strict --python-version 3.11 units/structural/SDP-STR-040-proxy
python -m mypy --strict --python-version 3.14 units/structural/SDP-STR-040-proxy
python -m ruff check --target-version py311 units/structural/SDP-STR-040-proxy
python -m ruff format --check units/structural/SDP-STR-040-proxy
python scripts/validate_repo.py
git diff --check
```

Run pytest and both mypy targets on both runtimes. The typing tests create isolated positive and
negative source controls in pytest's temporary directory and assert exactly two assignment errors
and one argument-type error. The eight checked-in Python files are strict checked as a group.
Each of the five README Python fences is extracted independently to `/tmp`, parsed with the 3.11
grammar, compiled and executed on both runtimes with examples on PYTHONPATH. The intentional
forwarding misuse fence is executable evidence, not claimed to pass static typing.

## Maintainer review boundaries

The fixed policy orders authorization before cache and target work, bounds cache entries to one,
uses full tenant/document keys, distinguishes cache eligibility from source freshness, and assigns
explicit exclusive target ownership. Factory failure, read failure, terminal close, callback reentry
and telemetry control exceptions have separate policies. Principal/authentication and trusted typed
inputs are preconditions; no production security, remote transport, concurrency or async guarantee
is claimed. Immutability is ordinary frozen value discipline, not a hostile-code sandbox.

Nine sources were opened and read. Nearby citations distinguish design choices, Python language and
library guarantees, static typing and the runtime-checkable Protocol change in 3.12. The GoF citation
is a publisher-hosted original-author excerpt, not claimed access to the complete chapter. All
teaching material and domains are original. No learner evidence, solution, private data or license
was invented. No NotebookLM upload occurred.

The diagrams and experiment table were inspected as text; all seven observation rows are asserted
by an executable test. No browser rendering was attempted or claimed. The prior Singleton local-URL
security block was not worked around through a server, another browser or indirect execution.

## Executed initialization checks — 2026-09-09

- Focused tests: 44 passed on CPython 3.14.7 and 44 passed on CPython 3.11.16.
- Strict mypy: all eight Python files passed 3.11 and 3.14 targets on both runtimes.
- Positive/negative controls: intended Catalog and ownership accepted; bytes return, absent close,
  and Boolean policy rejected with exactly the intended three errors, both targets on both runtimes.
- Ruff lint and format passed with Python 3.11 lint target. Initial lint findings in deliberate dynamic
  access demonstrations and redundant encoding spelling were corrected, then checks were rerun.
- Five README snippets independently parsed, compiled and executed on both runtimes.
- Demo: both printed the same headline twice, then `['miss', 'hit']`.
- Controlled experiment: all seven documented rows matched on both runtimes.
- Unsolved starter: both printed `denied=True, exports=1` and `target_complete=False`; three baseline
  tests passed as part of the focused suite.

Repository validator passed, including uv lock consistency and zero forbidden paths. Its first run
correctly reported the experiment and validation links before those files had been written; after
the records were added, it passed. Diff whitespace review passed. Final review and repository
regression follow after initialization. No check failure was bypassed.

## Initialization publication and final review

Initialization commit: `edca33d8df280cca1617f154f03f3482f34537ec`. Immediately before its push, the
exact remote topic probe was still absent. The local-only list against synchronized main and the
current-operation list since INIT_START contained that identical single commit. The normal exact-ref
push set upstream; local-only/remote-only counts were 0/0 afterward. No PR or merge occurred during
initialization. Further publication uses the explicit standing authorization.

Final review adds six behavioral cases: hits do not slide expiry, denial precedes clock access,
a failed other-key load discards the former slot, principal decisions stay per proxy, real-subject
self-calls stay on the actual receiver, and root cleanup closes a constructed target after read
failure. These verify documented boundaries without exposing a lab solution. The runtime design
needed no change after initialization. The table's remote interview scenario was clarified to refer
to an operation timeout rather than conflating a read with a write.

The experiment review explicitly distinguishes its preconstructed spy and factory invocation count
from actual deferred MemoryCatalog construction in the demo. It does not measure construction cost.

## Final observed results — 2026-09-09

| Check | Actual result |
|---|---|
| CPython 3.14.7 focused suite | 50 passed |
| CPython 3.11.16 focused suite | 50 passed |
| Strict mypy | Eight Python files passed both 3.11/3.14 targets on both runtimes |
| Negative typing controls | Two assignment errors and one callback arg-type error, exactly, on both targets/runtimes; positive controls passed |
| Ruff lint/format | Passed with py311 lint target; all 12 format-eligible unit files compliant |
| README snippets | Five independently parsed with 3.11 grammar, compiled and executed on both runtimes |
| Runnable artifacts | Demo, seven-row probe and unsolved starter passed on both runtimes |
| Full repository regression | 1,278 tests passed across 78 isolated directories on CPython 3.14.7 |
| Validator | Passed, including uv lock consistency and zero forbidden paths |
| Scope and diff checks | Only this unit's paths and matching artifact cell; no whitespace errors |
| Local ignored artifacts | All 24 recorded ignored paths present; all eleven ZIP SHA-256 fingerprints unchanged before publication |

The artifact is Approved after source, contract, teaching, failure, typing, visual and independent-lab
review. Learning remains Not started; no learner evidence is inferred. Final prose clarifications
and state changes do not change the tested code. Validation and formatting are repeated for those
final documentation changes before committing.

GitHub pre-publication inspection found no main rules/protection or CI workflows. PR-specific
base/head, commits, files, check runs and status contexts must still be inspected before the normal
squash merge. Publication and synchronization results are reported in the task and PR so the approved
commit need not be rewritten to include its own hash. No failed checks are bypassed.
