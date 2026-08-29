# Practice — SDP-FND-080 Dependency management, test seams, and test doubles

| Field | Value |
|---|---|
| Unit note | [SDP-FND-080](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-080) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Focused test command | `.venv/bin/pytest -q units/foundations/SDP-FND-080-dependency-management-test-seams-test-doubles/practice` |
| Status | Not attempted |

The starter, characterizations, and three controlled experiments have been run to verify the
artifact. That proves only that the supplied material executes as documented. It does **not** count
as Rahul's prediction, refactoring attempt, double selection, explanation, or learning evidence.

## Learning question

How can a renewal use case make time, persistence, payment, and audit collaborators controllable
without replacing every private call with a mock or making tests describe one implementation's
choreography?

## Lab cycle

```text
predict → run → observe → explain → characterize → choose seams → refactor → vary
```

Do not begin by adding four `Mock` objects. Begin by finding the observable contract and the
decisions currently hidden in construction.

## Starter files

```text
practice/
├── README.md
├── renewal_lab.py
├── test_renewal_lab.py
├── patch_lookup_experiment.py
├── mock_strictness_experiment.py
├── fake_contract_experiment.py
└── test_dependency_seam_experiments.py
```

- `renewal_lab.py` is the unsolved application-boundary refactoring starter.
- `test_renewal_lab.py` characterizes stable behavior and one deliberate idempotency defect.
- `patch_lookup_experiment.py` reproduces Python name-lookup behavior during patching.
- `mock_strictness_experiment.py` compares a loose `Mock` with an autospecced, `spec_set` double.
- `fake_contract_experiment.py` shows an in-memory fake drifting from a SQLite adapter's observable
  uniqueness rule.
- `test_dependency_seam_experiments.py` makes the experiment results reproducible.

## Problem

`renew_subscription()` renews one account. It currently:

1. creates a new `RenewalLedger`;
2. asks that ledger whether the request has already been handled;
3. creates a `BillingGateway` and charges the payment token;
4. creates a `SystemClock` and records the time;
5. saves a `RenewalReceipt`;
6. creates an `AuditPublisher` and publishes that receipt;
7. returns the receipt.

The function has a reasonable public input and output, but it also owns four unrelated
configuration and lifetime decisions. A test can control those decisions only by knowing which
module names the function looks up.

## Current dependency and object flow

```text
renew_subscription(command)
        │
        ├── constructs RenewalLedger() ───── new empty store per call
        │          │
        │          └── find(request_id) ─── always misses across calls
        │
        ├── constructs BillingGateway() ─── charge(...)
        ├── constructs SystemClock() ────── now()
        ├── ledger.save(receipt)
        └── constructs AuditPublisher() ─── publish(receipt)

test ──patches──> renewal_lab.BillingGateway / SystemClock / AuditPublisher
                     ▲
                     └── must know the implementation's lookup namespace
```

### How to read this visual

Follow the main function from top to bottom. Each `constructs` arrow is both a dependency choice
and a lifetime choice. Then read the test arrow: the only current control point is a module-level
name replacement, so the test must know how the function imports and constructs collaborators.

### Key insight

The test problem is a design signal: configuration and use are fused. The strongest seam is not
necessarily another patch; it is usually a small explicit input placed at the boundary that owns
the decision.

### Simplification or limitation

All adapters are synthetic and local; there is no network or production database. The visual
omits exception translation, transactions, retries, process boundaries, and concurrency. It is a
design model, not a framework dependency graph.

## Stable behavior to preserve

- A valid approved charge returns a `renewed` receipt with the provider reference.
- A normal payment decline returns a `declined` receipt with a reason; it is not raised as an
  infrastructure exception.
- The recorded time is timezone-aware.
- The saved and published value has the same business content as the returned receipt.
- Blank identifiers and tokens, and non-positive amounts, fail before any external collaboration.
- Receipt and charge-decision states remain coherent.

## Deliberate defect to expose and repair

The same `request_id` submitted twice must return the first saved receipt without a second charge
or a second audit event.

The starter violates that requirement because each call constructs a new empty `RenewalLedger`.
This is not merely a “mocking difficulty.” It is a hidden ownership and lifetime decision with a
business consequence.

## Prediction before the first run

Write answers before executing anything:

1. Which two receipts will the module print?
2. Will they compare equal?
3. Will they be the same Python object?
4. Why can the second call not see the first call's saved receipt?
5. Which names must a current test patch to make time, charging, and audit deterministic?
6. Which assertion in the characterization suite describes a defect rather than desired final
   behavior?

Record:

- Expected output:
- Dependency and call flow:
- Likely failure after the idempotency requirement:
- Reasoning:

## Baseline commands

From the repository root:

```bash
.venv/bin/python \
  units/foundations/SDP-FND-080-dependency-management-test-seams-test-doubles/practice/renewal_lab.py

.venv/bin/pytest -q \
  units/foundations/SDP-FND-080-dependency-management-test-seams-test-doubles/practice
```

Do not copy the output below into the prediction. The artifact-verification run observed:

```text
first=renewed:charge:req-42
second=renewed:charge:req-42
same_receipt_object=False
.............                                                            [100%]
13 passed in 0.10s
```

Timing is informational and may differ. The behavioral lines and pass count are the relevant
observations.

## Rahul's attempt

- Prediction:
- First run and actual output:
- First explanation:
- Attempt file or commit:
- Chosen seams:
- Double-role choices:
- Rejected alternative:
- Focused test result:
- Remaining uncertainty:

## Refactoring checkpoints

### Checkpoint 1 — Mark decisions, not classes

For every collaborator, write what varies and who should decide it.

| Collaborator | What varies | Current owner | Candidate configuration owner | Lifetime needed by idempotency |
|---|---|---|---|---|
| Clock | current instant | use-case function |  |  |
| Billing gateway | provider behavior and failure | use-case function |  |  |
| Ledger | storage implementation and state | use-case function |  |  |
| Audit publisher | delivery implementation | use-case function |  |  |

Do not write “because tests need a mock” in the change-pressure column. State the production or
behavioral force.

### Checkpoint 2 — State the smallest collaborator contracts

Describe only what `renew_subscription()` needs:

- clock:
- charge operation:
- receipt lookup:
- receipt save:
- audit operation:
- provider failure translation:

Then decide whether each boundary needs:

- a plain value;
- a callable;
- a small object used by duck typing;
- a `Protocol` for static feedback;
- no new abstraction at all.

An abstract base class is not required merely because there are a production implementation and a
test double.

### Checkpoint 3 — Separate assembly from use

Move concrete construction to one visible composition boundary. Keep the use-case code focused on
the renewal policy.

Acceptable Pythonic shapes include:

- explicit function parameters for a small stateless operation;
- constructor injection for a reusable service whose collaborators must always be present;
- a callable for `now`, `charge`, or `publish` when identity and rich state add no value;
- a small client-owned `Protocol` when static checking across modules earns its cost.

Do not introduce a dependency-injection framework, container, global registry, or service locator
for this lab.

### Checkpoint 4 — Replace the brittle characterization

After the seam exists, remove tests that exist only to prove which concrete class was constructed.
Prefer assertions on:

- the returned receipt;
- the fake ledger's stored state;
- the absence of a second payment call for the same request;
- the absence of a second audit event for the same request;
- translated provider failures;
- validation before side effects.

Keep an interaction assertion only when the interaction itself is part of the boundary contract.
“Do not charge the same request twice” is such a requirement. “Call private helper A before private
helper B” is not.

### Checkpoint 5 — Choose each double by role

Fill this before importing `unittest.mock`:

| Test need | Candidate double | Why this role | State or interaction verification? |
|---|---|---|---|
| Fixed timestamp |  |  |  |
| Approved payment result |  |  |  |
| Declined payment result |  |  |  |
| Persistent receipt state across calls |  |  |  |
| Count attempted charges |  |  |  |
| Record published audit events |  |  |  |
| Required but unused collaborator on validation failure |  |  |  |

The same Python object may play more than one role. Name the role from how the test configures and
verifies it, not from whether its class is named `Mock`.

### Checkpoint 6 — Repair idempotency

Add tests that prove:

1. the first valid request charges, saves, publishes, and returns a receipt;
2. the second request with the same `request_id` returns the saved receipt;
3. the second request does not charge;
4. the second request does not publish a duplicate audit event;
5. two different request IDs remain independent.

Decide and document what happens if the repeated command has the same request ID but different
account or amount data. Do not silently guess.

### Checkpoint 7 — Vary one boundary failure

Choose one:

- the billing adapter times out;
- the ledger rejects a duplicate save;
- the audit publisher fails after the ledger save;
- the clock produces a naive timestamp.

Write the required application meaning before coding. Then decide whether the use case should
translate, retry, compensate, surface, or record the failure. A mock `side_effect` can reproduce
the event, but it cannot decide the policy for you.

## Required edge cases

- blank `request_id`;
- blank `account_id`;
- blank `payment_token`;
- zero and negative `amount_cents`;
- approved result without a provider reference;
- declined result without a reason;
- naive timestamp;
- repeated request ID;
- distinct request IDs for the same account;
- one chosen infrastructure failure.

## Test-quality constraints

Your final unit tests should satisfy these rules:

1. No real network, sleep, system clock, or production database.
2. Fresh mutable test state unless a test deliberately proves lifetime behavior.
3. No assertion about a private helper, internal class construction, or irrelevant call order.
4. No chain such as `mock.return_value.session.return_value.execute.return_value`.
5. Any `Mock` used for a concrete signature should have an honest `spec`, `spec_set`, or autospec
   source unless a simpler handwritten double is clearer.
6. A fake ledger must have shared contract tests for the semantics relied upon by the use case.
7. At least one test must use a small handwritten fake or spy so the boundary remains readable
   without mock-framework fluency.
8. A passing focused test run is required, but passing tests alone do not close the exercise.

## Decision review

After the refactor, answer:

1. Where is the composition root?
2. Which dependencies are visible in the production signature?
3. Which dependency became a plain callable, and why?
4. Which collaborator needs state across calls?
5. Which double is a stub?
6. Which double is a spy?
7. Which double is a fake?
8. Did you use a mock? If so, which externally meaningful interaction does it verify?
9. Which former patch can now be deleted?
10. What real integration remains unproved by the unit tests?

## Progressive hints

Hints are intentionally not populated. Ask for one hint at a time after recording an attempt. The
first hint will target the earliest incorrect assumption, not reveal a finished design.

---

# Controlled experiments

The following experiments are completed observation tools, not learner solutions to the renewal
lab. Each separates a Python or library mechanism from the design judgment built on top of it.

## Shared verified environment

```text
Date: 2026-08-29
Operating system: Linux 7.0.0-30-generic
Architecture: x86_64
Python version: 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation: cpython
pytest: 8.4.2
unittest.mock: Python standard library
```

These are observations on the recorded environment. Experiment 1 relies on Python name binding
and `unittest.mock.patch` behavior, not on a CPython implementation detail. Experiment 3 uses
SQLite's standard-library adapter only as a bounded real implementation for contract comparison.

## SDP-FND-080-EXP-01 — Patch the lookup name

| Field | Value |
|---|---|
| Precise question | If a module imports `uuid4` directly, does patching `uuid.uuid4` replace the already-bound local name? |
| Classification | Python name binding + standard-library `unittest.mock.patch` behavior |
| Status | Reproduced |

### Why observation is necessary

“Patch where it is defined” sounds plausible and often produces a test that runs but does not
control the call. The effect depends on which name the system under test evaluates.

### Hypothesis

> Patching `uuid.uuid4` will change a call that performs `uuid.uuid4()` at execution time, but it
> will not change a different module's earlier `from uuid import uuid4` binding. Patching that
> module's `uuid4` name will change the direct-import path.

### Controls and variables

- Controlled: fixed UUID return values, same process, no printed random UUID.
- Changed: patch target—definition module versus the experiment's lookup namespace.
- Measured: equality with the fixed UUID, reported as booleans.

### Reproduction command

```bash
.venv/bin/python \
  units/foundations/SDP-FND-080-dependency-management-test-seams-test-doubles/practice/patch_lookup_experiment.py
```

### Predicted result

```text
definition_patch_changed_imported_alias=False
definition_patch_changed_module_lookup=True
use_site_patch_changed_imported_alias=True
```

### Observed result

```text
definition_patch_changed_imported_alias=False
definition_patch_changed_module_lookup=True
use_site_patch_changed_imported_alias=True
```

### Interpretation

1. **Directly shown:** two names that originally referenced the same function can be replaced
   independently; the call path using the patched name changes.
2. **Reasonable inference:** patch-based tests must target the name looked up by the system under
   test. A change in import style can therefore break a patch target even when business behavior
   is unchanged.
3. **Not shown:** explicit injection is always superior, every patch is fragile, or module imports
   are themselves a design defect.

### Visual interpretation

```text
import time                              test time

uuid.uuid4 ───────┐                  patch uuid.uuid4 = fixed-A
                  ├─ object F             │
client.uuid4 ─────┘                        ├─ uuid.uuid4() ──> fixed-A
                                          └─ client.uuid4() ─> original F

                                      patch client.uuid4 = fixed-B
                                          └─ client.uuid4() ─> fixed-B
```

#### How to read this visual

At import time, two names point to one function object. A patch later rebinds one name, not every
name that ever referred to the object. Follow the called name on the right to see which binding
controls the result.

#### Key insight

`patch()` replaces a binding for a scope; it does not search the process for all aliases to an
object.

#### Simplification or limitation

The sketch omits descriptors, proxy objects, import reloading, concurrent threads, and patch
cleanup. It is a name-binding model for these two import forms.

### Design conclusion

Patching the lookup namespace is correct mechanics for a tactical seam. If many tests must know
import details for ordinary collaborator selection, move that selection to an explicit assembly
boundary instead of teaching every test the module's wiring.

### Source

Python's `unittest.mock` documentation explains that `patch()` temporarily changes what a name
points to and must target the name used by the system under test
([Python 3.14, “Where to patch”](https://docs.python.org/3.14/library/unittest.mock.html#where-to-patch)).

## SDP-FND-080-EXP-02 — Loose Mock versus autospec and `spec_set`

| Field | Value |
|---|---|
| Precise question | What mistakes can a plain `Mock` accept that an autospecced, `spec_set` double rejects? |
| Classification | Python standard library |
| Status | Reproduced |

### Why observation is necessary

A plain `Mock` creates child attributes on access. This flexibility can let a misspelled method or
wrong call shape survive test setup. The exact protections from autospec are narrower than “the
mock is realistic,” so they should be observed precisely.

### Hypothesis

> A loose `Mock` will accept a misspelled `chagre` attribute. An autospecced, `spec_set` double
> based on `PaymentPort` will reject that attribute and reject arguments that do not match
> `charge(*, account_id, amount_cents)`. It will still accept any configured semantic return value.

### Controls and variables

- Controlled: one `PaymentPort` signature and one configured provider reference.
- Changed: plain `Mock` versus `create_autospec(..., instance=True, spec_set=True)`.
- Measured: attribute rejection, signature rejection, returned value, valid call count.

### Reproduction command

```bash
.venv/bin/python \
  units/foundations/SDP-FND-080-dependency-management-test-seams-test-doubles/practice/mock_strictness_experiment.py
```

### Predicted result

```text
loose_created_typo_attribute=True
strict_rejected_typo=True
strict_rejected_wrong_signature=True
stubbed_value=pay-42
recorded_valid_calls=1
```

### Observed result

```text
loose_created_typo_attribute=True
strict_rejected_typo=True
strict_rejected_wrong_signature=True
stubbed_value=pay-42
recorded_valid_calls=1
```

### Interpretation

1. **Directly shown:** the loose double created and recorded the misspelled attribute; the strict
   double rejected both an absent member and an invalid call shape.
2. **Reasonable inference:** autospec can make refactoring and typo failures more honest when a
   mock is the appropriate double.
3. **Not shown:** the configured provider reference has valid business meaning, the real service
   is reachable, the real adapter honors the signature, or the interaction is worth asserting.

### Visual interpretation

```text
Plain Mock                         autospec + spec_set

.chagre(...)                       .chagre(...)
    │                                  │
    └─ create child Mock               └─ AttributeError

.charge(wrong args)                .charge(wrong args)
    │                                  │
    └─ accept                           └─ TypeError

                 neither side proves
               provider/business semantics
```

#### How to read this visual

Compare each row horizontally. Strictness narrows the permitted member and call shape. Then read
the bottom statement across both columns: structural strictness does not prove semantic fidelity.

#### Key insight

Autospec improves API-shape honesty. Contract tests and integration tests are still required for
behavior and wiring.

#### Simplification or limitation

The experiment does not exercise autospec's documented limitations around dynamic instance
attributes, descriptors, introspection side effects, async methods, or deeply nested objects.

### Design conclusion

Use autospec or `spec_set` when a framework-generated double is useful and a concrete API source
is honest. Prefer a tiny handwritten stub or spy when it communicates the role more clearly. Do
not add interaction assertions simply because a `Mock` records calls.

### Source

The standard-library documentation says autospecced methods use the original call signatures and
that `spec_set=True` rejects attributes outside the spec; it also warns that isolated mocks do not
prove wiring
([Python 3.14, `create_autospec`](https://docs.python.org/3.14/library/unittest.mock.html#unittest.mock.create_autospec),
[autospeccing](https://docs.python.org/3.14/library/unittest.mock.html#autospeccing)).

## SDP-FND-080-EXP-03 — A fake can drift from the real contract

| Field | Value |
|---|---|
| Precise question | Can an in-memory repository fake pass ordinary happy-path tests while violating the real adapter's case-insensitive email contract? |
| Classification | Design-level contract test + Python standard-library `sqlite3` adapter |
| Status | Reproduced |

### Why observation is necessary

“Use a fake database” can sound safer than mocking, but a fake is an implementation with its own
semantics. If those semantics differ at a boundary the application relies upon, fast tests can
give false confidence.

### Hypothesis

> The SQLite adapter will find and reject case variants because its email column uses
> `COLLATE NOCASE UNIQUE`. A naive dictionary keyed by the original string will treat variants as
> different. A fake that normalizes keys will preserve this bounded contract.

### Controls and variables

- Controlled: the same `Account` values and the same contract function.
- Changed: SQLite adapter, naive fake, contract-faithful fake.
- Measured: case-insensitive lookup plus duplicate rejection, collapsed into one boolean.

### Reproduction command

```bash
.venv/bin/python \
  units/foundations/SDP-FND-080-dependency-management-test-seams-test-doubles/practice/fake_contract_experiment.py
```

### Predicted result

```text
sqlite_adapter=True
naive_fake=False
contract_faithful_fake=True
```

### Observed result

```text
sqlite_adapter=True
naive_fake=False
contract_faithful_fake=True
```

### Interpretation

1. **Directly shown:** for the tested inputs, the SQLite adapter and normalized fake satisfy the
   same lookup-and-duplicate contract; the naive fake does not.
2. **Reasonable inference:** running shared contract examples against doubles and real adapters can
   reveal semantic drift before a higher-level test depends on it.
3. **Not shown:** the normalized fake matches every SQLite behavior, all Unicode collation rules,
   transaction isolation, concurrency, durability, SQL constraints, or a production database.

### Visual interpretation

```text
shared contract
     │
     ├── add Rahul@Example.test
     ├── find rahul@example.test
     └── reject RAHUL@example.test as duplicate
             │
      ┌──────┼──────────────┐
      ▼      ▼              ▼
   SQLite  naive dict   normalized dict
     PASS     FAIL           PASS
       │                       │
       └──── agreement on this bounded behavior only ────┘
```

#### How to read this visual

Run the same three-step contract down every branch. Matching `PASS` results mean agreement only on
those examples, not implementation equivalence.

#### Key insight

A fake earns trust by preserving the observable contract the test relies on, not by being
in-memory or handwritten.

#### Simplification or limitation

SQLite `NOCASE` and Python `str.casefold()` are not claimed to be generally equivalent. The chosen
ASCII-like synthetic addresses make this a narrow repeatable demonstration, not a Unicode or
database-collation specification.

### Design conclusion

Use a fake when its stateful behavior makes tests clearer, then run bounded contract tests against
the real adapter. Keep at least one integration path for wiring and semantics the fake cannot
represent.

### Source

Martin Fowler's summary of Gerard Meszaros's vocabulary identifies a fake as a working shortcut
that is not suitable for production and distinguishes it from stubs, spies, and mocks
([Fowler, “Mocks Aren't Stubs”](https://martinfowler.com/articles/mocksArentStubs.html#TheDifferenceBetweenMocksAndStubs)).

## Experiment regression command

```bash
.venv/bin/pytest -q \
  units/foundations/SDP-FND-080-dependency-management-test-seams-test-doubles/practice/test_dependency_seam_experiments.py
```

The experiment tests are guards for the teaching artifact. They are not substitutes for making a
prediction and explaining why each result occurred.

## Troubleshooting

- Run commands from the repository root so local practice-module imports resolve as pytest and the
  scripts expect.
- Use the locked `.venv` interpreter; system Python may not match the repository's verified
  version.
- If a patch appears to do nothing, identify the exact name evaluated by the function under test.
- If a `Mock` accepts a typo, inspect whether it has a suitable spec or whether a handwritten
  double would be clearer.
- If a fake passes but integration fails, compare concrete boundary semantics and add a shared
  contract case before adding more mocking.

## Closure

Complete only after Rahul's attempt and review:

- Final learner solution:
- Focused test output:
- Repository-wide test output:
- Design explanation:
- Rejected alternative:
- Experiment interpretations:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
