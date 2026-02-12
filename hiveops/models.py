from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class AgentDomain(str, Enum):
    metrics = "metrics"
    deployments = "deployments"
    kubernetes = "kubernetes"
    cost = "cost"
    security = "security"


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Signal(BaseModel):
    domain: AgentDomain
    finding: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)


class IncidentRequest(BaseModel):
    incident_id: str = Field(min_length=3)
    service: str
    symptom: str
    severity: Severity = Severity.medium
    environment: Literal["dev", "staging", "prod"] = "prod"


class InvestigationResult(BaseModel):
    incident_id: str
    service: str
    environment: str
    status: Literal["resolved", "mitigated", "needs_human"]
    hypothesis: str
    suggested_action: str
    confidence: float = Field(ge=0.0, le=1.0)
    estimated_minutes_to_mitigate: int = Field(ge=1)
    audit_recommendations: list[str] = Field(default_factory=list)
    signals: list[Signal]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class IacRequest(BaseModel):
    intent: str = Field(min_length=10)
    provider: Literal["aws", "gcp", "azure"] = "aws"


class IacResponse(BaseModel):
    provider: str
    architecture: str
    terraform: str
    policy_checks: list[str]
    estimated_monthly_cost_usd: int


class EvolutionRequest(BaseModel):
    generation: int = Field(default=1, ge=1, le=1000)


class EvolutionResponse(BaseModel):
    generation: int
    best_variant: str
    speed_score: float
    reliability_score: float
    cost_score: float
    security_score: float
    composite_fitness: float


class PhaseItem(BaseModel):
    phase: str
    status: Literal["implemented", "in_progress", "planned"]
    capabilities: list[str]


class PlatformRoadmapResponse(BaseModel):
    product: str
    phases: list[PhaseItem]


class HealthResponse(BaseModel):
    status: str
    version: str
    agents: int
