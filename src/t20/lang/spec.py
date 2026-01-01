from enum import Enum, auto
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field

# --- Roles ---

class RoleType(str, Enum):
    RESEARCHER = "Researcher"
    ANALYST = "Analyst"
    STORYTELLER = "Storyteller"
    PLANNER = "Planner"
    CODER = "Coder"
    SUMMARIZER = "Summarizer"

class Role(BaseModel):
    """
    Cognitive stance with parameterization.
    """
    name: str
    role_type: RoleType
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
    def __repr__(self) -> str:
        return f"Role({self.name}, {self.role_type}, params={self.parameters})"

# Configurable sub-types can be factory functions or subclasses
def Researcher(name: str = "Researcher", depth: str = "high") -> Role:
    return Role(name=name, role_type=RoleType.RESEARCHER, parameters={"depth": depth})

def Analyst(name: str = "Analyst", approach: str = "causal") -> Role:
    return Role(name=name, role_type=RoleType.ANALYST, parameters={"approach": approach})

def Storyteller(name: str = "Storyteller", tone: str = "epic") -> Role:
    return Role(name=name, role_type=RoleType.STORYTELLER, parameters={"tone": tone})

def Summarizer(name: str = "Summarizer", brevity: str = "concise") -> Role:
    return Role(name=name, role_type=RoleType.SUMMARIZER, parameters={"brevity": brevity})

def Planner(name: str = "Planner", granularity: str = "fine") -> Role:
    return Role(name=name, role_type=RoleType.PLANNER, parameters={"granularity": granularity})

# --- Actions ---

class ActionType(str, Enum):
    # Knowledge Access
    FIND = "FIND"
    LIST = "LIST"
    DETAIL = "DETAIL"
    
    # Knowledge Structuring
    LINK = "LINK"
    MAP = "MAP"
    CLUSTER = "CLUSTER"
    CREATE = "CREATE"
    
    # Knowledge Transformation
    SUMMARIZE = "SUMMARIZE"
    COMPARE = "COMPARE"
    EXPLAIN = "EXPLAIN"
    ANALYZE = "ANALYZE"
    QUERY = "QUERY"
    
    # Meta Operations
    COMMENT = "COMMENT"
    PLAN = "PLAN"
    TRANSFORM = "TRANSFORM"

class Action(BaseModel):
    """
    An atomic unit of work in a KickLang pipeline.
    """
    verb: ActionType
    target: str
    # Parameters can store bindings, like 'context', 'output', etc.
    parameters: Dict[str, Any] = Field(default_factory=dict) 

# --- Placebo ---

class Placebo(BaseModel):
    """
    Meta-markers for deferred or flagged logic.
    """
    marker: str
    condition: Optional[str] = None
    
    def __repr__(self):
        return f"Placebo(marker={self.marker}, cond={self.condition})"
