from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

async def get_session() -> AsyncSession:
    async for s in get_db():
        return s