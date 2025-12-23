import logging
from typing import List, Dict, Set, Optional
from enum import Enum
import asyncio

from runtime.custom_types import Task, Plan

logger = logging.getLogger(__name__)

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"

class TaskManager:
    """
    Manages the lifecycle of tasks, including state transitions and dependency resolution.
    """
    def __init__(self, plan: Plan):
        self.plan = plan
        self.tasks: Dict[str, Task] = {t.id: t for t in plan.tasks}
        self.task_states: Dict[str, TaskStatus] = {t.id: TaskStatus.PENDING for t in plan.tasks}
        self.dependencies: Dict[str, List[str]] = {t.id: t.deps for t in plan.tasks}
        self.results: Dict[str, str] = {}

    def get_ready_tasks(self) -> List[Task]:
        """Returns a list of tasks that are READY to be executed."""
        ready_tasks = []
        for task_id, state in self.task_states.items():
            if state == TaskStatus.PENDING:
                if self._are_dependencies_met(task_id):
                    self.transition_state(task_id, TaskStatus.READY)
                    ready_tasks.append(self.tasks[task_id])
            elif state == TaskStatus.READY:
                ready_tasks.append(self.tasks[task_id])
        return ready_tasks

    def _are_dependencies_met(self, task_id: str) -> bool:
        """Checks if all dependencies for a task are COMPLETED."""
        deps = self.dependencies.get(task_id, [])
        return all(self.task_states.get(dep) == TaskStatus.COMPLETED for dep in deps)

    def transition_state(self, task_id: str, new_state: TaskStatus):
        """Transitions a task to a new state."""
        old_state = self.task_states.get(task_id)
        if old_state != new_state:
            logger.info(f"Task {task_id} transition: {old_state} -> {new_state}")
            self.task_states[task_id] = new_state

    def mark_running(self, task_id: str):
        self.transition_state(task_id, TaskStatus.RUNNING)

    def mark_completed(self, task_id: str, result: str):
        self.results[task_id] = result
        self.transition_state(task_id, TaskStatus.COMPLETED)

    def mark_failed(self, task_id: str, error: str):
        self.results[task_id] = error
        self.transition_state(task_id, TaskStatus.FAILED)

    def is_all_completed(self) -> bool:
        return all(state == TaskStatus.COMPLETED for state in self.task_states.values())
