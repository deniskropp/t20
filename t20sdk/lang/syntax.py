from typing import List, Optional, Union, Any, Dict
from pydantic import BaseModel, Field
from .spec import Role, Action, Placebo, ActionType

class Step(BaseModel):
    """
    A single step in a pipeline.
    """
    name: str
    role: Optional[Role] = None
    action: Union[Action, Placebo]
    
    # Input/Output binding
    input_var: Optional[str] = None
    output_var: Optional[str] = None

class Plan(BaseModel):
    """
    A sequence of steps (reasoning episodes).
    """
    name: str
    steps: List[Step] = Field(default_factory=list)
    parent_plan: Optional['Plan'] = None
    
    def add_step(self, step: Step):
        self.steps.append(step)

    def describe(self) -> str:
        lines = [f"PLAN: {self.name}"]
        for step in self.steps:
            role_str = f"{step.role.name} " if step.role else ""
            if isinstance(step.action, Placebo):
                lines.append(f"  [{step.name}] {role_str}(PLACEBO: {step.action.marker})")
            else:
                lines.append(f"  [{step.name}] {role_str}{step.action.verb.value} -> {step.output_var or 'void'}")
        return "\n".join(lines)

class Pipeline(BaseModel):
    """
    Top-level container for a KickLang workflow.
    """
    name: str
    root_plan: Plan
