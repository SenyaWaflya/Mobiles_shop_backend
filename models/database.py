from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


engine = create_engine(url=f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
