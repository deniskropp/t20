"""This module defines the core Agent class and related functionalities.

It includes the agent's lifecycle methods, task execution logic, and
helper functions for agent instantiation and discovery.
"""

import json as JSON
import uuid
from dataclasses import dataclass, field
import re
import logging
from typing import List, Dict, Any, Optional

from runtime.llm import LLM

from runtime.core import ExecutionContext, Session


logger = logging.getLogger(__name__)

from runtime.custom_types import AgentOutput

class Agent:
    """Represents a runtime agent instance."""
    name: str
    role: str
    goal: str
    model: str
    system_prompt: str
    llm: LLM

    def __init__(self, name, role, goal, model, system_prompt) -> None:
        self.name = name
        self.role = role
        self.goal = goal
        self.model = model
        self.system_prompt = system_prompt
        logger.info(f"Agent instance created: {self.name} (Role: {self.role}, Model: {self.model})")
        self.llm = LLM.factory(model)

    def update_system_prompt(self, new_prompt: str):
        """Updates the agent's system prompt."""

        self.system_prompt = new_prompt

        logger.info(f"Agent {self.name}'s system prompt updated:\n{self.system_prompt}\n")

    def execute_task(self, context: ExecutionContext) -> Optional[str]:
        """
        Executes a task using the Generative AI model based on the provided context.

        Args:
            context (ExecutionContext): The execution context containing goal, plan, and artifacts.

        Returns:
            Optional[str]: The result of the task execution as a string, or an error string.
        """

        task = context.current_step()

        context.record_artifact(f"{self.name}_prompt.txt", self.system_prompt)

        required_task_ids = ['none']
        required_task_ids.extend(task.requires)

        required_artifacts = {}

        if len(required_task_ids) != 0:
            for key, artifact in context.artifacts.items():
                logger.debug(f"Checking artifact from {key} with task ID {artifact.step.id}")
                if artifact.step.id in required_task_ids:
                    required_artifacts[key] = artifact

        previous_artifacts = "\n\n---\n\n".join(
            f"Artifact from {key} ({artifact.step.role})[{artifact.step.description}]:\n{artifact.content}"
            for key, artifact in required_artifacts.items()
        )

        task_prompt: List[str] = [
            f"The overall goal is: '{context.high_level_goal}'",
            f"Your role's specific goal is: '{self.goal}'\n"
            f"Your specific sub-task is: '{task.description}'",

            f"The team's roles are:\n    {context.plan}",
        ]

        if previous_artifacts:
            task_prompt.append(f"Please use the following outputs from the other agents as your input:\n\n{previous_artifacts}\n\n")

        task_prompt.append(
            f"Please execute your sub-task, keeping the overall goal and your role's specific goal in mind to ensure your output is relevant to the project."
        )

        #logger.info(f"Agent '{self.name}' is executing task: {task_prompt[1]}")
        #logger.info(f"Task requires outputs from task IDs: {required_task_ids}")
        #logger.info(
        #    f"Found {len(required_artifacts)} required artifacts from previous tasks. Previous artifacts preview: {previous_artifacts[:500]}"
        #)

        ret = self._run(context, "\n\n".join(task_prompt))
        logger.info(f"Agent '{self.name}' completed task: {task.description}")
        return ret


    def _run(self, context: ExecutionContext, prompt: str) -> Optional[str]:
        context.record_artifact(f"{self.name}_task.txt", prompt)

        try:
            response = self.llm.generate_content(   # ignore type
                model_name=self.model,
                contents=prompt,
                system_instruction=self.system_prompt,
                temperature=0.7,
                response_mime_type='application/json', #if self.role == 'Prompt Engineer' else None
                response_schema=AgentOutput
            )
            if isinstance(response, AgentOutput):
                result = response.model_dump_json()
                print(f"\n--- Output:\n{response.output}\n")
                if response.artifact and response.artifact.files:
                    for file in response.artifact.files:
                        print(f"\n--- File: {file.path}\n{file.content}\n")
                        context.session.add_artifact(file.path, file.content)
            else:
                result = response or '{}'

                if '```' in result:
                    match = re.search(r'```(json)?\s*([\s\S]*?)\s*```', result, re.IGNORECASE)
                    if match:
                        # Extract the JSON content from the markdown block
                        result = match.group(2).strip()

                json_data = JSON.loads(result)
                if isinstance(json_data, dict):
                    if "output" in json_data and json_data["output"] is not None:
                        output = JSON.dumps(json_data["output"], indent=4) if isinstance(json_data["output"], dict) else json_data["output"]
                        logger.info(f"Output:\n{output[:2000]}\n")

                    if "artifact" in json_data and json_data["artifact"] is not None:
                        if "files" in json_data["artifact"]:
                            for file_data in json_data["artifact"]["files"]:
                                if "path" in file_data and "content" in file_data:
                                    print(f"\n--- File: {file_data["path"]}")
                                    print(f"{file_data["content"]}")
                                    context.session.add_artifact(file_data["path"], file_data["content"])
                else:
                    logger.warning("Agent output is not in expected AgentOutput format. Processing as plain text.")
                    logger.info(f"Output: '\n{result[:2000]}\n'")

        except Exception as e:
            raise
            result = f"Error executing task for {self.name}: {e}"
            print(result)

        return result

def find_agent_by_role(agents: List[Agent], role: str) -> Optional[Agent]:
    """
    Finds an agent in a list by its role.

    Args:
        agents (List[Agent]): A list of Agent objects.
        role (str): The role of the agent to find.

    Returns:
        Optional[Agent]: The found Agent object, or None if not found.
    """
    logger.debug(f"Searching for agent with role: {role} in agents: {[agent.name for agent in agents]}")
    return next((agent for agent in agents if agent.role == role), None)
