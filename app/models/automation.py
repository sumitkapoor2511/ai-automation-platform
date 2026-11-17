from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class AutomationTask(SQLModel, table=True):
    __tablename__ = "automation_tasks"

    id: Optional[str] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    agent_type: str = Field(index=True)
    priority: int = Field(default=1)
    status: str = Field(default="queued")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    payload_raw: str = Field(default="{}")
