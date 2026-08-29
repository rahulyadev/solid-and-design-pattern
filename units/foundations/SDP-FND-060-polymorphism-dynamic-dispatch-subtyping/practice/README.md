# Practice — SDP-FND-060 Polymorphism, dynamic dispatch, and subtyping

| Field | Value |
|---|---|
| Unit note | [SDP-FND-060](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-060) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Focused test command | `.venv/bin/pytest -q units/foundations/SDP-FND-060-polymorphism-dynamic-dispatch-subtyping/practice` |
| Status | Not attempted |

The deterministic starter and runtime experiments have been executed to verify the artifact. That
does not count as Rahul's attempt, contract explanation, refactoring evidence, or learning state.

## Learning question

How can one client collaborate with several runtime types through one stable operation, while
ensuring that every advertised subtype keeps the behaviour the client was promised?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

Do not begin with “replace the `isinstance` chain.” First write the client-visible contract. The
branching smell is easy to move; the harder design work is deciding which inputs, results, failures,
side effects, and invariants every replacement must preserve.

## Starter files

```text
practice/
├── README.md
├── polymorphism_delivery_lab.py
├── test_polymorphism_delivery_lab.py
├── receiver_dispatch_experiment.py
├── special_method_dispatch_experiment.py
└── test_polymorphism_runtime_experiments.py
```

- `polymorphism_delivery_lab.py` is the unsolved refactoring starter.
- `test_polymorphism_delivery_lab.py` characterizes current behaviour, including two deliberate
  design pains.
- The experiment scripts are completed observation tools, not the lab solution.
- `test_polymorphism_runtime_experiments.py` makes the experiment outputs reproducible.

## Problem

A checkout service asks several delivery options for quotes. The concrete classes already expose a
method with the same name, but `collect_quotes()` still identifies each supported concrete type.

The starter therefore has three distinct facts:

1. `StandardDelivery`, `PriorityDelivery`, and `PickupDelivery` are nominal subclasses of
   `DeliveryOption`.
2. Each object can respond to `quote(request)` when called directly.
3. The central client nevertheless supports only the two types named in its branch.

There is also a contract inconsistency. `DeliveryRequest` accepts `metro`, `regional`, and `remote`
as valid zones. `StandardDelivery` returns a quote for all three, while `PriorityDelivery` raises a
plain `ValueError` for two of them. Decide whether this is invalid input, normal business
unavailability, or an infrastructure failure. Then make the chosen meaning consistent.

## Current structures and call flow

```text
NOMINAL CLASS GRAPH                    CURRENT CLIENT CONTROL FLOW

        DeliveryOption                 collect_quotes(request, options)
          ▲     ▲     ▲                          │
          │     │     │                          ▼
   Standard  Priority  Pickup             inspect concrete type
      │         │        │                  ├─ Standard? ─→ option.quote()
      └─────────┴────────┘                  ├─ Priority? ─→ option.quote()
         each defines quote()              └─ anything else ─→ TypeError

Direct call:  PickupDelivery.quote(request) ─→ valid quote
Client call:  collect_quotes(... Pickup ...) ─→ TypeError
```

### How to read this visual

Read the left side as the declared class relationship. Read the right side as the actual client
algorithm. The inheritance arrows do not make the client polymorphic: the client still owns a
closed list of concrete types. The final two lines compare the same object used directly and
through the client.

### Key insight

Having sibling methods or a shared base is not enough. Behavioural polymorphism appears only when
the client sends one stable message without choosing the concrete implementation itself.

### Simplification or limitation

This is a conceptual class-and-call visual, not a literal Python lookup trace. It omits descriptor
binding, the MRO, result validation, exception propagation, and any static type checker.

## Current observable behaviour

Predict before running, then confirm:

1. Metro quotes for `StandardDelivery` and `PriorityDelivery` are returned in input order.
2. Standard delivery handles all three valid zones.
3. Priority delivery raises `ValueError` for a valid non-metro request.
4. Pickup produces a coherent quote when called directly.
5. `collect_quotes()` rejects that same pickup object because its concrete type is not named.
6. All three classes pass `issubclass(..., DeliveryOption)`.
7. The frozen request remains unchanged.
8. `DeliveryQuote` rejects impossible available/unavailable field combinations.

Items 1, 2, 4, 7, and 8 are stable observable behaviour for the first refactoring. Items 3 and 5
expose the two design questions; do not accidentally preserve them as desirable contracts.

## Change pressure

Refactor for these requirements:

1. `collect_quotes()` must collaborate through one stable operation and must not name concrete
   option classes.
2. Adding `PickupDelivery` or one later option must not require editing the collection algorithm.
3. Input order and one-result-per-option behaviour must remain visible.
4. Every delivery option must accept every valid `DeliveryRequest` value.
5. Normal business ineligibility must be represented as a coherent unavailable quote, not as an
   invalid-input or infrastructure exception.
6. Invalid request construction must still fail before dispatch.
7. An option must not mutate the request.
8. Available results must preserve non-negative fee and ETA invariants.
9. Unexpected implementation failures must not be mislabeled as ordinary unavailability.
10. A reusable contract test must run against every advertised option.

Do not add a factory, registry, plugin loader, `Protocol`, ABC, dependency-injection container, or
framework merely to complete the first refactoring. Those may be compared after the smallest
design works.

## Contract worksheet — complete before editing code

Write the client-visible rule for each row. Use concrete examples, not words such as “works” or
“compatible.”

| Contract dimension | Supertype/client promise | Allowed subtype variation | Breaking example |
|---|---|---|---|
| Accepted requests |  |  |  |
| Available result |  |  |  |
| Business unavailability |  |  |  |
| Invalid input |  |  |  |
| Infrastructure failure |  |  |  |
| Request mutation |  |  |  |
| Result ordering |  |  |  |
| External side effects |  |  |  |

Then answer:

- Which rules are enforced by the value objects?
- Which rules need shared behavioural tests?
- Which rules exist only in prose unless you add evidence?
- Does `issubclass()` prove any of them?
- Could a type checker prove the business meaning of `available=False`?
- Who should translate provider-specific failures, if a provider is added later?

## Required refactoring evidence

Your attempt is complete only when it includes all of the following:

1. Preserve the original starter through Git history or a clearly named attempt copy.
2. Record the contract worksheet before the refactor.
3. Draw the pre-refactor decision flow and post-refactor receiver call separately.
4. Remove the client's concrete-type decision without changing result ordering.
5. Make the pickup option work through the client without adding a pickup branch.
6. Represent priority's non-metro business rule consistently with the stated contract.
7. Run one shared contract test against every advertised option.
8. Include invalid request, available quote, unavailable quote, and unexpected-failure cases.
9. Explain what the runtime receiver controls and what the static annotation does not control.
10. State whether nominal inheritance is still necessary after the refactor.
11. Name one simpler closed-world design you would keep if new options were not expected.
12. Identify one abstraction you deliberately did not add.

Passing tests alone is insufficient. The design can pass example tests and still leave an
ambiguous failure contract or a subtype that rejects a valid client call.

## Required edge cases

- blank order ID;
- unknown zone;
- zero or negative weight;
- boundary weights of 999, 1,000, and 1,001 grams;
- fragile and non-fragile requests;
- every valid zone for every option;
- a coherent available quote with zero fee and zero ETA;
- a coherent unavailable quote;
- negative fee or ETA rejected by the result value;
- one deliberately faulty option whose unexpected exception remains distinguishable;
- empty option tuple;
- repeated use of the same immutable request;
- a new option added without editing the collector.

Do not introduce timing, randomness, network access, credentials, a real courier SDK, or mutable
global registration.

## Commands

From the repository root:

```bash
.venv/bin/python units/foundations/SDP-FND-060-polymorphism-dynamic-dispatch-subtyping/practice/polymorphism_delivery_lab.py
.venv/bin/pytest -q units/foundations/SDP-FND-060-polymorphism-dynamic-dispatch-subtyping/practice/test_polymorphism_delivery_lab.py
.venv/bin/python units/foundations/SDP-FND-060-polymorphism-dynamic-dispatch-subtyping/practice/receiver_dispatch_experiment.py
.venv/bin/python units/foundations/SDP-FND-060-polymorphism-dynamic-dispatch-subtyping/practice/special_method_dispatch_experiment.py
.venv/bin/pytest -q units/foundations/SDP-FND-060-polymorphism-dynamic-dispatch-subtyping/practice
```

Quality checks:

```bash
.venv/bin/ruff check units/foundations/SDP-FND-060-polymorphism-dynamic-dispatch-subtyping/practice
.venv/bin/mypy units/foundations/SDP-FND-060-polymorphism-dynamic-dispatch-subtyping/practice
```

The locked `uv run` equivalents are also valid when the user-level `uv` cache is writable.

## Verified starter baseline

The focused practice suite ran on 2026-08-29:

```text
...................                                                      [100%]
19 passed in 0.14s
```

The focused Ruff and mypy checks also ran:

```text
All checks passed!
Success: no issues found in 5 source files
```

The exact pytest duration can vary. These results prove only that the distributed starter and
experiments are runnable and reproducible. They do not prove the required refactoring or Rahul's
understanding.

## Prediction before running

Complete this before the first learner run:

- Result order for the two current metro options:
- Exact priority behaviour for a remote request:
- Direct pickup behaviour:
- Pickup behaviour through `collect_quotes()`:
- Runtime object that receives each `quote` call:
- Decision currently owned by the client:
- Meaning currently assigned to `ValueError`:
- Request state before and after quoting:
- Why `issubclass(PriorityDelivery, DeliveryOption)` is insufficient evidence:

## Rahul's attempt

- Attempt file or commit:
- Contract worksheet:
- Prediction:
- Before call flow:
- After call flow:
- Reusable contract tests:
- Edge-case results:
- Rejected alternative:
- Remaining nominal relationship:
- Focused test result:
- Design explanation:

## Progressive hints

Do not add or reveal hints until requested. Give one hint at a time and identify the first
incorrect assumption before suggesting code.

## Observe and explain

After the baseline and after each refactoring step, answer:

1. Which code chooses a concrete implementation before the refactor?
2. Which runtime value controls method resolution after the refactor?
3. What does the annotation communicate, and what does it execute?
4. Which valid input exposed the broken behavioural promise?
5. How is business unavailability different from invalid input?
6. Which result invariants are mechanically enforced?
7. Which client assumptions require a reusable behavioural test?
8. Can an unrelated class participate without nominal inheritance? If so, what new trade-off does
   that expose for `SDP-FND-070`?
9. Would a two-case `if` remain clearer if the set of cases were permanently closed?
10. Did the refactor remove a branch or merely move it into another central dispatcher?

## Refactor checkpoints

Work in small, attributable steps:

1. Run the characterization suite unchanged.
2. Write the client-visible contract in the worksheet.
3. Add a failing test for pickup through the collector.
4. Introduce only the smallest collaboration change needed for that test.
5. Re-run the stable behaviour tests.
6. Add a failing contract case for non-metro priority.
7. Align business-unavailability semantics without swallowing unexpected failures.
8. Extract a shared contract test and apply it to all advertised options.
9. Add one new option without editing the collector.
10. Remove names or abstractions that no longer earn their cost.

At each checkpoint, record whether behaviour, structure, or both changed.

## Controlled experiment 1 — receiver-based method dispatch

### Precise question

When a base-class method calls `self.discount(...)`, does Python choose the implementation written
beside that base method or the override found from the receiver's runtime type? How does an
explicit `PricePolicy.discount(policy, ...)` call differ?

### Classification

Python language mechanics: ordinary attribute lookup and method binding. This is not a CPython
bytecode or cache claim.

### Hypothesis

> The ordinary `self.discount(...)` lookup will find `LoyaltyPricePolicy.discount` because `self`
> is a `LoyaltyPricePolicy` instance. Naming `PricePolicy.discount` explicitly will bypass that
> receiver-based choice.

### Environment

```text
Date: 2026-08-29
Operating system: Linux
Architecture: x86_64
Python version: 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation: cpython
Dependencies: Python standard library only
Relevant flags: none
```

### Controls and variables

- Controlled: subtotal, object instance, trace format, process environment.
- Changed: ordinary receiver lookup versus an explicitly named base function.
- Observed: chosen function, result, receiver bound into the method, and trace.

### Reproduction command

```bash
.venv/bin/python units/foundations/SDP-FND-060-polymorphism-dynamic-dispatch-subtyping/practice/receiver_dispatch_experiment.py
```

### Observed result

```text
runtime_type=LoyaltyPricePolicy
dynamic_result=9000
dynamic_trace=PricePolicy.final_price -> LoyaltyPricePolicy.discount
bound_receiver=LoyaltyPricePolicy
bound_function=LoyaltyPricePolicy.discount
explicit_base_result=0
explicit_base_trace=PricePolicy.discount
```

### Interpretation

1. The receiver was a `LoyaltyPricePolicy` even though the variable was annotated as
   `PricePolicy`.
2. The base algorithm ran first, and its ordinary `self.discount` lookup reached the override.
3. The retrieved bound method carried both the selected function and its receiver.
4. An explicitly named base function call executed the base implementation and returned zero.
5. The observation does not prove every override preserves the price contract; it proves only
   which implementation was selected.

### Visual interpretation

```text
ordinary call
policy.final_price(10_000)
        │ receiver = LoyaltyPricePolicy instance
        ▼
PricePolicy.final_price
        │ self.discount(10_000)  ── runtime lookup ──┐
        ▼                                            ▼
   surrounding algorithm                 LoyaltyPricePolicy.discount

explicit base function
PricePolicy.discount(policy, 10_000) ── named directly ──> base function
```

#### How to read this visual

Follow the ordinary call down and then across at `self.discount`. The receiver stays the same while
the method name is resolved. The bottom line names a function through the base class, so it does
not perform the same receiver lookup for `discount`.

#### Key insight

Dynamic dispatch selects behaviour; it does not validate that the selected behaviour is safe.

#### Simplification or limitation

The diagram is a language-level call model. It omits descriptor precedence, frames, bytecode,
inline caches, and MRO details beyond the chosen override.

### Design conclusion

Use ordinary receiver calls when variation belongs to the collaborator. Avoid explicit base-class
function calls in client code because they couple the client to one implementation and can bypass
the intended override point. A deliberate base call inside carefully designed inheritance is a
different case.

## Controlled experiment 2 — implicit special-method lookup

### Precise question

If `__len__` is attached only to one instance, will `len(instance)` use it? How does that compare
with defining `__len__` on the instance's type?

### Classification

Python language mechanics: implicit special-method lookup.

### Hypothesis

> An explicit `instance.__len__()` access will find the instance attribute, but `len(instance)`
> will require the operation on the type. A subclass with class-level `__len__` will participate.

### Controls and variables

- Controlled: returned integers and lack of other class behaviour.
- Changed: instance-level callable versus type-level special method.
- Observed: explicit and implicit call outcomes.

### Reproduction command

```bash
.venv/bin/python units/foundations/SDP-FND-060-polymorphism-dynamic-dispatch-subtyping/practice/special_method_dispatch_experiment.py
```

### Observed result

```text
ordinary_explicit=5
implicit_instance_override=TypeError
implicit_type_method=7
explicit_type_method=7
```

### Interpretation

1. Ordinary dotted lookup found the callable attached to the individual object.
2. The implicit `len()` operation did not use that instance attribute.
3. Defining `__len__` on `SizedBatch` made its instances participate in the sized operation.
4. This is a documented special-method lookup rule, not evidence that all Python method dispatch
   bypasses instances.

### Visual interpretation

```text
explicit dotted lookup                   implicit language operation

batch.__len__()                          len(batch)
      │                                       │
      └─ instance attribute → 5               └─ type(Batch).__len__ missing → TypeError

len(SizedBatch())
      └─ type-level SizedBatch.__len__ → 7
```

#### How to read this visual

Compare the lookup entry points. The left begins with an explicit attribute access. The right is a
language operation with special lookup rules. The last line supplies the special method where that
implicit operation expects it.

#### Key insight

“Python dispatches dynamically” is true but incomplete; the operation determines the lookup path.

#### Simplification or limitation

The visual omits metaclasses and the full special-method lookup rationale. It does not claim a
particular CPython optimization or internal data structure.

### Design conclusion

For Python protocol participation, implement the documented special method on the class. Do not
assume that attaching a same-named callable to one instance makes built-in syntax recognize it.

## Vary — production-design transfer

After the core refactor passes, choose one variation at a time:

1. Add a `ScheduledDelivery` option that is unavailable on one date but does not reject a valid
   request.
2. Add a provider boundary that can raise a synthetic timeout. Keep timeout distinct from normal
   business unavailability.
3. Add a bulk client that accepts an empty tuple and preserves exact option order.
4. Remove nominal inheritance and record what runtime behaviour still works; leave the full
   typing choice for `SDP-FND-070`.
5. Replace the objects with plain quote callables and compare discoverability, state, testing, and
   naming.
6. Make the supported set permanently closed at two options and argue whether direct conditionals
   are now simpler.

For each variation, state the new force before changing the design.

## Troubleshooting

- Run commands from the repository root so the test module's neighboring import resolves.
- Use the locked `.venv` commands when `uv` cannot write its user-level cache.
- If a refactor makes a characterization test fail, decide whether it represented stable behaviour
  or a documented pain before changing the test.
- If every implementation failure becomes `available=False`, the code is probably hiding defects;
  separate business outcomes from unexpected failures.
- If a test knows each concrete class through a large conditional, the test may have copied the
  production dispatch problem.
- If mypy accepts a class, remember that static assignability is not proof of the full behavioural
  contract.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Contract worksheet:
- Shared contract-test result:
- Edge-case result:
- Rejected alternative:
- Trade-offs:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
