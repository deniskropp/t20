"""
Agent Manager
-------------
Manages the lifecycle, instantiation, and retrieval of agents.
"""

import os
import yaml
import logging
from glob import glob
from typing import List, Dict, Any, Optional

from runtime.agent import Agent, find_agent_by_role
from runtime.orchestrator import Orchestrator
from runtime.message_bus import MessageBus
from runtime.loader import load_agent_classes
from aetheria_os.prompt_store import PromptStore

logger = logging.getLogger(__name__)

class AgentManager:
    def __init__(self, agents_dir: str, prompt_store: PromptStore, config: Any, message_bus: MessageBus, default_model: str):
        self.agents_dir = agents_dir
        self.prompt_store = prompt_store
        self.config = config
        self.message_bus = message_bus
        self.default_model = default_model
        self.agents: List[Agent] = []
        self.orchestrator: Optional[Orchestrator] = None

    def load_agents(self) -> None:
        """
        Loads agent templates and instantiates agents.
        """
        agent_specs = self._load_templates()
        agent_classes = load_agent_classes(self.agents_dir)
        
        all_agents = []
        for spec in agent_specs:
            spec["model"] = spec.get("model", self.default_model)
            agent = self._instantiate_agent(spec, agent_classes)
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
        
        self.agents = all_agents
        self.orchestrator = find_agent_by_role(self.agents, 'Orchestrator')

    def _load_templates(self) -> List[Dict[str, Any]]:
        logger.info(f"Loading agent templates from: {self.agents_dir}")
        if not os.path.exists(self.agents_dir):
             logger.warning(f"Agents directory not found: {self.agents_dir}")
             return []

        agent_files = glob(os.path.join(self.agents_dir, '*.yaml'))
        templates = []
        for agent_file in agent_files:
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    template = yaml.safe_load(f)
                    templates.append(template)
            except Exception as e:
                logger.error(f"Error loading agent template {agent_file}: {e}")
        return templates

    def _instantiate_agent(self, agent_spec: Dict[str, Any], agent_classes: Dict[str, Any]) -> Optional[Agent]:
        prompt_key = f"{agent_spec['name'].lower()}_instructions.txt"
        system_prompt = self.prompt_store.get_prompt(prompt_key)
        
        agent_class_name = agent_spec.get("agent_class")
        agent_class = agent_classes.get(agent_class_name, Agent)
        if agent_spec.get("delegation"):
             agent_class = Orchestrator

        return agent_class(
            name=agent_spec.get("name", "Unnamed Agent"),
            role=agent_spec.get("role", "Agent"),
            goal=agent_spec.get("goal", ""),
            model=agent_spec.get("model", self.default_model),
            system_prompt=system_prompt,
            message_bus=self.message_bus,
        )
