# Practice — SDP-PYT-040 iterators, generators, and context managers

| Field | Value |
|---|---|
| Unit note | [SDP-PYT-040](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-pyt-040) |
| Evidence target | E+I+D+X+T |
| Attempt required before solution | Yes |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-040-iterators-generators-context-managers/practice` |
| Status | Not attempted |

## Learning question

Can you separate lazy traversal from resource ownership so a caller can stop early without hidden
pre-consumption, while every successfully acquired archive still exits under an explicit policy?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

Complete the stages in order. The green starter tests characterize the legacy design only; they
do not prove the target design.

## Starter files

- [incident_archive_lab.py](incident_archive_lab.py): runnable eager export with handwritten
  cleanup.
- [test_incident_archive_lab.py](test_incident_archive_lab.py): phase-A characterization tests.

The worked alert-stream example uses another synthetic domain. This folder contains no target
implementation, hidden solution, released hint, or fabricated learner evidence.

## Problem and change pressure

An incident-reporting job receives an iterable, selects records at or above a priority threshold,
formats rows, writes them to a closeable archive, and returns the exported rows. The current code
materializes the complete source before writing and owns cleanup with `try/finally`.

New callers need two things:

1. inspect or consume selected rows one at a time, possibly stopping early; and
2. use the same export flow with a resource whose acquisition and exit policy are explicit.

The exercise is not “replace every loop with `yield`.” It is to decide which boundary owns
traversal state, which boundary drives it, and which boundary owns deterministic cleanup.

All records and failures are synthetic. The starter writes to memory and performs no file,
database, network, message, or framework operation.

## Legacy observable contract

| Dimension | Required observation |
|---|---|
| Selection | Include priorities greater than or equal to the exact threshold. |
| Result | Return formatted rows as a tuple in encounter order. |
| Duplicates | Preserve them. |
| Text | Preserve blank text, Unicode, spaces, colons, and literal pipes. |
| Mutation | Do not mutate input records. |
| Valid empty input | Return an empty tuple and close the archive exactly once. |
| Invalid threshold | Reject before touching the source or archive. |
| Source failure | The eager legacy version writes nothing and does not close an unacquired archive. |
| Archive failure | Preserve successful earlier writes, propagate the same failure, and close once. |
| Ownership | The function owns the supplied archive after validation starts. |

These are compatibility observations, not claims that the design is ideal.

## Prediction before running

Without running the code, record:

1. whether constructing a generator function result executes its body;
2. which source items the starter consumes before its first archive write;
3. what happens to the archive if materializing the source raises;
4. whether `break` from a `for` loop automatically calls `close()` on an arbitrary iterator;
5. whether an iterator can normally be traversed twice; and
6. what `__exit__()` must return to suppress a body exception.

No learner prediction has been recorded by the maintainer.

## Phase A — expose lazy traversal

Preserve `Incident`, `Archive`, and the existing `export_priority_incidents(...)` behavior. Add the
smallest separate traversal boundary that can yield qualifying formatted rows one at a time.

Your tests must demonstrate:

- creation does not consume the source;
- one request consumes only enough input to produce one selected row;
- order, duplicates, exact threshold, text, and one-pass sources are preserved;
- a source exception occurs when that point is requested, after already-yielded rows remain
  observed;
- the returned value is one-shot when it is an iterator; and
- a second call can create a fresh iterator when the original source is reusable.

Do not add a custom iterator class unless you need multiple independent cursors or explicit
methods beyond the generator protocol. Do not cache every row merely to make a one-shot iterator
appear reusable.

## Phase B — make resource ownership explicit

Refactor archive acquisition and cleanup behind a context manager. Decide whether the context
manager receives an already-created archive or a factory, and document the ownership consequence.
Preserve the compatibility function as an eager boundary that fully drives the lazy traversal
inside the archive context.

Add focused tests for:

- normal exit;
- an empty traversal;
- source failure after at least one successful write;
- archive write failure after at least one successful write;
- failed entry or factory creation;
- cleanup failure and its relationship to a body failure;
- exception identity when cleanup succeeds;
- exactly one exit for every successful entry; and
- no exit call when entry never returns successfully.

Suppression must be narrow and intentional. A normal resource manager should usually propagate
body failures by returning false or `None`; do not use broad suppression to make tests green.

## Required edge cases

- Thresholds `0`, an exact match, and an invalid negative value.
- Empty, singleton, duplicate, and one-pass sources.
- Long skipped prefixes before the first selected record.
- Blank and Unicode identifiers or summaries.
- A source that raises before its first item and after a yielded item.
- An archive that raises before any successful write and after one successful write.
- Early consumer stop with a still-referenced iterator.
- Repeated `next()` after exhaustion.
- Two independent traversals over a reusable source.
- Two attempts over the same one-shot source.
- A close operation that raises.

Add one meaningful case of your own and explain what caller promise it protects.

## Commands

Run from a clean dedicated Worktree. Keep environments and caches outside the repository because
the validator also inspects ignored paths:

```bash
SDP_PYT_040_TOOLS=$(mktemp -d /tmp/sdp-pyt-040-tools.XXXXXX)
export UV_PROJECT_ENVIRONMENT="$SDP_PYT_040_TOOLS/venv"
export UV_PYTHON_INSTALL_DIR="$SDP_PYT_040_TOOLS/python"
export UV_CACHE_DIR="$SDP_PYT_040_TOOLS/uv-cache"
export MYPY_CACHE_DIR="$SDP_PYT_040_TOOLS/mypy-cache"
export HYPOTHESIS_STORAGE_DIRECTORY="$SDP_PYT_040_TOOLS/hypothesis"
export PYTHONDONTWRITEBYTECODE=1

uv sync --locked --group dev
uv run --locked python units/pythonic/SDP-PYT-040-iterators-generators-context-managers/practice/incident_archive_lab.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-040-iterators-generators-context-managers
uv run --locked ruff check --no-cache units/pythonic/SDP-PYT-040-iterators-generators-context-managers
uv run --locked ruff format --check --no-cache units/pythonic/SDP-PYT-040-iterators-generators-context-managers
uv run --locked mypy units/pythonic/SDP-PYT-040-iterators-generators-context-managers
UV_CACHE_DIR="$SDP_PYT_040_TOOLS/uv-cache" python scripts/validate_repo.py
```

Use a separate external environment and `--python 3.11` for the interview-compatibility run. Pass
`--python-version 3.11` to mypy and record the runtime actually used.

## Observe and explain

After running, draw two timelines:

```text
consumer next ─► source reads ─► selected row ─► consumer
enter ─► drive traversal and writes ─► exit(exception state) ─► propagate/suppress
```

Explain why a lazy pipeline can delay parsing and failures, why it is usually one-shot, why
resource cleanup is not implied by laziness, and why materializing at an intentional API boundary
can still be the correct choice.

## Refactor record

Preserve your original attempt. Record:

- the change pressure;
- iterable versus iterator promises;
- the point where work begins;
- the point where errors appear;
- who owns the archive;
- how entry, normal exit, body failure, and cleanup failure behave;
- the simplest rejected design; and
- the condition that would justify a custom iterator class, `ExitStack`, async iteration, or an
  external streaming system.

## Progressive hints and review

No hints have been released and no learner review has occurred. After preserving an attempt, ask
for one hint at a time. Review must identify the first missing reasoning step with one focused
counterexample before replacement code is offered.

## Vary — backend transfer

The source becomes a database cursor and the archive becomes an object-store multipart upload.
Propose where transaction lifetime, cursor closure, cancellation, timeouts, partial writes,
idempotency, metrics, and retry ownership belong. Explain why neither a generator nor a context
manager alone promises rollback, retry safety, backpressure, or cross-process durability.

Do not implement a real database, object store, web framework, broker, or async client in this
unit.

## Interview checkpoint

Ask one question at a time, beginning: **“What is the difference between an iterable and an
iterator, and why does it matter to an API?”** Wait before probing laziness, exhaustion, cleanup,
exception suppression, or alternatives.

## Troubleshooting

- Starter tests are expected to pass; the design exercise remains unsolved.
- Code before the first `yield` in a generator function still waits until iteration begins.
- A generator object returns itself from `iter(...)`; a container normally returns fresh iterators.
- `break` ends a loop, but it is not a general resource-lifetime protocol.
- Keep lazy consumption inside the lifetime of any resource it needs.
- Do not depend on immediate garbage collection for cleanup.
- Hyphenated unit directories are not importable package names; run the documented paths.
- Publication of maintainer artifacts does not establish learner practice or recall.

## Closure requirements

Only after Rahul closes the exercise: link the preserved prediction and attempt; record prediction
versus observation; pass characterization and learner-added tests; explain error timing, ownership,
edge cases, rejected designs, and backend transfer; and complete review. A comparison solution may
then be added. Until that point, status remains **Not attempted** and the learning tracker remains
**Not started**.
