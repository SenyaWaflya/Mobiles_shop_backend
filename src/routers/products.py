from typing import Annotated

from fastapi import APIRouter, Form, Path, status

from src.schemas.products import ProductDto, ProductResponse
from src.services.products import ProductsService

router = APIRouter(prefix='/products', tags=['Products'])


@router.post('/', status_code=status.HTTP_201_CREATED, summary='Create Product')
async def create_product(
    brand: Annotated[str, Form(description='Фирма продукта', min_length=2, max_length=15, examples=['Apple'])],
    title: Annotated[str, Form(description='Название продукта', min_length=4, max_length=30, examples=['Iphone 16'])],
    price: Annotated[int, Form(description='Цена продукта', ge=0)],
    quantity: Annotated[int, Form(description='Количество имеющегося продукта', ge=0)],
) -> ProductResponse:
    product = ProductDto(brand=brand, title=title, price=price, quantity=quantity)
    return await ProductsService.create(product)


@router.get('/{product_id}', summary='Get Current Product')
async def get_product(product_id: Annotated[int, Path(description='ID продукта', ge=1)]) -> ProductResponse:
    return await ProductsService.get_product(product_id)


@router.get('/', summary='Get Products')
async def get_products() -> list[ProductResponse]:
    return await ProductsService.get_products()


@router.put('/{product_id}', summary='Edit Product')
async def edit_product(
    product_id: Annotated[int, Path(description='ID продукта', ge=1)],
    new_quantity: Annotated[int, Form(description='Новое количество продукта', ge=0)],
    new_price: Annotated[int, Form(description='Цена товара', ge=0)],
) -> ProductResponse:
    return await ProductsService.edit(product_id, new_quantity, new_price)


@router.delete('/{product_id}', summary='Delete Product')
async def delete_product(
    product_id: Annotated[int, Path(description='Id Продукта', ge=1)],
) -> ProductResponse:
    return await ProductsService.delete(product_id)
