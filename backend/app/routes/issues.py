import json
from fastapi import APIRouter, HTTPException
from ..database import get_db
from ..models.schemas import IssueCreate, IssueCommentCreate

router = APIRouter(prefix="/api/issues", tags=["issues"])

def _enrich_issue(row, conn):
    d = dict(row)
    d["labels"] = json.loads(d.get("labels", "[]")) if isinstance(d.get("labels"), str) else d.get("labels", [])
    author = conn.execute("SELECT id, username, full_name, email, avatar_url, role, created_at FROM users WHERE id = ?", (d.get("author_id"),)).fetchone() if d.get("author_id") else None
    d["author"] = dict(author) if author else None
    assignee = conn.execute("SELECT id, username, full_name, email, avatar_url, role, created_at FROM users WHERE id = ?", (d.get("assignee_id"),)).fetchone() if d.get("assignee_id") else None
    d["assignee"] = dict(assignee) if assignee else None
    d["comments_count"] = conn.execute("SELECT COUNT(*) as c FROM issue_comments WHERE issue_id = ?", (d["id"],)).fetchone()["c"]
    return d

@router.get("")
async def list_issues(project_id: int = 0, status: str = "", priority: str = "", board_column: str = "", limit: int = 50, offset: int = 0):
    with get_db() as conn:
        q = "SELECT * FROM issues WHERE 1=1"
        params = []
        if project_id:
            q += " AND project_id = ?"
            params.append(project_id)
        if status:
            q += " AND status = ?"
            params.append(status)
        if priority:
            q += " AND priority = ?"
            params.append(priority)
        if board_column:
            q += " AND board_column = ?"
            params.append(board_column)
        q += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params += [limit, offset]
        rows = conn.execute(q, params).fetchall()
        total_q = "SELECT COUNT(*) as c FROM issues WHERE 1=1"
        total_params = []
        if project_id:
            total_q += " AND project_id = ?"
            total_params.append(project_id)
        if status:
            total_q += " AND status = ?"
            total_params.append(status)
        total = conn.execute(total_q, total_params).fetchone()["c"]
        return {"items": [_enrich_issue(r, conn) for r in rows], "total": total}

@router.get("/board")
async def get_board(project_id: int = 1):
    with get_db() as conn:
        columns = ["backlog", "todo", "in_progress", "review", "done"]
        board = {}
        for col in columns:
            rows = conn.execute(
                "SELECT * FROM issues WHERE project_id = ? AND board_column = ? AND status = 'open' ORDER BY priority DESC, created_at DESC",
                (project_id, col),
            ).fetchall()
            board[col] = [_enrich_issue(r, conn) for r in rows]
        return board

@router.get("/{issue_id}")
async def get_issue(issue_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Issue not found")
        return _enrich_issue(row, conn)

@router.post("")
async def create_issue(data: IssueCreate):
    with get_db() as conn:
        max_iid = conn.execute("SELECT COALESCE(MAX(iid), 0) as m FROM issues WHERE project_id = 1").fetchone()["m"]
        conn.execute(
            "INSERT INTO issues (project_id, iid, title, description, priority, labels, assignee_id, author_id, board_column) VALUES (?,?,?,?,?,?,?,?,?)",
            (1, max_iid + 1, data.title, data.description, data.priority, json.dumps(data.labels), data.assignee_id, 1, data.board_column),
        )
        issue_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        row = conn.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
        return _enrich_issue(row, conn)

@router.put("/{issue_id}")
async def update_issue(issue_id: int, data: IssueCreate):
    with get_db() as conn:
        conn.execute(
            "UPDATE issues SET title=?, description=?, priority=?, labels=?, assignee_id=?, board_column=?, updated_at=datetime('now') WHERE id=?",
            (data.title, data.description, data.priority, json.dumps(data.labels), data.assignee_id, data.board_column, issue_id),
        )
        row = conn.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Issue not found")
        return _enrich_issue(row, conn)

@router.post("/{issue_id}/move")
async def move_issue(issue_id: int, column: str = "backlog"):
    with get_db() as conn:
        conn.execute("UPDATE issues SET board_column = ?, updated_at = datetime('now') WHERE id = ?", (column, issue_id))
        return {"message": f"Issue moved to {column}"}

@router.post("/{issue_id}/close")
async def close_issue(issue_id: int):
    with get_db() as conn:
        conn.execute("UPDATE issues SET status = 'closed', closed_at = datetime('now'), updated_at = datetime('now') WHERE id = ?", (issue_id,))
        return {"message": "Issue closed"}

@router.post("/{issue_id}/reopen")
async def reopen_issue(issue_id: int):
    with get_db() as conn:
        conn.execute("UPDATE issues SET status = 'open', closed_at = '', updated_at = datetime('now') WHERE id = ?", (issue_id,))
        return {"message": "Issue reopened"}

@router.get("/{issue_id}/comments")
async def list_comments(issue_id: int):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT c.*, u.username as author_name, u.full_name as author_full_name FROM issue_comments c LEFT JOIN users u ON c.author_id = u.id WHERE c.issue_id = ? ORDER BY c.created_at",
            (issue_id,),
        ).fetchall()
        return [dict(r) for r in rows]

@router.post("/{issue_id}/comments")
async def add_comment(issue_id: int, data: IssueCommentCreate):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO issue_comments (issue_id, author_id, body) VALUES (?,?,?)",
            (issue_id, 1, data.body),
        )
        return {"message": "Comment added"}
