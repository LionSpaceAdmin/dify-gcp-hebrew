# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Autonomous Dify.ai Deployment on Google Cloud Platform**

This project deploys Dify.ai (an open-source LLM application platform) on Google Cloud Platform with:
- Vertex AI integration (Gemini models)
- Hebrew language support with RTL layout
- Autonomous deployment pipeline
- Multi-agent orchestration system
- Persistent browser automation

The repository contains multiple deployment approaches:
- `dify-gcp-deployment/`: Docker-based deployment with Playwright automation
- `dify-direct/`: Direct macOS installation with uv package management
- Multi-agent orchestrator system with LangGraph

## Architecture

### Core Components
1. **Dify Backend API** (`dify-direct/api/`): Python Flask application with Domain-Driven Design
2. **Dify Frontend** (`dify-direct/web/`): Next.js 15 with TypeScript and React 19
3. **Multi-Agent Orchestrator** (`agents_orchestrator.py`): LangGraph-based coordination system
4. **Project Tracker** (`project-tracker.html`): Hebrew RTL progress tracking interface

### GCP Integration
- **Vertex AI**: Primary LLM provider (Gemini models)
- **Cloud Run**: Container deployment target
- **Cloud SQL**: PostgreSQL with pgvector for embeddings
- **Secret Manager**: Credential management
- **Cloud Storage**: File and document storage

## Development Commands

### Dify Backend (Direct Installation)

All Python commands use `uv` package manager:

```bash
# Start development servers
cd dify-direct/api
uv run --project . flask run --port 5001    # Start API server
uv run --project . celery -A app.celery worker --loglevel=info  # Start worker

# Database operations
uv run --project . flask db upgrade         # Run migrations
uv run --project . flask db migrate         # Create migration

# Testing
uv run --project . pytest                   # Run all tests
uv run --project . pytest tests/unit_tests/ # Unit tests only

# Code quality
uv run --project . ruff check --fix ./      # Fix linting issues
uv run --project . ruff format ./           # Format code
```

### Dify Frontend

```bash
cd dify-direct/web
pnpm install                # Install dependencies
pnpm dev                    # Start development server
pnpm build                  # Production build
pnpm test                   # Run tests
```

### Multi-Agent Orchestrator

```bash
# Activate virtual environment
source agents_env/bin/activate

# Set API key
export ANTHROPIC_API_KEY='your-key-here'

# Run orchestrator
python3 agents_orchestrator.py
```

### GCP Deployment

```bash
# Set up GCP authentication
gcloud auth login
gcloud config set project lionspace

# Deploy to Cloud Run
gcloud run deploy dify-api --source=dify-direct/api --region=us-east1
gcloud run deploy dify-web --source=dify-direct/web --region=us-east1
```

## MCP Server Configuration

The project uses Model Context Protocol (MCP) servers configured in `.mcp.json`:

### Persistent Browser Automation
- **Puppeteer MCP Server**: Provides persistent browser automation
- **Configuration**: `.claude/browser-config.json` with Dify credentials
- **User Data**: Persistent browser profile in `.claude/browser-data/`

### GCP Tools Integration
- **Google Cloud MCP Server**: Provides GCP service integration
- **Service Account**: `.claude/gcp-service-account.json`
- **Configuration**: `.claude/gcp-config.json` with project settings

## Important Notes

### Development Workflow
- **Language**: Work primarily in Hebrew (עברית)
- **Approach**: One step at a time, avoid assumptions
- **Progress Tracking**: Update `project-tracker.html` after each task
- **Browser Management**: Never use `open` command; use persistent MCP browser only

### Database Setup
- **Local PostgreSQL**: Running on default port with `dify` database
- **Admin Account**: `admin@dify.local` / `LionSpace2024!`
- **Vertex AI**: Pre-configured with 3 models (gemini-1.5-pro, gemini-1.5-flash, text-embedding-004)

### Testing Guidelines
- Use `pytest` for Python backend testing
- Use `pnpm test` for frontend testing
- Automated browser testing via MCP Puppeteer server
- Always test Vertex AI integration after changes

### Code Style
- **Python**: Use `uv` package manager, type hints required, follow Domain-Driven Design
- **TypeScript**: Strict configuration, avoid `any` type
- **Internationalization**: Hebrew RTL support with proper locale handling

### Deployment Pipeline
Current status: 12/16 tasks completed
- ✅ Local Dify installation with Vertex AI
- ✅ Persistent browser automation setup
- ⏳ Full functionality testing with Vertex AI
- 🔄 Next: GCP secrets management and cloud deployment

## Project-Specific Conventions

- All async tasks use Celery with Redis as broker
- Vector databases use pgvector extension for PostgreSQL
- Model providers managed through Dify's provider system
- Hebrew language support throughout the interface
- Autonomous deployment with minimal manual intervention