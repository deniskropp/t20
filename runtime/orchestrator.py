"""Orchestrator agent definition and related planning models."""

import json
from typing import List, Dict, Any, Optional
import logging

from colorama import Fore, Style

from pydantic import BaseModel, Field

from runtime.agent import Agent # Import Agent base class
from runtime.core import ExecutionContext, Session # Import Session and ExecutionContext
from runtime.llm import LLM
from runtime.util import read_file

logger = logging.getLogger(__name__)

from runtime.custom_types import Plan

class Orchestrator(Agent):
    """An agent responsible for creating and managing a plan for multi-agent workflows."""

    def __init__(self, name, role, goal, model, system_prompt) -> None:
        super().__init__(name, role, goal, model, system_prompt)

    def start_workflow(self, session: Session, initial_task: str, rounds: int = 1, plan_only: bool = False, files: List[str] = []):
        """
        Initiates and manages the entire workflow for multiple rounds.

        Args:
            session (Session): The current session object.
            initial_task (str): The high-level goal for the workflow.
            rounds (int): The number of rounds to execute the workflow.
            plan_only (bool): If True, only generates the plan without executing tasks.
            files (List[str]): List of files to be used in the task.
        """
        file_contents = {}
        if files:
            logger.info("Files provided:")
            for file_path in files:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        file_contents[file_path] = content
                        logger.info(f"  - {file_path}")
                except Exception as e:
                    logger.error(f"Error reading file {file_path}: {e}")

        plan = self._generate_plan(session, initial_task, file_contents)
        logger.info(f"Generated plan:\n{json.dumps(plan, indent=4)}")

        if not plan or "tasks" not in plan or "roles" not in plan:
            logger.error("Orchestration failed: Could not generate a valid plan.")
            return

        if plan_only:
            logger.info("Plan-only mode: Workflow execution skipped.")
            return

        context = ExecutionContext(session=session, high_level_goal=initial_task, plan=plan)

        if file_contents:
            context.record_artifact("initial_files.json", json.dumps(file_contents), True)

        for context.round_num in range(1, rounds + 1):
            logger.info(f"Orchestrator {self.name} is starting workflow round {context.round_num} for goal: '{initial_task}'")

            team_by_name = {agent.name: agent for agent in self.team.values()} if self.team else {}

            context.step_index = 0

            logger.info('')

            while context.step_index < len(plan["tasks"]):
                step = context.current_step()
                name = step.get("name", "Any")
                delegate_agent = team_by_name.get(name)

                if not delegate_agent:
                    logger.warning(f"No agent found with name '{name}'. Skipping step {context.step_index}.")
                    context.step_index += 1
                    continue

                if delegate_agent.role == 'Prompt Engineer':
                    logger.info(f"Orchestrator detected special role: {delegate_agent.name}. Preparing inputs.")

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
                            logger.error("Prompt Engineer's output was not a valid JSON for prompt update.")

                context.step_index += 1

            logger.info(f"Orchestrator has completed workflow round {context.round_num}.")

    def _check_new_prompts(self, session: Session, data_structure: dict | list):
        """
        Recursively checks for new prompts within a dictionary or list of objects
        and updates agent system prompts if 'target_agent_name' and 'new_system_prompt'
        keys are found.

        Args:
            session (Session): The current session object.
            data_structure (dict | list): The object (dictionary or list) to traverse for new prompt information.
        """
        if isinstance(data_structure, dict):
            self._check_new_prompt(session, data_structure)
            for key, value in data_structure.items():
                if isinstance(value, (dict, list)):
                    self._check_new_prompts(session, value)
        elif isinstance(data_structure, list):
            for item in data_structure:
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
                target_agent = next((a for a in self.team.values() or () if a.name == target_agent_name), None)
                if not target_agent:
                    target_agent = next((a for a in session.agents if a.name == target_agent_name), None)

                if target_agent:
                    target_agent.update_system_prompt(new_system_prompt)
                else:
                    logger.warning(f"Target agent '{target_agent_name}' not found for prompt update.")

    def _generate_plan(self, session: Session, high_level_goal: str, file_contents: Dict[str, str] = {}) -> Dict[str, Any]:
        """
        Invokes the language model to get a structured plan for the given high-level goal.

        Args:
            session (Session): The current session object.
            high_level_goal (str): The high-level goal for which to generate a plan.
            file_contents (Dict[str, str]): A dictionary of file paths and their contents.

        Returns:
            Dict[str, Any]: The generated plan as a dictionary, or an empty dictionary if an error occurs.
        """
        logger.info(f"Orchestrator {self.name} is generating a plan for: '{high_level_goal}'")
        if not self.llm or not self.team:
            logger.error("Orchestrator client or team not initialized.")
            return {}

        team_description = "\n".join(
            f"- Name: '{agent.name}'\n"
            f"  Role: `{agent.role}`\n"
            f"  Goal: \"{agent.goal}\""
            for agent in self.team.values()
        )

        planning_prompt = [
            f"We are meta-artificial intelligence, cohesively creating an iterative role and task plan, thinking step-by-step towards the high-level goal.",

#            f"Conceptual Framework: 'Echo'",

            f"High-Level Goal: '{high_level_goal}'",

            f"Team Members:\n{team_description}",

            f"Leverage each team member, guided by their goals, to maximize collaboration. Use prompt engineering to refine the system prompts for each agent based on their roles and tasks.",
        ]

        prompt = read_file("prompts/orcis_planning.txt").strip()
        planning_prompt = [prompt.format(
            high_level_goal=high_level_goal,
            team_description=team_description
        )]

        prompt = "\n\n".join(planning_prompt)

        print(f"{Fore.LIGHTCYAN_EX}Orchestrator {self.name}Planning Prompt:\n{prompt}{Style.RESET_ALL}")

        if file_contents:
            file_section = [f"\n--- Files Content ---"]
            for file_path, content in file_contents.items():
                file_section.append(f"File: {file_path}\n```\n{content}\n```")
            planning_prompt.append("\n".join(file_section))

        logger.debug(planning_prompt)
        session.add_artifact("planning_prompt.txt", prompt)

        try:
            response = self.llm.generate_content(
                model_name=self.model,
                contents="\n\n".join(planning_prompt),
                system_instruction=self.system_prompt,
                temperature=0.1,
                response_mime_type='application/json', #if self.role == 'Prompt Engineer' else None
                response_schema=Plan
            )
            plan = json.loads(response or '{}')
        except Exception as e:
            logger.error(f"Error generating plan for {self.name}: {e}")
            plan = {"error": str(e)}

        logger.info(f"\n\nPlan generated for {self.name}: {json.dumps(plan, indent='    ')}\n\n\n")
        session.add_artifact("initial_plan.json", plan)
        return plan
