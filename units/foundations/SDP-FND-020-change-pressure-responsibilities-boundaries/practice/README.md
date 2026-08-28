# Practice — SDP-FND-020 Change pressure, responsibilities, and boundaries

| Field | Value |
|---|---|
| Unit note | [SDP-FND-020](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-020) |
| Evidence target | D+T |
| Attempt required before solution | Yes |
| Test command | `uv run pytest -q units/foundations/SDP-FND-020-change-pressure-responsibilities-boundaries/practice` |
| Status | Not attempted |

## Learning question

Can you trace concrete change pressures through a checkout workflow, assign each responsibility to
a defensible owner with GRASP lenses, and keep the observable behaviour while refactoring?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

```text
practice/
├── README.md
├── responsibility_lab.py
└── test_responsibility_lab.py
```

## Problem

`responsibility_lab.py` contains one working `place_order` function. It calculates subtotals and
discounts, chooses a payment mechanism, builds a persistence record, and creates a receipt. Its
tests pass, but several independently changing decisions live in one owner.

Before changing code:

1. Run the script and predict the observable record, payment, and receipt.
2. Mark every line as knowing, deciding, coordinating, creating, or performing.
3. Write the change pressure behind each responsibility.
4. Compare at least two possible owners using named GRASP lenses.
5. Circle the smallest boundary that would contain each proven variation.

Then refactor in small behaviour-preserving steps. Functions and callables are enough; do not add a
class merely to satisfy a GRASP name.

## Current change map

| Incoming change | Current edit location | Design question |
|---|---|---|
| Loyalty discount changes | `place_order` | Is pricing part of coordination? |
| Wallet payment arrives | `place_order` | Which provider decision should the client see? |
| Receipt is resent later | `place_order` | Can notification happen without charging again? |
| Persistence representation changes | `place_order` | Why does checkout construct database-shaped data? |

## Expected observable behaviour

- A line subtotal is `unit_price * quantity` and an order subtotal is the sum of its lines.
- Customers whose ID starts with `LOYAL-` receive a ten-percent integer discount.
- `card` and `bank_transfer` produce their existing payment-reference formats.
- A successful call records one payment, one order, and one receipt.
- An unsupported payment method raises before any observable effect is recorded.
- The returned mapping remains equal to the stored order record during the refactoring.

These are characterization constraints, not a proposed final architecture.

## Required refactoring evidence

- A written pressure → responsibility → owner → boundary map.
- At least one decision that remains in the direct function, with a reason.
- At least one extracted responsibility justified by two GRASP lenses.
- Passing characterization tests after each small movement.
- One rejected class, interface, or service that would add no useful boundary.
- An explanation of the partial-failure risk between payment and persistence.

## Required edge cases

- An empty order.
- More than one line with quantities greater than one.
- A loyalty subtotal that does not divide evenly by ten.
- An unsupported payment method with zero recorded effects.
- Two payment mechanisms that preserve the same client-facing charge meaning.

## Commands

```bash
uv run python units/foundations/SDP-FND-020-change-pressure-responsibilities-boundaries/practice/responsibility_lab.py
uv run pytest -q units/foundations/SDP-FND-020-change-pressure-responsibilities-boundaries/practice
```

Record actual commands and output. Passing starter tests prove only that the characterization
harness works; they do not prove that responsibilities have been assigned well.

## Prediction before running

- Expected total:
- Expected payment reference:
- Expected effect order:
- First likely change collision:
- Reasoning:

## Rahul's attempt

- Attempt file:
- Responsibility map:
- GRASP lenses used:
- Boundary added:
- Rejected abstraction:
- Test result:

## Progressive hints

Do not add hints until requested.

## Observe and explain

After running, explain:

1. Which responsibility is pure calculation and which responsibilities are effects?
2. Why is the orchestrating function a Controller but not the Information Expert for every rule?
3. Where do Information Expert and High Cohesion point to different candidate owners?
4. Which boundary is Protected Variations, and what concrete variation does it protect?
5. Which technical owner is a Pure Fabrication?
6. What can fail after payment succeeds, and why does extraction not make the workflow atomic?

## Refactor

Preserve the public `place_order` behaviour while making the smallest useful responsibility moves.
You may change its internal collaborators and tests, but keep external effects explicit. Prefer
plain functions or callables unless state or lifecycle gives an object a real job.

## Vary: production transfer

Add a `wallet` payment mechanism and a destination-based tax rule. The point is not merely to make
the tests pass: show which files or owners change, which remain stable, and which abstraction you
still refuse to add. Use synthetic data only.

## Troubleshooting

- Run commands from the repository root so the starter import resolves consistently.
- If `uv` is unavailable, run the script with Python 3.11 or newer; install or activate the locked
  development environment before claiming pytest, Ruff, or mypy evidence.
- Do not weaken the characterization tests to make a refactoring appear behaviour-preserving.
- A boundary around payment does not by itself provide idempotency or distributed atomicity.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Trade-offs:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
