"""
KickLang Generation 2 CLI.

A modern, rich-text CLI for interacting with KickLang pipelines.
"""

import asyncio
import os
import typer
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.logging import RichHandler
import logging

from t20.kicklang.pipelines import Pipeline, PipelineConfig

# Configure nice logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)]
)

logger = logging.getLogger("t20.cli")
app = typer.Typer(help="KickLang Gen 2 Demo CLI", add_completion=False)
console = Console(force_terminal=True)

@app.command()
def run(
    goal: str = typer.Argument(..., help="The high-level goal for the pipeline."),
    files: Optional[List[str]] = typer.Option(None, "--file", "-f", help="Context files to include."),
    root: str = typer.Option(os.getcwd(), "--root", "-r", help="Project root directory."),
    model: str = typer.Option("gemini-2.5-flash-lite", "--model", "-m", help="Model to use.")
):
    """
    Run a KickLang pipeline execution.
    """
    console.print(Panel(f"[bold blue]KickLang Pipeline[/bold blue]\nGoal: [italic]{goal}[/italic]", border_style="blue"))
    
    config = PipelineConfig(
        root_dir=root,
        default_model=model,
        enable_tracing=True
    )
    
    try:
        pipeline = Pipeline(config)
    except Exception as e:
        console.print(f"[bold red]Initialization Failed:[/bold red] {e}")
        raise typer.Exit(code=1)

    async def execute():
        await pipeline.run(goal=goal, files=files or [])

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task(description="Running Pipeline...", total=None)
            asyncio.run(execute())
            progress.update(task, completed=True)
            
        console.print(Panel("[bold green]Execution Complete![/bold green]", border_style="green"))

    except Exception as e:
        console.print(f"[bold red]Execution Error:[/bold red] {e}")
        # Initialize pipeline is sync, run is async.
        # Errors in run are caught here.
        raise typer.Exit(code=1)

def main():
    app()

if __name__ == "__main__":
    main()
