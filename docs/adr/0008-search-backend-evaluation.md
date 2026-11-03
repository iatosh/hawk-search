# ADR-0008: Evaluate RustXNG before adoption; do not adopt TinyFish

**Status:** Accepted
**Date:** 2026-11-03

## Context

Two possible alternatives or additions to wigolo for web search came up:

- **TinyFish** — a cloud SaaS (search, fetch, browser, agent). Search and
  fetch are free but need an API key and are rate-limited (search 30 req/min,
  fetch 150 URLs/min).
- **RustXNG** (`sahenjp/RustXNG`) — a self-hosted metasearch engine written in
  Rust and based on SearXNG (AGPL-3.0). It has a JSON API and an MCP server
  (`search`, `read_page`). It was created on 2026-10-18.

Neither one covers wigolo's full scope (crawl, extract, cache, watch,
find_similar, research), so neither can replace wigolo as a whole.

## Decision

1. **Do not adopt TinyFish.** The rate limits are too tight for a research
   tool that fans out many queries. Being cloud-only and needing an API key
   also goes against the local-first, key-free direction set in ADR-0005.
2. **Benchmark RustXNG against wigolo before deciding whether to adopt it.**
   Adoption is decided only after the comparison. The options are:
   - A: use RustXNG as wigolo's SearXNG backend (`WIGOLO_SEARCH=hybrid`,
     `WIGOLO_SEARXNG_URL`), with no hawk code change
   - B: add a dedicated `RustXNGAdapter` to hawk
   - C: do not adopt
3. wigolo stays the primary backend whatever the outcome.

## Evaluation plan

- Configurations: wigolo `core`, wigolo `hybrid` with RustXNG behind it,
  and RustXNG `/search?format=json` called directly.
- About 30 queries across 5 categories: general Japanese, general English,
  technical docs, recent news, and niche/academic.
- Metrics: hit@5 against gold URLs or gold domains decided in advance,
  latency (p50/p95, cold and warm), failure rate, and response size.
- Pin the RustXNG version (v0.27.0) and record its settings. Run wigolo
  with the cache bypassed.

## Outcome (2026-11-03)

**RustXNG is not adopted (option C).** No re-evaluation is scheduled.
The full results and the benchmark code are in
[#23](https://github.com/iatosh/hawk-search/issues/23). The raw data is not
committed.

| config | hit@5 | p50 | p95 | Japanese hit@5 |
|---|---|---|---|---|
| wigolo `core` | 0.83 | 1.3 s | 1.6 s | 4/6 |
| RustXNG direct (B) | 0.77 | 1.7 s | 3.0 s | 3/6 |
| wigolo + RustXNG (A) | 0.10 | 19 s | 29 s | 0/6 |

- B is comparable to wigolo `core` or slightly worse: weaker on Japanese
  and slower. Using both adds only one hit (25/30 to 26/30).
- A cannot be used. wigolo's legacy `searxng` pipeline expands each query
  into 5 variants by appending English words (` tutorial`, ` guide`, …), even
  to Japanese queries. Relevance collapses and upstream load goes up 5×.
- That 5× load is the likely reason DuckDuckGo and other engines started
  returning CAPTCHAs during the run. Any future benchmark through wigolo's
  `searxng` mode must count the expanded queries when it sets rate limits.
- Adapter bugs found along the way: #24, #25, #26.

## Known risks

- RustXNG disabled Yahoo! JAPAN and Mojeek by default on 2026-11-03, after
  a review of their terms of use. Its earlier benchmark wins came mostly from
  Yahoo! JAPAN (189/254), so those numbers do not hold for the current
  defaults. Japanese queries are likely to be weaker.
- RustXNG is about two weeks old and its defaults change quickly, so results
  may not stay valid for long.
- It has not been confirmed that RustXNG's API matches what wigolo expects
  from a SearXNG backend. If it does not, option A is dropped.
- Both wigolo `core` and RustXNG query upstream search engines directly, so
  terms-of-use concerns apply to both, not only to RustXNG.

## Alternatives considered

- Replacing wigolo with TinyFish or RustXNG: rejected, because neither covers
  wigolo's feature set.
- Adopting RustXNG without measurement: rejected, because its advertised
  performance came from an engine configuration that is no longer the default.
