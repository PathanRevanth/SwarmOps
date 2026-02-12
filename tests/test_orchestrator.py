import pytest

from hiveops.models import IncidentRequest
from hiveops.orchestrator import SwarmOrchestrator


@pytest.mark.asyncio
async def test_triage_returns_signals_confidence_and_audit_recommendations():
    orchestrator = SwarmOrchestrator()
    request = IncidentRequest(
        incident_id="INC-101",
        service="checkout-api",
        symptom="latency spike after deploy",
        severity="high",
        environment="prod",
    )

    result = await orchestrator.triage(request)

    assert result.incident_id == "INC-101"
    assert result.status in {"mitigated", "resolved", "needs_human"}
    assert len(result.signals) == 5
    assert 0.0 <= result.confidence <= 1.0
    assert result.estimated_minutes_to_mitigate in {8, 15, 30}
    assert len(result.audit_recommendations) >= 1


@pytest.mark.asyncio
async def test_security_pattern_requires_human_escalation_for_critical_incident():
    orchestrator = SwarmOrchestrator()
    request = IncidentRequest(
        incident_id="INC-999",
        service="api-gateway",
        symptom="possible exploit attack pattern from waf",
        severity="critical",
        environment="prod",
    )

    result = await orchestrator.triage(request)

    assert result.status == "needs_human"
    assert "incident commander" in result.suggested_action.lower() or "waf" in result.suggested_action.lower()
