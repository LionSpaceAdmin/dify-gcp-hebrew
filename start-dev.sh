#!/bin/bash

# Dify Hebrew/Vertex AI Development Setup
set -e

echo "🚀 Starting Dify with Hebrew & Vertex AI support..."

# Check Docker is running
if ! docker version > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Create data directories
mkdir -p data/{db,redis,app-storage}

# Set permissions
chmod -R 755 data/

# Start core services first
echo "📦 Starting database and Redis..."
docker compose -f docker-compose.dev.yaml up -d db redis

# Wait for database
echo "⏳ Waiting for database to be ready..."
sleep 10

# Check database health
until docker compose -f docker-compose.dev.yaml exec -T db pg_isready -U postgres > /dev/null 2>&1; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done

echo "✅ Database is ready!"

# Check Redis
echo "⏳ Checking Redis..."
until docker compose -f docker-compose.dev.yaml exec -T redis redis-cli ping > /dev/null 2>&1; do
    echo "Waiting for Redis..."
    sleep 2
done

echo "✅ Redis is ready!"

echo "🎯 Core services are running. You can now:"
echo "   1. Start API:    docker compose -f docker-compose.dev.yaml up -d api"
echo "   2. Start Worker: docker compose -f docker-compose.dev.yaml up -d worker"
echo "   3. Start Web:    docker compose -f docker-compose.dev.yaml up -d web"
echo "   4. Start All:    docker compose -f docker-compose.dev.yaml up -d"
echo ""
echo "📱 Access points:"
echo "   - Web UI:        http://localhost:3000"
echo "   - API:           http://localhost:5001"
echo "   - Swagger:       http://localhost:5001/swagger-ui.html"
echo "   - Database:      localhost:5433 (postgres/difyai123456)"
echo ""
echo "🔍 Useful commands:"
echo "   - Logs:          docker compose -f docker-compose.dev.yaml logs -f"
echo "   - Stop:          docker compose -f docker-compose.dev.yaml down"
echo "   - Rebuild:       docker compose -f docker-compose.dev.yaml build --no-cache"