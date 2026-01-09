import logging
from typing import List, Dict, Set, Optional
from enum import Enum
import asyncio

from t20.core.custom_types import Task, Plan

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
    Supports Hierarchical Task Networks (HTN) by flattening subtasks and managing parent states.
    """
    def __init__(self, plan: Plan):
        self.plan = plan
        self.tasks: Dict[str, Task] = {}
        self.task_states: Dict[str, TaskStatus] = {}
        self.dependencies: Dict[str, List[str]] = {}
        self.parent_map: Dict[str, str] = {} # child_id -> parent_id
        self.children_map: Dict[str, List[str]] = {} # parent_id -> [child_ids]
        self.results: Dict[str, str] = {}

        self._flatten_tasks(plan.tasks)

    def _flatten_tasks(self, tasks: List[Task], parent_id: Optional[str] = None):
        """Recursively registers tasks and their relationships."""
        for task in tasks:
            if task.id in self.tasks:
                logger.warning(f"Duplicate task ID detected: {task.id}. This may cause issues.")
            
            self.tasks[task.id] = task
            self.task_states[task.id] = TaskStatus.PENDING
            self.dependencies[task.id] = task.deps
            
            if parent_id:
                self.parent_map[task.id] = parent_id
                if parent_id not in self.children_map:
                    self.children_map[parent_id] = []
                self.children_map[parent_id].append(task.id)

            if task.subtasks:
                self._flatten_tasks(task.subtasks, task.id)

    def get_ready_tasks(self) -> List[Task]:
        """Returns a list of tasks that are READY to be executed."""
        ready_tasks = []
        
        # Check PENDING tasks to see if they can transition
        # We copy items to avoid issues if we modify states inside the loop (though we try not to modify iterables being looped)
        pending_ids = [tid for tid, state in self.task_states.items() if state == TaskStatus.PENDING]
        
        for task_id in pending_ids:
            if self._can_start(task_id):
                task = self.tasks[task_id]
                if task.subtasks:
                    # Parent tasks with subtasks are "containers". 
                    # If they are ready, we auto-start them to unlock their children.
                    logger.info(f"Auto-expanding parent task {task_id} to RUNNING.")
                    self.mark_running(task_id)
                    # We do NOT return parent tasks for execution by agents.
                else:
                    self.transition_state(task_id, TaskStatus.READY)
                    ready_tasks.append(task)
        
        # Also gather tasks that are already in READY state (from previous ticks)
        for task_id, state in self.task_states.items():
            if state == TaskStatus.READY:
                task = self.tasks[task_id]
                # Avoid duplicates if it was just added effectively
                if task not in ready_tasks:
                    ready_tasks.append(task)
                    
        return ready_tasks

    def _can_start(self, task_id: str) -> bool:
        """
        Determines if a task is eligible to start.
        Conditions:
        1. All explicit dependencies are COMPLETED.
        2. Its parent (if any) is RUNNING (i.e., the container is active).
        """
        # 1. Check dependencies
        if not self._are_dependencies_met(task_id):
            return False
            
        # 2. Check parent state
        parent_id = self.parent_map.get(task_id)
        if parent_id:
            if self.task_states[parent_id] != TaskStatus.RUNNING:
                return False
                
        return True

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
        
        # Check if this completion finishes a parent task
        parent_id = self.parent_map.get(task_id)
        if parent_id:
            siblings = self.children_map.get(parent_id, [])
            if all(self.task_states.get(sib) == TaskStatus.COMPLETED for sib in siblings):
                logger.info(f"All subtasks of {parent_id} completed. Completing parent.")
                self.mark_completed(parent_id, "All subtasks completed.")

    def mark_failed(self, task_id: str, error: str):
        self.results[task_id] = error
        self.transition_state(task_id, TaskStatus.FAILED)
        # Failure propagation could be complex (fail parent?), but for now we leave it local.

    def is_all_completed(self) -> bool:
        return all(state == TaskStatus.COMPLETED for state in self.task_states.values())
