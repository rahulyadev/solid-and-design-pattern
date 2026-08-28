# Start Here

This repository has a one-time setup workflow, then a simple daily topic workflow.

## One-time bootstrap: use Local

The existing GitHub repository has a small tracked `README.md`. Extracting the bootstrap ZIP replaces it and adds the remaining files.

1. Extract `solid-design-pattern-bootstrap.zip` directly into the local repository root.
2. Open the first Codex chat using the **Local** checkout, not a Worktree.
3. Paste this exact prompt:

```text
Initialize the SOLID and Design Pattern repository bootstrap locally.

Read AGENTS.md and START_HERE.md. Inspect Git status and verify that the extracted curriculum, learning paths, Python references, progress tracker, projects, templates, configuration, links, and Git workflow are valid.

Create or resume the local branch setup/solid-design-pattern-bootstrap, run python scripts/validate_repo.py, commit only the validated bootstrap files, and report the validation results and commit.

Do not push, open a pull request, merge, initialize a topic, or initialize a project. Give me the exact publication prompt when the local bootstrap is ready.
```

The bootstrap stays local until you review it.

4. Publish the reviewed bootstrap with this exact prompt:

```text
Publish the validated SOLID and Design Pattern bootstrap.

Push setup/solid-design-pattern-bootstrap, create a pull request into main, merge it after validation passes, preferably using a squash merge, and synchronize local main.

Never force-push or bypass failed checks. Stop if authentication, conflicts, branch protection, or unrelated changes require my action.
```

Do not initialize a topic or project until `main` contains the validated bootstrap baseline.

## Daily topics: use one Worktree per topic

### 1. Choose a learning path

Open [LEARNING_PATHS.md](LEARNING_PATHS.md). Start with an interview path when time is short. Paths are recommendations, not gates.

### 2. Find the topic ID

Keep one permanent curriculum-helper chat and ask naturally:

```text
Which topic should I study for Strategy pattern?
```

or:

```text
Which topic covers Dependency Injection versus Dependency Inversion?
```

The helper returns the canonical topic ID, exact title, short reason, essential prerequisites, commonly confused units, relevant [Python Mastery references](PYTHON_REFERENCES.md), repository folder state, and the exact initialization prompt. It cannot know whether another ChatGPT or Codex chat exists.

### 3. Initialize one dedicated topic chat

1. Synchronize local `main`.
2. Open a new Codex chat using **Worktree** based on that `main`.
3. Say only:

```text
Initialize <TOPIC-ID>.
```

Example:

```text
Initialize SDP-BEH-010.
```

Codex safely creates or resumes exactly `topic/<TOPIC-ID>`, generates the initial note and required starter lab, validates them, and commits them. Before pushing, it lists every commit by which the local branch is ahead of the remote branch. It automatically pushes only commits created during this initialization operation. If older local-only learning commits would also be published, it stops and asks for explicit publication authorization. If the validated initialized version is already remote, it does not push again. Initialization never creates a pull request, merges, or modifies remote `main`.

### 4. Continue naturally

In the same topic chat, ask:

```text
Explain this visually.
Show me a simpler Python version.
Why is this better than an if/elif chain?
Compare this with State.
Give me a refactoring exercise.
Review my attempt.
Quiz me.
Ask me an interview question.
```

The topic ID does not need to be repeated. Only the validated initialization commit is pushed automatically. Later notes, exercises, attempts, reviews, experiments, and corrections may be committed locally but are not pushed automatically.

### 5. Finish the topic

Keep newer changes local:

```text
I completed <TOPIC-ID>. Keep any new changes local and do not push or merge.
```

Or publish the latest changes and merge:

```text
I completed <TOPIC-ID>. Finalize it, push the latest changes, and merge the topic branch into main.
```

If you omit the publication choice, Codex asks only:

```text
Should I keep the latest changes local, or push them and merge the branch into main?
```

The initialized version already exists on its GitHub branch even when newer learning changes stay local. Keep the Worktree pinned while it has unpushed or unmerged work.

## Milestone projects

Open a new Worktree from synchronized `main` and say:

```text
Initialize project <PROJECT-ID>.
```

Project initialization uses the same exact-branch comparison and current-operation-only push protection as topic initialization. It never publishes older local-only project commits, and it does not push again when the validated initialized version is already remote.

Complete locally:

```text
I completed project <PROJECT-ID>. Keep any new changes local and do not push or merge.
```

Or publish and merge:

```text
I completed project <PROJECT-ID>. Finalize it, push the latest changes, and merge the project branch into main.
```

Project evidence never advances a curriculum-unit state automatically.

Detailed branch, divergence, validation, teaching, lab, and evidence rules are in [docs/WORKFLOW.md](docs/WORKFLOW.md).
