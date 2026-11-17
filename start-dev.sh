#!/bin/bash

# Navigate to the directory where this script is located
cd "$(dirname "$0")"

echo "🚀 Starting Agent Command Center Stack..."

# 1. Start Docker Desktop if not already running
if ! docker info > /dev/null 2>&1; then
  echo "🐳 Opening Docker Desktop..."
  open -a Docker
  echo "⏳ Waiting for Docker daemon to start..."
  while ! docker info > /dev/null 2>&1; do
    sleep 2
  done
fi

# 2. Start all containers in detached mode
echo "📦 Starting FastAPI, PostgreSQL, Nginx, and n8n..."
docker compose up -d

# 3. Wait for FastAPI & n8n endpoints to respond
echo "🩺 Checking service health..."
until curl -s http://localhost/docs > /dev/null; do
  sleep 1
done
echo "✅ FastAPI Swagger is live at http://localhost/docs"

until curl -s http://localhost:5678 > /dev/null; do
  sleep 1
done
echo "✅ n8n Editor is live at http://localhost:5678"

# 4. Show running container status
docker compose ps

# 5. Open Swagger & n8n in browser
open http://localhost/docs
oplhost:5678/workflow/Tu7lspb42EQn5IvL

echo "🎉 All backend services are ready! Press Cmd + R in Xcode to launch the iOS app."
