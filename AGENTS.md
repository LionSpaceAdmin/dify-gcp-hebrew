# Repository Guidelines

## Project Structure & Modules
- `dify-gcp-updated/` – main workspace: Playwright tests, Python integrations (e.g., `vertex_ai_provider.py`, `agents_orchestrator.py`), Docker Compose, Nginx, docs.
- `dify-gcp-deployment/` – deployment templates (Dockerfiles, Cloud Build, docs).
- `dify-direct/` – web console (Next.js/React, TypeScript) under `web/app/...`.
- Root utilities – orchestration scripts and configs (`*.json`). Keep secrets out of VCS.

## Build, Test, and Development
- Node/Playwright (`dify-gcp-updated/`): `npm ci`, `npm run setup`, `npm test`, `node open-dify.js`.
- Docker (dev stack): `docker compose -f dify-gcp-updated/docker-compose.dev.yaml up --build` (DB, Redis, API, Web, Nginx).
- Python: use venv; run `pytest` where tests exist.

## Coding Style & Naming
- Python: 4 spaces, type hints, `snake_case` for modules/functions.
- JS/TS/React: 2 spaces, `camelCase` vars, `PascalCase` components (e.g., `HumanInTheLoopChat.jsx`).
- Directories: kebab-case; co-locate small parts in `components/`. Keep changes minimal and scoped.

## Testing Guidelines
- Playwright: `*.spec.(ts|js)` near helpers; prefer deterministic tests.
- Python: `test_*.py` with `pytest`. Cover Vertex AI provider, orchestrator, HITL flows.

## Commit & PR Guidelines
- Conventional Commits: `feat(api): add vertex routing`, `fix(web): rtl layout`.
- PRs: description, linked issue, test notes, UI screenshots if relevant, ENV/config changes.
- Prefer small PRs; separate refactors from behavior changes.

## Security & Configuration
- Never commit secrets (e.g., `gh_pat.txt`, API keys). Use env vars or mounts.
- Document required env vars in PRs with safe examples; sanitize logs.
- HITL API key (optional): set `HITL_API_KEY` to require `x-api-key` on `/api/chat-hitl` and `/api/human-intervention`.
 - Webhook token (optional): set `HITL_WEBHOOK_TOKEN` to require `x-webhook-token` on `/api/hitl-webhook`.

## HITL Testing (Next.js)
- Start web: `cd dify-direct/web && pnpm i && pnpm dev` (env: `GOOGLE_VERTEX_PROJECT`, `GOOGLE_VERTEX_LOCATION`).
- API tests: `cd dify-gcp-updated && HITL_BASE=http://localhost:3000 npm test` (runs Playwright, includes HITL API/UI specs).
- Auth tests: set `HITL_EXPECT_AUTH=1 HITL_API_KEY=...` before `npm test` to verify 401 without key.

## Webhook Integration
- Endpoint: `POST /api/hitl-webhook` (Next.js). Optional header: `x-webhook-token`.
- Quick setup: `export HITL_WEBHOOK_URL=http://localhost:3000/api/hitl-webhook` then run `python3 dify-gcp-updated/human_in_the_loop/setup_hitl_webhook.py`.

## Deploy Notes
- Next.js app (web): `cd dify-direct/web && docker build -t your-registry/dify-web:latest .` then run on Cloud Run/Kubernetes with env: `GOOGLE_VERTEX_PROJECT`, `GOOGLE_VERTEX_LOCATION`, optional `HITL_API_KEY`, `HITL_WEBHOOK_TOKEN`.
- Dify services: use existing Dockerfiles (`dify-gcp-updated/Dockerfile.api`, `Dockerfile.web`) or the dev compose as a reference.
- Cloud Run via Cloud Build: `gcloud builds submit --config=dify-direct/web/cloudbuild-web.yaml --project $PROJECT_ID --substitutions=_SERVICE_NAME=dify-web-hitl,_REGION=us-east1,_REPOSITORY=web` (ensure Artifact Registry repo exists).
- Cloud Run direct: `cp dify-direct/web/.env.deploy.example dify-direct/web/.env.deploy`, fill values, then run `bash dify-direct/web/scripts/deploy-cloud-run-web.sh`.

## Agent-Specific Instructions (HITL)
- Primary task file: `dify-gcp-updated/HUMAN_IN_THE_LOOP_TASK.md` (Human-in-the-Loop plan).
- Environment: export `GOOGLE_VERTEX_PROJECT`, `GOOGLE_VERTEX_LOCATION`, optional `OPENAI_API_KEY`; for Anthropic tools, `ANTHROPIC_API_KEY`.
- Bring up dev stack: see Docker command above; then `npm run setup` and `npm test` under `dify-gcp-updated/`.
- Implementation targets: extend `dify-gcp-updated/vertex_ai_provider.py`; complete `human_in_the_loop/{api,components,tests}` as outlined in the task file.
- Orchestrator: optional local run `python3 agents_orchestrator.py` (activate venv if needed) for multi-agent workflows.
