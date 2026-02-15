import json
from fastapi import APIRouter, HTTPException
from ..database import get_db
from ..models.schemas import MergeRequestCreate, MRCommentCreate

router = APIRouter(prefix="/api/merge-requests", tags=["merge_requests"])

def _enrich_mr(row, conn):
    d = dict(row)
    author = conn.execute("SELECT id, username, full_name, email, avatar_url, role, created_at FROM users WHERE id = ?", (d.get("author_id"),)).fetchone() if d.get("author_id") else None
    d["author"] = dict(author) if author else None
    assignee = conn.execute("SELECT id, username, full_name, email, avatar_url, role, created_at FROM users WHERE id = ?", (d.get("assignee_id"),)).fetchone() if d.get("assignee_id") else None
    d["assignee"] = dict(assignee) if assignee else None
    d["comments_count"] = conn.execute("SELECT COUNT(*) as c FROM mr_comments WHERE merge_request_id = ?", (d["id"],)).fetchone()["c"]
    pipe = conn.execute("SELECT status FROM pipelines WHERE id = ?", (d.get("pipeline_id"),)).fetchone() if d.get("pipeline_id") else None
    d["pipeline_status"] = pipe["status"] if pipe else ""
    return d

@router.get("")
async def list_merge_requests(project_id: int = 0, status: str = "", limit: int = 20, offset: int = 0):
    with get_db() as conn:
        q = "SELECT * FROM merge_requests WHERE 1=1"
        params = []
        if project_id:
            q += " AND project_id = ?"
            params.append(project_id)
        if status:
            q += " AND status = ?"
            params.append(status)
        q += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params += [limit, offset]
        rows = conn.execute(q, params).fetchall()
        total_q = "SELECT COUNT(*) as c FROM merge_requests WHERE 1=1"
        total_params = []
        if project_id:
            total_q += " AND project_id = ?"
            total_params.append(project_id)
        if status:
            total_q += " AND status = ?"
            total_params.append(status)
        total = conn.execute(total_q, total_params).fetchone()["c"]
        return {"items": [_enrich_mr(r, conn) for r in rows], "total": total}

@router.get("/{mr_id}")
async def get_merge_request(mr_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM merge_requests WHERE id = ?", (mr_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Merge request not found")
        return _enrich_mr(row, conn)

@router.get("/{mr_id}/diffs")
async def get_mr_diffs(mr_id: int):
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM mr_diffs WHERE merge_request_id = ?", (mr_id,)).fetchall()
        return [dict(r) for r in rows]

@router.get("/{mr_id}/comments")
async def get_mr_comments(mr_id: int):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT c.*, u.username as author_name, u.full_name as author_full_name, u.avatar_url as author_avatar FROM mr_comments c LEFT JOIN users u ON c.author_id = u.id WHERE c.merge_request_id = ? ORDER BY c.created_at",
            (mr_id,),
        ).fetchall()
        return [dict(r) for r in rows]

@router.post("/{mr_id}/comments")
async def add_mr_comment(mr_id: int, data: MRCommentCreate):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO mr_comments (merge_request_id, author_id, body, file_path, line_number, parent_id) VALUES (?,?,?,?,?,?)",
            (mr_id, 1, data.body, data.file_path, data.line_number, data.parent_id),
        )
        return {"message": "Comment added"}

@router.post("/{mr_id}/approve")
async def approve_mr(mr_id: int):
    with get_db() as conn:
        conn.execute("UPDATE merge_requests SET approved = 1, updated_at = datetime('now') WHERE id = ?", (mr_id,))
        return {"message": "Merge request approved"}

@router.post("/{mr_id}/merge")
async def merge_mr(mr_id: int):
    with get_db() as conn:
        mr = conn.execute("SELECT * FROM merge_requests WHERE id = ?", (mr_id,)).fetchone()
        if not mr:
            raise HTTPException(404, "Merge request not found")
        if mr["status"] != "open":
            raise HTTPException(400, "MR is not open")
        conn.execute("UPDATE merge_requests SET status = 'merged', merged_at = datetime('now'), updated_at = datetime('now') WHERE id = ?", (mr_id,))
        return {"message": "Merge request merged"}

@router.post("/{mr_id}/close")
async def close_mr(mr_id: int):
    with get_db() as conn:
        conn.execute("UPDATE merge_requests SET status = 'closed', updated_at = datetime('now') WHERE id = ?", (mr_id,))
        return {"message": "Merge request closed"}

@router.post("")
async def create_merge_request(data: MergeRequestCreate):
    with get_db() as conn:
        max_iid = conn.execute("SELECT COALESCE(MAX(iid), 0) as m FROM merge_requests WHERE project_id = 1").fetchone()["m"]
        conn.execute(
            "INSERT INTO merge_requests (project_id, iid, title, description, source_branch, target_branch, author_id, status) VALUES (?,?,?,?,?,?,?,?)",
            (1, max_iid + 1, data.title, data.description, data.source_branch, data.target_branch, 1, "open"),
        )
        mr_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        row = conn.execute("SELECT * FROM merge_requests WHERE id = ?", (mr_id,)).fetchone()
        return _enrich_mr(row, conn)
