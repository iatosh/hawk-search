"""Query parser — determines intent, depth, and platforms from user input."""

from ..models import Depth, Intent, ParsedQuery, Platform


class QueryParser:
    def parse(self, text: str, depth: Depth | None = None) -> ParsedQuery:
        """Parse a user query into intent, depth, platforms, and query string."""
        intent = self._detect_intent(text)
        if depth is None:
            depth = self._default_depth(intent)
        platforms = self._detect_platforms(text)
        if not platforms:
            platforms = ["web"]
        return ParsedQuery(
            intent=intent,
            depth=depth,
            platforms=platforms,
            query=text,
        )

    def _detect_intent(self, text: str) -> Intent:
        lower = text.lower()
        if " vs " in lower or " versus " in lower:
            return "compare"
        if any(kw in lower for kw in ["origins", "where did", "first proposed", "history of"]):
            return "trace"
        if any(kw in lower for kw in ["watch", "monitor"]):
            return "watch"
        return "lookup"

    def _default_depth(self, intent: Intent) -> Depth:
        if intent == "lookup":
            return "quick"
        if intent == "trace":
            return "deep"
        return "standard"

    def _detect_platforms(self, text: str) -> list[Platform]:
        lower = text.lower()
        platforms: list[Platform] = []
        if "github" in lower:
            platforms.append("github")
        if "twitter" in lower or "x.com" in lower:
            platforms.append("twitter")
        if "reddit" in lower:
            platforms.append("reddit")
        if "youtube" in lower:
            platforms.append("youtube")
        return platforms
