# Detailed NotebookLM Workflow

[Quick handoff](../NOTEBOOKLM.md) · [Curriculum](../CURRICULUM.md) · [Learning paths](../LEARNING_PATHS.md) · [Progress](../PROGRESS.md)

NotebookLM is a review surface, not a second repository or source of truth.

## Approved inputs

Upload approved unit notes, relevant curriculum and path sections, approved project explanations, and the source policy when history or Python-version details matter.

Do not upload drafts, progress trackers, learner reviews, raw attempts, solutions, whole project source trees, generated test output, caches, profiler data, private information, or copied copyrighted material.

## Notebook grouping

Use coherent groups of roughly 5–12 units:

- Design foundations and SOLID
- Pythonic design mechanisms
- Creational patterns
- Structural patterns
- Behavioral interview-core patterns
- Behavioral advanced patterns
- Backend application patterns
- Architecture and boundaries
- Refactoring and anti-patterns
- Senior comparisons

Use one-unit notebooks for LSP, DIP, a difficult pattern, or an immediate interview topic when mixing sources reduces precision.

## Physical Notebook Core flashcards

```text
Create flashcards from the Physical Notebook Core sections. Test the change pressure, one-sentence model, visual, invariants, minimal Python example, misconception, trade-offs, and interview cues. Avoid definition-only trivia and cite the exact unit section.
```

## Comparison quiz

```text
Create scenario-based comparison questions from these approved units. Make me choose among the patterns, explain rejected alternatives, and identify when the simplest Python solution needs no named pattern. Ask one question at a time.
```

## Learning-path quiz

```text
Use only the approved notes linked by the selected learning path. Mix recall, diagram reconstruction, code review, refactoring, pattern choice, misuse, and changed-requirement questions. Do not reveal an answer before my attempt.
```

## Senior mock interview

```text
Run a senior Python design-pattern interview using these approved sources. Ask one question at a time. Progress from simple definition to forces, collaboration, implementation, alternatives, failure handling, and critique. Cite the source section when reviewing my answer.
```

## Returning weaknesses

Bring back the complete `SDP-...` ID, exact question, Rahul’s answer, NotebookLM’s correction, cited source section, and what remains unclear.

Use the existing dedicated unit chat:

```text
NotebookLM exposed this weakness in <TOPIC-ID>. Find the first missing reasoning step, test me with one focused question, and update REVIEW.md. Change the canonical note only if the clarification is generally useful.
```

NotebookLM does not create repository files, update states, prove test results, establish historical truth, or override primary sources.
