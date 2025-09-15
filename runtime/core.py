"""This module provides the core data structures for the multi-agent runtime.

It defines the ExecutionContext for managing workflow state and the Session
for handling artifacts and session-specific data.
"""

from dataclasses import dataclass, field
from typing import Any, Dict
import uuid
import os
import logging
import json

logger = logging.getLogger(__name__)

@dataclass
class ExecutionContext:
    """Holds the state and context for a multi-agent workflow."""
    session: 'Session'
    high_level_goal: str
    plan: Dict[str, Any]
    step_index: int = 0
    round_num: int = 0
    artifacts: Dict[str, Any] = field(default_factory=dict)

    def current_step(self) -> Dict[str, Any]:
        """Returns the current step in the plan."""
        return self.plan.get("tasks", [])[self.step_index]

    def _remember_artifact(self, key: str, value: Any):
        """Remembers an artifact from a step's execution for future tasks."""
        self.artifacts[key] = {"content": value, "step": self.current_step()}

    def record_artifact(self, key: str, value: Any, mem: bool = False):
        """
        Records an artifact from a step's execution and optionally remembers it.

        Args:
            key (str): The key under which to store the artifact.
            value (Any): The content of the artifact.
            mem (bool): If True, the artifact is also stored in the execution context's memory.
        """
        artifact_key = f"{self.round_num}__step_{self.step_index}_{key}"
        self.session.add_artifact(artifact_key, value)
        if mem:
            self._remember_artifact(artifact_key, value)

    def record_initial(self, key: str, value: Any):
        """
        Records an artifact from a step's execution and optionally remembers it.

        Args:
            key (str): The key under which to store the artifact.
            value (Any): The content of the artifact.
        """
        artifact_key = f"{self.round_num}__step_{self.step_index}_{key}"
        self.session.add_artifact(artifact_key, value)
        self.artifacts[artifact_key] = {
            "content": value,
            "step": {"task_id": "none", "requires": []},
        }

@dataclass
class Session:
    """Manages the runtime context for a task, including session ID and artifact storage."""
    session_id: str = field(default_factory=lambda: f"session_{uuid.uuid4()}")
    agents: list = field(default_factory=list) # Type hint will be updated later to List[Agent]
    state: str = "initialized"
    session_dir: str = field(init=False)
    project_root: str = field(default_factory=str)

    def __post_init__(self):
        """Initializes the session directory."""
        if not self.project_root:
            self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.session_dir = os.path.join(self.project_root, 'sessions', self.session_id)
        os.makedirs(self.session_dir, exist_ok=True)
        logger.info(f"Session created: {self.session_id} (Directory: {self.session_dir})")

    def add_artifact(self, name: str, content: Any):
        """
        Saves an artifact in the session directory.

        Args:
            name (str): The name of the artifact file.
            content (Any): The content to write to the artifact file. Can be dict, list, or string.
        """
        artifact_path = os.path.join(self.session_dir, name)
        try:
            os.makedirs(os.path.dirname(artifact_path), exist_ok=True)
            with open(artifact_path, 'w', encoding='utf-8') as f:
                if isinstance(content, (dict, list)):
                    json.dump(content, f, indent=4)
                else:
                    f.write(str(content))
            logger.info(f"Artifact '{name}' saved in session {self.session_id}.")
        except (TypeError, IOError) as e:
            logger.error(f"Error saving artifact '{name}': {e}")

    def get_artifact(self, name: str) -> Any:
        """
        Loads an artifact from the session directory.

        Args:
            name (str): The name of the artifact file to load.

        Returns:
            Any: The content of the artifact, or None if an error occurs.
        """
        artifact_path = os.path.join(self.session_dir, name)
        try:
            with open(artifact_path, 'r', encoding='utf-8') as f:
                if name.endswith('.json'):
                    return json.load(f)
                return f.read()
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            logger.error(f"Error retrieving artifact '{name}': {e}")
            return None
