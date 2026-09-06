# Validation — SDP-PYT-100

## Scope and evidence boundary

| Field | Observed value |
|---|---|
| Date | 2026-09-06 |
| Exact branch | `topic/SDP-PYT-100` |
| Initialization baseline (`INIT_START`) | `da3b7f47517e5e263d3dcae243b12f4f61a5148f` |
| Initialization commit | `6e208387fcdc19bc8a16949a48d94a76d1530517` |
| Evidence profile | `E+I+D+X+T` |
| Canonical runtime | CPython 3.14.7 |
| Compatibility runtime | CPython 3.11.16 |
| Artifact state during this record | Approved |
| Learning state during this record | Not started |

This record validates maintainer-authored curriculum material. It contains no learner prediction,
attempt, explanation, delayed recall, transfer, refactoring submission, or interview answer.
Therefore only artifact state advances from Absent through Draft to Approved. Rahul's learning
state remains Not started, and every learner-evidence field in `PROGRESS.md` remains `—`.

## Sources actually read

- Python 3.14.7 Descriptor Guide for the protocol, data/non-data classification, instance/class/
  `super` invocation, lookup precedence, name notification, `__getattribute__` boundary,
  properties, function binding, static methods, class methods, and slot descriptors.
- Python 3.14.7 data model for `__init_subclass__` keyword forwarding, `__set_name__` timing,
  metaclass selection, namespace preparation, class-body execution, class-object creation,
  `__classcell__` labeling, decorator timing, call dispatch, and instance `__new__`/`__init__`.
- Python 3.14.7 class-definition reference for suite execution, decorator equivalence and bottom-up
  application, final name binding, declaration order, and type-parameter version history.
- Python 3.14.7 `annotationlib` documentation for lazy-annotation formats, post-creation
  `get_annotations`, and the pre-creation namespace helper.
- Python 3.11 data model for the compatibility-floor descriptor and class-creation contracts.
- PEP 487 for the rationale and contract of `__init_subclass__` and `__set_name__`, including
  simpler inheritance and reduced metaclass-conflict pressure.
- PEP 3115 for metaclass keyword syntax and the pre-class-body `__prepare__` hook.
- PEP 3135 for the implicit `__class__` closure cell used by zero-argument `super()`.

Subtle claims cite these sources near their mechanics. `__classcell__` is called a CPython
implementation detail, while design advice, framework risk, and production choices are labeled as
professional inference rather than interpreter guarantees. No copied book prose, external diagram,
framework source, real customer model, private data, production log, credential, or proprietary
schema was used.

## Executed checks

| Check | Observed result |
|---|---|
| Focused unit tests, CPython 3.14.7 | 60 passed across worked examples, three experiments, visual contracts, and unsolved-practice behavior. |
| Focused unit tests, CPython 3.11.16 | The same 60 tests passed. |
| Repository regression, CPython 3.14.7 | 838 tests passed across all 55 discovered test directories, using a separate pytest process per directory. |
| Ruff lint | Passed for the complete SDP-PYT-100 unit tree with cache disabled. |
| Ruff formatting | Every format-eligible unit file is formatted. |
| Strict mypy, Python 3.14 target | No issues in all 9 non-test Python source files. |
| Strict mypy, Python 3.11 target | No issues in the same 9 source files. |
| Controlled negative mypy case | Both targets rejected assigning `str` to the descriptor-managed `int` port with `[assignment]`. |
| README Python snippets | All 19 fenced Python snippets compiled on CPython 3.14.7 and CPython 3.11.16. |
| Worked demo | Both runtimes emitted the endpoint, health check, cooperative rule quote, and explicit metaclass-rejection decision. |
| Descriptor experiment | Both runtimes produced the same ten observations for data/non-data precedence, class access, method binding, assignment, and deletion. |
| Class-creation experiment | Both runtimes produced the same definition and instance phase trace. |
| Annotation-timing experiment | CPython 3.11.16 failed during class definition; CPython 3.14.7 completed definition and failed during value-form annotation evaluation, as recorded. |
| Practice starter | Both runtimes selected the synthetic standard policy with 30 days; target mechanism-selection work remains unsolved. |
| Embedded visual model | Tests matched every field in all eight embedded scenarios to maintained Python data and covered functions/dataclasses, property, descriptor, explicit map, subclass hook, class decorator, metaclass, and rejection. |
| HTML script syntax | The executable JavaScript block compiled with Node.js 24.19.0. |
| Static visual structure | Required accessible DOM targets, live region, balanced CSS braces, and responsive media rules were present. |
| Interactive browser rendering | Not performed: the in-app browser blocked the local `file:` URL under its URL security policy. No workaround, indirect navigation, alternate browser, or policy bypass was attempted. |
| Repository validator | All structure, metadata, Markdown, links, evidence, version, lock-file, source-policy, and hygiene checks passed with zero forbidden-path violations. |
| Git diff checks | Staged and unstaged whitespace/error checks passed; only SDP-PYT-100 and its matching progress row changed. |

The dual-runtime environments, mypy state, Hypothesis storage, controlled negative case, and uv
cache lived under `/tmp`. Python bytecode generation was disabled during final checks. No virtual
environment, bytecode, pytest/Ruff/mypy/Hypothesis cache, temporary typing input, or generated
validation output is committed.

The browser-policy limitation narrows visual evidence honestly: the artifact has maintained-data
parity, JavaScript syntax, DOM-target, CSS-balance, and responsive-source checks, but no claimed
rendered desktop/mobile or accessibility observation. The self-contained visual has no network
dependency.

## Manual content and boundary review

- Began with explicit-call change pressure and a least-powerful-mechanism ladder before protocol or
  metaclass mechanics.
- Compared functions, dataclasses, properties, ordinary decorators, explicit dictionaries/
  factories, descriptors, `__init_subclass__`, class decorators, and metaclasses.
- Explained `__get__`, `__set__`, `__delete__`, and `__set_name__`, including owner versus
  instance access and late-attachment behavior.
- Kept data-descriptor, instance dictionary, non-data descriptor, class value, and `__getattr__`
  lookup precedence explicit and runtime-tested.
- Connected function non-data descriptors to `__self__`/`__func__` method binding and instance
  method shadowing.
- Stored per-instance values on owners rather than the shared descriptor, tested inheritance and
  failed-write atomicity, and kept I/O out of attribute access.
- Treated `__init_subclass__` as a post-creation family rule, consumed and forwarded keywords,
  tested both cooperative base orders, and allowed leftover keywords to fail at
  `object.__init_subclass__`.
- Separated definition validation from application activation and explained import, reload,
  duplicate, worker, test-isolation, and global-state hazards.
- Distinguished in-place class decoration from replacement/wrapping and covered identity,
  metadata, MRO, inheritance, typing, inspection, serialization, and framework tooling.
- Tested bottom-up decorator application and proved a class decorator is not automatically re-run
  for descendants.
- Kept class objects, instances, and metaclass objects distinct; separated metaclass
  `__prepare__`, `__new__`, `__init__`, and `__call__` roles.
- Explained metaclass selection and conflicts using the subtype-of-all-candidates rule rather than
  a vague multiple-inheritance warning.
- Presented `__prepare__` only for real pre-body namespace behavior and noted that ordinary
  dictionaries already preserve declaration order.
- Propagated the complete namespace to `type.__new__`; the destructive `__classcell__` example is
  isolated in a CPython-gated negative test.
- Verified the material Python 3.14 lazy-annotation difference against current official docs and
  with identical no-future-flag source on Python 3.11 and 3.14.
- Kept all runnable unit code Python 3.11 compatible while explaining current Python 3.14
  annotation introspection.
- Covered definition-time failures, detection, containment, recovery, observability, safe event
  fields, concurrency/state boundaries, and performance/memory questions without invented
  benchmarks.
- Used one justified typed descriptor, one bounded cooperative subclass contract, explicit
  application activation, and a diagnostic metaclass that the worked backend explicitly rejects.
- Kept practice runnable but unsolved with predict → run → observe → explain → refactor → vary,
  progressive hints unreleased, original-attempt fields empty, and no false learning evidence.
- Included interview prompts with exact missing reasoning steps, follow-ups, a code-review exercise,
  a design-selection exercise, closed-book cues, and concise reconstruction notes.
- Used only synthetic endpoints, health checks, jobs, shipping rules, and retention policies; code
  performs no network, database, filesystem mutation, package discovery, credential handling, or
  production integration.

## Approval boundary

The artifact is Approved because repository validation, dual-runtime focused tests, the complete
repository regression, focused lint/formatting, strict dual-target typing, controlled negative
typing, dual-runtime snippet compilation, worked demo and practice execution, three reproduced
experiments, visual-data parity, JavaScript syntax, static visual checks, source review, and manual
pedagogical/runtime/production review passed.

Approval applies only to the teaching artifact. It does not claim Rahul has predicted, implemented,
debugged, explained, recalled, transferred, demonstrated, or retained SDP-PYT-100.
