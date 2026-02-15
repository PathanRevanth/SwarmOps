from fastapi import APIRouter, HTTPException
from ..database import get_db
from ..services.auth import hash_password, verify_password, create_token
from ..models.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
async def register(data: UserCreate):
    with get_db() as conn:
        existing = conn.execute("SELECT id FROM users WHERE username = ? OR email = ?", (data.username, data.email)).fetchone()
        if existing:
            raise HTTPException(400, "Username or email already exists")
        pw = hash_password(data.password)
        conn.execute(
            "INSERT INTO users (username, email, full_name, password_hash) VALUES (?,?,?,?)",
            (data.username, data.email, data.full_name, pw),
        )
        user = conn.execute("SELECT * FROM users WHERE username = ?", (data.username,)).fetchone()
        token = create_token(user["id"], user["username"])
        return TokenResponse(
            access_token=token,
            user=UserResponse(
                id=user["id"], username=user["username"], email=user["email"],
                full_name=user["full_name"], avatar_url=user["avatar_url"] or "",
                role=user["role"], created_at=user["created_at"],
            ),
        )

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (data.username,)).fetchone()
        if not user or not verify_password(data.password, user["password_hash"]):
            raise HTTPException(401, "Invalid credentials")
        token = create_token(user["id"], user["username"])
        return TokenResponse(
            access_token=token,
            user=UserResponse(
                id=user["id"], username=user["username"], email=user["email"],
                full_name=user["full_name"], avatar_url=user["avatar_url"] or "",
                role=user["role"], created_at=user["created_at"],
            ),
        )

@router.get("/me", response_model=UserResponse)
async def get_me():
    from ..services.auth import require_auth
    from fastapi import Depends
    return UserResponse(id=1, username="admin", email="admin@hiveops.io", full_name="Platform Admin", avatar_url="", role="admin", created_at="2026-01-01")
