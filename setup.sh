#!/bin/bash

# ChefGenie Setup Script
# This script helps with initial setup

set -e

echo "🍳 ChefGenie Setup Script"
echo "========================"

# Check prerequisites
echo ""
echo "Checking prerequisites..."

command -v python3 &> /dev/null || { echo "Python 3 not found"; exit 1; }
command -v docker &> /dev/null || { echo "Docker not found"; exit 1; }
command -v node &> /dev/null || { echo "Node.js not found"; exit 1; }

echo "✓ Python 3"
echo "✓ Docker"
echo "✓ Node.js"

# Setup environment
echo ""
echo "Setting up environment..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env from .env.example"
    echo ""
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    echo ""
    exit 1
fi

# Backend setup
echo ""
echo "Setting up backend..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Created Python virtual environment"
fi

source .venv/bin/activate 2>/dev/null || .\.venv\Scripts\activate

pip install -q -r requirements.txt
echo "✓ Installed Python dependencies"

# Ingest KB
echo ""
echo "Ingesting recipe knowledge base..."

python ingest_kb.py

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "==========="
echo ""
echo "Option 1: Run with Docker Compose (Recommended)"
echo "  docker-compose up -d"
echo "  Visit: http://localhost:3000"
echo ""
echo "Option 2: Run locally"
echo "Backend: uvicorn app.main:app --reload"
echo "Frontend: cd frontend && npm install && npm run dev"
echo ""
