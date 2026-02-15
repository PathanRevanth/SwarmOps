from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .services.seed import seed_demo_data
from .routes import auth, projects, pipelines, merge_requests, issues, registry, agents, dashboard

app = FastAPI(title="HiveOps Platform", version="1.0.0", description="AI-Native DevOps Platform")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(pipelines.router)
app.include_router(merge_requests.router)
app.include_router(issues.router)
app.include_router(registry.router)
app.include_router(agents.router)
app.include_router(dashboard.router)

@app.on_event("startup")
async def startup():
    init_db()
    seed_demo_data()

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "platform": "HiveOps", "version": "1.0.0"}
