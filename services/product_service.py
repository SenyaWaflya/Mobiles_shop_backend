from fastapi import  HTTPException, Depends
from sqlalchemy.orm import Session

from models.models import Product
from models.schemas.product_schema import ProductResponse, ProductDto
from routers.db_session import get_db


def get_all_products(db: Session = Depends(get_db)) -> list[ProductResponse]:
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail='No products found')
    return [ProductResponse.model_validate(product) for product in products]


def create(product: ProductDto, db: Session = Depends(get_db)) -> ProductResponse:
    db_product = Product(title=product.title, quantity=product.quantity)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_id(id: int, db: Session = Depends(get_db)) -> ProductResponse:
    db_product = db.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail='Product not found')
    return ProductResponse.model_validate(db_product)


def delete_product(id: int, db: Session = Depends(get_db)) -> ProductResponse:
    db_product = db.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail='Product not found')
    db.delete(db_product)
    db.commit()
    return ProductResponse.model_validate(db_product)


def edit_quantity_of_product_by_id(
        id: int,
        new_quantity: int,
        db: Session = Depends(get_db)
) -> ProductResponse:
    db_product = db.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail='Product not found')
    db_product.quantity = new_quantity
    db.commit()
    return ProductResponse.model_validate(db_product)
