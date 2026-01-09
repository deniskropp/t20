"""This module serves as the main entry point for the command-line interface.

It parses command-line arguments and initiates the system bootstrap process,
acting as the primary interface for running the multi-agent system.
"""

import asyncio
import json
import logging
import os
from typing import List, Optional
from pathlib import Path

import typer
from typing_extensions import Annotated

from t20.core import Plan
from t20.core.common.types import File
from t20.core.system.log import setup_logging
from t20.core.system.system import System
from t20.core.common.util import read_file

logger = logging.getLogger(__name__)

app = typer.Typer(help="T20 Multi-Agent Runtime CLI")

def setup_application_logging(log_level: str = "INFO") -> None:
    """
    Sets up the global logging configuration for the application.

    Args:
        log_level: The desired logging level (e.g., "DEBUG", "INFO", "WARNING").
    """
    try:
        setup_logging(level=log_level)
        logger.debug(f"Logging initialized with level: {log_level}")
    except ValueError as e:
        logger.error(f"Invalid log level '{log_level}': {e}")
        raise

async def system_run(
    task: Optional[str],
    plan_from: Optional[str],
    plan_only: bool,
    rounds: int,
    files: List[str],
    orchestrator: str,
    model: str
):
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../t20'))
        
        # 2. Initial logging setup
        setup_application_logging()

        # 3. Convert file paths to File objects
        file_objects = []
        for file_path in files:
            try:
                content = read_file(file_path)
                if content.startswith("Error:"):
                    logger.warning(f"Skipping file '{file_path}': {content}")
                    continue
                file_objects.append(File(path=file_path, content=content))
            except Exception as e:
                logger.error(f"Error processing file '{file_path}': {e}")

        # 4. Instantiate and set up the system
        system = System(root_dir=project_root, default_model=model)
        system.setup(orchestrator_name=orchestrator)

        # 5. Re-configure logging based on loaded config
        log_level = system.config.get("logging_level", "INFO")
        setup_application_logging(log_level=log_level)

        # 6. Start the system's main workflow
        plan_arg = None
        if plan_from:
            plan_content = read_file(plan_from)
            if plan_from.endswith(".kl") or plan_from.endswith(".md"):
                from t20.core.parsing import KickLangParser
                plan_arg = KickLangParser.parse(plan_content)
            else:
                plan_arg = Plan.model_validate_json(plan_content)

        plan = await system.start(
            high_level_goal=task,
            files=file_objects,
            plan=plan_arg
        )
        if plan_only:
            print(plan.model_dump_json(indent=4))
            logger.info("Plan-only mode: Workflow execution skipped.")
            return

        # 7. Run the system's main workflow
        async for step, result in system.run(
            plan=plan, rounds=rounds, files=file_objects
        ):
            try:
                result = json.dumps(json.loads(result), indent=4)
            except:
                pass
            # print(f"\n\n--- TASK [id: {step.id}, agent: {step.agent}, role: {step.role}, description: {step.description}] ---\n{result}\n")

    except (FileNotFoundError, RuntimeError) as e:
        logger.error(f"A critical error occurred: {e}")
        return
    except Exception as e:
        logger.error(f"An unexpected error occurred during system main execution: {e}")
        return

@app.command()
def run(
    task: Annotated[Optional[str], typer.Argument(help="The initial task for the orchestrator to perform.")] = None,
    plan_from: Annotated[Optional[str], typer.Option("--plan-from", "-P", help="Read plan from file.")] = None,
    plan_only: Annotated[bool, typer.Option("--plan-only", "-p", help="Generate only the plan without executing tasks.")] = False,
    rounds: Annotated[int, typer.Option("--rounds", "-r", help="The number of rounds to execute the workflow.")] = 1,
    files: Annotated[List[str], typer.Option("--files", "-f", help="List of files to be used in the task.")] = [],
    orchestrator: Annotated[str, typer.Option("--orchestrator", "-o", help="The name of the orchestrator to use.")] = "Meta-AI",
    model: Annotated[str, typer.Option("--model", "-m", help="Default LLM model to use.")] = "gemini-2.5-flash-lite",
):
    """
    Run the T20 Multi-Agent System.
    """
    if rounds < 1:
        typer.echo("Number of rounds must be at least 1.", err=True)
        raise typer.Exit(code=1)
    
    if not task and not plan_from:
        typer.echo("The task argument is required unless --plan-from is specified.", err=True)
        raise typer.Exit(code=1)

    asyncio.run(system_run(task, plan_from, plan_only, rounds, files, orchestrator, model))

def main():
    app()

if __name__ == "__main__":
    main()