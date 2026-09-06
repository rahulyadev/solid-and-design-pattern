# EXP-03 — Annotation evaluation timing on Python 3.11 and 3.14

| Field | Value |
|---|---|
| Owning unit | [SDP-PYT-100](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-pyt-100) |
| Precise question | If a class annotation names an undefined object and no future-annotations flag applies, does class definition fail immediately or only later annotation evaluation? |
| Classification | Version-dependent Python language and standard-library behavior |
| Status | Reproduced |

## Why observation is necessary

Class decorators, `__init_subclass__` hooks, and metaclasses sometimes read annotations as runtime
declarations. Python 3.14 changed annotation evaluation to lazy semantics and added `annotationlib`.
A framework that assumes Python 3.11 timing can move a failure to a different lifecycle stage after
an upgrade.

## Hypothesis

> On Python 3.11, evaluating `MissingType` while the class body executes will raise `NameError` and
> no class will be bound. On Python 3.14, class definition will complete, the class will expose a
> lazy annotation function, and asking `annotationlib` for value-form annotations will raise the
> `NameError`.

## Environment

~~~text
Date: 2026-09-06
Operating system: Linux 7.0.0-31-generic
Architecture: x86_64
Python runs: CPython 3.11.16 and CPython 3.14.7
Build: Clang 22.1.3
Dependencies: standard library only
Relevant flag: compile(..., dont_inherit=True) prevents this probe module's future import from changing the compiled source
~~~

## Controls and variables

- Controlled: identical source text, undefined name, fresh namespace, and no inherited future flag.
- Changed: Python runtime.
- Measured: definition outcome, class binding, lazy annotation hook, and value evaluation outcome.

## Reproduction commands

~~~bash
/tmp/sdp-pyt100-venv311/bin/python units/pythonic/SDP-PYT-100-descriptors-class-hooks-metaclasses-when-justified/examples/annotation_timing_probe.py
/tmp/sdp-pyt100-venv314/bin/python units/pythonic/SDP-PYT-100-descriptors-class-hooks-metaclasses-when-justified/examples/annotation_timing_probe.py
~~~

The `/tmp` environment paths record this validation run. Any Python 3.11 and 3.14 interpreters can
run the standard-library-only script.

## Observed result — CPython 3.11.16

~~~text
python=3.11
definition=NameError
class_bound=False
~~~

## Observed result — CPython 3.14.7

~~~text
python=3.14
definition=completed
class_bound=True
has_annotate=True
evaluation=NameError
~~~

## Interpretation

1. The identical annotation changes failure timing across the two supported runtimes.
2. On 3.11 the undefined name prevents completion of the class statement.
3. On 3.14 definition completes; requesting value-form annotations triggers evaluation and the
   unresolved name then fails.
4. This does not imply that every annotation fails, that string-form inspection must evaluate
   names, or that frameworks should consume annotations.
5. `from __future__ import annotations` and explicit string annotations are different inputs and
   are intentionally excluded by `dont_inherit=True`.

## Visual interpretation

~~~text
Python 3.11:
class body -> evaluate MissingType -> NameError -> no Config binding

Python 3.14:
class body -> store lazy annotation machinery -> Config bound
                                           |
annotationlib.get_annotations(..., VALUE) -+
                                           -> evaluate MissingType -> NameError
~~~

### How to read this visual

Follow each runtime left to right. The failure is the same kind of unresolved-name error, but the
phase owning it changes from class-body execution to later annotation evaluation.

### Key insight

Annotation-driven class machinery has a versioned lifecycle contract, not merely a different helper
function name.

### Simplification or limitation

The probe uses one unresolved global name and value-form evaluation. It does not cover future
annotations, explicit strings, forward-reference format, fake globals, type parameters, nested
classes, or framework-specific resolution.

## Design conclusion

Avoid annotation inspection unless annotations are an intentional runtime declaration API. If it
is required, use a version adapter around documented introspection, choose the needed format,
identify when resolution errors should surface, and test Python 3.11 and 3.14 separately.

## Sources

1. [Python 3.14 data model — lazy class annotations](https://docs.python.org/3.14/reference/datamodel.html#type.__annotations__).
2. [Python 3.14 `annotationlib`](https://docs.python.org/3.14/library/annotationlib.html).
3. [Python 3.11 data model — class annotations and class creation](https://docs.python.org/3.11/reference/datamodel.html).
