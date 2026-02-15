import sqlite3
import os
import json
from datetime import datetime, timezone
from contextlib import contextmanager

DB_PATH = os.environ.get("HIVEOPS_DB_PATH", "/data/app.db" if os.path.isdir("/data") else "hiveops.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL DEFAULT '',
            password_hash TEXT NOT NULL,
            avatar_url TEXT DEFAULT '',
            role TEXT DEFAULT 'developer',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            namespace TEXT NOT NULL,
            description TEXT DEFAULT '',
            visibility TEXT DEFAULT 'private',
            default_branch TEXT DEFAULT 'main',
            avatar_url TEXT DEFAULT '',
            stars_count INTEGER DEFAULT 0,
            forks_count INTEGER DEFAULT 0,
            owner_id INTEGER REFERENCES users(id),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(namespace, name)
        );

        CREATE TABLE IF NOT EXISTS repositories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER UNIQUE REFERENCES projects(id),
            disk_path TEXT NOT NULL,
            size_bytes INTEGER DEFAULT 0,
            last_activity_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            name TEXT NOT NULL,
            commit_sha TEXT NOT NULL,
            is_protected INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(project_id, name)
        );

        CREATE TABLE IF NOT EXISTS commits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            sha TEXT NOT NULL,
            message TEXT NOT NULL,
            author_name TEXT NOT NULL,
            author_email TEXT NOT NULL,
            branch TEXT DEFAULT 'main',
            parent_sha TEXT DEFAULT '',
            files_changed INTEGER DEFAULT 0,
            additions INTEGER DEFAULT 0,
            deletions INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(project_id, sha)
        );

        CREATE TABLE IF NOT EXISTS repo_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            branch TEXT DEFAULT 'main',
            path TEXT NOT NULL,
            name TEXT NOT NULL,
            file_type TEXT DEFAULT 'blob',
            content TEXT DEFAULT '',
            size_bytes INTEGER DEFAULT 0,
            language TEXT DEFAULT '',
            last_commit_sha TEXT DEFAULT '',
            last_commit_message TEXT DEFAULT '',
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS pipelines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            ref TEXT NOT NULL DEFAULT 'main',
            sha TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            source TEXT DEFAULT 'push',
            config_yaml TEXT DEFAULT '',
            duration_seconds INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            started_at TEXT DEFAULT '',
            finished_at TEXT DEFAULT '',
            triggered_by INTEGER REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS pipeline_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pipeline_id INTEGER REFERENCES pipelines(id),
            name TEXT NOT NULL,
            stage TEXT NOT NULL DEFAULT 'build',
            status TEXT DEFAULT 'pending',
            image TEXT DEFAULT 'node:18-alpine',
            script TEXT DEFAULT '',
            duration_seconds INTEGER DEFAULT 0,
            exit_code INTEGER DEFAULT -1,
            log_output TEXT DEFAULT '',
            artifacts_path TEXT DEFAULT '',
            allow_failure INTEGER DEFAULT 0,
            needs TEXT DEFAULT '[]',
            started_at TEXT DEFAULT '',
            finished_at TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS merge_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            iid INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            source_branch TEXT NOT NULL,
            target_branch TEXT NOT NULL DEFAULT 'main',
            status TEXT DEFAULT 'open',
            author_id INTEGER REFERENCES users(id),
            assignee_id INTEGER REFERENCES users(id),
            pipeline_id INTEGER REFERENCES pipelines(id),
            merge_commit_sha TEXT DEFAULT '',
            files_changed INTEGER DEFAULT 0,
            additions INTEGER DEFAULT 0,
            deletions INTEGER DEFAULT 0,
            ai_review_status TEXT DEFAULT 'pending',
            ai_review_summary TEXT DEFAULT '',
            approved INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            merged_at TEXT DEFAULT '',
            UNIQUE(project_id, iid)
        );

        CREATE TABLE IF NOT EXISTS mr_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merge_request_id INTEGER REFERENCES merge_requests(id),
            author_id INTEGER REFERENCES users(id),
            body TEXT NOT NULL,
            file_path TEXT DEFAULT '',
            line_number INTEGER DEFAULT 0,
            is_ai_generated INTEGER DEFAULT 0,
            is_resolved INTEGER DEFAULT 0,
            parent_id INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS mr_diffs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merge_request_id INTEGER REFERENCES merge_requests(id),
            file_path TEXT NOT NULL,
            old_path TEXT DEFAULT '',
            diff_content TEXT DEFAULT '',
            change_type TEXT DEFAULT 'modified',
            additions INTEGER DEFAULT 0,
            deletions INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            iid INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'open',
            priority TEXT DEFAULT 'medium',
            labels TEXT DEFAULT '[]',
            assignee_id INTEGER REFERENCES users(id),
            author_id INTEGER REFERENCES users(id),
            milestone TEXT DEFAULT '',
            due_date TEXT DEFAULT '',
            time_estimate INTEGER DEFAULT 0,
            time_spent INTEGER DEFAULT 0,
            board_column TEXT DEFAULT 'backlog',
            ai_triage_status TEXT DEFAULT '',
            ai_triage_summary TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            closed_at TEXT DEFAULT '',
            UNIQUE(project_id, iid)
        );

        CREATE TABLE IF NOT EXISTS issue_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id INTEGER REFERENCES issues(id),
            author_id INTEGER REFERENCES users(id),
            body TEXT NOT NULL,
            is_ai_generated INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS container_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            name TEXT NOT NULL,
            tag TEXT NOT NULL DEFAULT 'latest',
            digest TEXT DEFAULT '',
            size_bytes INTEGER DEFAULT 0,
            layers_count INTEGER DEFAULT 0,
            scan_status TEXT DEFAULT 'pending',
            vulnerabilities_count INTEGER DEFAULT 0,
            pushed_by INTEGER REFERENCES users(id),
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            package_type TEXT NOT NULL DEFAULT 'npm',
            size_bytes INTEGER DEFAULT 0,
            downloads INTEGER DEFAULT 0,
            published_by INTEGER REFERENCES users(id),
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS environments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            name TEXT NOT NULL,
            url TEXT DEFAULT '',
            status TEXT DEFAULT 'available',
            last_deployment_at TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS agent_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            agent_type TEXT NOT NULL,
            task_type TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            input_data TEXT DEFAULT '{}',
            output_data TEXT DEFAULT '{}',
            confidence REAL DEFAULT 0.0,
            duration_ms INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            completed_at TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            action TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            resource_id INTEGER DEFAULT 0,
            details TEXT DEFAULT '{}',
            ip_address TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """)
