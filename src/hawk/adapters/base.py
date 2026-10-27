"""Base adapter interface for all backends."""

from abc import ABC, abstractmethod
from typing import Any

from ..models import FetchResponse, SearchResponse


class BaseAdapter(ABC):
    """Abstract base class for all backend adapters."""

    name: str = "base"

    @abstractmethod
    async def available(self) -> bool:
        """Check if the backend is available/installed."""
        ...

    async def search(self, query: str, **kwargs: Any) -> SearchResponse:
        """Search (optional for some backends)."""
        raise NotImplementedError(f"{self.name} does not support search")

    async def fetch(self, url: str, **kwargs: Any) -> FetchResponse:
        """Fetch and extract content from a URL (optional)."""
        raise NotImplementedError(f"{self.name} does not support fetch")
