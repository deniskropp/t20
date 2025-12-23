"""
Knowledge Graph Interface
-------------------------
This file defines the interface for the Knowledge Graph.
It serves as the API for interacting with system components and their definitions.
"""

from typing import Dict, Optional, List
from data_models.kicklang_schemas import Component
from data_models.artifact_schemas import Artifact
from config.system_governance import SystemGovernance

class KnowledgeGraphInterface:
    """
    Interface for interacting with the Knowledge Graph (simulated for now).
    """
    
    def __init__(self):
        # In-memory store for simulation
        self._components: Dict[str, Component] = {}
        self._artifacts: List[Artifact] = []

    def add_artifact(self, artifact: Artifact) -> bool:
        """
        Adds a new artifact to the graph.
        """
        self._artifacts.append(artifact)
        return True

    def get_artifacts(self) -> List[Artifact]:
        """
        Returns all artifacts.
        """
        return self._artifacts

    def add_component(self, component: Component) -> bool:
        """
        Adds a new component to the graph.
        Returns True if successful, False if component with same name exists.
        """
        if component.name in self._components:
            return False
        
        self._components[component.name] = component
        return True

    def get_component(self, name: str) -> Optional[Component]:
        """
        Retrieves a component by name.
        """
        return self._components.get(name)

    def update_component_status(self, name: str, new_status: str) -> bool:
        """
        Updates a component's status, enforcing governance rules.
        Returns True if successful, False if invalid transition or component not found.
        """
        component = self.get_component(name)
        if not component:
            return False
            
        if not SystemGovernance.is_transition_valid(component.status, new_status):
            print(f"Invalid transition from {component.status} to {new_status}")
            return False
            
        component.status = new_status
        return True

    def list_components(self) -> List[Component]:
        """
        Returns a list of all components.
        """
        return list(self._components.values())
