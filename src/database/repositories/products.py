from sqlalchemy.sql import exists, select

from src.database.connection import async_session
from src.database.models import ProductModel
from src.schemas.products import ProductDto


class ProductsRepository:
    @staticmethod
    async def check_exists_product_by_title(product_title: str) -> bool:
        async with async_session() as session:
            query = select(exists().where(ProductModel.title == product_title))
            result = await session.execute(query)
            exists_product = result.scalar()
            return exists_product

    @staticmethod
    async def check_exists_product_by_id(product_id: int) -> bool:
        async with async_session() as session:
            query = select(exists().where(ProductModel.id == product_id))
            result = await session.execute(query)
            exists_product = result.scalar()
            return exists_product

    @staticmethod
    async def add(product_dto: ProductDto) -> ProductModel:
        async with async_session() as session:
            product_model = ProductModel(
                brand=product_dto.brand,
                title=product_dto.title,
                price=product_dto.price,
                quantity=product_dto.quantity,
                image_path=product_dto.image_path,
            )
            session.add(product_model)
            await session.commit()
            await session.refresh(product_model)
            return product_model

    @staticmethod
    async def get(product_id: int) -> ProductModel:
        async with async_session() as session:
            query = select(ProductModel).where(ProductModel.id == product_id)
            result = await session.execute(query)
            product_model = result.scalars().first()
            return product_model

    @staticmethod
    async def get_all() -> list[ProductModel]:
        async with async_session() as session:
            query = select(ProductModel)
            result = await session.execute(query)
            products_models = result.scalars().all()
            return products_models

    @staticmethod
    async def edit(product_id: int, new_quantity: int, new_price: int, new_image_path: str) -> ProductModel:
        async with async_session() as session:
            query = select(ProductModel).where(ProductModel.id == product_id)
            result = await session.execute(query)
            product_model = result.scalars().first()
            product_model.quantity = new_quantity
            product_model.price = new_price
            product_model.image_path = new_image_path
            await session.commit()
            await session.refresh(product_model)
            return product_model

    @staticmethod
    async def delete(product_id: int) -> ProductModel:
        async with async_session() as session:
            query = select(ProductModel).where(ProductModel.id == product_id)
            result = await session.execute(query)
            product_model = result.scalars().first()
            await session.delete(product_model)
            await session.commit()
            return product_model

    @staticmethod
    async def get_brands() -> list[str]:
        async with async_session() as session:
            query = select(ProductModel.brand).distinct()
            result = await session.execute(query)
            brands = result.scalars().all()
            return brands
