# AI-Native Full-Stack & Autonomous Agent Platform

An enterprise-grade, multi-tier automation ecosystem built with **FastAPI**, **PostgreSQL**, **n8n AI Agents (Google Gemini)**, and **Nginx Reverse Proxy**, orchestrated via **Docker Compose**.

## System Architecture
- **Gateway (`nginx:alpine`):** Unified entry point on Port 80 routing `/api/*` to FastAPI and `/webhook/*` to n8n while isolating internal services.
- **API Core (`FastAPI` + `SQLModel`):** Asynchronous REST API secured with OAuth2 JWT Bearer authentication, bcrypt password hashing, and strict Pydantic v2 validation.
- **Persistence (`postgres:16-alpine`):** Relational storage for users and automation task queues.
- **Agentic Orchestrator (`n8n`):** Autonomous webhook-driven AI agent with window buffer memory and dynamic HTTP tool-calling into FastAPI.

## Quick Start (< 60 Seconds)
1. Clone the repository and configure your `.env` secrets file.
2. Launch the full stack:
   ```bash
   docker compose up -d --build
   ```
3. Access API documentation at `http://localhost/docs`.

## Native iOS Client
This backend ecosystem pairs with a native **SwiftUI iOS Command Center** featuring Keychain JWT persistence, real-time PostgreSQL task sync, and conversational control over the n8n + Gemini AI Agent:

📱 **iOS Repository:** [ai-agent-command-center-ios](https://github.com)
