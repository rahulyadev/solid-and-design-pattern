# EXP-01 — Import cache, reload, and retained aliases

| Field | Value |
|---|---|
| Owning unit | [SDP-PYT-050](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-pyt-050) |
| Precise question | How do repeated import, reload, a retained imported value, and cache-key deletion differ? |
| Classification | Python import system and standard library |
| Status | Reproduced |

## Why observation is necessary

“A module runs once” collapses several operations into one slogan. Identity differs depending on
whether a name is found in `sys.modules`, the existing module is reloaded, or the cache key is
deleted while another reference retains the old module. A value bound from a module has its own
alias lifetime.

## Hypothesis

> The second import will reuse the first module without executing it again. Reload will reuse that
> module object but execute its code again and replace its marker. The previously bound marker will
> remain old. Deleting only the cache key, then importing, will create a new module while the
> retained old module remains reachable.

## Environment

```text
Date: 2026-09-06
Operating system: Linux 7.0.0-31-generic
Architecture: x86_64
Primary Python: CPython 3.14.7, Clang 22.1.3, glibc 2.43
Compatibility reproduction: CPython 3.11.16, Clang 22.1.3, glibc 2.43
Dependencies: Python standard library only
Relevant flags: none
```

## Controls and variables

- Controlled: one uniquely named synthetic target module, one process, one interpreter, fixed
  operation order, and restoration of any prior cache entry.
- Changed: repeated import, `importlib.reload`, and deletion of only the target's `sys.modules`
  key.
- Measured: module identity, execution-generation counter, and retained marker identity.

The probe never deletes arbitrary or essential module-cache entries.

## Reproduction command

From the repository root:

```bash
uv run --locked python units/pythonic/SDP-PYT-050-modules-import-caching-dependency-lifetimes/examples/import_cache_probe.py
/tmp/sdp-pyt-040-tools.b57yty/venv311/bin/python units/pythonic/SDP-PYT-050-modules-import-caching-dependency-lifetimes/examples/import_cache_probe.py
```

The second path records the available locked-tool Python 3.11.16 compatibility environment used
during this run; it is not a repository path or a required learner path.

## Predicted result

```text
first count = 1
repeat: same module, count still 1
reload: same module, count 2, old imported marker not rebound
delete key + import: different module, new count 1
```

## Observed result

Both CPython 3.14.7 and CPython 3.11.16 produced:

```json
{
  "cache_deletion_creates_new_module": true,
  "execution_count_after_reload": 2,
  "execution_count_after_repeat": 1,
  "first_execution_count": 1,
  "imported_alias_stays_old": true,
  "new_module_execution_count": 1,
  "reload_reuses_module": true,
  "repeat_returns_same_module": true
}
```

## Interpretation

1. The result directly shows cache reuse for one fully qualified name in this interpreter, code
   re-execution under reload, retained alias identity, and two live module objects after cache-key
   deletion plus re-import.
2. It supports designing tests around explicit owners instead of assuming reload is a fresh app.
3. It does not show that every loader behaves identically, that import means exactly once for a
   process lifetime, or that application resources receive cleanup.

## Visual interpretation

```text
import #1:  cache[name] ──> module M1 ──> marker G1
import #2:  cache[name] ──> module M1 ──> marker G1
reload:     cache[name] ──> module M1 ──> marker G2
                                          marker alias ──> G1
delete key; retain M1
re-import:  cache[name] ──> module M2 ──> marker G1
             retained reference ─────────> module M1
```

### How to read this visual

Follow `cache[name]` after each operation. Object labels describe identity within this run;
generation labels describe how often target code executed in that module dictionary.

### Key insight

Cache association, module identity, namespace contents, and external aliases are four different
things.

### Simplification or limitation

This conceptual identity graph omits import locks, loader behavior, parent packages, cycles,
extension modules, garbage collection, and concurrent reload.

## Design conclusion

Use modules confidently for declarations and stateless namespace APIs. Do not use cache deletion or
reload as an application lifecycle manager. Construct a fresh explicit owner when a test or app
needs independent runtime state.

## Limitations

- The target is an ordinary source module loaded by the default path machinery.
- Identity is compared directly but raw memory addresses are not recorded.
- The probe is single-threaded; official documentation separately marks reload as not thread-safe.
- Matching 3.11 and 3.14 observations do not turn every detail into a cross-implementation promise.

## Sources

1. Python Software Foundation, [Python 3.14 module cache](https://docs.python.org/3.14/reference/import.html#the-module-cache).
2. Python Software Foundation, [Python 3.14 loading process](https://docs.python.org/3.14/reference/import.html#loading).
3. Python Software Foundation, [Python 3.14 `importlib.reload`](https://docs.python.org/3.14/library/importlib.html#importlib.reload).
