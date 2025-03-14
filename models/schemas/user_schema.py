from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr
from pydantic import Field


class UserBase(BaseModel):
    username: Annotated[str, Field(..., title='Имя пользователя', min_length=2, max_length=15)]
    email: Optional[Annotated[EmailStr, Field(title='Почта пользователя', examples=['anymail@gmail.com'])]] = None
    is_superuser: Annotated[bool, Field(title='Права суперпользователя')] = False
    password: Annotated[str, Field(..., title='Пароль пользователя')]


class UserDto(UserBase):
    pass


class UserResponse(UserBase):
    id: Annotated[int, Field(..., title='Id пользователя', ge=1)]

    class Config:
        from_attributes = True
