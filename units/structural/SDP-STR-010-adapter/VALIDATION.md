# Validation — SDP-STR-010

## Scope and clean initialization baseline

Only `topic/SDP-STR-010`, this unit's files, and its matching PROGRESS.md artifact cell are in scope.
`INIT_START` is `5ea75a0c51b6e097eaa1909d6c90a9a7c7ea7e0a`, recorded after completely clean tracked,
staged, and untracked status. Detached Worktree HEAD, Local main, and freshly fetched origin/main
all identified that published Singleton baseline. Its tree matched the approved predecessor topic
tree `39f663baeaae8fd3523f7ef79715b48503d8034c`. No local or remote Adapter branch existed and no
other Worktree owned it. The exact branch was created at this baseline and the task pinned.

Authentication was checked before authoring. The restricted sandbox reported invalid authentication
with a network error; the elevated preflight succeeded as `rahulyadev`. The exact no-tag main fetch
succeeded and the exact remote topic probe returned absent (exit 2). No broad fetch, history rewrite,
or plaintext credential output was used. No PR or merge belongs to initialization.

The canonical entry, tracker and prerequisite rows, Python reference mappings, existing prerequisite
notes, template, workflow, source/version, copyright/license, and NotebookLM policies were read.
Adapter is the sole immediate successor to published SDP-CRE-050. No later unit is authored or
initialized. The artifact starts Draft; all learning cells remain Not started/unchanged.

## Executed initialization checks

Executed on 2026-09-09 in the dedicated Worktree:

| Check | Observed result |
|---|---|
| CPython 3.14.7 focused tests | 60 passed |
| CPython 3.11.16 focused tests | 60 passed |
| Positive/negative Protocol assignment | Positive semantic counterexample accepted; wrong method rejected with exactly one assignment error for both target versions on both runtimes |
| Strict mypy | Six non-test sources passed for both 3.11/3.14 targets on both runtimes |
| Ruff lint/format | Passed; 13 format-eligible files compliant |
| README Python snippets | Five independently compiled/executed on each runtime |
| Demo | Both: enough, unknown, short, queries=3, closes=1 |
| Probe | Both: converted_units=12, converted_decision=enough, signature_only_decision=short, runtime_shape_accepts_wrong_signature=True, actual_call_raises_type_error=True |
| Unsolved starter | Both: NORTH: 7 min; target_complete=False |
| Repository validator | Passed, including uv lock consistency and zero forbidden paths |
| Whitespace/scope | git diff --check passed; only this unit and exact Absent → Draft tracker cell changed |

The initial lint check found two long lines and import/style issues; formatting fixed them. The
initial probe deliberately made a statically invalid call, which mypy rejected. The probe now calls
through a runtime-checkable Protocol after narrowing from object, demonstrating that a shallow
presence check can permit a runtime call failure. The negative test independently verifies static
rejection. No failing check was bypassed and no broad type suppression was added.

Existing runtimes were inspected at `/home/parry/projects/solid-and-design-pattern/.venv/bin/python`
and `/tmp/sdp-cre-040/venv311/bin/python`; neither environment was changed. All generated state uses
task-owned `/tmp/sdp-str-010`: Hypothesis, mypy, Ruff, pytest temporary files, uv, coverage, bytecode,
snippets, and logs. Pytest's cache provider is disabled and basetemp parents exist. The complete
regression must inherit MYPY_CACHE_DIR because existing tests invoke mypy internally.

The Local checkout's 24 ignored paths and 11 foundation ZIP SHA-256 fingerprints were inventoried
under `/tmp` before edits. These approved unrelated artifacts are preserved, never staged or
published, and are not blockers. Validation is run in the dedicated Worktree.

## Teaching and evidence limits

The source examples, diagrams, payloads, and route lab are original and synthetic. The publisher's
Adapter excerpt and relevant official Python/typing sections were actually read and cited near
subtle claims. No copied diagrams, proprietary data, license addition, or learner evidence is included.

The note contains conceptual text diagrams and a five-field observation table. No browser-specific
visual is required; browser rendering is not claimed. The predecessor's blocked local-URL rendering
does not count as rendered evidence here. No server, alternate browser, or indirect workaround is used.

The synthetic SDK is sequential and has infallible close. No live vendor, network transport,
async/cancellation, concurrency stress, performance benchmark, or secret-free traceback claim is
made. The unit states where those contracts need further evidence. The separate lab remains
unsolved; maintainer execution does not advance learning state.
