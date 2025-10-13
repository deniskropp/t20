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

from runtime.custom_types import Plan, File

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
        logger.info(f"Orchestrator {self.name} is generating a plan for: '{high_level_goal}'")
        if not self.llm or not self.team:
            logger.error("Orchestrator client or team not initialized. Cannot generate plan.")
            return None

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

        # Format the planning prompt parts
        planning_prompt_parts = [general_prompt_template.format(
            high_level_goal=high_level_goal,
            team_description=team_description
        )]

        # Include file contents if provided
        file_section = []
        for file in files:
            file_section.append(f"\n--- File: '{file.path}'\n```\n{file.content}\n```")
        planning_prompt_parts.append("\n".join(file_section))

        logger.debug("Planning prompt parts for LLM: %s", planning_prompt_parts)

        # Combine prompt parts for the LLM call
        full_prompt_for_llm = "\n\n".join(planning_prompt_parts)
        logger.info(f"Orchestrator {self.name} Planning Prompt:\n{full_prompt_for_llm}")

        session.add_artifact("planning_prompt.txt", full_prompt_for_llm)

        try:
            response = self.llm.generate_content(
                model_name=self.model,
                contents="\n\n".join(planning_prompt_parts),
                system_instruction=self.system_prompt,
                temperature=0.0,
                response_mime_type='application/json', #if self.role == 'Prompt Engineer' else None
                response_schema=Plan
            )
            if isinstance(response, Plan):
                plan = response
            else:
                plan = Plan.model_validate_json(response or '{}')
        except (ValidationError, json.JSONDecodeError) as e:
            logger.exception(f"Error generating or validating plan for {self.name}: {e}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred during plan generation for {self.name}: {e}")
            return None

        return plan
