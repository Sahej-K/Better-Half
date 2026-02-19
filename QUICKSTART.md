# ChefGenie - Getting Started Guide

## Installation & Startup

### Option 1: Docker Compose (Easiest - Recommended)

**Requirements:**
- Docker & Docker Compose installed

**Steps:**

```bash
# 1. Clone and navigate
cd Better-Half

# 2. Setup environment
cp .env.example .env

# 3. Edit .env and add OpenAI key
# On macOS/Linux:
nano .env  # or use your favorite editor
# On Windows: edit .env in notepad

# 4. Start everything
docker-compose up -d

# 5. Wait for services to be healthy (30-60 seconds)
docker-compose ps

# 6. Open in browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

**Viewing Logs:**
```bash
docker-compose logs -f backend  # Backend logs
docker-compose logs -f frontend # Frontend logs  
docker-compose logs -f postgres # Database logs
```

**Stopping Services:**
```bash
docker-compose down
```

---

### Option 2: Local Development (Backend + Frontend Separate)

**Requirements:**
- Python 3.11+
- Node.js 18+
- PostgreSQL (or use SQLite in local .env)

**Backend Setup:**

```bash
# 1. Create and activate virtual environment
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env - make sure OPENAI_API_KEY is set

# 4. Ingest recipes
python ingest_kb.py

# 5. Run backend
uvicorn app.main:app --reload

# Backend will be at http://localhost:8000
```

**Frontend Setup (in another terminal):**

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Start development server
npm run dev

# Frontend will be at http://localhost:3000
```

---

## Using the App

### 1. Set Your Preferences
- Click **Preferences** in the navigation
- Select your allergies, dietary restrictions, and preferred cuisines
- Click **Save Preferences**

### 2. Add Ingredients
- Click **Pantry** in the navigation
- Add ingredients by typing name and quantity
- Or upload a food photo to auto-detect ingredients

### 3. Get Recipe Suggestions
- Click **Recipes** in the navigation
- Select a cuisine (optional)
- Click **Suggest Recipes**
- View suggested recipes with missing items

---

## API Usage Examples

### Using cURL

```bash
# Health check
curl http://localhost:8000/healthz

# Get preferences
curl http://localhost:8000/preferences

# Update preferences
curl -X PUT http://localhost:8000/preferences \
  -H "Content-Type: application/json" \
  -d '{
    "allergies": ["peanuts"],
    "diets": ["vegetarian"],
    "preferred_cuisines": ["Italian"]
  }'

# Add pantry item
curl -X POST http://localhost:8000/pantry \
  -H "Content-Type: application/json" \
  -d '{
    "name": "tomatoes",
    "quantity": "2 cups"
  }'

# Get recipe suggestions
curl -X POST http://localhost:8000/recipes/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "cuisine": "italian",
    "allow_missing": true
  }'
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Get preferences
prefs = requests.get(f"{BASE_URL}/preferences").json()

# Update preferences  
requests.put(f"{BASE_URL}/preferences", json={
    "allergies": ["peanuts"],
    "diets": ["vegetarian"]
})

# Add pantry item
requests.post(f"{BASE_URL}/pantry", json={
    "name": "tomatoes",
    "quantity": "2 cups"
})

# Get suggestions
suggestions = requests.post(f"{BASE_URL}/recipes/suggest", json={
    "cuisine": "italian"
}).json()

for recipe in suggestions['recipes']:
    print(f"- {recipe['title']} (Score: {recipe['score']}%)")
```

---

## Common Issues

### "Connection refused" error
- Make sure backend is running
- Check: `docker-compose ps` or `http://localhost:8000/docs`

### "OpenAI API key error"
- Verify key is in `.env`: `echo $OPENAI_API_KEY`
- Make sure no spaces or special chars around the key

### Frontend shows errors but backend is fine
- Clear browser cache (Cmd+Shift+Delete / Ctrl+Shift+Delete)
- Check browser console: F12 → Console tab
- Make sure `http://localhost:8000` is reachable

### PostgreSQL connection error
- In Docker: `docker-compose ps` should show postgres "healthy"
- Wait 30 seconds after starting for postgres to initialize
- Check logs: `docker-compose logs postgres`

### Recipe suggestions not working
- Check recipes were ingested: `curl http://localhost:8000/kb/stats`
- Make sure pantry has items added
- Check backend logs for LLM errors

---

## Useful Commands

```bash
# View all services status
docker-compose ps

# View logs
docker-compose logs -f

# Restart everything
docker-compose restart

# Rebuild images
docker-compose up -d --build

# Clean up (removes volumes)
docker-compose down -v

# Access database directly
docker exec -it chefgenie_db psql -U chefgenie -d chefgenie

# Rebuild frontend
cd frontend && npm run build

# Test API endpoints
curl http://localhost:8000/docs  # Swagger UI
```

---

## Environment Variables

Key variables in `.env`:

| Variable | Default | Notes |
|----------|---------|-------|
| `OPENAI_API_KEY` | None (required) | Your OpenAI API key |
| `SQLALCHEMY_DATABASE_URL` | `sqlite+aiosqlite:///./app.db` | Database connection |
| `VECTOR_DB_DIR` | `./chroma_store` | ChromaDB storage location |
| `LLM_PROVIDER` | `openai` | Use "azure" for Azure OpenAI |

---

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs for interactive API docs
2. **Add More Recipes**: Place markdown files in `app/kb/recipes/` and run `python ingest_kb.py`
3. **Customize**: Edit `frontend/src/components/` to change UI
4. **Deploy**: See README.md for deployment instructions

---

## Support

- API Docs: http://localhost:8000/docs
- FastAPI Help: https://fastapi.tiangolo.com/
- React Docs: https://react.dev
- ChromaDB: https://docs.trychroma.com/

---

Happy cooking! 🍳🤖
