from typing import Annotated
from pydantic import BaseModel
from pydantic import Field


class ProductBase(BaseModel):
    title: Annotated[str, Field(description='Название продукта', min_length=4, max_length=30, examples=['Iphone 16'])]
    price: Annotated[int, Field(description='Цена продукта', ge=0)]
    quantity: Annotated[int, Field(description='Количество имеющегося продукта', ge=0)]


class ProductDto(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: Annotated[int, Field(description='Id продукта', ge=1)]

    class Config:
        from_attributes = True
