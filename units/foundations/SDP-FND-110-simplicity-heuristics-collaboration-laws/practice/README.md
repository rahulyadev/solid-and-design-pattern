# Practice — SDP-FND-110 Simplicity heuristics and collaboration laws

| Field | Value |
|---|---|
| Unit note | [SDP-FND-110](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-110) |
| Evidence target | E+D+T |
| Attempt required before solution | Yes |
| Test command | `uv run pytest -q units/foundations/SDP-FND-110-simplicity-heuristics-collaboration-laws/practice` |
| Status | Not attempted |

## Learning question

Can you preserve a correct order-summary contract, identify which apparent problems are genuine
change coupling, and add one real representation without replacing a small program with a
principle-driven framework?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

Do not change the starter until the prediction and diagnosis worksheets contain specific claims.
The lab is not solved by making the tests pass; they already pass. The evidence is the reasoning
behind what you change, what you leave alone, and what you deliberately remove or reject.

## Starter files

```text
practice/
├── README.md
├── order_summary_lab.py
└── test_order_summary_lab.py
```

`order_summary_lab.py` contains valid current behaviour and deliberate design tension:

- nested customer/account/contact/address data;
- order validation and money rounding;
- discount and shipping rules;
- a total calculation;
- a text representation;
- a support-routing label whose threshold currently matches a discount threshold;
- inheritance used between calculation and text rendering;
- a `representation` argument with one supported value.

`test_order_summary_lab.py` protects outputs and boundary cases without prescribing a class count,
function layout, interface, or design pattern.

## Problem

The current public operation builds a deterministic text summary:

```python
build_order_summary(order) -> str
```

It works, but pricing knowledge appears in more than one place, the renderer knows a deep object
path, and representation is connected to calculation through inheritance. Some repeated values
may be shared business knowledge; others may only coincide today.

A confirmed new requirement now exists:

> A nightly audit job needs a structured Python record for the same completed quote. Text output
> must remain byte-for-byte compatible, pricing must be calculated once per summary request, and
> no dynamic plug-in discovery is required.

Use ordinary Python 3.11-compatible mechanisms. The result may use functions, immutable values,
composition, methods, or a small combination. Do not assume that every heuristic demands its own
abstraction.

## Current collaboration visual

```text
build_order_summary
        │
        ▼
TextOrderSummary ──inherits implementation from──> OrderCalculator
        │
        ├─ walks Order → Customer → Account → Contact
        ├─ walks Order → Customer → Account → Address
        ├─ recalculates subtotal / discount / shipping / total
        └─ renders text

OrderCalculator
        └─ calculates subtotal / discount / shipping / total
```

### How to read this visual

An arrow means runtime construction or use; “inherits” is the source-level inheritance relation.
Indented lines name knowledge held by each participant. Read the repeated calculation list as a
claim to investigate, not as an instruction to extract every matching line.

### Key insight

The lab contains both true and merely apparent duplication. A successful refactoring distinguishes
knowledge that must change together from rules that only share today's number.

### Simplification or limitation

This is a conceptual ownership view, not a complete call trace or Python object layout. It omits
dataclass validation and formatting helpers. A nested immutable value path is not automatically a
Law of Demeter violation; explain which caller should or should not know it.

## Stable behaviour to preserve

- Order, customer, account, SKU, email, country, quantity, price, and loyalty inputs are validated.
- Money is represented with `Decimal`.
- Values are rounded to cents with `ROUND_HALF_UP`.
- Subtotal is the sum of every `quantity × unit_price`, then rounded to cents.
- Customers with at least 1,000 loyalty points receive a 10% subtotal discount.
- A GB order with a subtotal of at least 50.00 receives free shipping.
- Other GB orders pay 5.00 shipping.
- Non-GB orders pay 15.00 shipping.
- Shipping qualification uses subtotal before discount.
- Support is labelled `priority` at 1,000 loyalty points and `standard` below it.
- Text fields, order, and line ordering remain exactly stable.
- The current default representation is text.
- An unsupported representation raises `ValueError` until the new requirement is implemented.
- No current operation performs file, network, environment, clock, or global-state I/O.

Do not silently “improve” a business rule. If you believe one is inconsistent, preserve it and
record the product question separately.

## Change pressure

Add the audit record without breaking the stable text contract.

The record must contain these typed values:

| Field | Type | Meaning |
|---|---|---|
| `order_id` | `str` | Stable order identifier |
| `customer_id` | `str` | Stable customer identifier |
| `email` | `str` | Current notification address |
| `tier` | `str` | Current account tier |
| `country_code` | `str` | Billing country used by current shipping policy |
| `support_lane` | `str` | Current support routing result |
| `subtotal` | `Decimal` | Rounded subtotal |
| `discount` | `Decimal` | Rounded discount |
| `shipping` | `Decimal` | Shipping charge |
| `total` | `Decimal` | Rounded final total |

The record may be a frozen dataclass, a `TypedDict`, or another clearly defended ordinary Python
value. It is not JSON serialization and it does not need a schema registry.

## Constraints

1. Preserve the original attempt in Git history or a copied attempt file before substantial
   restructuring.
2. Keep `build_order_summary(order)` compatible for existing text callers.
3. Add a clear public operation for the audit requirement.
4. Calculate pricing once per public summary/audit request.
5. Keep one authoritative representation of each pricing rule.
6. Decide whether discount eligibility and support routing are the same knowledge or merely share
   today's threshold; record the business-owner reasoning.
7. Explain whether the nested paths expose collaborator structure or honest transparent data.
8. Remove, retain, or replace inheritance only after stating the claimed substitution contract.
9. Do not add third-party dependencies, framework types, network I/O, persistence, or async code.
10. Do not add an ABC, `Protocol`, factory, registry, service locator, dependency-injection
    container, rules DSL, event bus, or plug-in loader unless an actual client in this lab requires
    it and you defend its cost.
11. Do not test private helper names, exact class count, number of dots, or chosen pattern.
12. Remain compatible with Python 3.11 and strict mypy.

## Prediction before the first run

Fill this before running code:

- Expected test result:
- Expected sample output:
- Current public contract:
- First business rule likely to drift:
- Deepest knowledge path:
- Suspected true knowledge duplication:
- Suspected coincidental duplication:
- Suspected speculative mechanism:
- Claimed inheritance relationship:
- Smallest change you currently expect:
- One mechanism you expect to reject:

## First observation

Run from the repository root:

```bash
uv run python \
  units/foundations/SDP-FND-110-simplicity-heuristics-collaboration-laws/practice/order_summary_lab.py

uv run pytest -q \
  units/foundations/SDP-FND-110-simplicity-heuristics-collaboration-laws/practice
```

Record actual output:

- Python command:
- Exit status:
- Output:
- Pytest command:
- Tests collected:
- Result:
- Difference from prediction:

The expected starting point is a passing characterization suite. Record the observed result instead
of copying that expectation.

## Diagnosis worksheet

### Current knowledge map

| Knowledge or decision | Current locations | Same authority or coincidence? | Expected owner | Evidence |
|---|---|---|---|---|
| Subtotal calculation |  |  |  |  |
| Loyalty discount threshold |  |  |  |  |
| Loyalty discount formula |  |  |  |  |
| Support priority threshold |  |  |  |  |
| GB free-shipping threshold |  |  |  |  |
| Shipping fee schedule |  |  |  |  |
| Money rounding |  |  |  |  |
| Text layout |  |  |  |  |
| Customer/account structure |  |  |  |  |

### Heuristic claims

Each claim must name evidence and a guardrail.

| Heuristic | Concrete current pressure | Proposed smallest move | Overapplication risk |
|---|---|---|---|
| KISS |  |  |  |
| DRY |  |  |  |
| YAGNI |  |  |  |
| Separation of concerns |  |  |  |
| Tell Don't Ask |  |  |  |
| Law of Demeter |  |  |  |
| Favour composition |  |  |  |

### Collaboration inventory

- What can `Order` answer because it owns the facts?
- Which pricing decisions change independently of `Order` representation?
- Does a renderer legitimately query a completed value?
- Which path makes the renderer know account internals?
- What stable meaning could cross that boundary instead?
- Does `TextOrderSummary` satisfy an “is-an `OrderCalculator`” client contract?
- If inheritance is removed, is a supplied collaborator needed, or is one direct function enough?
- Where should one concrete representation be selected?

### Change-cost baseline

Do not use a numeric “design score.” Record concrete surfaces:

- Files that must change for a discount threshold:
- Functions/classes that encode the discount formula:
- Files that must change for a text-label change:
- Knowledge needed to add the audit record:
- Existing extension mechanisms used by more than one current client:
- Current public contracts at risk:
- Current failure states:

## Refactoring checkpoints

Complete one checkpoint at a time and run the focused tests after each behaviour-changing edit.

### Checkpoint 1 — Preserve the contract

- Keep the original tests.
- Add missing characterization only for behaviour you can observe.
- Do not assert private structure.
- Record the first local commit or preserved attempt path.

### Checkpoint 2 — Establish pricing authority

- Identify which subtotal, discount, shipping, and rounding knowledge is genuinely shared.
- Make one calculation produce a completed result.
- Prove text output still uses exactly the same values.
- Keep support-routing reasoning separate until its business ownership is decided.

### Checkpoint 3 — Reduce unnecessary knowledge

- Redraw the renderer's collaborator path.
- Replace only the structural knowledge it should not own.
- Keep queries that are honest for representation.
- Avoid a chain of forwarding getters with no stable meaning.

### Checkpoint 4 — Resolve inheritance honestly

- State the base contract a subtype would have to preserve.
- Search for a client that needs any `OrderCalculator` subtype.
- Keep inheritance if the substitutability claim is real.
- Otherwise choose the smallest direct or composed alternative.

### Checkpoint 5 — Add the audit record

- Add the real second representation from one completed calculation.
- Preserve typed money values rather than formatting them as text.
- Keep text and audit representation policies separate from pricing.
- Do not add arbitrary runtime discovery.

### Checkpoint 6 — Apply YAGNI and KISS

- List every new abstraction and its current client.
- Delete a layer, interface, registry, flag, or wrapper that has no earned responsibility.
- Record the concrete evidence that would justify restoring it later.

### Checkpoint 7 — Vary the business rule

Change the confirmed free-shipping threshold from 50.00 to 75.00.

- Predict exactly which source and test locations should change.
- Make the change.
- Confirm both representations remain consistent.
- Explain whether the actual edit surface supports your DRY claim.
- Restore 50.00 after recording the observation unless the exercise is intentionally preserved on
  a separate commit.

## Required edge cases

- Exactly 999 and exactly 1,000 loyalty points.
- Exactly 49.99 and exactly 50.00 GB subtotal.
- Non-GB order above the GB free-shipping threshold.
- Zero-priced line.
- One line and several lines.
- Fractional input that exercises the rounding rule.
- Blank order, customer, account, SKU, and email data.
- Invalid lowercase or non-two-letter country code.
- Zero and negative quantity.
- Negative price and loyalty points.
- Text default through the existing public call.
- Explicit text selection if retained.
- Audit values remain `Decimal`, not formatted strings.
- Unsupported representation or operation has a deliberate error contract.
- The support threshold can diverge from discount eligibility without accidental coupling.

Do not add tax, currency conversion, persistence, delivery, dynamic providers, user-defined rules,
or framework request objects. They are unrelated forces for this lab.

## Required tests

Add behaviour tests that prove:

1. the old text output is unchanged;
2. pricing is calculated once per public request without asserting a private helper;
3. the audit record carries the required typed values;
4. text and audit outputs agree on one completed calculation;
5. support routing and discount policy can change independently if you classified them as separate
   knowledge;
6. validation and rounding remain stable;
7. unsupported selection fails explicitly;
8. the changed free-shipping threshold has one authoritative source.

For “calculated once,” prefer an observable supplied policy or a public calculation result over
patching private functions. If your simplest design has no meaningful seam and pure calculation is
cheap, explain why the requirement itself should instead be clarified; do not create a mock-only
interface.

## Observe and explain

After refactoring, answer:

1. Which current pain made each structural change necessary?
2. Which repeated lines were one piece of knowledge?
3. Which identical threshold was or was not coincidental?
4. Which owner now decides pricing?
5. Which queries remain, and why are they legitimate?
6. Which collaborator structure is no longer exposed?
7. What happened to the inheritance relationship?
8. Where is composition used, if anywhere, and what varies?
9. Which speculative mechanism was removed or rejected?
10. Which next real change is now local?
11. Which new names and failure states did the refactoring add?
12. What would make you simplify the design again?

## Before/after visual

Draw your actual result; do not copy the unit's generic quote visual.

```text
Before:
caller ──> ... ──> ... ──> decision / representation

After:
caller ──> [your actual stable meaning] ──> [your actual collaborator]
```

### How to read this visual

State whether arrows mean calls, source dependencies, data flow, or ownership. Name where concrete
selection occurs.

### Key insight

Write one conclusion about reduced knowledge or change surface, not “the code is cleaner.”

### Simplification or limitation

State what the diagram omits and whether the structure would still be justified with only one
representation.

## Production transfer

A production API now stores the audit record for seven years and may rerender text after pricing
rules have changed.

Write a design response covering:

- whether the stored record is an immutable pricing snapshot or a recalculation input;
- rule or schema versioning;
- authoritative money and currency representation;
- access control for email and other personal data;
- migration and backward compatibility;
- idempotent writes and duplicate requests;
- correlation identifiers and audit provenance;
- retry behaviour if storage succeeds but response rendering fails;
- which concerns stay in process;
- which future capability you still refuse to build.

Do not implement storage. The evidence target is a production-design transfer that preserves the
unit's simplicity judgment under data-lifetime and compatibility pressure.

## Design defence

Prepare a five-minute explanation:

1. **Pressure:** the real audit requirement and current change coupling.
2. **Diagnosis:** one true duplication, one coincidental similarity, and one knowledge leak.
3. **Move:** the smallest behaviour-preserving design change.
4. **Tension:** one pair of heuristics that disagreed.
5. **Rejection:** one interface, registry, hierarchy, or feature you did not add.
6. **Evidence:** tests and the temporary threshold change.
7. **Trade-off:** one cost the new design introduces.
8. **Revisit trigger:** evidence that would justify a larger mechanism.

## Rahul's attempt

- Prediction:
- Diagnosis worksheet:
- Preserved attempt path or commit:
- Refactoring sequence:
- Actual test output:
- Before/after visual:
- Rejected alternative:
- Production transfer:
- Remaining doubt:

## Progressive hints

No hints are included in the initialized lab. Ask for one hint at a time after preserving the first
attempt.

## Commands

Run from the repository root through the locked environment.

```bash
uv run python \
  units/foundations/SDP-FND-110-simplicity-heuristics-collaboration-laws/practice/order_summary_lab.py

uv run pytest -q \
  units/foundations/SDP-FND-110-simplicity-heuristics-collaboration-laws/practice

uv run ruff check \
  units/foundations/SDP-FND-110-simplicity-heuristics-collaboration-laws/practice

uv run mypy \
  units/foundations/SDP-FND-110-simplicity-heuristics-collaboration-laws/practice

python scripts/validate_repo.py
```

Record actual commands and output. Never describe an expected failure or passing check as observed
until the command has run.

## Maintainer artifact verification — 2026-08-30

This verifies the initialized starter, not Rahul's learning state or a completed learner attempt.

Environment:

```text
Linux 7.0.0-30-generic x86_64
Python 3.14.7
```

Observed runner result:

```text
order=order-7
customer=customer-3
email=rahul@example.test
tier=PLUS
country=GB
support=priority
subtotal=60.00
discount=6.00
shipping=0.00
total=54.00
```

Observed checks:

```text
pytest: 20 passed
all practice suites: 147 tests passed across 11 isolated directory runs
Ruff: all unit files passed
mypy: all 11 practice directories passed; this unit has 2 checked source files
repository validator: PASSED on a clean content copy; all automated categories passed
```

The repository-wide practice suites were invoked per directory because older units contain repeated
test module basenames that collide during one-shot pytest and mypy discovery. Isolated runs test
the same files without altering those pre-existing units.

The clean content copy excluded pre-existing ignored local environments and tool caches, so the
repository-hygiene result represents the files eligible for commit. The original working copy's
ignored `.venv`, `.pytest_cache`, `.ruff_cache`, `.mypy_cache`, and `__pycache__` directories were
not modified or staged.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Optional comparison solution:
- Trade-offs:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
