# EXP-02 — Class creation, decorator, and instance construction order

| Field | Value |
|---|---|
| Owning unit | [SDP-PYT-100](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-pyt-100) |
| Precise question | Which observed phases happen while a metaclass creates a class, after that class exists, and when the class is later called? |
| Classification | Python language behavior with one separately labeled CPython `__classcell__` detail |
| Status | Reproduced |

## Why observation is necessary

The word “creation” hides two different events: creating a class object and creating an instance of
that class. A metaclass's `__new__`/`__init__` participate in the first; its `__call__` can wrap
the second. Class decorators run after the class object is created. Mixing these phases produces
incorrect explanations and difficult framework bugs.

## Hypothesis

> Cooperative subclass hooks will run when `ShippingRule` is defined. `AuditedJob` will then
> record `__prepare__`, metaclass `__new__`, metaclass `__init__`, and its class decorator. Only
> `AuditedJob("nightly")` will record metaclass `__call__` followed by instance `__new__` and
> `__init__`.

## Environment

~~~text
Date: 2026-09-06
Operating system: Linux 7.0.0-31-generic
Architecture: x86_64
Python runs: CPython 3.14.7 and CPython 3.11.16
Canonical build: Clang 22.1.3
Dependencies: standard library only
Relevant flags: none
~~~

## Controls and variables

- Controlled: module import, fixed class bodies, one decorator, one instance argument.
- Changed: class definition versus later call of the completed class.
- Measured: ordered, explicitly emitted phase events.

## Reproduction command

~~~bash
uv run --locked python units/pythonic/SDP-PYT-100-descriptors-class-hooks-metaclasses-when-justified/examples/class_creation_probe.py
~~~

## Predicted result

~~~text
subclass hooks during the relevant subclass statement
prepare -> metaclass new -> metaclass init -> class decorator
metaclass call -> instance new -> instance init
~~~

## Observed result

Both CPython 3.14.7 and CPython 3.11.16 produced the same output:

~~~text
init_subclass:ShippingRule:schema_version=1
init_subclass:ShippingRule:code=standard
prepare:AuditedJob:custom namespace
meta_new_before:AuditedJob:class object absent
meta_new_after:AuditedJob:class object created
meta_init:AuditedJob:created class initialized
decorator:AuditedJob:label=audited; identity=preserved
meta_call:AuditedJob:instance construction
instance_new:AuditedJob:nightly
instance_init:AuditedJob:nightly
result:AuditedJob:nightly
~~~

## Interpretation

1. `ShippingRule`'s first base calls `super()` before recording, so the cooperative sibling's
   event appears first. Hook order follows actual MRO and method bodies, not a guessed left-to-right
   list.
2. `DefinitionMeta.__prepare__` supplies the mapping before the `AuditedJob` body runs.
3. Metaclass `__new__` returns the class object; metaclass `__init__` then initializes that class
   object; the in-place class decorator receives the completed class afterward.
4. Calling `AuditedJob` later invokes `DefinitionMeta.__call__`, which delegates to the normal
   instance `__new__`/`__init__` path.
5. The instrumentation records its own boundaries. It does not expose every interpreter operation
   or prove that application metaclasses are desirable.

## Visual interpretation

~~~text
class statement
  -> choose metaclass
  -> Meta.__prepare__
  -> execute class body into namespace
  -> call metaclass
       -> Meta.__new__ -> type.__new__
            -> __set_name__
            -> parent.__init_subclass__
       -> Meta.__init__
  -> apply class decorators, bottom upward
  -> bind resulting object to class name

later: Class(args)
  -> type(Class).__call__
       -> Class.__new__
       -> Class.__init__ when normal conditions hold
~~~

### How to read this visual

The first path happens once per class statement. The indented `type.__new__` callbacks happen while
the class object is being produced. The second path begins only when application code calls the
finished class.

### Key insight

A metaclass `__call__` usually controls construction of instances of its classes; it is not the
same hook as the metaclass `__new__` that creates those classes.

### Simplification or limitation

The visual assumes the usual `type`-derived metaclass that delegates correctly. It omits MRO-entry
resolution, decorator-expression evaluation, a non-type metaclass callable, unusual `__new__`
returns, exceptions, and implementation optimizations.

## Design conclusion

Post-creation validation normally belongs in `__init_subclass__` or a class decorator. Use a
metaclass only when the framework truly needs namespace preparation, coordinated class-object
creation, metaclass-level special behavior, or instance construction policy across the family.

## CPython-only safety note

The official data-model documentation labels `__classcell__` propagation a CPython implementation
detail. A `type`-derived metaclass should pass the complete namespace to `type.__new__`. A focused
test in this unit deliberately drops the cell and observes the documented `RuntimeError` on
CPython; it is skipped on other implementations and is not treated as a cross-implementation
language contract.

## Sources

1. [Python 3.14 data model — customizing class creation](https://docs.python.org/3.14/reference/datamodel.html#customizing-class-creation).
2. [Python 3.14 class-definition execution and decorators](https://docs.python.org/3.14/reference/compound_stmts.html#class-definitions).
3. [PEP 487 — simpler customization of class creation](https://peps.python.org/pep-0487/).
4. [PEP 3115 — `__prepare__` and metaclass syntax](https://peps.python.org/pep-3115/).
5. [PEP 3135 — implicit `__class__` cell and zero-argument `super()`](https://peps.python.org/pep-3135/).
