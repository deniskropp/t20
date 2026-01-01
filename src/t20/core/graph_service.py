"""
GraphService module for KickLang SDK.
Provides knowledge graph capabilities by delegating to a GraphBackend.
"""
from typing import List, Dict, Any, Union, Optional
from t20.core.graph_backend import GraphBackend, PythonGraphBackend

class GraphService:
    """
    Service for managing the Knowledge Graph.
    Delegates storage and query execution to a swappable backend.
    """
    
    def __init__(self, backend: Optional[GraphBackend] = None):
        """
        Initialize the GraphService.
        Args:
            backend: Optional backend instance. Defaults to PythonGraphBackend.
        """
        self.backend = backend or PythonGraphBackend()

    def add_concept(self, concept: Dict[str, Any]) -> bool:
        """Adds a concept to the graph."""
        return self.backend.add_concept(concept)

    def add_relationship(self, relationship: Dict[str, Any]) -> bool:
        """Adds a relationship to the graph."""
        return self.backend.add_relationship(relationship)

    def query(self, query_string: str) -> Union[List[Any], int, Exception]:
        """Executes a query against the graph."""
        return self.backend.query(query_string)
