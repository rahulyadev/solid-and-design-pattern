<!--
Create only when runtime observation materially explains the design.
Never invent output. Design-level collaboration alone does not require an experiment.
-->

# {{EXPERIMENT_ID}} — {{EXPERIMENT_TITLE}}

| Field | Value |
|---|---|
| Owning unit | [{{TOPIC_ID}}](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#{{TOPIC_ANCHOR}}) |
| Precise question | {{QUESTION}} |
| Classification | Python language / Standard library / CPython / Framework / Platform |
| Status | Planned / Run / Interpreted / Reproduced |

## Why observation is necessary

{{HIDDEN_RUNTIME_BEHAVIOUR}}

## Hypothesis

> {{PREDICTION_AND_REASON}}

## Environment

```text
Date:
Operating system:
Architecture:
Python version:
sys.version:
sys.implementation:
Dependencies:
Relevant flags:
```

## Controls and variables

- Controlled:
- Changed:
- Measured:

## Reproduction command

```bash
{{COMMAND}}
```

## Predicted result

```text
{{PREDICTION}}
```

## Observed result

Add only after execution.

```text
{{ACTUAL_OUTPUT}}
```

## Interpretation

1. What the result directly shows.
2. What can reasonably be inferred.
3. What cannot be inferred.

## Visual interpretation

```text
{{TIMELINE_OBJECT_LIFETIME_OR_DISPATCH_VISUAL}}
```

### How to read this visual

{{GUIDE}}

### Key insight

{{INSIGHT}}

### Simplification or limitation

{{LIMITATION}}

## Design conclusion

Explain whether the observation changes the recommended design or only deepens the Python mechanism.

## Limitations

- {{LIMITATION}}

## Sources

1. {{AUTHORITATIVE_SOURCE}}
