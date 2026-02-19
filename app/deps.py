<<<<<<< HEAD
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db


async def get_session() -> AsyncSession:
    async for s in get_db():
        return s
=======
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

# Re-export get_db as the session dependency.
# FastAPI understands async generator dependencies and will properly
# handle the cleanup (closing the session) after the request finishes.
get_session = get_db
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
