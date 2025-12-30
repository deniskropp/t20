import logging
import re
from typing import Optional, Any, Dict
from t20sdk.lang.spec import Action, ActionType, Role, RoleType

logger = logging.getLogger(__name__)

class SystemInterfaceLayer:
    """
    The System Interface Layer maps `e()` invocations to formal operations 
    within the multi-agent system.
    """

    def __init__(self):
        pass

    def e(self, taskType: str, instruction: str, context: Optional[str] = None) -> Action:
        """
        Translates high-level user intent into actionable commands.

        Args:
            taskType (str): Specifies the specialization of the agent (e.g., 'REASONING', 'KNOWLEDGE').
            instruction (str): A formalized query in KickLang syntax (e.g., 'GENERATE INSIGHTS FROM').
            context (Optional[str]): Index-based references to prior results.

        Returns:
            Action: A formal operation (CREATE, QUERY, ANALYZE) ready for execution.
        """
        logger.info(f"e() invoked with: taskType={taskType}, instruction='{instruction}', context={context}")

        # 1. Analyze parameters to determine the formal operation
        operation = self._map_to_operation(taskType, instruction)
        
        # 2. Extract target and parameters
        target = self._extract_target(instruction)
        parameters = self._build_parameters(taskType, instruction, context)

        # 3. Construct the Action
        action = Action(
            verb=operation,
            target=target,
            parameters=parameters
        )
        
        logger.info(f"Mapped to Action: {action}")
        return action

    def _map_to_operation(self, taskType: str, instruction: str) -> ActionType:
        """
        Interprets params to determine the appropriate formal operation.
        """
        instruction_upper = instruction.upper()
        
        # Heuristic mapping based on keywords
        if "GENERATE" in instruction_upper or "CREATE" in instruction_upper or "NEW" in instruction_upper:
            if "INSIGHTS" in instruction_upper: # Special case mentioned in prompt, mapped to ANALYZE?
                # User Prompt: "GENERATE INSIGHTS FROM" ... parsed to identify ... ANALYZE or QUERY
                return ActionType.ANALYZE
            return ActionType.CREATE
        
        if "QUERY" in instruction_upper or "FIND" in instruction_upper or "SEARCH" in instruction_upper:
            return ActionType.QUERY
            
        if "ANALYZE" in instruction_upper or "PROCESS" in instruction_upper:
            return ActionType.ANALYZE
            
        # Default fallback
        return ActionType.QUERY

    def _extract_target(self, instruction: str) -> str:
        """
        Naively extracts the object of the instruction.
        For 'GENERATE INSIGHTS FROM data', target might be 'data'.
        """
        # Simple regex to capture text after common verbs/prepositions
        # This is a placeholder for a real KickLang parser
        match = re.search(r"(?:FROM|ON|ABOUT|FOR)\s+(.*)", instruction, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Fallback: use the whole instruction as target if no preposition found
        # or perhaps a specific keyword if structured
        return instruction

    def _build_parameters(self, taskType: str, instruction: str, context: Optional[str]) -> Dict[str, Any]:
        """
        Constructs the parameter dictionary for the Action.
        """
        params = {
            "original_task_type": taskType,
            "raw_instruction": instruction
        }
        
        if context:
            # parsing index-based references e.g. <1>, <2>
            # For now, just store it
            params["context_refs"] = context
            
        return params
