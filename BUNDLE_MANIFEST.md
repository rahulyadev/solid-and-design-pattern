# Bootstrap Bundle Manifest

This bundle initializes the public `solid-and-design-pattern` learning repository. Extract it directly into the repository root. It contains no wrapper directory, Git metadata, generated learning units, generated projects, environment, secrets, private data, transcript, cache, or license file.

## File inventory

| Path | Purpose |
|---|---|
| `.gitignore` | Excludes environments, caches, build output, profiler data, secrets, and local generated noise. |
| `.python-version` | Pins the initially verified canonical CPython patch runtime. |
| `AGENTS.md` | Lean repository-wide Codex contract. |
| `BUNDLE_MANIFEST.md` | Lists bootstrap files, purposes, exclusions, and validation commands. |
| `CURRICULUM.md` | Canonical domains, 100 learning units, stable IDs, prerequisites, classifications, estimates, and anchors. |
| `LEARNING_PATHS.md` | Eight clickable interview, mastery, backend, refactoring, and comparison paths. |
| `PYTHON_REFERENCES.md` | Absolute links to exact supporting Python Mastery curriculum units. |
| `NOTEBOOKLM.md` | Short entry point for the NotebookLM handoff. |
| `PROGRESS.md` | Separate artifact and learning states plus the six-project tracker. |
| `PROJECTS.md` | Six staged milestone projects with stable IDs and definitions of done. |
| `README.md` | Repository overview and prominent `START_HERE.md` link. |
| `START_HERE.md` | One-time Local bootstrap and simple Worktree topic/project workflow. |
| `pyproject.toml` | Python baseline plus the real `dev` dependency group for pytest, coverage, Ruff, mypy, and Hypothesis. |
| `uv.lock` | Reproducible lock for the approved development tools and their required runtime dependencies. |
| `docs/COPYRIGHT_AND_LICENSE.md` | Public-repository copyright, quotation, reuse, confidentiality, and license-decision rules. |
| `docs/NOTEBOOKLM.md` | Detailed approved-note upload, flashcard, quiz, comparison, interview, and weakness-return workflow. |
| `docs/SOURCE_AND_VERSION_POLICY.md` | Authoritative source order, history, version compatibility, citation, experiment, and benchmark rules. |
| `docs/WORKFLOW.md` | Detailed Local, Worktree, Git, teaching, lab, evidence, validation, and publication procedures. |
| `scripts/validate_repo.py` | Standard-library-only working-tree and ZIP validator with JSON output. |
| `templates/experiment.md` | Reproducible runtime or behaviour experiment template. |
| `templates/practice.md` | Protected predict-run-observe-explain-refactor-vary practice template. |
| `templates/project.md` | Milestone-project starter and evidence template. |
| `templates/review.md` | Closed-book review, exact weakness, and status-evidence template. |
| `templates/unit.md` | Integrated Pythonic SOLID/pattern unit note with `Physical Notebook Core`. |

## Intentionally absent

The archive does not include:

```text
.git/
.venv/
units/
projects/
LICENSE
credentials
tokens
private data
transcripts
caches
```

`units/` and `projects/` are created just in time after the bootstrap is safely merged into `main`.

## Validation

Validate the extracted repository root:

```bash
python scripts/validate_repo.py
```

Validate a generated archive and write a machine-readable report:

```bash
python scripts/validate_repo.py \
  --archive solid-design-pattern-bootstrap.zip \
  --json solid-design-pattern-bootstrap-validation.json
```

The validator checks required files, curriculum and project integrity, all five SOLID principles, all 23 GoF patterns, classifications, prerequisite existence/cycles/order, path counts and timing totals, progress parity, Python Mastery references, TOML and lock consistency, Markdown, links, templates, IDs, terminology, repository hygiene, archive layout, and archive integrity.
