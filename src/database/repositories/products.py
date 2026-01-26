from sqlalchemy.sql import exists, select

from src.database.connection import async_session
from src.database.models import ProductModel
from src.schemas.products import ProductDto, ProductResponse


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
    async def add(product_dto: ProductDto) -> ProductResponse:
        async with async_session() as session:
            product = ProductModel(
                brand=product_dto.brand, title=product_dto.title, price=product_dto.price, quantity=product_dto.quantity
            )
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return ProductResponse.model_validate(product)

    @staticmethod
    async def get(product_id: int) -> ProductResponse:
        async with async_session() as session:
            query = select(ProductModel).where(ProductModel.id == product_id)
            result = await session.execute(query)
            product = result.scalars().first()
            return ProductResponse.model_validate(product)

    @staticmethod
    async def get_all() -> list[ProductResponse]:
        async with async_session() as session:
            query = select(ProductModel)
            result = await session.execute(query)
            products = result.scalars().all()
            return [ProductResponse.model_validate(product) for product in products]

    @staticmethod
    async def edit(product_id: int, new_quantity: int, new_price: int) -> ProductResponse:
        async with async_session() as session:
            query = select(ProductModel).where(ProductModel.id == product_id)
            result = await session.execute(query)
            product = result.scalars().first()
            product.quantity = new_quantity
            product.price = new_price
            await session.commit()
            await session.refresh(product)
            return ProductResponse.model_validate(product)

    @staticmethod
    async def delete(product_id: int) -> ProductResponse:
        async with async_session() as session:
            query = select(ProductModel).where(ProductModel.id == product_id)
            result = await session.execute(query)
            product = result.scalars().first()
            await session.delete(product)
            await session.commit()
            return ProductResponse.model_validate(product)
