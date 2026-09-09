# Validation — SDP-STR-030

## Scope and baseline

This operation authors only SDP-STR-030 and changes only its artifact-state cell in PROGRESS.md.
`INIT_START` is `63c9a0bf20e649ae5fdfbdf24fb17a762d69a61c`, recorded after the exact
`topic/SDP-STR-030` branch was created and tracked/staged/untracked porcelain status produced no
output. Worktree HEAD, Local main, and freshly fetched origin/main identified that same baseline.
The exact local and remote topic refs were absent and no other Worktree owned the branch.
The task was pinned before authoring. No older local work is included.

Before authoring, restricted `gh auth status` failed with a network error; elevated authentication
and `gh api user --jq .login` succeeded as `rahulyadev`. The exact allowed no-tag main fetch reached
origin; the exact topic probe returned absent (exit 2). No broad refspec or plaintext token output
was used. GitHub verified Facade PR #37 merged at the baseline with approved topic head
`519b038951d51aeb7c5509890036386cc1e7062f`. A mistyped commit reference failed without changing
state; branch creation then used the verified main ref. Git metadata required elevated filesystem
permission because the shared repository metadata lives outside the dedicated Worktree.

Read: AGENTS.md, workflow, canonical Decorator entry and evidence definitions, matching progress
and prerequisite rows, relevant Python-reference mappings, the unit template, applicable source,
rights and NotebookLM policies, existing structural-unit standards, and the composition prerequisite
notes. No other unit was initialized. Metadata preserves L/D2 and E+I+D+T. The artifact is initially
Draft and learning remains Not started, with all learner dates/weaknesses/evidence unchanged.

## Validation method

The existing interpreters were inspected rather than assumed:

- `/home/parry/projects/solid-and-design-pattern/.venv/bin/python`: CPython 3.14.7.
- `/tmp/sdp-cre-040/venv311/bin/python`: CPython 3.11.16.

Existing environments are not modified. All generated state goes under `/tmp/sdp-str-030`, including
Hypothesis, mypy, Ruff, pytest basetemp, uv, coverage, bytecode, snippets and logs. Pytest's repository
cache provider is disabled and basetemp parent directories are created. The complete regression
inherits MYPY_CACHE_DIR because some previously published tests invoke mypy internally.
Local's 24 ignored paths and all eleven foundation ZIP SHA-256 fingerprints were recorded before
work. They are approved unrelated artifacts, preserved and never staged or treated as blockers.

The checks run the ten Python source files through strict mypy for 3.11 and 3.14 targets on each
runtime; run the focused suite including positive/negative assignment and function-call controls;
run Ruff lint/format; independently parse all five README Python fences with the 3.11 grammar and
compile/execute them on each interpreter; and run the demo, object-order/effects probe,
function-order probe and unsolved starter. Results are appended after observed completion.

## Review boundaries

The examples are original synthetic notices and parcel quotes. The separate lab starts unsolved;
baseline tests preserve current behavior and confirm the target raises NotImplementedError. No
solution, learner attempt, personal evidence, private input, license decision, or upload was invented.

Sources were opened and read; subtle claims are linked near their use. The GoF source is an
original-author publisher excerpt discussing related patterns, not claimed access to the complete
Decorator chapter. Language, library, static typing, design choices, and interpreter observations
are distinguished. Metadata and shape do not prove semantic substitutability.

Text diagrams and observation tables are conceptual and were inspected as text. No browser
rendering was attempted or claimed. The earlier Singleton local-URL security block was not worked
around through a server or alternate path. Adapter/Facade text evidence remains a distinct kind of
verification. No concurrency, async cancellation, durable audit, secure rendering, live service,
resource-handle cleanup, or performance measurement is claimed here.

## Executed initialization checks — 2026-09-09

| Check | Actual result |
|---|---|
| Focused CPython 3.14.7 tests | 39 passed |
| Focused CPython 3.11.16 tests | 39 passed |
| Strict mypy | All ten Python files passed both 3.11 and 3.14 targets on both runtimes |
| Positive/negative typing | Good TextSource stack and typed wrapper accepted; bytes-returning source and integer argument rejected with exactly assignment and arg-type errors, both targets on both runtimes |
| Ruff lint/format | Passed with Python 3.11 compatibility target; 13 format-eligible files compliant |
| README Python snippets | Five independently parsed for 3.11 syntax, compiled and executed on both runtimes |
| Demo | Both: `[note: ready]`, success observation with 13 characters, one call and one close |
| Controlled probes | Both: seven object/effect/lifetime rows and all nine function phases matched the documented outputs |
| Unsolved lab | Both: plain=400, combined=500, target_complete=False; four baseline tests passed |
| Repository validator | Passed, including uv lock consistency and zero forbidden paths |
| Diff check | Passed; only this unit's artifact cell changes in PROGRESS.md |

The initial formatting pass corrected long test lines. Strict typing identified a statically
non-overlapping identity assertion; it was replaced by an explicit id comparison for the runtime
identity observation. The special-method test uses an intentionally false Sized cast to demonstrate
that a static cast cannot supply runtime behavior. Checks were rerun successfully; no failure was
bypassed. Maintainer review covered the source and exception boundaries, layer ordering, snapshot
and borrowed ownership, type/metadata limits, original sources, conceptual diagrams, and independent
unsolved lab. The artifact remains Draft until final review and regression.
