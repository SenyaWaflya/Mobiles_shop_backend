from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey

from models.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    password = Column(Text, nullable=False)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)


# class Favorite(Base):
#     __tablename__ = 'favorites'
#
#     id = Column(Integer, primary_key=True, index=True)
#     products = Column(JSON)
#     author_id = Column(Integer, ForeignKey('users.id'))
