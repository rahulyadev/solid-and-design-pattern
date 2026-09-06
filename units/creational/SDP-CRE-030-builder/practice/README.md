# Practice — SDP-CRE-030 staged archive-job construction

| Field | Value |
|---|---|
| Unit note | [SDP-CRE-030](../README.md) |
| Starter | [archive_job_lab.py](archive_job_lab.py) |
| Behavior tests | [test_archive_job_lab.py](test_archive_job_lab.py) |
| State | Unsolved |

## Scenario and change pressure

The baseline creates a validated `ArchiveJob` through one keyword-only factory. That is currently a
good design. A new operations flow now gathers configuration in stages:

1. a tenant boundary supplies identity and allowed datasets;
2. a scheduler chooses full or incremental mode;
3. a checkpoint service supplies a cursor only for incremental mode;
4. a routing policy chooses internal or partner delivery;
5. a key service supplies a reference only for partner delivery; and
6. the final boundary must reject an incomplete or contradictory candidate before any job is queued.

Your task is to preserve the final immutable Product and stable `summarize` consumer, then decide
whether a Builder has become the smallest clear construction boundary. Do not add a Director unless
two named, repeated recipes actually exist.

Keep the starter as the original attempt or copy it before refactoring. Passing baseline tests is
not evidence that the design exercise is complete, and it never changes `PROGRESS.md` by itself.

## Predict before running

Record one answer at a time:

1. Which constraints are field-local, and which relate two or more fields?
2. Which values are required for every Product, and which are conditional or optional?
3. At which line does the current Product become valid?
4. Can ordinary local variables plus the focused factory express the new six-stage flow clearly?
5. What invalid intermediate states may exist safely inside a request-local Builder?
6. What must `build()` report if identity, datasets, mode, or target is missing?
7. Should validation happen in the Builder, the Product, or both—and why?
8. After `build()`, may the Builder be reused, consumed, or explicitly reset?
9. What prevents later Builder mutation from changing an earlier Product?
10. Which configuration values and key references must observations omit?
11. Who owns any resource opened while resolving a checkpoint or key reference?
12. Does returning `self` make an API a GoF Builder?

No learner prediction has been recorded by the maintainer.

## Run

From the repository root:

~~~bash
PYTHONPYCACHEPREFIX=/tmp/sdp-cre-030-pycache \
  uv run --locked python units/creational/SDP-CRE-030-builder/practice/archive_job_lab.py
PYTHONPYCACHEPREFIX=/tmp/sdp-cre-030-pycache \
  uv run --locked pytest -q -p no:cacheprovider \
  units/creational/SDP-CRE-030-builder/practice
~~~

Record the runtime, exact output, and test count before editing.

## Observe

Find these baseline facts:

- construction is one keyword-only call, not yet an unreadable positional constructor;
- the frozen Product owns every invariant, so direct construction cannot bypass validation;
- the factory adds a name but no staged state;
- full/incremental and internal/partner rules are cross-field constraints;
- key references are omitted from the generated representation;
- the stable consumer knows nothing about how the Product was built; and
- `TARGET_REFACTOR_COMPLETE` is false although all baseline tests pass.

## Explain before refactoring

| Candidate | When it is enough | Cost or limit |
|---|---|---|
| Direct keyword-only Product | All inputs exist together and validation is readable | Call sites repeat policy defaults |
| Focused factory function | One named construction policy | Awkward if inputs arrive through a long staged workflow |
| Configuration dataclass | Inputs are data passed between layers | Does not by itself define finalization or prevent partial use |
| Local variables plus final factory | One local orchestration owns the stages | Repetition if several flows share the same sequence |
| Mutable fluent Builder | Staged optional input and final validation need one owner | Stale state, reuse, concurrency, and ordering rules |
| Typed stage objects | Illegal call order must be rejected statically | More types, transitions, and API surface |

## Refactor

1. Preserve the baseline Product invariants and behavior tests.
2. Write the simplest six-stage orchestration with local variables and the existing factory first.
3. Mark the exact duplication or partial-state leak that remains.
4. If justified, introduce one request-local Builder with named required and optional steps.
5. Keep intermediate state private; no consumer may run an incomplete job.
6. Make `build()` list every missing required step in deterministic order.
7. Let the final Product defend cross-field invariants even against direct construction.
8. Copy mutable collections into immutable tuples at finalization.
9. Choose and document one reuse contract: one-shot, explicit reset, or reusable snapshot.
10. Add allow-listed observations that omit tenant IDs, dataset names, cursors, and key references.
11. Add cleanup for a failure after one resource has been acquired; do not promise rollback of an
    already queued external job.
12. Add a second named recipe before—and only before—considering an optional Director.
13. Reject a shared module-global Builder and a speculative class hierarchy in writing.
14. Set `TARGET_REFACTOR_COMPLETE = True` only when code, tests, and explanation agree.

## Required edge cases

- missing identity, datasets, mode, and target, individually and together;
- blank and whitespace-padded values;
- duplicate datasets and non-ASCII but valid names;
- incremental without checkpoint and full with checkpoint;
- partner without encryption reference;
- retention values at 1, 365, and outside both bounds;
- repeated step calls and an explicit last-write-or-error decision;
- `build()` called twice under the documented reuse policy;
- reset after success and reset after failure;
- mutation after build that cannot change the earlier Product;
- two concurrent requests that do not share mutable staged state;
- failure after the first resource acquisition and cleanup in reverse order;
- observer failure policy; and
- diagnostics that omit all tenant, dataset, cursor, and encryption values.

## Rahul's attempt

- Original attempt file: —
- Prediction: —
- Smallest non-Builder design tried: —
- Remaining staged-construction pressure: —
- Required versus optional steps: —
- Final validation owner: —
- Reuse/reset contract: —
- Lifetime owner: —
- Runtime observation: —
- Test result: —

## Progressive hints

No hints are released. Ask for one hint at a time after recording an attempt.

## Observe and explain after refactoring

1. Point to the only operation that can publish a complete `ArchiveJob`.
2. Call `build()` early and interpret the missing-step result.
3. Construct a cross-field-invalid candidate and show the final Product rejects it.
4. Build once, mutate the Builder, and prove the first Product stays unchanged.
5. Demonstrate the exact reset/reuse behavior.
6. Inject a fake observation sink without patching module globals.
7. Fail the second resource acquisition and show cleanup of the first.
8. Replace the Builder with local variables plus a factory and name what clarity is lost or gained.

## Vary

Re-evaluate the design when:

- all values arrive in one parsed request;
- only the internal full-archive recipe remains;
- a second recipe changes the same sequence but not the Product representation;
- the same sequence must produce a dry-run manifest instead of an executable job;
- steps may arrive out of order;
- the call order itself is a safety property;
- resource acquisition becomes asynchronous and cancellation can occur; or
- one Builder would be shared across worker threads.

Name the smallest answer: keyword-only constructor, frozen dataclass, focused factory, local
variables, configuration object, Builder, typed stages, or Builder plus Director.

## Completion boundary

Maintainer tests validate only the unsolved starter artifact. Practice evidence requires a saved
prediction, preserved original attempt, added edge-case tests, actual runtime observations, an
explicit validation/reuse/lifetime decision, and a justified comparison with the non-Builder design.
