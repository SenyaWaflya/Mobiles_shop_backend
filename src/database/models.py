from sqlalchemy import Column, Integer, String, Text, BOOLEAN

from src.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_superuser = Column(BOOLEAN, default=False, nullable=False)
    is_owner = Column(BOOLEAN, default=False, nullable=False)
    password = Column(Text, nullable=False)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
