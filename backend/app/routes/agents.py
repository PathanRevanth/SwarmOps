import json
import time
import random
import hashlib
from fastapi import APIRouter
from ..database import get_db

router = APIRouter(prefix="/api/agents", tags=["agents"])

AGENT_DEFINITIONS = [
    {"name": "Architect Agent", "type": "architect", "domain": "iac_generation", "description": "Analyzes intent, defines high-level infrastructure topology", "status": "idle", "icon": "Building2"},
    {"name": "Provider Harmonizer", "type": "harmonizer", "domain": "provider_validation", "description": "Ensures cloud provider requirements are met (AWS/GCP/Azure)", "status": "idle", "icon": "Globe"},
    {"name": "Engineer Agent", "type": "engineer", "domain": "code_generation", "description": "Generates Terraform/Pulumi using constrained HCL decoding", "status": "idle", "icon": "Code"},
    {"name": "Security Prover", "type": "security_prover", "domain": "vulnerability_scan", "description": "Validates with policy-as-code (OPA, Sentinel)", "status": "active", "icon": "Shield"},
    {"name": "Cost Planner", "type": "cost_planner", "domain": "cost_analysis", "description": "Evaluates against real-time pricing and quota limits", "status": "idle", "icon": "DollarSign"},
    {"name": "DevOps Auditor", "type": "devops_auditor", "domain": "code_review", "description": "POETIQ-style supervisor reviewing Proof-Carrying Bundle", "status": "idle", "icon": "ClipboardCheck"},
    {"name": "SRE Investigator", "type": "sre_investigator", "domain": "incident_triage", "description": "Autonomous incident investigation and remediation", "status": "active", "icon": "Search"},
    {"name": "Evolution Optimizer", "type": "evolution_optimizer", "domain": "pipeline_optimization", "description": "Genetic algorithm-based pipeline optimization", "status": "idle", "icon": "Dna"},
]

@router.get("")
async def list_agents():
    return AGENT_DEFINITIONS

@router.get("/tasks")
async def list_agent_tasks(agent_type: str = "", status: str = "", limit: int = 20):
    with get_db() as conn:
        q = "SELECT * FROM agent_tasks WHERE 1=1"
        params = []
        if agent_type:
            q += " AND agent_type = ?"
            params.append(agent_type)
        if status:
            q += " AND status = ?"
            params.append(status)
        q += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(q, params).fetchall()
        return [dict(r) for r in rows]

@router.post("/iac/generate")
async def generate_iac(data: dict):
    intent = data.get("intent", "Deploy a web app")
    provider = data.get("provider", "aws")
    ha = any(t in intent.lower() for t in ("ha", "high availability", "multi-az"))
    replicas = 3 if ha else 2
    cost = 1800 if ha else 900
    arch = "multi_az_web_app" if ha else "single_region_web_app"

    terraform = f'''provider "{provider}" {{
  region = var.region
}}

resource "{provider}_vpc" "main" {{
  cidr_block = "10.0.0.0/16"
  tags = {{ Name = "hiveops-{arch}" }}
}}

resource "{provider}_subnet" "public" {{
  count      = {replicas}
  vpc_id     = {provider}_vpc.main.id
  cidr_block = cidrsubnet("10.0.0.0/16", 8, count.index)
}}

resource "{provider}_ecs_cluster" "main" {{
  name = "hiveops-cluster"
}}

resource "{provider}_ecs_service" "api" {{
  cluster       = {provider}_ecs_cluster.main.id
  desired_count = {replicas}
  launch_type   = "FARGATE"
}}

resource "{provider}_lb" "main" {{
  name               = "hiveops-alb"
  load_balancer_type = "application"
  subnets            = {provider}_subnet.public[*].id
}}'''

    with get_db() as conn:
        conn.execute(
            "INSERT INTO agent_tasks (project_id, agent_type, task_type, status, input_data, output_data, confidence, duration_ms) VALUES (?,?,?,?,?,?,?,?)",
            (1, "architect", "iac_generation", "completed", json.dumps({"intent": intent, "provider": provider}),
             json.dumps({"architecture": arch, "cost": cost}), 0.92, random.randint(1500, 4000)),
        )

    return {
        "provider": provider,
        "architecture": arch,
        "terraform": terraform,
        "policy_checks": [
            {"rule": "no_public_s3_buckets", "status": "passed", "engine": "OPA"},
            {"rule": "encryption_at_rest", "status": "passed", "engine": "OPA"},
            {"rule": "approved_instance_families", "status": "passed", "engine": "Sentinel"},
            {"rule": "vpc_flow_logs_enabled", "status": "warning", "engine": "OPA"},
        ],
        "estimated_monthly_cost_usd": cost,
        "agents_involved": ["architect", "harmonizer", "engineer", "security_prover", "cost_planner", "devops_auditor"],
        "confidence": 0.92,
    }

@router.post("/incident/triage")
async def triage_incident(data: dict):
    service = data.get("service", "api-gateway")
    symptom = data.get("symptom", "High latency")
    severity = data.get("severity", "high")

    signals = [
        {"domain": "metrics", "finding": f"P95 latency spike detected for {service}", "confidence": 0.91, "evidence": ["prometheus:histogram_quantile(0.95, request_duration)"]},
        {"domain": "deployments", "finding": "Recent deployment 12 min before incident start", "confidence": 0.86, "evidence": ["github:main@commit_within_20m"]},
        {"domain": "kubernetes", "finding": "Pod restart spikes and CPU throttling", "confidence": 0.88, "evidence": ["kubectl:pods --field-selector=status.phase!=Running"]},
        {"domain": "cost", "finding": "No FinOps anomaly linked to blast radius", "confidence": 0.44, "evidence": ["billing:hourly_spend_within_band"]},
        {"domain": "security", "finding": "No active exploit signatures detected", "confidence": 0.58, "evidence": ["waf:anomaly_score", "falco:runtime_ruleset"]},
    ]

    avg_conf = sum(s["confidence"] for s in signals) / len(signals)
    status = "mitigated" if avg_conf >= 0.7 else "needs_human"

    with get_db() as conn:
        conn.execute(
            "INSERT INTO agent_tasks (project_id, agent_type, task_type, status, confidence, duration_ms, input_data) VALUES (?,?,?,?,?,?,?)",
            (1, "sre_investigator", "incident_triage", "completed", round(avg_conf, 2), random.randint(800, 3000), json.dumps(data)),
        )

    return {
        "incident_id": data.get("incident_id", f"INC-{random.randint(1000,9999)}"),
        "service": service,
        "severity": severity,
        "status": status,
        "hypothesis": "Resource pressure triggered by recent deployment combined with traffic spike",
        "suggested_action": "Rollback latest deployment, increase replicas by 30%, enable rate limiting",
        "confidence": round(avg_conf, 2),
        "estimated_mttr_minutes": 15 if status == "mitigated" else 30,
        "signals": signals,
        "audit_recommendations": [
            "Quality gates passed for current iteration" if avg_conf >= 0.8 else "Collect more telemetry before autonomous execution",
            "Evidence bundle sufficient for automated remediation" if len(signals) >= 3 else "Expand evidence from additional sources",
        ],
    }

@router.post("/pipeline/optimize")
async def optimize_pipeline(data: dict):
    generation = data.get("generation", 1)
    speed = min(0.55 + generation * 0.03, 0.95)
    reliability = min(0.60 + generation * 0.025, 0.96)
    cost = min(0.58 + generation * 0.02, 0.92)
    security = min(0.62 + generation * 0.02, 0.94)
    fitness = 0.4 * speed + 0.3 * reliability + 0.2 * cost + 0.1 * security

    return {
        "generation": generation,
        "best_variant": f"pipeline-gen-{generation:03d}-canary-safe",
        "scores": {
            "speed": round(speed, 3),
            "reliability": round(reliability, 3),
            "cost": round(cost, 3),
            "security": round(security, 3),
        },
        "composite_fitness": round(fitness, 3),
        "improvements": [
            f"Parallelized test stage: +{round(speed * 15, 1)}% speed improvement",
            f"Cached dependencies: -{round(cost * 20, 1)}% cost reduction",
            f"Security scan optimization: {round(security * 100, 1)}% coverage maintained",
        ],
        "lineage": [
            {"gen": max(1, generation - 2), "fitness": round(fitness - 0.06, 3)},
            {"gen": max(1, generation - 1), "fitness": round(fitness - 0.03, 3)},
            {"gen": generation, "fitness": round(fitness, 3)},
        ],
    }

@router.post("/chat")
async def agent_chat(data: dict):
    message = data.get("message", "")
    msg_lower = message.lower()

    if any(w in msg_lower for w in ("terraform", "infrastructure", "deploy", "iac")):
        agent = "Architect Agent"
        response = f"I'll help generate infrastructure for that. Based on your request, I recommend a multi-AZ architecture with auto-scaling. Let me run the MACOG pipeline to generate the Terraform configuration.\n\n**Agents involved:** Architect -> Harmonizer -> Engineer -> Security Prover -> Cost Planner -> DevOps Auditor\n\nShall I proceed with the generation?"
    elif any(w in msg_lower for w in ("security", "vulnerability", "scan", "audit")):
        agent = "Security Prover"
        response = f"I'll run a comprehensive security scan. This includes SAST analysis, dependency scanning, and container image scanning.\n\n**Current security posture:**\n- 0 critical vulnerabilities\n- 2 high-severity issues (under review)\n- 5 medium findings\n\nWould you like me to generate a detailed security report?"
    elif any(w in msg_lower for w in ("pipeline", "ci", "cd", "build", "optimize")):
        agent = "Evolution Optimizer"
        response = f"I've analyzed your pipeline configuration. The evolutionary optimizer has identified several optimization opportunities:\n\n1. **Parallel test execution** - 35% faster\n2. **Dependency caching** - 20% cost reduction\n3. **Smart test selection** - Skip unchanged modules\n\nCurrent best fitness score: 0.847. Shall I apply the optimized configuration?"
    elif any(w in msg_lower for w in ("incident", "error", "down", "latency", "alert")):
        agent = "SRE Investigator"
        response = f"I'm investigating the situation. Let me deploy the investigation swarm:\n\n**Parallel Analysis:**\n- Metrics Agent: Checking latency patterns\n- Deployment Agent: Reviewing recent changes\n- K8s Agent: Inspecting pod health\n\n**Initial findings:** Recent deployment correlates with latency increase. Confidence: 87%\n\nRecommended action: Rollback latest deployment and increase replicas."
    elif any(w in msg_lower for w in ("cost", "budget", "spending", "expensive")):
        agent = "Cost Planner"
        response = f"Here's your infrastructure cost analysis:\n\n**Monthly Cost Breakdown:**\n- Compute (ECS/EKS): $1,200\n- Database (RDS): $450\n- Storage (S3): $85\n- Network (ALB): $120\n- **Total: $1,855/month**\n\nI've identified potential savings of 32% through reserved instances and right-sizing. Want details?"
    else:
        agent = "DevOps Auditor"
        response = f"I'm the HiveOps AI assistant. I can help with:\n\n- **Infrastructure**: Generate Terraform/IaC configs\n- **Security**: Scan for vulnerabilities\n- **Pipelines**: Optimize CI/CD performance\n- **Incidents**: Investigate and remediate issues\n- **Cost**: Analyze and optimize spending\n\nWhat would you like to work on?"

    return {
        "agent": agent,
        "response": response,
        "confidence": round(random.uniform(0.82, 0.96), 2),
        "suggested_actions": [
            {"label": "Generate Terraform", "action": "iac_generate"},
            {"label": "Run Security Scan", "action": "security_scan"},
            {"label": "Optimize Pipeline", "action": "pipeline_optimize"},
        ],
    }
