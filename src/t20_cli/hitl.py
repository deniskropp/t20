"""
HITL (Human-In-The-Loop) CLI for T20 System.
Runs the system with a pause before each task, waiting for confirmation via Ntfy.
"""

import asyncio
import json
import logging
import os
import sys
from typing import List, Optional
from typing_extensions import Annotated

import typer
from t20.core import Plan
from t20.core.common.types import File, Task
from t20.core.system.log import setup_logging
from t20.core.system.system import System
from t20.core.common.util import read_file
from t20.core.system.ntfy import NtfyClient

logger = logging.getLogger(__name__)

app = typer.Typer(help="HITL T20 Runtime with Ntfy integration.")

async def hitl_run(
    ntfy_topic: str,
    task: Optional[str],
    plan_from: Optional[str],
    rounds: int,
    files: List[str],
    orchestrator: str,
    model: str
):
    setup_logging(level="INFO")
    
    if not task and not plan_from:
        logger.error("Must provide a task or a plan file.")
        return

    logger.info(f"Starting HITL System on topic: {ntfy_topic}")
    logger.info(f"Please monitor https://ntfy.violass.club/{ntfy_topic}")

    ntfy = NtfyClient(ntfy_topic)

    async def ask_user(task: Task) -> bool:
        """Callback to ask user for confirmation via Ntfy."""
        logger.info(f"Asking user for approval on task: {task.description}")
        return await ntfy.send_confirmation_request(task.description)

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../t20'))
    
    # Core system setup (mirrors sysmain.py)
    file_objects = []
    for file_path in files:
         try:
             content = read_file(file_path)
             if content.startswith("Error:"):
                 logger.warning(f"Skipping file '{file_path}'")
                 continue
             file_objects.append(File(path=file_path, content=content))
         except Exception as e:
             logger.error(f"Error reading file '{file_path}': {e}")

    system = System(root_dir=project_root, default_model=model)
    try:
        system.setup(orchestrator_name=orchestrator)
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        return

    # Plan loading/generation
    plan_arg = None
    if plan_from:
        plan_content = read_file(plan_from)
        if plan_from.endswith(".kl") or plan_from.endswith(".md"):
             from t20.core.parsing import KickLangParser
             plan_arg = KickLangParser.parse(plan_content)
        else:
             plan_arg = Plan.model_validate_json(plan_content)

    try:
        plan = await system.start(
            high_level_goal=task,
            files=file_objects,
            plan=plan_arg
        )
    except Exception as e:
        logger.error(f"Planning failed: {e}")
        return

    # Execution with HITL
    logger.info("Plan generated. Starting execution with HITL checks...")
    
    async for step, result in system.run(
        plan=plan, 
        rounds=rounds, 
        files=file_objects,
        confirmation_callback=ask_user
    ):
        logger.info(f"Step {step.id} completed.")
        try:
             # Just pretty print the result
             pass
        except:
             pass

@app.command()
def run(
    ntfy_topic: Annotated[str, typer.Option("--ntfy-topic", help="The Ntfy topic to subscribe to for confirmation.")],
    task: Annotated[Optional[str], typer.Argument(help="Initial task goal.")] = None,
    plan_from: Annotated[Optional[str], typer.Option("--plan-from", "-p", help="Read plan from file.")] = None,
    rounds: Annotated[int, typer.Option("--rounds", "-r", help="Rounds to execute.")] = 1,
    files: Annotated[List[str], typer.Option("--files", "-f", help="Input files.")] = [],
    orchestrator: Annotated[str, typer.Option("--orchestrator", "-o", help="Orchestrator name.")] = "Meta-AI",
    model: Annotated[str, typer.Option("--model", "-m", help="Default model.")] = "gemini-2.5-flash-lite",
):
    """
    Run the T20 HITL System.
    """
    if not task and not plan_from:
        typer.echo("Must provide a task or a plan file.", err=True)
        raise typer.Exit(code=1)

    try:
        asyncio.run(hitl_run(ntfy_topic, task, plan_from, rounds, files, orchestrator, model))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")

def main():
    app()

if __name__ == "__main__":
    main()