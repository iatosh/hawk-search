# Issue #18: Implement latency optimizations

**Status:** Open
**Priority:** Medium
**Labels:** performance, optimization

## Description

Implement the latency optimization strategies identified in the design:

### 1. Persistent MCP Server
- Wigolo MCP server is started once when hawk starts
- Reused across all calls during hawk's execution
- Avoids subprocess spawn overhead for each search
- Configuration: `wigolo.mode: "persistent"` (default) or `"spawn-per-call"`

### 2. Parallel Fan-Out
- Multi-platform searches run in parallel using asyncio
- Takes time of slowest platform, not sum of all
- Implement in orchestrator

### 3. Streaming Results
- Results displayed as they arrive (not after all complete)
- `--stream` flag on search/research commands
- Progress indicators for long-running operations

### 4. Cache Hit Fast Path
- Quick searches use `search_depth="ultra-fast"` which checks wigolo cache first
- Cache hits return in ≤50ms (no network I/O)
- Cache is disk-based (SQLite), persists across hawk invocations

## Acceptance Criteria
- Quick web search with cache hit completes in ≤50ms
- 3-platform search is ~3x faster than sequential (parallel fan-out working)
- Streaming output shows results as they arrive
- `hawk doctor` reports backend availability and latency

## Notes
- Detailed design to be completed (see TODO #25)
- Depends on: Issue #5 (WigoloAdapter persistent mode), Issue #10 (orchestrator)
