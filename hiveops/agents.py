from __future__ import annotations

from dataclasses import dataclass

from .models import AgentDomain, IncidentRequest, Signal


@dataclass(slots=True)
class MicroAgent:
    """Small single-purpose agent that emits one signal based on incident context."""

    domain: AgentDomain

    async def investigate(self, incident: IncidentRequest) -> Signal:
        symptom = incident.symptom.lower()

        if self.domain == AgentDomain.metrics:
            latency_related = any(token in symptom for token in ("latency", "timeout", "slow"))
            confidence = 0.9 if latency_related else 0.62
            return Signal(
                domain=self.domain,
                finding=(
                    f"P95 latency regression detected for {incident.service}" if latency_related
                    else f"Error/traffic anomalies detected for {incident.service}"
                ),
                confidence=confidence,
                evidence=[
                    "prometheus:histogram_quantile(0.95, request_duration_seconds)",
                    "alertmanager:firing=SLOLatencyBurnRate",
                ],
            )

        if self.domain == AgentDomain.deployments:
            rollout_related = any(token in symptom for token in ("deploy", "release", "rollback"))
            confidence = 0.86 if rollout_related else 0.68
            return Signal(
                domain=self.domain,
                finding="Recent rollout/change-window overlap with incident start",
                confidence=confidence,
                evidence=[
                    "github:main@last_commit_within_20m",
                    "argo-rollouts:replicaset_transition",
                ],
            )

        if self.domain == AgentDomain.kubernetes:
            confidence = 0.88 if incident.environment == "prod" else 0.63
            return Signal(
                domain=self.domain,
                finding="Pod restart spikes and CPU throttling on serving tier",
                confidence=confidence,
                evidence=[
                    "kubectl:get pods --field-selector=status.phase!=Running",
                    "kube-state-metrics:container_cpu_cfs_throttled_seconds_total",
                ],
            )

        if self.domain == AgentDomain.cost:
            return Signal(
                domain=self.domain,
                finding="No immediate FinOps anomaly linked to incident blast radius",
                confidence=0.44,
                evidence=["billing:hourly_spend_within_expected_band"],
            )

        exploit_related = any(token in symptom for token in ("attack", "breach", "exploit", "waf"))
        confidence = 0.91 if exploit_related else 0.58
        return Signal(
            domain=self.domain,
            finding=(
                "Suspicious request signatures aligned with OWASP patterns"
                if exploit_related
                else "No active exploit signature in runtime telemetry"
            ),
            confidence=confidence,
            evidence=[
                "waf:anomaly_score",
                "falco:runtime_ruleset",
            ],
        )


DEFAULT_SWARM: tuple[MicroAgent, ...] = (
    MicroAgent(AgentDomain.metrics),
    MicroAgent(AgentDomain.deployments),
    MicroAgent(AgentDomain.kubernetes),
    MicroAgent(AgentDomain.cost),
    MicroAgent(AgentDomain.security),
)
