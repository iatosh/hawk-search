# ADR-0006: Latency optimization strategies

**Status:** Accepted
**Date:** 2026-07-09

## Context

hawk-search is a wrapper tool that orchestrates multiple backend tools (wigolo, agent-reach, imozuru). Each call to a backend involves spawning a subprocess, which adds overhead. For a research tool that may make many calls in quick succession, this overhead can become significant. We need strategies to minimize latency while maintaining the simplicity of the wrapper architecture.

## Decision

We will implement three latency optimization strategies:

### 1. Persistent MCP Server (within hawk session)

**Decision:** hawk spawns the wigolo MCP server once when hawk starts and reuses it across all calls within the same hawk session. When hawk exits, the wigolo server is terminated.

```python
class HawkSession:
    def __init__(self):
        # Spawn wigolo MCP server once
        self.wigolo = subprocess.Popen(
            ["wigolo", "serve"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
    
    def search(self, query):
        # Reuse the running server
        msg = mcp_encode("search", {"query": query})
        self.wigolo.stdin.write(msg)
        return mcp_decode(self.wigolo.stdout.readline())
    
    def cleanup(self):
        self.wigolo.terminate()
```

**Rationale:**
- Simple to implement (no daemon management)
- Eliminates spawn overhead for multiple calls within one hawk session
- Clean resource cleanup when hawk exits
- If spawn overhead across separate hawk invocations becomes a problem, we can migrate to a daemon-based approach (Option B) later

**Trade-off:** Spawn overhead still exists when running separate `hawk` commands in a shell (each is a separate session). This is acceptable for the initial implementation.

### 2. Parallel Fan-Out with Bounded Concurrency

**Decision:** Multi-platform searches run in parallel using asyncio, with a maximum of 3 concurrent searches controlled by `asyncio.Semaphore(3)`.

```python
async def fan_out_search(query):
    semaphore = asyncio.Semaphore(3)
    
    async def bounded_search(platform, adapter):
        async with semaphore:
            return await adapter.search(platform, query.query)
    
    tasks = []
    for platform in query.platforms:
        adapter = get_adapter(platform)
        tasks.append(bounded_search(platform, adapter))
    
    results = await asyncio.gather(*tasks)
    return synthesize(results)
```

**Rationale:**
- Takes time of the slowest platform, not the sum of all
- Bounded concurrency (max 3) prevents overwhelming backends with too many simultaneous requests
- Protects against rate limiting on platform APIs

**Trade-off:** Searches for 4+ platforms will be slower than fully parallel, but this is acceptable to protect backend resources.

### 3. Streaming Results (Arrival Order)

**Decision:** Results are displayed as they arrive, in arrival order (not grouped by platform). A `--grouped` flag is provided for users who prefer results grouped by platform.

```bash
# Default: arrival order
$ hawk search "react" --platforms web,github --stream
[web] React 19 release notes...
[web] React hooks tutorial...
[github] facebook/react repo...
[web] Next.js documentation...

# Grouped mode
$ hawk search "react" --platforms web,github --stream --grouped
[web]
React 19 release notes...
React hooks tutorial...
Next.js documentation...
[github]
facebook/react repo...
```

**Rationale:**
- Arrival order provides the fastest perceived response time
- Users see the first result as soon as it's available
- Grouped mode is available for users who prefer organized output

**Trade-off:** Default output may appear less organized, but speed is prioritized.

## Expected Performance Gains

| Scenario | Before optimization | After optimization |
|----------|-------------------|-------------------|
| Quick web search (cache hit) | ~150ms (spawn + cache) | ~50ms (no spawn, cache) |
| 3-platform search | ~1.5s (sequential) | ~500ms (parallel, max=3) |
| 10 searches in one session | ~1.5s (10 spawns) | ~500ms (1 spawn) |

## Alternatives Considered

- **Daemon-based MCP server (Option B):** A persistent daemon that survives across hawk invocations. More complex to implement (requires daemon management, recovery from crashes, multi-user considerations). Deferred to future if needed.
- **Fully parallel fan-out (no bound):** Maximum speed but risks overwhelming backends and hitting rate limits.
- **Grouped streaming by default:** More organized but slower perceived response time.

## Consequences

### Positive
- Significant latency reduction for common use cases
- Simple implementation that doesn't require changes to backend tools
- Progressive enhancement (can add daemon mode later if needed)

### Negative
- Spawn overhead still exists across separate hawk shell invocations
- Parallel searches use more CPU/memory temporarily
- Streaming output may appear less organized (mitigated by --grouped flag)
