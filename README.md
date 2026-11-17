# AI-Native Full-Stack & Autonomous Agent Platform

An enterprise-grade automation ecosystem built with **FastAPI**, **PostgreSQL**, **n8n AI Agents (Google Gemini)**, and **Nginx Reverse Proxy**, orchestrated via **Docker Compose**. For the complete ASCII architecture diagram, component breakdown, and full-CRUD agent specifications, please see the full repository structure.

## Quick Start (< 60 Seconds)

1. Copy `.env.example` to `.env` and fill in your secrets:
   ```bash
   cp .env.example .env
   ```
2. Launch the full stack:
   ```bash
   docker compose up -d --build
   ```
3. Access **FastAPI Swagger UI** at `http://localhost/docs` and **n8n** at `http://localhost:5678`.

## Native iOS Client

Pairs with a native SwiftUI iOS Command Center:
📱 **iOS Repository:** [ai-agent-command-center-ios](https://github.com)
