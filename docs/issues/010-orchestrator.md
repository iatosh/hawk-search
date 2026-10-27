# Issue #10: Implement orchestrator

**Status:** Open
**Priority:** High
**Labels:** core, orchestration

## Description

Create the orchestrator that routes parsed queries to the appropriate adapter(s) and coordinates multi-tool workflows.

### Routing Logic
```python
def route(query):
    if query.intent == "lookup" and query.depth == "quick":
        if query.platforms == ["web"]:
            return wigolo.search(query.query, depth="ultra-fast")
        else:
            return fan_out_search(query)  # parallel across platforms
    elif query.intent in ("lookup", "compare"):
        return orchestrate_research(query)
    elif query.intent == "trace":
        return orchestrate_tracing(query)
```

### Parallel Fan-Out
When searching across multiple platforms, all searches run in parallel using asyncio:
```python
async def fan_out_search(query):
    tasks = []
    if "web" in query.platforms:
        tasks.append(wigolo.search(query.query))
    if "github" in query.platforms:
        tasks.append(agent_reach.search("github", query.query))
    # ... more platforms
    results = await asyncio.gather(*tasks)
    return synthesize(results)
```

### Streaming Results
For long-running operations, results should be streamed as they arrive:
```bash
$ hawk search "react" --platforms web,github --stream
[web] React 19 release notes...       ← displayed as soon as web results arrive
[github] facebook/react repo...       ← displayed as soon as github results arrive
```

### Deep Research Coordination
- Manage multi-round imozuru workflows
- Termination criteria: rounds reached, saturation, barriers
- Progress reporting between rounds

## Acceptance Criteria
- Correctly routes queries based on intent and depth
- Multi-platform searches run in parallel (not sequential)
- Streaming output for long-running operations
- Graceful error handling when a backend fails
- Unit tests with mocked adapters
