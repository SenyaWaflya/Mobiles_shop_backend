from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now(), server_onupdate=func.now())


class UserProductModel(BaseModel):
    __tablename__ = 'users_product_association'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)


class UserModel(BaseModel):
    __tablename__ = 'users'

    tg_id: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True)

    products = relationship('ProductModel', secondary='users_product_association', back_populates='users')


class ProductModel(BaseModel):
    __tablename__ = 'products'

    brand: Mapped[str] = mapped_column(index=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_path: Mapped[str] = mapped_column(unique=True)

    users = relationship('UserModel', secondary='users_product_association', back_populates='products')
