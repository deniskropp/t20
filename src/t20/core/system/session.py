"""This module provides the core data structures for the multi-agent runtime.

It defines the ExecutionContext for managing workflow state and the Session
for handling artifacts and session-specific data.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from threading import Lock
import uuid
import os
import logging
import json

from t20.core.common.types import Plan, Task

logger = logging.getLogger(__name__)


class ContextItem:
    def __init__(self, name: str, content: Any, step: Task):
        self.name = name
        self.content = content
        self.step = step


@dataclass
class ExecutionContext:
    """Holds the state and context for a multi-agent workflow."""
    session: 'Session'
    plan: Plan
    items: Dict[str, ContextItem] = field(default_factory=dict)
    lock: Lock = field(default_factory=Lock)

    def _remember_artifact(self, key: str, value: Any, step: Task) -> None:
        """Remembers an artifact from a step's execution for future tasks."""
        self.items[key] = ContextItem(name=key, content=value, step=step)

    def record_artifact(self, key: str, value: Any, step: Task, mem: bool = False) -> None:
        """
        Records an artifact from a step's execution and optionally remembers it.
        """
        with self.lock:
            artifact_key = f"__step_{step.id}_{key}"
            self.session.add_artifact(artifact_key, value)
            if mem:
                self._remember_artifact(artifact_key, value, step)

    def record_initial(self, key: str, value: Any) -> None:
        """
        Records an artifact from a step's execution and optionally remembers it.
        """
        with self.lock:
            self._remember_artifact(key, value, step=Task(
                id='initial',
                description='Initial files provided by the user',
                role='User',
                agent='User',
                deps=[]
            ))




@dataclass
class Session:
    """Manages the runtime context for a task, including session ID and artifact storage."""
    session_id: str = field(default_factory=lambda: f"session_{uuid.uuid4()}")
    agents: list = field(default_factory=list) # Type hint will be updated later to List[Agent]
    state: str = "initialized"
    # session_dir is kept for compatibility if needed, but primary storage is now DB
    session_dir: str = field(init=False)
    project_root: str = field(default_factory=str)
    _db: Any = field(init=False, repr=False, default=None)

    def __post_init__(self) -> None:
        """Initializes the session database connection."""
        from t20.core.data.db import SessionDB
        
        if not self.project_root:
            self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # We ensure the sessions directory exists to store the DB file
        sessions_root = os.path.join(self.project_root, 'sessions')
        os.makedirs(sessions_root, exist_ok=True)
        
        self.session_dir = os.path.join(sessions_root, self.session_id)
        # We might not need to create the specific session dir if everything is in DB, 
        # but let's keep it if we want to store other things or for backward compat.
        # For now, we won't strictly enforce its creation for artifacts.
        
        db_path = os.path.join(sessions_root, "sessions.db")
        self._db = SessionDB.get_instance(db_path)
        
        # Register session in DB
        self._db.create_session(self.session_id)
        
        logger.info(f"Project Root: '{self.project_root}'")
        logger.info(f"Session DB: '{db_path}'")
        logger.debug(f"Session initialized: {self.session_id}")

    def add_artifact(self, name: str, content: Any) -> None:
        """
        Saves an artifact in the session database.

        Args:
            name (str): The name of the artifact.
            content (Any): The content to write.
        """
        if self._db:
            self._db.save_artifact(self.session_id, name, content)
        else:
            logger.error("Session DB not initialized.")

    def get_artifact(self, name: str) -> Any:
        """
        Loads an artifact from the session database.

        Args:
            name (str): The name of the artifact to load.

        Returns:
            Any: The content of the artifact, or None if not found or error.
        """
        if self._db:
            return self._db.get_artifact(self.session_id, name)
        logger.error("Session DB not initialized.")
        return None
