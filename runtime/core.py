"""Core data structures and utilities for the runtime."""

from dataclasses import dataclass, field
from typing import Any, Dict
import uuid
import os
import json
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init()

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

    def remember_artifact(self, key: str, value: Any):
        """Remembers an artifact from a step's execution for future tasks."""
        self.artifacts[key] = {'v': value, 's': self.current_step()}

    def record_artifact(self, key: str, value: Any, mem: bool = False):
        """
        Records an artifact from a step's execution and optionally remembers it.

        Args:
            key (str): The key under which to store the artifact.
            value (Any): The content of the artifact.
            mem (bool): If True, the artifact is also stored in the execution context's memory.
        """
        k = f"{self.round_num}__step_{self.step_index}_{key}"
        self.session.add_artifact(k, value)
        if mem:
            self.remember_artifact(k, value)

@dataclass
class Session:
    """Manages the runtime context for a task, including session ID and artifact storage."""
    session_id: str = field(default_factory=lambda: f"session_{uuid.uuid4()}")
    agents: list = field(default_factory=list) # Type hint will be updated later to List[Agent]
    state: str = "initialized"
    session_dir: str = field(init=False)

    def __post_init__(self):
        """Initializes the session directory."""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.session_dir = os.path.join(project_root, 'sessions', self.session_id)
        os.makedirs(self.session_dir, exist_ok=True)
        print(f"{Fore.GREEN}Session created: {self.session_id} (Directory: {self.session_dir}){Style.RESET_ALL}")

    def add_artifact(self, name: str, content: Any):
        """
        Saves an artifact in the session directory.

        Args:
            name (str): The name of the artifact file.
            content (Any): The content to write to the artifact file. Can be dict, list, or string.
        """
        artifact_path = os.path.join(self.session_dir, name)
        try:
            with open(artifact_path, 'w', encoding='utf-8') as f:
                if isinstance(content, (dict, list)):
                    json.dump(content, f, indent=4)
                else:
                    f.write(str(content))
            print(f"{Fore.BLUE}Artifact{Style.RESET_ALL} '{Fore.LIGHTBLUE_EX}{name}{Fore.LIGHTGREEN_EX}' saved in session {self.session_id}.{Style.RESET_ALL}")
        except (TypeError, IOError) as e:
            print(f"{Fore.RED}Error saving artifact '{name}'{Style.RESET_ALL}: {e}")

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
            print(f"{Fore.RED}Error retrieving artifact '{name}'{Style.RESET_ALL}: {e}")
            return None
