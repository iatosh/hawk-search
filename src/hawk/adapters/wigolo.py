"""Wigolo adapter — communicates with wigolo via MCP over stdio."""

import asyncio
import json
import logging
from typing import Any

from ..models import SearchResult, SearchResponse
from .base import BaseAdapter

logger = logging.getLogger(__name__)


class WigoloAdapter(BaseAdapter):
    name = "wigolo"

    def __init__(self, binary: str = "wigolo"):
        self.binary = binary
        self._process: asyncio.subprocess.Process | None = None
        self._request_id = 0

    async def available(self) -> bool:
        try:
            proc = await asyncio.create_subprocess_exec(
                self.binary, "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await asyncio.wait_for(proc.wait(), timeout=5)
            return proc.returncode == 0
        except (FileNotFoundError, asyncio.TimeoutError):
            return False

    async def _start(self) -> None:
        """Start the wigolo MCP server."""
        if self._process and self._process.returncode is None:
            return
        self._process = await asyncio.create_subprocess_exec(
            self.binary,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await self._initialize()

    async def _initialize(self) -> None:
        """Send MCP initialize handshake."""
        msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "hawk-search", "version": "0.1.0"},
            },
        }
        await self._send(msg)
        # Read until we get the response for id=1
        while True:
            resp = await self._recv()
            if resp and resp.get("id") == 1:
                if "error" in resp:
                    raise RuntimeError(f"MCP initialize error: {resp['error']}")
                break

    async def _send(self, msg: dict[str, Any]) -> None:
        if not self._process or not self._process.stdin:
            raise RuntimeError("MCP process not started")
        line = json.dumps(msg)
        self._process.stdin.write(f"{line}\n".encode())
        await self._process.stdin.drain()

    async def _recv(self) -> dict[str, Any] | None:
        if not self._process or not self._process.stdout:
            return None
        line = await asyncio.wait_for(self._process.stdout.readline(), timeout=30)
        if not line:
            return None
        try:
            return json.loads(line.decode().strip())
        except json.JSONDecodeError:
            return None

    async def _call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        self._request_id += 1
        msg = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }
        await self._send(msg)
        # Read until we get the response for our request id
        while True:
            resp = await self._recv()
            if resp and resp.get("id") == self._request_id:
                if "error" in resp:
                    raise RuntimeError(f"MCP error: {resp['error']}")
                return resp.get("result")

    async def search(self, query: str, **kwargs: Any) -> SearchResponse:
        """Search via wigolo's search tool."""
        await self._start()
        result = await self._call_tool("search", {
            "query": query,
            "search_depth": kwargs.get("depth", "quick"),
        })
        # Parse the MCP response: result.content is an array of content items
        # Each item has type and text. The text is the JSON result from wigolo.
        content = result.get("content", []) if result else []
        # Find the first text content item
        text_content = None
        for item in content:
            if item.get("type") == "text":
                text_content = item.get("text", "")
                break
        if not text_content:
            return SearchResponse(query=query, results=[], engine="wigolo")
        # Parse the JSON result
        try:
            data = json.loads(text_content)
        except json.JSONDecodeError:
            # If not valid JSON, treat the whole text as a single result
            return SearchResponse(
                query=query,
                results=[SearchResult(
                    title=text_content[:100],
                    url="",
                    snippet=text_content[:200],
                    source="wigolo",
                )],
                engine="wigolo",
            )
        # data should have a "results" array
        results = []
        for item in data.get("results", []):
            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("snippet", ""),
                source="wigolo",
                metadata={
                    "relevance_score": item.get("relevance_score"),
                    "evidence_score": item.get("evidence_score"),
                },
            ))
        return SearchResponse(
            query=query,
            results=results,
            engine="wigolo",
            metadata={"total": len(results)},
        )

    async def close(self) -> None:
        """Shut down the MCP process."""
        if self._process and self._process.returncode is None:
            self._process.terminate()
            try:
                await asyncio.wait_for(self._process.wait(), timeout=5)
            except asyncio.TimeoutError:
                self._process.kill()
