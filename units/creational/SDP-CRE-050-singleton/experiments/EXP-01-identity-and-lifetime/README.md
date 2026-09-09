# EXP-01 — Identity and lifetime — SDP-CRE-050

## Question and hypothesis

Does one identity imply one initialization, one factory execution, or one appropriate application
lifetime? The hypothesis is no: those properties depend on separate policies. Predict every row
before running; the maintainer observations below are not a learner prediction or attempt.

## Controlled variables

Use synthetic objects and two-worker thread executors. The cache-race factory waits at a two-party
barrier, forcing overlapping misses before either call returns. The provider case puts the barrier
outside the provider so both callers can contend for its lock. Barriers have five-second failure
bounds, and futures/subprocesses have bounded result waits. There are no arbitrary sleep timings.
All tested calls complete normally within these bounds. A timeout is a test failure, not evidence
that a construction policy succeeded.

`identity_probe.py` creates fresh local classes, factories, and provider objects for each observation
run. `mechanics_probe.py` executes deliberately flawed classes in a fresh subprocess, avoiding
mutation of imported example singletons or of other tests. Its pickle bytes are generated locally
from synthetic objects in that same subprocess; no external pickle is read.

## Environment and commands

Observed on 2026-09-09 under CPython 3.14.7 and CPython 3.11.16 on Linux. Both installed interpreters
use the ordinary GIL-enabled build. The locked tools are pytest 8.4.2, mypy 1.20.2, Ruff 0.16.1, and
Hypothesis 6.165.2. Hypothesis is part of the shared tool environment; these focused probes use
explicit deterministic schedules and examples, not generated property trials.

From the repository root, use the all-cache-to-`/tmp` exports in the
[unit commands](../../README.md#20-run-and-study), select the desired runtime as `python`, and run:

```bash
python units/creational/SDP-CRE-050-singleton/experiments/EXP-01-identity-and-lifetime/identity_probe.py
python units/creational/SDP-CRE-050-singleton/experiments/EXP-01-identity-and-lifetime/mechanics_probe.py
python -m pytest -p no:cacheprovider units/creational/SDP-CRE-050-singleton/experiments/EXP-01-identity-and-lifetime
```

The maintenance run used the existing Local locked 3.14 interpreter and the existing `/tmp`
3.11 environment; neither was changed. Exact paths and quality checks appear in
[VALIDATION.md](../../VALIDATION.md). Capture your own predictions and outputs separately.

## Observed identity results on both runtimes

The JSON `constructions` field is interpreted according to the count-unit column, not as a generic
performance measure. In particular, a failed factory attempt need not complete an allocation.

| Scenario | Count unit | Count | Same identity | Exact detail |
|---|---|---|---|---|
| repeated-init | Object allocations | 1 | true | `init calls=2; label=second` |
| cache-race | Wrapped factory calls / recorded misses | 2 | false | `two overlapping cache misses` |
| locked-provider | Factory calls | 1 | true | `one publication per provider` |
| retry | Factory attempts | 2 | true | `failed attempt was not published` |
| two-apps | Reader acquisitions | 2 | false | `both closed=True` |

The first row returns the same object after two constructor calls but overwrites its label. The
cache row exposes duplicate creation on a selected overlapping schedule. The provider serializes
creation within one provider, not across every provider in the program. Retry compares successful
accesses after a failed attempt. Each application in the final row internally shares its own reader,
but the two applications have different readers and both owners close successfully.

## Observed mechanics results on both runtimes

```text
child_has_child_type: false
child_init_ran: false
child_is_base: true
failed_object_still_cached: true
live_revision_after_restore: r1
mutable_init_calls: 1
partial_state_reachable: true
pickle_preserved_identity: true
```

Base-first construction makes the child's inherited cache return the Base object. A naive cached
allocation survives a throwing initializer and exposes partial state. A locally produced pickle of
revision r1 restores r1 into the same mutable object after its live revision was set to r2, without
another `__init__` call. This is a dangerous default-protocol interaction, not the explicit stateless
marker's reducer. The tests assert every field on both runtimes.

## Interpretation and limits

These observations support claims about the executed classes and schedules. They do not enumerate
all schedules, benchmark overhead, validate a database driver, exercise free-threaded Python, or
prove process-wide/distributed uniqueness. The fresh-process tests elsewhere check boundary effects
without numeric cross-process `id()` comparison. No fork or subinterpreter run is claimed.

A lock may make a returned object unique within the provider while its later operations remain
unsafe. A cached identity can still hold stale or partially initialized state. Explicit lifetime
owners can correctly create more than one object in one interpreter. Explain those three statements
in your own words before choosing a class Singleton for the separate lab.

## Visual contract

The [explorer](../../visuals/README.md) embeds all five identity observations. Its test compares every
field with a fresh Python probe run, checks selection order and static accessible structure, and
checks that referenced element IDs exist. Node checks script syntax separately. These checks do not
substitute for browser rendering; the direct local URL was blocked, with no bypass attempted.
