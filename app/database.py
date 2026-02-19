from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

<<<<<<< HEAD

class Base(DeclarativeBase):
    pass


=======
class Base(DeclarativeBase):
    pass

>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
