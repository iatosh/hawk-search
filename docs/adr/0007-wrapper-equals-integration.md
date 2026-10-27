# ADR-0007: Wrapper approach achieves integration functionality

**Status:** Accepted
**Date:** 2026-07-09

## Context

When designing hawk-search, we considered three architectural approaches:

- **Option A:** Extend imozuru with lightweight mode and platform access
- **Option B:** Create a new wrapper tool (hawk) that orchestrates existing tools
- **Option C:** Integrate all functionality into wigolo (single monolithic tool)

The user's requirement was that the underlying tools (wigolo, agent-reach, imozuru) would continue to evolve independently, and hawk should be able to adapt to their updates without requiring changes to the tools themselves.

## Decision

We chose **Option B** (wrapper tool) because:

1. It doesn't require changes to the underlying tools
2. It can adapt to new features/changes in the underlying tools without modifying them
3. It provides a stable interface for the user while the underlying tools change

A key question was whether the wrapper approach (B) could achieve the same functionality as full integration (C). The answer is **yes**, with proper design.

## Analysis

### What a wrapper can do

A wrapper tool can:
- Parse queries and route to appropriate backends
- Orchestrate multiple tools in sequence or parallel
- Combine and synthesize results from multiple tools
- Provide a unified CLI/MCP interface
- Adapt to backend API changes (by updating the wrapper, not the backends)

### What requires design attention

Three areas that might seem like limitations of the wrapper approach are actually solvable with proper design:

#### 1. Transparent cache sharing

**Concern:** Each wrapper invocation spawns a new backend process, potentially losing cache benefits.

**Solution:** Backend caches are disk-based (e.g., wigolo uses SQLite at `~/.wigolo/wigolo.db`). Each time the wrapper spawns the backend, it opens the same cache database. The cache is transparently shared across wrapper invocations without any special design.

#### 2. State sharing

**Concern:** In-memory state (e.g., research progress) cannot be shared across process boundaries.

**Solution:** Use file-based state management. imozuru already uses files (map.md, sources.jsonl, fetch-log.jsonl) to track research state. The wrapper reads and writes these files to track state across invocations. For in-memory state during an active run, the wrapper communicates via subprocess stdin/stdout.

#### 3. Real-time feedback

**Concern:** Streaming progress updates from subprocesses is complex.

**Solution:** Use subprocess streaming (read stdout line-by-line) or MCP progress notifications. Both are well-established patterns.

### Functional equivalence

| Capability | Integration (C) | Wrapper (B) |
|-----------|----------------|-------------|
| Unified interface | ✓ | ✓ |
| Multi-tool orchestration | ✓ | ✓ |
| Cache utilization | ✓ (in-process) | ✓ (disk-based) |
| State tracking | ✓ (in-memory) | ✓ (file-based) |
| Real-time feedback | ✓ | ✓ (streaming) |
| Independent backend updates | ✗ (requires re-integration) | ✓ (wrapper adapts) |

## Consequences

### Positive
- Each underlying tool evolves independently
- Wrapper can be updated without touching backends
- Users can still use underlying tools directly
- Clear separation of concerns

### Negative
- Slight overhead from subprocess spawning (typically <10ms, negligible)
- Cannot share in-memory state (mitigated by file-based state)
- Requires careful adapter design to handle backend API changes

## Conclusion

The wrapper approach (Option B) is functionally equivalent to full integration (Option C) for the purposes of hawk-search, with the additional benefit of allowing underlying tools to evolve independently. The three potential limitations (cache sharing, state sharing, real-time feedback) are all solvable with proper design patterns that are already used by the underlying tools.
