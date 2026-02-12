from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AuditDecision:
    sufficient: bool
    confidence: float
    recommendations: list[str]


class PoetiqMetaLayer:
    """Phase 2: recursive self-audit controller (deterministic MVP)."""

    def __init__(self, confidence_threshold: float = 0.82, max_iterations: int = 4):
        self.confidence_threshold = confidence_threshold
        self.max_iterations = max_iterations

    def audit(self, confidence: float, status: str, evidence_count: int) -> AuditDecision:
        recommendations: list[str] = []
        sufficient = confidence >= self.confidence_threshold and status != "needs_human"

        if confidence < self.confidence_threshold:
            recommendations.append("Collect more telemetry before autonomous execution")
        if evidence_count < 3:
            recommendations.append("Expand evidence bundle from additional data sources")
        if status == "needs_human":
            recommendations.append("Escalate to human incident commander with timeline summary")

        if not recommendations:
            recommendations.append("Quality gates passed for current iteration")

        return AuditDecision(
            sufficient=sufficient,
            confidence=round(confidence, 2),
            recommendations=recommendations,
        )
