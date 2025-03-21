from fastapi import APIRouter, status, Path, Form, Depends
from typing import Annotated

from src.auth.jwt import get_auth_user
from src.schemas.product import ProductResponse, ProductDto
from src.services.product import ProductService


router = APIRouter(prefix='/products', tags=['Products'])

@router.get('/', summary='Get Products (all)')
async def get_products() -> list[ProductResponse]:
    return await ProductService.get_all_products()


@router.get('/{id}', summary='Get Current Product (all)')
async def get_current_product(id: Annotated[int, Path(description='ID продукта', ge=1)]) -> ProductResponse:
    return await ProductService.get_product_by_id(id)


@router.post('/', status_code=status.HTTP_201_CREATED, summary='Create Product (authenticated admin)')
async def create_product(
        title: Annotated[str, Form(description='Название продукта', min_length=4, max_length=30, examples=['Iphone 16'])],
        price: Annotated[int, Form(description='Цена продукта', ge=0)],
        quantity: Annotated[int, Form(description='Количество имеющегося продукта', ge=0)],
        token_payload: dict = Depends(get_auth_user)
) -> ProductResponse:
    product = ProductDto(title=title, price=price, quantity=quantity)
    return await ProductService.create(product, token_payload)


@router.put('/{id}', summary='Edit Product (authenticated admin)')
async def edit_product(
        id: Annotated[int, Path(description='ID продукта', ge=1)],
        new_quantity: Annotated[int, Form(description='Новое количество продукта', ge=0)],
        new_price: Annotated[int, Form(description='Цена товара', ge=0)],
        token_payload: dict = Depends(get_auth_user)
) -> ProductResponse:
    return await ProductService.edit_product_by_id(id, new_quantity, new_price, token_payload)


@router.delete('/{id}', summary='Delete Product (authenticated admin)')
async def delete_product(
        id: Annotated[int, Path(description='Id Продукта', ge=1)],
        token_payload: dict = Depends(get_auth_user)
) -> dict[str, str]:
    return await ProductService.delete(id, token_payload)


@router.post('/{id}/favorites', status_code=status.HTTP_201_CREATED, summary='Append To Favorite (authenticated)')
async def append_to_favorite(
        id: Annotated[int, Path(description='Id Продукта', ge=1)],
        token_payload: dict = Depends(get_auth_user)
) -> ProductResponse:
    return await ProductService.append_favorite(id, token_payload)
