from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class AutomationTaskCreate(BaseModel):
    """
    Pydantic Schema to validate incoming JSON payloads
    for creating automated agent workflows.
    """
    title: str = Field(..., min_length=3, max_length=100, description="Name of the automation task")
    agent_type: str = Field(..., description="Target AI agent type (e.g., 'RAG_Search', 'Data_Extraction')")
    priority: int = Field(default=1, ge=1, le=5, description="Priority rating from 1 (Low) to 5 (Critical)")
    payload_data: Dict[str, Any] = Field(default={}, description="Arbitrary dynamic JSON payload for execution")

class AutomationTaskResponse(AutomationTaskCreate):
    """
    Pydantic Schema defining the exact structure returned to the client.
    Adds system-generated properties.
    """
    id: str = Field(..., description="Unique tracking UUID for the job")
    status: str = Field(default="queued", description="Execution state of the agent workflow")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        # Allows Pydantic to read standard database ORM objects cleanly downstream
        from_attributes = True

class AutomationTaskUpdate(BaseModel):
    """
    Pydantic Schema for updating task execution state.
    All fields are optional to allow partial PATCH updates.
    """
    status: Optional[str] = Field(default=None, description="Updated status (e.g., 'running', 'completed', 'failed')")
    priority: Optional[int] = Field(default=None, ge=1, le=5, description="Updated priority rating")
