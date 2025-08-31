"""Entry point and bootstrapping logic for the multi-agent runtime system."""

import os
import argparse
from typing import List, Dict, Any

from colorama import Fore, Style, init

from runtime.core import Session
from runtime.agent import Agent, instantiate_agent, find_agent_by_role
from runtime.orchestrator import Orchestrator
from runtime.loader import load_config, load_agent_templates, load_prompts

# Initialize colorama for cross-platform colored output
init()

def system_runtime_bootstrap(root_dir: str, initial_task: str, plan_only: bool = False, rounds: int = 1, files: List[str] = []):
    """
    Bootstraps the multi-agent runtime system.

    Args:
        root_dir (str): The root directory of the project.
        initial_task (str): The initial task for the orchestrator to perform.
        plan_only (bool): If True, only generates the plan without executing tasks.
        rounds (int): The number of rounds to execute the workflow.
        files (List[str]): List of files to be used in the task.
    """
    print(f"{Fore.LIGHTBLUE_EX}--- System Runtime Bootstrap ---{Style.RESET_ALL}")

    config = load_config(os.path.join(root_dir, "config", "runtime.yaml"))
    agent_specs = load_agent_templates(os.path.join(root_dir, "agents"))
    prompts = load_prompts(os.path.join(root_dir, "prompts"))

    all_team_members = {member.lower() for spec in agent_specs if 'team' in spec for member in spec['team']}

    agents: List[Agent] = []
    for spec in agent_specs:
        # Only instantiate top-level agents, not those that are part of another agent's team
        if spec['name'].lower() not in all_team_members:
            agent = instantiate_agent(spec, prompts, agent_specs)
            if agent:
                agents.append(agent)

    if not agents:
        print(f"{Fore.RED}Error: No agents could be instantiated. Bootstrap aborted.{Style.RESET_ALL}")
        return

    orchestrator_role = 'Orchestrator'
    orchestrator = find_agent_by_role(agents, orchestrator_role)

    if not orchestrator:
        print(f"{Fore.RED}Error: Orchestrator with role '{orchestrator_role}' not found. Bootstrap aborted.{Style.RESET_ALL}")
        return

    if not isinstance(orchestrator, Orchestrator):
        print(f"{Fore.RED}Error: Agent with role '{orchestrator_role}' is not a valid Orchestrator instance. Bootstrap aborted.{Style.RESET_ALL}")
        return

    session = Session(agents=agents)

    print(f"{Fore.LIGHTGREEN_EX}--- Starting Workflow ---{Style.RESET_ALL}")
    orchestrator.start_workflow(session, initial_task, rounds=rounds, plan_only=plan_only, files=files)

    print(f"{Fore.LIGHTBLUE_EX}--- System Runtime Bootstrap Complete ---{Style.RESET_ALL}")

def system_main():
    """
    Main entry point for the runtime system, parsing command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Run the Gemini agent runtime.")
    parser.add_argument("-p", "--plan-only", action="store_true", help="Generate only the plan without executing tasks.")
    parser.add_argument("-r", "--rounds", type=int, default=1, help="The number of rounds to execute the workflow.")
    parser.add_argument("-f", "--files", nargs='*', help="List of files to be used in the task.")
    parser.add_argument("task", type=str, help="The initial task for the orchestrator to perform.")
    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    system_runtime_bootstrap(project_root, args.task, args.plan_only, args.rounds, args.files or [])


if __name__ == "__main__":
    system_main()
