"""Orchestrator agent definition and related planning models."""

import json
from typing import List, Dict, Any, Optional

from colorama import Fore, Style, init
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

from runtime.agent import Agent # Import Agent base class
from runtime.core import ExecutionContext, Session # Import Session and ExecutionContext

# Initialize colorama for cross-platform colored output
init()

from runtime.types import Plan

class Orchestrator(Agent):
    """An agent responsible for creating and managing a plan for multi-agent workflows."""

    def start_workflow(self, session: Session, initial_task: str, rounds: int = 1, plan_only: bool = False):
        """
        Initiates and manages the entire workflow for multiple rounds.

        Args:
            session (Session): The current session object.
            initial_task (str): The high-level goal for the workflow.
            rounds (int): The number of rounds to execute the workflow.
            plan_only (bool): If True, only generates the plan without executing tasks.
        """
        plan = self._generate_plan(session, initial_task)
        print(f"{Fore.CYAN}Generated plan:{Style.RESET_ALL}\n{json.dumps(plan, indent=4)}")

        if not plan or "tasks" not in plan or "roles" not in plan:
            print(f"{Fore.RED}Orchestration failed: Could not generate a valid plan.{Style.RESET_ALL}")
            return

        if plan_only:
            print(f"{Fore.CYAN}Plan-only mode: Workflow execution skipped.")
            return

        context = ExecutionContext(session=session, high_level_goal=initial_task, plan=plan)

        for context.round_num in range(1, rounds + 1):
            print(f"{Fore.YELLOW}Orchestrator {self.name} is starting workflow round {context.round_num} for goal{Style.RESET_ALL}: '{initial_task}'")

            team_by_role = {agent.role: agent for agent in self.team} if self.team else {}

            context.step_index = 0

            print('')

            while context.step_index < len(plan["tasks"]):
                step = context.current_step()
                role = step.get("role", "Any Role")
                delegate_agent = team_by_role.get(role)

                if not delegate_agent:
                    print(f"{Fore.RED}Warning: No agent found with role '{role}'{Style.RESET_ALL}. Skipping step {context.step_index}.")
                    context.step_index += 1
                    continue

                if delegate_agent.role == 'Prompt Engineer':
                    print(f"{Fore.LIGHTBLUE_EX}Orchestrator detected special role{Style.RESET_ALL}: {delegate_agent.role}. Preparing inputs.")

                result = delegate_agent.execute_task(context)
                if result:
                    context.record_artifact(f"{delegate_agent.name}_result.txt", result, True)
                    if delegate_agent.role == 'Prompt Engineer':
                        try:
                            response = json.loads(result)
                            self._check_new_prompts(session, response)
                            for key, value in response.items() if isinstance(response, dict) else []:
                                if key == "refined_prompts" or key == "initial_prompts" or key == "initial_system_prompts":
                                    if "target_agent_name" in value:
                                        self._check_new_prompts(session, value)
                                    else:
                                        self._check_new_prompts(session, list(value))
                        except json.JSONDecodeError:
                            print(f"{Fore.RED}Prompt Engineer's output was not a valid JSON for prompt update.{Style.RESET_ALL}")

                context.step_index += 1

            print(f"{Fore.LIGHTRED_EX}Orchestrator has completed workflow round {context.round_num}.{Style.RESET_ALL}")

    def _check_new_prompts(self, session: Session, obj: dict | list):
        """
        Recursively checks for new prompts within a dictionary or list of objects
        and updates agent system prompts if 'target_agent_name' and 'new_system_prompt'
        keys are found.

        Args:
            session (Session): The current session object.
            obj (dict | list): The object (dictionary or list) to traverse for new prompt information.
        """
        if isinstance(obj, dict):
            self._check_new_prompt(session, obj)
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    self._check_new_prompts(session, value)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    self._check_new_prompts(session, item)

    def _check_new_prompt(self, session: Session, obj: dict):
        """
        Updates a single agent's system prompt if the provided dictionary contains
        'target_agent_name' and 'new_system_prompt' keys.

        Args:
            session (Session): The current session object.
            obj (dict): A dictionary expected to contain 'target_agent_name' and
                        'new_system_prompt' for a single agent update.
        """
        if "target_agent_name" in obj and "new_system_prompt" in obj:
            target_agent_name = obj.get("target_agent_name")
            new_system_prompt = obj.get("new_system_prompt")

            if target_agent_name and new_system_prompt:
                target_agent = next((a for a in self.team or () if a.name == target_agent_name), None)
                if not target_agent:
                    target_agent = next((a for a in session.agents if a.name == target_agent_name), None)

                if target_agent:
                    target_agent.update_system_prompt(new_system_prompt)
                else:
                    print(f"{Fore.CYAN}Warning: Target agent '{target_agent_name}' not found for prompt update.{Style.RESET_ALL}")

    def _generate_plan(self, session: Session, high_level_goal: str) -> Dict[str, Any]:
        """
        Invokes the language model to get a structured plan for the given high-level goal.

        Args:
            session (Session): The current session object.
            high_level_goal (str): The high-level goal for which to generate a plan.

        Returns:
            Dict[str, Any]: The generated plan as a dictionary, or an empty dictionary if an error occurs.
        """
        print(f"{Fore.MAGENTA}Orchestrator {self.name} is generating a plan for{Style.RESET_ALL}: '{high_level_goal}'")
        if not self.client or not self.team:
            print(f"{Fore.RED}Error: Orchestrator client or team not initialized.{Style.RESET_ALL}")
            return {}

        team_description = "\n".join(
            f"- Name: '{agent.name}'\n"
            f"  Role: `{agent.role}`\n"
            f"  Goal: \"{agent.goal}\""
            for agent in self.team
        )
        
        planning_prompt = [
            f"We are meta-artificial intelligence, cohesively creating an iterative role and task plan, thinking step-by-step towards the high-level goal.",

            f"Conceptual Framework: 'Echo'",

            f"High-Level Goal: '{high_level_goal}'",

            f"Team Members:\n{team_description}",

            f"Leverage each team member, guided by their goals, to maximize collaboration. Use prompt engineering to refine the system prompts for each agent based on their roles and tasks.",
        ]
        print(planning_prompt)
        session.add_artifact("planning_prompt.txt", "\n\n".join(planning_prompt))

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents="\n\n".join(planning_prompt),
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    response_mime_type="application/json",
                    response_schema=Plan,
                    temperature=0.1,
                ),
            )
            plan = json.loads(response.text or '{}')
        except Exception as e:
            print(f"{Fore.RED}Error generating plan for {self.name}{Style.RESET_ALL}: {e}")
            plan = {"error": str(e)}

        print(f"\n\n{Fore.GREEN}Plan generated for {self.name}{Style.RESET_ALL}: {json.dumps(plan, indent="    ")}\n\n\n")
        session.add_artifact("initial_plan.json", plan)
        return plan
