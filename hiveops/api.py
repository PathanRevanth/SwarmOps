from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response

from .evolution import EvolutionaryOptimizer
from .macog import MacogGenerator
from .models import (
    EvolutionRequest,
    EvolutionResponse,
    HealthResponse,
    IacRequest,
    IacResponse,
    IncidentRequest,
    InvestigationResult,
    PlatformRoadmapResponse,
)
from .orchestrator import SwarmOrchestrator
from .plans import StartupAlignmentPlan, build_alignment_plan
from .roadmap import build_platform_roadmap

app = FastAPI(title="HiveOps Platform", version="0.3.0")
orchestrator = SwarmOrchestrator()
macog = MacogGenerator()
evolution = EvolutionaryOptimizer()


@app.get("/", response_class=HTMLResponse)
async def dashboard() -> str:
    return """
    <html>
      <head>
        <title>HiveOps Platform</title>
        <style>
          body { font-family: Inter, Arial, sans-serif; margin: 2rem; background: #0b1020; color: #e6ecff; }
          .card { background: #141b33; border: 1px solid #2d3c70; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1rem; }
          code { background: #1b274a; padding: 0.2rem 0.35rem; border-radius: 6px; display:block; overflow-x:auto; }
          h1,h3 { margin-top: 0; }
          .ok { color: #7ef7b8; }
          ul { line-height: 1.6; }
        </style>
      </head>
      <body>
        <h1>🐝 HiveOps Platform</h1>
        <div class="card">
          <p class="ok"><strong>Status:</strong> Online</p>
          <p>Phase-by-phase autonomous DevOps platform demo is running.</p>
        </div>
        <div class="card">
          <h3>Implemented Phases</h3>
          <ul>
            <li>Phase 1: Autonomous SRE triage swarm</li>
            <li>Phase 2: POETIQ-style self-audit loop</li>
            <li>Phase 3: MACOG-style IaC generation</li>
            <li>Phase 4: Evolutionary pipeline optimization</li>
          </ul>
        </div>
        <div class="card">
          <h3>Endpoints</h3>
          <ul>
            <li><code>GET /health</code></li>
            <li><code>GET /platform/roadmap</code></li>
            <li><code>GET /platform/plan/alignment</code></li>
            <li><code>GET /platform/screenshot</code></li>
            <li><code>POST /incidents/triage</code></li>
            <li><code>POST /iac/generate</code></li>
            <li><code>POST /pipelines/evolve</code></li>
            <li><code>GET /docs</code></li>
          </ul>
        </div>
      </body>
    </html>
    """


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", version=app.version, agents=len(orchestrator.agents))




@app.get("/platform/screenshot")
async def platform_screenshot() -> Response:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b1020"/>
      <stop offset="100%" stop-color="#111a35"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="675" fill="url(#bg)"/>
  <text x="80" y="140" fill="#7ef7b8" font-family="Arial" font-size="52" font-weight="700">HiveOps Platform</text>
  <text x="80" y="195" fill="#e6ecff" font-family="Arial" font-size="28">Autonomous DevOps • Phase-by-Phase Demo Snapshot</text>
  <rect x="80" y="245" width="1040" height="320" rx="18" fill="#141b33" stroke="#2d3c70"/>
  <text x="120" y="305" fill="#e6ecff" font-family="Arial" font-size="28">Implemented:</text>
  <text x="140" y="355" fill="#c8d4ff" font-family="Arial" font-size="24">• Phase 1: Swarm incident triage</text>
  <text x="140" y="395" fill="#c8d4ff" font-family="Arial" font-size="24">• Phase 2: POETIQ-style meta-audit</text>
  <text x="140" y="435" fill="#c8d4ff" font-family="Arial" font-size="24">• Phase 3: MACOG-style IaC generation</text>
  <text x="140" y="475" fill="#c8d4ff" font-family="Arial" font-size="24">• Phase 4: Evolutionary pipeline optimizer</text>
  <text x="80" y="620" fill="#8ea3ff" font-family="Arial" font-size="22">Stable endpoint: /platform/screenshot (avoids expiring artifact links)</text>
</svg>"""
    return Response(content=svg, media_type="image/svg+xml")

@app.get("/platform/roadmap", response_model=PlatformRoadmapResponse)
async def platform_roadmap() -> PlatformRoadmapResponse:
    return build_platform_roadmap()


@app.get("/platform/plan/alignment", response_model=StartupAlignmentPlan)
async def platform_alignment_plan() -> StartupAlignmentPlan:
    return build_alignment_plan()


@app.post("/incidents/triage", response_model=InvestigationResult)
async def triage_incident(incident: IncidentRequest) -> InvestigationResult:
    return await orchestrator.triage(incident)


@app.post("/iac/generate", response_model=IacResponse)
async def generate_iac(req: IacRequest) -> IacResponse:
    plan = macog.generate(intent=req.intent, provider=req.provider)
    return IacResponse(**asdict(plan))


@app.post("/pipelines/evolve", response_model=EvolutionResponse)
async def evolve_pipeline(req: EvolutionRequest) -> EvolutionResponse:
    result = evolution.evolve(generation=req.generation)
    return EvolutionResponse(**asdict(result))
