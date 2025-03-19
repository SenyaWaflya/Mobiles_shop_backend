from fastapi import  HTTPException, status
from sqlalchemy import select

from src.database.database import new_session
from src.database.models import Product
from src.schemas.product import ProductDto, ProductResponse
from src.auth.jwt import validate_admin_permissions


class ProductService:
    @staticmethod
    async def get_all_products() -> list[ProductResponse]:
        async with new_session() as session:
            query = select(Product)
            result = await session.execute(query)
            products = result.scalars().all()
            if not products:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No products found')
            return [ProductResponse.model_validate(product) for product in products]


    @staticmethod
    async def create(product_dto: ProductDto, token_payload: dict) -> ProductResponse:
        validate_admin_permissions(token_payload)
        async with new_session() as session:
            product = Product(
                title=product_dto.title,
                quantity=product_dto.quantity
            )
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product


    @staticmethod
    async def get_product_by_id(id: int) -> ProductResponse:
        async with new_session() as session:
            query = select(Product).where(Product.id == id)
            result = await session.execute(query)
            product = result.scalars().first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
            return ProductResponse.model_validate(product)


    @staticmethod
    async def delete(id: int, token_payload: dict) -> dict[str, str]:
        validate_admin_permissions(token_payload)
        async with new_session() as session:
            query = select(Product).where(Product.id == id)
            result = await session.execute(query)
            product = result.scalars().first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
            await session.delete(product)
            await session.commit()
            return {"msg": "Product deleted successfully"}


    @staticmethod
    async def edit_quantity_of_product_by_id(id: int, new_quantity: int, token_payload: dict) -> ProductResponse:
        validate_admin_permissions(token_payload)
        async with new_session() as session:
            query = select(Product).where(Product.id == id)
            result = await session.execute(query)
            product = result.scalars().first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
            product.quantity = new_quantity
            await session.commit()
            await session.refresh(product)
            return ProductResponse.model_validate(product)
