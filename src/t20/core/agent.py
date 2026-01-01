"""This module defines the core Agent class and related functionalities.

It includes the agent's lifecycle methods, task execution logic, and
helper functions for agent instantiation and discovery.
"""

import json
import uuid
from dataclasses import dataclass, field
import re
import logging
from typing import List, Dict, Any, Optional

from t20.core.llm import LLM

from t20.core.core import ExecutionContext, Session


logger = logging.getLogger(__name__)

from t20.core.custom_types import AgentOutput, Task, AgentProfile, Feedback

from t20.core.message_bus import MessageBus

class Agent:
    """Represents a runtime agent instance."""
    profile: AgentProfile
    model: str
    system_prompt: str
    llm: LLM
    message_bus: MessageBus

    def __init__(self, name: str, role: str, goal: str, model: str, system_prompt: str, message_bus: MessageBus) -> None:
        self.profile = AgentProfile(name=name, role=role, goal=goal)
        self.model = model
        self.system_instructions = system_prompt
        self.system_prompt = system_prompt
        self.message_bus = message_bus
        logger.debug(f"Agent instance created: {self.profile.name} (Role: {self.profile.role}, Model: {self.model})")
        self.llm = LLM.factory(model)

    def subscribe(self, topic: str, callback: Any) -> None:
        """Subscribes to a topic on the message bus."""
        self.message_bus.subscribe(topic, callback)

    def publish(self, topic: str, message: Any) -> None:
        """Publishes a message to a topic on the message bus."""
        self.message_bus.publish(topic, message)

    def receive_feedback(self, context: ExecutionContext, feedback: Feedback):
        """Receives and stores feedback about a task execution."""
        feedback_artifact_name = f"feedback/{feedback.task_id}_{feedback.agent_name}_feedback.json"
        context.session.add_artifact(feedback_artifact_name, feedback.model_dump_json(indent=4))
        logger.info(f"Feedback received and stored for task {feedback.task_id}")

    def update_system_prompt(self, new_prompt: str) -> None:
        """Updates the agent's system prompt."""

        #self.system_instructions=f"{new_prompt}\n\n---\n\n{self.system_prompt}\n"
        self.system_instructions=f"{new_prompt}"

        logger.debug(f"Agent '{self.profile.name}' system prompt updated:\n{new_prompt}\n")

    async def execute_task(self, context: ExecutionContext, task: Task) -> Optional[str]:
        """
        Executes a task using the Generative AI model based on the provided context.

        Args:
            context (ExecutionContext): The execution context containing goal, plan, and artifacts.
            task (Task): The task to execute.

        Returns:
            Optional[str]: The result of the task execution as a string, or an error string.
        """
        context.record_artifact(f"{self.profile.name}_instructions.txt", self.system_instructions, task)

        required_task_ids = ['initial']
        required_task_ids.extend(task.deps)

        required_artifacts = []

        if len(required_task_ids) != 0:
            for key, artifact in context.items.items():
                logger.debug(f"Checking artifact from {key} with task ID {artifact.step.id}")
                if artifact.step.id in required_task_ids:
                    required_artifacts.append(artifact)

        previous_artifacts = "\n\n".join(
            #f"--- Artifact '{artifact.name}' from ({artifact.step.role}) in [{artifact.step.id}]:\n{artifact.content}"
            f"⫻context/artifact:{artifact.name}/{artifact.step.id}\n{artifact.content}"
            for artifact in required_artifacts
        )

        task_prompt: List[str] = [
            f"The overall goal is: '{context.plan.high_level_goal}'",
            f"Your role's specific goal is: '{self.profile.goal}'\n"
            f"Your specific sub-task is: '{task.description}'",

            f"The team's roles are:\n    {context.plan.model_dump_json()}",
        ]

        if previous_artifacts:
            #task_prompt.append(f"Please use the following outputs from the other agents as your input:\n\n{previous_artifacts}\n\n")
            task_prompt.append(f"{previous_artifacts}\n\n")

        task_prompt.append(
            f"Please execute your sub-task, keeping the overall goal and your role's specific goal in mind to ensure your output is relevant to the project."
        )

        prompt = "\n\n".join(task_prompt)

        context.record_artifact(f"{self.profile.name}_prompt.txt", prompt, task)

        ret = await self._run(prompt)

        logger.info(f"Agent '{self.profile.name}' completed task: {task.description}")

        print(f"\n====== Task '{task.id}' <= {task.deps} ======\n[{task.agent} | {task.role}] \"{task.description}\"\n")

        response = AgentOutput.model_validate_json(ret)

        print(f"\n--- Output:\n{response.output}\n")
        if response.artifact and response.artifact.files:
            for file in response.artifact.files:
                print(f"\n--- File: {file.path}\n{file.content}\n")
                context.session.add_artifact(file.path, file.content)
        if response.team:
            print(f"\n--- Team:\n\"{response.team.notes}\"")
            if response.team.prompts:
                print(f"\n{"".join(f"{p.agent} | {p.role}\n  {p.system_prompt}\n\n" for p in response.team.prompts)}")
        if response.reasoning:
            print(f"\n--- Reasoning:\n{response.reasoning}\n")

        return ret


    async def _run(self, prompt: str) -> Optional[str]:
        try:
            response = await self.llm.generate_content(
                model_name=self.model,
                contents=prompt,
                system_instruction=self.system_instructions,
                temperature=0.1,
                response_mime_type='application/json',
                response_schema=AgentOutput
            )

            if isinstance(response, AgentOutput):
                result = response.model_dump_json(indent=4)
            else:
                if isinstance(response, str):
                    result = response
                else:
                    result = json.dumps(response)

        except Exception as e:
            logger.exception(f"Error executing task for {self.profile.name}: {e}")
            return f"Error executing task for {self.profile.name}: {e}"

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
    logger.debug(f"Searching for agent with role: {role} in agents: {[agent.profile.name for agent in agents]}")
    return next((agent for agent in agents if agent.profile.role == role), None)
