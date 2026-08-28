# SOLID and Design Patterns in Python

> **Start here:** [Open `START_HERE.md`](START_HERE.md)

A Python-first, evidence-based repository for mastering software-design foundations, SOLID principles, all 23 Gang of Four patterns, Pythonic alternatives, application architecture, refactoring, and senior interview judgment.

## One-time setup and daily use

- Use the **Local** checkout once to validate and commit the extracted bootstrap on `setup/solid-design-pattern-bootstrap`.
- Publish that bootstrap only with the separate exact prompt in [`START_HERE.md`](START_HERE.md).
- After `main` contains the validated baseline, use one **Worktree** chat for each topic or project.
- Initialize a topic with `Initialize <TOPIC-ID>.`
- Initialize a project with `Initialize project <PROJECT-ID>.`
- Successful initialization may push only commits created during the current initialization operation on the exact topic or project branch; it never opens a pull request, merges, or changes remote `main`.
- Later learning changes remain local until an explicit completion choice.

Run repository validation with:

```bash
python scripts/validate_repo.py
```

## What this repository provides

- A canonical catalog of [100 learning units](CURRICULUM.md)
- All 23 Gang of Four patterns as independent units
- Eight [recommended learning paths](LEARNING_PATHS.md), led by urgent interview preparation
- Exact [Python Mastery cross-references](PYTHON_REFERENCES.md)
- One dedicated Codex chat and Worktree per learning unit
- Just-in-time unit and project folders
- Integrated, NotebookLM-ready learning notes with a `Physical Notebook Core`
- Protected exercises, labs, experiments, and closed-book reviews
- Evidence-based [unit and project progress tracking](PROGRESS.md)
- Six substantial [milestone projects](PROJECTS.md)
- Reproducible standard-library-only [repository validation](scripts/validate_repo.py)
- Explicit source, version, history, copyright, licensing, privacy, and Git-safety rules

## Important rules

- Examples must be idiomatic Python, not Java translated into Python syntax.
- Python 3.14 is canonical; Python 3.11 alternatives are shown when interview platforms may lag.
- Generated material does not prove learning.
- Every pattern must include the simpler design, the change pressure, trade-offs, misuse, and when not to use it.
- Before any initialization push, Codex enumerates local-only commits. It stops if a normal push would publish older learning work, and it does not push again when the validated initialized version is already remote.
- Questions and later learning edits may be committed locally but are not pushed automatically.
- Project completion does not automatically advance curriculum-unit learning states.
- No license has been selected. See [docs/COPYRIGHT_AND_LICENSE.md](docs/COPYRIGHT_AND_LICENSE.md).

## Repository map

| Path | Purpose |
|---|---|
| [`START_HERE.md`](START_HERE.md) | One-time bootstrap and shortest daily workflow |
| [`CURRICULUM.md`](CURRICULUM.md) | Canonical units, prerequisites, dimensions, estimates, order, and anchors |
| [`LEARNING_PATHS.md`](LEARNING_PATHS.md) | Clickable interview, mastery, backend, and refactoring sequences |
| [`PYTHON_REFERENCES.md`](PYTHON_REFERENCES.md) | Exact absolute links to supporting Python Mastery units |
| [`PROGRESS.md`](PROGRESS.md) | Evidence-based unit states and separate project tracker |
| [`PROJECTS.md`](PROJECTS.md) | Six staged integration projects |
| [`AGENTS.md`](AGENTS.md) | Lean durable repository-wide Codex behaviour |
| [`docs/WORKFLOW.md`](docs/WORKFLOW.md) | Detailed Local, Worktree, teaching, lab, evidence, push, and publication procedures |
| [`scripts/validate_repo.py`](scripts/validate_repo.py) | Standard-library-only repository and archive validator |
| [`templates/`](templates/unit.md) | Unit, practice, experiment, review, and project templates |
| [`NOTEBOOKLM.md`](NOTEBOOKLM.md) | Concise NotebookLM handoff |
| [`BUNDLE_MANIFEST.md`](BUNDLE_MANIFEST.md) | Archive inventory and validation expectations |

## Environment

The bootstrap pins the verified runtime in [`.python-version`](.python-version) and uses `uv` with [`pyproject.toml`](pyproject.toml) and [`uv.lock`](uv.lock). Install the locked development tool group when runnable learning artifacts exist:

```bash
uv sync --group dev
```

No `units/` or `projects/` directory exists until the first unit or project is initialized.
