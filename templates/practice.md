<!--
Create as units/{{DOMAIN_SLUG}}/{{TOPIC_ID}}-{{TOPIC_SLUG}}/practice/README.md only when practice has real content.
Exercises begin unsolved. Do not populate all hints or final solutions.
-->

# Practice — {{TOPIC_ID}} {{TOPIC_TITLE}}

| Field | Value |
|---|---|
| Unit note | [{{TOPIC_ID}}](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#{{TOPIC_ANCHOR}}) |
| Evidence target | E / I / D / X / T |
| Attempt required before solution | Yes |
| Test command | `{{TEST_COMMAND}}` |
| Status | Not attempted / In progress / Reviewed / Closed |

## Learning question

{{ONE_QUESTION_THE_LAB_MUST_ANSWER}}

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

```text
practice/
├── README.md
├── {{STARTER_MODULE}}.py
└── test_{{STARTER_MODULE}}.py
```

## Problem

{{EXACT_TASK_WITHOUT_SOLUTION_LEAKAGE}}

## Change pressure

The starter design handles {{CURRENT_REQUIREMENT}}. Add {{NEW_REQUIREMENT}} without breaking {{STABLE_BEHAVIOUR}}.

## Expected observable behaviour

- {{BEHAVIOUR_1}}
- {{BEHAVIOUR_2}}

## Required edge cases

- {{EDGE_CASE_1}}
- {{EDGE_CASE_2}}

## Commands

```bash
python {{STARTER_MODULE}}.py
pytest -q
```

Record actual commands and output. Never claim a run that did not occur.

## Prediction before running

- Expected behaviour:
- Dependency or call flow:
- Likely failure:
- Reasoning:

## Rahul’s attempt

- Attempt file:
- Design explanation:
- Rejected alternative:
- Test result:

## Progressive hints

Do not add hints until requested.

### Hint 1

{{SMALLEST_CONCEPTUAL_NUDGE}}

### Hint 2

{{NARROW_THE_FIRST_WRONG_ASSUMPTION}}

### Hint 3

{{SUGGEST_A_RESPONSIBILITY_OR_COLLABORATION_NOT_THE_FULL_SOLUTION}}

## Review

### What is correct

- {{SPECIFIC_POINT}}

### First incorrect assumption or missing reasoning step

{{EXACT_STEP}}

### Smallest case that exposes it

{{SCENARIO_OR_TEST}}

### Next attempt

{{ONE_TARGETED_CHANGE_OR_QUESTION}}

## Observe and explain

After running, explain:

1. Which object or callable owned the decision?
2. Which dependency direction changed?
3. Which tests prove the stable contract?
4. Which abstraction is essential?
5. Which abstraction could still be removed?

## Refactor

{{REFACTORING_CHECKPOINT}}

## Vary

Add one requirement that tests whether the design is genuinely extensible rather than merely rearranged.

## Troubleshooting

- {{COMMON_TEST_OR_IMPORT_PROBLEM}}

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Optional comparison solution:
- Trade-offs:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
