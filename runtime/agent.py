"""Agent definitions and related utility functions."""

import json as JSON
import uuid
from dataclasses import dataclass, field
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
    team: Dict[str,'Agent'] = {}
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

        logger.info(f"Agent {self.name}'s system prompt updated.")

    def execute_task(self, context: ExecutionContext) -> Optional[str]:
        """
        Executes a task using the Generative AI model based on the provided context.

        Args:
            context (ExecutionContext): The execution context containing goal, plan, and artifacts.

        Returns:
            Optional[str]: The result of the task execution as a string, or an error string.
        """
        step = context.current_step()
        task_id = step.get("task_id", "none")
        task_description = step.get("task", "No task description provided.")
        logger.info(f"\n\n\nAgent {self.name} is executing task: {task_description}")

        context.record_artifact(f"{self.name}_prompt.txt", self.system_prompt)

        task_prompt: List[str] = [
            f"The overall goal is: '{context.high_level_goal}'",
            f"Your role's specific goal is: '{self.goal}'\n"
            f"Your specific sub-task is: '{task_description}'",

            f"The team's roles are:\n    {context.plan}",
        ]

        required_task_ids = step.get('requires', [])
        if required_task_ids:
            required_artifacts = {
                key: value for key, value in context.artifacts.items()
                if value['s'].get('task_id') in required_task_ids
            }
            if required_artifacts:
                previous_artifacts = "\n\n---\n\n".join(
                    f"Artifact from {key} ({value['s'].get('role')})[{value['s'].get('task_id')}]:\n{value['v']}"
                    for key, value in required_artifacts.items()
                )
                task_prompt.append(f"Please use the following outputs from the other agents as your input:\n\n{previous_artifacts}\n\n")

        task_prompt.append(
            f"Please execute your sub-task, keeping the overall goal and your role's specific goal in mind to ensure your output is relevant to the project."
        )


        context.record_artifact(f"{self.name}_task.txt", "\n\n".join(task_prompt))

        try:
            response = self.llm.generate_content(   # ignore type
                model_name=self.model,
                contents="\n\n".join(task_prompt),
                system_instruction=self.system_prompt,
                temperature=0.7,
                response_mime_type='application/json', #if self.role == 'Prompt Engineer' else None
                response_schema=AgentOutput
            )
            result = response or ''
            logger.info(f"\nAgent '{self.name}' completed task.")
            #logger.debug(f"\nOutput: '\n{result[:2000]}\n'")

            json_data = JSON.loads(response or '{}')
            if isinstance(json_data, dict) and "output" in json_data:
                if "files" in json_data and isinstance(json_data["files"], list):
                    for file_data in json_data["files"]:
                        if "name" in file_data and "content" in file_data:
                            context.session.add_artifact(file_data["name"], file_data["content"])
                try:
                    output = JSON.loads(json_data["output"])
                except JSON.JSONDecodeError:
                    output = json_data["output"]
                #if isinstance(result, dict):
                output = JSON.dumps(output, indent=4)
                logger.info(f"Output:\n{output[:2000]}\n")
            else:
                logger.warning("Agent output is not in expected AgentOutput format. Processing as plain text.")
                logger.info(f"Output: '\n{result[:2000]}\n'")
                #result = response.text or ''

        except Exception as e:
            result = f"Error executing task for {self.name}: {e}"
            print(result)

        return result

def instantiate_agent(agent_spec: Dict[str, Any], prompts: Dict[str, str], all_agent_specs: List[Dict[str, Any]]) -> Optional[Agent]:
    """
    Instantiates an Agent (or a subclass) based on the provided specification.

    Args:
        agent_spec (Dict[str, Any]): A dictionary containing the agent's specifications.
        prompts (Dict[str, str]): A dictionary of available system prompts.
        all_agent_specs (List[Dict[str, Any]]): A list of all agent specifications for team resolution.

    Returns:
        Optional[Agent]: An instantiated Agent object, or None if the prompt is not found.
    """
    prompt_key = f"{agent_spec['name'].lower()}_instructions.txt"
    if agent_spec.get('name') == 'Meta-AI':
        prompt_key = 'orchestrator_instructions.txt'

    if prompt_key not in prompts:
        logger.warning(f"Prompt for agent '{agent_spec['name']}' not found with key '{prompt_key}'. Empty system prompt will be used.")

    agent = Orchestrator(
        name=agent_spec.get('name', 'Unnamed Agent'),
        role=agent_spec.get('role', 'Agent'),
        goal=agent_spec.get('goal', ''),
        model=agent_spec.get('model', 'default-model'),
        system_prompt="" if prompt_key not in prompts else prompts[prompt_key]
    )

    if agent_spec.get('delegation') and 'team' in agent_spec:
        agent.team = {}
        for team_member_name in agent_spec['team']:
            member_spec = next((s for s in all_agent_specs if s['name'].lower() == team_member_name.lower()), None)
            if member_spec:
                member_agent = instantiate_agent(member_spec, prompts, all_agent_specs) # Recursive call
            else:
                logger.warning(f"Team member '{team_member_name}' not found in agent specs.")
                member_agent = instantiate_agent(agent_spec = {
                        'name': team_member_name, 'role': 'Unknown', 'goal': '', 'model': agent_spec.get('model', 'default-model'), 'system_prompt': ''
                    }, prompts=prompts, all_agent_specs=all_agent_specs) # Recursive call
            if member_agent:
                agent.team[team_member_name] = member_agent
    return agent

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


from runtime.orchestrator import Orchestrator
