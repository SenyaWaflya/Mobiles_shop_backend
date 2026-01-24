from fastapi import  HTTPException, status
from sqlalchemy import select, and_

from src.database.database import new_session
from src.database.models import Product, UserProduct
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
                brand=product_dto.brand,
                title=product_dto.title,
                price=product_dto.price,
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
    async def edit_product_by_id(id: int, new_quantity: int, new_price: int, token_payload: dict) -> ProductResponse:
        validate_admin_permissions(token_payload)
        async with new_session() as session:
            query = select(Product).where(Product.id == id)
            result = await session.execute(query)
            product = result.scalars().first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
            product.quantity = new_quantity
            product.price = new_price
            await session.commit()
            await session.refresh(product)
            return ProductResponse.model_validate(product)


    @staticmethod
    async def append_favorite(product_id: int, token_payload: dict) -> ProductResponse:
        id = token_payload.get('sub')
        async with new_session() as session:
            product_query = select(Product).where(Product.id == product_id)
            product_result = await session.execute(product_query)
            product = product_result.scalars().first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
            favorite_exists_query = (
                select(UserProduct).where(and_(UserProduct.user_id == id, UserProduct.product_id == product_id))
            )
            favorite_exists_result = await session.execute(favorite_exists_query)
            favorite_exists = favorite_exists_result.scalars().first()
            if favorite_exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Product is already in favorites')
            favorite = UserProduct(
                user_id=id,
                product_id=product_id
            )
            session.add(favorite)
            await session.commit()
            await session.refresh(product)
            return product
