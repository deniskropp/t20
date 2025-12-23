"""
T20 Console CLI
---------------
This module provides a command-line interface to interact with the T20 system,
specifically focusing on component management via the Knowledge Graph.
"""

import argparse
import sys
import os
import logging
from typing import List

# Ensure we can import from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.system import System
from knowledge_graph.interface import KnowledgeGraphInterface
from data_models.kicklang_schemas import Component
from config.system_governance import SystemGovernance

logger = logging.getLogger(__name__)

def setup_logging(level="INFO"):
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def handle_list_components(kg: KnowledgeGraphInterface, args):
    components = kg.list_components()
    if not components:
        print("No components found.")
        return

    print(f"{'Name':<20} | {'Status':<15} | {'Description'}")
    print("-" * 60)
    for comp in components:
        print(f"{comp.name:<20} | {comp.status:<15} | {comp.description or ''}")

def handle_add_component(kg: KnowledgeGraphInterface, args):
    try:
        comp = Component(name=args.name, description=args.description)
        if kg.add_component(comp):
            print(f"Successfully added component '{args.name}'.")
        else:
            print(f"Error: Component '{args.name}' already exists.")
    except Exception as e:
        print(f"Error creating component: {e}")

def handle_update_status(kg: KnowledgeGraphInterface, args):
    if kg.update_component_status(args.name, args.status):
        print(f"Successfully updated '{args.name}' to '{args.status}'.")
    else:
        print(f"Error: Failed to update status for '{args.name}'. Check component existence and governance rules.")

def handle_list_artifacts(kg: KnowledgeGraphInterface, args):
    artifacts = kg.get_artifacts()
    if not artifacts:
        print("No artifacts found.")
        return

    print(f"{'Task ID':<15} | {'Summary'}")
    print("-" * 60)
    for art in artifacts:
        print(f"{art.system_task_id:<15} | {art.output_summary or ''}")

import asyncio
def handle_run_task(args):
    # Initialize System with proper root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    system = System(root_dir=project_root, default_model="gemini-2.5-flash")
    
    # We need to setup the system (load agents, etc.)
    # For CLI demo, we might need to mock or ensure we have a valid orchestrator/agent
    try:
        system.setup()
    except Exception as e:
        print(f"System setup failed: {e}")
        return

    # Use the shared KG if possible, OR rely on System's internal KG.
    # Since System instantiates its own KG, we can access it via system.kg
    
    print(f"Running task: {args.goal}")
    
    async def run():
        try:
            plan = await system.start(high_level_goal=args.goal)
            async for step, result in system.run(plan):
                print(f"Step {step.id} completed.")
        except Exception as e:
            print(f"Execution failed: {e}")

    asyncio.run(run())
    
    # Print Artifacts from System's KG
    print("\nGenerated Artifacts:")
    artifacts = system.kg.get_artifacts()
    for art in artifacts:
        print(f"- {art.output_summary}")

def main():
    parser = argparse.ArgumentParser(description="T20 System Console")
    parser.add_argument("--log-level", default="INFO", help="Set logging level")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List Components
    subparsers.add_parser("list-components", help="List all registered components")
    
    # Add Component
    add_parser = subparsers.add_parser("add-component", help="Register a new component")
    add_parser.add_argument("name", help="Unique name of the component")
    add_parser.add_argument("--description", help="Description of the component")
    
    # Update Status
    status_parser = subparsers.add_parser("update-status", help="Update component status")
    status_parser.add_argument("name", help="Name of the component")
    status_parser.add_argument("status", help="New status to transition to")

    # List Artifacts
    subparsers.add_parser("list-artifacts", help="List all generated artifacts")

    # Run Task
    run_parser = subparsers.add_parser("run-task", help="Execute a task via the System")
    run_parser.add_argument("goal", help="The high-level goal to execute")

    args = parser.parse_args()
    
    setup_logging(args.log_level)
    
    # Initialize Core Components
    kg = KnowledgeGraphInterface()
    
    if args.command == "list-components":
        handle_list_components(kg, args)
    elif args.command == "add-component":
        handle_add_component(kg, args)
    elif args.command == "update-status":
        handle_update_status(kg, args)
    elif args.command == "list-artifacts":
        handle_list_artifacts(kg, args)
    elif args.command == "run-task":
        handle_run_task(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
