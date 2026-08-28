# SOLID and Design Pattern Workflow

[Start here](../START_HERE.md) · [Curriculum](../CURRICULUM.md) · [Learning paths](../LEARNING_PATHS.md) · [Python references](../PYTHON_REFERENCES.md) · [Progress](../PROGRESS.md) · [Projects](../PROJECTS.md)

This document owns detailed operating procedures. Daily prompts remain short.

## 1. Daily operating model

- One permanent curriculum-helper chat finds the correct unit.
- One dedicated Worktree chat owns one learning unit or one project.
- Topic folders and project folders are created only when initialized.
- After initialization, Rahul asks normal follow-up questions without repeating an ID or selecting a mode.
- Only a validated initialization commit is pushed automatically.
- Later learning changes stay local until explicit completion publication.

## 2. Permanent curriculum-helper chat

Use a prompt such as:

```text
Find the best curriculum unit for <topic or question>. Return the canonical unit ID, exact title, short reason, essential prerequisites, commonly confused or related units, relevant Python Mastery references, whether its unit folder exists in the repository, and the exact initialization prompt. Do not initialize the unit unless I ask.
```

When a question spans units, the helper identifies one primary owner, lists related units, explains where each part belongs, and recommends the dedicated chat to use. It must not claim to know whether another ChatGPT or Codex chat exists.

## 3. One-time Local bootstrap

Extract the ZIP into the existing local repository root and use the exact bootstrap-local prompt in `START_HERE.md`.

Before branch work:

1. Inspect `git status --short --branch`.
2. Inspect the current commit and branch.
3. Inspect local and remote setup branches.
4. Create or resume exactly `setup/solid-design-pattern-bootstrap`.
5. Run `python scripts/validate_repo.py`.
6. Review the diff for unexpected or private content.
7. Commit only validated bootstrap files locally.

The bootstrap-local prompt never authorizes push, pull request, merge, topic initialization, or project initialization. The separate bootstrap-publication prompt authorizes publication after local review.

## 4. Worktree baseline and detached HEAD

For every new topic or project, Rahul opens a Worktree from the latest synchronized `main`.

A Worktree may start in detached `HEAD`. Before branch creation or resumption, inspect:

```bash
git status --short --branch
git rev-parse HEAD
git branch --show-current
git show-ref --verify --quiet refs/heads/main
git show-ref --verify --quiet refs/remotes/origin/main
git worktree list --porcelain
```

Refresh only the exact remote refs needed for comparison. Use no-tag fetches that can refresh a rewritten local remote-tracking ref:

```bash
git fetch --no-tags origin \
  +refs/heads/main:refs/remotes/origin/main
```

For a topic branch, inspect and fetch only the exact requested ref:

```bash
git ls-remote --exit-code --heads origin refs/heads/topic/<TOPIC-ID>
git fetch --no-tags origin \
  +refs/heads/topic/<TOPIC-ID>:refs/remotes/origin/topic/<TOPIC-ID>
```

For a project branch:

```bash
git ls-remote --exit-code --heads origin refs/heads/project/<PROJECT-ID>
git fetch --no-tags origin \
  +refs/heads/project/<PROJECT-ID>:refs/remotes/origin/project/<PROJECT-ID>
```

The leading `+` permits only the named local remote-tracking ref under `refs/remotes/origin/` to reflect a rewritten remote branch. It does not push anything, rewrite remote history, or move Rahul's local `main`, topic, or project branch.

A missing exact branch is a normal `ls-remote` non-zero result, not permission to invent another name. For a new branch, the selected Worktree commit, local `main`, and `origin/main` must identify the same synchronized baseline. Otherwise stop with the smallest synchronization instruction.

## 5. Exact branch ownership and remote comparison

Topic branch:

```text
topic/<TOPIC-ID>
```

Project branch:

```text
project/<PROJECT-ID>
```

Never create lowercase, shortened, suffixed, duplicate, `-2`, or `-new` variants.

Before checkout or creation, determine:

1. whether the exact local branch exists;
2. whether the exact remote branch exists;
3. whether another Worktree owns the local branch;
4. whether the current Worktree has unrelated uncommitted changes;
5. whether local and remote histories are identical, ahead, behind, or diverged.

When both refs exist, compare them with the exact names. For a topic:

```bash
git rev-list --left-right --count refs/heads/topic/<TOPIC-ID>...refs/remotes/origin/topic/<TOPIC-ID>
```

For a project:

```bash
git rev-list --left-right --count refs/heads/project/<PROJECT-ID>...refs/remotes/origin/project/<PROJECT-ID>
```

The first number is local-only commits; the second is remote-only commits.

### Branch-state decision matrix

| Branch state | Required safe action | Automatic initialization push |
|---|---|---|
| Neither local nor remote exists | Create the exact branch from the verified synchronized `main` commit. | Allowed only for commits created during this initialization. |
| Remote only | Fetch the exact ref and create the exact local tracking branch at that remote commit. | Do not push if the validated initialized version is already remote; otherwise only current-operation commits may be pushed. |
| Local only | Resume only in its owning Worktree. If it contains any commit that existed before this initialization, preserve it. | Blocked when a normal first push would publish older local-only commits; ask for explicit publication authorization. |
| Local and remote are identical | Resume the exact branch. | No push when initialization is already present; otherwise only current-operation commits may be pushed. |
| Local is ahead | Enumerate every local-only commit before doing any push. | Allowed only when every ahead commit was created during the current initialization operation; otherwise stop. |
| Remote is ahead | With a clean Worktree and zero local-only commits, fast-forward using the exact remote ref, then re-evaluate. | No push for already-remote initialization; later current-operation commits may be pushed normally. |
| Histories diverged | Stop and report the smallest explicit reconciliation decision required from Rahul. | Never. |
| Exact branch is owned by another Worktree | Stop and direct Rahul to the original pinned chat and Worktree. | Never from the current Worktree. |

Never reset, force, silently rebase, auto-merge divergence, or choose one side. Never stash or discard unrelated changes.

### Current-operation-only push proof

Before recording the initialization start, require a completely clean Worktree:

```bash
git status --porcelain=v1 --untracked-files=all
```

Any output means pre-existing tracked, staged, or untracked work exists. Stop and request an explicit decision before continuing. Never allow that work into an initialization commit, and never amend or rewrite a pre-existing commit during initialization.

Only after the command produces no output, record the branch tip immediately before creating initialization content:

```bash
git rev-parse HEAD
```

Call that commit `INIT_START`. Immediately before a topic push, enumerate all local-only commits:

```bash
git log --format='%H %s' --reverse refs/remotes/origin/topic/<TOPIC-ID>..refs/heads/topic/<TOPIC-ID>
```

If no remote topic branch exists, compare against synchronized `main`:

```bash
git log --format='%H %s' --reverse refs/heads/main..refs/heads/topic/<TOPIC-ID>
```

Enumerate commits created during the current operation:

```bash
git log --format='%H %s' --reverse INIT_START..HEAD
```

Use the equivalent `project/<PROJECT-ID>` refs for projects. Automatic push is allowed only when the local-only list and current-operation list are identical. If an older local-only commit appears, stop and ask for explicit publication authorization. If the validated initialized version is already present remotely and no new initialization commit exists, report `no push required`.

Use an exact normal push. On first topic push:

```bash
git push --set-upstream origin refs/heads/topic/<TOPIC-ID>:refs/heads/topic/<TOPIC-ID>
```

For an existing upstream:

```bash
git push origin refs/heads/topic/<TOPIC-ID>:refs/heads/topic/<TOPIC-ID>
```

Use the same exact refspec shape for `project/<PROJECT-ID>`. Stop on authentication failure, non-fast-forward rejection, branch protection, or any uncertain result.

## 6. Topic initialization

The exact command is:

```text
Initialize <TOPIC-ID>.
```

It authorizes:

1. Validate the complete ID in `CURRICULUM.md`.
2. Read the matching progress row and relevant Python-reference mappings.
3. Verify synchronized `main`, Worktree ownership, and the exact local/remote branch state.
4. Safely create, fast-forward, or resume exactly `topic/<TOPIC-ID>` according to the decision matrix.
5. Run `git status --porcelain=v1 --untracked-files=all`; if it prints anything, stop for an explicit decision. Only then record `INIT_START` before creating or changing initialization content.
6. Explain hard prerequisites briefly; provide a bridge and continue unless materially misleading.
7. Create `units/<domain-slug>/<TOPIC-ID>-<topic-slug>/README.md` from `templates/unit.md`.
8. Create a focused `practice/` starter when the evidence profile requires implementation or debugging.
9. Create no empty optional artifacts.
10. Update only the matching progress row to artifact state Draft; do not advance learning state.
11. Add only valid links to already existing indexes.
12. Run `python scripts/validate_repo.py`.
13. Run all relevant generated code and tests, normally through the locked development environment.
14. Inspect privacy, copyright, source, version, and solution-protection boundaries.
15. Commit the validated initialization content.
16. Enumerate local-only commits and current-operation commits exactly as defined above.
17. Push only when the lists match; set upstream on first push.
18. If older local-only learning commits would be published, stop and request explicit publication authorization.
19. If the validated initialized version is already remote, do not push again.
20. Report branch state, commits, files, validator, tests, and push or no-push result.

Initialization never authorizes a pull request, merge, remote `main` change, force-push, failed-check bypass, unrelated edit, or publication of pre-existing local learning commits.

## 7. Unit initialization content

The integrated note begins with `Physical Notebook Core`, then includes only applicable deep sections from `templates/unit.md`.

Every core SOLID or pattern unit should normally include a runnable starter lab. A clear reason is required to omit code, for example a purely comparative unit whose evidence is scenario selection and code review rather than implementation.

Initial content must be complete enough to study, but exercises remain unsolved. Working examples in the note must not reveal the separate lab solution.

## 8. Natural follow-up questions

In the established topic chat Rahul may ask:

```text
Explain this visually.
I still do not understand the dependency arrows.
Show me the simplest Python version.
Compare this with State.
Add a new requirement that breaks the naive design.
Give me a refactoring exercise.
Review my attempt.
Quiz me.
Interview me on this.
Update the notes with what we clarified.
```

Infer the activity. Do not ask Rahul to choose a mode.

## 9. Teaching sequence

Unless the question requires another order:

1. State the problem or change pressure.
2. Give a one-sentence mental model.
3. Show the simplest solution without the pattern.
4. Add the requirement that creates concrete pain.
5. Show participants, responsibilities, and dependency direction.
6. Trace object or call collaboration step by step.
7. Implement the smallest idiomatic Python version.
8. Add a typed production-oriented version when useful.
9. Compare a simpler Python alternative.
10. Show misuse, failure, testing, observability, and state-safety concerns.
11. Explain when to use and when not to use it.
12. Ask for reconstruction, transfer, or interview reasoning.

History and formal definitions follow simple intuition. Do not ask Rahul to memorize scripts.

## 10. Pythonic code standard

Prefer ordinary functions, first-class callables, composition, Protocols, dataclasses, enums, context managers, generators, small modules, and explicit dependency passing when they fit.

Use inheritance or ABCs only when a behavioural contract and substitution relationship justify them. Use descriptors, class hooks, or metaclasses only when the problem survives simpler alternatives.

For important patterns compare:

- simplest solution without the pattern;
- concrete pain after requirements change;
- pattern-based solution;
- most Pythonic form;
- overengineered or incorrect form.

Python 3.14 is canonical. Add Python 3.11-compatible alternatives when newer syntax or APIs may fail on interview platforms.

## 11. Visual standard

Use dependency arrows, before/after structures, Mermaid class or sequence diagrams, state diagrams, object graphs, call flows, lifecycles, exact comparison tables, or compact notebook ASCII diagrams when relationships are otherwise hidden.

Every non-trivial visual includes:

```md
### How to read this visual
### Key insight
### Simplification or limitation
```

Say whether the diagram is conceptual or literal runtime behaviour. Never present a conceptual object diagram as CPython memory layout.

## 12. Practice and lab cycle

Labs follow:

```text
predict → run → observe → explain → refactor → vary
```

A focused practice directory may contain starter code, tests, a short brief, commands, edge cases, troubleshooting, and reflection questions.

Rules:

1. Exercises begin unsolved.
2. Preserve Rahul’s original attempt and reasoning.
3. Ask for a prediction before execution when useful.
4. Give one progressive hint at a time.
5. Do not leak the solution through examples, comments, tests, fixtures, filenames, or expected internals.
6. Identify the first incorrect assumption before replacement code.
7. Passing tests are insufficient when the design reasoning is wrong.
8. Add a comparison solution only after Rahul closes the exercise.
9. Never claim a command or test ran unless actual output was observed.

## 13. Interview preparation

For interview-relevant units progress through:

1. simple definition;
2. problem and forces;
3. scenario recognition;
4. collaboration;
5. implementation;
6. trade-offs;
7. alternatives;
8. misuse;
9. comparison;
10. changed requirements;
11. production failure handling;
12. senior critique.

Include weak-answer traps, likely follow-ups, code review, refactoring, and small design exercises. During interactive interviews ask one question at a time, wait, then identify the exact missing reasoning step.

## 14. Durable note updates

A clarification belongs in canonical notes when it corrects an error, removes ambiguity, explains a recurring misconception, adds a missing boundary, improves an example, or records a generally useful comparison.

Keep personal confusion history in `REVIEW.md`. Make the smallest correct edit, validate, and commit locally on the same branch. Do not push later learning changes automatically.

## 15. Progress evidence

Use `PROGRESS.md` thresholds.

- Initialization changes only artifact state to Draft.
- Practiced requires an attempt, applicable passing tests, edge cases, and explanation.
- Recalled requires delayed closed-book reconstruction.
- Demonstrated requires selecting or rejecting the pattern for a new scenario, explaining alternatives, and successful refactoring or implementation.
- Retained requires later spaced retrieval or independently evaluated transfer.
- Project evidence may support but never automatically change a unit state.

## 16. Topic completion: keep newer changes local

```text
I completed <TOPIC-ID>. Keep any new changes local and do not push or merge.
```

Run repository validation and relevant tests, update evidence honestly, and commit remaining changes locally. Do not push, create a pull request, or merge. Report that the remote branch still contains the initialized version while newer changes remain in the pinned Worktree.

## 17. Topic completion: publish and merge

```text
I completed <TOPIC-ID>. Finalize it, push the latest changes, and merge the topic branch into main.
```

This authorizes final checks, accurate evidence edits, remaining commits, a normal push, pull-request creation when supported, merge after checks, and `main` synchronization. Prefer squash merge. Never force-push, bypass checks or protection, or discard unrelated work.

If completion omits the publication choice, ask only:

```text
Should I keep the latest changes local, or push them and merge the branch into main?
```

Archive a Worktree only after safe merge and confirmation that no local work remains.

## 18. Project initialization

The exact command is:

```text
Initialize project <PROJECT-ID>.
```

It authorizes:

1. Validate the ID in `PROJECTS.md`; never treat it as a curriculum unit.
2. Verify synchronized `main`, Worktree ownership, and the exact local/remote project branch state.
3. Safely create, fast-forward, or resume exactly `project/<PROJECT-ID>` according to the decision matrix.
4. Run `git status --porcelain=v1 --untracked-files=all`; if it prints anything, stop for an explicit decision. Only then record `INIT_START` before changing project initialization content.
5. Create `projects/<PROJECT-ID>-<project-slug>/README.md` from `templates/project.md` plus required starter code and tests.
6. Set only the matching project tracker row to Active.
7. Run `python scripts/validate_repo.py` and relevant project tests.
8. Commit the initialized project.
9. Enumerate local-only and current-operation commits with the exact project refs.
10. Push only when the lists match; set upstream on first push.
11. Stop for explicit publication authorization if older local-only project commits would also be published.
12. Do not push again if the validated initialized version is already remote.
13. Report branch state, commits, files, checks, tests, and push or no-push result.

It does not authorize a pull request, merge, remote `main` change, force-push, publication of older local work, or automatic unit-state advancement.

## 19. Project completion

Keep newer changes local:

```text
I completed project <PROJECT-ID>. Keep any new changes local and do not push or merge.
```

Publish and merge:

```text
I completed project <PROJECT-ID>. Finalize it, push the latest changes, and merge the project branch into main.
```

If the publication choice is missing, ask the same single local-versus-publish question used for topics.

## 20. Reproducible validation

Run the standard-library validator from the repository root:

```bash
python scripts/validate_repo.py
```

Install the locked development tools when runnable unit or project code exists:

```bash
uv sync --group dev
```

Run relevant tests and quality checks through the locked environment, for example:

```bash
uv run pytest
uv run ruff check .
uv run mypy units projects
```

Use only commands applicable to existing generated paths; the bootstrap intentionally has no `units/` or `projects/` directory.

For archive validation and machine-readable output:

```bash
python scripts/validate_repo.py \
  --archive solid-design-pattern-bootstrap.zip \
  --json solid-design-pattern-bootstrap-validation.json
```

The validator checks required files, 100 units, stable anchors, all five SOLID principles when a path claims complete coverage, all 23 GoF patterns, allowed classification values, prerequisite existence/cycles/order, progress parity, declared path counts, path ordering and bridge labels, rapid/full timing totals, six projects, project tracker parity, Python references, TOML parsing, locked development dependencies, Markdown, links, templates, IDs, terminology, hygiene, archive root layout, and archive integrity.

When `uv` is available, the validator runs `uv lock --check`; when it is unavailable, that external check is reported as `skipped`, never as `passed`. Automated checks are reported separately from manual review items such as pedagogical depth and future generated-code quality.

Use validation during bootstrap, unit initialization, project initialization, local completion, and publication. Run relevant generated code and tests in addition.

## 21. Markdown and link conventions

- Use complete `SDP-...`, `SDP-PRJ-...`, and approved `PY-...` IDs.
- Use stable lowercase anchors.
- Use repository-relative links internally and absolute GitHub links for Python Mastery.
- Do not link to an uncreated unit or project folder.
- Keep template placeholders only under `templates/`.
- Balance code fences and use four tildes around examples containing triple fences.
- Keep every Markdown table’s header, separator, and data rows at the same column count.
- Escape literal table-cell pipes as `\|`.

## 22. Source, copyright, and privacy

Use authoritative sources actually read. Cite subtle semantics, history, version claims, security, concurrency, performance, and CPython details near the claim. Summarize copyrighted books and papers in original wording; do not reproduce their diagrams or long examples.

Use synthetic business domains and data. Never commit credentials, secrets, private conversations, employer code, production logs, customer data, paid-course material, interview take-homes, or unlicensed copied examples.

## 23. Structural changes

Changing curriculum, project scope, classifications, prerequisites, templates, workflow, or validation requires explicit approval, updates to all affected references, validation, preservation of unrelated work, and a clear publication report.
