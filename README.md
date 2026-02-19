# ChefGenie - AI-Powered Recipe Suggestion App

A full-stack application that uses AI, RAG (Retrieval Augmented Generation), and LLMs to suggest recipes based on your pantry items, dietary restrictions, and allergies.

## Features

✨ **Smart Recipe Suggestions** - AI-powered recipe recommendations based on your ingredients
📸 **Image Recognition** - Upload photos of your food to automatically detect ingredients  
🥗 **Dietary Preferences** - Track allergies, dietary restrictions, and cuisine preferences
🔍 **RAG-Based Search** - Knowledge base of recipes with semantic search
🍳 **Missing Ingredients** - Get shopping lists for recipes you want to make
📱 **Full-Stack** - React frontend, FastAPI backend, PostgreSQL database

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (Docker) or SQLite (local)
- **Vector DB**: ChromaDB for RAG & semantic search
- **LLM**: OpenAI GPT-4o-mini (or Azure OpenAI)
- **Async**: SQLAlchemy async ORM

### Frontend  
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Router**: React Router v6

### DevOps
- **Containerization**: Docker & Docker Compose
- **Deployment Ready**: AWS, DigitalOcean, GCP

## Quick Start - Docker Compose (Recommended)

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key

### Steps

```bash
# Clone and setup
cd Better-Half
cp .env.example .env

# Add your OpenAI API key to .env
# OPENAI_API_KEY=your_key_here

# Start all services
docker-compose up -d
```

Access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: PostgreSQL on port 5432 (user: chefgenie)

## Quick Start - Local Development

### Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add OPENAI_API_KEY

# Ingest recipe knowledge base
python ingest_kb.py

# Run API server
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at http://localhost:3000

The dev server automatically proxies API calls to http://localhost:8000

## Project Structure

```
Better-Half/
├── app/                           # FastAPI Backend
│   ├── main.py                   # FastAPI application
│   ├── config.py                 # Configuration settings
│   ├── database.py               # Database initialization
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── schemas.py                # Pydantic request/response schemas
│   ├── deps.py                   # Dependency injection
│   │
│   ├── routers/                  # API Route Handlers
│   │   ├── pantry.py            # Pantry management endpoints
│   │   ├── preferences.py       # User preferences endpoints
│   │   ├── recipes.py           # Recipe suggestion endpoints
│   │   ├── vision.py            # Image analysis endpoints
│   │   └── kb.py                # Knowledge base endpoints
│   │
│   ├── services/                 # Business Logic
│   │   ├── llm.py               # OpenAI/Azure LLM integration
│   │   ├── rag.py               # RAG with ChromaDB
│   │   ├── image.py             # Vision/image processing
│   │   ├── recipe_suggester.py  # Recipe suggestion engine
│   │   └── utils.py             # Utility functions
│   │
│   └── kb/                       # Knowledge Base
│       └── recipes/              # Recipe markdown files with YAML front matter
│
├── frontend/                      # React + TypeScript Frontend
│   ├── src/
│   │   ├── pages/               # Page components (Pantry, Recipes, Preferences)
│   │   ├── components/          # Reusable UI components
│   │   ├── hooks/               # Custom React hooks (useAPI)
│   │   ├── types/               # TypeScript type definitions
│   │   ├── api/                 # API client
│   │   ├── App.tsx              # Main App component
│   │   ├── main.tsx             # React entry point
│   │   └── index.css            # Global styles
│   ├── index.html               # HTML template
│   └── Dockerfile               # Frontend container config
│
├── docker-compose.yml            # Multi-container orchestration
├── Dockerfile                    # Backend container config
├── requirements.txt              # Python dependencies
├── ingest_kb.py                  # Script to populate ChromaDB
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## API Endpoints

### Pantry Management
- `GET /pantry` - List all pantry items
- `POST /pantry` - Add item to pantry
- `PUT /pantry/{id}` - Update pantry item
- `DELETE /pantry/{id}` - Remove item from pantry
- `DELETE /pantry` - Clear entire pantry

### User Preferences
- `GET /preferences` - Get current user preferences
- `PUT /preferences` - Update preferences (allergies, diets, cuisines)

### Recipe Suggestions
- `POST /recipes/suggest` - Get recipe suggestions based on pantry and preferences

### Vision (Image Recognition)
- `POST /vision/pantry` - Analyze food image and add detected items to pantry

### Knowledge Base
- `GET /kb/stats` - Get knowledge base statistics

## Example API Usage

```bash
# Get user preferences
curl http://localhost:8000/preferences

# Update preferences  
curl -X PUT http://localhost:8000/preferences \
  -H "Content-Type: application/json" \
  -d '{
    "allergies": ["peanuts", "shellfish"],
    "diets": ["vegetarian"],
    "preferred_cuisines": ["italian"]
  }'

# Add pantry item
curl -X POST http://localhost:8000/pantry \
  -H "Content-Type: application/json" \
  -d '{"name": "tomato", "quantity": "3"}'

# Get recipe suggestions  
curl -X POST http://localhost:8000/recipes/suggest \
  -H "Content-Type: application/json" \
  -d '{"cuisine": "italian", "allow_missing": true}'

# Analyze food image
curl -X POST http://localhost:8000/vision/pantry \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/food.jpg",
    "add_to_pantry": true
  }'
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Server
APP_ENV=local
API_PORT=8000

# Database
SQLALCHEMY_DATABASE_URL=sqlite+aiosqlite:///./app.db
# For PostgreSQL in Docker: postgresql+psycopg2://chefgenie:chefgenie_password@postgres:5432/chefgenie

# LLM Provider
LLM_PROVIDER=openai  # or 'azure'
OPENAI_API_KEY=your_key_here
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBED_MODEL=text-embedding-3-small

# Vector Database
VECTOR_DB_DIR=./chroma_store
```

## Knowledge Base Format

Add recipes to `app/kb/recipes/` as markdown files with YAML front matter:

```yaml
---
id: kb_recipe_001
title: Pesto Pasta
cuisine: italian
tags: [pasta, vegetarian, quick]
ingredients:
  - pasta
  - basil
  - olive oil
  - garlic
  - parmesan
content: |
  Instructions and description here...
---
```

Then run: `python ingest_kb.py`

## Deployment

### Docker Compose (Single Command)
```bash
docker-compose up -d
```

### Building for Production

```bash
# Build backend image
docker build -t chefgenie-backend:latest .

# Build frontend image
docker build -t chefgenie-frontend:latest ./frontend
```

### AWS Deployment

1. Push images to Amazon ECR:
```bash
aws ecr create-repository --repository-name chefgenie-backend
docker tag chefgenie-backend:latest <account>.dkr.ecr.<region>.amazonaws.com/chefgenie-backend:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/chefgenie-backend:latest
```

2. Deploy using ECS, EKS, or Elastic Beanstalk

3. Set environment variables in AWS console

### DigitalOcean Deployment

1. Push to DigitalOcean Container Registry
2. Deploy using App Platform or Docker on a Droplet

### Other Cloud Providers

Similar process for GCP (Cloud Run), Azure (Container Instances), etc.

## Development

### Adding New Recipes
```bash
# Create recipe file in app/kb/recipes/your_recipe.md
# Rerun ingestion
python ingest_kb.py
```

### Database Migrations
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Frontend Build
```bash
cd frontend
npm run build  # Creates optimized dist/
npm run preview  # Preview production build
```

## Troubleshooting

**Backend won't start**: Make sure PostgreSQL is running if using Docker Compose
```bash
docker-compose ps
```

**API key error**: Verify OPENAI_API_KEY is set in .env
```bash
source .env
echo $OPENAI_API_KEY
```

**Frontend can't reach API**: Check CORS settings in `docker-compose.yml` or `app/main.py`

**Recipes not showing**: Verify recipes were ingested
```bash
curl http://localhost:8000/kb/stats
```

## Contributing

1. Create a feature branch
2. Make changes and test locally
3. Submit a pull request

## License

MIT License

## Support

For issues and questions, open a GitHub issue.

---

Built with ❤️ for food lovers and AI enthusiasts 🤖
