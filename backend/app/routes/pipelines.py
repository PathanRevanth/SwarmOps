import json
from fastapi import APIRouter, HTTPException
from ..database import get_db
from ..models.schemas import PipelineCreate, PipelineResponse, JobResponse

router = APIRouter(prefix="/api/pipelines", tags=["pipelines"])

@router.get("")
async def list_pipelines(project_id: int = 0, status: str = "", limit: int = 20, offset: int = 0):
    with get_db() as conn:
        q = "SELECT p.*, u.username as triggered_by_name FROM pipelines p LEFT JOIN users u ON p.triggered_by = u.id WHERE 1=1"
        params = []
        if project_id:
            q += " AND p.project_id = ?"
            params.append(project_id)
        if status:
            q += " AND p.status = ?"
            params.append(status)
        q += " ORDER BY p.created_at DESC LIMIT ? OFFSET ?"
        params += [limit, offset]
        rows = conn.execute(q, params).fetchall()
        total_q = "SELECT COUNT(*) as c FROM pipelines WHERE 1=1"
        total_params = []
        if project_id:
            total_q += " AND project_id = ?"
            total_params.append(project_id)
        if status:
            total_q += " AND status = ?"
            total_params.append(status)
        total = conn.execute(total_q, total_params).fetchone()["c"]
        items = []
        for r in rows:
            d = dict(r)
            jobs = conn.execute("SELECT * FROM pipeline_jobs WHERE pipeline_id = ? ORDER BY id", (r["id"],)).fetchall()
            d["jobs"] = [dict(j) for j in jobs]
            stages_set = []
            for j in jobs:
                if j["stage"] not in stages_set:
                    stages_set.append(j["stage"])
            d["stages"] = stages_set
            proj = conn.execute("SELECT name, namespace FROM projects WHERE id = ?", (r["project_id"],)).fetchone()
            d["project_name"] = f"{proj['namespace']}/{proj['name']}" if proj else ""
            items.append(d)
        return {"items": items, "total": total}

@router.get("/{pipeline_id}")
async def get_pipeline(pipeline_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT p.*, u.username as triggered_by_name FROM pipelines p LEFT JOIN users u ON p.triggered_by = u.id WHERE p.id = ?", (pipeline_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Pipeline not found")
        d = dict(row)
        jobs = conn.execute("SELECT * FROM pipeline_jobs WHERE pipeline_id = ? ORDER BY id", (pipeline_id,)).fetchall()
        d["jobs"] = [dict(j) for j in jobs]
        stages_set = []
        for j in jobs:
            if j["stage"] not in stages_set:
                stages_set.append(j["stage"])
        d["stages"] = stages_set
        return d

@router.get("/{pipeline_id}/jobs")
async def list_jobs(pipeline_id: int):
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM pipeline_jobs WHERE pipeline_id = ? ORDER BY id", (pipeline_id,)).fetchall()
        return [dict(r) for r in rows]

@router.get("/jobs/{job_id}")
async def get_job(job_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM pipeline_jobs WHERE id = ?", (job_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Job not found")
        return dict(row)

@router.get("/jobs/{job_id}/log")
async def get_job_log(job_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT log_output FROM pipeline_jobs WHERE id = ?", (job_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Job not found")
        return {"log": row["log_output"]}

@router.post("/{pipeline_id}/retry")
async def retry_pipeline(pipeline_id: int):
    with get_db() as conn:
        conn.execute("UPDATE pipelines SET status = 'pending' WHERE id = ?", (pipeline_id,))
        conn.execute("UPDATE pipeline_jobs SET status = 'pending', exit_code = -1 WHERE pipeline_id = ? AND status = 'failed'", (pipeline_id,))
        return {"message": "Pipeline retry triggered"}

@router.post("/{pipeline_id}/cancel")
async def cancel_pipeline(pipeline_id: int):
    with get_db() as conn:
        conn.execute("UPDATE pipelines SET status = 'canceled' WHERE id = ?", (pipeline_id,))
        conn.execute("UPDATE pipeline_jobs SET status = 'canceled' WHERE pipeline_id = ? AND status IN ('pending', 'running')", (pipeline_id,))
        return {"message": "Pipeline canceled"}

@router.post("/trigger")
async def trigger_pipeline(data: PipelineCreate):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO pipelines (project_id, ref, status, source) VALUES (?,?,?,?)",
            (1, data.ref, "running", "manual"),
        )
        pid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        for name, stage in [("build", "build"), ("test:unit", "test"), ("security:sast", "security")]:
            conn.execute(
                "INSERT INTO pipeline_jobs (pipeline_id, name, stage, status, image) VALUES (?,?,?,?,?)",
                (pid, name, stage, "pending", "node:18-alpine"),
            )
        return {"id": pid, "status": "running"}
