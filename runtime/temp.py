import os
import argparse
import logging
from typing import List, Optional

from runtime.core import Session
from runtime.agent import Agent, instantiate_agent, find_agent_by_role
from runtime.orchestrator import Orchestrator
from runtime.loader import load_config, load_agent_templates, load_prompts
from runtime.log import setup_logging

def temp_main():
    """
    Main entry point for the runtime system, parsing command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Run the Gemini agent runtime.")
    parser.add_argument("-p", "--plan-only", action="store_true", help="Generate only the plan without executing tasks.")
    parser.add_argument("-r", "--rounds", type=int, default=1, help="The number of rounds to execute the workflow.")
    parser.add_argument("-f", "--files", nargs='*', help="List of files to be used in the task.")
    parser.add_argument("-o", "--orchestrator", type=str, help="The name of the orchestrator to use.", default="Meta-AI")
    parser.add_argument("-m", "--model", type=str, help="Default LLM.", default="gemini-2.5-flash-lite")
    parser.add_argument("task", type=str, help="The initial task for the orchestrator to perform.")
    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    system_runtime_bootstrap(project_root, args.task, args.plan_only, args.rounds, args.files or [], args.orchestrator, args.model)


if __name__ == "__main__":
    temp_main()
