"""Data models for hawk-search."""

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str = ""
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResponse:
    query: str
    results: list[SearchResult] = field(default_factory=list)
    total_time_ms: int = 0
    engine: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FetchResponse:
    url: str
    title: str = ""
    markdown: str = ""
    links: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str = ""


Intent = Literal["lookup", "compare", "trace", "watch"]
Depth = Literal["quick", "standard", "comprehensive", "deep"]
Platform = Literal[
    "web", "github", "twitter", "reddit", "youtube",
    "bilibili", "xiaohongshu", "facebook", "instagram",
    "v2ex", "xueqiu", "linkedin", "rss", "academic",
]


@dataclass
class ParsedQuery:
    intent: Intent
    depth: Depth
    platforms: list[Platform]
    query: str
