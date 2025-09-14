"""This module provides a factory function for instantiating agents.

It centralizes the agent creation logic, decoupling it from the bootstrap
and agent modules to avoid circular dependencies.
"""

import logging
from typing import Any, Dict, List, Optional

from runtime.agent import Agent
from runtime.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


def instantiate_agent(
    agent_spec: Dict[str, Any],
    prompts: Dict[str, str],
    all_agent_specs: List[Dict[str, Any]],
) -> Optional[Agent]:
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
    if agent_spec.get("name") == "Meta-AI":
        prompt_key = "orchestrator_instructions.txt"

    if prompt_key not in prompts:
        logger.warning(
            f"Prompt for agent '{agent_spec['name']}' not found with key '{prompt_key}'. Empty system prompt will be used."
        )

    agent = Orchestrator(
        name=agent_spec.get("name", "Unnamed Agent"),
        role=agent_spec.get("role", "Agent"),
        goal=agent_spec.get("goal", ""),
        model=agent_spec.get("model", "default-model"),
        system_prompt="" if prompt_key not in prompts else prompts[prompt_key],
    )

    if agent_spec.get("delegation") and "team" in agent_spec:
        agent.team = {}
        for team_member_name in agent_spec["team"]:
            member_spec = next(
                (
                    s
                    for s in all_agent_specs
                    if s["name"].lower() == team_member_name.lower()
                ),
                None,
            )
            if member_spec:
                member_agent = instantiate_agent(
                    member_spec, prompts, all_agent_specs
                )  # Recursive call
            else:
                logger.warning(
                    f"Team member '{team_member_name}' not found in agent specs."
                )
                member_agent = instantiate_agent(
                    agent_spec={
                        "name": team_member_name,
                        "role": "Unknown",
                        "goal": "",
                        "model": agent_spec.get("model", "default-model"),
                        "system_prompt": "",
                    },
                    prompts=prompts,
                    all_agent_specs=all_agent_specs,
                )  # Recursive call
            if member_agent:
                agent.team[team_member_name] = member_agent
    return agent
