from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

# Re-export get_db as the session dependency.
# FastAPI understands async generator dependencies and will properly
# handle the cleanup (closing the session) after the request finishes.
get_session = get_db
