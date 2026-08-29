# Practice — SDP-FND-040 Abstraction, encapsulation, information hiding, and contracts

| Field | Value |
|---|---|
| Unit note | [SDP-FND-040](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-040) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Test command | `uv run pytest -q units/foundations/SDP-FND-040-abstraction-encapsulation-information-hiding-contracts/practice` |
| Status | Not attempted |

## Learning question

Can you turn a public mutable quota ledger into a stable capability and behavioural contract, keep
the representation changeable, and prove the invariant survives invalid calls and a storage-shape
change?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

```text
practice/
├── README.md
├── assert_contract_experiment.py
├── quota_lab.py
└── test_quota_lab.py
```

The domain, tenants, operations, and values are synthetic. The code performs no network requests,
uses no credentials, and is not copied from a production quota system.

## Problem

`QuotaAccount` offers a useful capability—consume units from a tenant limit—but its boundary is
weak:

- `usage_entries` is a public mutable list;
- clients calculate reports by reading the list's tuple representation;
- external code can append negative units and create more remaining quota than the original limit;
- required runtime checks use `assert`;
- error meaning is only assertion text;
- the component cannot change from an entry list to aggregated or persistent storage without
  editing clients.

The starter is deliberately unsolved. Its characterization tests pass in normal interpreter mode;
that proves the current behaviour is reproduced, not that the design is safe.

## Current dependency and mutation shape

```text
                         reads tuple shape
build_usage_report ─────────────────────────┐
                                           ▼
QuotaAccount.consume ──appends──> public usage_entries: list[(operation, units)]
                                           ▲
                                           │ any caller can append/remove/replace
```

### How to read this visual

Read each arrow as knowledge or mutation authority. The report knows the exact tuple shape.
`QuotaAccount` uses the same list, but it does not exclusively control it because every caller has
the public alias.

### Key insight

Putting the list inside a dataclass gives it an object home; it does not hide the representation or
protect the quota invariant.

### Simplification or limitation

The diagram shows source-level knowledge and mutable access. It omits runtime call order, aliases
stored elsewhere, persistence, and concurrency.

## Current observable behaviour

Before refactoring, predict and then verify:

- a new account reports zero used units and its full limit remaining;
- consumption appends `(operation, units)` to `usage_entries`;
- repeated operation names are grouped in reports;
- report rows are sorted by operation name;
- blank tenant/operation values, negative limits, non-positive units, and excess consumption raise
  `AssertionError` in normal mode;
- a rejected call leaves the current list unchanged;
- direct list mutation can bypass every check and break `0 <= remaining_units <= limit_units`.

Separate **current observation** from **intended public contract**. The assertion type and public
list are design defects to migrate deliberately, not promises to preserve forever.

## Change pressure

The current list records one tuple per call. The next release must permit the owner to aggregate
usage by operation—or store it behind a persistence adapter—without changing reporting clients.

The stable use-case meaning is:

1. construct a valid account with a non-negative limit;
2. consume a positive number of units for a named operation;
3. reject a request that exceeds remaining quota without changing state;
4. inspect an immutable usage summary;
5. preserve `0 <= used_units <= limit_units` and
   `remaining_units == limit_units - used_units` after every public operation.

Do not preserve `usage_entries` merely to make old implementation-shaped tests pass. First record
the compatibility decision, then migrate tests to the intended contract.

## Contract worksheet — complete before code changes

### Abstraction

- Client and its goal:
- Public capability names:
- Public result/value meanings:
- Details the client should no longer know:

### Preconditions

- Valid tenant ID:
- Valid limit:
- Valid operation:
- Valid unit count:

### Postconditions

- Successful consumption guarantees:
- Rejected consumption guarantees:
- Summary guarantees:

### Invariants

- Quota arithmetic invariant:
- Mutation ownership invariant:
- Any ordering or uniqueness invariant:

### Failure contract

| Situation | Stable failure category | Can caller retry unchanged? | State after failure |
|---|---|---|---|
| Invalid account input |  |  |  |
| Invalid consumption input |  |  |  |
| Quota exceeded |  |  |  |
| Unexpected storage failure |  |  |  |

### Effects and consistency

- What mutates on success?
- What must not mutate on failure?
- Is the starter single-thread-only, thread-safe, or storage-atomic?
- What does a returned summary represent: live view or point-in-time snapshot?

The blank cells are learner work. Do not fill them with a solution before preserving the first
attempt.

## Required refactoring evidence

- The completed contract worksheet.
- Rahul's original code attempt and reasoning preserved at a separate path or commit.
- A before/after boundary diagram with arrow meanings.
- No public mutable alias to quota representation.
- Required runtime rejection expressed without relying on `assert`.
- Stable programmatic failure categories; client code does not parse error text.
- An immutable or otherwise safe public summary.
- Tests written against results, failures, and invariants rather than private field names.
- The controlled representation-change observation below.
- One rejected abstraction and the concrete reason it adds no change protection.
- A production-design transfer explaining where atomicity would live with shared storage.

Passing the original tests alone is insufficient. Some original assertions intentionally describe
the defective representation and must be replaced only after the intended contract is written.

## Required edge cases

- Blank and whitespace-only tenant ID.
- Negative limit and zero limit.
- Blank and whitespace-only operation.
- Zero and negative consumption.
- Exact remaining-quota consumption.
- One unit beyond remaining quota.
- Several successful calls for the same operation.
- Several operation names with deterministic summary ordering.
- Rejected call after earlier successes, with the prior snapshot unchanged.
- Attempted mutation of any returned summary/container.
- Replacement of internal representation without client-test edits.

If you add refunds, resets, expiry, or concurrency, define their contracts separately rather than
silently expanding `consume`.

## Commands

Run from the repository root:

```bash
uv run python units/foundations/SDP-FND-040-abstraction-encapsulation-information-hiding-contracts/practice/quota_lab.py
uv run pytest -q units/foundations/SDP-FND-040-abstraction-encapsulation-information-hiding-contracts/practice
```

After refactoring:

```bash
uv run ruff check units/foundations/SDP-FND-040-abstraction-encapsulation-information-hiding-contracts/practice
uv run mypy \
  units/foundations/SDP-FND-040-abstraction-encapsulation-information-hiding-contracts/practice/quota_lab.py \
  units/foundations/SDP-FND-040-abstraction-encapsulation-information-hiding-contracts/practice/assert_contract_experiment.py
```

Record actual output. Do not describe a command as passed until it has run.

## Prediction before running

- Final report from `quota_lab.py`:
- Public ledger contents:
- Result of consuming zero units in normal mode:
- Result of consuming `-3` units with `python -O`:
- Invariant after direct negative-list mutation:
- First client expected to break if the list becomes a dictionary:
- Reasoning:

## Rahul's attempt

- Attempt path or commit:
- Contract worksheet path:
- Before boundary diagram:
- After boundary diagram:
- Public API chosen:
- Hidden decision:
- Rejected abstraction:
- Test result:
- Remaining weakness:

## Progressive hints

Do not add hints until requested. Reveal one hint at a time and preserve the original attempt.

## Observe and explain

After the initial run, answer:

1. Which starter behaviour is a useful capability, and which is only representation leakage?
2. Who can currently mutate the quota invariant?
3. Why does returning `list(account.usage_entries)` avoid aliasing but still reveal representation?
4. Which current tests should become durable contract tests?
5. Which current tests should be replaced during the explicit compatibility migration?
6. Why are type annotations insufficient to reject negative units at runtime?
7. Which failures can a client recover from, and how should it distinguish them?
8. What observable facts must remain stable when the internal list disappears?

## Refactor

Refactor in small, tested steps:

1. Preserve the original attempt.
2. Write the intended contract table before choosing private fields.
3. Introduce one owner-controlled consumption operation and one safe query/snapshot.
4. Replace debug-only public guards with required runtime validation.
5. Migrate the report to public meaning rather than tuple representation.
6. Remove the public mutable alias.
7. Re-run behaviour and invariant tests.
8. Change the hidden storage shape and verify that client contract tests remain unchanged.

Do not solve the exercise by renaming `usage_entries` to `_usage_entries` while returning it through
a getter. Do not add an ABC, `Protocol`, repository, event bus, or service layer unless the stated
change pressure makes that boundary earn its cost.

## Controlled representation-change observation

This is a design-change experiment for the `D+T` evidence target, not a benchmark.

### Precise question

After refactoring, can the quota owner replace the list of individual tuples with an internal
per-operation aggregate without editing reporting clients or their contract tests?

### Hypothesis

> Before refactoring, changing the list shape breaks `build_usage_report`, direct ledger
> assertions, and callers that append. After a useful boundary, only the owner implementation and
> representation-focused tests should change; capability clients should remain unchanged.

### Controlled change

Change only representation:

- before: `list[tuple[str, int]]` with one entry per consumption;
- after: an internal `dict[str, int]` containing total units by operation.

Do not add reset windows, persistence, refund rules, expiry, or concurrency in the same observation.

### Protocol

1. Before refactoring, predict every source/test location affected by the representation change.
2. Search for `usage_entries` and tuple-unpacking knowledge; record matches.
3. Apply the representation change to a preserved copy of the starter; record failures.
4. Restore the original attempt.
5. Complete the contract-focused refactor and pass its tests.
6. Apply the same representation change behind the new boundary.
7. Run owner unit tests, client contract tests, and the full practice suite separately.
8. Compare changed files and explain discrepancies from the hypothesis.

### Evidence table

| Observation | Before boundary refactor | After boundary refactor | Explanation |
|---|---|---|---|
| Client source files edited |  |  |  |
| Client tests edited |  |  |  |
| Representation names visible outside owner |  |  |  |
| Contract behaviours changed |  |  |  |
| Owner/infrastructure files legitimately edited |  |  |  |

File counts alone are not proof. Explain which knowledge stopped crossing the boundary and which
shared meaning still required review.

## Controlled runtime experiment

### Precise question

Does Python preserve an `assert`-only public validation rule when the interpreter runs with `-O`?

### Classification

Python language/runtime behaviour. This experiment supports contract design; it is not a
performance benchmark.

### Hypothesis

> Normal mode will reject `consume("generation", -3)` with `AssertionError`. Optimized mode will
> omit the guard, append negative usage, and violate the quota arithmetic invariant.

### Environment

```text
Date: 2026-08-29
Operating system: Linux 7.0.0-30-generic, glibc 2.43
Architecture: x86_64
Python: CPython 3.14.7
sys.implementation: cpython
Dependencies: Python standard library only
Relevant flags: normal execution and -O
```

This is the repository's locked interpreter and matches its canonical Python 3.14 patch baseline.

### Reproduction commands

```bash
uv run python units/foundations/SDP-FND-040-abstraction-encapsulation-information-hiding-contracts/practice/assert_contract_experiment.py
uv run python -O units/foundations/SDP-FND-040-abstraction-encapsulation-information-hiding-contracts/practice/assert_contract_experiment.py
```

### Predicted result

```text
normal: debug=True, rejected, used=0, remaining=10
-O:     debug=False, accepted, used=-3, remaining=13
```

### Observed result

Both commands ran on 2026-08-29 and produced:

```text
debug=True
outcome=rejected:AssertionError
used_units=0
remaining_units=10
debug=False
outcome=accepted
used_units=-3
remaining_units=13
```

Normal mode rejected the invalid request before mutation. Optimized mode omitted the assertion
guard, appended `-3`, and made remaining quota exceed the configured limit.

### Visual interpretation

```text
source contains assert
          │
          ├── normal compile ──> guard emitted ──> invalid call rejected
          │
          └── python -O ───────> guard omitted ──> invalid mutation proceeds
```

#### How to read this visual

Read from one source file into two interpreter modes. The branch describes documented compilation
behaviour and the expected consequence for this deliberately defective starter.

#### Key insight

Required runtime correctness cannot depend only on a statement Python is allowed to omit.

#### Simplification or limitation

This single example does not compare validation libraries, prove all assertions are inappropriate,
or measure optimization performance. Internal debug assertions can still be useful when their
removal cannot make an invalid external request succeed.

### Design conclusion

Required public validation needs explicit checks and stable exceptions whose execution is not
conditional on `__debug__`. Internal assertions can remain useful as redundant developer checks
when removing them cannot make an invalid external operation succeed or corrupt required state.

### Source

Python Software Foundation,
[“The `assert` statement,” Python 3.14 language reference](https://docs.python.org/3.14/reference/simple_stmts.html#the-assert-statement).

## Vary: production-design transfer

Move the refactored quota state behind storage shared by multiple application processes. Do not
implement a real database unless requested. Produce a design note that answers:

- Which operation must be atomic?
- Can a summary be stale, and if so by how much or for how long?
- What happens if the write commits but the caller times out?
- Is an idempotency key needed, and what does replay return?
- Which storage failures become stable application failures?
- Which implementation causes remain internal but observable in logs?
- Can two processes ever make `used_units > limit_units`?
- Which contract tests can be shared by in-memory and persistent implementations?

This transfer proves judgment only when the design names consistency and failure semantics rather
than merely adding a “repository” class.

## Troubleshooting

- Run commands from the repository root so sibling imports resolve consistently.
- The starter's assertions are expected to disappear under `-O`; that is the observation, not a
  test-runner defect.
- If a refactor changes every test, identify which tests described representation rather than
  behaviour before weakening any assertion.
- A copied list prevents direct alias mutation but still couples callers to list/tuple meaning.
- A property can manage access but can still expose a mutable object or expensive hidden I/O.
- Do not catch `Exception` and return one generic result; preserve recoverable failure distinctions.
- Do not claim thread safety because mutation occurs inside one method.
- Keep the exercise deterministic and standard-library-only; no internet, clock, or credentials are
  required.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Contract table:
- Controlled representation-change result:
- Runtime experiment interpretation:
- Production-design transfer:
- Trade-offs:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
