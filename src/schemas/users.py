from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    tg_id: Annotated[str, Field(description='ID пользователя в telegram', examples=['123456789'])]
    username: Annotated[str, Field(description='Имя пользователя', min_length=2, max_length=15, examples=['username'])]
    email: Annotated[EmailStr, Field(description='Почта пользователя', examples=['anymail@gmail.com'])]


class UserDto(UserBase):
    pass


class UserResponse(UserBase):
    id: Annotated[int, Field(description='Id пользователя', ge=1)]

    class Config:
        from_attributes = True
