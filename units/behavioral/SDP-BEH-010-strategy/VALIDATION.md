# Validation — SDP-BEH-010 Strategy

## Scope and baseline

Only this unit and its matching tracker artifact cell are in scope. Learning remains Not started;
no learner attempt, review date or evidence is invented. The unit uses the unit/practice templates
with E+I+D+T artifacts. An experiment template was inspected but no X requirement or benchmark is
added. Visuals are conceptual text diagrams and an observation table; no browser rendering is
attempted or claimed. No subagent or parallel curriculum authoring is used.

`INIT_START` is `56dae05b61701bd14e620fbcf379719aa841d343`. HEAD, Local main and origin/main matched
that synchronized baseline, the Worktree was fully clean, and neither exact Strategy ref existed.
The exact main no-tag fetch succeeded; the exact topic probe reached origin and returned absent.
The dedicated branch is `topic/SDP-BEH-010`. It was created from that baseline and the task pinned.

GitHub independently confirmed Flyweight PR #42 merged at this baseline, with approved topic head
`b3a4acbf532e193310c55149eae74dac224a134f`. Both predecessor trees equal
`e1326cd6ed7ae7f0478cbfd58b9b546408132384`. The baseline repository validator passed, including uv
lock consistency and zero forbidden paths.

The restricted authentication check reported invalid token together with network failure. Elevated
`gh auth status` and `gh api user --jq .login` succeeded as rahulyadev; no plaintext token was
exposed. Elevated Git permission is needed for network and shared metadata outside the Worktree.
After interruption, authentication and exact-ref checks were repeated successfully; branch/baseline
remained unchanged and clean before initialization content was written on 2026-09-10.

Independent preservation evidence is in `/tmp/sdp-beh-010/local-artifacts-before.json`: 24 ignored
Local paths and SHA-256 hashes for 11 foundation ZIPs. No unrelated Local environment or artifact
is modified. Read: AGENTS.md, workflow, matching curriculum/progress rows, prerequisite rows and
Python mappings, applicable templates, source/version, rights and NotebookLM policies, and recent
unit standards. Source availability limits are disclosed beside the affected claims in the note.

## Reproduction environment and commands

Verified installed runtimes: `/home/parry/projects/solid-and-design-pattern/.venv/bin/python`
(CPython 3.14.7) and `/tmp/sdp-cre-040/venv311/bin/python` (CPython 3.11.16).
Both have pytest 8.4.2, mypy 1.20.2, Ruff 0.16.1 and Hypothesis 6.165.2.

Use the selected interpreter as `python` below. Export these controls for the entire regression,
including existing tests that launch mypy internally:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-beh-010/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-beh-010/mypy
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-beh-010/hypothesis
export RUFF_CACHE_DIR=/tmp/sdp-beh-010/ruff
export UV_CACHE_DIR=/tmp/sdp-beh-010/uv
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-beh-010/venv
export COVERAGE_FILE=/tmp/sdp-beh-010/coverage
mkdir -p /tmp/sdp-beh-010/pytest
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-beh-010/pytest/focused \
  units/behavioral/SDP-BEH-010-strategy
python -m mypy --strict --python-version 3.11 units/behavioral/SDP-BEH-010-strategy
python -m mypy --strict --python-version 3.14 units/behavioral/SDP-BEH-010-strategy
python -m ruff check --target-version py311 units/behavioral/SDP-BEH-010-strategy
python -m ruff format --check units/behavioral/SDP-BEH-010-strategy
python units/behavioral/SDP-BEH-010-strategy/examples/run_strategy_demo.py
python units/behavioral/SDP-BEH-010-strategy/practice/packing_lab.py
python scripts/validate_repo.py
git diff --check
```

Use distinct cache/basetemp paths for independent simultaneous checks. Extract each README Python
fence into `/tmp`, parse with the 3.11 grammar, then compile/execute independently on both runtimes
with `examples/` on PYTHONPATH. Parse all source files with the same grammar. For repository
regression, run each pytest directory independently to avoid collisions among educational modules.

## Manual review boundaries

The common context checks a complete ID permutation; policy-specific tests check algorithm meaning.
The result checks cannot enforce purity or reverse arbitrary policy effects. Typed tuple/Job inputs
and normal frozen APIs are preconditions. Callable objects, closures and method objects share the
same core in the worked comparison; shipping all forms is not recommended. The independent packing
lab remains unsolved, with baseline tests only and no hidden comparison solution or hints.

## Initialization checks — 2026-09-10

Both CPython 3.14.7 and 3.11.16 passed 66 focused tests. These include the positive static clients
and exactly ten intended negative diagnostics under each 3.11/3.14 typing target. Strict mypy passed
all seven source files for both targets on both runtimes. Ruff py311 lint and formatting passed
(ten eligible files). Initial lint found three long lines; imports were split and formatting fixed
before these successful checks. No check failure was bypassed.

All seven source files parsed with Python 3.11 grammar. Four independent README Python snippets
parsed with that grammar, compiled and executed on both runtimes. The demo printed:

```text
arrival: ids=(7, 2, 9, 5); pages=15
fewest: ids=(5, 2, 9, 7); pages=15
small: ids=(2, 9, 5, 7); pages=15
callable object == method object: True
```

The separate starter printed `((6,), (6, 4), (4,))` and `target_complete=False` under both runtimes.
Both validator runs passed, including uv lock consistency and zero forbidden paths. Whitespace
checks passed; scoped review found only ten unit files and the matching Draft tracker cell.
Logs and extracted snippets are under `/tmp/sdp-beh-010/init314` and `init311`.

The complete Draft material is ready for its initialization commit and current-operation-only push
proof. Final artifact approval awaits final review and repository regression. Initialization does
not create a PR or merge, and these author checks do not advance learning state.

## Initialization publication and final review

Initialization commit: `4ffaea1cef9b5dad88e8aaff2e388ed27d1be9cb`. Immediately before push,
the exact no-tag main refresh still matched INIT_START and the topic probe returned absent.
The local-only commit list and current-operation list were identical and contained only that
commit. Normal exact-ref push set upstream; local-only/remote-only counts were 0/0. No PR or merge
occurred during initialization.

Final review adds four targeted cases: equal-page ties with IDs in descending arrival order,
the exact 64-job/6400-page limit and extreme valid IDs, invented output for an empty batch, and an
independent method-based policy with no implementation inheritance. The tie case matters because
generated IDs ascend in input order and therefore cannot alone expose an accidental numeric-ID
tiebreaker. Runtime implementation and the unsolved starter remain unchanged.

## Final observed results — 2026-09-10

| Check | Actual result |
|---|---|
| Focused CPython 3.14.7 | 70 passed |
| Focused CPython 3.11.16 | 70 passed |
| Strict mypy | All seven Python files passed 3.11 and 3.14 targets on both runtimes |
| Static contract controls | Positive clients passed; exactly ten intended negative diagnostics per target/runtime |
| Ruff | py311 lint and format checks passed; ten eligible unit files |
| README Python | Four independent snippets parsed with 3.11 grammar, compiled and executed on both runtimes |
| Source compatibility | All seven Python files parsed with 3.11 grammar |
| Demo and lab | Both ran on both runtimes; exact demo rows above; starter remains incomplete |
| Repository regression | 1,536 passed across all 86 isolated pytest directories on CPython 3.14.7; every exit zero |
| Repository validator | Passed on both runtimes, including uv lock consistency and zero forbidden paths |
| Scope and whitespace | Only ten unit files and the Strategy tracker artifact cell; no whitespace errors |
| Local preservation before publication | All 24 ignored paths present; all 11 ZIP hashes unchanged; Local main clean |

The runtime platform is Linux 7.0.0-31-generic x86_64 with glibc 2.43. Focused logs and extracted
snippets are under `/tmp/sdp-beh-010/final314` and `final311`; per-directory regression results are
under `/tmp/sdp-beh-010/regression`. All tracked pytest directories were included, with none outside
`units/`. No generated state appeared in the dedicated Worktree.

The final review approves the artifact while preserving learning Not started and the unsolved lab.
After the successful code checks, only citation precision, approval cells and this result record
changed; final validator, format/lint and whitespace checks precede commit. No learner evidence or
performance result is inferred from author verification.

GitHub currently reports no main rules, no branch protection (explicit HTTP 404: Branch not
protected), and zero CI workflows. Publication uses a normal push, exact PR base/head/commit/file
review and a verified-head squash merge after checking current reviews, statuses and check runs.
No bypass or force-push is authorized. The task report records final commit/PR/merge IDs, tree parity,
safe Local main synchronization and artifact preservation without rewriting this commit to include
its own hash.
