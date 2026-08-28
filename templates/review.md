<!--
Create as units/{{DOMAIN_SLUG}}/{{TOPIC_ID}}-{{TOPIC_SLUG}}/REVIEW.md at the first formal review.
This stores learner-specific evidence, not duplicated canonical notes.
-->

# Review — {{TOPIC_ID}} {{TOPIC_TITLE}}

| Field | Value |
|---|---|
| Unit note | [{{TOPIC_ID}}](README.md) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Artifact state | Absent / Draft / Approved |
| Learning state | Not started / Learning / Practiced / Recalled / Demonstrated / Retained |
| Last evidence date | {{YYYY_MM_DD}} |
| Next review | {{YYYY_MM_DD_OR_NONE}} |
| Mastery badge | No / Yes with evidence |
| Strongest area | {{SPECIFIC_CAPABILITY}} |
| Weakest area | {{SPECIFIC_MISSING_REASONING_STEP}} |

## Evidence checklist

- [ ] Explains the change pressure and mental model.
- [ ] Reconstructs the essential visual.
- [ ] Identifies participants and dependency direction.
- [ ] Implements or refactors the required collaboration.
- [ ] Passes relevant tests and explains them.
- [ ] Handles important edge cases and failures.
- [ ] Chooses or rejects the design for a new scenario.
- [ ] Explains at least one rejected alternative.
- [ ] Distinguishes the pattern from commonly confused designs.
- [ ] Explains when not to use it.
- [ ] Separates design mechanics from Python or CPython mechanics.

## Review session — {{YYYY_MM_DD}}

| Field | Value |
|---|---|
| Closed book | Yes / No |
| Time since study | {{DURATION}} |
| Hints used | None / {{COUNT_AND_TYPE}} |
| Python baseline | {{VERSION}} |

### Blank-page reconstruction

- Problem or force:
- One-sentence model:
- Essential visual:
- Governing rules:
- Minimal Python form:
- Misuse:
- Trade-off:

### One-question-at-a-time record

#### Question 1

{{QUESTION}}

**Rahul’s answer summary**

{{FAITHFUL_SUMMARY}}

**What was correct**

- {{POINT}}

**Exact missing reasoning step**

- {{STEP}}

**Correction**

{{CONCISE_CORRECTION}}

### Practice and project evidence

| Evidence link | Result | What it proves | Remaining limitation |
|---|---|---|---|
| {{LINK}} | {{RESULT}} | {{EVIDENCE}} | {{LIMITATION}} |

### Demonstrated weaknesses

| Weakness | Evidence | Severity | Corrective action | Owning note section |
|---|---|---|---|---|
| {{PRECISE_WEAKNESS}} | {{QUESTION_OR_TEST}} | Critical / Important / Minor | {{ACTION}} | {{SECTION}} |

### Status evaluation

Recommended state: **{{STATE}}**

Reason:

{{EVIDENCE_BASED_REASON}}

Evidence link for `PROGRESS.md`:

{{VALID_RELATIVE_LINK}}

### Next review

- Date:
- Comparison scenario:
- Refactoring or implementation target:
- No-hint requirement:
