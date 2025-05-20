from typing import Optional

from pydantic import BaseModel, Field


class ServiceNowIncident(BaseModel):
    sys_id: str = Field(..., description="Unique incident identifier")
    number: str = Field(..., description="Incident number")
    short_description: str
    description: str
    configuration_item: Optional[str]
    related_ci: list[str] = []
    application: Optional[str]
    priority: int
    state: int


class AnalysisResult(BaseModel):
    incident_id: str
    agent_name: str
    findings: list[str]
    recommendations: list[str]
    confidence: float
