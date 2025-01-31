# from pydantic import BaseModel, Field
# from typing import Annotated
#
#
# class FavoriteBase(BaseModel):
#     product: Annotated[dict, Field(title='Список id продуктов, добавленных в избранное')]
#     author_id: Annotated[int, Field(title='Id пользователя, кому принадлежит данный список избранных продуктов', ge=1)]
#
#
# class FavoriteDto(FavoriteBase):
#     pass
#
#
# class FavoriteResponse(FavoriteBase):
#     id: Annotated[int, Field(title='Id списка избранных продуктов')]
#
#     class Config:
#         from_attributes = True
