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

class IfBlock(BaseModel):
    """
    Conditional execution block.
    Matches spec: IF condition: ... ELSE: ...
    """
    condition: str
    then_branch: List[Union['Step', 'IfBlock']] = Field(default_factory=list)
    else_branch: Optional[List[Union['Step', 'IfBlock']]] = None

class Plan(BaseModel):
    """
    A sequence of steps (reasoning episodes).
    """
    name: str
    steps: List[Union[Step, IfBlock]] = Field(default_factory=list)
    parent_plan: Optional['Plan'] = None
    
    def add_step(self, step: Union[Step, IfBlock]):
        self.steps.append(step)

    def describe(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}PLAN: {self.name}"]
        for step in self.steps:
            if isinstance(step, IfBlock):
                lines.append(f"{prefix}  IF {step.condition}:")
                for sub_step in step.then_branch:
                    lines.append(self._describe_item(sub_step, indent + 2))
                if step.else_branch:
                    lines.append(f"{prefix}  ELSE:")
                    for sub_step in step.else_branch:
                        lines.append(self._describe_item(sub_step, indent + 2))
            else:
                lines.append(self._describe_item(step, indent))
        return "\n".join(lines)

    def _describe_item(self, item: Union[Step, IfBlock], indent: int) -> str:
        prefix = "  " * indent
        if isinstance(item, IfBlock):
            # Recursively describe if-blocks if nested
            sub_lines = []
            sub_lines.append(f"{prefix}  IF {item.condition}:")
            for s in item.then_branch:
                 sub_lines.append(self._describe_item(s, indent + 2))
            if item.else_branch:
                sub_lines.append(f"{prefix}  ELSE:")
                for s in item.else_branch:
                    sub_lines.append(self._describe_item(s, indent + 2))
            return "\n".join(sub_lines)
        else:
            role_str = f"{item.role.name} " if item.role else ""
            if isinstance(item.action, Placebo):
                return f"{prefix}  [{item.name}] {role_str}(PLACEBO: {item.action.marker})"
            else:
                return f"{prefix}  [{item.name}] {role_str}{item.action.verb.value} -> {item.output_var or 'void'}"

class Pipeline(BaseModel):
    """
    Top-level container for a KickLang workflow.
    """
    name: str
    root_plan: Plan
