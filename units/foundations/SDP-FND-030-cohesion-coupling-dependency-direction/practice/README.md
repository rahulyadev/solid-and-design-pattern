# Practice — SDP-FND-030 Cohesion, coupling, and dependency direction

| Field | Value |
|---|---|
| Unit note | [SDP-FND-030](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-030) |
| Evidence target | D+T |
| Attempt required before solution | Yes |
| Test command | `uv run pytest -q units/foundations/SDP-FND-030-cohesion-coupling-dependency-direction/practice` |
| Status | Not attempted |

## Learning question

Can you separate delivery-selection policy from carrier-specific translation, point source
dependencies toward stable delivery meaning, and demonstrate that a carrier change has a smaller
blast radius?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

```text
practice/
├── README.md
├── acme_carrier.py
├── delivery_lab.py
└── test_delivery_lab.py
```

`acme_carrier.py` is a deterministic, synthetic carrier simulator. It is not copied from a real
SDK and performs no network requests.

## Problem

`delivery_lab.py` owns two different kinds of knowledge:

- stable application policy: a non-urgent parcel uses the cheapest quote; an urgent parcel accepts
  only quotes of at most two days; ties are deterministic;
- volatile carrier translation: Acme request types, kilograms, rate field names, and exceptions.

The starter works and its characterization tests pass. Its dependency shape is deliberately poor:

```text
test_delivery_lab.py ──imports──> delivery_lab.py ──imports──> acme_carrier.py
                                      │
                                      ├── delivery policy
                                      └── Acme translation
```

This visual is a source-dependency map. Read arrows from consumer to supplier. It omits runtime
calls and returned data. The key insight is that one policy module knows two independently changing
vocabularies.

Refactor in small behaviour-preserving steps. Preserve the public delivery meanings while making
carrier-specific knowledge stop at one boundary. A passed function or small object is enough; do
not create a framework, container, registry, or class hierarchy merely to add layers.

## Current change map

| Incoming change | Current edit location | Design question |
|---|---|---|
| Acme renames `charge_minor` | Carrier module and `delivery_lab.py` | Why does selection policy know a vendor field? |
| Acme changes kilograms to grams | `delivery_lab.py` | Who owns provider units? |
| Add ParcelJet with a different schema | New branch inside policy | Can translation vary while selection remains fixed? |
| Urgent threshold changes from two days to one | Mixed policy/translation function | Can policy change without provider knowledge? |
| Acme timeout class changes | `delivery_lab.py` | Where should infrastructure errors gain application meaning? |

## Expected observable behaviour

- `weight_grams` must be positive; invalid input fails before the carrier is called.
- Acme currently receives the weight converted to kilograms.
- A non-urgent parcel selects the lowest price.
- An urgent parcel considers only offers taking at most two days.
- Equal prices prefer fewer days, then the lexicographically smaller service name.
- An unknown zone becomes `DeliveryUnavailable`.
- A carrier timeout becomes `QuoteServiceUnavailable`.
- No eligible urgent quote becomes `DeliveryUnavailable`.
- A successful plan retains the order ID and normalized price, service, and day values.

These are characterization constraints, not a proposed final module structure.

## Required refactoring evidence

- A diagram of the source graph before and after, with arrow meaning stated.
- A one-sentence cohesive purpose for each resulting module or callable.
- A list of every Acme-specific name still visible to selection policy; the target is none.
- A client-owned normalized quote meaning that does not mirror either provider blindly.
- Passing policy tests that construct no `AcmeRate` values.
- Focused adapter tests for request, response, unit, and exception translation.
- One rejected abstraction and the concrete reason it would not reduce change cost.
- The completed change-impact experiment below.

Do not count files or interfaces as proof. Explain which knowledge moved and why the next named
change stops at a different boundary.

## Controlled change-impact experiment

This is a design-change observation, not a benchmark. Preserve the original starter and record
your attempt separately before changing it.

### Precise question

Does isolating Acme translation reduce the code and test locations that must understand an Acme
schema-and-unit change?

### Hypothesis

> Before refactoring, Acme field and unit changes reach selection policy and mixed tests. After a
> useful boundary, only the Acme adapter and its focused tests should understand those changes.

### Controlled change

Treat this as one provider release:

- `charge_minor` becomes a major-unit decimal string such as `"8.25"`;
- `mass_kilograms` becomes integer grams;
- delivery meaning remains price in integer cents.

Do not change urgency or tie-breaking policy in the same experiment.

### Observation protocol

1. Before refactoring, predict every source and test location affected by the release.
2. Search for Acme-specific symbols and record the matches.
3. Make the provider release in the preserved attempt and run the focused tests.
4. Record failures and the minimum edits needed to restore behaviour.
5. Restore the characterized baseline in your working attempt, then complete the boundary refactor.
6. Apply the same provider release behind the new boundary.
7. Run policy, adapter, and full practice tests separately.
8. Compare affected locations; explain any difference from the hypothesis.

### Evidence table

| Observation | Before refactor | After refactor | Why it changed or did not |
|---|---|---|---|
| Acme symbols referenced outside adapter |  |  |  |
| Source files edited |  |  |  |
| Test files edited |  |  |  |
| Policy tests failing from schema change |  |  |  |
| Meanings legitimately reviewed |  |  |  |

The goal is not a guaranteed count of one file. Composition and contract tests may legitimately be
reviewed. The result supports a design claim only when provider representation stops spreading
while shared delivery semantics remain explicit.

## Required edge cases

- Weight of zero and negative weight, with no carrier call.
- Unknown destination zone.
- Carrier timeout.
- Empty rate list.
- Urgent parcel with only slow offers.
- Equal price with different delivery days.
- Equal price and days with different service names.
- Exact conversion for a weight that is not a whole kilogram.

## Commands

```bash
uv run python units/foundations/SDP-FND-030-cohesion-coupling-dependency-direction/practice/delivery_lab.py
uv run pytest -q units/foundations/SDP-FND-030-cohesion-coupling-dependency-direction/practice
```

For code-quality checks after refactoring:

```bash
uv run ruff check units/foundations/SDP-FND-030-cohesion-coupling-dependency-direction/practice
uv run mypy \
  units/foundations/SDP-FND-030-cohesion-coupling-dependency-direction/practice/acme_carrier.py \
  units/foundations/SDP-FND-030-cohesion-coupling-dependency-direction/practice/delivery_lab.py
```

Record actual commands and output. Passing starter tests prove only that the characterization
harness works; they do not prove that the dependency shape is good.

## Prediction before running

- Selected standard service and reason:
- Selected urgent service and reason:
- Acme request weight for `1_250` grams:
- Source dependency arrows:
- First likely failure after the controlled provider release:
- Reasoning:

## Rahul's attempt

- Attempt path or commit:
- Before dependency map:
- After dependency map:
- Cohesive purpose of each boundary:
- Rejected abstraction:
- Test result:
- Change-impact evidence:

## Progressive hints

Do not add hints until requested. Reveal one hint at a time and preserve the original attempt.

## Observe and explain

After running and refactoring, explain:

1. Which starter elements are cohesive around selection policy?
2. Which elements are cohesive around Acme translation?
3. Which coupling remains necessary after the refactor?
4. How do source dependency and runtime call directions differ?
5. Why would returning an Acme-shaped dictionary through a callable still be tightly coupled?
6. Which changed files demonstrate reduced accidental blast radius?
7. Which shared semantic change would legitimately affect policy and every adapter?

## Refactor

Preserve `DeliveryPlan` behaviour while separating policy from the current provider. Keep concrete
wiring explicit at the edge. You may add focused modules and tests, but every new abstraction must
have a named responsibility and change pressure.

Do not modify or weaken characterization assertions merely to make the refactor pass. Move
provider-specific assertions into focused adapter tests when their boundary changes.

## Vary: production transfer

Add a synthetic `ParcelJet` provider with all of these differences:

- it accepts grams instead of kilograms;
- it returns price as a major-unit decimal string;
- it calls delivery time `business_days`;
- an unavailable zone is represented by an empty successful response;
- a transport failure uses a different exception class.

The existing selection policy must work with both providers without provider branches. Then answer:

- Which new code was additive?
- Which existing code changed?
- Where did provider choice enter the composition?
- Did the client-owned contract preserve important error distinctions?
- Would running both providers concurrently introduce new temporal or state coupling?

Use only synthetic data and a deterministic in-memory client.

## Troubleshooting

- Run commands from the repository root so sibling starter imports resolve consistently.
- If `uv` is unavailable, use Python 3.11 or newer for the script; do not claim pytest, Ruff, or
  mypy evidence until those tools actually run.
- A moved import is not enough if policy still knows provider fields, units, sentinels, or errors.
- `TYPE_CHECKING` or a string annotation can change import-time behaviour without repairing source
  ownership.
- Keep the provider simulator deterministic; this lab requires no internet or credentials.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Trade-offs:
- Controlled experiment result:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
