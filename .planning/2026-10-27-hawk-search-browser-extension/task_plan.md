# hawk-search: Unified Agent Research Tool

**Goal:** Build a single research tool for AI agents that handles the full spectrum: quick lookup → multi-source research → deep source tracing (like imozuru's berrypicking). Cross-platform (web, social, code, video, academic).

**Status:** planning
**Next Step:** Clarify form factor (CLI? MCP server? library?) and how it relates to existing tools (wigolo, agent-reach)

## Core Insight

Three existing tools, three different depths:
- **Quick lookup:** "What's the current version of React?" → search → answer
- **Research:** "Compare React vs Vue for 2026" → multi-source → synthesized report
- **Deep tracing:** "Find where this concept originated" → berrypicking, citation chaining, author tracking, media mapping

Currently agents have to know which tool to use and how to chain them. hawk-search should abstract that into one interface.

## Design Questions

### 1. Form Factor
- **Option A: CLI tool.** `hawk search "query"`, `hawk research "question"`, `hawk trace "concept"`. Easy to integrate, scriptable.
- **Option B: MCP server.** Agent connects via MCP protocol. More structured, better for multi-turn.
- **Option C: Library.** Import into agent code. Most flexible but hardest to integrate.
- **Decision:** TBD

### 2. Relationship to Existing Tools
- **Option A: Wrapper/Orchestrator.** hawk calls wigolo/agent-reach/imozuru under the hood. Leverages existing implementations.
- **Option B: Standalone.** reimplements the necessary parts. More control, more work.
- **Option C: Hybrid.** Uses existing tools where they excel, implements new logic for the orchestration layer.
- **Decision:** TBD

### 3. Depth Abstraction
How does the agent specify depth?
- **Explicit:** `hawk search --depth quick|standard|deep`
- **Auto-detect:** hawk analyzes the query and decides
- **Progressive:** Start quick, escalate if needed
- **Decision:** TBD

### 4. Platform Abstraction
How does the agent specify platform?
- **Explicit:** `hawk search --platforms web,github,twitter`
- **Auto-detect:** hawk decides based on query type
- **Profile-based:** `hawk search --profile academic` or `--profile tech`
- **Decision:** TBD

## Phases (tentative)

### Phase 1: Interface Design
- Define CLI/MCP interface
- Design query parsing (depth, platform, intent detection)

### Phase 2: Quick Search
- Wrap existing search capabilities (wigolo search, exa, etc.)
- Fast lookup: query → top results + answer synthesis

### Phase 3: Multi-Source Research
- Question decomposition
- Parallel search across platforms
- Synthesis with source attribution
- Gap analysis

### Phase 4: Deep Tracing (imozuru-style)
- Source classification (paper/blog/tweet/video/official)
- Citation chaining (backward/forward/author)
- Media mapping (where does this field publish?)
- Termination criteria (saturation, rounds, coverage)
- Output: map, extracts, report

### Phase 5: Platform Integrations
- Web search (Exa, DuckDuckGo, etc.)
- GitHub (repos, issues, code)
- YouTube (search, subtitles)
- Reddit, Twitter/X, etc. (via agent-reach)
- Academic (OpenAlex, arXiv, DOI)

## Constraints
- Must be agent-callable (CLI or MCP)
- Should work with existing tools where possible
- Must handle the full depth spectrum
- Cross-platform is core to the vision

## Open Questions
1. CLI or MCP server or both?
2. Build on top of existing tools or standalone?
3. How to handle auth for login-walled platforms?
4. What's the output format? (JSON for machines, markdown for humans?)
