# ChefGenie - First Time Setup Checklist

Follow this checklist to get ChefGenie running on your machine.

## Pre-Requisites Check

- [ ] Git installed (`git --version`)
- [ ] Python 3.11+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Docker installed (`docker --version`)
- [ ] Docker Compose installed (`docker-compose --version`)
- [ ] OpenAI Account with API key credit

## 1. Clone & Navigate

```bash
# Clone if needed (or use existing repo)
git clone https://github.com/yourusername/Better-Half.git
cd Better-Half
```

- [ ] Repository cloned
- [ ] Currently in Better-Half directory

## 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit with your editor
nano .env  # or use VS Code, Sublime, etc.
# Add: OPENAI_API_KEY=sk-...
```

- [ ] `.env` file created
- [ ] `OPENAI_API_KEY` added
- [ ] Other values verified (optional)

## 3. Docker Compose Deployment (Recommended)

```bash
# Start all services
docker-compose up -d

# Wait 30-60 seconds for services to initialize
docker-compose ps

# Check logs if issues
docker-compose logs -f
```

- [ ] Docker services started
- [ ] PostgreSQL healthy
- [ ] Backend healthy
- [ ] Frontend healthy
- [ ] All services showing as "Up"

## 4. Verify Installation

```bash
# Check backend health
curl http://localhost:8000/healthz

# Check knowledge base loaded
curl http://localhost:8000/kb/stats

# Check frontend is accessible
curl http://localhost:3000
```

- [ ] Backend responding at port 8000
- [ ] Recipes loaded in KB (count > 0)
- [ ] Frontend accessible at port 3000

## 5. First Time Usage

### Open Application

1. [ ] Open browser
2. [ ] Go to http://localhost:3000
3. [ ] See ChefGenie navigation bar
4. [ ] All pages load without errors

### Set Your Preferences

1. [ ] Click "Preferences" in navigation
2. [ ] Select allergies (or skip)
3. [ ] Select dietary restrictions (or skip)
4. [ ] Select preferred cuisines
5. [ ] Click "Save Preferences"
6. [ ] See success message

### Add Some Ingredients

1. [ ] Click "Pantry" in navigation
2. [ ] Click "Add Item"
3. [ ] Enter ingredient name: "tomato"
4. [ ] Enter quantity: "3" (optional)
5. [ ] Click "Add"
6. [ ] See item appear in pantry list
7. [ ] Add 3-4 more ingredients
8. [ ] Each appears immediately

### Get Recipe Suggestions

1. [ ] Click "Recipes" in navigation
2. [ ] Click "Suggest Recipes" button
3. [ ] Wait 10-30 seconds (LLM is thinking)
4. [ ] See 3 recipe cards appear
5. [ ] Each recipe shows:
   - [ ] Title and cuisine
   - [ ] Match score (%)
   - [ ] Ingredients you have
   - [ ] Missing ingredients
   - [ ] Cooking steps

### Test Image Upload (Optional)

1. [ ] Find a food image URL online (must be publicly accessible)
   - Example: https://images.unsplash.com/photo-...
2. [ ] Go back to "Pantry"
3. [ ] Paste URL in "Image URL" field
4. [ ] Click "Analyze Image"
5. [ ] Wait 10 seconds
6. [ ] See detected ingredients appear
7. [ ] Items should be added to pantry

- [ ] UI responds to interactions
- [ ] Recipe suggestions appear
- [ ] Images can be analyzed (if available)
- [ ] Preferences are saved

## 6. Explore API Documentation

1. [ ] Go to http://localhost:8000/docs
2. [ ] See interactive API documentation
3. [ ] Try an endpoint: Click "Try it out"
4. [ ] For example, GET `/preferences`
5. [ ] Click "Execute"
6. [ ] See response with your preferences

- [ ] Swagger UI loads
- [ ] Can execute API calls
- [ ] Responses are valid JSON

## 7. Check Backend Logs

```bash
docker-compose logs backend | tail -50
```

- [ ] No error messages
- [ ] Server is responding to requests
- [ ] LLM calls are working

## 8. Database Verification (Optional)

```bash
# Connect to PostgreSQL
docker exec -it chefgenie_db psql -U chefgenie -d chefgenie

# In psql prompt, try:
\dt  # List table
SELECT COUNT(*) FROM user_preferences;
SELECT COUNT(*) FROM pantry_items;
\q  # Exit
```

- [ ] Database connection works
- [ ] Tables exist
- [ ] Can read data

## 9. Local Development (Optional)

If you want to modify code:

```bash
# Stop Docker
docker-compose down

# Backend only
source .venv/bin/activate  # or source it if exists
pip install -r requirements.txt
python ingest_kb.py
uvicorn app.main:app --reload

# Frontend in new terminal
cd frontend
npm install
npm run dev
```

- [ ] Virtual environment activated
- [ ] Backend runs locally on 8000
- [ ] Frontend runs locally on 3000
- [ ] Changes are automatically reloaded

## 10. Troubleshooting

If something doesn't work:

### Backend not responding
```bash
# Check if running
docker-compose ps

# View logs
docker-compose logs backend

# Restart
docker-compose restart backend
```

- [ ] Backend container is running
- [ ] No Python errors in logs
- [ ] Port 8000 is not in use

### Frontend stuck
```bash
# Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
# Hard reload (Ctrl+Shift+R or Cmd+Shift+R)
# Check browser console (F12)
```

- [ ] Console shows no errors
- [ ] API calls are reaching localhost:8000

### API Key error
```bash
# Make sure key is in .env
cat .env | grep OPENAI_API_KEY

# Restart containers
docker-compose down
docker-compose up -d
```

- [ ] Key exists in .env  
- [ ] No extra spaces in key
- [ ] Containers restarted

### Recipes not loading
```bash
# Ingest recipes
docker exec chefgenie_api python ingest_kb.py

# Check count
curl http://localhost:8000/kb/stats
```

- [ ] Recipe count > 0
- [ ] Recipe files exist in app/kb/recipes/

## 11. Success Criteria

You're done if you can:

- [ ] Access frontend at http://localhost:3000
- [ ] Set preferences and they save
- [ ] Add ingredients to pantry
- [ ] Get recipe suggestions
- [ ] See API docs at http://localhost:8000/docs
- [ ] Make API calls successfully
- [ ] See logs in `docker-compose logs -f`

## 12. Next Steps

Once everything works:

1. **Add More Recipes**
   - Create new `.md` files in `app/kb/recipes/`
   - Run `docker exec chefgenie_api python ingest_kb.py`

2. **Explore the Code**
   - Backend: `app/routers/` and `app/services/`
   - Frontend: `frontend/src/pages/` and `frontend/src/components/`

3. **Customize**
   - Change colors in `frontend/src/index.css`
   - Add new recipe suggestions in recipes.py service
   - Extend database models in `app/models.py`

4. **Deploy**
   - Follow `DEPLOYMENT.md` for AWS, GCP, Azure, DigitalOcean

## 13. Keep Things Clean

```bash
# Stop Docker Compose
docker-compose down

# Remove volumes (keeps data)
docker-compose down -v

# See disk space
docker system df

# Cleanup unused images
docker image prune
```

- [ ] Understand how to stop/start services
- [ ] Know how to clean up Docker resources

## 14. Get Help

If you're stuck:

1. Check `README.md` - main documentation
2. Check `QUICKSTART.md` - common issues  
3. View logs: `docker-compose logs -f`
4. Check API docs: http://localhost:8000/docs
5. Open a GitHub issue with error details

---

## 🎉 Congratulations!

If you've checked off most of these boxes, your ChefGenie application is fully functional!

**You have successfully set up:**
- ✅ Full-stack AI application
- ✅ PostgreSQL database with Docker
- ✅ Vice Framework backend
- ✅ React TypeScript frontend
- ✅ Recipe knowledge base
- ✅ Image recognition
- ✅ RAG system

**Ready for:**
- Building new features
- Deploying to cloud
- Sharing with others
- Learning about AI/LLMs

---

## Quick Reference

| What | Where | Command |
|------|-------|---------|
| Start App | Terminal | `docker-compose up -d` |
| Stop App | Terminal | `docker-compose down` |
| View Logs | Terminal | `docker-compose logs -f` |
| Frontend | Browser | http://localhost:3000 |
| Backend API | Browser | http://localhost:8000 |
| API Docs | Browser | http://localhost:8000/docs |
| Database CLI | Terminal | `docker exec -it chefgenie_db psql -U chefgenie -d chefgenie` |

---

*You're all set! Enjoy using ChefGenie!* 🍳🤖
