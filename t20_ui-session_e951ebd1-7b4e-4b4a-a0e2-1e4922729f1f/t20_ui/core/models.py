# Data models for tasks, agents, sessions, etc.

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class AgentConfig:
    name: str
    role: str
    goal: str
    model: Optional[str] = None
    delegation: bool = False
    team: Optional[List[str]] = None

@dataclass
class TaskConfig:
    goal: str
    orchestrator: str
    model: str
    rounds: int
    files: List[str] = field(default_factory=list)

@dataclass
class AgentOutput:
    agent_name: str
    output: str
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None

@dataclass
class SessionInfo:
    session_id: str
    start_time: str
    end_time: Optional[str] = None
    task_goal: str
    final_output: Optional[str] = None
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "Running" # e.g., Running, Completed, Failed

