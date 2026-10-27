# Issue #5: Implement WigoloAdapter (MCP client)

**Status:** Open
**Priority:** High
**Labels:** adapter, mcp

## Description

Create the WigoloAdapter class that communicates with the wigolo MCP server over stdio.

The MCP server is started in **persistent mode**: it's spawned once when hawk starts and reused across all calls. This minimizes latency by avoiding process spawn overhead for each search request.

The adapter needs to handle MCP message framing (JSON-RPC 2.0 with Content-Length headers).

### Persistent Mode

```python
# Started once at hawk initialization
self.wigolo_process = subprocess.Popen(
    ["node", wigolo_path, "serve"],
    stdin=PIPE, stdout=PIPE
)

# Reused for all subsequent calls
self.wigolo_process.stdin.write(json.dumps(mcp_request).encode())
```

This is the default mode. A "spawn-per-call" mode can be configured for debugging or special cases.

### Methods to implement
- `search(query, max_results, search_depth)` 
- `fetch(url, timeout)`
- `crawl(url, strategy, max_pages)`
- `extract(url, schema)`
- `find_similar(url, topic)`
- `cache(action, ...)`
- `watch(action, ...)`
- `research(question, depth)`

## Acceptance Criteria
- Can send MCP requests to wigolo server and parse responses
- Persistent mode: server started once, reused across calls
- Handles MCP error responses gracefully
- Unit tests mock the subprocess communication
