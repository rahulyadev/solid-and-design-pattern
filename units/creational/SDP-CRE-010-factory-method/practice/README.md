# Practice — SDP-CRE-010 incident export construction boundary

| Field | Value |
|---|---|
| Unit note | [SDP-CRE-010](../README.md) |
| Starter | [incident_export_lab.py](incident_export_lab.py) |
| Behavior tests | [test_incident_export_lab.py](test_incident_export_lab.py) |
| State | Unsolved |

## Scenario and change pressure

The working baseline exports a small incident report as text or deterministic JSON. The
conditional is honest and currently cheap. A third format, `compact`, is now requested by a team
that also needs to replace the exporter in tests and in a separate deployment.

Your task is to protect `publish_report` from the variable construction/selection decision using
the smallest justified seam. First use a factory function or injected callable. Add a class-based
Factory Method only if you can name a stable Creator hierarchy that already has meaningful
subclass-specific behavior beyond choosing an exporter.

Preserve the starter as the original attempt, or copy it to a new attempt file before refactoring.
Do not edit `PROGRESS.md` merely because tests pass.

## Predict before running

Record answers before executing code:

1. Which line currently selects variable behavior?
2. Does two fixed cases justify any abstraction yet?
3. When `compact` arrives, what must remain unchanged?
4. Should an exporter be a function, callable object, or class instance here? Why?
5. Who validates an unknown configuration name?
6. If the caller injects a ready exporter, is a factory still needed?
7. What requirement would make subclass override more useful than a callable?
8. Which error must happen before `output.append`?
9. Would an alternate constructor on `IncidentReport` solve this variation?
10. Who owns cleanup if your factory creates a resource-bearing exporter?

No learner prediction has been recorded by the maintainer.

## Run

From the repository root:

~~~bash
uv run --locked python units/creational/SDP-CRE-010-factory-method/practice/incident_export_lab.py
uv run --locked pytest -q -p no:cacheprovider units/creational/SDP-CRE-010-factory-method/practice
~~~

Record the runtime, exact output, and test count. Maintainer validation is artifact evidence, not
your prediction, attempt, or explanation.

## Observe

Identify:

- domain validation in `IncidentReport`;
- construction/selection mixed into `export_report`;
- stable publish behavior;
- deterministic JSON formatting;
- the no-write guarantee on selection failure; and
- why `TARGET_REFACTOR_COMPLETE` remains false despite passing starter tests.

## Explain before refactoring

Compare these candidate boundaries:

| Candidate | What changes | What remains explicit | Current verdict |
|---|---|---|---|
| Direct call | Nothing varies | Concrete exporter | Fine before the new pressure |
| Small conditional | One visible branch grows | All supported names | Still defensible for a closed set |
| Factory function | Selection and construction move together | One function call | Likely first refactor |
| Dictionary of callables | Application-owned names become data | Registry construction | Useful for several fixed choices |
| Injected callable | Caller chooses behavior | Dependency in signature | Best test seam if construction is external |
| Creator hierarchy | Subclasses override construction | Inheritance relationship | Must be earned, not assumed |

## Refactor

Work in small commits or saved attempts:

1. Freeze current behavior with the supplied tests.
2. Add the `compact` behavior without changing `publish_report`'s workflow contract.
3. Move name validation and selection to one explicit composition boundary.
4. Make unknown versus disallowed formats different public errors.
5. Inject a fake exporter or factory without patching module globals.
6. If construction needs a dependency, bind it at the composition root.
7. If construction opens a resource, guarantee cleanup on success and failure.
8. Reject or justify a Creator hierarchy in writing.
9. Set `TARGET_REFACTOR_COMPLETE = True` only after code, tests, and explanation agree.

## Required edge cases

- blank, non-ASCII, and valid incident IDs;
- zero counts, equal counts, negative counts, and resolved greater than opened;
- exact deterministic JSON output;
- unknown and known-but-disallowed format names;
- selection failure before any write;
- exporter failure before any write;
- writer failure after one attempted effect;
- two calls receiving independent stateful Products when that lifetime is promised;
- cleanup after success and failure for resource-bearing Products;
- registry mutation isolation between tests;
- deterministic handling of case and whitespace in configured names; and
- observation events that omit report content and credentials.

## Rahul's attempt

- Attempt file: —
- Prediction: —
- Smallest seam chosen: —
- Why a factory is or is not needed: —
- Why inheritance is accepted or rejected: —
- Error boundary: —
- Lifetime owner: —
- Runtime evidence: —
- Test result: —

## Progressive hints

No hints are released. Ask for one at a time after recording an attempt.

## Observe and explain after refactoring

1. Point to the single line where a Product is constructed.
2. Point to the stable workflow and prove it does not know concrete exporter names.
3. Show the error phase for malformed, unknown, disallowed, and execution failures.
4. Replace one factory with a fake without patching a global.
5. Explain whether the returned object is new per call, cached, pooled, or caller-owned.
6. Trigger a failure and prove cleanup order.
7. Show that logs or events omit report body and configuration secrets.
8. Remove one abstraction and state exactly what capability is lost.

## Vary

Re-evaluate the design for one change:

- only one exporter remains;
- the three exporters are fixed for the life of the application;
- separately installed packages provide exporters;
- construction needs a request-scoped database session;
- a coherent family of parser, validator, and exporter must vary together;
- export assembly becomes multi-stage and validated; or
- a preconfigured exporter should be copied for each job.

Name the smallest answer: direct construction, conditional, function, callable map, injected
dependency, Factory Method, dynamic registration, Abstract Factory, Builder, or Prototype. The
last four comparisons are recognition only; do not implement their future units here.

## Completion boundary

Passing the starter tests proves only preserved baseline behavior. Practice evidence additionally
requires the prediction, original attempt, added tests, actual observations, an explanation of the
chosen seam and lifetime, and a justified rejection of at least one more elaborate alternative.
