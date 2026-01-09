"""
KickLang Generation 2 Pipelines.

This module defines the high-level Pipeline class that integrates
t20.core.System with a Knowledge Graph backend for generational memory.
"""

import asyncio
import logging
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

from t20.core.system.system import System
from t20.core.data.graph_backend import PythonGraphBackend
from t20.core.common.types import Plan, File, Task

logger = logging.getLogger(__name__)

class PipelineConfig(BaseModel):
    """Configuration for the Pipeline."""
    root_dir: str
    default_model: str = "gemini-2.5-flash-lite"
    enable_tracing: bool = True

class Pipeline:
    """
    Represents a KickLang execution pipeline (Generation 2).
    
    Integrates the robust t20.core.System for agentic workflows with
    a GraphBackend for persistent, queryable execution traces (Generational Memory).
    """

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.system = System(root_dir=config.root_dir, default_model=config.default_model)
        self.trace_graph = PythonGraphBackend() if config.enable_tracing else None
        
        # Initialize System
        try:
            self.system.setup()
        except RuntimeError as e:
            logger.error(f"Failed to initialize System: {e}")
            raise

    async def run(self, goal: str, files: List[str] = []) -> Plan:
        """
        Executes the pipeline for a given goal.

        Args:
            goal (str): The high-level objective.
            files (List[str]): List of file paths to include as context.

        Returns:
            Plan: The executed plan and results.
        """
        logger.info(f"Pipeline started with goal: {goal}")

        # Prepare files
        input_files = []
        for fpath in files:
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    input_files.append(File(path=fpath, content=content, extension=fpath.split('.')[-1]))
            except Exception as e:
                logger.warning(f"Could not read file {fpath}: {e}")

        # Start System (Planning)
        plan = await self.system.start(high_level_goal=goal, files=input_files)
        
        if self.trace_graph:
            self._trace_plan(plan)

        # Execute Plan
        async for task, result in self.system.run(plan, files=input_files):
            if self.trace_graph:
                self._trace_task_execution(task, result)

        logger.info("Pipeline execution completed.")
        return plan

    def _trace_plan(self, plan: Plan):
        """Records the initial plan into the knowledge graph."""
        # Trace Goal
        self.trace_graph.add_concept({
            "id": "goal_root",
            "type": "Goal",
            "properties": {"description": plan.high_level_goal}
        })

        # Trace Tasks (Nodes)
        for task in plan.tasks:
            self.trace_graph.add_concept({
                "id": f"task_{task.id}",
                "type": "Task",
                "properties": {
                    "description": task.description,
                    "role": task.role,
                    "agent": task.agent
                }
            })
            
            # Link to Goal
            self.trace_graph.add_relationship({
                "source": "goal_root",
                "target": f"task_{task.id}",
                "type": "has_subtask"
            })
            
            # dependencies
            for dep in task.deps:
                 self.trace_graph.add_relationship({
                    "source": f"task_{dep}",
                    "target": f"task_{task.id}",
                    "type": "precedes"
                })

    def _trace_task_execution(self, task: Task, result: Optional[str]):
        """Updates the graph with execution results."""
        self.trace_graph.add_concept({
            "id": f"result_{task.id}",
            "type": "Result",
            "properties": {
                "output": result or "",
                "status": "completed" if result else "failed"
            }
        })
        
        self.trace_graph.add_relationship({
            "source": f"task_{task.id}",
            "target": f"result_{task.id}",
            "type": "produced"
        })
