"""
System Governance
-----------------
This file defines the ethics and compliance rules for the system,
specifically enforcing the Purified Task-Agnostic Steps (TAS).
"""

from typing import List, Optional

class SystemGovernance:
    """
    Enforces system rules and workflows.
    """
    
    # Define valid component statuses in order
    COMPONENT_STATUS_FLOW = [
        "Defined",
        "Designed",
        "Implemented",
        "Verified",
        "Documented",
        "Refined"
    ]

    @staticmethod
    def get_next_allowed_status(current_status: str) -> Optional[str]:
        """
        Returns the next allowed status in the workflow.
        Returns None if the status is invalid or terminal.
        """
        if current_status not in SystemGovernance.COMPONENT_STATUS_FLOW:
            return None
        
        try:
            current_index = SystemGovernance.COMPONENT_STATUS_FLOW.index(current_status)
            if current_index + 1 < len(SystemGovernance.COMPONENT_STATUS_FLOW):
                return SystemGovernance.COMPONENT_STATUS_FLOW[current_index + 1]
        except ValueError:
            return None
            
        return None

    @staticmethod
    def is_transition_valid(current_status: str, new_status: str) -> bool:
        """
        Checks if a transition from current_status to new_status is valid.
        Currently enforces a strict linear progression.
        """
        # Allow staying in the same status (updates)
        if current_status == new_status:
            return True
            
        next_allowed = SystemGovernance.get_next_allowed_status(current_status)
        return new_status == next_allowed

    @staticmethod
    def validate_component_metadata(metadata: dict) -> List[str]:
        """
        Validates component metadata against governance rules.
        Returns a list of error messages, empty if valid.
        """
        errors = []
        # Example rule: must have an owner
        if "owner" not in metadata:
            errors.append("Metadata missing required field: 'owner'")
        return errors
