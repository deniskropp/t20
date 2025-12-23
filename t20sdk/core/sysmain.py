"""This module serves as the main entry point for the command-line interface.

It parses command-line arguments and initiates the system bootstrap process,
acting as the primary interface for running the multi-agent system.
"""

import argparse
import asyncio
import json
import logging
import os
from typing import List, Optional

from pydantic import BaseModel

from t20sdk.core import Plan
from t20sdk.core.custom_types import File
from t20sdk.core.log import setup_logging
from t20sdk.core.system import System
from t20sdk.core.util import read_file

logger = logging.getLogger(__name__)


def parse_command_line_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for the runtime system.

    Returns:
        An argparse.Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="T20 multi-agent runtime.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    general_group = parser.add_argument_group("General Settings")
    general_group.add_argument(
        "-S", "--serve", action="store_true", help="Serve the runtime via HTTP."
    )
    general_group.add_argument(
        "-P", "--plan-from", type=str, default=None, help="Read plan from file."
    )
    general_group.add_argument(
        "-p",
        "--plan-only",
        action="store_true",
        help="Generate only the plan without executing tasks.",
    )
    general_group.add_argument(
        "-r",
        "--rounds",
        type=int,
        default=1,
        help="The number of rounds to execute the workflow.",
    )
    general_group.add_argument(
        "-f",
        "--files",
        nargs="*",
        help="List of files to be used in the task.",
        default=[],
    )

    orchestrator_group = parser.add_argument_group("Orchestrator Settings")
    orchestrator_group.add_argument(
        "-o",
        "--orchestrator",
        type=str,
        help="The name of the orchestrator to use.",
        default="Meta-AI",
    )
    orchestrator_group.add_argument(
        "-m",
        "--model",
        type=str,
        help="Default LLM model to use.",
        default="gemini-2.5-flash-lite",
    )

    parser.add_argument(
        "task",
        nargs="?",
        default=None,
        help="The initial task for the orchestrator to perform.",
    )

    args = parser.parse_args()

    if args.rounds < 1:
        parser.error("Number of rounds must be at least 1.")
    if not args.task and not args.serve and not args.plan_from:
        parser.error("The task argument is required when not in serve mode, unless --plan-from is specified.")

    return args


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


class StartRequest(BaseModel):
    high_level_goal: str
    files: Optional[List[File]] = []
    plan_from: Optional[str] = None
    orchestrator: str = "Meta-AI"
    model: str = "gemini-2.5-flash-lite"


class RunRequest(BaseModel):
    plan: Plan
    rounds: int = 1
    files: Optional[List[File]] = []


def serving():
    """
    Starts the FastAPI server to expose the runtime system functionality.
    """
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # This is a simple way to manage state for a local server.
    # For a production environment, a more robust solution would be needed.
    state = {}

    @app.post("/start")
    async def start_workflow(request: StartRequest):
        """
        Initializes the system and creates a plan. This corresponds to steps 4, 5, and 6.
        """
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # 4. Instantiate and set up the system
        system = System(root_dir=project_root, default_model=request.model)
        system.setup(orchestrator_name=request.orchestrator)
        state["system"] = system

        # 5. Re-configure logging based on loaded config
        log_level = system.config.get("logging_level", "INFO")
        setup_application_logging(log_level=log_level)

        # 6. Start the system's main workflow
        plan_arg = None
        if request.plan_from:
            plan_content = read_file(request.plan_from)
            if request.plan_from.endswith(".kl") or request.plan_from.endswith(".md"):
                from t20sdk.core.parsing import KickLangParser
                plan_arg = KickLangParser.parse(plan_content)
            else:
                plan_arg = Plan.model_validate_json(plan_content)

        plan = await system.start(
            high_level_goal=request.high_level_goal,
            files=request.files,
            plan=plan_arg
        )
        state["plan"] = plan
        return {"plan": plan.model_dump()}

    @app.post("/run")
    async def run_workflow(request: RunRequest):
        """
        Runs the system's main workflow. This corresponds to step 7.
        """
        system = state.get("system")
        if not system:
            return {"error": "System not initialized. Please call /start first."}

        results = []
        async for step, result in system.run(
            plan=request.plan, rounds=request.rounds, files=request.files
        ):
            try:
                result = json.dumps(json.loads(result), indent=4)
            except:
                pass
            results.append({"step": step.model_dump(), "result": result})
        return {"results": results}

    uvicorn.run(app, host="127.0.0.1", port=8000)


async def system_main():
    """
    Main entry point for the runtime system.
    Parses arguments, sets up logging and configuration, and runs the system.
    """
    try:
        # 1. Parse command line arguments
        args = parse_command_line_arguments()

        if args.serve:
            setup_application_logging()
            logger.info("Starting server mode.")
            serving()
            return

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # 2. Initial logging setup
        setup_application_logging()

        # 3. Convert file paths to File objects
        file_objects = []
        for file_path in args.files:
            try:
                content = read_file(file_path)
                if content.startswith("Error:"):
                    logger.warning(f"Skipping file '{file_path}': {content}")
                    continue
                file_objects.append(File(path=file_path, content=content))
            except Exception as e:
                logger.error(f"Error processing file '{file_path}': {e}")

        # 4. Instantiate and set up the system
        system = System(root_dir=project_root, default_model=args.model)
        system.setup(orchestrator_name=args.orchestrator)

        # 5. Re-configure logging based on loaded config
        log_level = system.config.get("logging_level", "INFO")
        setup_application_logging(log_level=log_level)

        # 6. Start the system's main workflow
        plan_arg = None
        if args.plan_from:
            plan_content = read_file(args.plan_from)
            if args.plan_from.endswith(".kl") or args.plan_from.endswith(".md"):
                from t20sdk.core.parsing import KickLangParser
                plan_arg = KickLangParser.parse(plan_content)
            else:
                plan_arg = Plan.model_validate_json(plan_content)

        plan = await system.start(
            high_level_goal=args.task,
            files=file_objects,
            plan=plan_arg
        )
        if args.plan_only:
            print(plan.model_dump_json(indent=4))
            logger.info("Plan-only mode: Workflow execution skipped.")
            return

        # 7. Run the system's main workflow
        async for step, result in system.run(
            plan=plan, rounds=args.rounds, files=file_objects
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


def main():
    try:
        asyncio.run(system_main())
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return
    except KeyboardInterrupt as e:
        print("")
        return


if __name__ == "__main__":
    main()
