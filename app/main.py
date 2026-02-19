from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.routers import pantry, preferences, recipes, vision, kb
import os

app = FastAPI(title="ChefGenie API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/healthz")
def health():
    return {"status": "ok"}


app.include_router(preferences.router)
app.include_router(pantry.router)
app.include_router(vision.router)
app.include_router(recipes.router)
app.include_router(kb.router)


# Serve the HTML frontend
_static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(_static_dir):
    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(_static_dir, "index.html"))
