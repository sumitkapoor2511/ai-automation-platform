# AI-Native Full-Stack & Autonomous Agent Platform

An enterprise-grade automation ecosystem built with **FastAPI**, **PostgreSQL**, **n8n AI Agents (Google Gemini)**, and **Nginx Reverse Proxy**, orchestrated via **Docker Compose**.

## System Architecture

```text
+-------------------+       HTTPS / HTTP (Port 80)       +------------------------+
|  SwiftUI iOS App  | ---------------------------------> |  Nginx Reverse Proxy   |
| (Command Center)  |                                    |     (nginx:alpine)     |
+-------------------+                                    +------------------------+
                                                              |              |
                                 /api/v1/*                    |              |  /webhook/*
                     +----------------------------------------+              +--------------------+
                     v                                                                            v
+----------------------------------------+                                    +------------------------------------+
|           FastAPI Gateway              | <---- HTTP Tool Calling (CRUD) --- |       n8n Agent Orchestrator       |
|   (Python + SQLModel + OAuth2 JWT)     |                                    |  (Google Gemini + Window Memory)   |
+----------------------------------------+                                    +------------------------------------+
                     |
                     | Async SQL / ORM
                     v
+----------------------------------------+
|          PostgreSQL Database           |
|         (postgres:16-alpine)           |
+----------------------------------------+
```

### Core Components
* **Gateway (`nginx:alpine`):** Routes `/api/*` traffic to FastAPI and `/webhook/*` requests to n8n on Port 80.
* **API Core (`FastAPI + SQLModel`):** Asynchronous REST API with OAuth2 JWT Bearer authentication, OpenAPI/Swagger docs, and Pydantic v2 schema validation.
* **Persistence (`postgres:16-alpine`):** Relational storage for authenticated users and automation task queues (`RAG_Search` and `Data_Extraction`).
* **Agentic Orchestrator (`n8n` + Google Gemini):** Stateful webhook-driven AI agent utilizing window buffer session memory (`sessionId`) and dynamic HTTP tool-calling into FastAPI.

## Autonomous Agent Capabilities (Full CRUD)

The n8n and Google Gemini agent manages database tasks safely through multi-turn validation and chained tool execution:

* **Create (`POST /api/v1/tasks`):** Validates required fields (`agent_type`, `title`, `priority`) via conversational follow-ups before writing to PostgreSQL.
* **Read (`GET /api/v1/tasks`):** Queries, filters, counts, and summarizes queued tasks in real time.
* **Update (`PATCH /api/v1/tasks/{task_id}`):** Chains `list_tasks` with `update_task` to resolve task IDs by name and update task status or priority.
* **Delete (`DELETE /api/v1/tasks/{task_id}`):** Looks up exact task IDs before safely removing records from PostgreSQL.

## Repository Structure

```text
ai-automation-platform/
├── app/                   # FastAPI application, models, routers, and JWT auth
├── n8n_workflows/         # Exported n8n AI Agent workflow JSON (full CRUD tools)
├── nginx/                 # Nginx reverse proxy routing configuration
├── .env.example           # Environment variables template
├── docker-compose.yml     # Multi-container orchestration (FastAPI, Postgres, n8n, Nginx)
├── Dockerfile             # FastAPI container build instructions
├── requirements.txt       # Python dependencies
└── start-dev.sh           # One-click startup and health-check script for macOS
```

## Quick Start (< 60 Seconds)

1. **Configure Environment Secrets:**
   ```bash
   cp .env.example .env
   ```
2. **Launch the Full Stack:**
   ```bash
   docker compose up -d --build
   ```
   *(On macOS, you can also run `./start-dev.sh` to automatically start Docker Desktop, verify service health, and open both dashboards.)*
3. **Access Services:**
   * **FastAPI Swagger UI:** `http://localhost/docs`
   * **n8n Agent Orchestrator:** `http://localhost:5678` (import the workflow JSON from `n8n_workflows/`, attach your Google Gemini API key, and toggle the workflow **Active**).

## Native iOS Client

This backend ecosystem pairs with a native **SwiftUI iOS Command Center** featuring iOS Keychain JWT persistence, real-time PostgreSQL task sync, and conversational control over the n8n + Gemini AI Agent:

📱 **iOS Repository:** [ai-agent-command-center-ios](https://github.com/sumitkapoor2511/ai-agent-command-center-ios)
