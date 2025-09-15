"""This module defines the Orchestrator agent and its planning capabilities.

The Orchestrator is a specialized agent responsible for generating, managing,
and executing the workflow plan based on a high-level goal.
"""

import os
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

from runtime.custom_types import Plan, AgentOutput

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
            files (List[str]): List of file paths to be used as context in the task.
        """
        file_contents = {}
        if files:
            logger.info("Files provided:")
            for file_path in files:
                try:
                    with open(file_path, 'r') as file_handle:
                        content = file_handle.read()
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
            context.record_initial("initial_files.json", json.dumps(file_contents))

        for context.round_num in range(1, rounds + 1):
            logger.info(f"Orchestrator {self.name} is starting workflow round {context.round_num} for goal: '{initial_task}'")

            team_by_name = {agent.name: agent for agent in self.team.values()} if self.team else {}

            context.step_index = 0

            logger.info('')

            while context.step_index < len(plan["tasks"]):
                step = context.current_step()
                agent_name = step.get("name", "Any")
                delegate_agent = team_by_name.get(agent_name)

                if not delegate_agent:
                    logger.warning(f"No agent found with name '{agent_name}'. Skipping step {context.step_index}.")
                    context.step_index += 1
                    continue

                result = delegate_agent.execute_task(context)
                if result:
                    context.record_artifact(f"{delegate_agent.name}_result.txt", result, True)
                    try:
                        # Attempt to parse the output as AgentOutput
                        agent_output = AgentOutput.model_validate_json(result)
                        if agent_output.prompts:
                            logger.info(f"Agent {delegate_agent.name} provided new prompts.")
                            for prompt_data in agent_output.prompts:
                                self._update_agent_prompt(session, prompt_data.name, prompt_data.content)
                    except Exception as e:
                        logger.warning(f"Could not parse agent output as AgentOutput: {e}. Treating as plain text.")


                context.step_index += 1

            logger.info(f"Orchestrator has completed workflow round {context.round_num}.")

    def _update_agent_prompt(self, session: Session, agent_name: str, new_prompt: str):
        """
        Updates an agent's system prompt.

        Args:
            session (Session): The current session object.
            agent_name (str): The name of the agent to update.
            new_prompt (str): The new system prompt.
        """
        if agent_name and new_prompt:
            # Search for the target agent within the orchestrator's team or the session's agents
            target_agent = self.team.get(agent_name)
            if not target_agent:
                target_agent = next((a for a in session.agents if a.name == agent_name), None)

            if target_agent:
                target_agent.update_system_prompt(new_prompt)
                logger.info(f"Agent '{agent_name}' system prompt updated.")
            else:
                logger.warning(f"Target agent '{agent_name}' not found for prompt update.")

    def _generate_plan(self, session: Session, high_level_goal: str, file_contents: Dict[str, str] = {}) -> Dict[str, Any]:
        """
        Invokes the language model to get a structured plan for the given high-level goal.
        The plan includes a sequence of tasks and the roles responsible for them.

        Args:
            session (Session): The current session object.
            high_level_goal (str): The high-level goal for which to generate a plan.
            file_contents (Dict[str, str]): A dictionary of file paths and their contents to provide context to the LLM.

        Returns:
            Dict[str, Any]: The generated plan as a dictionary, or an empty dictionary if an error occurs.
        """
        logger.info(f"Orchestrator {self.name} is generating a plan for: '{high_level_goal}'")
        if not self.llm or not self.team:
            logger.error("Orchestrator client or team not initialized. Cannot generate plan.")
            return {}

        # Construct a description of the available agents and their roles/goals
        team_description = "\n".join(
            f"- Name: '{agent.name}'\n"
            f"  Role: `{agent.role}`\n"
            f"  Goal: \"{agent.goal}\""
            for agent in self.team.values()
        )

        # Load the general planning prompt template
        t20_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Not used
        general_prompt_template = read_file(os.path.join(t20_root, "prompts", "general_planning.txt")).strip()
        planning_prompt_parts = [general_prompt_template.format(
            high_level_goal=high_level_goal,
            team_description=team_description
        )]

        # Combine prompt parts for the LLM call
        full_prompt_for_llm = "\n\n".join(planning_prompt_parts)

        logger.info(f"Orchestrator {self.name} Planning Prompt:\n{full_prompt_for_llm}")

        # Include file contents if provided
        if file_contents:
            file_section = [f"\n--- Files Content ---"]
            for file_path, content in file_contents.items():
                file_section.append(f"File: {file_path}\n```\n{content}\n```")
            planning_prompt_parts.append("\n".join(file_section))

        logger.debug("Planning prompt parts for LLM: %s", planning_prompt_parts)
        session.add_artifact("planning_prompt.txt", full_prompt_for_llm)

        try:
            response = self.llm.generate_content(
                model_name=self.model,
                contents="\n\n".join(planning_prompt_parts),
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
