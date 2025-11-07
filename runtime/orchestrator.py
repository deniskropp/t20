"""This module defines the Orchestrator agent and its planning capabilities.

The Orchestrator is a specialized agent responsible for generating, managing,
and executing the workflow plan based on a high-level goal. This is being
refactored to move workflow execution to the System class.
"""

import os
import json
from typing import List, Dict, Optional, Tuple
import logging

from pydantic import BaseModel, Field, ValidationError

from runtime.agent import Agent
from runtime.core import Session
from runtime.util import read_file

logger = logging.getLogger(__name__)

from runtime.custom_types import Plan, File, AgentProfile


class PlanningPrompt(BaseModel):
    agents: list[AgentProfile] = Field(..., default_factory=list)
    files: list[File] = Field(..., default_factory=list)

    def make(self, goal: str) -> str:
        # Construct a description of the available agents and their roles/goals
        team_description = "\n".join(
            f"- Name: '{agent.name}'\n"
            f"  Role: `{agent.role}`\n"
            f"  Goal: \"{agent.goal}\""
            for agent in self.agents
        )

        # Load the general planning prompt template
        t20_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Not used
        general_prompt_template = read_file(os.path.join(t20_root, "prompts", "general_planning.txt")).strip()

        # Format the planning prompt parts
        planning_prompt_parts = [general_prompt_template.format(
            high_level_goal=goal,
            team_description=team_description
        )]

        # Include file contents if provided
        file_section = []
        for file in self.files:
            file_section.append(f"⫻context/file:{file.path}\n{file.content}\n\n\n")
        planning_prompt_parts.append("\n".join(file_section))

        logger.debug("Planning prompt parts for LLM: %s", planning_prompt_parts)

        # Combine prompt parts for the LLM call
        return "\n\n\n".join(planning_prompt_parts)


class Orchestrator(Agent):
    """An agent responsible for creating and managing a plan for multi-agent workflows."""
    team: Dict[str,Agent] = {}

    def generate_plan(self, session: Session, high_level_goal: str, files: List[File] = []) -> Optional[Plan]:
        """
        Invokes the language model to get a structured plan for the given high-level goal.
        The plan includes a sequence of tasks and the roles responsible for them.

        Args:
            session (Session): The current session object.
            high_level_goal (str): The high-level goal for which to generate a plan.
            file_contents (List[Tuple[str, str]]): A list of file paths and their contents to provide context to the LLM.

        Returns:
            Optional[Plan]: The generated plan as a Pydantic object, or None if an error occurs.
        """
        logger.info(f"Orchestrator {self.profile.name} is generating a plan for: '{high_level_goal}'")
        if not self.llm or not self.team:
            logger.error("Orchestrator client or team not initialized. Cannot generate plan.")
            return None

        planning_prompt = f"""
You are an expert orchestrator. Your goal is to break down a high-level goal into a detailed, actionable plan for a team of specialized agents.
The plan should be a sequence of tasks, each assigned to a specific agent role.

Here's the high-level goal: '{high_level_goal}'

Here are the available agents and their roles:
{json.dumps([{"name": agent.profile.name, "role": agent.profile.role, "goal": agent.profile.goal} for agent in self.team.values()], indent=4)}

Here are the files provided by the user:
{json.dumps([file.model_dump() for file in files], indent=4)}

Your plan should adhere to the following structure (Pydantic Plan model):
{Plan.model_json_schema(by_alias=False, mode='serialization')}

Key considerations for your plan:
1.  **Break down the goal**: Decompose the `high_level_goal` into smaller, manageable `tasks`.
2.  **Assign roles**: Each `task` must be assigned to an `agent` by its `name` and/or `role`. Ensure the assigned agent's goal aligns with the task's requirements.
3.  **Dependencies**: Define `requires` for each task, indicating which previous tasks must be completed before the current one can start. Use the `id` of the preceding tasks. The first task should have `requires: []`.
4.  **Comprehensive**: Ensure all aspects of the `high_level_goal` are covered by the tasks, hence `reasoning`.
5.  **Logical flow**: The sequence of tasks should be logical and progressive towards achieving the overall goal.
6.  **Output**: Your response MUST be a JSON object that strictly conforms to the `Plan` schema.
7.  **Team Updates (Optional)**: If necessary, you can include `team` updates in the plan, such as new `system_prompts` for agents or general `notes` about team coordination.
    -   If you update a `system_prompt`, ensure the `agent` name matches an existing agent exactly.
    -   The `system_prompt` should be the full, new system prompt, not just a diff.
"""

        planning_prompt = PlanningPrompt(agents=[t.profile for t in self.team.values()], files=files).make(high_level_goal)

        logger.info(f"Orchestrator {self.profile.name} Planning Prompt:\n{planning_prompt}")

        session.add_artifact("planning_prompt.txt", planning_prompt)

#        response = self.llm.generate_content(
#            model_name=self.model,
#            contents=planning_prompt,
#            system_instruction=self.system_instruction,
#            temperature=0.0
#        )

#        session.add_artifact("planning_response.txt", response)

        try:
            response = self.llm.generate_content(
                model_name=self.model,
                contents=planning_prompt,
                system_instruction=self.system_instruction,
                temperature=0.0,
                response_mime_type='application/json',
                response_schema=Plan
            )
            if isinstance(response, Plan):
                plan = response
            else:
                plan = Plan.model_validate_json(response or '{}')
        except (ValidationError, json.JSONDecodeError) as e:
            logger.exception(f"Error generating or validating plan for {self.profile.name}: {e}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred during plan generation for {self.profile.name}: {e}")
            return None

        return plan
