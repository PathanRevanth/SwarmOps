from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    email: str
    full_name: str = ""
    password: str = Field(min_length=4)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    avatar_url: str
    role: str
    created_at: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    namespace: str = Field(min_length=1, max_length=100)
    description: str = ""
    visibility: str = "private"
    default_branch: str = "main"

class ProjectResponse(BaseModel):
    id: int
    name: str
    namespace: str
    description: str
    visibility: str
    default_branch: str
    avatar_url: str
    stars_count: int
    forks_count: int
    owner_id: Optional[int] = None
    created_at: str
    updated_at: str
    last_commit: Optional[dict] = None
    open_issues_count: int = 0
    open_mrs_count: int = 0
    pipeline_status: str = ""

class BranchResponse(BaseModel):
    id: int
    name: str
    commit_sha: str
    is_protected: bool
    created_at: str

class CommitCreate(BaseModel):
    message: str
    branch: str = "main"
    files: list[dict] = []

class CommitResponse(BaseModel):
    id: int
    sha: str
    message: str
    author_name: str
    author_email: str
    branch: str
    parent_sha: str
    files_changed: int
    additions: int
    deletions: int
    created_at: str

class FileTreeItem(BaseModel):
    name: str
    path: str
    file_type: str
    size_bytes: int
    language: str
    last_commit_sha: str
    last_commit_message: str

class FileContentResponse(BaseModel):
    name: str
    path: str
    content: str
    size_bytes: int
    language: str
    last_commit_sha: str

class PipelineCreate(BaseModel):
    ref: str = "main"
    variables: dict = {}

class PipelineResponse(BaseModel):
    id: int
    project_id: int
    ref: str
    sha: str
    status: str
    source: str
    duration_seconds: int
    created_at: str
    started_at: str
    finished_at: str
    triggered_by: Optional[int] = None
    jobs: list[dict] = []
    stages: list[str] = []

class JobResponse(BaseModel):
    id: int
    pipeline_id: int
    name: str
    stage: str
    status: str
    image: str
    duration_seconds: int
    exit_code: int
    log_output: str
    allow_failure: bool
    needs: list[str]
    started_at: str
    finished_at: str

class MergeRequestCreate(BaseModel):
    title: str
    description: str = ""
    source_branch: str
    target_branch: str = "main"
    assignee_id: Optional[int] = None

class MergeRequestResponse(BaseModel):
    id: int
    project_id: int
    iid: int
    title: str
    description: str
    source_branch: str
    target_branch: str
    status: str
    author_id: Optional[int] = None
    author: Optional[UserResponse] = None
    assignee_id: Optional[int] = None
    pipeline_id: Optional[int] = None
    pipeline_status: str = ""
    merge_commit_sha: str
    files_changed: int
    additions: int
    deletions: int
    ai_review_status: str
    ai_review_summary: str
    approved: bool
    comments_count: int = 0
    created_at: str
    updated_at: str
    merged_at: str

class MRCommentCreate(BaseModel):
    body: str
    file_path: str = ""
    line_number: int = 0
    parent_id: int = 0

class MRCommentResponse(BaseModel):
    id: int
    merge_request_id: int
    author_id: Optional[int] = None
    author: Optional[UserResponse] = None
    body: str
    file_path: str
    line_number: int
    is_ai_generated: bool
    is_resolved: bool
    parent_id: int
    created_at: str

class DiffResponse(BaseModel):
    file_path: str
    old_path: str
    diff_content: str
    change_type: str
    additions: int
    deletions: int

class IssueCreate(BaseModel):
    title: str
    description: str = ""
    priority: str = "medium"
    labels: list[str] = []
    assignee_id: Optional[int] = None
    milestone: str = ""
    due_date: str = ""
    board_column: str = "backlog"

class IssueResponse(BaseModel):
    id: int
    project_id: int
    iid: int
    title: str
    description: str
    status: str
    priority: str
    labels: list[str]
    assignee_id: Optional[int] = None
    assignee: Optional[UserResponse] = None
    author_id: Optional[int] = None
    author: Optional[UserResponse] = None
    milestone: str
    due_date: str
    time_estimate: int
    time_spent: int
    board_column: str
    ai_triage_status: str
    ai_triage_summary: str
    comments_count: int = 0
    created_at: str
    updated_at: str
    closed_at: str

class IssueCommentCreate(BaseModel):
    body: str

class IssueCommentResponse(BaseModel):
    id: int
    issue_id: int
    author_id: Optional[int] = None
    author: Optional[UserResponse] = None
    body: str
    is_ai_generated: bool
    created_at: str

class ContainerImageResponse(BaseModel):
    id: int
    project_id: int
    name: str
    tag: str
    digest: str
    size_bytes: int
    layers_count: int
    scan_status: str
    vulnerabilities_count: int
    pushed_by: Optional[int] = None
    created_at: str

class PackageResponse(BaseModel):
    id: int
    project_id: int
    name: str
    version: str
    package_type: str
    size_bytes: int
    downloads: int
    published_by: Optional[int] = None
    created_at: str

class AgentTaskResponse(BaseModel):
    id: int
    project_id: Optional[int] = None
    agent_type: str
    task_type: str
    status: str
    input_data: dict
    output_data: dict
    confidence: float
    duration_ms: int
    created_at: str
    completed_at: str

class IaCGenerateRequest(BaseModel):
    intent: str = Field(min_length=5)
    provider: str = "aws"

class IncidentTriageRequest(BaseModel):
    incident_id: str
    service: str
    symptom: str
    severity: str = "medium"
    environment: str = "prod"

class PipelineOptimizeRequest(BaseModel):
    generation: int = 1

class DashboardStats(BaseModel):
    total_projects: int = 0
    total_pipelines: int = 0
    pipeline_success_rate: float = 0.0
    total_merge_requests: int = 0
    open_issues: int = 0
    total_commits: int = 0
    active_agents: int = 8
    container_images: int = 0
    packages: int = 0
    recent_pipelines: list[dict] = []
    recent_commits: list[dict] = []
    recent_issues: list[dict] = []
    agent_activity: list[dict] = []
    pipeline_trends: list[dict] = []

class EnvironmentResponse(BaseModel):
    id: int
    project_id: int
    name: str
    url: str
    status: str
    last_deployment_at: str
    created_at: str
