from __future__ import annotations

import asyncio

from .agents import DEFAULT_SWARM, MicroAgent
from .meta import PoetiqMetaLayer
from .models import AgentDomain, IncidentRequest, InvestigationResult, Severity, Signal


class SwarmOrchestrator:
    def __init__(
        self,
        agents: tuple[MicroAgent, ...] = DEFAULT_SWARM,
        meta_layer: PoetiqMetaLayer | None = None,
    ):
        self.agents = agents
        self.meta_layer = meta_layer or PoetiqMetaLayer()

    async def triage(self, incident: IncidentRequest) -> InvestigationResult:
        signals = await asyncio.gather(*(agent.investigate(incident) for agent in self.agents))
        return self._synthesize(incident, list(signals))

    def _synthesize(self, incident: IncidentRequest, signals: list[Signal]) -> InvestigationResult:
        if not signals:
            return InvestigationResult(
                incident_id=incident.incident_id,
                service=incident.service,
                environment=incident.environment,
                status="needs_human",
                hypothesis="No evidence available",
                suggested_action="Escalate to on-call engineer and gather telemetry",
                confidence=0.0,
                estimated_minutes_to_mitigate=45,
                audit_recommendations=["Increase connector coverage before autonomous triage"],
                signals=[],
            )

        weighted = sorted(signals, key=lambda s: s.confidence, reverse=True)
        top = weighted[0]
        avg_confidence = round(sum(signal.confidence for signal in signals) / len(signals), 2)

        status = "mitigated"
        hypothesis = "Resource pressure likely triggered by traffic spike and recent changes"
        action = (
            "Rollback latest deployment, increase replicas by 30%, and enable temporary "
            "rate limiting while monitoring error budget burn"
        )

        if top.domain == AgentDomain.security and top.confidence >= 0.85:
            hypothesis = "Potential security-driven incident impacting application stability"
            action = "Enable WAF strict mode, block suspicious IP ranges, rotate high-risk credentials"
            status = "needs_human" if incident.severity in {Severity.high, Severity.critical} else "mitigated"

        if incident.severity in {Severity.low, Severity.medium} and avg_confidence >= 0.8:
            status = "resolved"
            action = "Applied verified remediation via canary and promoted change to production"

        if incident.severity == Severity.critical and avg_confidence < 0.75:
            status = "needs_human"
            action = "Escalate to incident commander with full evidence bundle and rollback recommendation"

        eta_map = {
            "resolved": 8,
            "mitigated": 15,
            "needs_human": 30,
        }

        audit = self.meta_layer.audit(
            confidence=avg_confidence,
            status=status,
            evidence_count=sum(len(signal.evidence) for signal in weighted),
        )

        return InvestigationResult(
            incident_id=incident.incident_id,
            service=incident.service,
            environment=incident.environment,
            status=status,
            hypothesis=hypothesis,
            suggested_action=action,
            confidence=avg_confidence,
            estimated_minutes_to_mitigate=eta_map[status],
            audit_recommendations=audit.recommendations,
            signals=weighted,
        )
