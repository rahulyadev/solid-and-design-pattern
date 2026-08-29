# Practice — SDP-FND-050 Composition, delegation, and inheritance

| Field | Value |
|---|---|
| Unit note | [SDP-FND-050](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-050) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Focused test command | `.venv/bin/pytest -q units/foundations/SDP-FND-050-composition-delegation-inheritance/practice` |
| Status | Not attempted |

The deterministic starter and runtime experiments have been executed to verify the artifact. That
does not count as Rahul's attempt, design explanation, or learning evidence.

## Learning question

When requirements change along independent axes, which relationships should be composition,
which calls should be delegation, and which—if any—should remain inheritance?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

Do not begin by replacing the code with a memorized “composition over inheritance” shape. First
predict the current lookup and call flow, identify the exact change collision, and defend every
relationship in the revised design.

## Starter files

```text
practice/
├── README.md
├── reminder_lab.py
├── test_reminder_lab.py
├── special_method_delegation_experiment.py
├── cooperative_mro_experiment.py
└── test_runtime_experiments.py
```

- `reminder_lab.py` is the unsolved refactoring starter.
- `test_reminder_lab.py` characterizes current observable behaviour and one deliberate API leak.
- The two experiment scripts are completed observation tools, not the lab solution.
- `test_runtime_experiments.py` makes their outputs reproducible.

## Problem

`RenewalReminderService` sends subscription-renewal SMS messages. It inherits from `SmsGateway`
only to reuse `send_message()` and transport state.

The design currently works, but the relationship says more than the business needs:

- the reminder service is recognized as an `SmsGateway`;
- every public gateway operation becomes part of the service's surface;
- a caller can send a transport-only message without the reminder policy or audit effect;
- business construction is coupled to the SMS gateway's constructor and lifetime;
- adding another channel pressures the design toward another service subclass.

The exercise is not “remove all inheritance.” It is to decide which observable promises justify a
type relationship and which implementation reuse should become an object collaboration.

## Current structure and call flow

```text
CLASS RELATIONSHIP                       ONE reminder call

RenewalReminderService                   caller
          │ inherits                         │ remind(customer, 3)
          ▼                                  ▼
      SmsGateway                 RenewalReminderService
          │ owns transport state             │ build SMS body
          │                                   │ inherited lookup
          └── send_message() ◀────────────────┘
                              │
                              ├── record SentMessage
                              └── return ID → append audit → receipt

Unwanted extra path:
caller → service.send_message(...) → transport effect with no reminder audit
```

### How to read this visual

Read the left side as a class relationship and the right side as runtime messages. Inheritance
makes gateway methods available through method lookup. The reminder call then reuses one of those
methods. The final line shows that the same inherited API is also callable without `remind()`.

### Key insight

The current reuse mechanism changes what the service *is* and what it publicly offers, even though
the business need is only to *use* one transport capability.

### Simplification or limitation

This is a conceptual design and call-flow visual. It omits descriptors, the full attribute lookup
algorithm, network failures, concurrency, and vendor SDK state. `SmsGateway` is a deterministic
synthetic stand-in, not a real provider implementation.

## Current observable behaviour

Before refactoring, predict and then confirm:

1. A valid reminder returns a deterministic `ReminderReceipt`.
2. The transport records the exact recipient, sender, and body.
3. The audit entry is appended only after a successful send.
4. Non-positive `days_remaining` is rejected before transport or audit mutation.
5. Successful message IDs advance from `msg-001`.
6. The service is currently an instance of `SmsGateway`.
7. A caller can invoke `service.send_message(...)` and bypass reminder auditing.

Items 1–5 are stable behaviours for the first refactoring. Items 6–7 characterize the design pain;
they should not be preserved as desired public contracts.

## Change pressure

Add the following requirements without changing the stable reminder meaning:

1. Support an email transport in addition to SMS.
2. Select a channel for a request without duplicating the message policy in one subclass per
   channel.
3. Add a retry rule for explicitly transient transport failures only.
4. Keep audit behaviour independent of channel selection and retry policy.
5. Prevent callers from treating the business service as a raw transport client.
6. Allow a deterministic test transport to be supplied without subclassing the business service.
7. Make collaborator ownership explicit: a shared transport must not be closed by a service that
   merely borrows it.

Do not implement a real email or network integration. A deterministic in-memory collaborator is
enough to expose the design forces.

## Decision worksheet — complete before code changes

For each row, write **direct code**, **composition**, **delegation**, or **inheritance**, then defend
the choice from the change pressure rather than from a slogan.

| Relationship or action | Choice | Concrete force | Promise created | Rejected alternative |
|---|---|---|---|---|
| Reminder policy to transport capability |  |  |  |  |
| `remind()` to the operation that performs delivery |  |  |  |  |
| SMS and email implementations |  |  |  |  |
| Retry behaviour to transport behaviour |  |  |  |  |
| Domain failure categories, if introduced |  |  |  |  |
| Shared collaborator lifetime |  |  |  |  |

Then answer:

- Which decision changes independently?
- Which object owns each mutable list or connection-like resource?
- Which object is allowed to close or replace each collaborator?
- Which public operations should a caller discover on the reminder service?
- If inheritance remains, can every instance honestly satisfy the base promise?
- Does an override need undocumented base state or call order?

## Required refactoring evidence

Your attempt must include all of the following:

1. Preserve the original starter before editing through Git history or a clearly named attempt
   copy; do not overwrite evidence silently.
2. Draw the before and after object graphs separately from the call sequence.
3. Mark ownership versus a borrowed reference for every mutable collaborator.
4. Keep current stable business tests passing or explain an intentional contract change.
5. Replace the test that celebrates the raw-gateway API leak with a test of the intended boundary.
6. Add a second deterministic channel without copying the reminder policy.
7. Test one transient failure followed by success and one permanent failure with no retry.
8. Prove that a rejected request creates neither a transport effect nor an audit entry.
9. State whether any inheritance remains and why substitution is honest there.
10. Name one simpler design you rejected and one abstraction you deliberately did not add.

Passing tests without the relationship and ownership explanation is incomplete evidence.

## Required edge cases

- blank customer fields;
- zero and negative `days_remaining`;
- blank recipient at the transport boundary;
- transport rejection before an audit record exists;
- retry exhaustion with no duplicate success record;
- a shared collaborator used by two service instances;
- unsupported channel selection;
- two successful sends with deterministic, distinct IDs.

Do not add timing, randomness, internet access, credentials, or a real provider.

## Commands

From the repository root:

```bash
.venv/bin/python units/foundations/SDP-FND-050-composition-delegation-inheritance/practice/reminder_lab.py
.venv/bin/pytest -q units/foundations/SDP-FND-050-composition-delegation-inheritance/practice/test_reminder_lab.py
.venv/bin/python units/foundations/SDP-FND-050-composition-delegation-inheritance/practice/special_method_delegation_experiment.py
.venv/bin/python units/foundations/SDP-FND-050-composition-delegation-inheritance/practice/cooperative_mro_experiment.py
.venv/bin/pytest -q units/foundations/SDP-FND-050-composition-delegation-inheritance/practice
```

When the normal `uv` cache is writable, the equivalent commands may be prefixed with `uv run`.
The recorded verification used the locked `.venv` interpreter directly because the execution
sandbox made the user-level `uv` cache read-only.

## Verified starter baseline

The focused practice suite ran on 2026-08-29:

```text
..........                                                               [100%]
10 passed in 0.14s
```

This proves the distributed starter is runnable and its recorded experiments are reproducible. It
does not prove the required refactor, design defence, or Rahul's understanding.

## Prediction before running

Complete this before the first learner run:

- Expected `remind()` result:
- Attribute lookup path for `self.send_message`:
- Object that owns `_sent_messages`:
- Effect order on success:
- Effect order on rejection:
- Public method that should not belong to the business service:
- Requirement most likely to cause subclass growth:
- Reasoning:

## Rahul's attempt

- Attempt file or commit:
- Before object graph:
- After object graph:
- Call sequence:
- Decision worksheet:
- Rejected alternative:
- Focused test result:
- Edge-case result:
- Design explanation:

## Progressive hints

Do not add or reveal hints until requested. Give only one hint at a time and identify the first
incorrect assumption before suggesting code.

## Observe and explain

After the baseline and after each refactoring step, answer:

1. Which names arrived on `RenewalReminderService` only because of inheritance?
2. Which state belongs to transport, business policy, and audit responsibility?
3. Does the revised object graph let transport and policy change independently?
4. Which method delegates, and what does it do before and after delegation?
5. Which exceptions cross the boundary, and which remain provider details?
6. Can a caller still bypass the business operation through an exposed collaborator?
7. Did the refactor replace one rigid hierarchy with a needless family of wrapper classes?

## Refactor checkpoints

Work in small behaviour-preserving steps:

1. Keep the current characterization tests green.
2. Identify the smallest transport capability the business policy actually needs.
3. Introduce one seam without adding the second channel yet.
4. Move construction to the composition boundary.
5. Replace the deliberate API-leak characterization with the intended boundary assertion.
6. Add the second deterministic transport.
7. Add transient-failure handling at the smallest boundary that owns retry policy.
8. Re-run focused tests after every step.
9. Remove any abstraction unsupported by the final requirements.

Do not start by designing a universal plugin framework, service locator, or deep interface tree.

## Controlled experiment 1 — automatic delegation and special methods

### Precise question

If `__getattr__` forwards missing attributes to a contained list, do ordinary method calls,
`len(wrapper)`, and `wrapper[index]` all delegate in the same way?

### Classification

Python language mechanics. This experiment explains a limitation of automatic delegation; it does
not compare design quality or performance.

### Hypothesis

> `append` and `count` will reach the contained list after ordinary lookup invokes `__getattr__`,
> but implicit `len` and subscripting will fail because Python looks up their special methods on
> the wrapper's type rather than forwarding through the instance fallback.

### Environment

```text
Date: 2026-08-29
Operating system: Linux 7.0.0-30-generic, glibc 2.43
Architecture: x86_64
Python: CPython 3.14.7
sys.implementation: cpython
Dependencies: Python standard library only
Relevant flags: normal execution
```

### Controls and variables

- Controlled: one wrapper type, one contained `list[int]`, one interpreter, no monkeypatching.
- Changed: ordinary explicit attribute call versus implicit special-method syntax.
- Measured: resulting value or stable exception class.

### Reproduction command

```bash
.venv/bin/python units/foundations/SDP-FND-050-composition-delegation-inheritance/practice/special_method_delegation_experiment.py
```

### Observed result

The command ran on 2026-08-29 and produced:

```text
explicit_append=(10, 20, 30)
explicit_count=1
implicit_len=TypeError
implicit_getitem=TypeError
```

### Interpretation

The result directly shows that these ordinary missing attributes were forwarded while these two
implicit operations were not. The Python data model specifies that implicit special-method lookup
generally bypasses instance lookup machinery, including instance `__getattribute__`; defining
`__getattr__` is therefore not a transparent substitute for implementing the relevant protocol on
the wrapper type
([Python 3.14 data model, “Special method lookup”](https://docs.python.org/3.14/reference/datamodel.html#special-method-lookup)).

The result does not prove that explicit delegation is always preferable or that every special
method must be copied. A wrapper should implement only the public capabilities it intends to
promise.

### Visual interpretation

```text
wrapper.append(30)
  │ ordinary lookup misses on wrapper
  └── __getattr__("append") ──> contained list.append ──> succeeds

len(wrapper)
  │ implicit __len__ lookup on type(wrapper)
  └── no DelegatingList.__len__ ────────────────────────> TypeError
```

#### How to read this visual

Read each path from syntax to lookup owner. The first path reaches the instance fallback. The
second asks the wrapper type for protocol participation and never treats the contained list as the
wrapper's type.

#### Key insight

Broad attribute forwarding can look transparent in a few calls while still exposing an incomplete
and surprising protocol.

#### Simplification or limitation

The visual covers one wrapper and selected operations. Descriptor precedence, binary reflected
operations, iteration fallbacks, static typing, pickling, and framework introspection need separate
analysis when they are part of the promised API.

### Design conclusion

Prefer explicit delegation for a narrow business boundary. Use automatic delegation only when a
broad proxy surface is intentional, documented, tested—including required special methods—and
worth the discoverability and compatibility cost. The official Python FAQ demonstrates
`__getattr__` forwarding as one delegation mechanism; it does not make that wrapper automatically
identical to its collaborator
([Python 3.14 Programming FAQ, “What is delegation?”](https://docs.python.org/3.14/faq/programming.html#what-is-delegation)).

## Controlled experiment 2 — `super()` follows the MRO

### Precise question

In `CombinedHandler(AuditLayer, RetryLayer)`, does `super().handle()` inside `AuditLayer` jump to
its textually named base `TerminalHandler`, or to the next class in `CombinedHandler`'s MRO?

### Classification

Python language mechanics. The experiment observes cooperative multiple-inheritance dispatch; it
does not recommend this hierarchy for retry and audit policy.

### Hypothesis

> The MRO will be `CombinedHandler, AuditLayer, RetryLayer, TerminalHandler, object`, so the
> `super()` call in `AuditLayer` will reach `RetryLayer` before `TerminalHandler`.

### Controls and variables

- Controlled: fixed class definitions, signatures, interpreter, and one call.
- Changed: no runtime input; the declared base order is the inspected condition.
- Measured: `__mro__` and the deterministic before/after trace.

### Reproduction command

```bash
.venv/bin/python units/foundations/SDP-FND-050-composition-delegation-inheritance/practice/cooperative_mro_experiment.py
```

### Observed result

The command ran on 2026-08-29 and produced:

```text
mro=CombinedHandler -> AuditLayer -> RetryLayer -> TerminalHandler -> object
trace=AuditLayer.before -> RetryLayer.before -> TerminalHandler -> RetryLayer.after -> AuditLayer.after
```

### Interpretation

The trace directly shows `RetryLayer` executing between `AuditLayer` and `TerminalHandler`.
`super()` returns a proxy whose search begins after the current class in the relevant MRO; it does
not mean “call my one fixed parent”
([Python 3.14 built-in `super`](https://docs.python.org/3.14/library/functions.html#super)).

Python uses a linearized resolution order for multiple inheritance and requires cooperative
participants to use compatible signatures and call `super()` consistently. The official tutorial
describes the ordering properties; more complex hierarchies may even be impossible to linearize
([Python 3.14 classes tutorial, “Multiple Inheritance”](https://docs.python.org/3.14/tutorial/classes.html#multiple-inheritance),
[Python MRO HOWTO](https://docs.python.org/3.14/howto/mro.html)).

### Visual interpretation

```text
CombinedHandler.__mro__

Combined → Audit → Retry → Terminal → object
              │       │        │
call handle ──┘       │        │
Audit super() ────────┘        │
Retry super() ─────────────────┘
```

#### How to read this visual

Read left to right along the actual MRO. Each cooperative method performs work and asks the proxy
to continue after its own class. The arrows are dispatch order, not object ownership.

#### Key insight

A cooperative `super()` call is hierarchy-relative. Adding or reordering a base can change which
implementation executes next without editing the method containing that call.

#### Simplification or limitation

This controlled diamond uses one method, compatible arguments, and no state. Real mixins can also
collide on initialization, attributes, exceptions, return values, and side-effect order.

### Design conclusion

Multiple inheritance can deliberately compose cooperative class behaviours, but it creates a
shared protocol across the whole MRO. For independently selectable retry and audit policy, object
composition is usually easier to wire, inspect, and vary. This is a judgment from the stated change
forces, not a claim that multiple inheritance is universally wrong.

## Vary — production-design transfer

After the local refactor, move transport behind a synthetic remote boundary. Do not add a real
provider. Produce a design note answering:

- Which object owns connection setup and shutdown?
- Is the transport shared, pooled, request-scoped, or process-scoped?
- Which failures are transient, permanent, or ambiguous after a timeout?
- Can a retry duplicate a delivered reminder, and what idempotency key would contain that risk?
- Does audit record intent, provider acceptance, durable delivery, or all three as separate events?
- Which concrete provider facts belong in logs without leaking credentials or message contents?
- Can channel choice change at runtime, and who may mutate it safely?
- Which tests are reusable across SMS, email, and an in-memory implementation?
- What observable promise, if any, still justifies inheritance?

The transfer is complete only when ownership, failure semantics, retries, and duplicate effects are
explicit. Adding a class named `Repository`, `Manager`, or `Factory` is not evidence by itself.

## Troubleshooting

- Run commands from the repository root so the practice imports resolve consistently.
- If `uv run` cannot write its user cache in a restricted environment, use the locked `.venv/bin`
  commands shown above; do not install a second environment into the unit.
- The raw-gateway characterization is expected to conflict with the desired refactor. Preserve the
  original evidence, then replace that assertion deliberately rather than weakening it silently.
- If every collaborator receives `*args` and `**kwargs`, make the intended capability explicit
  before diagnosing inheritance.
- Do not forward every unknown attribute merely to make old tests pass; decide the promised API.
- A composed collaborator is not automatically owned. Record who created it and who closes it.
- Do not catch every exception and retry. Validation and permanent rejection are not transient.
- A mock assertion about private call order is not a substitute for observable behaviour.
- Do not introduce `Protocol`, ABC, metaclass, or plugin machinery unless the attempt has a concrete
  typing, runtime registration, or extension requirement.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Before and after visuals:
- Decision worksheet:
- Focused and edge-case test results:
- Runtime experiment interpretations:
- Production-design transfer:
- Rejected alternative:
- Trade-offs:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
