from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class StakeholderInfo(BaseModel):
    name: str
    role: str


class ProcessMetadataCreate(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=200)
    purpose: str = Field(..., min_length=10, description="Why does this project exist")
    business_summary: str = Field(
        ...,
        min_length=20,
        description="High level summary of what the business process does",
    )
    stakeholders: List[StakeholderInfo] = Field(
        ..., description="Who are the stakeholders"
    )
    # Power automate flow file is handled separately via file upload


class ProcessMetadataUpdate(BaseModel):
    project_name: Optional[str] = Field(None, max_length=200)
    purpose: Optional[str] = None
    business_summary: Optional[str] = None
    stakeholders: Optional[List[StakeholderInfo]] = None


class ProcessMetadataResponse(BaseModel):
    id: int
    project_name: str
    purpose: str
    business_summary: str
    stakeholders: List[StakeholderInfo]
    flow_filename: Optional[str]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime
    status: str
    ollama_analysis: Optional[str]

    class Config:
        from_attributes = True


class ProcessListResponse(BaseModel):
    id: int
    project_name: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
