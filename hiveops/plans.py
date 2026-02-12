from __future__ import annotations

from pydantic import BaseModel


class SourceCoverage(BaseModel):
    source_file: str
    confirmed_topics: list[str]


class PhaseExecutionItem(BaseModel):
    phase: str
    objective: str
    now_implemented: list[str]
    next_implementation: list[str]
    exit_criteria: list[str]


class StartupAlignmentPlan(BaseModel):
    startup: str
    source_coverage: list[SourceCoverage]
    execution_phases: list[PhaseExecutionItem]


def build_alignment_plan() -> StartupAlignmentPlan:
    return StartupAlignmentPlan(
        startup="HiveOps",
        source_coverage=[
            SourceCoverage(
                source_file="DevOps Agent Swarm & Meta Layer.pdf",
                confirmed_topics=[
                    "Kimi K2.5 MoE + swarm intelligence foundations",
                    "POETIQ recursive self-improvement loop",
                    "Parallel orchestration and autonomous DevOps positioning",
                ],
            ),
            SourceCoverage(
                source_file="HiveOps_Final_Documentation.md",
                confirmed_topics=[
                    "5-layer architecture + phased GTM/roadmap",
                    "PRD requirements: swarm, POETIQ, MACOG, SRE, evolution",
                    "Benchmarks and market positioning assumptions",
                ],
            ),
            SourceCoverage(
                source_file="HiveOps_Final_Research_Backed_Documentation.docx",
                confirmed_topics=[
                    "Research-backed synthesis narrative",
                    "Business + technical targets mirrored with markdown plan",
                    "Investor-style storyline and milestones",
                ],
            ),
        ],
        execution_phases=[
            PhaseExecutionItem(
                phase="Phase A — Product Surface & Demo Reliability",
                objective="Provide a reliable platform shell for demos and stakeholder validation.",
                now_implemented=[
                    "FastAPI platform shell with dashboard and core endpoints",
                    "Stable /platform/screenshot endpoint to avoid expiring artifact links",
                    "Demo runbook in docs/DEMO.md",
                ],
                next_implementation=[
                    "API auth scaffold (API key/JWT)",
                    "Tenant/workspace scoping for all endpoints",
                ],
                exit_criteria=[
                    "Authenticated API calls",
                    "Tenant-isolated responses",
                ],
            ),
            PhaseExecutionItem(
                phase="Phase B — Autonomous SRE Core",
                objective="Operationalize incident triage with reproducible evidence and escalation logic.",
                now_implemented=[
                    "Swarm-based triage orchestration with confidence scoring",
                    "Security-aware escalation and mitigation recommendations",
                    "Audit recommendations embedded in incident response",
                ],
                next_implementation=[
                    "Real Prometheus/Kubernetes/GitHub connectors",
                    "Incident persistence and timeline replay",
                ],
                exit_criteria=[
                    "Live connector-backed evidence",
                    "Stored incident history with query API",
                ],
            ),
            PhaseExecutionItem(
                phase="Phase C — MACOG IaC Generation",
                objective="Move from static template generation to constrained, validated IaC pipelines.",
                now_implemented=[
                    "Intent-to-Terraform endpoint with provider parameter",
                    "Policy check bundle and cost estimate in response",
                ],
                next_implementation=[
                    "Terraform plan validation execution",
                    "OPA/Sentinel policy enforcement before output approval",
                ],
                exit_criteria=[
                    "Valid terraform plan artifact returned",
                    "Policy pass/fail report attached",
                ],
            ),
            PhaseExecutionItem(
                phase="Phase D — Evolution Engine",
                objective="Progress from simulated scoring to measurable pipeline optimization loops.",
                now_implemented=[
                    "Generation-based optimizer simulation with composite fitness",
                ],
                next_implementation=[
                    "Shadow pipeline execution telemetry ingestion",
                    "Mutation/crossover tracking with lineage persistence",
                ],
                exit_criteria=[
                    "Measured fitness from real runs",
                    "Lineage graph for variant outcomes",
                ],
            ),
            PhaseExecutionItem(
                phase="Phase E — Platform Hardening for GTM",
                objective="Close the gap between research vision and production readiness.",
                now_implemented=[
                    "Phase roadmap endpoint and implementation docs",
                    "Automated tests for current API surface",
                ],
                next_implementation=[
                    "RBAC, audit logs, and change approval workflows",
                    "Postgres/Redis state backbone and observability dashboards",
                    "Deployment manifests and CI/CD release workflow",
                ],
                exit_criteria=[
                    "Production deployment guide",
                    "Security baseline checklist complete",
                    "Pilot-ready SLO dashboards",
                ],
            ),
        ],
    )
