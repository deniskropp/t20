"""
Artifact Schemas
----------------
This file defines the schemas for task artifacts using Pydantic.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class ArtifactFile(BaseModel):
    """
    Represents a file generated as part of an artifact.
    Maps to the 'Artifact_Files' table.
    """
    file_id: Optional[int] = Field(None, description="Unique identifier for the file")
    artifact_id: Optional[int] = Field(None, description="ID of the parent artifact")
    path: str = Field(..., description="File path or name")
    content: str = Field(..., description="Full content of the file")
    file_type: Optional[str] = Field(None, description="MIME type or file extension")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="Creation timestamp")

class Artifact(BaseModel):
    """
    Represents metadata about task-generated outputs.
    Maps to the 'Artifacts' table.
    """
    artifact_id: Optional[int] = Field(None, description="Unique identifier for the artifact")
    system_task_id: str = Field(..., description="System task identifier (e.g., 'T-02')")
    generated_by_agent_id: Optional[int] = Field(None, description="ID of the agent who generated this")
    generated_for_component_id: Optional[int] = Field(None, description="ID of the component this belongs to")
    output_summary: Optional[str] = Field(None, description="Summary of the output")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="Creation timestamp")
    files: List[ArtifactFile] = Field(default_factory=list, description="List of files associated with this artifact")
