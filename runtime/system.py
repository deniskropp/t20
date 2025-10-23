"""This module defines the core System class for the multi-agent runtime.

It encapsulates the state and behavior of the entire system, including
configuration loading, agent instantiation, and workflow execution.
"""

import os
import json
import yaml
from glob import glob

import logging
from typing import Any, Generator, List, Optional, Dict, Tuple

import concurrent

from .core import Session, ExecutionContext
from .agent import Agent, find_agent_by_role
from .orchestrator import Orchestrator
from .log import setup_logging
from .loader import load_agent_classes
from .paths import AGENTS_DIR_NAME, CONFIG_DIR_NAME, PROMPTS_DIR_NAME, RUNTIME_CONFIG_FILENAME

from .custom_types import AgentOutput, Artifact, Plan, File, Task
logger = logging.getLogger(__name__)

from .message_bus import MessageBus

class System:
    """
    Represents the entire multi-agent system, handling setup, execution, and state.
    """
    def __init__(self, root_dir: str, default_model: str = "gemini-2.5-flash-lite"):
        """
        Initializes the System.

        Args:
            root_dir (str): The root directory of the project.
            default_model (str): The default LLM model to use.
        """
        self.root_dir = root_dir
        self.default_model = default_model
        self.message_bus = MessageBus()
        self.config: dict = {}
        self.agents: List[Agent] = []
        self.session: Optional[Session] = None
        self.orchestrator: Optional[Orchestrator] = None
        self.completed_tasks: set = set()

    def setup(self, orchestrator_name: Optional[str] = None) -> None:
        """
        Sets up the system by loading configurations and instantiating agents.

        Args:
            orchestrator_name (str, optional): The name of the orchestrator to use.

        Raises:
            RuntimeError: If no agents or orchestrator can be set up.
        """
        logger.info("--- System Setup ---")
        print(f"Using default model: {self.default_model}")

        self.config = self._load_config(os.path.join(self.root_dir, CONFIG_DIR_NAME, RUNTIME_CONFIG_FILENAME))
        agent_specs = self._load_agent_templates(os.path.join(self.root_dir, AGENTS_DIR_NAME), self.config, self.default_model)
        prompts = self._load_prompts(os.path.join(self.root_dir, PROMPTS_DIR_NAME))
        agent_classes = load_agent_classes(os.path.join(self.root_dir, AGENTS_DIR_NAME))

        # Instantiate all agents
        all_agents = []
        for spec in agent_specs:
            spec["model"] = spec.get("model", self.default_model)
            agent = self._instantiate_agent(spec, prompts, agent_classes)
            if agent:
                all_agents.append(agent)

        # Build teams
        agents_by_name = {agent.profile.name.lower(): agent for agent in all_agents}
        for agent in all_agents:
            if isinstance(agent, Orchestrator):
                spec = next((s for s in agent_specs if s["name"].lower() == agent.profile.name.lower()), None)
                if spec and "team" in spec:
                    agent.team = {}
                    for team_member_name in spec["team"]:
                        team_member = agents_by_name.get(team_member_name.lower())
                        if team_member:
                            agent.team[team_member_name] = team_member
                        else:
                            logger.warning(f"Team member '{team_member_name}' for orchestrator '{agent.profile.name}' not found.")

        self.agents = all_agents

        if not self.agents:
            raise RuntimeError("No agents could be instantiated. System setup failed.")

        orchestrator: Optional[Agent] = None
        if orchestrator_name:
            orchestrator = next((agent for agent in self.agents if agent.profile.name.lower() == orchestrator_name.lower()), None)
        else:
            orchestrator = find_agent_by_role(self.agents, 'Orchestrator')

        if not orchestrator:
            error_msg = f"Orchestrator with name '{orchestrator_name}' not found." if orchestrator_name else "Orchestrator with role 'Orchestrator' not found."
            raise RuntimeError(f"{error_msg} System setup failed.")

        if not isinstance(orchestrator, Orchestrator):
            raise RuntimeError(f"Agent '{orchestrator.profile.name}' is not a valid Orchestrator instance. System setup failed.")

        self.orchestrator = orchestrator
        self.session = Session(agents=self.agents, project_root="./")
        logger.info("--- System Setup Complete ---")

    def start(self, high_level_goal: str, files: List[File] = [], plan: Plan = None) -> Plan:
        """
        Starts the system's main workflow, generating a plan if one is not provided.

        Args:
            high_level_goal (str): The high-level goal for the orchestrator to perform.
            files (List[File]): List of files to be used in the task.
            plan (Plan, optional): An optional pre-existing plan to use. If not provided,
                                   the orchestrator will generate one.

        Returns:
            Plan: The generated or provided plan.

        Raises:
            RuntimeError: If the system is not set up before running.
        """
        if not self.orchestrator or not self.session:
            raise RuntimeError("System is not set up. Please call setup() before start().")

        if not plan:
            plan = self.orchestrator.generate_plan(self.session, high_level_goal, files)
            if not plan:
                raise RuntimeError("Orchestration failed: Could not generate plan.")

        plan = Plan.model_validate(plan)
        if not plan:
            raise RuntimeError("Orchestration failed: Could not validate plan.")

        logger.debug(f"{plan.model_dump_json()}")

        if not plan or not plan.tasks or not plan.roles:
            raise RuntimeError("Orchestration failed: Could not find a valid plan.")

        print(f"\n\nInitial Plan: {plan.model_dump_json(indent=4)}\n\n\n")
        self.session.add_artifact("initial_plan.json", plan.model_dump_json(indent=4))

        return plan

    def run(self, plan: Plan, rounds: int = 1, files: List[File] = []) -> Generator[Tuple[Task, Optional[str]]]:
        """
        Runs the multi-agent workflow based on the provided plan.

        Args:
            plan (Plan): The execution plan generated by the orchestrator.
            rounds (int): The number of rounds to execute the workflow.
            files (List[File]): Initial files provided to the system.

        Yields:
            Tuple[Task, Optional[str]]: A tuple containing the executed task and its result.

        Raises:
            RuntimeError: If the system is not set up before running.
        """
        if not self.orchestrator or not self.session:
            raise RuntimeError("System is not set up. Please call start() before run().")

        logger.info("--- Starting Workflow ---")

        context = ExecutionContext(session=self.session, plan=plan)
        context.record_initial("files", Artifact(task='initial',files=files).model_dump_json())

        if plan.team and plan.team.prompts:
            logger.info(f"Plan provided new prompts.")
            for prompt_data in plan.team.prompts:
                self._update_agent_prompt(self.session, prompt_data.agent, prompt_data.system_prompt)

        dependency_graph = {task.id: task.requires for task in plan.tasks}
        self.completed_tasks = set()
        task_map = {task.id: task for task in plan.tasks}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {}
            while len(self.completed_tasks) < len(plan.tasks):
                ready_tasks = []
                for task_id, dependencies in dependency_graph.items():
                    if task_id not in self.completed_tasks and task_id not in futures:
                        if all(dep in self.completed_tasks for dep in dependencies):
                            ready_tasks.append(task_map[task_id])

                for task in ready_tasks:
                    futures[executor.submit(self._execute_task, task, context)] = task

                for future in concurrent.futures.as_completed(futures):
                    task = futures.pop(future)
                    try:
                        result = future.result()
                        self.completed_tasks.add(task.id)
                        yield task, result
                    except Exception as e:
                        logger.exception(f"Error executing task {task.id}: {e}")
                        yield task, f"Error executing task {task.id}: {e}"
        logger.info("--- Workflow Complete ---")

    def _execute_task(self, task: Task, context: ExecutionContext) -> Optional[str]:
        agent_name = task.agent
        team_by_name = {agent.profile.name: agent for agent in self.orchestrator.team.values()} if self.orchestrator.team else {}
        delegate_agent = team_by_name.get(agent_name)
        if not delegate_agent:
            delegate_agent = next((agent for agent in self.agents if agent.profile.name.lower() == agent_name.lower()), None)

        if not delegate_agent:
            logger.warning(f"No agent found with name '{agent_name}'. Execution will continue with the Orchestrator as the fallback agent.")
            delegate_agent = self.orchestrator

        logger.info(f"Agent '{delegate_agent.profile.name}' is executing step {task.id}: '{task.description}' (Role: {task.role})")

        result = delegate_agent.execute_task(context, task)
        if result:
            context.record_artifact(f"{delegate_agent.profile.name}_result.txt", result, task, True)
            try:
                agent_output = AgentOutput.model_validate_json(result)
                if agent_output.team and agent_output.team.prompts:
                    logger.info(f"Agent {delegate_agent.profile.name} provided new prompts.")
                    for prompt_data in agent_output.team.prompts:
                        self._update_agent_prompt(self.session, prompt_data.agent, prompt_data.system_prompt)
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Could not parse agent output as AgentOutput: {e}. Treating as plain text.")
        return result

    def _update_agent_prompt(self, session: Session, agent_name: str, new_prompt: str) -> None:
        """
        Updates an agent's system prompt.

        Args:
            session (Session): The current session object.
            agent_name (str): The name or role of the agent to update.
            new_prompt (str): The new system prompt.
        """
        if not (agent_name and new_prompt):
            return

        if not (self.orchestrator and self.orchestrator.team):
            logger.warning("Orchestrator or its team is not initialized. Cannot update agent prompt.")
            return

        # Combine team agents and session agents for a comprehensive search, ensuring uniqueness
        all_agents = {agent.profile.name: agent for agent in list(self.orchestrator.team.values()) + session.agents}.values()

        # First, try to find by name
        target_agent = next((agent for agent in all_agents if agent.profile.name.lower() == agent_name.lower()), None)

        # If not found by name, try to find by role
        if not target_agent:
            target_agent = next((agent for agent in all_agents if agent.profile.role.lower() == agent_name.lower()), None)

        if target_agent:
            target_agent.update_system_prompt(new_prompt)
            logger.info(f"Agent '{target_agent.profile.name}' (matched by '{agent_name}') system prompt updated.")
        else:
            logger.warning(f"Target agent '{agent_name}' not found for prompt update.")

    def _instantiate_agent(self, agent_spec: Dict[str, Any], prompts: Dict[str, str], agent_classes: Dict[str, Any]) -> Optional[Agent]:
        """
        Instantiates an Agent (or a subclass) based on the provided specification.

        Args:
            agent_spec (Dict[str, Any]): A dictionary containing the agent's specifications.
            prompts (Dict[str, str]): A dictionary of available system prompts.
            agent_classes (Dict[str, Any]): A dictionary of available agent classes.

        Returns:
            Optional[Agent]: An instantiated Agent object, or None if the prompt is not found.
        """
        prompt_key = f"{agent_spec['name'].lower()}_instructions.txt"
        system_prompt = prompts.get(prompt_key, "")
        if not system_prompt:
            logger.warning(
                f"Prompt for agent '{agent_spec['name']}' not found with key '{prompt_key}'. Empty system prompt will be used."
            )

        agent_class_name = agent_spec.get("agent_class")
        if agent_class_name and agent_class_name in agent_classes:
            agent_class = agent_classes[agent_class_name]
        else:
            agent_class = Orchestrator if agent_spec.get("delegation") else Agent
            
        return agent_class(
            name=agent_spec.get("name", "Unnamed Agent"),
            role=agent_spec.get("role", "Agent"),
            goal=agent_spec.get("goal", ""),
            model=agent_spec.get("model", self.default_model),
            system_prompt=system_prompt,
            message_bus=self.message_bus,
        )

    def _load_config(self, config_path: str) -> Any:
        """
        Loads the runtime configuration from a YAML file.

        Args:
            config_path (str): The absolute path to the configuration file.

        Returns:
            dict: The loaded configuration as a dictionary.
        """
        logger.info(f"Loading configuration from: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _load_agent_templates(self, agents_dir: str, config: dict, default_model: str) -> List[Dict[str, Any]]:
        """
        Loads all agent specifications from YAML files within a specified directory.

        Args:
            agents_dir (str): The absolute path to the directory containing agent YAML files.

        Returns:
            list: A list of dictionaries, where each dictionary represents an agent's specification.
        """
        logger.info(f"Loading agent templates from: {agents_dir}")
        agent_files = glob(os.path.join(agents_dir, '*.yaml'))
        templates = []
        for agent_file in agent_files:
            with open(agent_file, 'r', encoding='utf-8') as f:
                template = yaml.safe_load(f)
                # Resolve prompt path relative to the agent file's directory
                if 'system_prompt' in template and template['system_prompt']:
                    base_dir = os.path.dirname(agent_file)
                    prompt_path = os.path.abspath(os.path.join(base_dir, template['system_prompt']))
                    template['system_prompt_path'] = prompt_path
                template["model"] = default_model
                templates.append(template)
        logger.info(f"{len(templates)} agent templates loaded.")
        return templates

    def _load_prompts(self, prompts_dir: str) -> Dict[str, str]:
        """
        Loads all system prompts from text files within a specified directory.

        Args:
            prompts_dir (str): The absolute path to the directory containing prompt text files.

        Returns:
            dict: A dictionary where keys are prompt filenames (e.g., 'agent_instructions.txt')
                and values are the content of the prompt files.
        """
        logger.info(f"Loading prompts from: {prompts_dir}")
        prompt_files = glob(os.path.join(prompts_dir, '*.txt'))
        prompts = {}
        for prompt_file in prompt_files:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                # Use the absolute path as the key for reliable lookup
                prompts[os.path.basename(prompt_file)] = f.read()
        logger.info(f"{len(prompts)} prompts loaded.")
        return prompts
