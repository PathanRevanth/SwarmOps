from fastapi import APIRouter, HTTPException
from ..database import get_db

router = APIRouter(prefix="/api/registry", tags=["registry"])

@router.get("/containers")
async def list_container_images(project_id: int = 0, limit: int = 50):
    with get_db() as conn:
        q = "SELECT ci.*, u.username as pushed_by_name FROM container_images ci LEFT JOIN users u ON ci.pushed_by = u.id"
        params = []
        if project_id:
            q += " WHERE ci.project_id = ?"
            params.append(project_id)
        q += " ORDER BY ci.created_at DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(q, params).fetchall()
        return [dict(r) for r in rows]

@router.get("/containers/{image_id}")
async def get_container_image(image_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT ci.*, u.username as pushed_by_name FROM container_images ci LEFT JOIN users u ON ci.pushed_by = u.id WHERE ci.id = ?", (image_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Image not found")
        return dict(row)

@router.get("/packages")
async def list_packages(project_id: int = 0, package_type: str = "", limit: int = 50):
    with get_db() as conn:
        q = "SELECT p.*, u.username as published_by_name FROM packages p LEFT JOIN users u ON p.published_by = u.id WHERE 1=1"
        params = []
        if project_id:
            q += " AND p.project_id = ?"
            params.append(project_id)
        if package_type:
            q += " AND p.package_type = ?"
            params.append(package_type)
        q += " ORDER BY p.created_at DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(q, params).fetchall()
        return [dict(r) for r in rows]

@router.get("/packages/{package_id}")
async def get_package(package_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT p.*, u.username as published_by_name FROM packages p LEFT JOIN users u ON p.published_by = u.id WHERE p.id = ?", (package_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Package not found")
        return dict(row)
