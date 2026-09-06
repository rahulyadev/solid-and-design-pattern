# Practice — SDP-PYT-070 practical interface design

| Field | Value |
|---|---|
| Unit note | [SDP-PYT-070](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-pyt-070) |
| Evidence target | `E+I+D+T` |
| Attempt required before solution | Yes |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-070-practical-interface-design-protocols-abcs-duck-typing/practice` |
| Status | Not attempted |

## Learning question

Can you replace a concrete vendor dependency with the smallest honest Python-facing interface while
preserving runtime behavior and proving both static compatibility and behavioral substitutability?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

Work in order. The starter tests pass because they characterize the current behavior. Green tests
do not mean the dependency direction or interface is already suitable.

## Starter files

- [report_export_lab.py](report_export_lab.py) couples application code to a synthetic vendor SDK
  shape.
- [test_report_export_lab.py](test_report_export_lab.py) records the observable contract without
  naming a target abstraction.

The worked audit-delivery example uses a different synthetic domain. This directory contains no
target implementation, comparison solution, hidden fixture, released hint, learner attempt, or
fabricated learning evidence.

## Problem and change pressure

`export_report(...)` accepts `PartnerBlobClient`, calls its vendor-specific `put_blob(...)` method,
then reads a broad dictionary. A local filesystem exporter and a second cloud vendor now need to
join the same use case. Some implementations are third-party and cannot inherit a class we own.

The application needs much less than the SDK exposes:

- accept one validated report and one idempotency request identifier;
- return a stable report identifier and location;
- never call the collaborator after local validation fails;
- preserve the collaborator's operational failure; and
- avoid claiming that a shallow shape check proves those behaviors.

All reports, buckets, locations, and failures are synthetic. The starter performs no real network,
filesystem, database, clock, or framework access.

## Predict before running

Record a prediction without executing code:

1. Which exact members of `PartnerBlobClient` does `export_report(...)` use?
2. Would an unrelated object with a compatible `put_blob(...)` method run successfully despite the
   concrete annotation?
3. Would a strict static checker accept that unrelated object at this call site?
4. Which parts of the current behavior are application promises, and which leak vendor vocabulary?
5. What could a `Protocol` verify that runtime duck typing cannot?
6. What could neither a `Protocol` nor an ABC prove about idempotency or failures?
7. Does this boundary need shared implementation or an intentional runtime family?

No learner prediction has been recorded by the maintainer.

## Run and observe

From the repository root:

```bash
uv run --locked python units/pythonic/SDP-PYT-070-practical-interface-design-protocols-abcs-duck-typing/practice/report_export_lab.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-070-practical-interface-design-protocols-abcs-duck-typing/practice
```

Record the exact runtime and output. Then add one temporary probe using an unrelated object with the
same `put_blob(...)` shape. Compare what happens at runtime with what strict mypy reports. Do not
treat maintainer-generated starter results as learner evidence.

## Phase A — write the behavioral contract first

Before choosing a mechanism, state:

- accepted inputs and local validation order;
- the smallest success result the application needs;
- failure propagation or translation policy;
- idempotency meaning and ownership;
- side-effect count on success and failure; and
- any thread-safety, lifecycle, or retry promise.

Add a shared behavior-test helper that can run against at least two factories. Do not assert concrete
private fields or inheritance unless those are intentional public requirements.

## Phase B — choose the smallest interface

Choose one primary form and defend it:

- a plain callable when the collaboration is one stateless operation;
- ordinary duck typing when the boundary is local and static feedback adds little;
- a client-owned `Protocol` when independent implementations need static structural checking; or
- an ABC only if direct subclasses form an owned family that needs abstract-member enforcement or
  useful shared behavior.

If the vendor vocabulary differs from the application vocabulary, add an adapter. Do not register a
third-party class merely to avoid writing the translation that the boundary really needs.

Add a positive static conformance witness. Add one deliberately incompatible candidate in a
temporary or documented negative checker case; do not leave the repository's normal mypy run red.

## Phase C — prove runtime and static claims separately

Add focused checks for:

- two structurally independent implementations preserving the same behavior contract;
- the incompatible signature being rejected by strict static checking;
- the real call—not `isinstance()`—exercising the runtime behavior;
- failures before and after the side-effect boundary;
- Unicode, colons, and literal pipes in identifiers or content;
- zero, one, and repeated calls; and
- the chosen idempotency semantics.

If you experiment with `@runtime_checkable`, include a wrong-signature object that still has the
right member name. Explain why recognition can succeed while the real call fails.

## Phase D — compare with an ABC honestly

Sketch an owned ABC variation only long enough to answer:

- Which abstract members block incomplete direct subclasses from instantiation?
- What real shared algorithm earns inheritance?
- Would a virtual subclass receive that algorithm through its MRO?
- Does registration validate a signature or business behavior?
- Does the client need an `isinstance()` branch at all?

Delete the ABC variation if the answers do not justify its coupling.

## Required edge cases

- Empty, surrounding-space, Unicode, colon-containing, and pipe-containing input.
- Local validation failure before collaborator invocation.
- Collaborator success, timeout, malformed result, and duplicate request.
- Two independent implementations plus one incompatible same-name method.
- A test fake with only the client-required capability.
- Repeat delivery under the documented idempotency rule.
- One concurrency scenario stated explicitly, even if the starter stays synchronous.
- A deliberately shallow runtime-recognition probe when `@runtime_checkable` is considered.

## Rahul's attempt

- Attempt file: —
- Prediction: —
- Interface choice and change pressure: —
- Rejected alternative: —
- Runtime evidence: —
- Static evidence: —
- Test result: —

## Progressive hints

No hints are released. Ask for one at a time after recording an attempt.

## Observe and explain

After refactoring, explain:

1. Which boundary does the client own?
2. What happens at runtime when an annotated parameter receives an object?
3. Which conformance claim did mypy establish, and what did it not establish?
4. Which shared behavior tests demonstrate substitutability?
5. Why is an adapter better than inheritance for the foreign SDK here?
6. What would justify replacing the chosen form with an ABC?
7. Which abstraction could still be removed?

## Refactor checkpoint

The target is not “use a `Protocol`.” It is a small client-owned contract, honest runtime behavior,
useful static feedback where justified, independent implementation tests, and no stronger coupling
than the change pressure earns.

## Vary

Choose one change pressure:

- exports become asynchronous and cancellable;
- batch export must be all-or-nothing;
- the SDK returns retryable and permanent failures through one exception type;
- a plugin loader needs deliberate runtime admission; or
- many callers require discoverable shared configuration and lifecycle methods.

State whether the call shape, behavior contract, adapter, test suite, or interface mechanism changes.

## Troubleshooting

- Run from the repository root so pytest resolves the sibling starter module.
- If runtime succeeds but mypy rejects a call, compare annotations and the complete signature,
  including keyword-only parameter names.
- If `isinstance(candidate, RuntimeProtocol)` succeeds but the call fails, remember that the check is
  shallow and ignores signatures.
- If a registered virtual subclass cannot call the ABC's concrete method, inspect its MRO.
- If every test fake implements ten unused methods, shrink the client-facing boundary.
- If an ABC exists only to spell one abstract method, try a callable or `Protocol`.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution: —
- Optional comparison solution: —
- Trade-offs: —
- Remaining weakness: —
- Evidence link for `PROGRESS.md`: —
