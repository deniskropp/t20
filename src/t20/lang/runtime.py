import logging
from typing import Dict, Any, List
from .spec import ActionType, Role, Placebo
from .ast import Plan, Step, Pipeline

logger = logging.getLogger(__name__)

class ExecutionContext:
    def __init__(self):
        self.scope: Dict[str, Any] = {}
        self.artifacts: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self.scope[key] = value

    def get(self, key: str) -> Any:
        return self.scope.get(key)

class PlanExecutor:
    def __init__(self):
        self.context = ExecutionContext()

    def execute_pipeline(self, pipeline: Pipeline):
        logger.info(f"Starting Pipeline: {pipeline.name}")
        self.execute_plan(pipeline.root_plan)
        logger.info(f"Finished Pipeline: {pipeline.name}")

    def execute_plan(self, plan: Plan):
        logger.info(f"  Executing PLAN: {plan.name}")
        for step in plan.steps:
            self.execute_step(step)

    def execute_step(self, step: Step):
        role_info = f"[{step.role.name}]" if step.role else "[System]"
        
        if isinstance(step.action, Placebo):
            logger.info(f"    {role_info} Skipped (Placebo): {step.action.marker}")
            return

        action = step.action
        logger.info(f"    {role_info} Executing {action.verb} on '{action.target}'")

        # Mock Execution Logic based on Verb
        result = f"Result of {action.verb} on {action.target}"
        
        # Handle Nested PLANs (Meta Operations)
        if action.verb == ActionType.PLAN:
            # In a real implementation, 'target' might be a sub-pipeline or plan name
            # For now, we simulate a nested execution if parameters provide a sub-plan
            sub_plan = action.parameters.get("sub_plan")
            if sub_plan and isinstance(sub_plan, Plan):
                logger.info(f"    -> Entering Nested Plan: {sub_plan.name}")
                self.execute_plan(sub_plan)
                result = f"Output of Nested Plan {sub_plan.name}"

        # Bind Output
        if step.output_var:
            self.context.set(step.output_var, result)
            logger.info(f"      -> Bound result to '${step.output_var}'")
