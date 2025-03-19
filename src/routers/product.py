from fastapi import APIRouter, status, Path, Query, Form, Depends
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
        quantity: Annotated[int, Form(description='Количество имеющегося продукта', ge=0)],
        token_payload: dict = Depends(get_auth_user)
) -> ProductResponse:
    product = ProductDto(title=title, quantity=quantity)
    return await ProductService.create(product, token_payload)


@router.put('/{id}', summary='Edit Quantity Of Product (authenticated admin)')
async def edit_quantity_of_product(
        id: Annotated[int, Path(description='ID продукта', ge=1)],
        new_quantity: Annotated[int, Query(description='Новое количество продукта', ge=0)],
        token_payload: dict = Depends(get_auth_user)
) -> ProductResponse:
    return await ProductService.edit_quantity_of_product_by_id(id, new_quantity, token_payload)


@router.delete('/{id}', summary='Delete Product (authenticated admin)')
async def delete_product(
        id: Annotated[int, Path(description='Id Продукта', ge=1)],
        token_payload: dict = Depends(get_auth_user)
) -> dict[str, str]:
    return await ProductService.delete(id, token_payload)
