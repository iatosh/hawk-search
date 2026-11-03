# Contributing to hawk-search

hawk-search is a unified research tool for AI agents. It orchestrates three
existing tools (wigolo, agent-reach, imozuru) through a single CLI interface.

## Development Workflow

Every change goes through: **Issue → Branch → PR → Review → Merge → Release**

### 1. Find or Create an Issue

Work is tracked as GitHub issues. Every PR must close at least one issue.

**Issue types:**
- **Task**: One piece of work ending in one pull request.
- **Feature**: A group of new functionality (epic). Has no branch; each child Task branches separately.
- **Bug**: Something the tool does wrong.

**Area labels** (pick the most specific):
- `area:core` — Query parsing, intent detection, orchestrator, routing
- `area:adapters` — WigoloAdapter, AgentReachAdapter, ImozuruAdapter
- `area:cli` — CLI interface, commands, output formatting
- `area:config` — Configuration loading, defaults
- `area:docs` — README, design docs, usage guide
- `area:tests` — Unit tests, integration tests, test fixtures
- `area:dev` — CONTRIBUTING.md, AGENTS.md, CI, dev environment
- `area:release` — Versioning, packaging, PyPI

**Priority:**
- **Urgent**: Blocks all other work
- **High**: Taken next among ready issues
- **Medium**: Default
- **Low**: Backlog

**Dependencies:** Set in GitHub issue sidebar under "Blocked by", never in the issue body.

### 2. Branch

Branch from `main` only. Name format:

```
issue-<issue-number>-<slug>
```

Example: `issue-5-implement-wigolo-adapter`

### 3. Commit

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short imperative summary>

<body explaining why, if needed>
```

Types:
- `feat:` — new functionality (triggers minor version bump)
- `fix:` — bug fix (triggers patch version bump)
- `docs:` — documentation only
- `refactor:` — code change with no behavior change
- `chore:` — tooling, dependencies, CI
- `test:` — test changes

Rules:
- Summary is imperative, lowercase, no period
- Breaking changes: `feat!: ...` or add `BREAKING CHANGE:` footer
- One commit per PR is the goal (squash if needed)
- No `Co-Authored-By` trailers

### 4. Pull Request

Use the template in `.github/pull_request_template.md`. GitHub fills it in
when you open a PR.

The PR body must start with one `Closes #<issue-number>` line per issue
it closes. With `Closes #24, #25`, GitHub closes only #24, so write:

```
Closes #24
Closes #25
```

Then write the sections:
- **Summary**: what changed and why. If the PR closes several issues, write
  one line per issue.
- **Test plan**: commands run and their result
- **Impact** (optional): behavior changes, breaking changes, new dependencies
- **Design change** (optional): ADR or docs/spec files touched
- **Deviations** (optional): differences from the issue or the agreed
  design, such as scope that was added or dropped, Out of scope items that
  were touched, or decisions made during implementation (link the ADR)

Delete an optional section when it does not apply.

Design changes (new terminology, architectural decisions) must be in the
same PR as the code, not a follow-up.

### 5. Merge

Default: **squash merge**. Every PR becomes one commit on `main`.

Use a **merge commit** only when every commit in the PR stands alone.

### 6. Release

Releases happen on `main`. Version bump levels:
- **patch**: bug fix, docs, refactor
- **minor**: new feature, backward-compatible
- **major**: breaking change

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=hawk --cov-report=term-missing
```

Every PR that changes `src/hawk/` must include tests or update existing ones.

## Development Environment

```bash
# Install dependencies
pip install -e ".[dev]"

# Run the CLI during development
hawk --help
```

Install the git hooks once per clone:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

The hooks in `.pre-commit-config.yaml` check:
- **pre-commit**: `ruff check` and `ruff format --check` on staged Python files
- **commit-msg**: the summary is a Conventional Commit
- **pre-push**: the branch is `main` or `issue-<n>-<slug>`

## Code Style

- Python 3.11+ type hints required
- Line length: 100 characters
- Format: `ruff format`
- Lint: `ruff check`

```bash
# Format and lint
ruff format src/hawk/ tests/
ruff check src/hawk/ tests/
```
