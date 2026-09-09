# Unsolved dispatch lab — SDP-CRE-040

## Brief and evidence boundary

A small dispatch service currently constructs a profile from channel and destination inputs. The
starter works. A new requirement introduces approved, externally configured routing profiles and
request-specific working copies. Your job is to decide whether copying is justified and, if so,
define its contract before choosing an API. The target is intentionally not implemented.

Do not edit the query-graph example to solve this exercise. Do not open a comparison solution: none
is supplied. Keep `dispatch_lab.py` and the original baseline tests as the record of the starting
point. Save your first attempt in a new file in this directory, with a short original prediction and
reasoning note. Do not overwrite later corrections onto the original attempt.

## Predict → run → observe → explain → refactor → vary

1. **Predict:** Draw the references created by `prepare_dispatch`. Predict what happens when the
   caller mutates its input destination list. Then predict the effect of assigning the same profile
   to two requests, shallow copying it, and deeply copying it. State which prediction is based on
   the current flat structure and could change when routes become nested.
2. **Run:** Execute the unchanged starter and its baseline tests with the commands below.
3. **Observe:** Record the actual output, identities, and mutation effects. Distinguish new outer
   objects from independent reachable mutable values. Record surprises without deleting predictions.
4. **Explain:** Describe who owns the input list and attempt history. State why a green baseline does
   not satisfy the new requirement. Explain the smallest alternative to Prototype.
5. **Refactor:** Implement your own approach and tests for the target requirements. Preserve channel
   validation. Do not add a registry or inheritance unless your reasoning identifies a concrete need.
6. **Vary:** Accept one changed requirement at a time after review; amend your design or reject the
   pattern with evidence. Explain the first violated invariant before writing replacement code.

## Target requirements (behavior, not prescribed implementation)

- A request starts from one approved configured routing profile without modifying it.
- Each request can edit its destination/routing state independently from the exemplar and siblings.
- Attempt history begins empty even if the exemplar has prior diagnostic attempts.
- A request supplies a new business identity; copying never authorizes a tenant change.
- A stale configuration revision is rejected before any result is published.
- Invalid configuration leaves the exemplar unchanged and returns no partial request profile.
- Credentials and active delivery sessions are not duplicated into the result.
- If routing becomes a graph, define explicitly which internal aliases should survive; demonstrate
  one repeated-node case and one cycle or explain why cycles are invalid for your domain.

Choose your data model and API. The tests here deliberately do not reveal a target constructor,
field layout, clone body, registry, or fixture for those requirements. Passing them proves only
baseline behavior. Write black-box target tests and explain the ownership edges they verify.

## Commands

From the repository root, select an already installed locked development interpreter as `python`.
Keep generated artifacts outside the Worktree:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=/tmp/sdp-cre-040-practice/bytecode
export MYPY_CACHE_DIR=/tmp/sdp-cre-040-practice/mypy
export RUFF_CACHE_DIR=/tmp/sdp-cre-040-practice/ruff
export HYPOTHESIS_STORAGE_DIRECTORY=/tmp/sdp-cre-040-practice/hypothesis
export UV_CACHE_DIR=/tmp/sdp-cre-040-practice/uv
export COVERAGE_FILE=/tmp/sdp-cre-040-practice/coverage
python units/creational/SDP-CRE-040-prototype/practice/dispatch_lab.py
python -m pytest -p no:cacheprovider units/creational/SDP-CRE-040-prototype/practice
```

The baseline prints its channel/destination count and `target_complete=False`. These commands do not
initialize another unit or update progress. Do not run an environment-creating command in the
Worktree unless its environment directory is explicitly redirected to `/tmp`.

## Changed requirements for later review

Choose only one: two profiles share a read-only routing vocabulary; an editor may update approved
profiles while requests start; a provider needs async acquisition with cancellation; or a new policy
version changes which destination combinations are legal. Identify whether clone, reconfiguration,
factory, or immutable replacement is now the smallest adequate design.

## Hint and review discipline

Ask for one progressive hint when stuck; no hint ladder or solution is stored here. The reviewer
should locate the first incorrect assumption before suggesting code. Evidence requires your attempt,
prediction/observations, edge cases, and explanation. Maintainer-authored examples and tests do not
advance your learning state.
