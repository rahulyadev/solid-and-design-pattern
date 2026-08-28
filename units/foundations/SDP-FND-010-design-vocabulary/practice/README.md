# Practice — SDP-FND-010 Design vocabulary

| Field | Value |
|---|---|
| Unit note | [SDP-FND-010](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-010) |
| Evidence target | D+T |
| Attempt required before solution | Yes |
| Test command | `uv run pytest -q units/foundations/SDP-FND-010-design-vocabulary/practice` |
| Status | Not attempted |

## Learning question

Can you classify a design claim from evidence about its problem, scope, portability, and control
flow—and reject a confident label when the evidence is insufficient?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

```text
practice/
├── README.md
├── classification_lab.py
└── test_classification_lab.py
```

## Problem

`classification_lab.py` labels design claims with keyword matching. Its output looks decisive, but
the classifier ignores context and can be fooled by wording. A word such as “system,” “Python,” or
“calls” is not proof of a design level.

Before changing code:

1. Run the script and predict which labels are accidental.
2. For each claim, write what evidence is present and what evidence is missing.
3. Decide whether the claim supports one label, several precise labels, or `unclassified`.

Then refactor the model and classifier so a decision can use explicit evidence rather than magic
words. Do not optimize for matching the starter output.

## Change pressure

The starter handles carefully phrased examples. Add a paraphrased claim containing a misleading
keyword without changing the meaning, and keep the classification defensible.

## Expected observable behaviour

- Every input claim appears exactly once in the report.
- The decision exposes enough reasoning to be reviewed; it is not merely a label.
- Insufficient or conflicting evidence remains visible instead of being guessed away.
- Rephrasing a claim without changing its evidence does not silently change its classification.

## Required edge cases

- A single claim legitimately describes more than one level.
- A claim contains a label-like keyword but provides no supporting evidence.
- Two claims use different wording for the same design evidence.
- An unknown or empty statement does not receive a confident label.

## Commands

```bash
uv run python units/foundations/SDP-FND-010-design-vocabulary/practice/classification_lab.py
uv run pytest -q units/foundations/SDP-FND-010-design-vocabulary/practice
```

Record actual commands and output. Starter checks prove only that the harness preserves claims and
renders every category; they do not prove semantic classification.

## Prediction before running

- Expected labels:
- Claims with insufficient evidence:
- Likely keyword failures:
- Reasoning:

## Rahul's attempt

- Attempt file:
- Design explanation:
- Rejected alternative:
- Test result:

## Progressive hints

Do not add hints until requested.

## Observe and explain

After running, explain:

1. Which labels came from evidence and which came only from vocabulary?
2. Which axis—kind, scope, portability, or control—resolved each ambiguity?
3. Why can one feature receive several labels without contradiction?
4. Which test protects meaning rather than implementation shape?
5. What information must remain unknown rather than guessed?

## Refactor

Replace keyword inference with the smallest explicit representation that makes the reasoning
reviewable. Preserve report completeness while allowing uncertainty and overlap.

## Vary: production transfer

Choose one feature from a real or synthetic backend. Describe it at every applicable level, then
defend one label you rejected. Use synthetic names and data; do not paste employer or customer
material.

## Troubleshooting

- Run commands from the repository root so the starter module import resolves consistently.
- If `uv` is unavailable, use `python classification_lab.py` for the script; install or activate the
  locked development environment before claiming pytest evidence.
- A passing starter suite is a harness check, not a completed attempt.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Trade-offs:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
