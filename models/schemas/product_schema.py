from typing import Annotated

from pydantic import BaseModel
from pydantic import Field


class ProductBase(BaseModel):
    title: Annotated[str, Field(..., title='Название продукта')]
    quantity: Annotated[int, Field(..., title='Количество имеющегося продукта')]


class ProductDto(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: Annotated[int, Field(..., title='Id продукта', ge=1)]

    class Config:
        from_attributes = True
