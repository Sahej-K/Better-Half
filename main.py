import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine
from app.database import engine, Base
from app.routers import pantry, preferences, recipes, vision, kb

app = FastAPI(title="ChefGenie API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # Auto-create tables (for demo). In production: use Alembic migrations.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(preferences.router)
app.include_router(pantry.router)
app.include_router(vision.router)
app.include_router(recipes.router)
app.include_router(kb.router)

@app.get("/healthz")
def health():
    return {"status": "ok"}