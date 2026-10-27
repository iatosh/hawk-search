# ADR-0003: Python over Node.js

**Status:** Accepted
**Date:** 2026-10-27

## Context

hawk needs to orchestrate three backend tools via subprocess calls and HTTP.
Initially chose Node.js for startup speed and agent ecosystem fit. User
correctly pointed out that for a tool installed once and called occasionally,
startup speed differences (Python ~200ms vs Node ~50ms) are negligible against
network-bound operations that take 1-5 seconds.

## Decision

Use Python 3.12+ with uv for package management and distribution.

## Rationale

1. **Subprocess API**: Python's `subprocess.run()` is cleaner than Node's
   `child_process.exec()` for the callback-style API.
2. **HTTP client**: httpx provides a clean, modern async HTTP client.
3. **Text processing**: Python has stronger standard library and ecosystem
   for HTML parsing, regex, and markdown processing.
4. **imo-zuru integration**: imozuru is Python; Python→Python subprocess calls
   are more natural than Node→Python.
5. **Distribution**: `uv tool install` provides clean single-binary-like
   installation experience.

## Consequences

- hawk integrates more naturally with Python-based tools
- Slightly slower startup (~150ms difference, negligible in practice)
- Agent ecosystem is Node-heavy, but this is not a hard requirement

## Alternatives considered

Node.js: rejected after user pointed out startup speed argument is weak for
this use case. TypeScript ecosystem is strong but doesn't outweigh Python
advantages for this specific tool.
