import json
from fastapi import APIRouter
from ..database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/stats")
async def get_dashboard_stats():
    with get_db() as conn:
        total_projects = conn.execute("SELECT COUNT(*) as c FROM projects").fetchone()["c"]
        total_pipelines = conn.execute("SELECT COUNT(*) as c FROM pipelines").fetchone()["c"]
        success_pipes = conn.execute("SELECT COUNT(*) as c FROM pipelines WHERE status = 'success'").fetchone()["c"]
        success_rate = round(success_pipes / max(total_pipelines, 1) * 100, 1)
        total_mrs = conn.execute("SELECT COUNT(*) as c FROM merge_requests").fetchone()["c"]
        open_issues = conn.execute("SELECT COUNT(*) as c FROM issues WHERE status = 'open'").fetchone()["c"]
        total_commits = conn.execute("SELECT COUNT(*) as c FROM commits").fetchone()["c"]
        total_images = conn.execute("SELECT COUNT(*) as c FROM container_images").fetchone()["c"]
        total_packages = conn.execute("SELECT COUNT(*) as c FROM packages").fetchone()["c"]

        recent_pipelines = conn.execute(
            "SELECT p.id, p.status, p.ref, p.duration_seconds, p.created_at, pr.name as project_name, pr.namespace FROM pipelines p JOIN projects pr ON p.project_id = pr.id ORDER BY p.created_at DESC LIMIT 8"
        ).fetchall()

        recent_commits = conn.execute(
            "SELECT c.sha, c.message, c.author_name, c.created_at, pr.name as project_name FROM commits c JOIN projects pr ON c.project_id = pr.id ORDER BY c.created_at DESC LIMIT 8"
        ).fetchall()

        recent_issues = conn.execute(
            "SELECT i.id, i.iid, i.title, i.priority, i.status, i.created_at, pr.name as project_name FROM issues i JOIN projects pr ON i.project_id = pr.id ORDER BY i.created_at DESC LIMIT 6"
        ).fetchall()

        agent_tasks = conn.execute(
            "SELECT agent_type, task_type, status, confidence, duration_ms, created_at FROM agent_tasks ORDER BY created_at DESC LIMIT 10"
        ).fetchall()

        pipe_statuses = conn.execute(
            "SELECT status, COUNT(*) as count FROM pipelines GROUP BY status"
        ).fetchall()

        return {
            "total_projects": total_projects,
            "total_pipelines": total_pipelines,
            "pipeline_success_rate": success_rate,
            "total_merge_requests": total_mrs,
            "open_issues": open_issues,
            "total_commits": total_commits,
            "active_agents": 8,
            "container_images": total_images,
            "packages": total_packages,
            "recent_pipelines": [dict(r) for r in recent_pipelines],
            "recent_commits": [dict(r) for r in recent_commits],
            "recent_issues": [dict(r) for r in recent_issues],
            "agent_activity": [dict(r) for r in agent_tasks],
            "pipeline_breakdown": [dict(r) for r in pipe_statuses],
            "pipeline_trends": [
                {"day": "Mon", "success": 12, "failed": 2, "total": 14},
                {"day": "Tue", "success": 15, "failed": 1, "total": 16},
                {"day": "Wed", "success": 18, "failed": 3, "total": 21},
                {"day": "Thu", "success": 14, "failed": 2, "total": 16},
                {"day": "Fri", "success": 20, "failed": 1, "total": 21},
                {"day": "Sat", "success": 8, "failed": 0, "total": 8},
                {"day": "Sun", "success": 5, "failed": 1, "total": 6},
            ],
            "security_overview": {
                "critical": 0,
                "high": 2,
                "medium": 5,
                "low": 12,
                "total_scans": 45,
                "last_scan": "2026-02-15T12:00:00Z",
            },
            "cost_summary": {
                "current_monthly": 1855,
                "projected_monthly": 2100,
                "savings_identified": 594,
                "optimization_score": 78,
            },
        }

@router.get("/activity")
async def get_activity_feed(limit: int = 20):
    with get_db() as conn:
        activities = []
        commits = conn.execute(
            "SELECT 'commit' as type, c.sha as ref, c.message as title, c.author_name as actor, c.created_at, pr.name as project FROM commits c JOIN projects pr ON c.project_id = pr.id ORDER BY c.created_at DESC LIMIT ?",
            (limit // 3,),
        ).fetchall()
        activities.extend([dict(r) for r in commits])

        mrs = conn.execute(
            "SELECT 'merge_request' as type, CAST(m.iid AS TEXT) as ref, m.title, u.username as actor, m.created_at, pr.name as project FROM merge_requests m JOIN projects pr ON m.project_id = pr.id LEFT JOIN users u ON m.author_id = u.id ORDER BY m.created_at DESC LIMIT ?",
            (limit // 3,),
        ).fetchall()
        activities.extend([dict(r) for r in mrs])

        pipes = conn.execute(
            "SELECT 'pipeline' as type, CAST(p.id AS TEXT) as ref, p.status as title, u.username as actor, p.created_at, pr.name as project FROM pipelines p JOIN projects pr ON p.project_id = pr.id LEFT JOIN users u ON p.triggered_by = u.id ORDER BY p.created_at DESC LIMIT ?",
            (limit // 3,),
        ).fetchall()
        activities.extend([dict(r) for r in pipes])

        activities.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return activities[:limit]
