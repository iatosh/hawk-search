# AI Agent Guidelines

These rules apply to all AI coding agents working in this repository.

## Before You Start

1. Read `CONTRIBUTING.md` for the development workflow.
2. Read `docs/design.md` for the architecture.
3. Check the issue tracker for the issue you're working on.

## Issue Workflow

When you complete an issue:
1. Verify all "Done when" checkboxes are actually true in the code.
2. Check that "Out of scope" items were not touched.
3. Run the full test suite (`pytest`).
4. Run linter (`ruff check src/hawk/ tests/`).
5. Run formatter (`ruff format src/hawk/ tests/`).
6. Create a branch named `issue-<number>-<slug>`.
7. Commit with a conventional commit message.
8. Open a PR with `Closes #<issue-number>` as the first line.

## What NOT to Do

- **Do not skip tests.** Every change to `src/hawk/` needs test coverage.
- **Do not break backward compatibility** without a `feat!:` commit or a breaking change issue.
- **Do not merge PRs yourself.** Create the PR and wait for human review.
- **Do not release versions** without explicit user instruction.
- **Do not modify `docs/design.md`** without a design discussion issue.
- **Do not change adapter interfaces** (`src/hawk/adapters/base.py`) without updating all adapters.

## Testing Requirements

Before considering a task complete:

```bash
# All tests must pass
pytest

# No lint errors
ruff check src/hawk/ tests/

# Code is formatted
ruff format --check src/hawk/ tests/
```

## Error Handling Rules

hawk is an orchestrator — it must handle partial failures gracefully:

1. If one backend is unavailable, try the next.
2. Never silently return empty results — always report which backends were tried.
3. Timeouts must be reasonable (default 30s for search, 60s for fetch).
4. Errors must include enough context for debugging (which backend, which operation, what failed).

## Security Rules

- Never log credentials or authentication tokens.
- Validate URLs before fetching (SSRF protection).
- Use timeouts for all network operations.
- Do not execute arbitrary code from fetched content.
