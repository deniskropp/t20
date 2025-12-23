"""This module defines the core System class for the multi-agent runtime.

It encapsulates the state and behavior of the entire system, including
configuration loading, agent instantiation, and workflow execution.
"""

import os
import json
import yaml
import logging
import asyncio
from typing import Any, AsyncGenerator, List, Optional, Dict, Tuple
from pydantic import BaseModel

from runtime.core import Session, ExecutionContext
from runtime.agent import Agent
from runtime.orchestrator import Orchestrator
from runtime.log import setup_logging
from runtime.paths import AGENTS_DIR_NAME, CONFIG_DIR_NAME, PROMPTS_DIR_NAME, RUNTIME_CONFIG_FILENAME
from runtime.custom_types import Task, Plan, File
from runtime.message_bus import MessageBus

# Aetheria OS Components
from aetheria_os.prompt_store import PromptStore
from aetheria_os.agent_manager import AgentManager
from aetheria_os.workflow_engine import WorkflowEngine

# KickLang Components
from kicklang.interpreter import KickLangInterpreter

logger = logging.getLogger(__name__)

class SystemConfig(BaseModel):
    """
    Pydantic model for validating the structure of the system configuration.
    """
    logging_level: str = "INFO"
    default_model: str = "gemini-2.5-flash-lite"

class System:
    """
    Represents the entire multi-agent system, handling setup, execution, and state.
    """
    def __init__(self, root_dir: str, default_model: str = "gemini-2.5-flash-lite"):
        self.root_dir = root_dir
        self.default_model = default_model
        self.message_bus = MessageBus()
        self.config: SystemConfig = SystemConfig()
        self.session: Optional[Session] = None
        
        # Core Components
        self.prompt_store: Optional[PromptStore] = None
        self.agent_manager: Optional[AgentManager] = None
        self.workflow_engine: Optional[WorkflowEngine] = None
        self.kicklang: Optional[KickLangInterpreter] = None
        
        # Inject Knowledge Graph Interface
        from knowledge_graph.interface import KnowledgeGraphInterface
        self.kg = KnowledgeGraphInterface()

    def setup(self, orchestrator_name: Optional[str] = None) -> None:
        """
        Sets up the system by loading configurations and instantiating components.
        """
        logger.info("--- System Setup ---")
        print(f"Using default model: {self.default_model}")

        # Load Config
        config_path = os.path.join(self.root_dir, CONFIG_DIR_NAME, RUNTIME_CONFIG_FILENAME)
        logger.info(f"Loading configuration from: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            raw_config = yaml.safe_load(f)
            # Simple merge for now
            if raw_config:
                 self.config.logging_level = raw_config.get('logging_level', 'INFO')

        # Initialize Components
        prompts_dir = os.path.join(self.root_dir, PROMPTS_DIR_NAME)
        self.prompt_store = PromptStore(prompts_dir)
        
        agents_dir = os.path.join(self.root_dir, AGENTS_DIR_NAME)
        self.agent_manager = AgentManager(
            agents_dir=agents_dir, 
            prompt_store=self.prompt_store, 
            config=self.config, 
            message_bus=self.message_bus,
            default_model=self.default_model
        )
        self.agent_manager.load_agents() # Load agents and build teams
        
        if not self.agent_manager.agents:
            raise RuntimeError("No agents could be instantiated. System setup failed.")

        # Resolve Orchestrator
        orchestrator = self.agent_manager.orchestrator
        if orchestrator_name:
             orchestrator = next((a for a in self.agent_manager.agents if a.profile.name.lower() == orchestrator_name.lower()), None)
        
        if not orchestrator:
             raise RuntimeError("Orchestrator not found.")
        
        # Initialize Session
        self.session = Session(agents=self.agent_manager.agents, project_root="./", kg=self.kg)
        
        # Initialize Workflow Engine
        self.workflow_engine = WorkflowEngine(
            session=self.session, 
            agents=self.agent_manager.agents,
            orchestrator=orchestrator
        )
        
        # Initialize KickLang
        self.kicklang = KickLangInterpreter()
        
        logger.info("--- System Setup Complete ---")

    async def start(self, high_level_goal: str, files: List[File] = [], plan: Plan = None) -> Plan:
        if not self.workflow_engine:
             raise RuntimeError("System not setup.")
        
        if not plan:
             plan = await self.workflow_engine.generate_plan(high_level_goal, files)
        
        return plan

    async def run(self, plan: Plan, rounds: int = 1, files: List[File] = []) -> AsyncGenerator[Tuple[Task, Optional[str]], None]:
        if not self.workflow_engine:
             raise RuntimeError("System not setup.")
        
        context = ExecutionContext(session=self.session, plan=plan)
        # Record initial files
        from runtime.custom_types import Artifact as RunArtifact
        # Note: Importing Artifact here might conflict with the new Pydantic Artifact if not careful,
        # but custom_types.Artifact is a Pydantic model itself (likely different).
        # We should check custom_types.
        
        context.record_initial("files", RunArtifact(task='initial', files=files).model_dump_json())

        async for task, result in self.workflow_engine.run(plan, context):
            yield task, result
