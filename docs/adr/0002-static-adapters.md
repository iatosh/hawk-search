# ADR-0002: Static adapter approach (assume fixed backend versions)

**Status:** Accepted
**Date:** 2026-10-27

## Context

wigolo, agent-reach, and imozuru are actively maintained tools that may change
their CLI interfaces, output formats, and MCP schemas over time. hawk needs to
decide how to handle this.

Options:
1. Dynamic adapter — inspect backend capabilities at startup, adapt routing
2. Static adapter — pin to known versions, update adapter code when backends change

## Decision

Use static adapters with version pinning. Each adapter specifies which
backend version(s) it supports. `hawk doctor` checks installed versions and
warns on mismatch.

## Consequences

- Simpler implementation (no runtime introspection)
- More maintenance burden (must update adapters when backends change)
- Predictable behavior (no surprises from backend changes)
- hawk doctor provides clear upgrade guidance

## Alternatives considered

Dynamic adapter: rejected because it adds complexity and makes behavior
harder to predict/test. The three backends are relatively stable and we
can accept the maintenance cost.
