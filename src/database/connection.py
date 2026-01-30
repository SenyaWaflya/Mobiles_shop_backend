from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.database.models import BaseModel
from src.settings import settings

engine = create_async_engine(url=settings.db_url)

async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
