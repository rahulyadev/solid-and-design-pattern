# Practice — SDP-SOL-010 Single Responsibility Principle

| Field | Value |
|---|---|
| Unit note | [SDP-SOL-010](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-sol-010) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Test command | `uv run pytest -q units/solid/SDP-SOL-010-single-responsibility-principle/practice` |
| Status | Not attempted |

## Learning question

Can you identify the independent policy decisions in a working completion-bulletin workflow,
preserve its current contract, and add a useful preview without creating a class for every step?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

Start with a prediction, then run the supplied characterization tests. They should pass before
refactoring: the design exercise is intentionally unsolved even when the baseline is green.

## Starter files

- [completion_lab.py](completion_lab.py): valid attendance data, the existing public operation,
  a typed archive row, and a synthetic sample runner.
- [test_completion_lab.py](test_completion_lab.py): observable outputs, boundaries, and failure
  behaviour. No required private helper, class count, or pattern is encoded in the tests.

## Problem and change pressure

A workshop system publishes a participant's completion result. Academic staff control completion
eligibility. Learner-support staff control who needs follow-up. Communications controls the
bulletin wording. Platform staff maintains the archive schema and delivery integration. In this
small organization, the same coordinator may relay requests from all four groups.

The existing public operation is:

```python
publish_completion(attendance, record, send) -> str
```

Two real requests arrive, to be handled in separate checkpoints:

1. Staff need a preview of the exact bulletin before publication. Previewing must not record
   anything or send a message. Existing publication callers must continue to work.
2. After the behaviour-preserving refactoring is complete, academic staff raise the completion
   threshold from 75% to 80%. Learner-support policy stays unchanged.

The first request is the implementation task. The second tests whether the proposed boundaries
follow policy ownership. You choose the smallest API and structure that satisfy them.

## Stable behaviour before the policy change

| Concern | Existing public contract |
|---|---|
| Input | Nonblank participant ID; positive scheduled sessions; attended is between zero and scheduled |
| Completion | Eligible at 75% attendance or above, inclusive |
| Follow-up | Required strictly below 75% attendance |
| Arithmetic | Compare the exact integer ratio, without rounding a display percentage |
| Bulletin | Four lines, no trailing newline; exact labels and ordering from the supplied test |
| Archive | One row with participant ID, `attendance` as `attended/scheduled`, and two boolean decisions |
| Delivery | One message addressed by participant ID; its body matches the returned string |
| Ordering | Record first, then send; return only after both callbacks return normally |
| Record error | Propagates; delivery is not attempted |
| Send error | Propagates; completed record is still visible |

Callbacks are synchronous. Their successful return is the only success signal in this exercise.
There is no real database, email delivery, transactional guarantee, or untyped HTTP parser.

## Current ownership visual

```text
Attendance
    │
    ▼
publish_completion
    ├─ decides completion
    ├─ decides follow-up
    ├─ builds bulletin wording
    ├─ builds archive representation
    ├─ invokes record
    └─ invokes send
```

### How to read this visual

The top arrow supplies the facts; the branches list decisions and effects currently inside one
operation. This describes the starter, not a target list of six classes.

### Key insight

The starter has only one public function, but that does not tell us how many independent policies
it owns. Identify those policies from the change requests.

### Simplification or limitation

This conceptual map omits validation and callback implementation. It does not prescribe the
refactoring or imply that every branch needs its own object or file.

## Commands

Run from the repository root. Keep development environments and caches outside the repository so
the strict hygiene validator does not mistake them for deliverable artifacts:

```bash
export UV_PROJECT_ENVIRONMENT=/tmp/sdp-sol-010-venv
export UV_CACHE_DIR=/tmp/sdp-sol-010-uv-cache
export PYTHONDONTWRITEBYTECODE=1
export MYPY_CACHE_DIR=/tmp/sdp-sol-010-mypy-cache
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-sol-010-hypothesis

uv sync --locked --group dev
uv run --locked python units/solid/SDP-SOL-010-single-responsibility-principle/practice/completion_lab.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-010-single-responsibility-principle
uv run --locked ruff check --no-cache units/solid/SDP-SOL-010-single-responsibility-principle
uv run --locked mypy units/solid/SDP-SOL-010-single-responsibility-principle
python scripts/validate_repo.py
```

The paths are disposable development locations, never files to add to Git. If the repository
already contains ignored environments, leave them alone and use a clean Worktree for the hygiene
check. Record actual output rather than copying the maintainer's validation results.

## Prediction before running

Fill these fields before editing or running the starter:

- Expected sample bulletin:
- Expected archive and message counts:
- Expected behaviour for 2/3, 3/4, and 4/5 attendance:
- Expected state after record failure:
- Expected state after send failure:
- First change you expect to be difficult:
- Reason for that prediction:

## Rahul's attempt

Not yet supplied. Preserve the first code attempt in a separate attempt file or local commit
before substantial revisions. Do not replace it with the teaching example or a generated solution.

- Attempt file or commit:
- Proposed boundary and reason:
- Rejected alternative and cost:
- Actual test command and result:
- First unexpected observation:

## Diagnosis worksheet

| Decision or invariant | Present location | Who can change it? | What must remain stable? | Proposed owner and reason |
|---|---|---|---|---|
| Valid attendance range |  |  |  |  |
| Completion eligibility |  |  |  |  |
| Follow-up eligibility |  |  |  |  |
| Bulletin wording |  |  |  |  |
| Archive representation |  |  |  |  |
| Publication order and success |  |  |  |  |

Do not infer ownership solely from equal constants, one person's name, an execution sequence,
or the number of functions. Write the supporting requirement for each claimed boundary.

## Refactoring checkpoints

### Checkpoint 1 — Characterize and explain

Run the original suite unchanged. Record the outputs and explain what it protects. Identify a
policy claim the tests alone cannot establish.

### Checkpoint 2 — Choose boundaries

Draw your proposed collaborators and label the knowledge each one hides. Name the handoff values
and the authority for every decision. Keep related invariants together. Explain what will remain
in one module and why.

### Checkpoint 3 — Add preview

Implement a public preview operation with no record or send effects. Choose its name and contract.
Keep `publish_completion(attendance, record, send)` compatible and the original 75% policy intact.
Avoid copying formulas into a second report or into test expectation helpers.

Add behaviour tests demonstrating that preview and publication agree for equivalent input,
including boundary attendance. If your preview API accepts any effectful collaborators, prove
they are not called. If it accepts none, explain how that API constrains side effects and test
its result and input preservation; do not invent a mock-only interface.

### Checkpoint 4 — Preserve failures

Keep record-before-send ordering and error propagation. Do not hide an exception by returning a
plausible success message. Explain who owns recovery and what the synchronous callbacks cannot
tell you about a real external system.

### Checkpoint 5 — Review the cost

List the current client and hidden knowledge for every new abstraction. Remove any layer that
adds only forwarding or breaks one cohesive decision into arbitrary steps. Passing tests are
necessary but do not settle this review.

## Vary

Apply the confirmed academic change to 80% only after checkpoint 5. Predict the edited source
locations and affected test expectations first. Preserve the original baseline through Git
history; do not silently reinterpret it as if the new requirement always existed.

- Verify just below, exactly at, and above the new completion boundary.
- Verify learner-support results remain consistent with its unchanged policy.
- Check preview, returned bulletin, archived decisions, and delivered bulletin for agreement.
- Record changed implementations separately from outputs that merely consume changed decisions.
- Explain whether your actual edits support or contradict the ownership map.

Optional transfer after the primary task: platform staff wants a new archive format with separate
integer attendance fields, while existing archive consumers still need the original schema.
Propose a migration that preserves their contract. Do not build a plug-in framework in anticipation.

## Required edge cases

- Zero attendance and full attendance.
- Exact old and new thresholds; one session ratio just below each.
- A ratio such as 2/3 that must not be rounded into eligibility.
- Blank identifier, zero or negative scheduled count, negative attendance, attendance above total.
- Preview called repeatedly with no effects.
- Separate participants without shared result state.
- Archive failure before delivery and delivery failure after recording.
- Identical policy facts with different presentation requests, if you introduce such an option.

## Constraints

Use Python 3.11-compatible code, ordinary functions, values, and explicit dependencies. Add no
network calls, database, framework, dependency-injection container, ABC, registry, event bus,
third-party package, or service boundary unless a current requirement actually needs it.

Do not test private helper names, enforce a class count, or solve the ownership question with an
automatic metric. Do not change unrelated unit files or advance the learner tracker automatically.

## Progressive hints

No hints have been supplied. Ask for one progressive hint after preserving an attempt. The next
hint should target the first missing reasoning step, not reveal the full structure.

## Observe and explain

After each checkpoint, record the observed contract, remaining coupling, most useful boundary,
unnecessary abstraction, and one rejected alternative. Include actual test output and explain
which requirement it supports. A copied green result does not establish your explanation.

## Troubleshooting

- Run pytest from the repository root using the explicit path; the code uses normal pytest import
  discovery rather than installing these hyphenated curriculum folders as Python packages.
- Use the locked environment. Do not install missing tools into the repository tree.
- Initial tests passing is expected. The preview and policy-change acceptance tests are still
  your work; there are no hidden completed solutions or silently skipped TODO tests.
- If policy-change assertions differ from the old characterization suite, separate intentional
  expectation changes from accidental regressions and preserve the old baseline.

## Review and closure

No learner review or closure has occurred. Once an attempt exists, record what was correct, the
first incorrect assumption, the smallest exposing example, and one targeted next step. Add a
comparison solution only after Rahul closes the exercise. Practiced or later states require the
attempt, relevant passing tests, edge cases, explanation, and valid evidence links in `PROGRESS.md`.
