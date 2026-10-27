"""hawk-search CLI entry point."""

import asyncio
import sys

import typer

from .core.orchestrator import Orchestrator
from .core.parser import QueryParser

app = typer.Typer(
    name="hawk",
    help="Unified agent research tool: search, research, trace",
)


@app.command()
def search(
    query: str,
    depth: str = typer.Option("quick", help="Search depth: quick, standard, comprehensive"),
):
    """Quick search across web and platforms."""
    parser = QueryParser()
    parsed = parser.parse(query, depth=depth)  # type: ignore[arg-type]

    async def run():
        orchestrator = Orchestrator()
        try:
            response = await orchestrator.search(parsed)
            _print_results(response)
        except Exception as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1)
        finally:
            await orchestrator.close()

    asyncio.run(run())


@app.command()
def research(query: str, depth: str = typer.Option("standard", help="Research depth")):
    """Deep research with multi-source verification (coming soon)."""
    typer.echo("Research command coming soon. Use 'hawk search' for now.")


def _print_results(response) -> None:
    """Print search results in a simple format."""
    if not response.results:
        typer.echo("No results found.")
        return
    for i, result in enumerate(response.results, 1):
        typer.echo(f"{i}. {result.title}")
        typer.echo(f"   {result.url}")
        if result.snippet:
            typer.echo(f"   {result.snippet[:200]}")
        typer.echo()
    typer.echo(f"({response.total_time_ms}ms via {response.engine})")


if __name__ == "__main__":
    app()
