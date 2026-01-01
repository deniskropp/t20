"""This module defines the Orchestrator agent and its planning capabilities.

The Orchestrator is a specialized agent responsible for generating, managing,
and executing the workflow plan based on a high-level goal. This is being
refactored to move workflow execution to the System class.
"""

import os
import json
from typing import List, Dict, Optional, Tuple
import logging
from colorama import Fore, Style

from pydantic import BaseModel, Field, ValidationError

from t20.core.agent import Agent
from t20.core.core import Session
from t20.core.util import read_file

logger = logging.getLogger(__name__)

from t20.core.custom_types import Plan, File, AgentProfile


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
        general_prompt_template = read_file(os.path.join(t20_root, "assets", "prompts", "general_planning.txt")).strip()

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

    async def generate_plan(self, session: Session, high_level_goal: str, files: List[File] = []) -> Optional[Plan]:
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
        if not self.llm or not self.team:
            logger.error("Orchestrator client or team not initialized. Cannot generate plan.")
            return None

        planning_prompt = PlanningPrompt(agents=[t.profile for t in self.team.values()], files=files)

        logger.debug(f"Orchestrator '{self.profile.name}' is using: '{planning_prompt.model_dump_json()}'")
        logger.debug(f"Orchestrator '{self.profile.name}' is generating a plan for: '{high_level_goal}'")

        planning_prompt = planning_prompt.make(high_level_goal)

        print(f"\n{Fore.CYAN}Orchestrator '{self.profile.name}' Instructions:{Style.RESET_ALL}\n{self.system_instructions}")
        print(f"\n{Fore.CYAN}Orchestrator '{self.profile.name}' Planning:{Style.RESET_ALL}\n{planning_prompt}")

        session.add_artifact("planning_instructions.txt", self.system_instructions)
        session.add_artifact("planning_prompt.txt", planning_prompt)

        try:
            response = await self.llm.generate_content(
                model_name=self.model,
                contents=planning_prompt,
                system_instruction=self.system_instructions,
                temperature=0.0
            )

            print(f"\n{Fore.CYAN}Orchestrator '{self.profile.name}' Planning Response:{Style.RESET_ALL}\n{response}")

            session.add_artifact("planning_response.txt", response)

            response = await self.llm.generate_content(
                model_name=self.model,
                contents=planning_prompt,
                system_instruction=self.system_instructions,
                temperature=0.0,
                response_mime_type='application/json',
                response_schema=Plan
            )
            result = response or Plan(high_level_goal="[]", reasoning="", roles=[], tasks=[])

            session.add_artifact("planning_result.txt", result)

            if isinstance(result, str):
                result = Plan.model_validate_json(result)
        except (ValidationError, json.JSONDecodeError) as e:
            logger.exception(f"Error generating or validating plan for {self.profile.name}: {e}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred during plan generation for {self.profile.name}: {e}")
            return None

        print(f"\n{Fore.CYAN}Orchestrator '{self.profile.name}' Planning Result:{Style.RESET_ALL}\n{result.model_dump_json(indent=4)}")
        return result
