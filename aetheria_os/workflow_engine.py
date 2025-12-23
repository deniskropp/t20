"""
Workflow Engine
---------------
Manages the execution of the agent workflow.
"""

import asyncio
import logging
from typing import List, Optional, AsyncGenerator, Tuple

from runtime.core import Session, ExecutionContext
from runtime.custom_types import Task, Plan, File, AgentOutput, Artifact
from runtime.task_manager import TaskManager
from runtime.agent import Agent
from runtime.orchestrator import Orchestrator

logger = logging.getLogger(__name__)

class WorkflowEngine:
    def __init__(self, session: Session, agents: List[Agent], orchestrator: Orchestrator):
        self.session = session
        self.agents = agents
        self.orchestrator = orchestrator

    async def generate_plan(self, high_level_goal: str, files: List[File] = []) -> Plan:
        if not self.orchestrator:
             raise RuntimeError("Orchestrator not available.")
        
        plan = await self.orchestrator.generate_plan(self.session, high_level_goal, files)
        if not plan:
             raise RuntimeError("Plan generation failed.")
        
        plan = Plan.model_validate(plan)
        self.session.add_artifact("initial_plan.json", plan.model_dump())
        return plan

    async def run(self, plan: Plan, context: ExecutionContext) -> AsyncGenerator[Tuple[Task, Optional[str]], None]:
        task_manager = TaskManager(plan)
        running_tasks = {}

        while not task_manager.is_all_completed():
            ready_tasks = task_manager.get_ready_tasks()
            
            # Filter running
            running_ids = {t.id for t in running_tasks.values()}
            ready_tasks = [t for t in ready_tasks if t.id not in running_ids]

            for task in ready_tasks:
                task_manager.mark_running(task.id)
                coro = self._execute_task(task, context)
                running_tasks[asyncio.create_task(coro)] = task

            if not running_tasks:
                if not task_manager.is_all_completed():
                     logger.error("Workflow stuck.")
                     break
                else:
                    break

            done, pending = await asyncio.wait(running_tasks.keys(), return_when=asyncio.FIRST_COMPLETED)

            for future in done:
                task = running_tasks.pop(future)
                try:
                    result = await future
                    task_manager.mark_completed(task.id, result)
                    yield task, result
                except Exception as e:
                    logger.exception(f"Error executing task {task.id}: {e}")
                    task_manager.mark_failed(task.id, str(e))
                    yield task, f"Error: {e}"

    async def _execute_task(self, task: Task, context: ExecutionContext) -> Optional[str]:
        # Simple delegation logic
        delegate_agent = next((a for a in self.agents if a.profile.name.lower() == task.agent.lower()), self.orchestrator)
        
        logger.info(f"Executing task {task.id} with agent {delegate_agent.profile.name}")
        result = await delegate_agent.execute_task(context, task)
        
        # Result handling (simplified from System)
        if result:
            context.record_artifact(f"{delegate_agent.profile.name}_result.txt", result, task, True)
            try:
                # Try to update prompts if response contains them
                agent_output = AgentOutput.model_validate_json(result)
                if agent_output.team and agent_output.team.prompts:
                     self._update_prompts(agent_output.team.prompts, context.session)
            except:
                pass
        return result

    def _update_prompts(self, prompts_data, session):
        # Placeholder for dynamic prompt update logic
        pass

