"""Orchestrator — routes queries to the appropriate backend adapter."""

import asyncio
import logging
import time

from ..adapters.base import BaseAdapter
from ..models import ParsedQuery, SearchResponse
from ..adapters.wigolo import WigoloAdapter

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, adapters: list[BaseAdapter] | None = None):
        if adapters is None:
            adapters = [WigoloAdapter()]
        self.adapters = adapters

    async def search(self, parsed: ParsedQuery) -> SearchResponse:
        """Execute a search using the appropriate adapter(s)."""
        start = time.time()
        # For MVP: use the first available adapter that supports search
        for adapter in self.adapters:
            if not await adapter.available():
                logger.warning(f"Adapter {adapter.name} not available, skipping")
                continue
            if not hasattr(adapter, "search"):
                continue
            try:
                logger.info(f"Searching via {adapter.name}: {parsed.query}")
                response = await adapter.search(parsed.query)
                response.total_time_ms = int((time.time() - start) * 1000)
                response.query = parsed.query
                return response
            except Exception as e:
                logger.error(f"Search via {adapter.name} failed: {e}")
                continue
        raise RuntimeError("No available adapters could complete the search")

    async def close(self) -> None:
        """Close all adapters."""
        for adapter in self.adapters:
            if hasattr(adapter, "close"):
                await adapter.close()
