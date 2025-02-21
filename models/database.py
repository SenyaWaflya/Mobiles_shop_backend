from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings


engine = create_engine(url=f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
