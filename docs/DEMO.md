# HiveOps Demo & Screenshot Guide

If a chat artifact screenshot link expires or shows `not found`, use this repeatable demo flow.

## Run the platform

```bash
uvicorn hiveops.api:app --host 0.0.0.0 --port 8000
```

Then open:
- `http://127.0.0.1:8000/` (dashboard)
- `http://127.0.0.1:8000/docs` (interactive API)
- `http://127.0.0.1:8000/platform/screenshot` (stable built-in snapshot image)

## Verify core endpoints

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/platform/roadmap
curl -s http://127.0.0.1:8000/platform/plan/alignment
curl -s -X POST http://127.0.0.1:8000/incidents/triage \
  -H 'content-type: application/json' \
  -d '{"incident_id":"INC-2026","service":"checkout-api","symptom":"latency spike after deploy","severity":"high","environment":"prod"}'
```

## Why screenshots can fail in chat

Browser artifact links are environment-scoped and can expire between runs. If one breaks,
regenerate a screenshot from a fresh running server.


## Stable screenshot endpoint

Use `/platform/screenshot` when artifact links in chat expire. It is served directly by the app and does not depend on temporary artifact storage.
