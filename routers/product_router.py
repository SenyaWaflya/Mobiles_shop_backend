from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from typing import Annotated

from models.schemas.product_schema import ProductResponse, ProductDto
from routers.db_session import get_db
from services.product_service import get_all_products, create, get_product_by_id, delete_product, \
    edit_quantity_of_product_by_id

router = APIRouter()


@router.get('/products')
async def get_products(db: Session = Depends(get_db)) -> list[ProductResponse]:
    return get_all_products(db)


@router.get('/product/{id}')
async def get_current_product(
        id: Annotated[int, Path(..., title='Id продукта', ge=1)],
        db: Session = Depends(get_db)
) -> ProductResponse:
    return get_product_by_id(id, db)


@router.post('/product')
async def create_product(product: ProductDto, db: Session = Depends(get_db)) -> ProductResponse:
    return create(product, db)


@router.put('/product/{id}')
async def edit_quantity_of_product(
        id: Annotated[int, Path(..., title='Id продукта', ge=1)],
        new_quantity: Annotated[int, Query(..., title='Новое количество продукта')],
        db: Session = Depends(get_db)
) -> ProductResponse:
    return edit_quantity_of_product_by_id(id, new_quantity, db)


@router.delete('/product/{id}')
async def delete(
        id: Annotated[int, Path(..., title='Id Продукта', ge=1)],
        db: Session = Depends(get_db)
) -> ProductResponse:
    return delete_product(id, db)
