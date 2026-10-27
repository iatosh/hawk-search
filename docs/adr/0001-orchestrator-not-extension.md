# ADR-0001: hawk is an orchestrator, not a browser extension

**Status:** Accepted
**Date:** 2026-10-27

## Context

Initial assumption was that hawk would be a browser extension providing search
overlays on every page. User corrected: the goal is a research tool for AI
agents that combines the capabilities of three existing tools (wigolo,
agent-reach, imozuru).

## Decision

hawk is a CLI tool (orchestrator) that:
- Takes a research query from an agent or user
- Parses the query to determine intent and depth
- Routes to the appropriate backend tool(s)
- Synthesizes and returns results

## Consequences

- hawk has no UI of its own (CLI only)
- hawk depends on wigolo, agent-reach, and imozuru being installed
- hawk's value is in orchestration, not in providing search capability itself
- Agents call hawk like any other CLI tool: `hawk search "query"`
