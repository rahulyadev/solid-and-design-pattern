# Validation — SDP-STR-020

## Scope and initialization baseline

Only this unit's files and the matching PROGRESS.md artifact cell are in scope on
`topic/SDP-STR-020`. `INIT_START` is `c5de4ced2f486ce6d979a9fd291f3a80a7485639`, recorded after
completely clean tracked, staged, and untracked status. Detached Worktree HEAD, Local main, and
freshly fetched origin/main matched the published Adapter baseline. The exact local/remote Facade
branches were absent, with no other Worktree owning the branch. The exact branch was created from
that synchronized commit and this task was pinned.

Authentication was checked before authoring. Restricted access reported invalid authentication with
a network error; elevated `gh auth status` and `gh api user --jq .login` succeeded as `rahulyadev`.
The exact no-tag main fetch reached origin; the exact topic probe returned absent (exit 2).
No broad fetch or plaintext token output was used. Initialization does not create a PR or merge.

The curriculum entry, tracker and prerequisite rows, relevant Python-reference mappings, prerequisite
notes, unit template, workflow, source/version, rights, and NotebookLM policies were read. The metadata
preserves the canonical M/D2 scope and E+I+D+T profile. No other unit was authored or initialized.
The artifact starts Draft and learning remains Not started.

## Executed initial checks — 2026-09-09

| Check | Observed result |
|---|---|
| Focused CPython 3.14.7 tests | 33 passed |
| Focused CPython 3.11.16 tests | 33 passed |
| Strict mypy | All nine Python files, including tests, passed both 3.11 and 3.14 targets on both runtimes |
| Negative typing control | Valid Archive/PacketBuilder accepted; wrong archive return type rejected with exactly one assignment error, both targets on both runtimes |
| Ruff lint/format | Passed; 12 format-eligible files compliant |
| README Python fences | Four independently parsed for 3.11 syntax, compiled and executed on each runtime |
| Demo | Both: WEEK-1/1, 14 bytes, load/render/store, one maintenance key, one close |
| Failure probe | Both: all five scenarios matched the observation table |
| Unsolved starter | Both: CLI/dictionary baseline fits=True, target_complete=False |

Observed probe output on both runtimes:

```text
success | acknowledged | 1 | 1 | load,render,store
missing | load:not_attempted | 0 | 0 | load
render | render:not_attempted | 0 | 0 | load,render
store_before | store:unknown | 1 | 0 | load,render,store
lost_ack | store:unknown | 1 | 1 | load,render,store
```

The initial formatting pass reformatted one test signature; no failed check was bypassed. Exact
interpreter paths inspected and used: `/home/parry/projects/solid-and-design-pattern/.venv/bin/python`
(CPython 3.14.7) and `/tmp/sdp-cre-040/venv311/bin/python` (CPython 3.11.16). Existing environments were
not modified. All generated state is routed to `/tmp/sdp-str-020`: Hypothesis, mypy, Ruff, uv, pytest,
coverage, bytecode, snippets, and logs. Pytest's cache provider is disabled, custom basetemp parents
exist, and the complete regression must inherit MYPY_CACHE_DIR for tests that call mypy internally.

Local's 24 ignored paths and all eleven foundation ZIP SHA-256 fingerprints were recorded before
authoring. These approved unrelated artifacts are preserved, not staged, and not blockers. Validation
is performed in the dedicated Worktree.

## Review and evidence limits

The text diagrams and observation table are conceptual/readable directly. No browser rendering was
performed or claimed. The earlier local-URL browser block in Singleton was not worked around and
Adapter's text-only evidence is kept distinct from rendering.

The original synthetic report example has a documented input, output, effect, error, ordering, trust,
and lifetime contract. Fault tests show no automatic retry and a write whose acknowledgement is lost.
The archive is in-memory, sequential, and non-durable, with infallible close. No live vendor, security
implementation, concurrent/async execution, transaction, cancellation, or performance result is claimed.

Sources were actually read and cited near subtle claims. The GoF intent attribution explicitly uses
the publisher's Shalloway/Trott account, not an assertion that the original book chapter was read.
No copied diagrams, external implementation, license addition, or learner evidence is included.
The independent preflight lab is unsolved; its baseline tests do not certify completion.

Initial repository validation passed, including uv lock consistency and zero forbidden paths.
Whitespace review passed. The tracker diff changes only this unit's Absent → Draft artifact cell;
all learning, dates, weaknesses, and evidence cells remain unchanged. Scoped code, notes, lab boundaries,
and source/rights claims were reviewed before the initialization commit.
