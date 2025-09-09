# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Autonomous Dify.ai Deployment with Vertex AI Integration**

This project implements a complete Dify.ai deployment on Google Cloud Platform with Hebrew language support and Vertex AI integration. The system combines automated deployment, browser testing, and AI orchestration.

Key components:
- **Dify Platform**: Full Dify.ai source with Hebrew RTL support
- **Vertex AI Integration**: Complete Google Cloud Vertex AI provider with Hebrew-optimized Gemini models
- **Multi-Agent Orchestrator**: LangGraph-based system with 4 specialized agents
- **Browser Automation**: Playwright-based testing with Hebrew locale configuration
- **Visual Progress Tracking**: HTML dashboard with RTL Hebrew layout

## Development Commands

### Container Development (Docker)

```bash
# Automated startup with Hebrew/Vertex AI support
./start-dev.sh                               # Start core services (DB + Redis)

# Manual service management  
docker compose -f docker-compose.dev.yaml up -d db redis    # Core only
docker compose -f docker-compose.dev.yaml up -d             # All services

# Service-specific startup
docker compose -f docker-compose.dev.yaml up -d api         # API server
docker compose -f docker-compose.dev.yaml up -d worker      # Background worker  
docker compose -f docker-compose.dev.yaml up -d web         # Frontend

# Health checks
curl http://localhost:3000                   # Web interface
curl http://localhost:5001/health           # API health
```

### Browser Automation & Testing

```bash
# Hebrew-configured browser automation
npm run browser                              # Launch persistent Hebrew browser
npm run open-dify                           # Alternative browser launcher
npm run setup                               # Install Playwright browsers

# Testing suite
npm test                                     # Run all Playwright tests
npm run test:ui                             # Interactive test runner
npm run test:debug                          # Debug mode with breakpoints
```

### Vertex AI Integration Testing

```bash
# Validate Vertex AI integration structure
python validate_implementation.py

# Test Vertex AI Hebrew capabilities (requires GCP credentials)
python test_vertex_ai.py

# Quick integration test without API calls
python test_integration_structure.py

# Hebrew conversation test with Vertex AI
python quick_test_vertex_ai.py
```

### Multi-Agent Orchestrator

```bash
# Setup virtual environment
python3 -m venv agents_env
source agents_env/bin/activate
pip install langgraph langchain langchain-anthropic

# Run orchestrator with API key
export ANTHROPIC_API_KEY='your-anthropic-api-key'
python3 agents_orchestrator.py
```

## Architecture Understanding

### Vertex AI Integration Layer
The project includes a complete Vertex AI integration with three main components:

1. **vertex_ai_provider.py**: Core Vertex AI provider with Hebrew text detection and RTL optimization
2. **dify_vertex_ai_integration.py**: Dify compatibility layer that bridges Vertex AI with Dify's model provider architecture
3. **Automated Hebrew Enhancement**: Detects Hebrew text (Unicode \u0590-\u05FF) and automatically enhances prompts with Hebrew-specific instructions

### Multi-Agent System Architecture
- **State Management**: Shared TypedDict maintaining conversation context across agents
- **Agent Roles**: Planner (strategy), Researcher (analysis), Coder (implementation), Reviewer (validation)
- **LangGraph Workflow**: Conditional routing based on task complexity and agent expertise
- **Hebrew Context**: All agents understand Hebrew requirements and RTL layout principles

### Browser Automation Framework
- **Persistent Sessions**: Maintains state between test runs using Playwright's browser server
- **Hebrew Locale**: Automatic he-IL configuration with RTL layout testing
- **Visual Tracking**: Updates `project-tracker.html` with Hebrew progress indicators
- **Dify Integration**: Automated navigation and setup of Dify admin interface

## Critical Configuration Files

### Docker Environment (`docker-compose.dev.yaml`)
Contains Hebrew-optimized environment variables:
```yaml
LANG: he_IL.UTF-8
LC_ALL: he_IL.UTF-8
GOOGLE_VERTEX_PROJECT: lionspace
GOOGLE_VERTEX_LOCATION: us-east1
```

### Browser Configuration (`playwright.config.js`)
Hebrew locale settings:
```javascript
locale: 'he-IL'
timezoneId: 'Asia/Jerusalem' 
```

### Progress Tracking (`project-tracker.html`)
RTL Hebrew dashboard with:
- Visual timeline with completion status
- Hebrew task descriptions
- Color-coded progress indicators
- Statistics tracking

## Development Workflow Requirements

### Mandatory Updates
- **Always update `project-tracker.html`** after completing tasks
- **Use Hebrew language** for all progress descriptions and documentation
- **Test RTL layout** for any UI changes
- **Validate Hebrew text processing** in Vertex AI responses

### Browser Management Protocol
- **NEVER use `open` command** - always use `npm run browser` 
- **Persistent browser sessions** - browser maintains state across runs
- **Hebrew configuration** - automatic RTL and he-IL locale applied
- **State preservation** - login sessions and navigation state maintained

### Testing Requirements
- **Structure validation**: Run `python test_integration_structure.py` before commits
- **Hebrew text testing**: Verify Hebrew input/output in all components  
- **Vertex AI validation**: Test Hebrew enhancement with `python quick_test_vertex_ai.py`
- **Browser automation**: All changes must pass Playwright Hebrew locale tests

## Vertex AI Hebrew Features

### Automatic Hebrew Detection
The integration automatically detects Hebrew text using Unicode ranges and enhances prompts:

```python
# Input: "מה זה Dify.ai?"
# Enhanced prompt includes:
"""אנא השב בעברית בצורה ברורה ומדויקת. 
שים לב לכיווניות הטקסט (RTL) ולתקינות הדקדוק העברי.

מה זה Dify.ai?"""
```

### Supported Models
- **gemini-pro**: Advanced reasoning with Hebrew optimization
- **gemini-flash**: Fast responses with Hebrew RTL support

### Configuration Options
All model parameters support Hebrew context:
- Temperature control for Hebrew coherence
- Token limits optimized for Hebrew text length
- Safety settings adapted for Hebrew content

## Security and Credentials

### Environment Variables Required
```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_VERTEX_PROJECT=your-gcp-project-id  
GOOGLE_VERTEX_LOCATION=us-east1
ANTHROPIC_API_KEY=your-anthropic-key
```

### GCP Service Account Permissions
Required roles for Vertex AI integration:
- `roles/aiplatform.user` - Vertex AI access
- `roles/storage.objectViewer` - Model access  
- `roles/serviceusage.serviceUsageConsumer` - API usage

## File Organization

### Core Integration Files
- `vertex_ai_provider.py` - Core Vertex AI provider with Hebrew support
- `dify_vertex_ai_integration.py` - Dify compatibility layer
- `agents_orchestrator.py` - Multi-agent coordination system

### Testing and Validation
- `test_vertex_ai.py` - Comprehensive Vertex AI tests
- `validate_implementation.py` - Code structure validation
- `quick_test_vertex_ai.py` - Hebrew conversation testing

### Browser Automation
- `open-dify.js` - Hebrew-configured browser launcher
- `test-browser.js` - Comprehensive browser testing suite
- `complete-setup.js` - Automated Dify admin setup

### Documentation
- `VERTEX_AI_SETUP.md` - Complete Vertex AI setup guide
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- `project-tracker.html` - Visual Hebrew progress dashboard

This project represents a complete autonomous deployment system with advanced Hebrew language support and production-ready Vertex AI integration.