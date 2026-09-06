# Practice — SDP-PYT-100 least-powerful retention policy design

| Field | Value |
|---|---|
| Unit note | [SDP-PYT-100](../README.md) |
| Starter | [retention_policy_lab.py](retention_policy_lab.py) |
| Behavior tests | [test_retention_policy_lab.py](test_retention_policy_lab.py) |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-100-descriptors-class-hooks-metaclasses-when-justified/practice` |
| State | Unsolved |

## Scenario and change pressure

A backend chooses one of a small, application-owned set of data-retention policies. The current
design uses a frozen dataclass and two functions. It is explicit, typed, easy to test, and has no
definition-time side effect. Keep it if the problem remains this small.

Three possible changes arrive:

1. several mutable configuration objects may need the same assignment-time validation;
2. every subclass in an existing policy-handler hierarchy may need a validated `policy_code`; and
3. a framework proposal asks one metaclass to collect annotated declarations, reject duplicate
   names while the class body runs, and control instance construction.

Your task is to evaluate each change separately. Add only the mechanism whose unique power is
required. A correct solution may reject the descriptor, hook, decorator, or metaclass for one or
more variants. Preserve this starter as the original attempt, or copy it to a new attempt file
before refactoring.

## Predict before running

Record answers before executing anything:

1. Which current requirement cannot be handled by these functions and dataclass?
2. Would a property be enough if only one class owns `days`?
3. What exact repetition would earn a descriptor?
4. If a non-data descriptor and an instance dictionary both contain `days`, which wins?
5. At what moment would `__init_subclass__` validate a new handler?
6. Which class-definition keywords must each cooperative hook consume and forward?
7. Does an in-place class decorator preserve `is` identity?
8. Can a replacing class decorator change inheritance and tooling observations?
9. What power does `__prepare__` have that a post-creation hook does not?
10. Which proposed framework requirement is too vague to justify a metaclass?

No learner prediction has been recorded by the maintainer.

## Run the starter

From the repository root:

~~~bash
uv run --locked python units/pythonic/SDP-PYT-100-descriptors-class-hooks-metaclasses-when-justified/practice/retention_policy_lab.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-100-descriptors-class-hooks-metaclasses-when-justified/practice
~~~

Record the runtime, output, and test count. Maintainer validation is artifact evidence, not your
prediction, attempt, or explanation.

## Observe the existing design

Identify:

- the stable value object;
- the normalization and invariant boundary;
- why `bool` must be rejected even though it is an `int` subclass;
- why tuple input makes accidental registry mutation impossible here;
- the ambiguity policy for duplicate names; and
- the absence of any reason to intercept attribute lookup or class creation.

## Explain before refactoring

Explain the mechanisms as different answers to different questions:

| Mechanism | Question it can answer |
|---|---|
| Function | “How do I validate or transform this value now?” |
| Frozen dataclass | “How do I represent this small value?” |
| Property | “How does this one class manage this one attribute?” |
| Descriptor | “How do several attributes/classes share lookup, assignment, or deletion behavior?” |
| Ordinary decorator | “How do I wrap one function or callable?” |
| Class decorator | “How do I explicitly transform this completed class once?” |
| `__init_subclass__` | “What must every future subclass in this owned hierarchy satisfy?” |
| Metaclass | “Must I control namespace preparation or class/instance creation for a family of classes?” |

## Refactor in three bounded rounds

### Round A — managed values

Add a second mutable configuration owner only if the scenario you choose needs post-construction
assignment. Start with a property or helper. Introduce a descriptor only when at least two managed
attributes or owners genuinely share the same lookup/assignment/deletion policy.

If you add a descriptor:

- implement and test `__get__`, `__set__`, `__delete__`, and `__set_name__`;
- return the descriptor on class access;
- keep state in each owner instance, not on the shared descriptor;
- test data-descriptor precedence deliberately;
- do not perform network, database, logging-with-values, or async work in lookup; and
- keep errors tied to the public field without exposing sensitive values.

### Round B — subclass contract

Assume an existing handler hierarchy is already justified. Add `policy_code` validation using
`__init_subclass__` only if every future subclass must participate.

- consume only the hook's own keyword;
- forward all remaining keywords with `super()`;
- make a second cooperative base prove the chain;
- fail at definition time with the class and rule in the error;
- separate validation from registration; and
- keep registration explicit unless definition-time global mutation is truly required.

### Round C — framework proposal

Write a short decision record before coding. Compare a class decorator and a metaclass. Reject the
metaclass unless the accepted requirement needs one of these powers:

- a custom namespace before the class body executes;
- coordinated class-object creation across an inheritance family;
- metaclass-level special operations; or
- deliberate control of instance construction for all classes using it.

If the need is only post-creation validation, registration, or adding attributes, use a smaller
mechanism. If you do implement a metaclass, preserve the complete namespace passed to `type.__new__`
and test zero-argument `super()`.

## Required edge cases

- blank and whitespace-only names;
- lower and upper retention bounds;
- `bool`, float, and string values for days;
- two instances with independent managed values;
- class versus instance descriptor access;
- same-named instance entries against data and non-data descriptors;
- deletion before and after assignment;
- descriptor attachment after class creation;
- invalid and duplicate subclass metadata;
- two cooperative hooks in both useful base orders;
- an unconsumed class keyword reaching `object.__init_subclass__`;
- in-place decorator identity;
- replacement decorator identity and MRO;
- decorator order when two decorators are stacked;
- metaclass selection conflict;
- namespace duplicate detection if `__prepare__` is chosen;
- metaclass `__call__` before instance `__new__` and `__init__`; and
- zero-argument `super()` when a custom metaclass copies or filters the namespace.

## Rahul's attempt

- Attempt file: —
- Prediction: —
- Smallest mechanism chosen in each round: —
- Lookup precedence explanation: —
- Cooperative hook explanation: —
- Identity/tooling analysis: —
- Metaclass decision: —
- Runtime evidence: —
- Test result: —

## Progressive hints

No hints are released. Ask for one at a time after recording an attempt.

## Observe and explain after refactoring

1. Show where each managed value is stored.
2. Prove the descriptor object is shared but instance values are not.
3. Put a conflicting value directly in `__dict__` and explain the result.
4. Show the actual cooperative hook order; do not infer it from visual base order alone.
5. Explain why all custom class keywords eventually need a consumer.
6. Prove whether the decorated name refers to the original class.
7. List tools that could notice replacement: `isinstance`, pickling, `inspect`, typing, ORM mapping,
   or dependency injection.
8. If a metaclass remains, name the requirement no smaller mechanism meets.
9. Trigger one definition-time failure and show the import consequence.
10. Remove one mechanism and state what behavior is lost.

## Vary

Choose one change and walk the decision ladder again:

- policies become immutable input records loaded once at startup;
- only one class owns the managed attribute;
- independently installed providers supply policy implementations;
- a framework must preserve declaration order and reject duplicates during the class body;
- registration must be tenant-local rather than process-global;
- class metadata uses forward annotations under Python 3.11 and 3.14; or
- handler construction needs a request-scoped database dependency.

State whether the response is a function, dataclass, property, explicit map, descriptor,
`__init_subclass__`, class decorator, metaclass, factory, dependency injection, or rejection.

## Completion boundary

Passing the starter tests proves only preserved baseline behavior. Practice evidence additionally
requires the recorded prediction, an original attempt, new edge-case tests, runtime observations,
an explanation of the lookup and class-creation mechanics, and a justified rejection of at least
one advanced mechanism. Do not update `PROGRESS.md` until that evidence exists.
