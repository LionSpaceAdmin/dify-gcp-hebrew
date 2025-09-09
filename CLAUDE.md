# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Autonomous Dify.ai Deployment on Google Cloud Platform**

This project deploys Dify.ai (an open-source LLM application platform) on Google Cloud Platform with Hebrew language support and Vertex AI integration. It combines:

- **Primary Goal**: Full production deployment of Dify.ai on GCP with Hebrew RTL support
- **Multi-Agent System**: LangGraph-based orchestrator with 4 specialized agents (Planner, Researcher, Coder, Reviewer)
- **Deployment Approaches**: Both Docker-based containerization and direct macOS installation
- **Automation**: Playwright browser automation with persistent Hebrew-configured sessions
- **Progress Tracking**: HTML-based visual tracking system with RTL Hebrew layout

## Architecture

The project employs a multi-layered architecture:

### Core Components
1. **Dify Platform** (`dify/` directory): Full Dify.ai source code
   - Backend API: Python Flask with Domain-Driven Design
   - Frontend Web: Next.js with TypeScript and Hebrew i18n
   - Database: PostgreSQL with pgvector extension for embeddings
   - Cache/Queue: Redis for session management and background jobs

2. **Multi-Agent Orchestrator** (`agents_orchestrator.py`): 
   - LangGraph-based workflow coordination
   - 4 specialized agents with shared state management
   - Anthropic Claude integration for decision making

3. **Deployment Infrastructure**:
   - Docker Compose with Hebrew database collation
   - GCP deployment configurations (Cloud Run, Cloud SQL, Secret Manager)
   - Terraform infrastructure as code (planned)

4. **Testing & Automation**:
   - Playwright configuration with Hebrew locale (he-IL)
   - Persistent browser sessions with automatic Dify navigation
   - Visual progress tracking with timeline interface

### GCP Integration Strategy
- **Vertex AI**: Primary LLM provider (Gemini Pro/Flash models)
- **Cloud Run**: Multi-service container deployment
- **Cloud SQL**: Managed PostgreSQL with pgvector
- **Cloud Storage**: Document and file management
- **Secret Manager**: Secure credential storage
- **Cloud Armor**: WAF protection

## Development Commands

### Docker-Based Development

```bash
# Start core infrastructure
./start-dev.sh                              # Automated setup script

# Manual service management
docker-compose -f docker-compose.dev.yaml up -d db redis  # Core services
docker-compose -f docker-compose.dev.yaml up -d           # All services

# Health checks
curl http://localhost                        # Web interface
curl http://localhost:5001/health           # API health
```

### Browser Automation

```bash
# Persistent browser with Hebrew configuration
npm run browser                              # Primary browser command
npm run setup                                # Install Playwright browsers

# Testing
npm test                                     # Run all Playwright tests
npm run test:ui                              # Interactive test runner
npm run test:debug                           # Debug mode
```

### Multi-Agent Orchestrator

```bash
# Setup virtual environment
python3 -m venv agents_env
source agents_env/bin/activate
pip install langgraph langchain langchain-anthropic

# Set API key and run
export ANTHROPIC_API_KEY='your-key'
python3 agents_orchestrator.py
```

### GCP Deployment (Planned)

```bash
# Authentication and project setup
gcloud auth login
gcloud config set project lionspace

# Build and deploy (using Cloud Build)
gcloud builds submit --config cloudbuild-api.yaml
```

## Critical Development Guidelines

### Browser Management
- **NEVER use `open` command** - always use `npm run browser`
- **Persistent sessions**: Browser maintains state between runs
- **Hebrew configuration**: Automatic RTL layout and he-IL locale
- **Automation scripts**: Located in root directory (open-dify.js, test-browser.js, etc.)

### Progress Tracking
- **Mandatory updates**: Always update `project-tracker.html` after tasks
- **Visual timeline**: Shows completed/in-progress/pending tasks
- **RTL Hebrew**: All tracking in Hebrew with proper text direction
- **Status indicators**: Color-coded progress with completion statistics

### Code Architecture

#### Multi-Agent System
- **State Management**: Shared TypedDict with context preservation
- **Agent Specialization**: Each agent has distinct responsibilities
- **LangGraph Integration**: Workflow orchestration with conditional routing
- **Claude Integration**: Using Claude Sonnet for reasoning tasks

#### Deployment Configuration
- **Hebrew Database**: Custom collation support for RTL text
- **Environment Separation**: Development vs production configurations  
- **Security First**: All credentials via Secret Manager
- **Scalable Design**: Cloud Run auto-scaling with Cloud SQL connection pooling

## File Structure Understanding

### Root Level Files
- `agents_orchestrator.py`: Main multi-agent system
- `project-tracker.html`: Visual progress tracking (Hebrew RTL)
- `start-dev.sh`: Automated development environment setup
- `docker-compose.dev.yaml`: Development container configuration
- `playwright.config.js`: Browser automation configuration (Hebrew locale)

### Key Directories
- `dify/`: Full Dify.ai platform source code
- `scripts/`: Database initialization and automation scripts
- `docs/`: Architecture documentation and deployment guides
- `screenshots/`: Visual documentation of setup process
- `configs/`: Configuration files for various services

### Browser Automation Scripts
- `open-dify.js`: Main browser launcher with Hebrew configuration
- `test-browser.js`: Comprehensive testing suite
- `complete-setup.js`: Automated Dify initial setup
- `install-dify.js`: Installation verification scripts

## Project-Specific Conventions

### Language and Localization
- **Primary Language**: Hebrew (עברית) for all documentation and UI
- **RTL Support**: Proper right-to-left layout throughout
- **Timezone**: Asia/Jerusalem for all date/time operations
- **Character Encoding**: UTF-8 with Hebrew font family preferences

### Database Configuration
- **PostgreSQL**: Version 15+ with pgvector extension
- **Hebrew Collation**: Proper sorting and comparison for Hebrew text
- **Connection Pooling**: Optimized for Cloud SQL integration
- **Migration Strategy**: Version-controlled schema updates

### Development Workflow
- **One Step at a Time**: Incremental development approach
- **Visual Feedback**: HTML progress tracker must be updated
- **Automation First**: Prefer automated solutions over manual processes
- **Testing Required**: All changes must include browser automation tests

### Security Considerations
- **No Hardcoded Secrets**: All credentials via environment variables
- **Secure Defaults**: Production-ready security configurations
- **Access Control**: RBAC implementation with proper role separation
- **Audit Trail**: Comprehensive logging for security monitoring

This project represents a comprehensive autonomous deployment system with strong Hebrew language support and modern cloud-native architecture.