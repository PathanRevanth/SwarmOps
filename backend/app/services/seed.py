import json
import hashlib
import random
from datetime import datetime, timedelta, timezone
from ..database import get_db
from .auth import hash_password


def seed_demo_data():
    with get_db() as conn:
        existing = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()
        if existing["c"] > 0:
            return

        now = datetime.now(timezone.utc)

        pw = hash_password("admin123")
        conn.execute(
            "INSERT INTO users (username, email, full_name, password_hash, role) VALUES (?,?,?,?,?)",
            ("admin", "admin@hiveops.io", "Platform Admin", pw, "admin"),
        )
        conn.execute(
            "INSERT INTO users (username, email, full_name, password_hash, role) VALUES (?,?,?,?,?)",
            ("sarah.chen", "sarah@hiveops.io", "Sarah Chen", pw, "maintainer"),
        )
        conn.execute(
            "INSERT INTO users (username, email, full_name, password_hash, role) VALUES (?,?,?,?,?)",
            ("alex.kim", "alex@hiveops.io", "Alex Kim", pw, "developer"),
        )
        conn.execute(
            "INSERT INTO users (username, email, full_name, password_hash, role) VALUES (?,?,?,?,?)",
            ("hiveops-bot", "bot@hiveops.io", "HiveOps AI Bot", pw, "bot"),
        )

        projects_data = [
            ("web-platform", "hiveops", "Main web platform - React + FastAPI monorepo", "internal"),
            ("infra-core", "hiveops", "Core infrastructure - Terraform modules and K8s manifests", "private"),
            ("ml-pipeline", "hiveops", "ML training and inference pipeline service", "private"),
            ("docs-site", "hiveops", "Documentation site built with MkDocs", "public"),
            ("api-gateway", "hiveops", "API Gateway with rate limiting and auth", "internal"),
            ("mobile-app", "hiveops", "React Native mobile application", "private"),
        ]

        for name, ns, desc, vis in projects_data:
            conn.execute(
                "INSERT INTO projects (name, namespace, description, visibility, owner_id) VALUES (?,?,?,?,?)",
                (name, ns, desc, vis, 1),
            )

        for pid in range(1, 7):
            conn.execute(
                "INSERT INTO repositories (project_id, disk_path, size_bytes) VALUES (?,?,?)",
                (pid, f"/repos/hiveops/{projects_data[pid-1][0]}.git", random.randint(500000, 50000000)),
            )
            for branch_name in ["main", "develop", "feature/auth", "fix/memory-leak"]:
                sha = hashlib.sha1(f"{pid}-{branch_name}".encode()).hexdigest()
                conn.execute(
                    "INSERT INTO branches (project_id, name, commit_sha, is_protected) VALUES (?,?,?,?)",
                    (pid, branch_name, sha, 1 if branch_name == "main" else 0),
                )

        commit_messages = [
            "feat: add user authentication with JWT tokens",
            "fix: resolve memory leak in WebSocket handler",
            "chore: update dependencies to latest versions",
            "feat: implement RBAC permission system",
            "fix: correct pagination offset calculation",
            "refactor: extract service layer from controllers",
            "feat: add real-time pipeline status streaming",
            "docs: update API documentation for v2 endpoints",
            "test: add integration tests for auth flow",
            "feat: implement container registry OCI endpoints",
            "fix: handle concurrent merge request updates",
            "perf: optimize database queries with proper indexing",
            "feat: add AI-powered code review suggestions",
            "security: patch XSS vulnerability in markdown renderer",
            "feat: implement drag-and-drop issue board",
            "fix: resolve race condition in pipeline scheduler",
            "feat: add GitLab-compatible CI/CD YAML parser",
            "chore: configure production logging with structured output",
            "feat: implement merge request diff viewer",
            "feat: add evolutionary pipeline optimizer endpoint",
        ]
        authors = [
            ("Sarah Chen", "sarah@hiveops.io"),
            ("Alex Kim", "alex@hiveops.io"),
            ("Admin", "admin@hiveops.io"),
        ]

        for pid in range(1, 7):
            for i, msg in enumerate(commit_messages[:12]):
                author = authors[i % len(authors)]
                sha = hashlib.sha1(f"{pid}-{i}-{msg}".encode()).hexdigest()
                parent = hashlib.sha1(f"{pid}-{i-1}-prev".encode()).hexdigest() if i > 0 else ""
                ts = (now - timedelta(hours=random.randint(1, 720))).isoformat()
                conn.execute(
                    "INSERT INTO commits (project_id, sha, message, author_name, author_email, branch, parent_sha, files_changed, additions, deletions, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (pid, sha, msg, author[0], author[1], "main", parent,
                     random.randint(1, 15), random.randint(5, 200), random.randint(0, 80), ts),
                )

        sample_files = {
            "blob": [
                ("README.md", "# HiveOps Web Platform\n\nAI-Native DevOps Platform with agent swarm intelligence.\n\n## Getting Started\n\n```bash\nnpm install\nnpm run dev\n```\n\n## Architecture\n\n- **Frontend**: React 18 + TypeScript + TailwindCSS\n- **Backend**: FastAPI + PostgreSQL\n- **AI Engine**: 8-agent MACOG pipeline\n- **CI/CD**: Real Docker-based execution\n", "markdown"),
                ("src/main.ts", 'import { createApp } from "./app";\nimport { setupAuth } from "./auth";\nimport { initAgentSwarm } from "./agents";\n\nconst app = createApp();\nsetupAuth(app);\ninitAgentSwarm(app);\n\napp.listen(8080, () => {\n  console.log("HiveOps server running on :8080");\n});\n', "typescript"),
                ("src/components/Dashboard.tsx", 'import React from "react";\nimport { PipelineGraph } from "./PipelineGraph";\nimport { AgentStatus } from "./AgentStatus";\n\nexport function Dashboard() {\n  return (\n    <div className="grid grid-cols-3 gap-4">\n      <PipelineGraph />\n      <AgentStatus />\n    </div>\n  );\n}\n', "tsx"),
                ("Dockerfile", "FROM node:18-alpine AS builder\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci\nCOPY . .\nRUN npm run build\n\nFROM node:18-alpine\nWORKDIR /app\nCOPY --from=builder /app/dist ./dist\nCOPY --from=builder /app/node_modules ./node_modules\nEXPOSE 8080\nCMD [\"node\", \"dist/main.js\"]\n", "dockerfile"),
                (".hiveops-ci.yml", "stages:\n  - build\n  - test\n  - security\n  - deploy\n\nbuild:\n  stage: build\n  image: node:18-alpine\n  script:\n    - npm ci\n    - npm run build\n  artifacts:\n    paths:\n      - dist/\n\ntest:unit:\n  stage: test\n  needs: [build]\n  image: node:18-alpine\n  script:\n    - npm run test:unit\n  coverage: '/All files[^|]*\\|[^|]*\\s+([\\d\\.]+)/'\n\nsecurity:sast:\n  stage: security\n  image: hiveops/security-agent:latest\n  script:\n    - hiveops-agent scan --type sast\n\ndeploy:staging:\n  stage: deploy\n  image: hiveops/iac-agent:latest\n  environment:\n    name: staging\n  script:\n    - hiveops-agent deploy --env staging\n  only:\n    - develop\n", "yaml"),
                ("package.json", '{\n  "name": "hiveops-web-platform",\n  "version": "2.1.0",\n  "scripts": {\n    "dev": "vite",\n    "build": "tsc && vite build",\n    "test:unit": "vitest run",\n    "lint": "eslint src/"\n  },\n  "dependencies": {\n    "react": "^18.3.0",\n    "react-dom": "^18.3.0",\n    "@tanstack/react-query": "^5.0.0",\n    "reactflow": "^11.10.0"\n  }\n}\n', "json"),
                ("terraform/main.tf", 'provider "aws" {\n  region = var.aws_region\n}\n\nmodule "vpc" {\n  source  = "./modules/vpc"\n  cidr    = "10.0.0.0/16"\n  azs     = ["us-east-1a", "us-east-1b"]\n}\n\nmodule "eks" {\n  source       = "./modules/eks"\n  cluster_name = "hiveops-${var.environment}"\n  vpc_id       = module.vpc.vpc_id\n  subnet_ids   = module.vpc.private_subnets\n}\n', "hcl"),
                ("src/agents/SecurityAuditor.ts", 'import { Agent, Finding } from "./types";\n\nexport class SecurityAuditor implements Agent {\n  async review(diff: string): Promise<Finding[]> {\n    const findings: Finding[] = [];\n    if (diff.includes("password") && !diff.includes("hash")) {\n      findings.push({\n        severity: "high",\n        message: "Plain text password detected",\n        suggestion: "Use bcrypt or argon2 for password hashing",\n      });\n    }\n    return findings;\n  }\n}\n', "typescript"),
            ],
            "tree": [
                ("src", ""),
                ("src/components", ""),
                ("src/agents", ""),
                ("terraform", ""),
                ("tests", ""),
                ("docs", ""),
            ],
        }

        for pid in range(1, 7):
            sha = hashlib.sha1(f"{pid}-main".encode()).hexdigest()
            for dirname, _ in sample_files["tree"]:
                conn.execute(
                    "INSERT INTO repo_files (project_id, branch, path, name, file_type, content, language, last_commit_sha) VALUES (?,?,?,?,?,?,?,?)",
                    (pid, "main", dirname, dirname.split("/")[-1], "tree", "", "", sha),
                )
            for filename, content, lang in sample_files["blob"]:
                conn.execute(
                    "INSERT INTO repo_files (project_id, branch, path, name, file_type, content, size_bytes, language, last_commit_sha, last_commit_message) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (pid, "main", filename, filename.split("/")[-1], "blob", content, len(content), lang, sha, "feat: initial commit"),
                )

        pipeline_statuses = ["success", "success", "success", "failed", "running", "success", "pending", "success"]
        job_templates = [
            ("build", "build", "node:18-alpine", "npm ci && npm run build"),
            ("test:unit", "test", "node:18-alpine", "npm run test:unit"),
            ("test:integration", "test", "node:18-alpine", "npm run test:integration"),
            ("security:sast", "security", "hiveops/security-agent:latest", "hiveops-agent scan --type sast"),
            ("deploy:staging", "deploy", "hiveops/iac-agent:latest", "hiveops-agent deploy --env staging"),
        ]

        for pid in range(1, 4):
            for i in range(8):
                p_status = pipeline_statuses[i % len(pipeline_statuses)]
                sha = hashlib.sha1(f"{pid}-pipe-{i}".encode()).hexdigest()
                ts = (now - timedelta(hours=random.randint(1, 168))).isoformat()
                dur = random.randint(30, 600) if p_status in ("success", "failed") else 0
                conn.execute(
                    "INSERT INTO pipelines (project_id, ref, sha, status, source, duration_seconds, created_at, triggered_by) VALUES (?,?,?,?,?,?,?,?)",
                    (pid, "main", sha, p_status, "push", dur, ts, (i % 3) + 1),
                )
                pipe_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

                for j_name, j_stage, j_image, j_script in job_templates:
                    if p_status == "pending":
                        j_status = "pending"
                    elif p_status == "running":
                        j_status = "running" if j_name == "build" else "pending"
                    elif p_status == "failed" and j_name == "test:integration":
                        j_status = "failed"
                    else:
                        j_status = "success" if p_status == "success" else ("failed" if j_name == "test:integration" else "success")

                    j_dur = random.randint(5, 120) if j_status in ("success", "failed") else 0
                    log = _generate_job_log(j_name, j_status)
                    needs = json.dumps(["build"]) if j_stage != "build" else "[]"
                    conn.execute(
                        "INSERT INTO pipeline_jobs (pipeline_id, name, stage, status, image, script, duration_seconds, exit_code, log_output, needs) VALUES (?,?,?,?,?,?,?,?,?,?)",
                        (pipe_id, j_name, j_stage, j_status, j_image, j_script, j_dur,
                         0 if j_status == "success" else (1 if j_status == "failed" else -1), log, needs),
                    )

        mr_data = [
            ("feat: Add real-time pipeline streaming", "Implements WebSocket-based pipeline log streaming with auto-reconnect", "feature/streaming", "main", "open"),
            ("fix: Resolve memory leak in agent pool", "Fixed a memory leak caused by unreleased agent contexts after task completion", "fix/memory-leak", "main", "merged"),
            ("feat: Implement RBAC permission system", "Adds role-based access control with project-level permissions", "feature/rbac", "main", "open"),
            ("refactor: Extract CI runner into service", "Moves CI runner logic into a dedicated service layer for better testability", "refactor/ci-runner", "main", "merged"),
            ("feat: Add container registry scanning", "Integrates Trivy for automated container image vulnerability scanning", "feature/registry-scan", "main", "open"),
            ("security: Patch XSS in markdown renderer", "Sanitizes HTML output from markdown rendering to prevent XSS attacks", "fix/xss-patch", "main", "merged"),
        ]

        for pid in range(1, 3):
            for i, (title, desc, src, tgt, status) in enumerate(mr_data):
                iid = i + 1
                author_id = (i % 3) + 1
                ts = (now - timedelta(hours=random.randint(1, 336))).isoformat()
                merged_at = (now - timedelta(hours=random.randint(1, 48))).isoformat() if status == "merged" else ""
                conn.execute(
                    "INSERT INTO merge_requests (project_id, iid, title, description, source_branch, target_branch, status, author_id, files_changed, additions, deletions, ai_review_status, ai_review_summary, approved, created_at, merged_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (pid, iid, title, desc, src, tgt, status, author_id,
                     random.randint(2, 20), random.randint(30, 500), random.randint(5, 100),
                     "completed" if status == "merged" else "pending",
                     "AI review: No critical issues found. Code quality is good." if status == "merged" else "",
                     1 if status == "merged" else 0, ts, merged_at),
                )
                mr_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

                conn.execute(
                    "INSERT INTO mr_diffs (merge_request_id, file_path, diff_content, change_type, additions, deletions) VALUES (?,?,?,?,?,?)",
                    (mr_id, "src/services/pipeline.ts",
                     "@@ -45,6 +45,15 @@\n export class PipelineService {\n+  async streamLogs(pipelineId: string) {\n+    const ws = new WebSocket(`/ws/pipelines/${pipelineId}/logs`);\n+    ws.onmessage = (event) => {\n+      this.emit('log', JSON.parse(event.data));\n+    };\n+    ws.onerror = () => this.reconnect();\n+    return ws;\n+  }\n+\n   async execute(config: PipelineConfig) {",
                     "modified", random.randint(10, 50), random.randint(2, 15)),
                )
                conn.execute(
                    "INSERT INTO mr_diffs (merge_request_id, file_path, diff_content, change_type, additions, deletions) VALUES (?,?,?,?,?,?)",
                    (mr_id, "tests/pipeline.test.ts",
                     "@@ -1,4 +1,20 @@\n+import { PipelineService } from '../src/services/pipeline';\n+\n+describe('PipelineService', () => {\n+  it('should stream logs via WebSocket', async () => {\n+    const service = new PipelineService();\n+    const ws = await service.streamLogs('pipe-001');\n+    expect(ws).toBeDefined();\n+  });\n+});\n",
                     "added", random.randint(10, 30), 0),
                )

                if status == "merged":
                    conn.execute(
                        "INSERT INTO mr_comments (merge_request_id, author_id, body, is_ai_generated) VALUES (?,?,?,?)",
                        (mr_id, 4, "**AI Review Summary**\n\nNo critical security issues found. Code follows established patterns. Test coverage is adequate.\n\n**Suggestions:**\n- Consider adding error boundary for WebSocket reconnection\n- Add timeout configuration for long-running connections", 1),
                    )
                conn.execute(
                    "INSERT INTO mr_comments (merge_request_id, author_id, body) VALUES (?,?,?)",
                    (mr_id, 2, "Looks good! Nice implementation. Let's merge after CI passes."),
                )

        issue_data = [
            ("Pipeline fails intermittently on large repos", "The CI pipeline times out when processing repositories over 500MB. Need to investigate Docker resource limits.", "bug", "high", "in_progress"),
            ("Add support for GitLab CI YAML import", "Users should be able to import existing .gitlab-ci.yml files and convert them to .hiveops-ci.yml format", "feature", "medium", "backlog"),
            ("Container registry cleanup policy", "Implement automatic cleanup of old container images based on configurable retention policies", "feature", "medium", "todo"),
            ("Security: Rate limit API endpoints", "Add rate limiting to prevent abuse. Target: 100 req/min for authenticated, 20 for anonymous", "security", "high", "in_progress"),
            ("Improve AI code review accuracy", "The Security Auditor agent has 15% false positive rate. Need to fine-tune prompts.", "improvement", "medium", "backlog"),
            ("Dashboard loading is slow", "Dashboard takes 3+ seconds to load when there are many projects. Need to optimize queries.", "bug", "high", "todo"),
            ("Add merge request templates", "Support project-level MR description templates similar to GitLab", "feature", "low", "backlog"),
            ("POETIQ meta-layer timeout handling", "The recursive self-audit loop sometimes exceeds the 30s timeout. Need graceful degradation.", "bug", "critical", "in_progress"),
            ("Implement webhook notifications", "Add webhook support for pipeline events, MR updates, and issue changes", "feature", "medium", "todo"),
            ("Cost optimization recommendations", "The Cost Planner agent should provide actionable cost reduction suggestions", "feature", "medium", "backlog"),
        ]

        for pid in range(1, 4):
            for i, (title, desc, label, priority, col) in enumerate(issue_data):
                iid = i + 1
                author_id = (i % 3) + 1
                assignee = ((i + 1) % 3) + 1 if col == "in_progress" else None
                ts = (now - timedelta(hours=random.randint(1, 720))).isoformat()
                status = "closed" if random.random() < 0.2 else "open"
                conn.execute(
                    "INSERT INTO issues (project_id, iid, title, description, status, priority, labels, assignee_id, author_id, board_column, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (pid, iid, title, desc, status, priority, json.dumps([label]), assignee, author_id, col, ts),
                )

        image_data = [
            ("web-platform", "v2.1.0", 245000000, 12, "passed", 0),
            ("web-platform", "v2.0.9", 243000000, 12, "passed", 2),
            ("web-platform", "latest", 248000000, 13, "scanning", 0),
            ("api-gateway", "v1.5.0", 89000000, 8, "passed", 0),
            ("api-gateway", "latest", 91000000, 8, "failed", 5),
            ("ml-pipeline", "v3.0.0-rc1", 1200000000, 24, "passed", 1),
        ]
        for name, tag, size, layers, scan, vulns in image_data:
            digest = hashlib.sha256(f"{name}:{tag}".encode()).hexdigest()
            conn.execute(
                "INSERT INTO container_images (project_id, name, tag, digest, size_bytes, layers_count, scan_status, vulnerabilities_count, pushed_by) VALUES (?,?,?,?,?,?,?,?,?)",
                (1, name, tag, f"sha256:{digest}", size, layers, scan, vulns, 1),
            )

        pkg_data = [
            ("@hiveops/ui-kit", "2.1.0", "npm", 450000),
            ("@hiveops/agent-sdk", "1.3.0", "npm", 230000),
            ("hiveops-client", "0.9.0", "pypi", 180000),
            ("hiveops-terraform-provider", "1.0.0", "generic", 15000000),
        ]
        for name, ver, ptype, size in pkg_data:
            conn.execute(
                "INSERT INTO packages (project_id, name, version, package_type, size_bytes, downloads, published_by) VALUES (?,?,?,?,?,?,?)",
                (1, name, ver, ptype, size, random.randint(50, 5000), 1),
            )

        for pid in range(1, 4):
            for env_name, url, status in [("production", "https://app.hiveops.io", "available"), ("staging", "https://staging.hiveops.io", "available"), ("development", "https://dev.hiveops.io", "stopped")]:
                conn.execute(
                    "INSERT INTO environments (project_id, name, url, status) VALUES (?,?,?,?)",
                    (pid, env_name, url, status),
                )

        agent_types = [
            ("architect", "iac_generation", "completed", 0.92, 2340),
            ("harmonizer", "provider_validation", "completed", 0.88, 1560),
            ("engineer", "code_generation", "completed", 0.95, 4200),
            ("security_prover", "vulnerability_scan", "running", 0.0, 0),
            ("cost_planner", "cost_analysis", "completed", 0.87, 890),
            ("devops_auditor", "code_review", "completed", 0.91, 3100),
            ("sre_investigator", "incident_triage", "completed", 0.89, 1800),
            ("evolution_optimizer", "pipeline_optimization", "running", 0.0, 0),
        ]
        for agent, task, status, conf, dur in agent_types:
            conn.execute(
                "INSERT INTO agent_tasks (project_id, agent_type, task_type, status, confidence, duration_ms, input_data, output_data) VALUES (?,?,?,?,?,?,?,?)",
                (1, agent, task, status, conf, dur, "{}", "{}"),
            )


def _generate_job_log(job_name: str, status: str) -> str:
    logs = {
        "build": "$ npm ci\nadded 1247 packages in 12.4s\n$ npm run build\nvite v5.2.0 building for production...\n✓ 847 modules transformed.\ndist/index.html     1.23 kB │ gzip: 0.65 kB\ndist/assets/index-DkB3x2.js  245.67 kB │ gzip: 78.12 kB\n✓ built in 4.21s\nJob succeeded",
        "test:unit": "$ npm run test:unit\n\n RUN  v1.4.0\n\n ✓ src/components/Dashboard.test.tsx (3 tests) 45ms\n ✓ src/services/pipeline.test.ts (5 tests) 89ms\n ✓ src/agents/SecurityAuditor.test.ts (4 tests) 67ms\n\n Test Files  3 passed (3)\n      Tests  12 passed (12)\n   Start at  14:23:01\n   Duration  1.24s\n\nJob succeeded",
        "test:integration": "$ npm run test:integration\n\nConnecting to test database...\nRunning migrations...\n\n ✓ API: auth flow (2 tests) 234ms\n ✓ API: pipeline CRUD (4 tests) 567ms\n ✗ API: merge request creation (1 test) 1203ms\n   → Expected status 201, received 500\n   → Error: Database constraint violation\n\n Test Files  2 passed, 1 failed (3)\n      Tests  6 passed, 1 failed (7)\n\nJob failed" if status == "failed" else "$ npm run test:integration\n\n ✓ All 7 tests passed\n\nJob succeeded",
        "security:sast": "$ hiveops-agent scan --type sast\n\nScanning 847 files...\nAnalyzing JavaScript/TypeScript patterns...\n\nFindings:\n  INFO: No critical vulnerabilities detected\n  WARN: 2 low-severity issues found\n    - src/utils/parse.ts:45 - Potential prototype pollution\n    - src/config.ts:12 - Hardcoded default timeout\n\nScan completed: PASS\nJob succeeded",
        "deploy:staging": "$ hiveops-agent deploy --env staging\n\nGenerating deployment manifest...\nApplying to EKS cluster hiveops-staging...\nDeployment web-platform updated (3 replicas)\nService web-platform-svc configured\nIngress staging.hiveops.io ready\n\n✓ Deployment successful\nURL: https://staging.hiveops.io\nJob succeeded",
    }
    return logs.get(job_name, f"$ echo 'Running {job_name}'\nJob {'succeeded' if status == 'success' else 'failed'}")
