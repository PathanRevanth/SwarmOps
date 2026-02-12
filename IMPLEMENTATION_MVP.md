# HiveOps Platform Build (Phase-by-Phase)

This repository now ships a **phase-based platform implementation** aligned to your architecture vision.

## Phase 1 — Autonomous SRE Foundation (Implemented)
- Parallel micro-agent swarm for incident triage
- Evidence-backed confidence scoring
- Deterministic status output: `resolved` / `mitigated` / `needs_human`

## Phase 2 — POETIQ Meta-Audit Layer (Implemented)
- Recursive-style self-audit recommendations
- Quality gates based on confidence and evidence density
- Audit output attached directly to triage response

## Phase 3 — MACOG IaC Generator (Implemented)
- Intent-to-IaC endpoint for AWS/GCP/Azure providers
- Terraform template generation
- Policy check bundle + monthly cost estimate

## Phase 4 — Evolutionary Optimizer (Implemented)
- Generation-based optimization endpoint
- Composite fitness from speed/reliability/cost/security
- Deterministic variant tracking for demos and tests

## Phase 5 — Live Integrations + Execution Fabric (Planned)
- Real cloud/observability connector adapters
- Human-in-the-loop gated production remediation
- Persistent state + compliance + multi-tenant controls

## Run platform locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn hiveops.api:app --reload
```

## Demo endpoints

- `GET /`
- `GET /health`
- `GET /platform/roadmap`
- `POST /incidents/triage`
- `POST /iac/generate`
- `POST /pipelines/evolve`
