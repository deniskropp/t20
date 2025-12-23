"""
KickLang Schemas
----------------
This file defines the data structures for KickLang using Pydantic.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime

class KickLangDefinition(BaseModel):
    """
    Represents the KickLang-structured metadata or definition for a component.
    """
    syntax_version: str = Field(..., description="Version of the KickLang syntax used")
    commands: List[str] = Field(default_factory=list, description="List of supported commands")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Configuration parameters")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class Component(BaseModel):
    """
    Represents a system component under development.
    Maps to the 'Components' table in strict_schema.sql.
    """
    component_id: Optional[int] = Field(None, description="Unique identifier for the component")
    name: str = Field(..., description="Unique name of the component")
    description: Optional[str] = Field(None, description="Description of the component")
    status: str = Field(default="Defined", description="Current status of the component")
    kicklang_definition: Optional[KickLangDefinition] = Field(None, description="KickLang definition")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, description="Last update timestamp")
