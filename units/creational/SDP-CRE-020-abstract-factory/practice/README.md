# Practice — SDP-CRE-020 coherent notification families

| Field | Value |
|---|---|
| Unit note | [SDP-CRE-020](../README.md) |
| Starter | [notification_family_lab.py](notification_family_lab.py) |
| Behavior tests | [test_notification_family_lab.py](test_notification_family_lab.py) |
| State | Unsolved |

## Scenario and change pressure

The baseline sends a synthetic operational notice through either an internal or partner channel.
Each choice currently selects two products: a renderer and a sender. The pairs use incompatible
content types, so mixing one product from each family must be impossible or detected before a
write.

A third `partner-v2` family is requested. It needs its own renderer, sender, and acknowledgement
decoder. Different deployments allow different families, and tests need isolated in-memory
families without patching globals.

Your task is to preserve `publish_notice`, identify the family invariant, and choose the smallest
boundary. Start by considering ordinary dependency injection of a ready bundle. Use an Abstract
Factory only if policy code must repeatedly create related products from the selected family.

Keep this starter as the original attempt or copy it before refactoring. Passing baseline tests is
not evidence that the target refactor is complete, and it never changes `PROGRESS.md` by itself.

## Predict before running

Record one answer at a time:

1. Which lines know the concrete family names?
2. What exact invariant relates renderer output to sender input?
3. At what earliest boundary can a mixed family be rejected?
4. Does one startup choice plus one publish call need repeatable factory operations?
5. Would injecting `(renderer, sender)` be enough? What makes that a bundle rather than a bag?
6. Who distinguishes malformed, unknown, and known-but-disallowed configuration?
7. Who owns and closes a sender created for one publish operation?
8. What must observations include, and what notice data must they omit?
9. Would Factory Method solve one product role or the whole compatibility family?
10. What test proves a third family does not change policy code?

No learner prediction has been recorded by the maintainer.

## Run

From the repository root:

~~~bash
uv run --locked python units/creational/SDP-CRE-020-abstract-factory/practice/notification_family_lab.py
uv run --locked pytest -q -p no:cacheprovider units/creational/SDP-CRE-020-abstract-factory/practice
~~~

Record the runtime, exact output, and test count before editing.

## Observe

Find these facts in the starter:

- validation happens before rendering;
- selection and concrete construction live inside `prepare_delivery`;
- `publish_notice` is otherwise a stable render-then-send workflow;
- each rendered value carries a content type;
- each sender defends its accepted content type;
- unknown selection happens before the external-write list changes; and
- `TARGET_REFACTOR_COMPLETE` is false even though the baseline works.

## Explain before refactoring

| Candidate | When it is enough | What it cannot guarantee by itself |
|---|---|---|
| Direct construction | One permanent family | Future family substitution |
| Small conditional | Two closed, local families | Separation from policy code |
| Ready bundle via DI | One selected set per workflow | Repeatable creation/lifetime policy |
| Tuple of callables | Tiny local code with clear naming | Semantic coherence unless validated |
| Abstract Factory | One choice must create several compatible roles repeatedly | Cross-process rollout or business correctness |
| Global registry | Almost never in policy code | Visible dependencies and test isolation |

## Refactor

1. Freeze the baseline behavior and no-write-on-selection-failure rule.
2. Name the product roles and their smallest behavior contracts.
3. Express one family identity or compatibility capability without relying only on class names.
4. Move configuration parsing, allow-listing, and concrete imports to a composition boundary.
5. First inject a coherent ready bundle; record whether this solves the actual pressure.
6. If repeatable creation remains real, define one family-factory contract with one creation
   operation per product role.
7. Add `partner-v2` without editing the stable publish workflow.
8. Detect a deliberately mixed renderer/sender before any output mutation.
9. Make new, cached, pooled, and borrowed lifetimes explicit; implement only the needed one.
10. Add safe observations and prove the body, destination, and credentials are absent.
11. Reject a global service locator and one speculative plugin mechanism in writing.
12. Set `TARGET_REFACTOR_COMPLETE = True` only when code, tests, and explanation agree.

## Required edge cases

- blank, non-ASCII, and separator-containing notice IDs;
- blank and Unicode notice bodies;
- exact internal and partner encodings;
- malformed, unknown, and known-but-disallowed family names;
- registry alias disagreeing with returned factory identity;
- a renderer from one family paired with another family’s sender;
- mismatch rejection before any write;
- constructor/acquisition failure after an earlier resource opens;
- sender failure followed by cleanup;
- independent per-call state when promised;
- frozen registry behavior under concurrent reads, or an explicit non-thread-safe contract;
- observer failure policy; and
- observation fields that omit notice bodies, destinations, tokens, and complete configuration.

## Rahul's attempt

- Original attempt file: —
- Prediction: —
- Named family invariant: —
- Smallest design tried first: —
- Why Abstract Factory is accepted or rejected: —
- Configuration/error boundary: —
- Lifetime owner: —
- Runtime observation: —
- Test result: —

## Progressive hints

No hints are released. Ask for one hint at a time after recording an attempt.

## Observe and explain after refactoring

1. Point to the stable policy function and prove it contains no concrete family name.
2. Show the single composition boundary that chooses a family.
3. Show how the chosen family relates every product role.
4. Inject a fake coherent family without patching a module global.
5. Construct a mixed family and prove failure occurs before a write.
6. Trigger use failure and show cleanup order.
7. Replace the Abstract Factory with a ready bundle and state exactly what capability disappears.
8. Remove one abstraction and explain whether clarity improves.

## Vary

Re-evaluate the smallest design when:

- only the internal family remains;
- one ready family is built once at startup;
- each job needs a fresh sender from one selected family;
- product roles expand every month but concrete families rarely change;
- concrete families expand often but product roles rarely change;
- independent packages provide families;
- one resource is async and request-scoped; or
- the third change is staged construction of one complex sender rather than a related family.

Name the best answer: direct construction, conditional, ready-object injection, bundle, simple
factory, Abstract Factory, dynamic registration, or Builder. Later curriculum units remain
recognition comparisons only.

## Completion boundary

Maintainer tests validate the starter artifact only. Practice evidence requires the saved
prediction, original attempt, added tests, actual runtime observations, a coherent-family
explanation, a lifetime/error-boundary decision, and a justified simpler-design comparison.
