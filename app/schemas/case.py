from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class CaseStatus(str, Enum):
    """Allowed status values for a case."""
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class CaseBase(BaseModel):
    """Base Pydantic schema for case fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Brief title of the case")
    description: str = Field(..., min_length=1, description="Detailed description of the case")
    status: CaseStatus = Field(..., description="Current status of the case (OPEN, IN_PROGRESS, RESOLVED, CLOSED)")


class CaseCreate(CaseBase):
    """Schema for creating a new case."""
    pass


class CaseUpdate(CaseBase):
    """Schema for full update/replacement of an existing case (PUT)."""
    pass


class CaseResponse(CaseBase):
    """Schema for returning case details in API responses."""
    id: int = Field(..., description="Unique case identifier")
    created_at: datetime = Field(..., description="Timestamp when case was created")
    updated_at: datetime = Field(..., description="Timestamp when case was last updated")

    model_config = ConfigDict(from_attributes=True)
