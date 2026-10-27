# ADR-0004: Vertical slice before horizontal completeness

**Status:** Accepted
**Date:** 2026-10-27

## Context

The full hawk design includes 4 commands (search, research, trace, watch),
3 adapters (wigolo, agent-reach, imozuru), and numerous features. Building
everything at once risks never getting a working system.

## Decision

Build a minimal end-to-end vertical slice first:
- `hawk search "query"` command only
- WigoloAdapter only (the most critical backend)
- Basic query parsing (intent detection, platform detection)
- Basic output formatting

Then iterate: add imozuru, then agent-reach, then research/trace/watch commands.

## Rationale

- Proves the core architecture works (subprocess → adapter → orchestrator → CLI)
- Provides immediate value to users
- Reveals integration issues early
- Each iteration adds measurable value

## Consequences

- Initial hawk has limited functionality (wigolo search only)
- Users can see progress and provide feedback early
- Reduces risk of building the wrong thing at scale
