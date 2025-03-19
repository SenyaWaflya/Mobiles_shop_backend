from sqlalchemy import Column, ForeignKey, Integer, String, Text, BOOLEAN
from sqlalchemy.orm import relationship

from src.database.database import Base


class UserProduct(Base):
    __tablename__ = 'users_product_association'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_superuser = Column(BOOLEAN, default=False, nullable=False)
    is_owner = Column(BOOLEAN, default=False, nullable=False)
    password = Column(Text, nullable=False)

    products = relationship('Product', secondary='users_product_association', back_populates='users')

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)

    users = relationship('User', secondary='users_product_association', back_populates='products')
