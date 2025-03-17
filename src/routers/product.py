from fastapi import APIRouter, Path, Query, Form
from typing import Annotated

from src.schemas.product import ProductResponse, ProductDto
from src.services.product import ProductService


router = APIRouter(prefix='/products', tags=['Products'])

@router.get('/')
async def get_products() -> list[ProductResponse]:
    return await ProductService.get_all_products()


@router.get('/{id}')
async def get_current_product(id: Annotated[int, Path(description='ID продукта', ge=1)]) -> ProductResponse:
    return await ProductService.get_product_by_id(id)


@router.post('/')
async def create_product(
        title: Annotated[str, Form(description='Название продукта', min_length=4, max_length=30, examples=['Iphone 16'])],
        quantity: Annotated[int, Form(description='Количество имеющегося продукта', ge=0)]
) -> ProductResponse:
    product = ProductDto(
        title=title,
        quantity=quantity
    )
    return await ProductService.create(product)


@router.put('/{id}')
async def edit_quantity_of_product(
        id: Annotated[int, Path(description='ID продукта', ge=1)],
        new_quantity: Annotated[int, Query(description='Новое количество продукта', ge=0)]
) -> ProductResponse:
    return await ProductService.edit_quantity_of_product_by_id(id, new_quantity)


@router.delete('/{id}')
async def delete(id: Annotated[int, Path(description='Id Продукта', ge=1)]) -> ProductResponse:
    return await ProductService.delete_product(id)
