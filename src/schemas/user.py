from typing import Annotated
from pydantic import BaseModel, EmailStr
from pydantic import Field


class UserBase(BaseModel):
    username: Annotated[str, Field(title='Имя пользователя', min_length=2, max_length=15, examples=['username'])]
    email: Annotated[EmailStr, Field(title='Почта пользователя', examples=['anymail@gmail.com'])]
    is_superuser: Annotated[bool, Field(title='Права суперпользователя')] = False


class UserDto(UserBase):
    password: Annotated[str, Field(title='Пароль пользователя', min_length=8, examples=['secretPassword'])]


class UserResponse(UserBase):
    id: Annotated[int, Field(title='Id пользователя', ge=1)]

    class Config:
        from_attributes = True
