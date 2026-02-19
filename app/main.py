<<<<<<< HEAD
=======
import asyncio
import pathlib
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
<<<<<<< HEAD
from app.database import engine, Base
from app.routers import pantry, preferences, recipes, vision, kb
import os
=======
from sqlalchemy.ext.asyncio import AsyncEngine
from app.database import engine, Base
from app.routers import pantry, preferences, recipes, vision, kb
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0

app = FastAPI(title="ChefGenie API", version="1.0")

app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


=======
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

<<<<<<< HEAD

@app.get("/healthz")
def health():
    return {"status": "ok"}


=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
app.include_router(preferences.router)
app.include_router(pantry.router)
app.include_router(vision.router)
app.include_router(recipes.router)
app.include_router(kb.router)

<<<<<<< HEAD

# Serve the HTML frontend
_static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(_static_dir):
    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(_static_dir, "index.html"))
=======
_STATIC = pathlib.Path(__file__).parent / "static"

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/")
def index():
    return FileResponse(_STATIC / "index.html")

app.mount("/static", StaticFiles(directory=_STATIC), name="static")
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
