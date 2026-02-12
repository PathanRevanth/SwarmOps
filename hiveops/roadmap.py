from __future__ import annotations

from .models import PhaseItem, PlatformRoadmapResponse


def build_platform_roadmap() -> PlatformRoadmapResponse:
    return PlatformRoadmapResponse(
        product="HiveOps",
        phases=[
            PhaseItem(
                phase="Phase 1 - Autonomous SRE Foundation",
                status="implemented",
                capabilities=[
                    "Parallel swarm incident triage",
                    "Evidence-backed confidence scoring",
                    "Dashboard + health endpoints",
                ],
            ),
            PhaseItem(
                phase="Phase 2 - POETIQ Meta-Audit",
                status="implemented",
                capabilities=[
                    "Recursive audit recommendations",
                    "Confidence threshold-based quality gates",
                ],
            ),
            PhaseItem(
                phase="Phase 3 - MACOG IaC Generation",
                status="implemented",
                capabilities=[
                    "Intent-to-Terraform generation",
                    "Policy check bundle",
                    "Cost estimation",
                ],
            ),
            PhaseItem(
                phase="Phase 4 - Evolutionary Pipeline Optimizer",
                status="implemented",
                capabilities=[
                    "Generation-based fitness scoring",
                    "Deterministic speed/reliability/cost/security trade-off model",
                ],
            ),
            PhaseItem(
                phase="Phase 5 - Multi-Cluster Live Integrations",
                status="planned",
                capabilities=[
                    "Real connector runtime for cloud + observability",
                    "Human-in-the-loop remediation execution",
                    "Persistent state and compliance workflows",
                ],
            ),
        ],
    )
