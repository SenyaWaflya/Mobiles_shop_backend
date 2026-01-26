from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings
from src.database.models import BaseModel

engine = create_async_engine(
    url=f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
)

async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
