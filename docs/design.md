# hawk-search Design Document

## Overview

hawk-search is a unified research tool for AI agents that provides three research depths through a single interface:

1. **Quick Search** — Fast lookup across web and platforms
2. **Multi-Source Research** — Question decomposition, parallel search, synthesis with citations
3. **Deep Tracing** — Berrypicking-style source tracing (imozuru methodology): citation chaining, author tracking, media mapping, saturation-based termination

hawk is an **orchestrator** that delegates to three existing tools:
- **wigolo** — Local-first web intelligence (search, fetch, crawl, extract, cache, watch)
- **agent-reach** — Multi-platform access (15 platforms: social, dev, video, career)
- **imozuru** — Deep research scripts (fetch with OCR, citation chaining, report generation)

## Architecture

```
Agent
  ↓ calls "hawk search/research/trace ..."
hawk CLI (Python)
  ↓ parses query → intent, depth, platforms
Orchestrator
  ↓ routes to appropriate adapter(s)
┌─────────────┐  ┌──────────────────┐  ┌─────────────────┐
│ WigoloAdapter│  │AgentReachAdapter │  │ ImozuruAdapter  │
│ (MCP client)│  │ (subprocess)     │  │ (subprocess)    │
└──────┬──────┘  └────────┬─────────┘  └────────┬────────┘
       ↓                   ↓                     ↓
wigolo MCP server    agent-reach CLI      imozuru scripts
(node process)       (Python CLI)         (Python scripts)
       ↓                   ↓                     ↓
   Web/Docs          Platforms               PDFs/OpenAlex/RSS
```

## CLI Commands

```bash
# Quick lookup
hawk search "react version"
hawk search "react hooks" --platforms web,github
hawk search "latest AI news" --depth quick --platforms web,twitter

# Multi-source research
hawk research "best state management for React 2026"
hawk research "PostgreSQL vs SQLite for mobile" --depth comprehensive
hawk research "Rust vs Go for web servers" --platforms web,github,reddit

# Deep tracing (imozuru-style)
hawk trace "attention mechanism origins"
hawk trace "btrfs filesystem design decisions" --rounds 3
hawk trace "who first proposed transformers" --output map,report

# Watch pages
hawk watch add "https://react.dev/blog" --interval 3600
hawk watch list
hawk watch check
hawk watch remove <id>

# Manage research sessions
hawk sessions list
hawk sessions show <id>
hawk sessions export <id> --format markdown

# Check environment
hawk doctor

# Check/install dependencies
hawk setup --check
hawk setup --install
```

## Adapter Layer

hawk uses **static adapters** — each adapter is a Python class that knows how to call one specific backend tool with its current API.

### WigoloAdapter
- **Protocol:** MCP (Model Context Protocol) over stdio
- **Connection:** `subprocess.Popen(["node", wigolo_path, "serve"], stdin=PIPE, stdout=PIPE)`
- **Tools wrapped:** search, fetch, crawl, extract, research, agent, diff, watch, cache, find_similar
- **Best for:** Web search (ML-reranked), page fetching (JS rendering), structured extraction, comprehensive research, page watching

### AgentReachAdapter
- **Protocol:** subprocess (CLI)
- **Command pattern:** `agent-reach <platform> <action> [args...]`
- **Platforms:** web, github, twitter, reddit, youtube, bilibili, xiaohongshu, facebook, instagram, v2ex, xueqiu, linkedin, rss
- **Best for:** Platform-specific searches (GitHub repos, Twitter posts, Reddit threads), video subtitles, RSS feeds

### ImozuruAdapter
- **Protocol:** subprocess (Python scripts)
- **Scripts wrapped:**
  - `fetch.py <sources_dir> <name> <url>` — Download with PDF/OCR/YouTube support
  - `chain.py refs|cites|author` — Citation chaining via OpenAlex
  - `watch.py add|list|check` — RSS monitoring
  - `report.py` — Generate extracted quotes page
  - `digest.py` — Generate detailed research report
- **Best for:** Academic citation tracing, PDF handling (OCR, layout), deep research report generation

## Query Parsing

hawk parses the user's query to determine:

| Field | Type | Values | Default |
|-------|------|--------|---------|
| `intent` | enum | `lookup`, `compare`, `trace`, `watch` | `lookup` |
| `depth` | enum | `quick`, `standard`, `comprehensive`, `deep` | `quick` |
| `platforms` | list[str] | `web`, `github`, `twitter`, `reddit`, `youtube`, `academic`, ... | `[web]` |
| `query` | str | The actual search term/question | required |

### Intent Detection (heuristics)
- "compare X vs Y" → `compare`
- "origins of X" / "where did X come from" / "first proposed X" → `trace`
- "watch X" / "monitor X" → `watch`
- Everything else → `lookup`

### Depth by Command
- `hawk search` → `quick` (override with `--depth`)
- `hawk research` → `standard` (override with `--depth`)
- `hawk trace` → `deep` (always)

## Orchestrator Routing

```python
def route(query: ParsedQuery):
    if query.intent == "lookup" and query.depth == "quick":
        # Fast path: direct search, no orchestration overhead
        if query.platforms == ["web"]:
            return wigolo.search(query.query, search_depth="ultra-fast")
        else:
            # Fan out to platform-specific adapters
            return fan_out_search(query)

    elif query.intent in ("lookup", "compare") and query.depth in ("standard", "comprehensive"):
        # Multi-source research
        return orchestrate_research(query)

    elif query.intent == "trace" or query.depth == "deep":
        # Deep tracing with imozuru workflow
        return orchestrate_tracing(query)
```

### Multi-Source Research Flow
1. Decompose question into sub-queries (via wigolo research or simple heuristics)
2. For each sub-query, pick the best platform(s):
   - Code-related → github
   - Discussion → reddit, twitter
   - General → web (wigolo)
   - Academic → academic (wigolo + openalex)
3. Search in parallel
4. Fetch and extract content from top results
5. Synthesize with cross-referencing and gap analysis
6. Return structured brief with citations

### Deep Tracing Flow (imozuru-style)
1. Create topic directory and map.md
2. **Round 0:** Identify terms, people, media, canonical sources
   - Search in 2 different ways (e.g., English + Japanese)
   - Build map.md with findings
3. **Each round:**
   - Pick highest-value clue to follow
   - Fetch source (imozuru fetch.py for PDF/quality)
   - Trace links: backward (references), forward (citations), author
   - Update map.md with new findings
4. **Termination check:**
   - All research points have sources → stop
   - Saturation: 70%+ of findings already known → stop
   - 4 rounds → stop
   - Login/paywall barrier → stop and report
5. Generate outputs:
   - map.md (knowledge map)
   - report.html (extracted quotes)
   - digest.html (detailed report with Lv1/2/3 explanations)

## Configuration

`~/.hawk/config.yaml`:

```yaml
# Tool connection settings
wigolo:
  binary: "wigolo"          # path to wigolo binary or "auto"
  endpoint: "http://localhost:3000"  # or "auto" to start it
  enabled: true

agent_reach:
  binary: "agent-reach"     # path to agent-reach binary
  enabled: true

imozuru:
  scripts_dir: "~/.agents/skills/imozuru/scripts"
  research_dir: "~/research"
  enabled: true

# Default behavior
defaults:
  search_depth: "quick"
  platforms: ["web"]
  output_format: "rich"     # rich | plain | json
```

## Error Handling

- Backend unavailable → fall back to next available backend, or clear error message
- Search timeout → partial results with warning
- All backends fail → structured error with diagnosis hints
- Never silently return empty results

## Output Formats

- **rich (default):** Formatted with rich library (colors, tables)
- **plain:** Plain text for piping
- **json:** Structured JSON for programmatic use

```bash
hawk search "react" --output json | jq '.results[].title'
```

## Update Strategy

hawk adapters are **static** — they assume a specific version of each backend tool.

When a backend tool updates:
1. If the API is backward-compatible → hawk continues to work
2. If the API changes → update the corresponding adapter in hawk
3. An agent can review the tool's changelog and update hawk's adapter accordingly

Version tracking in `config.yaml`:
```yaml
tested_with:
  wigolo: "0.1.43-beta.2"
  agent_reach: "1.2"
  imozuru: "current"
```

## File Structure

```
hawk-search/
├── pyproject.toml
├── src/hawk/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point (typer)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py       # Configuration loading
│   │   ├── parser.py       # Query parsing and intent detection
│   │   └── orchestrator.py # Routing and flow orchestration
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base.py         # BaseAdapter ABC
│   │   ├── wigolo.py       # Wigolo MCP adapter
│   │   ├── agent_reach.py  # Agent-reach CLI adapter
│   │   └── imozuru.py      # Imozuru scripts adapter
│   └── models.py           # Data models (SearchResult, etc.)
├── tests/
└── docs/
    ├── design.md           # This file
    └── architecture.md     # Mermaid diagrams
```
