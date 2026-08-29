# Practice — SDP-FND-070 Duck typing, structural typing, nominal typing, Protocols, and ABCs

| Field | Value |
|---|---|
| Unit note | [SDP-FND-070](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-070) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Focused test command | `.venv/bin/pytest -q units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice` |
| Status | Not attempted |

The deterministic starter and three mechanics experiments have been executed to verify the
artifact. That does not count as Rahul's prediction, interface decision, refactoring, contract
explanation, or learning evidence.

## Learning question

For a client that needs one alert-delivery operation from first-party, third-party, test, and
legacy collaborators, when should the boundary rely on ordinary duck typing, a small
`typing.Protocol`, an ABC, nominal inheritance, a callable, or an adapter?

## Lab cycle

```text
predict → run → observe → explain → state the contract → choose → refactor → vary
```

Do not begin by replacing `AlertChannel` with `Protocol`. First distinguish the current facts:

1. which objects can actually perform the operation;
2. which objects pass the nominal runtime gate;
3. which relationship the client genuinely needs;
4. what static feedback is required;
5. which behavioural promises no type mechanism can prove.

## Starter files

```text
practice/
├── README.md
├── alert_delivery_lab.py
├── test_alert_delivery_lab.py
├── protocol_runtime_experiment.py
├── abc_virtual_subclass_experiment.py
├── protocol_static_experiment.py
└── test_runtime_experiments.py
```

- `alert_delivery_lab.py` is the unsolved application-boundary refactoring starter.
- `test_alert_delivery_lab.py` characterizes stable behaviour and one deliberate nominal-coupling
  pain.
- `protocol_runtime_experiment.py` is a completed observation tool for actual calls versus shallow
  runtime protocol checks.
- `abc_virtual_subclass_experiment.py` is a completed observation tool for direct and virtual ABC
  relationships.
- `protocol_static_experiment.py` runs isolated positive and negative mypy cases without leaving
  the repository's normal type-check failing.
- `test_runtime_experiments.py` makes all experiment outputs reproducible.

## Problem

An operations service delivers a validated `Alert` through configured channels.

The starter has:

- `EmailChannel` and `SmsChannel`, which directly inherit `AlertChannel`;
- `PartnerWebhookChannel`, an unrelated class with a compatible
  `deliver(Alert) -> DeliveryReceipt` operation;
- `LegacyPager`, whose `push(text, priority) -> str` API has a genuinely different shape;
- `deliver_alert()`, whose annotation and `isinstance()` preflight require nominal
  `AlertChannel` membership;
- `deliver_batch()`, which preserves channel order but inherits the same restriction.

The partner implementation works when called directly. The client rejects it before making the
same call.

The lab is not “make every object pass.” You must select mechanisms for two different cases:

1. **Compatible but unrelated:** use the partner without modifying its class or lying about its
   API.
2. **Incompatible legacy API:** translate arguments, result, and failure meaning deliberately.

## Current structures and call flow

```text
NOMINAL CLASS GRAPH                         CURRENT CLIENT FLOW

            AlertChannel (ABC)              deliver_alert(alert, channel)
                ▲       ▲                              │
                │       │                              ▼
             Email     SMS                    isinstance(AlertChannel)?
                                                        │
PartnerWebhook ── no inheritance ───────────────────────┤ false → TypeError
       │                                                │ true
       └─ deliver(Alert) -> DeliveryReceipt             ▼
                                                channel.deliver(alert)

LegacyPager ── push(text, priority) -> str      shape and meaning differ
```

### How to read this visual

Read the class graph on the left and the client algorithm on the right. The partner already has
the operation at the bottom-left, but the right-side gate asks a different question—nominal family
membership—before using it. The pager is separate because it does not have the required shape.

### Key insight

Remove accidental nominal coupling for the partner; do not erase a real adaptation requirement
for the pager.

### Simplification or limitation

This diagram omits static checker reasoning, result invariants, provider failures, external side
effects, and ABC metaclass details. It does not claim that every unrelated same-shaped object is
behaviourally compatible.

## Current observable behaviour

Predict before running, then confirm:

1. Critical email and SMS receipts are returned in input order.
2. SMS treats an `info` alert as normal policy non-delivery, not a provider exception.
3. The partner returns a coherent receipt when called directly.
4. `deliver_alert()` rejects that same partner because `isinstance(partner, AlertChannel)` is
   false.
5. `EmailChannel` and `SmsChannel` include the ABC in their MRO.
6. An incomplete direct subclass cannot be instantiated.
7. The legacy pager has `push`, not `deliver`.
8. Frozen alerts are unchanged by delivery.
9. Invalid alert and incoherent receipt states fail before boundary selection.
10. An empty batch is a valid no-work request.

Items 1, 2, 8, 9, and 10 are stable observable behaviour. Items 3 and 4 expose the coupling
decision. Items 5 and 6 are ABC mechanics to preserve only if the final design still needs them.
Item 7 requires adaptation rather than structural wishful thinking.

## Change pressure

Refactor for these requirements:

1. `deliver_alert()` must accept unrelated, statically compatible alert channels without editing
   those channel classes.
2. Client runtime code must use the operation directly rather than admit collaborators through a
   concrete or nominal preflight gate.
3. The accepted typed boundary must contain only members this client needs.
4. `deliver_batch()` must preserve exact input order and one receipt per channel.
5. Every advertised channel must accept every valid `Alert`; normal policy suppression is a
   coherent non-delivery receipt.
6. Unexpected provider failure must remain distinguishable from normal non-delivery.
7. Input and result value invariants must remain enforced.
8. A compatible test fake must not inherit production implementation machinery.
9. The legacy pager must be usable only through an explicit translation boundary.
10. The final explanation must say whether `AlertChannel` still earns a role and, if so, for which
    clients or implementations.
11. Static evidence must demonstrate one unrelated compatible acceptance and one incompatible
    signature rejection.
12. No `@runtime_checkable` query may be presented as signature or behaviour validation.

Do not add a factory, registry, service locator, framework, network SDK, or plugin loader. They do
not address the current learning question.

## Contract worksheet — complete before editing code

Write concrete client-visible rules. Do not write only “works” or “correct.”

| Contract dimension | Required promise | Allowed implementation variation | Breaking example | Evidence type |
|---|---|---|---|---|
| Accepted alerts |  |  |  |  |
| Delivered receipt |  |  |  |  |
| Policy non-delivery |  |  |  |  |
| Invalid input |  |  |  |  |
| Provider failure |  |  |  |  |
| Input mutation |  |  |  |  |
| Batch ordering |  |  |  |  |
| External side effects |  |  |  |  |
| Retry/idempotency |  |  |  |  |

Then mark each rule as one or more of:

- enforced by `Alert` or `DeliveryReceipt`;
- expressible in a method signature;
- checked statically;
- exercised by a shared behavioural test;
- verified only at a provider integration boundary;
- documented but not yet mechanically proven.

## Mechanism-selection worksheet

Complete before naming the final boundary:

| Candidate | Concrete requirement it solves here | Cost introduced | Keep or reject |
|---|---|---|---|
| Plain direct duck typing |  |  |  |
| `Callable[[Alert], DeliveryReceipt]` |  |  |  |
| Client-owned `Protocol` |  |  |  |
| Direct ABC inheritance |  |  |  |
| ABC virtual registration |  |  |  |
| `@runtime_checkable` protocol |  |  |  |
| Ordinary nominal base class |  |  |  |
| Pager adapter |  |  |  |

Required questions:

1. Is `deliver` a useful domain name that a bare callable would hide?
2. Does the client need static member/signature feedback?
3. Must implementations be unrelated and unmodifiable?
4. Does any final client need runtime family categorization?
5. Is shared base implementation genuinely useful?
6. Must direct subclasses be blocked until they implement primitives?
7. Would virtual registration make a stronger claim than the registering code has verified?
8. Does the pager differ only syntactically, or also semantically?
9. Which choice preserves dependency direction toward client policy?
10. Which mechanism are you deliberately not adding?

## Required refactoring evidence

Your attempt is complete only when it includes all of the following:

1. Preserve the starter through Git history or a clearly named attempt copy.
2. Record predictions before the first learner run.
3. Complete the contract worksheet before the structural refactor.
4. Complete the mechanism-selection worksheet with at least two rejected alternatives.
5. Draw the pre-refactor nominal gate and post-refactor runtime call separately.
6. Make `PartnerWebhookChannel` work through `deliver_alert()` without changing its bases.
7. Keep the runtime client free from a concrete/nominal preflight check.
8. Demonstrate static acceptance of the partner-shaped implementation.
9. Demonstrate static rejection of one wrong method signature.
10. Add a reusable behavioural contract test for all advertised channels.
11. Preserve batch order, non-delivery meaning, immutability, and value invariants.
12. Add an adapter for `LegacyPager`; do not modify `LegacyPager.push()` into the target shape.
13. Exercise one synthetic pager/provider failure without swallowing it as policy non-delivery.
14. State whether the ABC remains, is narrowed to another role, or is removed—and why.
15. Compare the final choice with a direct callable.
16. Explain why passing mypy and passing `isinstance` are not behavioural proof.
17. Run focused pytest, Ruff, mypy, and all three experiments.
18. Identify one abstraction deliberately omitted.

Passing tests alone is insufficient. A design can pass examples while its failure meaning,
dependency direction, or interface ownership remains wrong.

## Required edge cases

- blank event ID;
- blank message;
- unknown severity;
- `info`, `warning`, and `critical` alerts through every advertised channel;
- SMS policy non-delivery remains distinct from exceptional failure;
- delivered receipt with blank or missing provider reference rejected;
- delivered receipt with a non-delivery reason rejected;
- non-delivery with provider reference rejected;
- non-delivery without a reason rejected;
- empty channel tuple;
- batch result order matches channel input order;
- repeated use of one immutable alert;
- unrelated compatible partner through the client;
- a compatible fake without production inheritance;
- a wrong-signature candidate rejected statically;
- pager priority mapping at all severities;
- synthetic pager/provider exception retains cause/context;
- adding one new compatible channel requires no edit to the client algorithm.

Do not introduce timing, randomness, real network access, credentials, mutable global
registration, or a vendor dependency.

## Commands

From the repository root:

```bash
.venv/bin/python units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice/alert_delivery_lab.py
.venv/bin/pytest -q units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice/test_alert_delivery_lab.py
.venv/bin/python units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice/protocol_runtime_experiment.py
.venv/bin/python units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice/abc_virtual_subclass_experiment.py
.venv/bin/python units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice/protocol_static_experiment.py
.venv/bin/pytest -q units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice
```

Quality checks:

```bash
.venv/bin/ruff check units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice
.venv/bin/mypy units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice
```

Repository validation:

```bash
python scripts/validate_repo.py
```

The locked `uv run` equivalents are valid when the user-level `uv` cache is writable.

## Verified starter baseline

The focused practice suite ran on 2026-08-29:

```text
........................                                                 [100%]
24 passed in 4.30s
```

Ruff and mypy also ran:

```text
All checks passed!
Success: no issues found in 6 source files
```

The exact pytest duration can vary. These results prove only that the distributed starter,
characterization tests, and controlled experiments are runnable. They do not prove the required
refactoring or Rahul's understanding.

## Prediction before running

Complete this before the first learner run:

- Critical email receipt:
- Critical SMS receipt:
- `info` SMS behaviour:
- Direct partner behaviour:
- Partner behaviour through `deliver_alert()`:
- Result of `isinstance(partner, AlertChannel)`:
- Whether `AlertChannel` appears in the partner MRO:
- Incomplete direct subclass construction result:
- Empty batch result:
- Whether delivery mutates the alert:
- Which current line owns the compatibility decision:
- Which of these facts a static `Protocol` annotation would change at runtime:

Experiment predictions:

- Wrong-signature object under runtime-checkable protocol:
- Wrong-signature actual call:
- Dynamic `__getattr__` object under `hasattr`:
- Dynamic object under runtime protocol on Python 3.14:
- Virtual ABC subclass in MRO:
- Virtual subclass access to ABC concrete method:
- Registered incomplete object's `isinstance` result:
- Mypy result for unrelated compatible class:
- Mypy result for wrong signature:

## Rahul's attempt

- Attempt file or commit:
- Prediction:
- Contract worksheet:
- Mechanism-selection worksheet:
- Before visual:
- After visual:
- Partner compatibility evidence:
- Pager adapter evidence:
- Static positive case:
- Static negative case:
- Shared behavioural tests:
- Edge-case results:
- Rejected alternatives:
- Remaining or removed ABC role:
- Callable comparison:
- Omitted abstraction:
- Focused pytest result:
- Ruff result:
- Mypy result:
- Final explanation:

## Progressive hints

Do not add or reveal hints until requested. Give exactly one hint at a time. Before suggesting code,
identify the first incorrect assumption among these categories:

- confusing runtime callability with nominal recognition;
- confusing structural static acceptance with runtime validation;
- treating runtime protocol presence as signature proof;
- assuming ABC registration supplies inheritance;
- using typing to avoid a real adapter;
- choosing a mechanism before writing the client contract.

The original attempt must remain preserved before any hint-driven edit.

## Observe and explain

After the baseline and after each refactoring checkpoint, answer:

1. Which exact line rejects the partner before the refactor?
2. Can the partner perform the operation without any type-mechanism change?
3. What static evidence is missing from ordinary duck typing here?
4. What runtime code would a `Protocol` annotation add?
5. Why is a `Callable` plausible, and why might the method name still be useful?
6. Which ABC benefit exists in the starter besides the nominal gate?
7. Does the final client still need that benefit?
8. What does virtual registration change in `isinstance()` and MRO?
9. Why can an incomplete registered class still be recognized?
10. Why does the pager need an adapter rather than a wider protocol?
11. Which result rules are enforced by `DeliveryReceipt`?
12. Which failure rules require behavioural or integration tests?
13. How could `Any` hide a wrong provider signature?
14. Which new implementation can be added without editing the client?
15. What evidence would be required before claiming behavioural substitutability?

## Refactor checkpoints

Work in small, attributable steps:

1. Run all starter characterization tests unchanged.
2. Record predictions and actual differences.
3. Complete the client contract worksheet.
4. Add a failing test for the partner through the client.
5. Remove only the runtime nominal admission decision.
6. Re-run stable behavioural tests.
7. Decide whether plain duck typing is an acceptable endpoint; record the answer.
8. Add the smallest static boundary only if the requirements demand it.
9. Run a static positive partner case and negative wrong-signature case.
10. Extract reusable behavioural contract cases.
11. Add the pager adapter and its failure translation tests.
12. Re-evaluate the ABC role; remove or retain it deliberately.
13. Compare the result with a callable boundary.
14. Add one new structurally compatible channel without editing client control flow.
15. Run all focused and repository checks.

At every checkpoint, label the change as one or more of:

- runtime behaviour;
- static feedback;
- nominal relationship;
- dependency direction;
- behavioural contract;
- test evidence;
- vocabulary/documentation.

## Controlled experiment 1 — runtime Protocol recognition versus actual calls

### Precise question

Can a same-named wrong-signature method pass a runtime-checkable protocol query and still fail when
called? Can an operation supplied through `__getattr__` work when called but fail the Python 3.14
runtime protocol query?

### Classification

Standard-library and version-dependent behaviour for `typing.runtime_checkable`, plus ordinary
runtime call behaviour. This is not a CPython bytecode or cache claim.

### Hypothesis

> The compatible sender will pass and run. The wrong-signature sender will pass the shallow
> runtime presence query but fail the actual call. The dynamic sender will satisfy `hasattr` and
> run, but Python 3.14's `inspect.getattr_static`-based protocol lookup will not recognize its
> dynamically generated member.

### Environment

```text
Date: 2026-08-29
Operating system: Linux 7.0.0-30-generic, glibc 2.43
Architecture: x86_64
Python version: 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation: cpython
Dependencies: Python standard library only
Relevant flags: none
```

### Controls and variables

- Controlled: protocol member name, input text, output labels, fresh process.
- Changed: compatible signature, incompatible signature, and dynamic attribute provision.
- Observed: actual result/exception, `hasattr`, and runtime protocol recognition.

### Reproduction command

```bash
.venv/bin/python units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice/protocol_runtime_experiment.py
```

### Observed result

```text
compatible_call=ok:5
compatible_runtime_protocol=True
wrong_runtime_protocol=True
wrong_actual_call=TypeError
dynamic_hasattr=True
dynamic_call=dynamic:5
dynamic_runtime_protocol=False
```

### Interpretation

1. The compatible object both ran and passed the query.
2. The wrong-signature object had the member name, so the runtime query returned true.
3. Calling that method with the protocol's argument failed.
4. The dynamic object produced a working method during ordinary attribute access.
5. Python 3.14's runtime protocol lookup did not treat the dynamic `__getattr__` result as a
   statically present member.
6. No result proves business behaviour such as delivery semantics.

### Visual interpretation

```text
                              member   signature   actual call
CompatibleSender               yes       yes          works
WrongSignatureSender           yes       no           TypeError
DynamicSender via __getattr__   dynamic   unmodelled   works

runtime Protocol on Python 3.14
        │
        └─ static member presence ──> compatible yes / wrong yes / dynamic no
```

#### How to read this visual

Read each row across before reading the final query line. The runtime protocol result follows only
its member-presence model, not the other columns.

#### Key insight

Recognition, typed compatibility, and successful invocation are distinct.

#### Simplification or limitation

The experiment uses ordinary classes and one method. Python 3.11 used older runtime protocol
lookup behaviour and may recognize the dynamic attribute. Descriptors and monkey patches can add
other cases.

### Design conclusion

Do not use `@runtime_checkable` to admit arbitrary plugins as “validated.” Use it only for a
shallow optional-capability branch, and still exercise the actual behavioural contract.

## Controlled experiment 2 — ABC direct inheritance versus virtual registration

### Precise question

When a class is registered as a virtual ABC subclass, does it gain the ABC in its MRO, inherit a
concrete ABC method, or receive abstract-member implementation enforcement?

### Classification

Python standard-library `abc` behaviour.

### Hypothesis

> A direct subclass will be recognized, include the ABC in its MRO, and inherit the concrete
> method. A registered class will be recognized but will not gain MRO membership or inherited
> behaviour. Registration will also accept an incomplete class because it is a declaration, not an
> implementation verifier.

### Controls and variables

- Controlled: one ABC, one abstract method, one concrete base method, fixed message.
- Changed: direct inheritance, compatible registration, and incomplete registration.
- Observed: `isinstance`, MRO, inherited member presence, actual calls.

### Reproduction command

```bash
.venv/bin/python units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice/abc_virtual_subclass_experiment.py
```

### Observed result

```text
nominal_isinstance=True
nominal_in_mro=True
nominal_default=sends-text
registered_isinstance=True
registered_in_mro=False
registered_has_default=False
registered_call=registered:5
incomplete_isinstance=True
incomplete_actual_call=AttributeError
```

### Interpretation

1. Direct inheritance supplied both recognition and normal method inheritance.
2. Registration made the compatible unrelated object recognizable.
3. The registered class's MRO did not change, and it did not gain the base concrete method.
4. Registration also made an incomplete class recognizable.
5. The missing operation failed only when called.
6. Registration therefore places a compatibility responsibility on the registering code.

### Visual interpretation

```text
DIRECT                                    VIRTUAL REGISTRATION

NominalSender                             RegisteredSender
      │ inherits                                │ registry says “recognized”
      ▼                                         ├─ MRO unchanged
SendsTextABC                                    ├─ no inherited default
      ├─ abstract guard                         └─ abstract operation not verified
      └─ concrete default
```

#### How to read this visual

The left arrow is inheritance and carries ordinary MRO consequences. The right relationship feeds
runtime subclass recognition only.

#### Key insight

ABC registration is recognition without inheritance or construction enforcement.

#### Simplification or limitation

The visual omits subclass hooks, cache invalidation tokens, metaclass conflicts, and static checker
treatment of registration.

### Design conclusion

Prefer a direct tested adapter when an external API needs translation or inherited defaults.
Reserve registration for authoritative, stable compatibility claims.

## Controlled experiment 3 — static structural acceptance and rejection

### Precise question

Will mypy accept an unrelated class with a compatible protocol method and reject an unrelated class
whose same-named method has an incompatible signature?

### Classification

Third-party static analyzer behaviour under the repository's locked mypy 1.20.2 environment,
guided by the Python typing specification.

### Hypothesis

> The compatible unrelated class will type-check without protocol inheritance. The wrong-signature
> class will produce an `arg-type` error at the protocol-typed client call.

### Environment

```text
mypy: 1.20.2 (compiled: no)
Configuration: --strict --no-incremental --no-error-summary --show-error-codes
Python executing mypy: CPython 3.14.7
Input files: generated isolated temporary sources
Network: none
```

### Controls and variables

- Controlled: protocol definition, client function, call site, checker flags.
- Changed: candidate method parameter and return signature.
- Observed: checker return code, error count, and stable error-code category.

### Reproduction command

```bash
.venv/bin/python units/foundations/SDP-FND-070-duck-typing-structural-typing-nominal-typing-protocols-abcs/practice/protocol_static_experiment.py
```

### Observed result

```text
compatible: returncode=0 errors=0 codes=-
wrong_signature: returncode=1 errors=1 codes=arg-type
```

### Interpretation

1. Inheritance was unnecessary for static structural compatibility.
2. The checker compared member signatures rather than only member names.
3. The wrong candidate failed where it was passed to the protocol-shaped client.
4. This is stronger evidence than a runtime protocol presence query for call shape.
5. It remains weaker than behavioural contract evidence.

### Visual interpretation

```text
UnrelatedButCompatible ── member types match ──> SendsText Protocol ── accepted
WrongSignature         ── member types differ ─> SendsText Protocol ── arg-type error

No candidate imports or inherits SendsText.
```

#### How to read this visual

The arrows represent the checker's assignability comparison, not runtime inheritance or call flow.

#### Key insight

Structural static checking can give early signature feedback without nominal coupling.

#### Simplification or limitation

This is one mypy version and strict configuration. `Any`, inaccurate stubs, ignores, overloads, or
other analyzers may change diagnostics. The experiment does not execute the candidate method.

### Design conclusion

Use a small `Protocol` when this form of early feedback is valuable to the client. Keep the normal
runtime call and behavioural test suite as separate evidence.

## Cross-experiment reconstruction

Without looking back, fill this table:

| Observation | Duck call | Static `Protocol` | Runtime `Protocol` | Direct ABC | Registered ABC |
|---|---|---|---|---|---|
| Requires explicit inheritance |  |  |  |  |  |
| Checks method signature |  |  |  |  |  |
| Actually invokes operation |  |  |  |  |  |
| Adds base to MRO |  |  |  |  |  |
| Supplies base methods |  |  |  |  |  |
| Blocks incomplete direct subclass construction |  |  |  |  |  |
| Proves behavioural meaning |  |  |  |  |  |

Then explain every cell that contains “sometimes” or needs a qualifier.

## Vary — production-design transfer

After the core refactor passes, choose one variation at a time:

1. Replace the method protocol with `Callable[[Alert], DeliveryReceipt]`; compare naming,
   discoverability, fakes, and future capability growth.
2. Add a resource-owning channel with `close()`. Keep delivery-only clients dependent on the
   smaller capability.
3. Add an async sender as a separate protocol and explain why a sync/async return union would
   complicate the client.
4. Make an explicit protocol subclass and observe MRO and abstractness differences.
5. Add a read-only `channel_code` property to the protocol, then compare it with a mutable
   attribute.
6. Build a controlled `__subclasshook__` and find one false-positive class.
7. Remove static annotations and argue whether tests give enough feedback in a small script.
8. Keep a framework-owned ABC only for first-party managed channels while the application client
   accepts a structural capability. Explain the two roles.
9. Add a provider timeout and ensure the adapter preserves its distinction from policy
   non-delivery.
10. Use a module object as an implementation and run the static checker.

For every variation, state the new force before changing the mechanism.

## Interview drill

Use these one at a time. Do not answer all at once.

1. “Your class has the right method but does not inherit my interface. Will Python accept it?”
2. “Why not put `@runtime_checkable` on every protocol?”
3. “What exactly does `ABC.register()` do?”
4. “Show a case where ABC is better than Protocol.”
5. “Show a case where a callable is better than both.”
6. “Mypy passes. What remains unproved?”

For each answer, identify the exact missing reasoning step before moving to the next question.

## Troubleshooting

- Run commands from the repository root so neighboring test imports resolve.
- Use the locked `.venv` commands when `uv` cannot write its user-level cache.
- If mypy rejects the partner after refactoring, inspect the exact protocol method parameter and
  return types before adding ignores.
- If runtime code still calls `isinstance(channel, AlertChannel)`, the nominal gate remains.
- If the pager is made to “match” by adding aliases directly to it, the adapter boundary has likely
  been skipped.
- If a broad `except Exception` returns a non-delivery receipt, provider defects are being hidden.
- If every fake inherits a large base, inspect whether the client protocol copied provider details.
- If `@runtime_checkable` becomes necessary only because the code wants to preflight every call,
  question the preflight requirement.
- If virtual registration seems to supply base behaviour, inspect the registered class MRO and run
  experiment 2 again.
- If the static negative experiment unexpectedly passes, check for `Any`, suppressed errors, and
  the checker command/version.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Preserved original attempt:
- Contract worksheet:
- Mechanism-selection worksheet:
- Static positive/negative evidence:
- Shared contract-test result:
- Pager adapter and failure evidence:
- Edge-case result:
- Rejected alternatives:
- Final ABC role:
- Callable comparison:
- Trade-offs:
- Remaining weakness:
- Delayed closed-book review date:
- Evidence link for `PROGRESS.md`:
