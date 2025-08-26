"""Agent definitions and related utility functions."""

import json as JSON
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from colorama import Fore, Style, init
from runtime.llm import LLM

from runtime.core import ExecutionContext, Session

# Initialize colorama for cross-platform colored output
init()

from runtime.types import AgentOutput

class Agent:
    """Represents a runtime agent instance."""
    name: str
    role: str
    goal: str
    model: str
    system_prompt: str
    team: Optional[Dict[str,'Agent']] = {}

    def __init__(self, name, role, goal, model, system_prompt) -> None:
        self.name = name
        self.role = role
        self.goal = goal
        self.model = model
        self.system_prompt = system_prompt
        print(f"{Fore.YELLOW}Agent instance created: {self.name} (Role: {self.role}, Model: {self.model}){Style.RESET_ALL}")

    def update_system_prompt(self, new_prompt: str):
        """Updates the agent's system prompt."""

        self.system_prompt = new_prompt

        print(f"{Fore.WHITE}Agent {self.name}'s system prompt updated.{Style.RESET_ALL}")

    def execute_task(self, context: ExecutionContext) -> Optional[str]:
        """
        Executes a task using the Generative AI model based on the provided context.

        Args:
            context (ExecutionContext): The execution context containing goal, plan, and artifacts.

        Returns:
            Optional[str]: The result of the task execution, or None if an error occurs.
        """
        step = context.current_step()
        task_id = step.get("task_id", "none")
        task_description = step.get("task", "No task description provided.")
        print(f"\n\n\n{Fore.GREEN}Agent {self.name} is executing task{Style.RESET_ALL}: {task_description}")

        context.record_artifact(f"{self.name}_prompt.txt", self.system_prompt)

        task_prompt: List[str] = [
            f"The overall goal is: '{context.high_level_goal}'",
            f"Your role's specific goal is: '{self.goal}'\n"
            f"Your specific sub-task is: '{task_description}'",

            f"The team's roles are:\n    {context.plan}",
        ]

        previous_artifacts = "\n\n---\n\n".join(
            f"Artifact from {key} ({value['s'].get("role")})[{value['s'].get("task_id")}]:\n{value['v']}"
            for key, value in context.artifacts.items()
        )
        if previous_artifacts:
            task_prompt.append(f"Please use the following outputs from the other agents as your input:\n\n{previous_artifacts}\n\n")

        task_prompt.append(
            f"Please execute your sub-task, keeping the overall goal and your role's specific goal in mind to ensure your output is relevant to the project."
        )


        context.record_artifact(f"{self.name}_task.txt", "\n\n".join(task_prompt))

        try:
            llm = LLM.factory()
            response = llm.generate_content(   # ignore type
                model_name=self.model,
                contents="\n\n".join(task_prompt),
                system_instruction=self.system_prompt,
                temperature=0.7,
                response_mime_type='application/json', #if self.role == 'Prompt Engineer' else None
                response_schema=AgentOutput
            )
            result = response or ''
            print(f"\n{Fore.BLUE}Agent '{self.name}' completed task.{Style.RESET_ALL}")
            #print(f"\n{Fore.BLUE}Output:{Style.RESET_ALL} '\n{result[:2000]}\n'")

            json = JSON.loads(response or '{}')
            if isinstance(json, dict) and "output" in json:
                if "files" in json and isinstance(json["files"], list):
                    for file_data in json["files"]:
                        if "name" in file_data and "content" in file_data:
                            context.session.add_artifact(file_data["name"], file_data["content"])
                try:
                    output = JSON.loads(json["output"])
                except JSON.JSONDecodeError:
                    output = json["output"]
                #if isinstance(result, dict):
                output = JSON.dumps(output, indent=4)
                print(f"{Fore.BLUE}Output:{Style.RESET_ALL}\n{output[:2000]}\n")
            else:
                print(f"{Fore.RED}Warning: Agent output is not in expected AgentOutput format. Processing as plain text.{Style.RESET_ALL}")
                print(f"{Fore.BLUE}Output:{Style.RESET_ALL} '\n{result[:2000]}\n'")
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
        print(f"{Fore.RED}Warning: Prompt for agent '{agent_spec['name']}' not found with key '{prompt_key}'{Style.RESET_ALL}. Skipping.")
        return None

    agent_class = Orchestrator if agent_spec.get('role') == 'Orchestrator' else Agent
    """ """
    """ """
    agent = agent_class(
        name=agent_spec.get('name', 'Unnamed Agent'),
        role=agent_spec.get('role', 'Agent'),
        goal=agent_spec.get('goal', ''),
        model=agent_spec.get('model', 'default-model'),
        system_prompt=prompts[prompt_key]
    )

    if agent_spec.get('delegation') and 'team' in agent_spec:
        agent.team = {}
        for team_member_name in agent_spec['team']:
            member_spec = next((s for s in all_agent_specs if s['name'].lower() == team_member_name.lower()), None)
            if member_spec:
                """ """
                """ """
                member_agent = instantiate_agent(member_spec, prompts, all_agent_specs) # Recursive call
                if member_agent:
                    agent.team[team_member_name] = member_agent
            else:
                print(f"{Fore.RED}Warning: Team member '{team_member_name}' not found in agent specs.{Style.RESET_ALL}")
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
    print("\n", f"Searching for orchestrator with role: {role} in agents: {[agent.name for agent in agents]}")
    return next((agent for agent in agents if agent.role == role), None)


from runtime.orchestrator import Orchestrator # Import Session and ExecutionContext
