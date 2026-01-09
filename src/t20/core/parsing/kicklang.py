import re
from typing import List, Optional, Dict, Any
from t20.core.common.types import Plan, Task, Role

class KickLangParser:
    """Parses KickLang PLAN blocks into runtime Plan objects."""

    @staticmethod
    def parse(text: str) -> Plan:
        """
        Parses a KickLang PLAN block string into a Plan object.
        
        Expected format:
        rolePlanner PLAN PipelineName [Granularity...]
        Stage1 action params...
        Stage2 roleSub PLAN SubPipeline...
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            return Plan(high_level_goal="", reasoning="", roles=[], tasks=[])

        metadata: Dict[str, Any] = {}

        # 1. Parse Header
        header_pattern = r"^(\w+)\s+PLAN\s+(\w+)(?:\s+(.*))?$"
        header_match = re.match(header_pattern, lines[0])
        
        if not header_match:
             # Fallback or error? For now, simplistic parsing
            high_level_goal = lines[0]
            plan_name = "UnnamedPlan"
            planner_role = "unknown"
        else:
            planner_role, plan_name, params = header_match.groups()
            high_level_goal = f"Execute plan {plan_name}"
            # Extract params into metadata
            # e.g. "GranularityFine HorizonShort" -> {"Granularity": "Fine", "Horizon": "Short"}
            # Simple heuristic: Split by Space, try to split CamelCase if possible or just store as list of tags
            if params:
                high_level_goal += f" with params: {params}"
                # For now, store raw params string in metadata, and maybe simple tags
                metadata["raw_params"] = params
                metadata["tags"] = params.split()

        tasks: List[Task] = []
        roles_set = {planner_role} if header_match else set()
        
        # Context for conditionals
        # We maintain a stack of conditions if we want nested IFs, but let's start with single level or flat state
        # "current_condition" applies to all tasks parsed until it changes
        current_condition: Optional[str] = None
        
        # 2. Parse Stages
        for i, line in enumerate(lines[1:]):
            parts = line.split()
            if not parts:
                continue

            # Handle IF/ELSE/END
            # Case 1: IF condition
            if parts[0] == "IF":
                # Condition is the rest of the line
                condition_expr = " ".join(parts[1:])
                current_condition = condition_expr
                continue
            
            # Case 2: ELSE
            if parts[0] == "ELSE":
                # Negate current condition. Valid only if we are in an IF block.
                # Simplistic negation: "NOT (condition)"
                if current_condition and not current_condition.startswith("NOT "):
                    current_condition = f"NOT ({current_condition})"
                elif current_condition and current_condition.startswith("NOT "):
                     # If we were already in ELSE (not typical for simple ELSE), logic might be complex.
                     # But standard ELSE just flips.
                     # Let's assume we flip back to original? No, ELSE follows IF.
                     # IF A -> cond=A
                     # ELSE -> cond=NOT A
                     pass
                else:
                    # Fallback for unexpected ELSE
                    current_condition = "ELSE"
                continue

            # Case 3: END (Optional explicit end of block, though indentation is pythonic, KickLang often uses implicit scope or END)
            if parts[0] == "END":
                current_condition = None
                continue
            
            # Case 4: Normal Stage
            stage_id = parts[0]
            
            # Heuristic for role: check if second word starts with 'role'
            current_role = planner_role # default to planner if not specified
            action_start_idx = 1
            
            if len(parts) > 1 and parts[1].startswith("role"):
                current_role = parts[1]
                action_start_idx = 2
                roles_set.add(current_role)
            
            description = " ".join(parts[action_start_idx:])
            
            # Extract structured Action Verb and Params
            # Heuristic: The first word of description is the Verb if it is UPPERCASE
            action_parts = description.split()
            action_verb = None
            action_params = []
            
            if action_parts and action_parts[0].isupper():
                action_verb = action_parts[0]
                action_params = action_parts[1:]
            
            # Dependencies: Linear dependency for now
            deps = [tasks[-1].id] if tasks else []
            
            # Construct Task
            task = Task(
                id=stage_id,
                description=description,
                role=current_role,
                agent="TBD", # Agent assignment happens at runtime or we can default
                deps=deps,
                condition=current_condition,
                action_verb=action_verb,
                action_params=action_params
            )
            tasks.append(task)

        # Create Roles list
        roles = [Role(title=r, purpose="Executes tasks in the plan") for r in roles_set]

        return Plan(
            high_level_goal=high_level_goal,
            reasoning=f"Parsed from KickLang PLAN: {plan_name}",
            roles=roles,
            tasks=tasks,
            metadata=metadata
        )
