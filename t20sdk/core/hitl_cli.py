"""
HITL (Human-In-The-Loop) CLI for T20 System.
Runs the system with a pause before each task, waiting for confirmation via Ntfy.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import List

from t20sdk.core import Plan
from t20sdk.core.custom_types import File, Task
from t20sdk.core.log import setup_logging
from t20sdk.core.system import System
from t20sdk.core.util import read_file
from t20sdk.core.ntfy import NtfyClient

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="T20 HITL Runtime with Ntfy integration.")
    
    parser.add_argument(
        "--ntfy-topic", 
        type=str, 
        required=True, 
        help="The Ntfy topic to subscribe to for confirmation."
    )
    
    # Arguments copied/adapted from sysmain.py
    parser.add_argument(
        "-p", "--plan-from", type=str, default=None, help="Read plan from file."
    )
    parser.add_argument(
        "-r", "--rounds", type=int, default=1, help="Rounds to execute."
    )
    parser.add_argument(
        "-f", "--files", nargs="*", default=[], help="Input files."
    )
    parser.add_argument(
        "-o", "--orchestrator", type=str, default="Meta-AI", help="Orchestrator name."
    )
    parser.add_argument(
        "-m", "--model", type=str, default="gemini-2.5-flash-lite", help="Default model."
    )
    parser.add_argument(
        "task", nargs="?", default=None, help="Initial task goal."
    )
    
    return parser.parse_args()

async def hitl_main():
    setup_logging(level="INFO")
    args = parse_args()
    
    if not args.task and not args.plan_from:
        logger.error("Must provide a task or a plan file.")
        return

    logger.info(f"Starting HITL System on topic: {args.ntfy_topic}")
    logger.info(f"Please monitor https://ntfy.violass.club/{args.ntfy_topic}")

    ntfy = NtfyClient(args.ntfy_topic)

    async def ask_user(task: Task) -> bool:
        """Callback to ask user for confirmation via Ntfy."""
        logger.info(f"Asking user for approval on task: {task.description}")
        return await ntfy.send_confirmation_request(task.description)

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) # Adjust path to root
    
    # Core system setup (mirrors sysmain.py)
    file_objects = []
    for file_path in args.files:
         try:
             content = read_file(file_path)
             if content.startswith("Error:"):
                 logger.warning(f"Skipping file '{file_path}'")
                 continue
             file_objects.append(File(path=file_path, content=content))
         except Exception as e:
             logger.error(f"Error reading file '{file_path}': {e}")

    system = System(root_dir=project_root, default_model=args.model)
    try:
        system.setup(orchestrator_name=args.orchestrator)
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        return

    # Plan loading/generation
    plan_arg = None
    if args.plan_from:
        plan_content = read_file(args.plan_from)
        if args.plan_from.endswith(".kl") or args.plan_from.endswith(".md"):
             from t20sdk.core.parsing import KickLangParser
             plan_arg = KickLangParser.parse(plan_content)
        else:
             plan_arg = Plan.model_validate_json(plan_content)

    try:
        plan = await system.start(
            high_level_goal=args.task,
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
        rounds=args.rounds, 
        files=file_objects,
        confirmation_callback=ask_user
    ):
        logger.info(f"Step {step.id} completed.")
        try:
             # Just pretty print the result
             pass
        except:
             pass

def main():
    try:
        asyncio.run(hitl_main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
