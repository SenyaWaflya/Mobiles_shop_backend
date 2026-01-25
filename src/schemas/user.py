from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: Annotated[str, Field(description='Имя пользователя', min_length=2, max_length=15, examples=['username'])]
    email: Annotated[EmailStr, Field(description='Почта пользователя', examples=['anymail@gmail.com'])]
    is_superuser: Annotated[bool, Field(description='Права суперпользователя')] = False
    is_owner: Annotated[bool, Field(description='Права владельца')] = False


class UserDto(UserBase):
    password: Annotated[str, Field(description='Пароль пользователя', min_length=8, examples=['secretPassword'])]


class UserResponse(UserBase):
    id: Annotated[int, Field(description='Id пользователя', ge=1)]

    class Config:
        from_attributes = True
