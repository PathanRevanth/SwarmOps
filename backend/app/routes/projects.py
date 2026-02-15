import json
from fastapi import APIRouter, HTTPException, Query
from ..database import get_db
from ..models.schemas import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/api/projects", tags=["projects"])

def _project_response(row, conn) -> dict:
    pid = row["id"]
    last_commit = conn.execute(
        "SELECT sha, message, author_name, created_at FROM commits WHERE project_id = ? ORDER BY created_at DESC LIMIT 1", (pid,)
    ).fetchone()
    open_issues = conn.execute("SELECT COUNT(*) as c FROM issues WHERE project_id = ? AND status = 'open'", (pid,)).fetchone()["c"]
    open_mrs = conn.execute("SELECT COUNT(*) as c FROM merge_requests WHERE project_id = ? AND status = 'open'", (pid,)).fetchone()["c"]
    latest_pipe = conn.execute("SELECT status FROM pipelines WHERE project_id = ? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    return ProjectResponse(
        id=row["id"], name=row["name"], namespace=row["namespace"],
        description=row["description"], visibility=row["visibility"],
        default_branch=row["default_branch"], avatar_url=row["avatar_url"] or "",
        stars_count=row["stars_count"], forks_count=row["forks_count"],
        owner_id=row["owner_id"], created_at=row["created_at"], updated_at=row["updated_at"],
        last_commit=dict(last_commit) if last_commit else None,
        open_issues_count=open_issues, open_mrs_count=open_mrs,
        pipeline_status=latest_pipe["status"] if latest_pipe else "",
    ).model_dump()

@router.get("")
async def list_projects(search: str = "", visibility: str = "", limit: int = 50, offset: int = 0):
    with get_db() as conn:
        q = "SELECT * FROM projects WHERE 1=1"
        params = []
        if search:
            q += " AND (name LIKE ? OR description LIKE ?)"
            params += [f"%{search}%", f"%{search}%"]
        if visibility:
            q += " AND visibility = ?"
            params.append(visibility)
        q += " ORDER BY updated_at DESC LIMIT ? OFFSET ?"
        params += [limit, offset]
        rows = conn.execute(q, params).fetchall()
        total = conn.execute("SELECT COUNT(*) as c FROM projects").fetchone()["c"]
        return {"items": [_project_response(r, conn) for r in rows], "total": total}

@router.get("/{project_id}")
async def get_project(project_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Project not found")
        return _project_response(row, conn)

@router.post("", response_model=ProjectResponse)
async def create_project(data: ProjectCreate):
    with get_db() as conn:
        existing = conn.execute("SELECT id FROM projects WHERE namespace = ? AND name = ?", (data.namespace, data.name)).fetchone()
        if existing:
            raise HTTPException(400, "Project already exists in this namespace")
        conn.execute(
            "INSERT INTO projects (name, namespace, description, visibility, default_branch, owner_id) VALUES (?,?,?,?,?,?)",
            (data.name, data.namespace, data.description, data.visibility, data.default_branch, 1),
        )
        row = conn.execute("SELECT * FROM projects WHERE namespace = ? AND name = ?", (data.namespace, data.name)).fetchone()
        return _project_response(row, conn)

@router.get("/{project_id}/branches")
async def list_branches(project_id: int):
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM branches WHERE project_id = ? ORDER BY name", (project_id,)).fetchall()
        return [dict(r) for r in rows]

@router.get("/{project_id}/commits")
async def list_commits(project_id: int, branch: str = "main", limit: int = 20, offset: int = 0):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM commits WHERE project_id = ? AND branch = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (project_id, branch, limit, offset),
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) as c FROM commits WHERE project_id = ? AND branch = ?", (project_id, branch)).fetchone()["c"]
        return {"items": [dict(r) for r in rows], "total": total}

@router.get("/{project_id}/tree")
async def get_file_tree(project_id: int, branch: str = "main", path: str = ""):
    with get_db() as conn:
        if path:
            rows = conn.execute(
                "SELECT * FROM repo_files WHERE project_id = ? AND branch = ? AND path LIKE ? AND path != ? ORDER BY file_type DESC, name",
                (project_id, branch, f"{path}/%", path),
            ).fetchall()
            result = []
            for r in rows:
                rel = r["path"][len(path)+1:] if r["path"].startswith(path + "/") else r["path"]
                if "/" not in rel:
                    result.append(dict(r))
            return result
        else:
            rows = conn.execute(
                "SELECT * FROM repo_files WHERE project_id = ? AND branch = ? AND path NOT LIKE '%/%' ORDER BY file_type DESC, name",
                (project_id, branch),
            ).fetchall()
            top_dirs = conn.execute(
                "SELECT DISTINCT SUBSTR(path, 1, INSTR(path || '/', '/') - 1) as top FROM repo_files WHERE project_id = ? AND branch = ? AND path LIKE '%/%'",
                (project_id, branch),
            ).fetchall()
            items = [dict(r) for r in rows]
            seen = {i["path"] for i in items}
            for d in top_dirs:
                if d["top"] and d["top"] not in seen:
                    items.append({"name": d["top"], "path": d["top"], "file_type": "tree", "size_bytes": 0, "language": "", "last_commit_sha": "", "last_commit_message": ""})
                    seen.add(d["top"])
            items.sort(key=lambda x: (0 if x["file_type"] == "tree" else 1, x["name"]))
            return items

@router.get("/{project_id}/blob")
async def get_file_content(project_id: int, path: str, branch: str = "main"):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM repo_files WHERE project_id = ? AND branch = ? AND path = ? AND file_type = 'blob'",
            (project_id, branch, path),
        ).fetchone()
        if not row:
            raise HTTPException(404, "File not found")
        return dict(row)

@router.get("/{project_id}/environments")
async def list_environments(project_id: int):
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM environments WHERE project_id = ?", (project_id,)).fetchall()
        return [dict(r) for r in rows]
